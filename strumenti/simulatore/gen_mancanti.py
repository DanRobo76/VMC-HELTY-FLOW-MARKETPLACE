"""Famiglia M: scenari per le automazioni, gli script e i rami che gli scenari di gen.py non eseguono mai.

copertura.py sui 17.264 scenari fissi (famiglie S, P, F, C, W, K, R) da' mai eseguite 5 automazioni su 14
(audio_allerte_e_stato, cambio_ip_vmc_riavvio_di_h_a, esclusivita_finestre_opzioni, riepilogo_audio_avvio,
ripartenza_della_vmc) piu' 2 solo nell'avvio (inizializza_tempi_di_attesa, riallineamento_allerte_al_riavvio),
e 37 script su 51 (audio, notifiche, profili, pulizia, reset_filtro_vmc, upgrade_sensors) piu' 1 solo
nell'avvio (ripristina_tempi_attesa). Qui ogni scenario fa quello che fa l'utente o la casa:

- AUD  avvisi audio: media player scelto nella scheda, Profilo Audio, poi un'allerta (inizio e fine) o un cambio
       di velocita'; rami: audio spento, nessun media player, fuori fascia oraria, fascia oltre la mezzanotte
       (dentro e fuori), categoria spenta;
- RIE  riepilogo audio dell'avvio: «Esegui azioni» dell'automazione dall'interfaccia (automation.trigger con le
       condizioni) con un'allerta in corso o no, a VMC OFF-Line, con audio o riepilogo spenti, e la spia
       dell'avvio rimasta accesa 10 minuti (secondo trigger dell'automazione);
- RIA  riallineamento delle allerte al riavvio (automation.trigger: le sue 4 fasi in 200 s) con un'allerta che
       inizia durante la fase 1;
- INI  inizializzazione dei tempi di attesa: automation.trigger (con e senza condizioni) e
       vmc_master_attese_inizializzate spento;
- IP   Cambio IP VMC: IP scritto nel campo della scheda (non valido, uguale, di un'altra VMC, valido con le
       risposte del servizio vmc_master.verifica_ip finto: ok, non_risponde, altro_dispositivo, nome_diverso,
       IP cambiato durante la verifica);
- FIN / UI  finestre e pannelli della scheda (input_boolean) aperti e chiusi;
- NOT  notifiche al cellulare: cellulare dell'app (integrazione Mobile App simulata, simlib.aggiungi_telefono)
       scelto o no, cambi di velocita', sensori scelti non disponibili, cellulare tolto, servizio di notifica
       mancante, notifiche senza chiamante nel package (Cambio Filtro alle 08:00, Errore Media Player) dallo
       script;
- PUL  pulizia della cronologia (conferma Si / No) e della cache audio;
- PRO  profili e tasti della scheda (Profilo Inizializzazione, Calendario, Free, PdR, Umidita', Audio, Azzera
       Offset, Azzera Aria Scambiata, Reset Filtro, Agg. Sensori);
- VAR  Rinomina VMC, nuova versione nel repository (sensore rest, qui scritto dallo scenario), scelta dei
       sensori;
- RIP  ripartenza della VMC: taglio della corrente piu' breve del Black-Out, la VMC riparte a Velocita' 1.

Uso: gen_mancanti.famiglia() -> lista di scenari nel formato di gen.py (targeted.scegli li aggiunge a quelli di
gen.all_scenarios, quindi «^M\\|» li sceglie tutti).
"""
import alerts
from alerts import A_OFF, A_ON

IB = 'input_boolean.vmc_master_'
MP = 'media_player.sim_cucina'
SEL_MP = 'input_select.vmc_master_selected_media_player_entity'
SEL_TEL = 'input_select.vmc_master_selected_notification_device'
AGG_MP = 'script.vmc_master_aggiorna_elenco_entita_media_player'
AGG_TEL = 'script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo'
TEL = 'Telefono Simulatore'            # slugify -> telefono_simulatore (servizio notify.mobile_app_telefono_simulatore)
TEL_SLUG = 'telefono_simulatore'
TRACKER = 'device_tracker.' + TEL_SLUG
NOTIFICA = IB + 'notifica_status_vmc'
AUDIO = IB + 'notifica_audio'
INIZIO_AUDIO = 'input_datetime.vmc_master_audio_start_time'
FINE_AUDIO = 'input_datetime.vmc_master_audio_end_time'
AUTO = 'automation.vmc_master_'
SC = 'script.vmc_master_'
SENSORI = {'te': 'sensor.sim_te', 'ti': 'sensor.sim_ti', 'ue': 'sensor.sim_ue', 'ui': 'sensor.sim_ui', 'co2': 'sensor.sim_co2'}

# allerte (inizio, fine) oltre a quelle di alerts.py: congelamento e Δ Temp. «[No ma Prossimo]»
ON = {**A_ON, 'CONGP': [('env', {'te': -16.0})], 'DELTAP': [('env', {'te': -1.0})]}
OFF = {**A_OFF, 'CONGP': [('env', {'te': 10.0})], 'DELTAP': [('env', {'te': 10.0})]}


def ui(dominio, servizio, **dati):
    return ('ui', dominio, servizio, dati)


def acceso(entita):
    return ui('input_boolean', 'turn_on', entity_id=entita)


def spento(entita):
    return ui('input_boolean', 'turn_off', entity_id=entita)


def tasto(script, **dati):
    """Tasto della scheda che lancia uno script (script.turn_on con il contesto dell'utente)."""
    return ('script', script, dati, True)


def esegui(automazione, condizioni=True):
    """«Esegui azioni» di un'automazione dall'interfaccia di Home Assistant (automation.trigger)."""
    return ui('automation', 'trigger', entity_id=automazione, skip_condition=not condizioni)


def orario(entita, hhmm):
    return ui('input_datetime', 'set_datetime', entity_id=entita, time=hhmm + ':00')


def scenario(id_, s0=1, setup=(), timeline=(), end=300, **extra):
    sc = {'id': 'M|' + id_, 'setup': [('latency', 0.5), ('press', s0)] + list(setup), 'timeline': list(timeline),
          'checks': [], 'end': end, 'meta': {'fam': 'M', 's0': s0, 'vmc': 'F', 'alerts': [], 'presses': []}}
    sc.update(extra)
    return sc


def allerta(a, t_on, t_off):
    return [(t_on, x) for x in ON[a]] + ([(t_off, x) for x in OFF[a]] if t_off is not None else [])


def setup_media_player(profilo=True):
    """Media player in casa, elenco aggiornato e media player scelto nella scheda; poi il Profilo Audio
    (audio acceso, fascia 08:00-21:00, volume 0,30, tutte le categorie)."""
    s = [('stato', MP, 'idle', {'friendly_name': 'Cucina', 'volume_level': 0.4}), tasto(AGG_MP), ('attendi', 7),
         ui('input_select', 'select_option', entity_id=SEL_MP, option=MP), ('attendi', 7)]
    if profilo:
        s += [tasto(SC + 'audio_profilo'), ('attendi', 3)]
    return s


def setup_telefono(con_servizio=True):
    """Cellulare con l'app Home Assistant, elenco aggiornato e cellulare scelto nella scheda."""
    return [('telefono', TEL, con_servizio), tasto(AGG_TEL), ('attendi', 7),
            ui('input_select', 'select_option', entity_id=SEL_TEL, option=TEL_SLUG), ('attendi', 7)]


def free(mode):
    """Allerta Free Heating (H) / Free Cooling (C) come la famiglia F: setup e timeline (10 s sfavorevole,
    200 s favorevole)."""
    return alerts.free_setup(mode), [(10, x) for x in alerts.FREE_UNFAV[mode]] + [(200, x) for x in alerts.FREE_FAV[mode]]


def fam_audio():
    out = []
    # ogni allerta (inizio a 10 s, fine a 200 s) e i cambi di velocita' con l'audio tutto acceso
    for a in ['CO2', 'VOC', 'PDR', 'UMIDA', 'UMIDS', 'CONG', 'CONGP', 'DELTA', 'DELTAP', 'BO']:
        out.append(scenario(f'AUD|{a}|-', setup=setup_media_player(), timeline=allerta(a, 10, 200), end=330))
    for mode in 'HC':
        fs, ft = free(mode)
        out.append(scenario(f'AUD|FREE{mode}|-', setup=fs + setup_media_player(), timeline=ft, end=330))
    vel = [(10, ('press', 3)), (60, ('press', 0)), (120, ('card_u', 2)), (180, ('press', 6))]
    out.append(scenario('AUD|VEL|-', setup=setup_media_player(), timeline=vel, end=300))
    # rami delle condizioni: audio spento, nessun media player, fuori fascia, fascia oltre la mezzanotte, categoria spenta
    rami = {
        'SPENTO': setup_media_player() + [spento(AUDIO)],
        'NO_MP': [tasto(SC + 'audio_profilo'), ('attendi', 3)],
        'FUORI': setup_media_player() + [orario(INIZIO_AUDIO, '11:00'), orario(FINE_AUDIO, '12:00')],
        'NOTTE': setup_media_player() + [orario(INIZIO_AUDIO, '20:00'), orario(FINE_AUDIO, '10:45')],
        'NOTTE_FUORI': setup_media_player() + [orario(INIZIO_AUDIO, '20:00'), orario(FINE_AUDIO, '09:00')],
        'CATEGORIA': setup_media_player() + [spento(IB + 'notifica_allerta_inquinanti'),
                                             spento(IB + 'notifica_allerta_status_velocita')],
        'VOLUME': setup_media_player() + [ui('input_number', 'set_value', entity_id='input_number.vmc_master_audio_volume', value=0.75)],
    }
    for nome, s in rami.items():
        out.append(scenario(f'AUD|CO2|{nome}', setup=s, timeline=allerta('CO2', 10, 200), end=330))
        out.append(scenario(f'AUD|VEL|{nome}', setup=s, timeline=vel, end=300))
    return out


def fam_riepilogo():
    out = []
    rie = AUTO + 'riepilogo_audio_avvio'
    for a in ['NONE', 'CO2', 'VOC', 'PDR', 'UMIDA', 'CONG', 'CONGP', 'DELTA', 'DELTAP', 'BO', 'FREEH']:
        setup = setup_media_player(); tl = []
        if a == 'FREEH':
            fs, ft = free('H'); setup = fs + setup; tl = [x for x in ft if x[0] == 10]
        elif a != 'NONE':
            tl = allerta(a, 10, 280)
        out.append(scenario(f'RIE|{a}', setup=setup, timeline=tl + [(130, esegui(rie))], end=330))
    # allerta CO2 che inizia durante il riepilogo (la spia dell'avvio e' accesa: niente avviso audio subito)
    out.append(scenario('RIE|CO2_DURANTE', setup=setup_media_player(), timeline=[(10, esegui(rie))] + allerta('CO2', 15, 200),
                        end=330))
    # condizioni non vere: audio spento, riepilogo spento; senza condizioni ma senza media player
    out.append(scenario('RIE|SPENTO', setup=setup_media_player() + [spento(AUDIO)], timeline=[(10, esegui(rie))], end=150))
    out.append(scenario('RIE|SENZA_RIEPILOGO', setup=setup_media_player() + [spento(IB + 'notifica_allerta_riepilogo')],
                        timeline=[(10, esegui(rie))], end=150))
    out.append(scenario('RIE|SENZA_CONDIZIONI', setup=[], timeline=[(10, esegui(rie, condizioni=False))], end=150))
    # riepilogo interrotto: spia dell'audio all'avvio rimasta accesa 10 minuti
    out.append(scenario('RIE|SPIA', setup=[], timeline=[(10, acceso(IB + 'avvio_home_assistant_in_corso_per_audio'))], end=640))
    return out


def fam_riallineamento():
    out = []
    ria = AUTO + 'riallineamento_allerte_al_riavvio'
    for a in ['NONE', 'CO2', 'VOC', 'PDR', 'UMIDA', 'CONG', 'DELTA', 'BO', 'FREEH']:
        setup = []; tl = [(10, esegui(ria))]
        if a == 'FREEH':
            fs, ft = free('H'); setup = fs; tl += [(20, x) for _, x in ft[:1]] + [(260, x) for _, x in ft[1:]]
        elif a == 'BO':
            tl += allerta(a, 20, 120)
        elif a != 'NONE':
            tl += allerta(a, 20, 260)
        out.append(scenario(f'RIA|{a}', s0=2, setup=setup, timeline=tl, end=380))
    return out


def fam_inizializza():
    ini = AUTO + 'inizializza_tempi_di_attesa'
    cambia = ui('input_number', 'set_value', entity_id='input_number.vmc_master_attesa_pdr_cambio', value=30)
    return [
        scenario('INI|ESEGUI', setup=[cambia], timeline=[(10, esegui(ini, condizioni=False))], end=90),
        scenario('INI|CONDIZIONI', setup=[cambia], timeline=[(10, esegui(ini))], end=90),
        scenario('INI|SPENTO', setup=[cambia], timeline=[(10, spento(IB + 'attese_inizializzate'))], end=90),
    ]


def fam_cambio_ip():
    out = []
    campo = 'input_text.vmc_master_ip_insert'
    scrivi = lambda ip: ui('input_text', 'set_value', entity_id=campo, value=ip)
    for nome, ip in [('NON_VALIDO', '192.168.1.300'), ('LOOPBACK', '127.0.0.1'), ('LINK_LOCAL', '169.254.3.4'),
                     ('ZERI', '192.168.01.5'), ('TESTO', 'vmc'), ('STESSO', '192.168.1.160')]:
        out.append(scenario(f'IP|{nome}', timeline=[(10, scrivi(ip))], end=90))
    out.append(scenario('IP|ALTRA_VMC', setup=[('stato', 'sensor.vmc_soggiorno_ip', '192.168.1.161', {'friendly_name': 'IP'})],
                        timeline=[(10, scrivi('192.168.1.161'))], end=90))
    for esito in ['ok', 'non_risponde', 'altro_dispositivo', 'nome_diverso']:
        out.append(scenario(f'IP|{esito.upper()}', setup=[('verifica_ip', esito, 2)], timeline=[(10, scrivi(' 192.168.1.170 '))],
                            end=90))
    # un secondo IP scritto durante la verifica del primo: il primo non riavvia, il secondo (in coda) si'
    out.append(scenario('IP|CODA', setup=[('verifica_ip', 'ok', 3)], timeline=[(10, scrivi('192.168.1.170')),
                                                                              (11, scrivi('192.168.1.171'))], end=90))
    # VMC OFF-Line: nome non letto, la verifica parte con il nome vuoto
    out.append(scenario('IP|OK_OFFLINE', setup=[('verifica_ip', 'ok', 2)],
                        timeline=[(10, ('online', False)), (60, scrivi('192.168.1.170')), (120, ('online', True))], end=220))
    return out


FINESTRE = ['opzioni_vmc', 'opzioni_monitoraggio_sensori', 'opzioni_interruttore_offset_sensori',
            'opzioni_interruttore_monitoraggio_sensori_extra', 'opzioni_interruttore_sensori_vmc_interni',
            'opzioni_interruttore_calendario', 'opzioni_offset_sensori', 'opzioni_punto_di_rugiada', 'opzioni_calendario_main',
            'opzioni_calendario', 'opzioni_free_heating_o_free_cooling', 'opzioni_avvisi', 'opzioni_lettura_sensori',
            'opzioni_scelta_sensori', 'opzioni_elementi_chimici', 'opzione_finestra_audio', 'opzione_finestra_prossime_letture',
            'opzione_finestra_tempi_attesa']


def fam_finestre():
    out = []
    for f in FINESTRE:
        out.append(scenario(f'UI|{f}', timeline=[(10, acceso(IB + f)), (40, spento(IB + f))], end=100))
    # esclusivita': la finestra Timer Lettura Dati VMC e le finestre Extra, VMC Interni, Offset; il pannello Sensori
    sens = ['opzioni_interruttore_monitoraggio_sensori_extra', 'opzioni_interruttore_sensori_vmc_interni',
            'opzioni_interruttore_offset_sensori']
    tl = [(10, acceso(IB + 'opzioni_monitoraggio_sensori'))]
    tl += [(15 + 5 * i, acceso(IB + f)) for i, f in enumerate(sens)]
    tl += [(35, acceso(IB + 'opzione_finestra_prossime_letture'))]
    tl += [(45 + 10 * i, x) for i, f in enumerate(sens) for x in [acceso(IB + f)]]
    tl += [(80, acceso(IB + 'opzione_finestra_prossime_letture')), (90, spento(IB + 'opzioni_monitoraggio_sensori'))]
    out.append(scenario('FIN|TIMER', timeline=tl, end=160))
    # la finestra Tempi di Attesa e le altre finestre di Opzioni; il pannello Opzioni
    altre = ['opzioni_calendario_main', 'opzioni_free_heating_o_free_cooling', 'opzioni_calendario', 'opzioni_punto_di_rugiada',
             'opzioni_scelta_sensori', 'opzioni_elementi_chimici', 'opzione_finestra_audio', 'conferma_pulizia_cronologia']
    tl = [(10, acceso(IB + 'opzioni_offset_sensori'))]
    tl += [(15 + 5 * i, acceso(IB + f)) for i, f in enumerate(altre)]
    tl += [(60, acceso(IB + 'opzione_finestra_tempi_attesa'))]
    tl += [(70 + 10 * i, x) for i, f in enumerate(altre) for x in [acceso(IB + f), acceso(IB + 'opzione_finestra_tempi_attesa')]]
    tl = sorted(tl, key=lambda x: x[0])
    tl += [(160, spento(IB + 'opzioni_offset_sensori')), (170, acceso(IB + 'opzione_finestra_tempi_attesa')),
           (180, acceso(IB + 'opzioni_offset_sensori'))]
    out.append(scenario('FIN|TEMPI', timeline=tl, end=240))
    return out


def fam_notifiche():
    out = []
    vel = [(5, acceso(NOTIFICA)), (40, ('press', 0)), (100, ('press', 2)), (160, ('card_u', 0))]
    out.append(scenario('NOT|VEL', setup=setup_telefono(), timeline=vel, end=260))
    out.append(scenario('NOT|VEL|SENZA_TELEFONO', timeline=vel, end=260))
    out.append(scenario('NOT|VEL|NOTIFICA_SPENTA', setup=setup_telefono(), timeline=vel[1:], end=260))
    out.append(scenario('NOT|VEL|SERVIZIO_MANCANTE', setup=setup_telefono(con_servizio=False), timeline=vel, end=260))
    for k, e in SENSORI.items():
        valore = {'te': 10.0, 'ti': 20.0, 'ue': 30.0, 'ui': 50.0, 'co2': 500.0}[k]
        tl = [(5, acceso(NOTIFICA)), (40, ('stato', e, 'unavailable', {})), (150, ('env', {k: valore}))]
        out.append(scenario(f'NOT|ERR_{k.upper()}', setup=setup_telefono(), timeline=tl, end=260))
    out.append(scenario('NOT|ERR_TE|SENZA_TELEFONO', timeline=[(5, acceso(NOTIFICA)), (40, ('stato', SENSORI['te'], 'unavailable', {})),
                                                               (150, ('env', {'te': 10.0}))], end=260))
    # cellulare tolto dall'app (device_tracker non disponibile): avviso nella scheda
    out.append(scenario('NOT|TELEFONO_TOLTO', setup=setup_telefono(),
                        timeline=[(5, acceso(NOTIFICA)), (40, ('stato', TRACKER, 'unavailable', {'friendly_name': TEL}))], end=150))
    # notifiche che nel package non hanno un chiamante raggiungibile: dallo script (interfaccia di HA)
    for con in (True, False):
        s = setup_telefono() if con else []
        sfx = '' if con else '|SENZA_TELEFONO'
        out.append(scenario('NOT|FILTRO' + sfx, setup=s, timeline=[(10, tasto(SC + 'notifica_cambio_filtro'))], end=60))
        out.append(scenario('NOT|MEDIA_PLAYER' + sfx, setup=s + setup_media_player(profilo=False),
                            timeline=[(10, tasto(SC + 'notifica_errore_media_player'))], end=60))
    return out


def fam_pulizia():
    conferma = IB + 'conferma_pulizia_cronologia'
    return [
        scenario('PUL|SI', timeline=[(10, acceso(conferma)), (20, tasto(SC + 'pulisci_cronologia_entita'))], end=90),
        scenario('PUL|NO', timeline=[(10, acceso(conferma)), (20, spento(conferma))], end=90),
        scenario('PUL|AUDIO', timeline=[(10, tasto(SC + 'pulisci_cronologia_audio'))], end=60),
    ]


def fam_profili():
    out = []
    for p in ['profilo_calendario', 'profilo_free_heating_cooling', 'profilo_pdr', 'profilo_umidita', 'audio_profilo',
              'reset_filtro_vmc', 'azzera_aria_scambiata', 'upgrade_sensors']:
        out.append(scenario(f'PRO|{p}', timeline=[(10, tasto(SC + p))], end=150))
    for s0 in (2, 0):
        out.append(scenario(f'PRO|profilo_inizializzazione|{s0}', s0=s0, timeline=[(10, tasto(SC + 'profilo_inizializzazione'))],
                            end=200))
    offset = [ui('input_number', 'set_value', entity_id=f'input_number.vmc_master_offset_{o}', value=v)
              for o, v in [('temp_esterna', 1.5), ('temp_interna', -1), ('umidita_esterna', 3), ('umidita_interna', -2),
                           ('co2', 50), ('voc', 10)]]
    out.append(scenario('PRO|azzera_offset_sensors', setup=offset, timeline=[(10, tasto(SC + 'azzera_offset_sensors'))], end=120))
    return out


def fam_varie():
    nome = 'input_text.vmc_master_nome_da_inserire'
    repo = 'sensor.vmc_master_versione_repository'
    sel = [('temp_external', 'sensor.vmc_master_temp_esterna_status_senza_offset'),
           ('temp_internal', 'sensor.vmc_master_temp_interna_status_senza_offset'),
           ('humidity_external', 'sensor.sim_ui'), ('humidity_internal', 'sensor.vmc_master_umidita_interna_status_senza_offset'),
           ('co2_internal', 'sensor.vmc_master_co2_status_senza_offset')]
    return [
        scenario('VAR|NOME', timeline=[(10, ui('input_text', 'set_value', entity_id=nome, value='Soggiorno'))], end=90),
        scenario('VAR|NOME_NON_VALIDO', timeline=[(10, ui('input_text', 'set_value', entity_id=nome, value='Nome lungo!'))], end=90),
        scenario('VAR|REPOSITORY', timeline=[(10, ('stato', repo, '9.0.0b99', {'friendly_name': 'Versione Repository'})),
                                             (60, ('stato', repo, '9.0.0b41', {'friendly_name': 'Versione Repository'}))], end=120),
        # scelta dei sensori, del media player e del cellulare nella scheda (elenchi gia' aggiornati)
        scenario('VAR|SENSORI', setup=[('stato', MP, 'idle', {'friendly_name': 'Cucina'}), ('telefono', TEL, True),
                                       tasto(AGG_MP), tasto(AGG_TEL), ('attendi', 7)],
                 timeline=[(10 + 10 * i, ui('input_select', 'select_option', entity_id=f'input_select.vmc_master_selected_{s}_entity',
                                            option=o)) for i, (s, o) in enumerate(sel)]
                 + [(60, ui('input_select', 'select_option', entity_id=SEL_MP, option=MP)),
                    (70, ui('input_select', 'select_option', entity_id=SEL_TEL, option=TEL_SLUG))], end=150),
    ]


def fam_ripartenza():
    out = []
    taglio = [(20, ('online', False)), (30, ('online', True))]
    for s in [2, 3, 4, 5, 6, 7, 1]:
        out.append(scenario(f'RIP|{s}', s0=s, timeline=taglio, end=200))
    out.append(scenario('RIP|3|RIPRENDE', s0=3, setup=[('resume', True)], timeline=taglio, end=200))
    # comando di un'altra velocita' dalla scheda durante il taglio: non e' una ripartenza
    out.append(scenario('RIP|3|COMANDO', s0=3, timeline=[(20, ('online', False)), (25, ('card_u', 2)), (30, ('online', True))],
                        end=200))
    # durante la 1a Fascia del Calendario (Velocita' 3, minuti 1-5): Spia Black-Out del Calendario
    import gen
    setup, t0a, _ = gen.cal_setup(3, 2, False)
    out.append(scenario('RIP|CALENDARIO', s0=0, setup=setup, timeline=[(150, ('online', False)), (160, ('online', True))],
                        end=420, setup_t0=t0a + [('switch', gen.CAL_SW, True)], align_minute=True))
    return out


def famiglia():
    out = (fam_audio() + fam_riepilogo() + fam_riallineamento() + fam_inizializza() + fam_cambio_ip() + fam_finestre()
           + fam_notifiche() + fam_pulizia() + fam_profili() + fam_varie() + fam_ripartenza())
    ids = [s['id'] for s in out]
    assert len(ids) == len(set(ids)), 'id ripetuti'
    return out


if __name__ == '__main__':
    import collections
    f = famiglia()
    print(len(f), dict(collections.Counter(s['id'].split('|')[1] for s in f)))
