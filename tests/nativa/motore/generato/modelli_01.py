"""Modelli Jinja del package, tradotti in Python (parte 1 di 9).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from custom_components.vmc_master.nativa.motore import jinja as J


def m0001(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))))
    return ''.join(_o)


def m0002(c, V):
    # {{ states('input_text.vmc_master_velocita_precedente') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_velocita_precedente'))))
    return ''.join(_o)


def m0003(c, V):
    # {{ velocita_corrente }}
    _o = []
    _o.append(J.testo(V['velocita_corrente']))
    return ''.join(_o)


def m0004(c, V):
    # {{ velocita_corrente != velocita_precedente }}
    _o = []
    _o.append(J.testo((V['velocita_corrente'] != V['velocita_precedente'])))
    return ''.join(_o)


def m0005(c, V):
    # {{ trigger.platform == 'time' }}
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'platform') == 'time')))
    return ''.join(_o)


def m0006(c, V):
    # {% set p = portate.get(velocita_corrente, 0) %} {{ (p / 3600) | float | round(6) }}
    v_p = J.MANCANTE
    _o = []
    v_p = J.chiama(J.attributo(V['portate'], 'get'), V['velocita_corrente'], 0)
    _o.extend((' ', J.testo(J.f_round(J.f_float((J.leggi(v_p, 'p') / 3600)), 6))))
    return ''.join(_o)


def m0007(c, V):
    # {% set map = { 'Velocità 1': 'input_number.vmc_master_aria_scambiata_v1', 'Velocità 2':...
    v_map = J.MANCANTE
    _o = []
    v_map = {'Velocità 1': c.N('input_number.vmc_master_aria_scambiata_v1'), 'Velocità 2': c.N('input_number.vmc_master_aria_scambiata_v2'), 'Velocità 3': c.N('input_number.vmc_master_aria_scambiata_v3'), 'Velocità 4': c.N('input_number.vmc_master_aria_scambiata_v4'), 'Iperventilazione': c.N('input_number.vmc_master_aria_scambiata_iperventilazione'), 'Notturna': c.N('input_number.vmc_master_aria_scambiata_notte'), 'Free Cooling': c.N('input_number.vmc_master_aria_scambiata_freecooling')}
    _o.extend((' ', J.testo(J.elemento(J.leggi(v_map, 'map'), V['velocita_corrente']))))
    return ''.join(_o)


def m0008(c, V):
    # {{ states('sensor.vmc_master_tempo_mancante_ricambio') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_tempo_mancante_ricambio'))))
    return ''.join(_o)


def m0009(c, V):
    # {{ states('input_number.vmc_master_volume_da_inserire') | float(0) }}
    _o = []
    _o.append(J.testo(J.f_float(c.states(c.N('input_number.vmc_master_volume_da_inserire')), 0)))
    return ''.join(_o)


def m0010(c, V):
    # {{ states('input_number.vmc_master_aria_scambiata_ricomincio') | float(0) }}
    _o = []
    _o.append(J.testo(J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_ricomincio')), 0)))
    return ''.join(_o)


def m0011(c, V):
    # {{ (states(ricomincio_entity) | float(0)) + incremento }}
    _o = []
    _o.append(J.testo((J.f_float(c.states(V['ricomincio_entity']), 0) + V['incremento'])))
    return ''.join(_o)


def m0012(c, V):
    # {{ ricomincio_entity }}
    _o = []
    _o.append(J.testo(V['ricomincio_entity']))
    return ''.join(_o)


def m0013(c, V):
    # {#- solo '0 secondi': con '1 secondo' (testo del sensore) ogni ricambio si chiuderebbe ...
    _o = []
    _o.append(J.testo(((V['tempo_mancante'] in ['0 secondi']) and (V['ricomincio_val'] > 0))))
    return ''.join(_o)


def m0014(c, V):
    # {{ totale_entity }}
    _o = []
    _o.append(J.testo(V['totale_entity']))
    return ''.join(_o)


def m0015(c, V):
    # {{ (states(totale_entity) | float(0) + incremento) | round(6) }}
    _o = []
    _o.append(J.testo(J.f_round((J.f_float(c.states(V['totale_entity']), 0) + V['incremento']), 6)))
    return ''.join(_o)


def m0016(c, V):
    # {{ nuovo_valore >= volume }}
    _o = []
    _o.append(J.testo((V['nuovo_valore'] >= V['volume'])))
    return ''.join(_o)


def m0017(c, V):
    # {{ nuovo_valore | round(6) }}
    _o = []
    _o.append(J.testo(J.f_round(V['nuovo_valore'], 6)))
    return ''.join(_o)


def m0018(c, V):
    # {{ trigger.platform != 'time' }}
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'platform') != 'time')))
    return ''.join(_o)


def m0019(c, V):
    # {{ velocita_corrente in ['Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Iperv...
    _o = []
    _o.append(J.testo((V['velocita_corrente'] in ['Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Iperventilazione', 'Notturna', 'Free Cooling'])))
    return ''.join(_o)


def m0020(c, V):
    # {{ trigger.id == 'spia_avvio_rimasta_accesa' }}
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'id') == 'spia_avvio_rimasta_accesa')))
    return ''.join(_o)


def m0021(c, V):
    # {{ is_state('sensor.vmc_master_status_ip_interfaccia', 'OFF-Line') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line')))
    return ''.join(_o)


def m0022(c, V):
    # {{ is_state('sensor.vmc_master_status_ip_interfaccia', 'ON-Line') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line')))
    return ''.join(_o)


def m0023(c, V):
    # {{ is_state('sensor.vmc_master_congelamento_verifica_soglia', 'Si') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_congelamento_verifica_soglia'), 'Si')))
    return ''.join(_o)


def m0024(c, V):
    # {{ is_state('sensor.vmc_master_congelamento_verifica_soglia', '[No ma Prossimo]') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_congelamento_verifica_soglia'), '[No ma Prossimo]')))
    return ''.join(_o)


def m0025(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_congelamento', 'Nessuna Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_congelamento'), 'Nessuna Allerta')))
    return ''.join(_o)


def m0026(c, V):
    # {{ is_state('sensor.vmc_master_delta_temp_verifica_soglia', 'Si') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_delta_temp_verifica_soglia'), 'Si')))
    return ''.join(_o)


def m0027(c, V):
    # {{ is_state('sensor.vmc_master_delta_temp_verifica_soglia', '[No ma Prossimo]') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_delta_temp_verifica_soglia'), '[No ma Prossimo]')))
    return ''.join(_o)


def m0028(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_delta', 'Nessuna Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_delta'), 'Nessuna Allerta')))
    return ''.join(_o)


def m0029(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_co2', 'Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_co2'), 'Allerta')))
    return ''.join(_o)


def m0030(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_co2', 'Nessuna Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_co2'), 'Nessuna Allerta')))
    return ''.join(_o)


def m0031(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_voc', 'Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_voc'), 'Allerta')))
    return ''.join(_o)


def m0032(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_voc', 'Nessuna Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_voc'), 'Nessuna Allerta')))
    return ''.join(_o)


def m0033(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_pdr', 'Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_pdr'), 'Allerta')))
    return ''.join(_o)


def m0034(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_pdr', 'Nessuna Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_pdr'), 'Nessuna Allerta')))
    return ''.join(_o)


def m0035(c, V):
    # {{ states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) not in ['unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0036(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_umidita', 'Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_umidita'), 'Allerta')))
    return ''.join(_o)


def m0037(c, V):
    # {{ is_state('sensor.vmc_master_alert_monitoraggio_umidita', 'Nessuna Allerta') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_umidita'), 'Nessuna Allerta')))
    return ''.join(_o)


def m0038(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_status_ventola_lettura_codice_interpretato_i...
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'))))
    return ''.join(_o)


def m0039(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_umidita' and trigger.to_s...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_umidita')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Allerta'))))
    return ''.join(_o)


def m0040(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_umidita' and trigger.to_s...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_umidita')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Nessuna Allerta'))))
    return ''.join(_o)


def m0041(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_co2' and trigger.to_state...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_co2')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Allerta'))))
    return ''.join(_o)


def m0042(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_co2' and trigger.to_state...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_co2')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Nessuna Allerta'))))
    return ''.join(_o)


def m0043(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_voc' and trigger.to_state...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_voc')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Allerta'))))
    return ''.join(_o)


def m0044(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_voc' and trigger.to_state...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_voc')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Nessuna Allerta'))))
    return ''.join(_o)


def m0045(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_pdr' and trigger.to_state...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_pdr')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Allerta'))))
    return ''.join(_o)


def m0046(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_pdr' and trigger.to_state...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_pdr')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Nessuna Allerta'))))
    return ''.join(_o)


def m0047(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_status_ip_interfaccia' and trigger.to_state....
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_status_ip_interfaccia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'OFF-Line'))))
    return ''.join(_o)


def m0048(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_status_ip_interfaccia' and trigger.to_state....
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_status_ip_interfaccia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'ON-Line'))))
    return ''.join(_o)


def m0049(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooli...
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi'))))
    return ''.join(_o)


def m0050(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_congelamento_verifica_soglia' and trigger.to...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_congelamento_verifica_soglia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Si'))))
    return ''.join(_o)


def m0051(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_congelamento_verifica_soglia' and trigger.to...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_congelamento_verifica_soglia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == '[No ma Prossimo]'))))
    return ''.join(_o)


def m0052(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_congelamento_verifica_soglia' and trigger.to...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_congelamento_verifica_soglia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'No'))))
    return ''.join(_o)


def m0053(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_delta_temp_verifica_soglia' and trigger.to_s...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_delta_temp_verifica_soglia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'Si'))))
    return ''.join(_o)


def m0054(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_delta_temp_verifica_soglia' and trigger.to_s...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_delta_temp_verifica_soglia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == '[No ma Prossimo]'))))
    return ''.join(_o)


def m0055(c, V):
    # {{ trigger.entity_id == 'sensor.vmc_master_delta_temp_verifica_soglia' and trigger.to_s...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'entity_id') == c.N('sensor.vmc_master_delta_temp_verifica_soglia')) and (J.attributo(J.attributo(V['trigger'], 'to_state'), 'state') == 'No'))))
    return ''.join(_o)


def m0056(c, V):
    # {{ states('input_text.vmc_master_ip_insert') | trim }}
    _o = []
    _o.append(J.testo(J.f_trim(c.states(c.N('input_text.vmc_master_ip_insert')))))
    return ''.join(_o)


def m0057(c, V):
    # {%- set ottetti = (ip.split('.') + ['', '']) | map('int', 0) | list -%} {{ ip is match(...
    v_ottetti = J.MANCANTE
    _o = []
    v_ottetti = J.f_list(J.f_map((J.chiama(J.attributo(V['ip'], 'split'), '.') + ['', '']), 'int', 0))
    _o.append(J.testo((((J.t_match(V['ip'], '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$') and (J.elemento(J.leggi(v_ottetti, 'ottetti'), 0) not in [0, 127])) and (J.elemento(J.leggi(v_ottetti, 'ottetti'), 0) < 224)) and (J.elemento(J.leggi(v_ottetti, 'ottetti'), slice(None, 2, None)) != [169, 254]))))
    return ''.join(_o)


def m0058(c, V):
    # {%- set ns = namespace(uso=false) -%} {%- for s in states.sensor | rejectattr('attribut...
    v_ns = J.MANCANTE
    _o = []
    v_ns = J.namespace(uso=False)
    for v_s_1 in J.f_rejectattr(J.f_selectattr(J.f_rejectattr(J.attributo(c.states, 'sensor'), 'attributes.restored', c.test('eq'), True), 'entity_id', c.test('search'), '^sensor\\.vmc_[a-z]+_ip$'), 'entity_id', c.test('eq'), c.N('sensor.vmc_master_ip')):
        if (J.f_trim(J.attributo(v_s_1, 'state')) == V['ip']):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'uso', True)
    _o.append(J.testo(((not J.attributo(J.leggi(v_ns, 'ns'), 'uso')) and (V['ip'] != J.f_trim(c.states(c.N('sensor.vmc_master_ip')))))))
    return ''.join(_o)


def m0059(c, V):
    # verifica {{ ip }}
    _o = []
    _o.extend(('verifica ', J.testo(V['ip'])))
    return ''.join(_o)


def m0060(c, V):
    # {{ ip }}
    _o = []
    _o.append(J.testo(V['ip']))
    return ''.join(_o)


def m0061(c, V):
    # {%- set nome = states('sensor.vmc_master_nome_status') | trim -%} {{ '' if nome in ['No...
    v_nome = J.MANCANTE
    _o = []
    v_nome = J.f_trim(c.states(c.N('sensor.vmc_master_nome_status')))
    _o.append(J.testo(('' if (J.leggi(v_nome, 'nome') in ['Non disponibile', 'unknown', 'unavailable']) else J.leggi(v_nome, 'nome'))))
    return ''.join(_o)


def m0062(c, V):
    # {{ verifica.esito }} {{ ip }}
    _o = []
    _o.extend((J.testo(J.attributo(V['verifica'], 'esito')), ' ', J.testo(V['ip'])))
    return ''.join(_o)


def m0063(c, V):
    # {{ verifica.esito == 'ok' and states('input_text.vmc_master_ip_insert') | trim == ip }}
    _o = []
    _o.append(J.testo(((J.attributo(V['verifica'], 'esito') == 'ok') and (J.f_trim(c.states(c.N('input_text.vmc_master_ip_insert'))) == V['ip']))))
    return ''.join(_o)


def m0064(c, V):
    # {{ ip_valido and ip_libero }}
    _o = []
    _o.append(J.testo((V['ip_valido'] and V['ip_libero'])))
    return ''.join(_o)


def m0065(c, V):
    # {{ trigger.id.split('|') }}
    _o = []
    _o.append(J.testo(J.chiama(J.attributo(J.attributo(V['trigger'], 'id'), 'split'), '|')))
    return ''.join(_o)


def m0066(c, V):
    # {{ states('input_number.vmc_master_attesa_' ~ parti[2]) | int(0) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(J.concat(c.N('input_number.vmc_master_attesa_'), J.elemento(V['parti'], 2))), 0)))
    return ''.join(_o)


def m0067(c, V):
    # {{ parti[3][:250] }}
    _o = []
    _o.append(J.testo(J.elemento(J.elemento(V['parti'], 3), slice(None, 250, None))))
    return ''.join(_o)


def m0068(c, V):
    # {%- if parti[1] != 'free_annullamento' -%}{{ parti[1] }} {%- elif is_state('input_boole...
    _o = []
    if (J.elemento(V['parti'], 1) != 'free_annullamento'):
        _o.append(J.testo(J.elemento(V['parti'], 1)))
    elif c.is_state(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'on'):
        _o.append('free_heating_annullamento')
    elif c.is_state(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'on'):
        _o.append('free_cooling_annullamento')
    elif c.is_state(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'), 'Free Cooling'):
        _o.append('free_cooling_annullamento')
    else:
        _o.append('free_heating_annullamento')
    return ''.join(_o)


def m0069(c, V):
    # {{ ['free_heating_annullamento', 'free_cooling_annullamento'] if parti[1] == 'free_annu...
    _o = []
    _o.append(J.testo((['free_heating_annullamento', 'free_cooling_annullamento'] if (J.elemento(V['parti'], 1) == 'free_annullamento') else [J.elemento(V['parti'], 1)])))
    return ''.join(_o)


def m0070(c, V):
    # {{ testo }}
    _o = []
    _o.append(J.testo(V['testo']))
    return ''.join(_o)


def m0071(c, V):
    # input_text.vmc_master_countdown_{{ famiglia }}
    _o = []
    _o.extend((c.N('input_text.vmc_master_countdown_'), J.testo(V['famiglia'])))
    return ''.join(_o)


def m0072(c, V):
    # {{ '%02d:%02d:%02d' % (secondi // 3600, (secondi % 3600) // 60, secondi % 60) }}
    _o = []
    _o.append(J.testo(('%02d:%02d:%02d' % ((V['secondi'] // 3600), ((V['secondi'] % 3600) // 60), (V['secondi'] % 60), ))))
    return ''.join(_o)


def m0073(c, V):
    # timer.vmc_master_countdown_{{ famiglia }}
    _o = []
    _o.extend((c.N('timer.vmc_master_countdown_'), J.testo(V['famiglia'])))
    return ''.join(_o)


def m0074(c, V):
    # {{ parti[0] == 'ON' }}
    _o = []
    _o.append(J.testo((J.elemento(V['parti'], 0) == 'ON')))
    return ''.join(_o)


def m0075(c, V):
    # timer.vmc_master_countdown_{{ repeat.item }}
    _o = []
    _o.extend((c.N('timer.vmc_master_countdown_'), J.testo(J.attributo(V['repeat'], 'item'))))
    return ''.join(_o)


def m0076(c, V):
    # input_text.vmc_master_countdown_{{ repeat.item }}
    _o = []
    _o.extend((c.N('input_text.vmc_master_countdown_'), J.testo(J.attributo(V['repeat'], 'item'))))
    return ''.join(_o)


def m0077(c, V):
    # {{ states('input_text.vmc_master_countdown_' ~ repeat.item) == testo }}
    _o = []
    _o.append(J.testo((c.states(J.concat(c.N('input_text.vmc_master_countdown_'), J.attributo(V['repeat'], 'item'))) == V['testo'])))
    return ''.join(_o)


def m0078(c, V):
    # {{ famiglie_off }}
    _o = []
    _o.append(J.testo(V['famiglie_off']))
    return ''.join(_o)


def m0079(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0080(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0081(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0082(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0083(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0084(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0085(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0086(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0087(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0088(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0089(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0090(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0091(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne scons...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0092(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0093(c, V):
    # {{ ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsigl...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0094(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_punto_di_rugiada_verifica_c...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0095(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0096(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0097(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0098(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0099(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0100(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0101(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0102(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0103(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0104(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0105(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0106(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0107(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0108(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0109(c, V):
    # {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sconsi...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0110(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_punto_di_rugiada_verifica...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0111(c, V):
    # {{ ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sconsigl...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0112(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_punto_di_rugiada_verifica_c...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0113(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0114(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0115(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0116(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0117(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0118(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0119(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0120(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0121(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0122(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0123(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0124(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0125(c, V):
    # {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sc...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0126(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( ( states('sensor.vmc_master_punto_di_rugiada_veri...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0127(c, V):
    # {{ ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne sconsigl...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on') or ((c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on') and (((c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) or ((c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')))))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0128(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_punto_di_rugiada_verifica_c...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on') or ((c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on') and (((c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) or ((c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')))))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0129(c, V):
    # {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne scon...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0130(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0131(c, V):
    # {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne scon...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0132(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0133(c, V):
    # {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne scon...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0134(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0135(c, V):
    # {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne scon...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0136(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0137(c, V):
    # {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') != "Se ne scon...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0138(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( ( states('sensor.vmc_master_punto_di_rugiada_verifi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0139(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')!="Se ne sconsig...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0140(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verific...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0141(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0142(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0143(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0144(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0145(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0146(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0147(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0148(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)']) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0149(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo((((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Heating Programmato', 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling']) or (((c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('input_select.vmc_master_speed_umidita')) != 'Velocità 0')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')))) and (not ((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")))) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0150(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Heating Programmato', 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling']) or (((c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('input_select.vmc_master_speed_umidita')) != 'Velocità 0')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')))) and (not ((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")))) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0151(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo((((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Cooling Programmato', 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling']) or (((c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('input_select.vmc_master_speed_umidita')) != 'Velocità 0')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')))) and (not ((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")))) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0152(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Cooling Programmato', 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling']) or (((c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('input_select.vmc_master_speed_umidita')) != 'Velocità 0')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')))) and (not ((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")))) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0153(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Heating Programmato', 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Velocità 1', 'Free Cooling'])) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0154(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Heating Programmato', 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Velocità 1', 'Free Cooling'])) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0155(c, V):
    # {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Cooling Programmato', 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Velocità 1', 'Free Cooling'])) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0156(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_alert_monitoraggio_free_h...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Cooling Programmato', 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti']) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Velocità 1', 'Free Cooling'])) and (c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0157(c, V):
    # {{ ( ( states('sensor.vmc_master_status_ip_interfaccia') == "OFF-Line" and states('sens...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0158(c, V):
    # {%- set vmc_master_esito -%} {{ ( ( states('sensor.vmc_master_status_ip_interfaccia') =...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)
