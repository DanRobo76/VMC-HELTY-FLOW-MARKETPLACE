"""Avvio di Home Assistant per il simulatore e funzioni comuni (servizi, attese, sensori).

Rispetto al simulatore della b36 (stesso comportamento, piu' determinismo):
- nessun thread: i lavori che Home Assistant manderebbe in un executor (lettura TCP dei sensori,
  caricamento del YAML, import delle integrazioni) girano subito, nel thread del ciclo, e il loro
  risultato arriva al ciclo come un normale callback (EsecutoreSincrono). Con i thread l'istante
  reale in cui un lavoro finisce decideva in che punto della coda del ciclo entrava il risultato:
  allo stesso istante virtuale due giri potevano vedere eventi in ordine diverso;
- il package resta identico a quello installato (build_config.py): la chiave «recorder:» non avvia
  il registro e il sensore «platform: rest» non viene creato (vedi boot);
- block_async_io spento: i lavori «da executor» girano nel ciclo e non sono errori;
- il server http (caricato perche' notify dipende da repairs e repairs da http) non apre la porta 8123:
  nella b36 un secondo giro in parallelo trovava la porta occupata e l'avvio prendeva un'altra strada;
- integrazioni personalizzate (in <cfg>/custom_components, per esempio il motore nativo di una variante):
  si caricano come in Home Assistant, ma senza le dipendenze DIPENDENZE_TOLTE (frontend, http, ...);
- scarto dei «time change» stabile (_scarto_stabile): Home Assistant sposta ogni ascoltatore di un orario
  (trigger time_pattern e time, modelli con now() rinfrescati al secondo 0) di 50-500 ms presi da
  random.randint, nell'ordine in cui gli ascoltatori nascono. Con il seme fisso A contro A' coincide, ma una
  variante che crea gli ascoltatori in un altro ordine (o in numero diverso, o che usa random) si ritrova gli
  stessi scarti assegnati ad ascoltatori diversi e differenze di frazioni di secondo che non dicono niente.
  Qui lo scarto dipende solo dall'orario richiesto (ora, minuto, secondo, locale);
- aggancio delle varianti (runner.carica_variante): prima_dell_avvio(hass) prima di hass.async_run,
  avvia(hass) subito dopo l'avvio.
"""
import sys, os, asyncio, logging, selectors, socket, json, zlib, concurrent.futures, time as _t
import vclock
import fakevmc
from fakevmc import VMC
REAL = vclock._real_time
HASS = None
VARIANTE = None   # modulo della variante (boot): il suo aggancio facoltativo «servizio» per le chiamate degli scenari


class EsecutoreSincrono(concurrent.futures.ThreadPoolExecutor):
    """Executor senza thread: esegue il lavoro subito, in submit, e restituisce un Future gia' finito.
    asyncio.wrap_future consegna il risultato al ciclo con call_soon_threadsafe, cioe' in coda ai
    callback pronti nell'ordine in cui i lavori sono stati chiesti: l'ordine non dipende piu' dal tempo reale."""
    def __init__(self):
        super().__init__(max_workers=1)

    def submit(self, fn, /, *args, **kwargs):
        f = concurrent.futures.Future()
        try:
            r = fn(*args, **kwargs)
        except BaseException as e:   # noqa: BLE001 - come un thread: l'errore va nel Future
            f.set_exception(e)
        else:
            f.set_result(r)
        return f

    def shutdown(self, wait=True, *, cancel_futures=False):
        pass


def _esecutore():
    """SIM_ESECUTORE=thread rimette i thread della b36 (solo per provare che danno giri non ripetibili)."""
    if os.environ.get('SIM_ESECUTORE') == 'thread':
        return concurrent.futures.ThreadPoolExecutor(4)
    return EsecutoreSincrono()


def installa_esecutori(loop):
    loop._default_executor = _esecutore()
    if os.environ.get('SIM_ESECUTORE') == 'thread':
        return
    from homeassistant import core
    if not getattr(core.HomeAssistant.__init__, '_sim', False):
        orig = core.HomeAssistant.__init__
        def init(self, *a, **k):
            orig(self, *a, **k)
            self.import_executor = EsecutoreSincrono()
        init._sim = True
        core.HomeAssistant.__init__ = init


# dipendenze che un'integrazione personalizzata non porta nel simulatore (server web, interfaccia, avvisi:
# vorrebbero porte, thread e file; il manifest di vmc_master le dichiara)
DIPENDENZE_TOLTE = frozenset({'frontend', 'http', 'lovelace', 'repairs', 'onboarding', 'websocket_api', 'api',
                              'config', 'cloud', 'auth', 'person', 'zeroconf', 'ssdp', 'usb', 'bluetooth', 'dhcp'})


def _scarto_stabile(a, b):
    """Al posto di random.randint in homeassistant.helpers.event (e update_coordinator): scarto in [a, b]
    funzione dell'orario dell'ascoltatore (argomenti di async_track_utc_time_change) o del nome del
    coordinatore, non della posizione nella sequenza casuale. Due ascoltatori dello stesso orario scattano
    allo stesso istante, nell'ordine di registrazione (vclock.TimerOrdinato). SIM_SCARTI=casuali: come in
    Home Assistant (solo per provarne l'effetto, varianti/prova_casuale.py)."""
    f = sys._getframe(1)
    loc = f.f_locals
    if f.f_code.co_name == 'async_track_utc_time_change':
        chiave = ('orario', loc.get('hour'), loc.get('minute'), loc.get('second'), loc.get('local'))
    else:
        chiave = (f.f_code.co_name, loc.get('name'))
    return a + zlib.crc32(repr(chiave).encode()) % (b - a + 1)


async def _nessuna_piattaforma(*a, **k):
    return None


async def _niente(*a, **k):
    return None


def _spegni_parti_non_simulate():
    """Parti del package installato che il simulatore non puo' usare (restano nel file)."""
    from homeassistant import bootstrap, block_async_io
    block_async_io.enable = lambda: None
    if not getattr(bootstrap._get_domains, '_sim', False):
        orig = bootstrap._get_domains
        def get_domains(hass, config):
            d = orig(hass, config)
            d.discard('recorder')   # registro: niente database ne' thread; servizi recorder.* finti (sotto)
            return d
        get_domains._sim = True
        bootstrap._get_domains = get_domains
    # http (dipendenza di repairs, a sua volta dipendenza di notify) aprirebbe la porta 8123 vera: con due giri
    # in parallelo il secondo trova la porta occupata e segue un altro percorso di avvio. Il server resta
    # configurato ma non apre socket.
    if os.environ.get('SIM_HTTP') != 'vero':   # SIM_HTTP=vero: porta vera come nella b36 (solo per provarne l'effetto)
        from homeassistant.components.http import server as http_server
        http_server.HomeAssistantHTTP.async_bind = _niente
        http_server.HomeAssistantHTTP.start = _niente
        http_server.HomeAssistantHTTP.stop = _niente
    if os.environ.get('SIM_SCARTI') != 'casuali':
        from homeassistant.helpers import event as ev_helper, update_coordinator
        ev_helper.randint = _scarto_stabile
        update_coordinator.randint = _scarto_stabile
    from homeassistant.components.rest import sensor as rest_sensor   # versione del repository: niente rete
    rest_sensor.async_setup_platform = _nessuna_piattaforma
    # le integrazioni personalizzate (es. il motore nativo di una variante) non riportano dentro frontend, http
    # e le altre integrazioni tolte qui sotto: tolte dalle loro dipendenze dichiarate nel manifest
    from functools import cached_property
    from homeassistant import loader
    if not getattr(loader.Integration.dependencies, '_sim', False):
        def dipendenze(self):
            dip = self.manifest.get('dependencies', [])
            return dip if self.is_built_in else [d for d in dip if d not in DIPENDENZE_TOLTE]
        p = cached_property(dipendenze); p.__set_name__(loader.Integration, 'dependencies'); p._sim = True
        loader.Integration.dependencies = p


async def boot(cfg, variante=None, dopo_setup=None):
    """Avvia Home Assistant dalla cartella cfg. variante: modulo (runner.carica_variante) o None.
    dopo_setup(hass): chiamata appena creato hass, prima della variante e di hass.async_run
    (il runner ci aggancia la registrazione della traccia)."""
    global HASS, VARIANTE
    VARIANTE = variante
    from homeassistant import bootstrap, runner
    loop = asyncio.get_running_loop(); VMC.loop = loop
    fakevmc.install()
    installa_esecutori(loop)
    _spegni_parti_non_simulate()
    bootstrap.CRITICAL_INTEGRATIONS.clear(); bootstrap.FRONTEND_INTEGRATIONS.clear()
    bootstrap.STAGE_0_INTEGRATIONS = tuple(x for x in bootstrap.STAGE_0_INTEGRATIONS if x[0] in ('logging, http deps',))
    bootstrap.STAGE_1_INTEGRATIONS.clear()
    keep = {'automation','script','counter','input_boolean','input_button','input_datetime','input_number','input_select','input_text','timer','logger',
            'sensor','binary_sensor','button','switch','number','select','text','event','notify'}
    bootstrap.DEFAULT_INTEGRATIONS.clear(); bootstrap.DEFAULT_INTEGRATIONS.update(keep)
    bootstrap.LOGGING_AND_HTTP_DEPS_INTEGRATIONS.clear(); bootstrap.LOGGING_AND_HTTP_DEPS_INTEGRATIONS.update({'logger'})
    rc = runner.RuntimeConfig(config_dir=cfg, skip_pip=True, safe_mode=False, verbose=False,
        log_rotate_days=None, log_file=None, log_no_color=True, debug=False, open_ui=False)
    # nessuna scrittura su disco: lo stato di ogni scenario non deve contaminare i successivi
    import shutil
    shutil.rmtree(os.path.join(cfg, '.storage'), ignore_errors=True)
    from homeassistant.helpers import restore_state, storage
    async def _nodump(self, *a, **k): return None
    restore_state.RestoreStateData.async_dump_states = _nodump
    storage.Store._async_handle_write_data = _nodump
    hass = await bootstrap.async_setup_hass(rc)
    if hass is None:
        raise RuntimeError(f'Home Assistant non si avvia dalla cartella {cfg} (vedi {cfg}/home-assistant.log)')
    HASS = hass
    from homeassistant.core import SupportsResponse
    async def stats(call): return {}
    if not hass.services.has_service('recorder', 'get_statistics'):
        hass.services.async_register('recorder', 'get_statistics', stats, supports_response=SupportsResponse.ONLY)
    async def noop(call): return None
    if not hass.services.has_service('vmc_master', 'verifica_ip'):
        # come il servizio dell'integrazione (solo risposta): esito e ritardo scelti dallo scenario (VERIFICA_IP)
        hass.services.async_register('vmc_master', 'verifica_ip', _verifica_ip, supports_response=SupportsResponse.ONLY)
    for d, s in [('tts','speak'),('media_player','play_media'),('media_player','volume_set'),('tts','google_translate_say'),('notify','notify'),
                 ('tts','clear_cache'),('recorder','purge_entities')]:
        if not hass.services.has_service(d, s): hass.services.async_register(d, s, noop)
    # un riavvio vero fermerebbe il simulatore: la chiamata resta nella traccia, il servizio non fa niente
    hass.services.async_register('homeassistant', 'restart', noop)
    await _crea_utente(hass)
    if dopo_setup is not None: dopo_setup(hass)
    if variante is not None and hasattr(variante, 'prima_dell_avvio'):
        await variante.prima_dell_avvio(hass)
    asyncio.ensure_future(hass.async_run(attach_signals=False))
    await asyncio.sleep(1)
    from homeassistant.core import CoreState
    for _ in range(600):   # di solito gia' avviato dopo 1 s virtuale (come nella b36)
        if hass.state is CoreState.running: break
        await asyncio.sleep(1)
    if variante is not None and hasattr(variante, 'avvia'):
        await variante.avvia(hass)
    return hass

UTENTE = 'utente_simulatore'   # user_id dei contesti delle azioni di un utente (scheda, interfaccia di HA: runner)


async def _crea_utente(hass):
    """Utente amministratore con id UTENTE: le azioni della scheda (runner: 'ui', 'card_u', tasti degli script)
    hanno un Context con il suo user_id, come quelle del frontend. Con un utente che non esiste i servizi delle
    entita' (input_boolean.turn_on, automation.trigger...) rifiutano la chiamata (UnknownUser)."""
    if await hass.auth.async_get_user(UTENTE) is not None:
        return
    utente = await hass.auth.async_create_user('Simulatore', group_ids=['system-admin'])
    utenti = hass.auth._store._users   # id fisso al posto di quello casuale (uuid4)
    utenti.pop(utente.id)
    utente.id = UTENTE
    utenti[UTENTE] = utente


VERIFICA_IP = ['non_risponde', 0]   # esito e ritardo (s virtuali) del servizio finto vmc_master.verifica_ip


async def _verifica_ip(call):
    """Servizio finto vmc_master.verifica_ip (risposta come _async_verifica_ip dell'integrazione): non legge la
    rete, l'esito lo sceglie lo scenario (azione 'verifica_ip' del runner); di base nessuno risponde."""
    esito, ritardo = VERIFICA_IP
    if ritardo:
        await asyncio.sleep(ritardo)   # le due prove di lettura del nome sulla porta 5001
    nome = {'ok': call.data.get('nome') or 'Master', 'nome_diverso': 'Soggiorno'}.get(esito, '')
    return {'risponde': esito != 'non_risponde', 'nome': nome, 'esito': esito}


def aggiungi_telefono(nome, con_servizio=True):
    """Cellulare con l'app Home Assistant come lo crea l'integrazione Mobile App (senza avviarla): voce di
    configurazione, dispositivo con il nome del cellulare, device_tracker della piattaforma mobile_app (anche in
    entity_sources, letto da integration_entities('mobile_app')) e, con con_servizio, il servizio
    notify.mobile_app_<nome> finto (le chiamate restano nella traccia). Senza servizio: cellulare tolto
    dall'app ma ancora nell'elenco, la notifica non riesce."""
    from types import MappingProxyType
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers import device_registry as dr, entity_registry as er
    from homeassistant.helpers.entity import entity_sources
    from homeassistant.util import slugify
    slug = slugify(nome)
    voce = ConfigEntry(data={}, discovery_keys=MappingProxyType({}), domain='mobile_app', entry_id=f'sim_mobile_app_{slug}',
                       minor_version=1, options={}, source='registration', subentries_data=None, title=nome,
                       unique_id=f'sim_{slug}', version=1)
    HASS.config_entries._entries[voce.entry_id] = voce   # registrata senza avviare l'integrazione (niente http, webhook)
    disp = dr.async_get(HASS).async_get_or_create(config_entry_id=voce.entry_id, identifiers={('mobile_app', f'sim_{slug}')},
                                                  name=nome, manufacturer='Simulatore', model='Telefono')
    ent = er.async_get(HASS).async_get_or_create('device_tracker', 'mobile_app', f'sim_{slug}', suggested_object_id=slug,
                                                 config_entry=voce, device_id=disp.id)
    entity_sources(HASS)[ent.entity_id] = {'domain': 'mobile_app', 'custom_component': False, 'config_entry': voce.entry_id}
    HASS.states.async_set(ent.entity_id, 'home', {'source_type': 'gps', 'friendly_name': nome})
    if con_servizio:
        async def noop(call): return None
        HASS.services.async_register('notify', f'mobile_app_{slug}', noop)
    return ent.entity_id


def st(e):
    s = HASS.states.get(e); return s.state if s else None

async def svc(domain, service, data=None, blocking=True, context=None):
    """Servizio chiamato da uno scenario (preparazione, azioni dell'utente). Se la variante ha l'aggancio
    facoltativo «async servizio(hass, dominio, servizio, dati, blocking, contesto) -> bool» lo chiama per primo:
    True = la variante ha fatto la chiamata a modo suo (per esempio sulle entita' native di domani)."""
    if VARIANTE is not None and hasattr(VARIANTE, 'servizio') and await VARIANTE.servizio(
            HASS, domain, service, dict(data or {}), blocking, context):
        return
    await HASS.services.async_call(domain, service, data or {}, blocking=blocking, context=context)

async def wait(sec): await asyncio.sleep(sec)

def setsensor(eid, val, unit=None, dc=None):
    attrs = {}
    if unit: attrs['unit_of_measurement'] = unit
    if dc: attrs['device_class'] = dc; attrs['state_class'] = 'measurement'
    HASS.states.async_set(eid, str(val), attrs)

def fork_prepare_child():
    """Call in a forked child: new selector + self-pipe + executor."""
    loop = VMC.loop
    loop._selector = vclock.VSelector(loop, selectors.DefaultSelector())
    for sk in (loop._ssock, loop._csock):
        try: os.close(sk.detach())
        except Exception: pass
    loop._ssock, loop._csock = socket.socketpair()
    loop._ssock.setblocking(False); loop._csock.setblocking(False)
    loop._internal_fds += 1
    loop._add_reader(loop._ssock.fileno(), loop._read_from_self)
    loop._default_executor = _esecutore()
