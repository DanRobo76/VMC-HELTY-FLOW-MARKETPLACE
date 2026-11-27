"""Esecutore degli scenari: avvia Home Assistant una volta, poi un processo figlio (fork) per scenario.

Come il runner della b36, piu':
- traccia completa di ogni scenario (tracce.py): campo 'trz' del risultato (voci e attributi, compressi:
  tracce.decomprimi) e 't0' (istante virtuale dell'inizio della timeline);
- prima riga del file dei risultati con id '__avvio__': traccia dell'avvio e del riscaldamento
  (dall'avvio di Home Assistant al fork), con lo stato iniziale ('iniziale', subito dopo il setup
  delle integrazioni) e quello al fork ('finale') di tutte le entita' della VMC;
- varianti (carica_variante): prepara_configurazione(cfg) la usa differenziale.py; prima_dell_avvio(hass)
  e avvia(hass) li chiama simlib.boot; script(hass, entity_id, dati, contesto) la chiama do_action
  per l'azione 'script' (se restituisce True la chiamata script.turn_on non si fa);
- determinismo: seme di random fisso nel padre e in ogni figlio (dall'id dello scenario), executor
  senza thread (simlib.EsecutoreSincrono); PYTHONHASHSEED fisso lo impone assicura_determinismo().
"""
import sys, os, json, asyncio, time, traceback, pickle, random, zlib, importlib, importlib.util
import vclock, simlib, fakevmc, scen, tracce
from simlib import *
from tracce import TR
VMC = fakevmc.VMC
VARIANTE = None   # modulo della variante caricata (carica_variante)
UTENTE = simlib.UTENTE        # user_id dei contesti delle azioni fatte da un utente (scheda, interfaccia di HA)
CODA = 0          # secondi virtuali registrati nella traccia dopo la fine dello scenario ('end'), run_all(coda=...)
SEME = 20261125


def assicura_determinismo():
    """Rilancia il processo con PYTHONHASHSEED=0 se non e' gia' impostato: l'ordine di set e dict di
    stringhe (entity_id nei modelli, nei tracker...) deve essere lo stesso in ogni giro."""
    if os.environ.get('PYTHONHASHSEED') != '0':
        env = dict(os.environ, PYTHONHASHSEED='0')
        os.execve(sys.executable, [sys.executable] + sys.argv, env)


def carica_variante(spec):
    """Modulo della variante: nome di modulo importabile (es. varianti.identica, cercato anche nella cartella
    del simulatore) o percorso di un file .py. Puo' definire:
      prepara_configurazione(cfg_dir) -> None      modifica la configurazione generata (differenziale.py)
      async prima_dell_avvio(hass) -> None         facoltativa: dopo il setup, prima di hass.async_run
      async avvia(hass) -> None                    subito dopo l'avvio, prima del riscaldamento
      async script(hass, entity_id, dati, contesto) -> bool   facoltativa: azione 'script' degli scenari
    """
    global VARIANTE
    if spec is None:
        VARIANTE = None; return None
    if spec.endswith('.py') or os.sep in spec:
        nome = 'variante_' + os.path.splitext(os.path.basename(spec))[0]
        sp = importlib.util.spec_from_file_location(nome, os.path.abspath(spec))
        mod = importlib.util.module_from_spec(sp); sys.modules[nome] = mod; sp.loader.exec_module(mod)
    else:
        qui = os.path.dirname(os.path.abspath(__file__))
        if qui not in sys.path: sys.path.insert(0, qui)
        mod = importlib.import_module(spec)
    VARIANTE = mod
    return mod
CODE2SPEED = {f'000000{i}': i for i in range(8)}
SPEED_LABEL = {'Velocità 0':0,'Velocità 1':1,'Velocità 2':2,'Velocità 3':3,'Velocità 4':4,'Iperventilazione':5,'Notturna':6,'Free Cooling':7}

ALERT_SENS = dict(co2='sensor.vmc_master_alert_monitoraggio_co2', voc='sensor.vmc_master_alert_monitoraggio_voc', pdr='sensor.vmc_master_punto_di_rugiada_verifica_confronto',
    umid='sensor.vmc_master_alert_monitoraggio_umidita', cong='sensor.vmc_master_congelamento_verifica_soglia', delta='sensor.vmc_master_delta_temp_verifica_soglia',
    free='sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi', ip='sensor.vmc_master_status_ip_interfaccia')
class Rec:
    def __init__(self): self.reset()
    def reset(self):
        self.seen = []   # (t, speed) HA readback of status_ventola_memorizzata
        self.events = [] # (t, kind, data)
        self.trig = []
        self.raw = []    # (t, campo [1] del sensore grezzo sensor.vmc_master_status_ventola, o il suo stato se non valido)
        self.ip = []     # (t, stato di sensor.vmc_master_status_ip_interfaccia): quando HA vede la VMC ON-Line / OFF-Line
REC = Rec()

def install_patch():
    from homeassistant.components.automation import entity as aent
    orig = aent.AutomationEntity._async_trigger_if_enabled
    async def patched(self, run_variables, context=None, skip_condition=False):
        if self.entity_id == 'automation.automazione_vmc_master':
            tr = run_variables.get('trigger', {})
            REC.trig.append((vclock._V[0], str(tr.get('id'))))
        return await orig(self, run_variables, context, skip_condition)
    aent.AutomationEntity._async_trigger_if_enabled = patched

def install_listeners(hass):
    from homeassistant.core import callback
    from homeassistant.helpers.event import async_track_state_change_event
    @callback
    def on_status(ev):
        ns = ev.data.get('new_state')
        if ns is None: return
        parts = ns.state.split(',')
        if len(parts) > 1 and parts[1] in ('00000','00001','00002','00003','00004','00005','00006','00007'):
            REC.seen.append((vclock._V[0], int(parts[1])))
    async_track_state_change_event(hass, ['sensor.vmc_master_status_ventola_memorizzata'], on_status)
    @callback
    def on_raw(ev):       # (aggiunto 21-11-2026 per la b36 578aeff, solo registrazione) letture grezze e rete viste da HA
        ns = ev.data.get('new_state')
        if ns is None: return
        if ev.data.get('entity_id') == 'sensor.vmc_master_status_ventola':
            parts = ns.state.split(',')
            REC.raw.append((vclock._V[0], parts[1] if len(parts) > 1 else ns.state))
        else:
            REC.ip.append((vclock._V[0], ns.state))
    # ascolto diretto del bus (non con async_track_state_change_event: aggiungere un tracker per entita' cambia l'ordine
    # di due trigger dell'automazione allo stesso istante)
    RAW_IDS = ('sensor.vmc_master_status_ventola', 'sensor.vmc_master_status_ip_interfaccia')
    hass.bus.async_listen('state_changed', on_raw, event_filter=callback(lambda d: d.get('entity_id') in RAW_IDS))
    @callback
    def on_trig(ev):
        if ev.data.get('entity_id') == 'automation.automazione_vmc_master':
            REC.trig.append((vclock._V[0], str(ev.data.get('source'))[:160]))


async def do_action(a):
    k = a[0]
    if k == 'env': scen.env(**a[1])
    elif k == 'voc':
        VMC.sens['voc'] = a[1]
        if VMC.online: await svc('homeassistant','update_entity',{'entity_id':'sensor.vmc_master_sensori'})
        else:   # VMC spenta: il nuovo valore VOC viene letto alla prima lettura dopo il ritorno della corrente
            VMC.voc_dirty = True
            def _upd():
                VMC.voc_dirty = False
                simlib.HASS.async_create_task(svc('homeassistant','update_entity',{'entity_id':'sensor.vmc_master_sensori'}))
            VMC.on_voc_dirty = _upd
    elif k == 'online':
        VMC.power(a[1])
    elif k == 'press':      # telecomando / app: VMC changes immediately
        if VMC.online: VMC.set_speed(a[1], 'user')
        REC.events.append((vclock._V[0], 'press', a[1]))
    elif k == 'card':       # card button -> shell_command by the user
        REC.events.append((vclock._V[0], 'press', a[1]))
        VMC.user_cmd = True
        await svc('shell_command', scen.SPEED_SVC[a[1]], {}, blocking=False)
    elif k == 'card_u':     # (aggiunto 21-11-2026) tasto della scheda/Telecomando di HA premuto da un utente: shell_command
        REC.events.append((vclock._V[0], 'press', a[1]))   # con Context(user_id) non vuoto, come in HA vero
        VMC.user_cmd = True
        from homeassistant.core import Context
        await svc('shell_command', scen.SPEED_SVC[a[1]], {}, blocking=False, context=Context(user_id=UTENTE))
    elif k == 'switch':
        await svc('input_boolean', 'turn_on' if a[2] else 'turn_off', {'entity_id': a[1]}, blocking=False)
        REC.events.append((vclock._V[0], 'switch', a[1], a[2]))
    elif k == 'select':
        await svc('input_select','select_option',{'entity_id':a[1],'option':a[2]})
    elif k == 'number':
        await svc('input_number','set_value',{'entity_id':a[1],'value':a[2]})
    elif k == 'datetime':
        await svc('input_datetime','set_datetime',{'entity_id':a[1],'time':a[2]})
    elif k == 'script':     # ('script', entity_id[, dati[, utente]]): utente=True come un tasto della scheda (Context con user_id)
        REC.events.append((vclock._V[0], 'script', a[1]))
        from homeassistant.core import Context
        dati = dict(a[2]) if len(a) > 2 and a[2] else {}
        # lo stesso contesto che async_call creerebbe senza contesto, o quello di un utente della scheda
        ctx = Context(user_id=UTENTE) if len(a) > 3 and a[3] else Context()
        if VARIANTE is not None and hasattr(VARIANTE, 'script') and await VARIANTE.script(simlib.HASS, a[1], dati, ctx):
            pass          # la variante ha eseguito lo script (motore nativo)
        else:
            dati_turn_on = {'entity_id': a[1]}
            if dati: dati_turn_on['variables'] = dati
            await simlib.HASS.services.async_call('script', 'turn_on', dati_turn_on, blocking=False, context=ctx)
    elif k == 'ui':         # ('ui', dominio, servizio, dati): azione della scheda o dell'interfaccia di HA fatta da un utente
        REC.events.append((vclock._V[0], 'ui', a[1], a[2]))
        from homeassistant.core import Context
        await svc(a[1], a[2], dict(a[3]), blocking=False, context=Context(user_id=UTENTE))
    elif k == 'stato':      # ('stato', entity_id, stato, attributi): entita' esterna al package (media player, sensore di un'altra VMC...)
        simlib.HASS.states.async_set(a[1], a[2], dict(a[3]) if len(a) > 3 else {})
    elif k == 'telefono':   # ('telefono', nome[, con_servizio]): cellulare con l'app Home Assistant (integrazione Mobile App)
        simlib.aggiungi_telefono(a[1], a[2] if len(a) > 2 else True)
    elif k == 'verifica_ip':   # ('verifica_ip', esito[, ritardo]): risposta del servizio finto vmc_master.verifica_ip
        simlib.VERIFICA_IP[:] = [a[1], a[2] if len(a) > 2 else 0]
    elif k == 'attendi': await wait(a[1])
    elif k == 'latency': VMC.latency = a[1]
    elif k == 'mute': VMC.mute = a[1]
    elif k == 'resume': VMC.resume = a[1]
    elif k == 'mark': REC.events.append((vclock._V[0], 'mark', a[1]))
    else: raise ValueError(a)

async def run_scenario(sc):
    """sc: dict(id, setup=[actions], timeline=[(t, action)], end=T, checks=[(t, name)])"""
    VMC.log.clear(); REC.reset(); TR.reset(); fakevmc.SHELL_LOG.clear()
    for a in sc.get('setup', []): await do_action(a)
    await wait(sc.get('settle', 90))
    if sc.get('align_minute'):
        now = vclock.vtime(); nxt = (int(now // 60) + 1) * 60 + 1
        await wait(nxt - now)
    t0 = vclock._V[0]
    for a in sc.get('setup_t0', []):   # actions needing t0 (calendar times relative to t0)
        if a[0] == 'datetime_min':
            import datetime as _d
            from homeassistant.util import dt as dtu
            ts = vclock.START_EPOCH[0] + t0 - 1 + 60 * a[2]
            loc = _d.datetime.fromtimestamp(ts, dtu.DEFAULT_TIME_ZONE)
            await svc('input_datetime','set_datetime',{'entity_id':a[1],'time':loc.strftime('%H:%M:00')})
        else:
            await do_action(a)
    VMC.log.clear(); REC.reset()
    REC.seen.append((t0, VMC.speed))
    snaps = {}
    tl = sorted(sc['timeline'] + [(t, ('snap', n)) for t, n in sc.get('checks', [])], key=lambda x: x[0])
    for t, a in tl:
        now = vclock._V[0] - t0
        if t > now: await wait(t - now)
        if a[0] == 'snap':
            snaps[a[1]] = (VMC.speed, VMC.online, {k: st(v) for k, v in ALERT_SENS.items()})
        else:
            await do_action(a)
    now = vclock._V[0] - t0
    if sc['end'] > now: await wait(sc['end'] - now)
    snaps['final'] = (VMC.speed, VMC.online)
    rel = lambda t: round(t - t0, 2)
    res = dict(id=sc['id'], t0=round(t0, 6), snaps=snaps,
                log=[(rel(l[0]),) + tuple(l[1:]) for l in VMC.log],
                seen=[(rel(t), s) for t, s in REC.seen], events=[(rel(e[0]),) + tuple(e[1:]) for e in REC.events], trig=[(rel(t), s) for t, s in REC.trig],
                raw=[(rel(t), s) for t, s in REC.raw], ip=[(rel(t), s) for t, s in REC.ip])
    if CODA > 0:   # solo per la traccia: i campi del runner sopra restano quelli fino a 'end'
        await wait(CODA); res['coda'] = CODA
    tr, attr = TR.esporta(t0)
    res['trz'] = tracce.comprimi(dict(tr=tr, attr=attr))
    return res

def child(sc, wfd):
    try:
        fork_prepare_child()
        random.seed(zlib.crc32(sc['id'].encode('utf-8')) ^ SEME)
        loop = VMC.loop
        res = loop.run_until_complete(run_scenario(sc))
    except BaseException as e:
        res = dict(id=sc['id'], error=traceback.format_exc()[-2000:])
    data = json.dumps(res).encode()
    with os.fdopen(wfd, 'wb') as f: f.write(data)
    os._exit(0)

ID_AVVIO = '__avvio__'

def run_all(scenarios, out_path, nproc=4, cfg='cfg', variante=None, coda=0):
    """variante: nome o percorso del modulo (carica_variante) o None (nessuna variante: come la b36).
    coda: secondi virtuali in piu' dopo 'end' registrati solo nella traccia (comandi o cambi di stato in
    ritardo che altrimenti resterebbero fuori dal confronto)."""
    global CODA
    CODA = coda
    import logging
    logging.disable(logging.CRITICAL)
    random.seed(SEME)
    var = carica_variante(variante) if isinstance(variante, str) else variante
    globals()['VARIANTE'] = var
    loop = vclock.VLoop(); asyncio.set_event_loop(loop)
    simlib.installa_esecutori(loop)
    avvio = {}
    def dopo_setup(hass):
        TR.reset(); fakevmc.EVENTI = TR.ev
        TR.installa(hass)
        avvio['iniziale'] = TR.istantanea(hass)
    async def warm():
        install_patch()
        hass = await boot(cfg, var, dopo_setup)
        install_listeners(hass)
        await scen.base_setup()
        await wait(300)
        avvio['finale'] = TR.istantanea(hass)
        tr, attr = TR.esporta(0.0)
        usati = {x[2] for x in avvio['iniziale'] + avvio['finale']}   # istantanee: [entity_id, stato, attr]
        attr.update({d: json.loads(TR.attr[d]) for d in usati})
        dati = dict(tr=tr, attr=dict(sorted(attr.items())), iniziale=avvio.pop('iniziale'), finale=avvio.pop('finale'))
        avvio.update(id=ID_AVVIO, t0=round(vclock._V[0], 6), trz=tracce.comprimi(dati),
                     variante=getattr(var, '__name__', None), cfg=os.path.abspath(cfg))
    t_boot = vclock._real_time()
    try:
        loop.run_until_complete(warm())
    except BaseException:
        # Home Assistant manda le eccezioni non gestite nel suo log (spento): l'errore va stampato qui
        traceback.print_exc(); sys.stderr.flush()
        raise SystemExit(f'avvio o riscaldamento non riuscito (cfg {cfg}, variante {variante})')
    sys.excepthook = sys.__excepthook__
    done_ids = set()
    if os.path.exists(out_path):
        for line in open(out_path):
            try: done_ids.add(json.loads(line)['id'])
            except Exception: pass
    todo = [s for s in scenarios if s['id'] not in done_ids]
    print(f'warm ok ({vclock._real_time() - t_boot:.0f} s); todo {len(todo)} (done {len(done_ids)})', flush=True)
    out = open(out_path, 'a')
    if ID_AVVIO not in done_ids:
        avvio['real_s'] = round(vclock._real_time() - t_boot, 2)
        out.write(json.dumps(avvio) + '\n'); out.flush()
    running = {}  # pid -> (sc, rfd, start)
    i = 0; t_start = vclock._real_time(); n_done = 0
    import select as _sel
    while i < len(todo) or running:
        while i < len(todo) and len(running) < nproc:
            sc = todo[i]; i += 1
            r, w = os.pipe()
            pid = os.fork()
            if pid == 0:
                os.close(r); child(sc, w)
            os.close(w)
            running[pid] = (sc, r, vclock._real_time(), [])
        # read pipes
        fds = {v[1]: pid for pid, v in running.items()}
        rl, _, _ = _sel.select(list(fds), [], [], 1.0)
        for fd in rl:
            pid = fds[fd]
            chunk = os.read(fd, 1 << 20)
            if chunk: running[pid][3].append(chunk); continue
            os.close(fd); os.waitpid(pid, 0)
            sc, _, st0, chunks = running.pop(pid)
            try: res = json.loads(b''.join(chunks))
            except Exception: res = dict(id=sc['id'], error='no output')
            res['real_s'] = round(vclock._real_time() - st0, 2)
            out.write(json.dumps(res) + '\n'); out.flush(); n_done += 1
            if n_done % 200 == 0:
                el = vclock._real_time() - t_start
                print(f'{n_done}/{len(todo)} in {el:.0f}s, eta {el/n_done*(len(todo)-n_done)/60:.0f} min', flush=True)
        # timeouts
        for pid, v in list(running.items()):
            if vclock._real_time() - v[2] > 600:
                os.kill(pid, 9)
    out.close()
