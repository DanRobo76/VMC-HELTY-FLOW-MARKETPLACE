"""Modelli Jinja del package, tradotti in Python (parte 9 di 10).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from .. import jinja as J


def m1032(c, V):
    # {% set mp = states('input_select.vmc_master_selected_media_player_entity') %} {% set in...
    v_mp = v_invalid = v_audio_interruttore = v_now_time = v_start_raw = v_end_raw = v_start_time = v_end_time = J.MANCANTE
    _o = []
    v_mp = c.states(c.N('select.vmc_master_selected_media_player_entity'))
    _o.append(' ')
    v_invalid = ['Aggiorna Elenco Media Player', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_audio_interruttore = c.states(c.N('switch.vmc_master_notifica_audio'))
    _o.append(' ')
    v_now_time = J.chiama(J.attributo(c.now(), 'time'))
    _o.extend(('\n', ' '))
    v_start_raw = J.elemento(c.states(c.N('time.vmc_master_audio_start_time')), slice(None, 5, None))
    _o.append(' ')
    v_end_raw = J.elemento(c.states(c.N('time.vmc_master_audio_end_time')), slice(None, 5, None))
    _o.append('\n')
    v_start_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_start_raw, 'start_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_start_raw, 'start_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append(' ')
    v_end_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_end_raw, 'end_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_end_raw, 'end_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append('\n')
    if (J.leggi(v_start_time, 'start_time') and J.leggi(v_end_time, 'end_time')):
        _o.append('\n  ')
        if (J.leggi(v_start_time, 'start_time') <= J.leggi(v_end_time, 'end_time')):
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('switch.vmc_master_notifica_allerta_black_out')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('switch.vmc_master_notifica_allerta_black_out')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1033(c, V):
    # {{ ip | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(V['ip'], '')))
    return ''.join(_o)


def m1034(c, V):
    # "{{ states('input_text.vmc_master_nome_da_inserire') | replace('"', '') | replace('\\',...
    _o = []
    _o.extend(('"', J.testo(J.f_replace(J.f_replace(c.states(c.N('text.vmc_master_nome_da_inserire')), '"', ''), '\\', '')), '"'))
    return ''.join(_o)


def m1035(c, V):
    # {% set entity_id = states('input_select.vmc_master_selected_temp_external_entity') %} {...
    v_temp = V.get('temp', J.MANCANTE)
    v_entity_id = J.MANCANTE
    _o = []
    v_entity_id = c.states(c.N('select.vmc_master_selected_temp_external_entity'))
    _o.append(' ')
    if J.chiama(J.attributo(J.leggi(v_entity_id, 'entity_id'), 'startswith'), 'sensor.'):
        _o.append('\n  ')
        if J.f_is_number(c.timer.states(J.leggi(v_entity_id, 'entity_id'))):
            _o.extend(('\n    ', J.testo(c.timer.states(J.leggi(v_entity_id, 'entity_id'))), '\n  '))
        else:
            _o.append('\n    -100\n  ')
        _o.append('\n')
    elif J.chiama(J.attributo(J.leggi(v_entity_id, 'entity_id'), 'startswith'), 'weather.'):
        _o.append('\n  ')
        v_temp = c.timer.state_attr(J.leggi(v_entity_id, 'entity_id'), 'temperature')
        _o.append('\n  ')
        if (not J.t_none(J.leggi(v_temp, 'temp'))):
            _o.extend(('\n    ', J.testo(J.leggi(v_temp, 'temp')), '\n  '))
        else:
            _o.append('\n    -100\n  ')
        _o.append('\n')
    else:
        _o.append('\n  -100\n')
    return ''.join(_o)


def m1036(c, V):
    # {% set entity_id = states('input_select.vmc_master_selected_temp_internal_entity') %} {...
    v_entity_id = J.MANCANTE
    _o = []
    v_entity_id = c.states(c.N('select.vmc_master_selected_temp_internal_entity'))
    _o.append(' ')
    if (J.leggi(v_entity_id, 'entity_id') and J.f_is_number(c.timer.states(J.leggi(v_entity_id, 'entity_id')))):
        _o.extend(('\n  ', J.testo(c.timer.states(J.leggi(v_entity_id, 'entity_id'))), '\n'))
    else:
        _o.append('\n  -100\n')
    return ''.join(_o)


def m1037(c, V):
    # {% set entity_id = states('input_select.vmc_master_selected_humidity_external_entity') ...
    v_hum = V.get('hum', J.MANCANTE)
    v_entity_id = J.MANCANTE
    _o = []
    v_entity_id = c.states(c.N('select.vmc_master_selected_humidity_external_entity'))
    _o.append(' ')
    if J.chiama(J.attributo(J.leggi(v_entity_id, 'entity_id'), 'startswith'), 'sensor.'):
        _o.append('\n  ')
        if J.f_is_number(c.timer.states(J.leggi(v_entity_id, 'entity_id'))):
            _o.extend(('\n    ', J.testo(c.timer.states(J.leggi(v_entity_id, 'entity_id'))), '\n  '))
        else:
            _o.append('\n    -100\n  ')
        _o.append('\n')
    elif J.chiama(J.attributo(J.leggi(v_entity_id, 'entity_id'), 'startswith'), 'weather.'):
        _o.append('\n  ')
        v_hum = c.timer.state_attr(J.leggi(v_entity_id, 'entity_id'), 'humidity')
        _o.append('\n  ')
        if (not J.t_none(J.leggi(v_hum, 'hum'))):
            _o.extend(('\n    ', J.testo(J.leggi(v_hum, 'hum')), '\n  '))
        else:
            _o.append('\n    -100\n  ')
        _o.append('\n')
    else:
        _o.append('\n  -100\n')
    return ''.join(_o)


def m1038(c, V):
    # {% set entity_id = states('input_select.vmc_master_selected_humidity_internal_entity') ...
    v_entity_id = J.MANCANTE
    _o = []
    v_entity_id = c.states(c.N('select.vmc_master_selected_humidity_internal_entity'))
    _o.append(' ')
    if (J.leggi(v_entity_id, 'entity_id') and J.f_is_number(c.timer.states(J.leggi(v_entity_id, 'entity_id')))):
        _o.extend(('\n  ', J.testo(c.timer.states(J.leggi(v_entity_id, 'entity_id'))), '\n'))
    else:
        _o.append('\n  -100\n')
    return ''.join(_o)


def m1039(c, V):
    # {% set entity_id = states('input_select.vmc_master_selected_co2_internal_entity') %} {%...
    v_entity_id = J.MANCANTE
    _o = []
    v_entity_id = c.states(c.N('select.vmc_master_selected_co2_internal_entity'))
    _o.append(' ')
    if (J.leggi(v_entity_id, 'entity_id') and (c.timer.states(J.leggi(v_entity_id, 'entity_id')) not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])):
        _o.append('\n  ')
        if (c.timer.states(J.leggi(v_entity_id, 'entity_id')) == '-'):
            _o.append('\n    0\n  ')
        else:
            _o.extend(('\n    ', J.testo((J.f_float(c.timer.states(J.leggi(v_entity_id, 'entity_id'))) if J.f_is_number(c.timer.states(J.leggi(v_entity_id, 'entity_id'))) else (-100))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  -100\n')
    return ''.join(_o)


def m1040(c, V):
    # {%- set ip = states('input_text.vmc_master_ip_insert') | trim -%} {%- set esito = state...
    v_ip = v_esito = v_ottetti = v_ns = J.MANCANTE
    _o = []
    v_ip = J.f_trim(c.states(c.N('text.vmc_master_ip_insert')))
    v_esito = c.states(c.N('input_text.vmc_master_ip_insert_esito'))
    v_ottetti = J.f_list(J.f_map((J.chiama(J.attributo(J.leggi(v_ip, 'ip'), 'split'), '.') + ['', '']), 'int', 0))
    v_ns = J.namespace(uso=False)
    for v_s_1 in J.f_rejectattr(J.f_selectattr(J.f_rejectattr(J.attributo(c.states, 'sensor'), 'attributes.restored', c.test('eq'), True), 'entity_id', c.test('search'), '^sensor\\.vmc_[a-z]+_ip$'), 'entity_id', c.test('eq'), c.N('sensor.vmc_master_ip')):
        if (J.f_trim(J.attributo(v_s_1, 'state')) == J.leggi(v_ip, 'ip')):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'uso', True)
    if (J.leggi(v_ip, 'ip') == ''):
        _o.append('Nessun IP')
    elif ((((not J.t_match(J.leggi(v_ip, 'ip'), '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')) or (J.elemento(J.leggi(v_ottetti, 'ottetti'), 0) in [0, 127])) or (J.elemento(J.leggi(v_ottetti, 'ottetti'), 0) >= 224)) or (J.elemento(J.leggi(v_ottetti, 'ottetti'), slice(None, 2, None)) == [169, 254])):
        _o.append('IP non Valido')
    elif (J.leggi(v_ip, 'ip') == J.f_trim(c.states(c.N('sensor.vmc_master_ip')))):
        _o.append('IP già impostato')
    elif J.attributo(J.leggi(v_ns, 'ns'), 'uso'):
        _o.append('IP già in uso')
    elif (J.leggi(v_esito, 'esito') == J.concat('non_risponde ', J.leggi(v_ip, 'ip'))):
        _o.append('VMC non risponde')
    elif (J.leggi(v_esito, 'esito') == J.concat('altro_dispositivo ', J.leggi(v_ip, 'ip'))):
        _o.append('Non è una VMC')
    elif (J.leggi(v_esito, 'esito') == J.concat('nome_diverso ', J.leggi(v_ip, 'ip'))):
        _o.append('Nome VMC diverso')
    elif (J.leggi(v_esito, 'esito') != J.concat('ok ', J.leggi(v_ip, 'ip'))):
        _o.append('Verifica VMC in corso')
    else:
        _o.append(J.testo(J.leggi(v_ip, 'ip')))
    return ''.join(_o)


def m1041(c, V):
    # {% set stati = ['OFF-Line'] %} {{ 'OFF-Line' if states('sensor.vmc_master_status_ip') i...
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['OFF-Line']
    _o.extend((' ', J.testo(('OFF-Line' if (c.states(c.N('sensor.vmc_master_status_ip')) in J.leggi(v_stati, 'stati')) else 'ON-Line'))))
    return ''.join(_o)


def m1042(c, V):
    # {% if states('sensor.vmc_master_status_ip') == 'OFF-Line' %} mdi:fan-alert {% else %} m...
    _o = []
    if (c.states(c.N('sensor.vmc_master_status_ip')) == 'OFF-Line'):
        _o.append('\n  mdi:fan-alert\n')
    else:
        _o.append('\n  mdi:fan-chevron-down\n')
    return ''.join(_o)


def m1043(c, V):
    # {#- Trigger «Black-Out a Velocità 0» -#} {%- set t1 = ( ( states('sensor.vmc_master_sta...
    v_t1 = v_t2 = v_t3 = v_t4 = v_t5 = v_t6 = v_t7 = v_t8 = v_t9 = v_t10 = v_t11 = J.MANCANTE
    _o = []
    v_t1 = (((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t2 = (((((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t3 = ((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))
    v_t4 = (((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')))
    v_t5 = (((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t6 = (((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t7 = (((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t8 = (((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t9 = (((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))
    v_t10 = ((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off'))) and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')))
    v_t11 = (((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')))
    _o.append(J.testo(((((((((((J.leggi(v_t1, 't1') or J.leggi(v_t2, 't2')) or J.leggi(v_t3, 't3')) or J.leggi(v_t4, 't4')) or J.leggi(v_t5, 't5')) or J.leggi(v_t6, 't6')) or J.leggi(v_t7, 't7')) or J.leggi(v_t8, 't8')) or J.leggi(v_t9, 't9')) or J.leggi(v_t10, 't10')) or J.leggi(v_t11, 't11'))))
    return ''.join(_o)


def m1044(c, V):
    # {{ 'mdi:power-plug-off' if is_state('binary_sensor.vmc_master_black_out_rilevato', 'on'...
    _o = []
    _o.append(J.testo(('mdi:power-plug-off' if c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') else 'mdi:power-plug')))
    return ''.join(_o)


def m1045(c, V):
    # {% set invalid = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"]...
    v_parts = V.get('parts', J.MANCANTE)
    v_invalid = v_vmc_nome = J.MANCANTE
    _o = []
    v_invalid = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_vmc_nome = c.states(c.N('sensor.vmc_master_nome_memorizzata'))
    _o.append(' ')
    if (J.leggi(v_vmc_nome, 'vmc_nome') in J.leggi(v_invalid, 'invalid')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_parts = J.chiama(J.attributo(J.leggi(v_vmc_nome, 'vmc_nome'), 'split'), ' ', 1)
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_parts, 'parts')) >= 2):
            _o.extend(('\n    ', J.testo(J.f_trim(J.elemento(J.leggi(v_parts, 'parts'), 1))), '\n  '))
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1046(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_codice_status = V.get('codice_status', J.MANCANTE)
    v_stati = v_valid_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_valid_stati = ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 1):
            _o.append('\n    ')
            v_codice_status = J.elemento(J.leggi(v_componenti, 'componenti'), 1)
            _o.extend(('\n    ', J.testo((J.leggi(v_codice_status, 'codice_status') if (J.leggi(v_codice_status, 'codice_status') in J.leggi(v_valid_stati, 'valid_stati')) else 'Non disponibile')), '\n  '))
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1047(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_codice = V.get('codice', J.MANCANTE)
    v_stati = v_codici = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_codici = {'00000': 'Velocità 0', '00001': 'Velocità 1', '00002': 'Velocità 2', '00003': 'Velocità 3', '00004': 'Velocità 4', '00005': 'Iperventilazione', '00006': 'Notturna', '00007': 'Free Cooling'}
    _o.append('\n')
    if (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 1):
            _o.append('\n    ')
            v_codice = J.elemento(J.leggi(v_componenti, 'componenti'), 1)
            _o.extend(('\n    ', J.testo(J.chiama(J.attributo(J.leggi(v_codici, 'codici'), 'get'), J.leggi(v_codice, 'codice'), 'Non disponibile')), '\n  '))
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1048(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 0') or ('Velocità 0' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1049(c, V):
    # {{ 'mdi:numeric-0-box' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:numeric-0-box' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 0') or (not ('Velocità 0' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1050(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 1') or ('Velocità 1' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1051(c, V):
    # {{ 'mdi:numeric-1-box' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:numeric-1-box' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 1') or (not ('Velocità 1' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1052(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 2') or ('Velocità 2' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1053(c, V):
    # {{ 'mdi:numeric-2-box' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:numeric-2-box' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 2') or (not ('Velocità 2' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1054(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 3') or ('Velocità 3' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1055(c, V):
    # {{ 'mdi:numeric-3-box' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:numeric-3-box' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 3') or (not ('Velocità 3' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1056(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 4') or ('Velocità 4' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1057(c, V):
    # {{ 'mdi:numeric-4-box' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:numeric-4-box' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Velocità 4') or (not ('Velocità 4' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1058(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Notturna') or ('Notturna' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1059(c, V):
    # {{ 'mdi:weather-night' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:weather-night' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Notturna') or (not ('Notturna' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1060(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') =...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Iperventilazione') or ('Iperventilazione' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))))
    return ''.join(_o)


def m1061(c, V):
    # {{ 'mdi:wind-power' if states('sensor.vmc_master_status_ventola_lettura_codice_interpre...
    _o = []
    _o.append(J.testo(('mdi:wind-power' if ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Iperventilazione') or (not ('Iperventilazione' in J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · ')))) else 'mdi:restore')))
    return ''.join(_o)


def m1062(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia').s...
    _o = []
    _o.append(J.testo((J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')), 'startswith'), 'Free') or (J.f_count(J.f_list(J.f_select(J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · '), 'match', 'Free'))) > 0))))
    return ''.join(_o)


def m1063(c, V):
    # {{ 'mdi:weather-sunny' if states('sensor.vmc_master_status_ventola_lettura_codice_inter...
    _o = []
    _o.append(J.testo(('mdi:weather-sunny' if (J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')), 'startswith'), 'Free') or (not (J.f_count(J.f_list(J.f_select(J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · '), 'match', 'Free'))) > 0))) else 'mdi:restore')))
    return ''.join(_o)


def m1064(c, V):
    # {{ 'mdi:snowflake' if states('sensor.vmc_master_status_ventola_lettura_codice_interpret...
    _o = []
    _o.append(J.testo(('mdi:snowflake' if (J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')), 'startswith'), 'Free') or (not (J.f_count(J.f_list(J.f_select(J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · '), 'match', 'Free'))) > 0))) else 'mdi:restore')))
    return ''.join(_o)


def m1065(c, V):
    # {{ 'mdi:sun-snowflake-variant' if states('sensor.vmc_master_status_ventola_lettura_codi...
    _o = []
    _o.append(J.testo(('mdi:sun-snowflake-variant' if (J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')), 'startswith'), 'Free') or (not (J.f_count(J.f_list(J.f_select(J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_velocita_registrata')), 'split'), ' · '), 'match', 'Free'))) > 0))) else 'mdi:restore')))
    return ''.join(_o)


def m1066(c, V):
    # {{ states('sensor.vmc_master_status_sensori_lettura_codice_interpretato') == 'Accesi' }}
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_sensori_lettura_codice_interpretato')) == 'Accesi')))
    return ''.join(_o)


def m1067(c, V):
    # {{ states('sensor.vmc_master_status_sensori_lettura_codice_interpretato') == 'Spenti' }}
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_sensori_lettura_codice_interpretato')) == 'Spenti')))
    return ''.join(_o)


def m1068(c, V):
    # {{ states('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato') in ['Acc...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')) in ['Acceso', 'Verificare Filtro'])))
    return ''.join(_o)


def m1069(c, V):
    # {{ 'mdi:air-filter' if states('sensor.vmc_master_status_led_pannello_lettura_codice_int...
    _o = []
    _o.append(J.testo(('mdi:air-filter' if (c.states(c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')) == 'Verificare Filtro') else 'mdi:led-on')))
    return ''.join(_o)


def m1070(c, V):
    # {{ states('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato') == 'Spen...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')) == 'Spento')))
    return ''.join(_o)


def m1071(c, V):
    # {%- set mese_free = states('sensor.vmc_master_status_mese_corrente_freeheating_o_freeco...
    v_mese_free = v_nome_free = v_nomi = v_annullata = v_att = v_att_k = v_allerte = v_ns = J.MANCANTE
    _o = []
    v_mese_free = c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'))
    v_nome_free = (J.leggi(v_mese_free, 'mese_free') if ((J.leggi(v_mese_free, 'mese_free') in ['Free Heating', 'Free Cooling']) and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling')) != '[Non Calcolabile]')) else 'Free Heat./Cool.')
    v_nomi = {'0': 'Velocità 0', '1': 'Velocità 1', '2': 'Velocità 2', '3': 'Velocità 3', '4': 'Velocità 4', 'notturna': 'Notturna', 'iperventilazione': 'Iperventilazione', 'freecooling': J.leggi(v_nome_free, 'nome_free')}
    v_annullata = (c.timer.is_state(c.N('timer.vmc_master_countdown_free_heating_annullamento'), 'active') or c.timer.is_state(c.N('timer.vmc_master_countdown_free_cooling_annullamento'), 'active'))
    v_att = c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'))
    v_att_k = ('freecooling' if J.chiama(J.attributo(J.leggi(v_att, 'att'), 'startswith'), 'Free') else ('notturna' if (J.leggi(v_att, 'att') == 'Notturna') else ('iperventilazione' if (J.leggi(v_att, 'att') == 'Iperventilazione') else J.f_replace(J.leggi(v_att, 'att'), 'Velocità ', ''))))
    v_allerte = [['Congelamento', c.N('binary_sensor.vmc_master_spia_velocita_{}_congelamento'), J.f_list(J.chiama(J.attributo(J.leggi(v_nomi, 'nomi'), 'keys')))], ['Δ Temp.', c.N('binary_sensor.vmc_master_spia_velocita_{}_delta_temp_verifica_soglia_valore'), J.f_list(J.chiama(J.attributo(J.leggi(v_nomi, 'nomi'), 'keys')))], ['Inquinanti', c.N('binary_sensor.vmc_master_spia_velocita_{}_co2_o_voc'), ['0']], ['Inquinanti', c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), ['0']], ['Lim. Δ Punto di Rugiada', c.N('binary_sensor.vmc_master_spia_velocita_{}_un_solo_avvio'), J.f_list(J.chiama(J.attributo(J.leggi(v_nomi, 'nomi'), 'keys')))], ['Lim. Δ Punto di Rugiada', c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), ['0']], ['Avviso Free Cooling', c.N('binary_sensor.vmc_master_spia_velocita_{}_un_solo_avvio_per_programmazione_freecooling'), ['freecooling'], 'Free Cooling'], ['Avviso Free Heating', c.N('binary_sensor.vmc_master_spia_velocita_{}_un_solo_avvio_per_programmazione_freeheating'), ['freecooling'], 'Free Heating'], ['Umidità', c.N('binary_sensor.vmc_master_spia_umidita_velocita_{}'), J.f_list(J.chiama(J.attributo(J.leggi(v_nomi, 'nomi'), 'keys')))], ['Black-Out', c.N('binary_sensor.vmc_master_spia_velocita_{}'), J.f_list(J.chiama(J.attributo(J.leggi(v_nomi, 'nomi'), 'keys')))]]
    v_ns = J.namespace(righe=[], viste=[])
    for v_a_1 in J.leggi(v_allerte, 'allerte'):
        for v_k_2 in J.elemento(v_a_1, 2):
            if (((c.timer.is_state(J.f_replace(J.elemento(v_a_1, 1), '{}', v_k_2), 'on') and (v_k_2 != J.leggi(v_att_k, 'att_k'))) and (v_k_2 not in J.attributo(J.leggi(v_ns, 'ns'), 'viste'))) and (not ((J.f_count(v_a_1) > 3) and J.leggi(v_annullata, 'annullata')))):
                J.imposta_ns(J.leggi(v_ns, 'ns'), 'righe', (J.attributo(J.leggi(v_ns, 'ns'), 'righe') + [(J.elemento(v_a_1, 3) if (J.f_count(v_a_1) > 3) else J.elemento(J.leggi(v_nomi, 'nomi'), v_k_2))]))
                J.imposta_ns(J.leggi(v_ns, 'ns'), 'viste', (J.attributo(J.leggi(v_ns, 'ns'), 'viste') + [v_k_2]))
    _o.append(J.testo((J.elemento(J.f_join(J.attributo(J.leggi(v_ns, 'ns'), 'righe'), ' · '), slice(None, 255, None)) if ((J.f_count(J.attributo(J.leggi(v_ns, 'ns'), 'righe')) > 0) and (J.leggi(v_att, 'att') != 'Non disponibile')) else 'Nessuna')))
    return ''.join(_o)


def m1072(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_codici = V.get('codici', J.MANCANTE)
    v_componenti = V.get('componenti', J.MANCANTE)
    v_codice = V.get('codice', J.MANCANTE)
    v_stati = v_codici_base = v_free_h_c = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_codici_base = {'00000': 'Velocità 0', '00001': 'Velocità 1', '00002': 'Velocità 2', '00003': 'Velocità 3', '00004': 'Velocità 4', '00005': 'Iperventilazione', '00006': 'Notturna', '00007': 'Free Cooling'}
    _o.append('\n')
    v_free_h_c = c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling'))
    _o.append(' ')
    if (c.is_state(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'), 'Free Heating') and (J.leggi(v_free_h_c, 'free_h_c') != '[Non Calcolabile]')):
        _o.append('\n  ')
        v_codici = {'00000': 'Velocità 0', '00001': 'Velocità 1', '00002': 'Velocità 2', '00003': 'Velocità 3', '00004': 'Velocità 4', '00005': 'Iperventilazione', '00006': 'Notturna', '00007': 'Free Heating'}
        _o.append('\n')
    elif (c.is_state(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'), 'Free Cooling') and (J.leggi(v_free_h_c, 'free_h_c') != '[Non Calcolabile]')):
        _o.append('\n  ')
        v_codici = J.leggi(v_codici_base, 'codici_base')
        _o.append('\n')
    elif (c.is_state(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'), 'Disabilitata') or (J.leggi(v_free_h_c, 'free_h_c') == '[Non Calcolabile]')):
        _o.append('\n  ')
        v_codici = {'00000': 'Velocità 0', '00001': 'Velocità 1', '00002': 'Velocità 2', '00003': 'Velocità 3', '00004': 'Velocità 4', '00005': 'Iperventilazione', '00006': 'Notturna', '00007': 'Free Cool./Heat.'}
        _o.append('\n')
    else:
        _o.append('\n  ')
        v_codici = J.leggi(v_codici_base, 'codici_base')
        _o.append('\n')
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 1):
            _o.append('\n    ')
            v_codice = J.elemento(J.leggi(v_componenti, 'componenti'), 1)
            _o.extend(('\n    ', J.testo(J.chiama(J.attributo(J.leggi(v_codici, 'codici'), 'get'), J.leggi(v_codice, 'codice'), 'Non disponibile')), '\n  '))
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1073(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_codice = V.get('codice', J.MANCANTE)
    v_stati = v_codici = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_codici = {'00003': 'Spenti', '00001': 'Accesi', '00002': 'Spenti', '00000': 'Accesi'}
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 4):
            _o.append('\n    ')
            v_codice = J.elemento(J.leggi(v_componenti, 'componenti'), 4)
            _o.extend(('\n    ', J.testo(J.chiama(J.attributo(J.leggi(v_codici, 'codici'), 'get'), J.leggi(v_codice, 'codice'), 'Non disponibile')), '\n  '))
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1074(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_codice = V.get('codice', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 14):
            _o.append('\n    ')
            v_codice = J.elemento(J.leggi(v_componenti, 'componenti'), 14)
            _o.append('\n    ')
            if (J.leggi(v_codice, 'codice') == '00000'):
                _o.append('\n      Spento\n    ')
            elif (J.leggi(v_codice, 'codice') == '00032'):
                _o.append('\n      Verificare Filtro\n    ')
            else:
                _o.append('\n      Acceso\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1075(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_first_digit = V.get('first_digit', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_sensori_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 2):
            _o.append('\n    ')
            v_first_digit = J.elemento(J.elemento(J.leggi(v_componenti, 'componenti'), 2), 0)
            _o.append('\n    ')
            if (J.leggi(v_first_digit, 'first_digit') == '1'):
                _o.append('\n      negativo\n    ')
            else:
                _o.append('\n      positivo\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1076(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_first_digit = V.get('first_digit', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_sensori_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 1):
            _o.append('\n    ')
            v_first_digit = J.elemento(J.elemento(J.leggi(v_componenti, 'componenti'), 1), 0)
            _o.append('\n    ')
            if (J.leggi(v_first_digit, 'first_digit') == '1'):
                _o.append('\n      negativo\n    ')
            else:
                _o.append('\n      positivo\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1077(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set temp_ext...
    v_vmc = V.get('vmc', J.MANCANTE)
    v_temp_float = V.get('temp_float', J.MANCANTE)
    v_stati = v_temp_ext = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_temp_ext = c.states(c.N('sensor.vmc_master_temperatura_esterna_selezionata'))
    _o.append(' ')
    if (J.leggi(v_temp_ext, 'temp_ext') in J.leggi(v_stati, 'stati')):
        v_vmc = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), default=None)
        _o.extend(('\n  ', J.testo((J.f_round(J.leggi(v_vmc, 'vmc'), 1) if (not J.t_none(J.leggi(v_vmc, 'vmc'))) else 'Non disponibile')), '\n'))
    else:
        _o.append('\n  ')
        v_temp_float = J.f_float(J.leggi(v_temp_ext, 'temp_ext'), default=None)
        _o.append('\n  ')
        if (J.leggi(v_temp_float, 'temp_float') == None):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.extend(('\n    ', J.testo(J.f_round((J.leggi(v_temp_float, 'temp_float') + J.f_float(c.states(c.N('number.vmc_master_offset_temp_esterna')), 0)), 1)), '\n  '))
        _o.append('\n')
    return ''.join(_o)


def m1078(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set sensor_v...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_raw_temp = V.get('raw_temp', J.MANCANTE)
    v_temp_value = V.get('temp_value', J.MANCANTE)
    v_stati = v_sensor_value = v_temp_sign = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_sensor_value = c.states(c.N('sensor.vmc_master_sensori_memorizzata'))
    _o.append(' ')
    v_temp_sign = c.states(c.N('sensor.vmc_master_temp_esterna_positivo_negativo'))
    _o.append(' ')
    if ((J.leggi(v_sensor_value, 'sensor_value') not in J.leggi(v_stati, 'stati')) and (J.leggi(v_temp_sign, 'temp_sign') in ['positivo', 'negativo'])):
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(J.leggi(v_sensor_value, 'sensor_value'), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 2):
            _o.append('\n    ')
            v_raw_temp = J.elemento(J.leggi(v_componenti, 'componenti'), 2)
            _o.append('\n    ')
            if ((J.chiama(J.attributo(J.leggi(v_raw_temp, 'raw_temp'), 'isdigit')) or (J.chiama(J.attributo(J.leggi(v_raw_temp, 'raw_temp'), 'startswith'), '1') and J.chiama(J.attributo(J.elemento(J.leggi(v_raw_temp, 'raw_temp'), slice(1, None, None)), 'isdigit')))) and (not ((J.leggi(v_temp_sign, 'temp_sign') == 'negativo') and (J.f_length(J.leggi(v_raw_temp, 'raw_temp')) < 2)))):
                if (J.leggi(v_temp_sign, 'temp_sign') == 'negativo'):
                    _o.append('\n        ')
                    v_temp_value = (-J.f_float((J.f_int(J.elemento(J.leggi(v_raw_temp, 'raw_temp'), slice(1, None, None))) / 10)))
                    _o.append('\n      ')
                else:
                    _o.append('\n        ')
                    v_temp_value = J.f_float((J.f_int(J.leggi(v_raw_temp, 'raw_temp')) / 10))
                    _o.append('\n      ')
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_temp_value, 'temp_value'), 1)), '\n    '))
            else:
                _o.append('\n      Non disponibile\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    else:
        _o.append('\n  Non disponibile\n')
    return ''.join(_o)


def m1079(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set temp_int...
    v_vmc = V.get('vmc', J.MANCANTE)
    v_temp_float = V.get('temp_float', J.MANCANTE)
    v_stati = v_temp_int = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_temp_int = c.states(c.N('sensor.vmc_master_temperatura_interna_selezionata'))
    _o.append(' ')
    if (J.leggi(v_temp_int, 'temp_int') in J.leggi(v_stati, 'stati')):
        v_vmc = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_status_senza_offset')), default=None)
        _o.extend(('\n  ', J.testo((J.f_round(J.leggi(v_vmc, 'vmc'), 1) if (not J.t_none(J.leggi(v_vmc, 'vmc'))) else 'Non disponibile')), '\n'))
    else:
        _o.append('\n  ')
        v_temp_float = J.f_float(J.leggi(v_temp_int, 'temp_int'), default=None)
        _o.append('\n  ')
        if (J.leggi(v_temp_float, 'temp_float') == None):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.extend(('\n    ', J.testo(J.f_round((J.leggi(v_temp_float, 'temp_float') + J.f_float(c.states(c.N('number.vmc_master_offset_temp_interna')), 0)), 1)), '\n  '))
        _o.append('\n')
    return ''.join(_o)


def m1080(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set sensor_v...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_raw_temp = V.get('raw_temp', J.MANCANTE)
    v_temp_value = V.get('temp_value', J.MANCANTE)
    v_stati = v_sensor_value = v_temp_sign = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_sensor_value = c.states(c.N('sensor.vmc_master_sensori_memorizzata'))
    _o.append(' ')
    v_temp_sign = c.states(c.N('sensor.vmc_master_temp_interna_positivo_negativo'))
    _o.append(' ')
    if ((J.leggi(v_sensor_value, 'sensor_value') not in J.leggi(v_stati, 'stati')) and (J.leggi(v_temp_sign, 'temp_sign') in ['positivo', 'negativo'])):
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(J.leggi(v_sensor_value, 'sensor_value'), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 1):
            _o.append('\n    ')
            v_raw_temp = J.elemento(J.leggi(v_componenti, 'componenti'), 1)
            _o.append('\n    ')
            if ((J.chiama(J.attributo(J.leggi(v_raw_temp, 'raw_temp'), 'isdigit')) or (J.chiama(J.attributo(J.leggi(v_raw_temp, 'raw_temp'), 'startswith'), '1') and J.chiama(J.attributo(J.elemento(J.leggi(v_raw_temp, 'raw_temp'), slice(1, None, None)), 'isdigit')))) and (not ((J.leggi(v_temp_sign, 'temp_sign') == 'negativo') and (J.f_length(J.leggi(v_raw_temp, 'raw_temp')) < 2)))):
                if (J.leggi(v_temp_sign, 'temp_sign') == 'negativo'):
                    _o.append('\n        ')
                    v_temp_value = (-J.f_float((J.f_int(J.elemento(J.leggi(v_raw_temp, 'raw_temp'), slice(1, None, None))) / 10)))
                    _o.append('\n      ')
                else:
                    _o.append('\n        ')
                    v_temp_value = J.f_float((J.f_int(J.leggi(v_raw_temp, 'raw_temp')) / 10))
                    _o.append('\n      ')
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_temp_value, 'temp_value'), 1)), '\n    '))
            else:
                _o.append('\n      Non disponibile\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    else:
        _o.append('\n  Non disponibile\n')
    return ''.join(_o)


def m1081(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% if states('s...
    v_humidity = V.get('humidity', J.MANCANTE)
    v_umidita_relativa_esterna = V.get('umidita_relativa_esterna', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_umidita_esterna_selezionata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_humidity = c.states(c.N('sensor.vmc_master_umidita_esterna_selezionata'))
        _o.append('\n  ')
        if J.t_none(J.f_float(J.leggi(v_humidity, 'humidity'), default=None)):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.append('\n    ')
            v_umidita_relativa_esterna = (J.f_float(J.leggi(v_humidity, 'humidity'), 0) + J.f_float(c.states(c.N('number.vmc_master_offset_umidita_esterna')), 0))
            _o.append('\n    ')
            if ((J.leggi(v_umidita_relativa_esterna, 'umidita_relativa_esterna') > 0) and (J.leggi(v_umidita_relativa_esterna, 'umidita_relativa_esterna') <= 100)):
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_umidita_relativa_esterna, 'umidita_relativa_esterna'), 1)), '\n    '))
            elif (J.leggi(v_umidita_relativa_esterna, 'umidita_relativa_esterna') <= 0):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.append('\n      100\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1082(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set umidita_...
    v_vmc = V.get('vmc', J.MANCANTE)
    v_umidita_float = V.get('umidita_float', J.MANCANTE)
    v_umidita_relativa = V.get('umidita_relativa', J.MANCANTE)
    v_stati = v_umidita_int = v_offset = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_umidita_int = c.states(c.N('sensor.vmc_master_umidita_interna_selezionata'))
    _o.append(' ')
    v_offset = J.f_float(c.states(c.N('number.vmc_master_offset_umidita_interna')), 0)
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_umidita_interna_selezionata')) in J.leggi(v_stati, 'stati')):
        v_vmc = J.f_float(c.states(c.N('sensor.vmc_master_umidita_interna_status_senza_offset')), default=None)
        _o.extend(('\n  ', J.testo((J.f_round(J.leggi(v_vmc, 'vmc'), 1) if (not J.t_none(J.leggi(v_vmc, 'vmc'))) else 'Non disponibile')), '\n'))
    else:
        _o.append('\n  ')
        v_umidita_float = J.f_float(J.leggi(v_umidita_int, 'umidita_int'), default=None)
        _o.append('\n  ')
        if J.t_none(J.leggi(v_umidita_float, 'umidita_float')):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.append('\n    ')
            v_umidita_relativa = (J.leggi(v_umidita_float, 'umidita_float') + J.leggi(v_offset, 'offset'))
            _o.append('\n    ')
            if (J.leggi(v_umidita_relativa, 'umidita_relativa') > 100):
                _o.append('\n      100\n    ')
            elif (J.leggi(v_umidita_relativa, 'umidita_relativa') <= 0):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_umidita_relativa, 'umidita_relativa'), 1)), '\n    '))
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1083(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set dati_sen...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_umidita_relativa = V.get('umidita_relativa', J.MANCANTE)
    v_stati = v_dati_sensori = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_dati_sensori = c.states(c.N('sensor.vmc_master_sensori_memorizzata'))
    _o.append(' ')
    if (J.leggi(v_dati_sensori, 'dati_sensori') in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(J.leggi(v_dati_sensori, 'dati_sensori'), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 3):
            _o.append('\n    ')
            v_umidita_relativa = (J.f_float(J.elemento(J.leggi(v_componenti, 'componenti'), 3), 0) / 10)
            _o.append('\n    ')
            if (J.leggi(v_umidita_relativa, 'umidita_relativa') > 100):
                _o.append('\n      100\n    ')
            elif (J.leggi(v_umidita_relativa, 'umidita_relativa') <= 0):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_umidita_relativa, 'umidita_relativa'), 1)), '\n    '))
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1084(c, V):
    # {% set stati = ['unknown', 'unavailable', '-100', 'Non disponibile'] %} {% set co2_int ...
    v_vmc = V.get('vmc', J.MANCANTE)
    v_co2_float = V.get('co2_float', J.MANCANTE)
    v_co2_with_offset = V.get('co2_with_offset', J.MANCANTE)
    v_stati = v_co2_int = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable', '-100', 'Non disponibile']
    _o.append(' ')
    v_co2_int = c.states(c.N('sensor.vmc_master_co2_interna_selezionata'))
    _o.append(' ')
    if (J.leggi(v_co2_int, 'co2_int') in J.leggi(v_stati, 'stati')):
        v_vmc = J.f_float(c.states(c.N('sensor.vmc_master_co2_status_senza_offset')), default=None)
        _o.append('\n  ')
        if ((not J.t_none(J.leggi(v_vmc, 'vmc'))) and (J.leggi(v_vmc, 'vmc') > 0)):
            _o.extend(('\n    ', J.testo(J.f_round(J.leggi(v_vmc, 'vmc'), 0)), '\n  '))
        elif (J.leggi(v_co2_int, 'co2_int') == '-100'):
            _o.append('\n    -\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    else:
        _o.append('\n  ')
        v_co2_float = J.f_float(J.leggi(v_co2_int, 'co2_int'), default=0)
        _o.append('\n  ')
        v_co2_with_offset = J.f_round((J.leggi(v_co2_float, 'co2_float') + J.f_float(c.states(c.N('number.vmc_master_offset_co2')), default=0)), 0)
        if (J.leggi(v_co2_with_offset, 'co2_with_offset') == 0):
            _o.append('\n    -\n  ')
        elif (J.leggi(v_co2_with_offset, 'co2_with_offset') > 0):
            _o.extend(('\n    ', J.testo(J.leggi(v_co2_with_offset, 'co2_with_offset')), '\n  '))
        elif (J.leggi(v_co2_with_offset, 'co2_with_offset') < 0):
            _o.append('\n    -\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1085(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_co2 = V.get('co2', J.MANCANTE)
    v_stati = v_dati_sensori = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_dati_sensori = c.states(c.N('sensor.vmc_master_sensori_memorizzata'))
    _o.append(' ')
    if (J.leggi(v_dati_sensori, 'dati_sensori') in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(J.leggi(v_dati_sensori, 'dati_sensori'), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 4):
            _o.append('\n    ')
            v_co2 = J.f_float(J.elemento(J.leggi(v_componenti, 'componenti'), 4), 0)
            _o.append('\n    ')
            if (J.leggi(v_co2, 'co2') > 0):
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_co2, 'co2'), 0)), '\n    '))
            else:
                _o.append('\n      -\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1086(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_voc = V.get('voc', J.MANCANTE)
    v_stati = v_dati_sensori = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_dati_sensori = c.states(c.N('sensor.vmc_master_sensori_memorizzata'))
    _o.append(' ')
    if (J.leggi(v_dati_sensori, 'dati_sensori') in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(J.leggi(v_dati_sensori, 'dati_sensori'), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 11):
            _o.append('\n    ')
            v_voc = (J.f_float(J.elemento(J.leggi(v_componenti, 'componenti'), 11), 0) + J.f_float(c.states(c.N('number.vmc_master_offset_voc')), 0))
            if (J.leggi(v_voc, 'voc') > 0):
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_voc, 'voc'), 0)), '\n    '))
            else:
                _o.append('\n      -\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1087(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_voc = V.get('voc', J.MANCANTE)
    v_stati = v_dati_sensori = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_dati_sensori = c.states(c.N('sensor.vmc_master_sensori_memorizzata'))
    _o.append(' ')
    if (J.leggi(v_dati_sensori, 'dati_sensori') in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(J.leggi(v_dati_sensori, 'dati_sensori'), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 11):
            _o.append('\n    ')
            v_voc = J.f_float(J.elemento(J.leggi(v_componenti, 'componenti'), 11), 0)
            _o.append('\n    ')
            if (J.leggi(v_voc, 'voc') > 0):
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_voc, 'voc'), 0)), '\n    '))
            else:
                _o.append('\n      -\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    Non disponibile\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1088(c, V):
    # {{ is_number(states('sensor.vmc_master_temp_esterna_status')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_temp_esterna_status')))))
    return ''.join(_o)


def m1089(c, V):
    # {{ states('sensor.vmc_master_temp_esterna_status') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_temp_esterna_status'))))
    return ''.join(_o)


def m1090(c, V):
    # {{ is_number(states('sensor.vmc_master_temp_interna_status')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_temp_interna_status')))))
    return ''.join(_o)


def m1091(c, V):
    # {{ states('sensor.vmc_master_temp_interna_status') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_temp_interna_status'))))
    return ''.join(_o)


def m1092(c, V):
    # {{ is_number(states('sensor.vmc_master_umidita_esterna_status')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_umidita_esterna_status')))))
    return ''.join(_o)


def m1093(c, V):
    # {{ states('sensor.vmc_master_umidita_esterna_status') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_umidita_esterna_status'))))
    return ''.join(_o)


def m1094(c, V):
    # {{ is_number(states('sensor.vmc_master_umidita_interna_status')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_umidita_interna_status')))))
    return ''.join(_o)


def m1095(c, V):
    # {{ states('sensor.vmc_master_umidita_interna_status') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status'))))
    return ''.join(_o)


def m1096(c, V):
    # {{ is_number(states('sensor.vmc_master_co2_status')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_co2_status')))))
    return ''.join(_o)


def m1097(c, V):
    # {{ states('sensor.vmc_master_co2_status') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_co2_status'))))
    return ''.join(_o)


def m1098(c, V):
    # {{ is_number(states('sensor.vmc_master_voc_status')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_voc_status')))))
    return ''.join(_o)


def m1099(c, V):
    # {{ states('sensor.vmc_master_voc_status') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_voc_status'))))
    return ''.join(_o)


def m1100(c, V):
    # {{ is_number(states('sensor.vmc_master_punto_di_rugiada_esterno')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_punto_di_rugiada_esterno')))))
    return ''.join(_o)


def m1101(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_esterno') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_punto_di_rugiada_esterno'))))
    return ''.join(_o)


def m1102(c, V):
    # {{ is_number(states('sensor.vmc_master_punto_di_rugiada_interno')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno')))))
    return ''.join(_o)


def m1103(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_interno') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno'))))
    return ''.join(_o)


def m1104(c, V):
    # {{ is_number(states('sensor.vmc_master_punto_di_rugiada_valore')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_punto_di_rugiada_valore')))))
    return ''.join(_o)


def m1105(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_valore') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_punto_di_rugiada_valore'))))
    return ''.join(_o)


def m1106(c, V):
    # {{ is_number(states('sensor.vmc_master_umidita_assoluta_esterna')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_umidita_assoluta_esterna')))))
    return ''.join(_o)


def m1107(c, V):
    # {{ states('sensor.vmc_master_umidita_assoluta_esterna') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_umidita_assoluta_esterna'))))
    return ''.join(_o)


def m1108(c, V):
    # {{ is_number(states('sensor.vmc_master_umidita_assoluta_interna')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_umidita_assoluta_interna')))))
    return ''.join(_o)


def m1109(c, V):
    # {{ states('sensor.vmc_master_umidita_assoluta_interna') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_umidita_assoluta_interna'))))
    return ''.join(_o)


def m1110(c, V):
    # {{ is_number(states('sensor.vmc_master_temp_esterna_status_senza_offset')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')))))
    return ''.join(_o)


def m1111(c, V):
    # {{ states('sensor.vmc_master_temp_esterna_status_senza_offset') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset'))))
    return ''.join(_o)


def m1112(c, V):
    # {{ is_number(states('sensor.vmc_master_temp_interna_status_senza_offset')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_temp_interna_status_senza_offset')))))
    return ''.join(_o)


def m1113(c, V):
    # {{ states('sensor.vmc_master_temp_interna_status_senza_offset') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_temp_interna_status_senza_offset'))))
    return ''.join(_o)


def m1114(c, V):
    # {{ is_number(states('sensor.vmc_master_umidita_interna_status_senza_offset')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_umidita_interna_status_senza_offset')))))
    return ''.join(_o)


def m1115(c, V):
    # {{ states('sensor.vmc_master_umidita_interna_status_senza_offset') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status_senza_offset'))))
    return ''.join(_o)


def m1116(c, V):
    # {{ is_number(states('sensor.vmc_master_co2_status_senza_offset')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_co2_status_senza_offset')))))
    return ''.join(_o)


def m1117(c, V):
    # {{ states('sensor.vmc_master_co2_status_senza_offset') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_co2_status_senza_offset'))))
    return ''.join(_o)


def m1118(c, V):
    # {{ is_number(states('sensor.vmc_master_voc_status_senza_offset')) }}
    _o = []
    _o.append(J.testo(J.f_is_number(c.states(c.N('sensor.vmc_master_voc_status_senza_offset')))))
    return ''.join(_o)


def m1119(c, V):
    # {{ states('sensor.vmc_master_voc_status_senza_offset') }}
    _o = []
    _o.append(J.testo(c.states(c.N('sensor.vmc_master_voc_status_senza_offset'))))
    return ''.join(_o)


def m1120(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_umidita_soglia_float = V.get('umidita_soglia_float', J.MANCANTE)
    v_stati = v_umidita_soglia = v_umidita_soglia_limite = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_umidita_soglia = c.states(c.N('sensor.vmc_master_umidita_interna_status'))
    _o.append(' ')
    v_umidita_soglia_limite = J.f_float(c.states(c.N('number.vmc_master_umidita_avvio')), 65)
    _o.append(' ')
    if (J.leggi(v_umidita_soglia, 'umidita_soglia') in J.leggi(v_stati, 'stati')):
        _o.append('\n  [Non Calcolabile]\n')
    else:
        _o.append('\n  ')
        v_umidita_soglia_float = J.f_float(J.leggi(v_umidita_soglia, 'umidita_soglia'), default=None)
        _o.append('\n  ')
        if J.t_none(J.leggi(v_umidita_soglia_float, 'umidita_soglia_float')):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.append('\n    ')
            if ((J.leggi(v_umidita_soglia_float, 'umidita_soglia_float') >= 1) and (J.leggi(v_umidita_soglia_float, 'umidita_soglia_float') <= 35)):
                _o.extend(('\n      UMIDITÀ AL ', J.testo(J.leggi(v_umidita_soglia_float, 'umidita_soglia_float')), "%. POSSIBILE SECCHEZZA, DISIDRATAZIONE. SI CONSIGLIA DI UMIDIFICARE L'AMBIENTE.\n    "))
            elif ((J.leggi(v_umidita_soglia_float, 'umidita_soglia_float') > 35) and (J.leggi(v_umidita_soglia_float, 'umidita_soglia_float') < J.leggi(v_umidita_soglia_limite, 'umidita_soglia_limite'))):
                _o.extend(('\n      UMIDITÀ AL ', J.testo(J.leggi(v_umidita_soglia_float, 'umidita_soglia_float')), '%. SITUAZIONE NORMALE.\n    '))
            elif ((J.leggi(v_umidita_soglia_float, 'umidita_soglia_float') >= J.leggi(v_umidita_soglia_limite, 'umidita_soglia_limite')) and (J.leggi(v_umidita_soglia_float, 'umidita_soglia_float') <= 100)):
                _o.extend(('\n      UMIDITÀ AL ', J.testo(J.leggi(v_umidita_soglia_float, 'umidita_soglia_float')), "%. POTREBBE VERIFICARSI UNA PROLIFERAZIONE DI MUFFE E BATTERI. SI CONSIGLIA DI DEUMIDIFICARE L'AMBIENTE.\n    "))
            else:
                _o.append('\n      [Non Calcolabile]\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1121(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_PdRi_str = V.get('PdRi_str', J.MANCANTE)
    v_PdRe_str = V.get('PdRe_str', J.MANCANTE)
    v_calcolabilita = V.get('calcolabilita', J.MANCANTE)
    v_PdRi_val = V.get('PdRi_val', J.MANCANTE)
    v_PdRe_val = V.get('PdRe_val', J.MANCANTE)
    v_Delta = V.get('Delta', J.MANCANTE)
    v_diff_esatta = V.get('diff_esatta', J.MANCANTE)
    v_diff = V.get('diff', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.extend(('\n  ', '\n  '))
        v_PdRi_str = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno'))
        _o.append('\n  ')
        v_PdRe_str = c.states(c.N('sensor.vmc_master_punto_di_rugiada_esterno'))
        _o.append('\n  ')
        v_calcolabilita = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno_esterno_non_calcolabile'))
        _o.extend(('\n  \n  ', '\n  '))
        if (J.leggi(v_calcolabilita, 'calcolabilita') == '[Non Calcolabile]'):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.extend(('\n    ', '\n    '))
            if ((J.leggi(v_PdRi_str, 'PdRi_str') in ['Non disponibile']) or (J.leggi(v_PdRe_str, 'PdRe_str') in ['Non disponibile'])):
                _o.append('\n      Non disponibile\n    ')
            elif ((J.leggi(v_PdRi_str, 'PdRi_str') == '[Non Calcolabile]') or (J.leggi(v_PdRe_str, 'PdRe_str') == '[Non Calcolabile]')):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.extend(('\n      ', '\n      '))
                v_PdRi_val = J.f_float(J.leggi(v_PdRi_str, 'PdRi_str'), default=None)
                _o.append('\n      ')
                v_PdRe_val = J.f_float(J.leggi(v_PdRe_str, 'PdRe_str'), default=None)
                _o.extend(('\n      \n      ', '\n      '))
                if (J.t_none(J.leggi(v_PdRi_val, 'PdRi_val')) or J.t_none(J.leggi(v_PdRe_val, 'PdRe_val'))):
                    _o.append('\n        [Non Calcolabile]\n      ')
                else:
                    _o.extend(('\n        ', '\n        '))
                    v_Delta = J.f_float(c.states(c.N('number.vmc_master_offset_verifica_impiego_vmc')), default=None)
                    _o.extend(('\n        \n        ', '\n        '))
                    if J.t_none(J.leggi(v_Delta, 'Delta')):
                        _o.append('\n          [Non Calcolabile]\n        ')
                    else:
                        v_diff_esatta = J.f_round((J.leggi(v_PdRe_val, 'PdRe_val') - J.leggi(v_PdRi_val, 'PdRi_val')), 2)
                        _o.append('\n          ')
                        v_diff = J.f_round(J.leggi(v_diff_esatta, 'diff_esatta'), 2)
                        _o.append('\n          ')
                        if (J.leggi(v_diff_esatta, 'diff_esatta') < J.leggi(v_Delta, 'Delta')):
                            _o.extend(('\n            Δ PUNTO DI RUGIADA RILEVATO ', J.testo(J.leggi(v_diff, 'diff')), ' °C, MINORE DEL VALORE IMPOSTATO (', J.testo(J.leggi(v_Delta, 'Delta')), ' °C).\n          '))
                        elif (J.leggi(v_diff_esatta, 'diff_esatta') == J.leggi(v_Delta, 'Delta')):
                            _o.extend(('\n            Δ PUNTO DI RUGIADA RILEVATO ', J.testo(J.leggi(v_diff, 'diff')), ' °C, UGUALE AL VALORE IMPOSTATO (', J.testo(J.leggi(v_Delta, 'Delta')), ' °C).\n          '))
                        else:
                            _o.extend(('\n            Δ PUNTO DI RUGIADA RILEVATO ', J.testo(J.leggi(v_diff, 'diff')), ' °C, MAGGIORE DEL VALORE IMPOSTATO (', J.testo(J.leggi(v_Delta, 'Delta')), ' °C).\n          '))
                        _o.append('\n        ')
                    _o.append('\n      ')
                _o.append('\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1122(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_PdRi_str = V.get('PdRi_str', J.MANCANTE)
    v_PdRe_str = V.get('PdRe_str', J.MANCANTE)
    v_calcolabilita = V.get('calcolabilita', J.MANCANTE)
    v_PdRi_val = V.get('PdRi_val', J.MANCANTE)
    v_PdRe_val = V.get('PdRe_val', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_PdRi_str = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno'))
        _o.append('\n  ')
        v_PdRe_str = c.states(c.N('sensor.vmc_master_punto_di_rugiada_esterno'))
        _o.append('\n  ')
        v_calcolabilita = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno_esterno_non_calcolabile'))
        _o.extend(('\n\n  ', '\n  '))
        if (J.leggi(v_calcolabilita, 'calcolabilita') == 'Non disponibile'):
            _o.append('\n    Non disponibile\n  ')
        elif (J.leggi(v_calcolabilita, 'calcolabilita') == '[Non Calcolabile]'):
            _o.append('\n    [Non Calcolabile]\n  ')
        elif (J.leggi(v_calcolabilita, 'calcolabilita') == 'Si può impiegare'):
            _o.extend(('\n    ', '\n    '))
            if ((J.leggi(v_PdRi_str, 'PdRi_str') == 'Non disponibile') or (J.leggi(v_PdRe_str, 'PdRe_str') == 'Non disponibile')):
                _o.append('\n      Non disponibile\n    ')
            elif ((J.leggi(v_PdRi_str, 'PdRi_str') == '[Non Calcolabile]') or (J.leggi(v_PdRe_str, 'PdRe_str') == '[Non Calcolabile]')):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.append('\n      ')
                v_PdRi_val = J.f_float(J.leggi(v_PdRi_str, 'PdRi_str'), default=None)
                _o.append('\n      ')
                v_PdRe_val = J.f_float(J.leggi(v_PdRe_str, 'PdRe_str'), default=None)
                _o.append('\n      \n      ')
                if (J.t_none(J.leggi(v_PdRi_val, 'PdRi_val')) or J.t_none(J.leggi(v_PdRe_val, 'PdRe_val'))):
                    _o.append('\n        [Non Calcolabile]\n      ')
                else:
                    _o.extend(('\n        ', J.testo(J.f_round((J.leggi(v_PdRe_val, 'PdRe_val') - J.leggi(v_PdRi_val, 'PdRi_val')), 2)), '\n      '))
                _o.append('\n    ')
            _o.append('\n  ')
        else:
            _o.extend(('\n    ', '\n    [Non Calcolabile]\n  '))
        _o.append('\n')
    return ''.join(_o)


def m1123(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_umidita_soglia = V.get('umidita_soglia', J.MANCANTE)
    v_umidita_soglia_limite = V.get('umidita_soglia_limite', J.MANCANTE)
    v_umidita_float = V.get('umidita_float', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_umidita_soglia = c.states(c.N('sensor.vmc_master_umidita_interna_status'))
        _o.append('\n  ')
        v_umidita_soglia_limite = J.f_float(c.states(c.N('number.vmc_master_umidita_avvio')), 65)
        _o.append('\n  ')
        if (J.leggi(v_umidita_soglia, 'umidita_soglia') not in ['unknown', 'unavailable', '[Non Calcolabile]']):
            _o.append('\n    ')
            v_umidita_float = J.f_float(J.leggi(v_umidita_soglia, 'umidita_soglia'), default=None)
            _o.append('\n    ')
            if J.t_none(J.leggi(v_umidita_float, 'umidita_float')):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.append('\n      ')
                if ((J.leggi(v_umidita_float, 'umidita_float') >= 1) and (J.leggi(v_umidita_float, 'umidita_float') <= 35)):
                    _o.append('\n        Possibile Secchezza, Disidratazione\n      ')
                elif ((J.leggi(v_umidita_float, 'umidita_float') > 35) and (J.leggi(v_umidita_float, 'umidita_float') < J.leggi(v_umidita_soglia_limite, 'umidita_soglia_limite'))):
                    _o.append('\n        Normale\n      ')
                elif ((J.leggi(v_umidita_float, 'umidita_float') >= J.leggi(v_umidita_soglia_limite, 'umidita_soglia_limite')) and (J.leggi(v_umidita_float, 'umidita_float') <= 100)):
                    _o.append('\n        Possibile Muffe, Batteri\n      ')
                else:
                    _o.append('\n        [Non Calcolabile]\n      ')
                _o.append('\n    ')
            _o.append('\n  ')
        else:
            _o.append('\n    [Non Calcolabile]\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1124(c, V):
    # {% set co2_raw = states('sensor.vmc_master_co2_status') %} {% set stati = ["sconosciuto...
    v_co2 = V.get('co2', J.MANCANTE)
    v_co2_raw = v_stati = J.MANCANTE
    _o = []
    v_co2_raw = c.states(c.N('sensor.vmc_master_co2_status'))
    _o.append(' ')
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        if (J.leggi(v_co2_raw, 'co2_raw') == '-'):
            _o.append('\n    -\n  ')
        else:
            _o.append('\n    ')
            v_co2 = J.f_float(J.leggi(v_co2_raw, 'co2_raw'), default=None)
            _o.append('\n    ')
            if J.t_none(J.leggi(v_co2, 'co2')):
                _o.append('\n      [Non Disponibile]\n    ')
            elif (J.leggi(v_co2, 'co2') <= 0):
                _o.append('\n      -\n    ')
            elif ((J.leggi(v_co2, 'co2') > 0) and (J.leggi(v_co2, 'co2') <= 800)):
                _o.append('\n      Bassa Concentrazione\n    ')
            elif ((J.leggi(v_co2, 'co2') > 800) and (J.leggi(v_co2, 'co2') <= 1000)):
                _o.append('\n      Moderata Concentrazione\n    ')
            elif ((J.leggi(v_co2, 'co2') > 1000) and (J.leggi(v_co2, 'co2') < 1400)):
                _o.append('\n      Alta Concentrazione\n    ')
            else:
                _o.append('\n      Pessima Concentrazione\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1125(c, V):
    # {% set voc_raw = states('sensor.vmc_master_voc_status') %} {% set stati = ["sconosciuto...
    v_voc = V.get('voc', J.MANCANTE)
    v_voc_raw = v_stati = J.MANCANTE
    _o = []
    v_voc_raw = c.states(c.N('sensor.vmc_master_voc_status'))
    _o.append(' ')
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        if (J.leggi(v_voc_raw, 'voc_raw') == '-'):
            _o.append('\n    -\n  ')
        else:
            _o.append('\n    ')
            v_voc = J.f_float(J.leggi(v_voc_raw, 'voc_raw'), default=None)
            _o.append('\n    ')
            if J.t_none(J.leggi(v_voc, 'voc')):
                _o.append('\n      [Non Disponibile]\n    ')
            elif (J.leggi(v_voc, 'voc') <= 0):
                _o.append('\n      -\n    ')
            elif ((J.leggi(v_voc, 'voc') > 0) and (J.leggi(v_voc, 'voc') <= 300)):
                _o.append('\n      Bassa Concentrazione\n    ')
            elif ((J.leggi(v_voc, 'voc') > 300) and (J.leggi(v_voc, 'voc') <= 600)):
                _o.append('\n      Moderata Concentrazione\n    ')
            else:
                _o.append('\n      Pessima Concentrazione\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1126(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_congelamento = V.get('congelamento', J.MANCANTE)
    v_congelamento_vmc = V.get('congelamento_vmc', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_congelamento = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), default=None)
        _o.append('\n  ')
        v_congelamento_vmc = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), default=None)
        if (J.t_none(J.leggi(v_congelamento, 'congelamento')) and J.t_none(J.leggi(v_congelamento_vmc, 'congelamento_vmc'))):
            _o.append('\n    [Non Disponibile]\n  ')
        elif (((not J.t_none(J.leggi(v_congelamento, 'congelamento'))) and (J.leggi(v_congelamento, 'congelamento') <= (-18))) or ((not J.t_none(J.leggi(v_congelamento_vmc, 'congelamento_vmc'))) and (J.leggi(v_congelamento_vmc, 'congelamento_vmc') <= (-18)))):
            _o.append('\n    Si\n  ')
        elif ((((not J.t_none(J.leggi(v_congelamento, 'congelamento'))) and (J.leggi(v_congelamento, 'congelamento') > (-18))) and (J.leggi(v_congelamento, 'congelamento') <= (-15))) or (((not J.t_none(J.leggi(v_congelamento_vmc, 'congelamento_vmc'))) and (J.leggi(v_congelamento_vmc, 'congelamento_vmc') > (-18))) and (J.leggi(v_congelamento_vmc, 'congelamento_vmc') <= (-15)))):
            _o.append('\n    [No ma Prossimo]\n  ')
        else:
            _o.append('\n    No\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1127(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_temperatura_esterna = V.get('temperatura_esterna', J.MANCANTE)
    v_temperatura_interna = V.get('temperatura_interna', J.MANCANTE)
    v_temperatura_esterna_vmc = V.get('temperatura_esterna_vmc', J.MANCANTE)
    v_temperatura_interna_vmc = V.get('temperatura_interna_vmc', J.MANCANTE)
    v_congelamento = V.get('congelamento', J.MANCANTE)
    v_congelamento_vmc = V.get('congelamento_vmc', J.MANCANTE)
    v_delta = V.get('delta', J.MANCANTE)
    v_delta_vmc = V.get('delta_vmc', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_temperatura_esterna = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), default=None)
        _o.append('\n  ')
        v_temperatura_interna = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_status')), default=None)
        _o.append('\n  ')
        v_temperatura_esterna_vmc = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), default=None)
        _o.append('\n  ')
        v_temperatura_interna_vmc = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_status_senza_offset')), default=None)
        _o.append('\n  ')
        v_congelamento = J.leggi(v_temperatura_esterna, 'temperatura_esterna')
        _o.append('\n  ')
        v_congelamento_vmc = J.leggi(v_temperatura_esterna_vmc, 'temperatura_esterna_vmc')
        v_delta = (J.f_round((J.leggi(v_temperatura_interna, 'temperatura_interna') - J.leggi(v_temperatura_esterna, 'temperatura_esterna')), 1) if ((not J.t_none(J.leggi(v_temperatura_interna, 'temperatura_interna'))) and (not J.t_none(J.leggi(v_temperatura_esterna, 'temperatura_esterna')))) else None)
        _o.append('\n  ')
        v_delta_vmc = (J.f_round((J.leggi(v_temperatura_interna_vmc, 'temperatura_interna_vmc') - J.leggi(v_temperatura_esterna_vmc, 'temperatura_esterna_vmc')), 1) if ((not J.t_none(J.leggi(v_temperatura_interna_vmc, 'temperatura_interna_vmc'))) and (not J.t_none(J.leggi(v_temperatura_esterna_vmc, 'temperatura_esterna_vmc')))) else None)
        _o.append('\n  ')
        if (J.t_none(J.leggi(v_delta, 'delta')) and J.t_none(J.leggi(v_delta_vmc, 'delta_vmc'))):
            _o.append('\n    [Non Disponibile]\n  ')
        elif (((not J.t_none(J.leggi(v_congelamento, 'congelamento'))) and (J.leggi(v_congelamento, 'congelamento') <= (-18))) or ((not J.t_none(J.leggi(v_congelamento_vmc, 'congelamento_vmc'))) and (J.leggi(v_congelamento_vmc, 'congelamento_vmc') <= (-18)))):
            _o.append('\n    -                                                               \n  ')
        else:
            _o.append('\n    ')
            if (((not J.t_none(J.leggi(v_delta, 'delta'))) and (J.leggi(v_delta, 'delta') > 23)) or ((not J.t_none(J.leggi(v_delta_vmc, 'delta_vmc'))) and (J.leggi(v_delta_vmc, 'delta_vmc') > 23))):
                _o.append('\n      Si\n    ')
            elif ((((not J.t_none(J.leggi(v_delta, 'delta'))) and (J.leggi(v_delta, 'delta') >= 20)) and (J.leggi(v_delta, 'delta') <= 23)) or (((not J.t_none(J.leggi(v_delta_vmc, 'delta_vmc'))) and (J.leggi(v_delta_vmc, 'delta_vmc') >= 20)) and (J.leggi(v_delta_vmc, 'delta_vmc') <= 23))):
                _o.append('\n      [No ma Prossimo]\n    ')
            else:
                _o.append('\n      No\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1128(c, V):
    # {% set stati = ['unknown','unavailable'] %} {% if states('sensor.vmc_master_sensori_mem...
    v_Rh = V.get('Rh', J.MANCANTE)
    v_Tc = V.get('Tc', J.MANCANTE)
    v_Es = V.get('Es', J.MANCANTE)
    v_E = V.get('E', J.MANCANTE)
    v_Dp = V.get('Dp', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['unknown', 'unavailable']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_Rh = J.f_float(c.states(c.N('sensor.vmc_master_umidita_interna_status')), default=None)
        _o.append('\n  ')
        v_Tc = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_status')), default=None)
        _o.append('\n  ')
        if (J.t_none(J.leggi(v_Rh, 'Rh')) or J.t_none(J.leggi(v_Tc, 'Tc'))):
            _o.append('\n    [Non Disponibile]\n  ')
        else:
            _o.append('\n    ')
            v_Es = (6.11 * (10 ** ((7.5 * J.leggi(v_Tc, 'Tc')) / (237.7 + J.leggi(v_Tc, 'Tc')))))
            _o.append('\n    ')
            v_E = ((J.leggi(v_Es, 'Es') * J.leggi(v_Rh, 'Rh')) / 100)
            _o.append('\n    ')
            if (((J.leggi(v_Rh, 'Rh') > 0) and (J.leggi(v_Rh, 'Rh') <= 100)) and (J.leggi(v_E, 'E') > 0)):
                _o.append('\n      ')
                v_Dp = (((-430.22) + (237.7 * J.log(J.leggi(v_E, 'E')))) / ((-J.log(J.leggi(v_E, 'E'))) + 19.08))
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_Dp, 'Dp'), 2)), '\n    '))
            else:
                _o.append('\n      [Non Calcolabile]\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1129(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_Rh = V.get('Rh', J.MANCANTE)
    v_Tc = V.get('Tc', J.MANCANTE)
    v_Es = V.get('Es', J.MANCANTE)
    v_E = V.get('E', J.MANCANTE)
    v_Dp = V.get('Dp', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_Rh = J.f_float(c.states(c.N('sensor.vmc_master_umidita_esterna_status')), default=None)
        _o.append('\n  ')
        v_Tc = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), default=None)
        _o.append('\n\n  ')
        if (J.t_none(J.leggi(v_Rh, 'Rh')) or J.t_none(J.leggi(v_Tc, 'Tc'))):
            _o.append('\n    [Non Disponibile]\n  ')
        else:
            _o.append('\n    ')
            v_Es = (6.11 * (10 ** ((7.5 * J.leggi(v_Tc, 'Tc')) / (237.7 + J.leggi(v_Tc, 'Tc')))))
            _o.append('\n    ')
            v_E = ((J.leggi(v_Es, 'Es') * J.leggi(v_Rh, 'Rh')) / 100)
            _o.append('\n\n    ')
            if (((J.leggi(v_Rh, 'Rh') > 0) and (J.leggi(v_Rh, 'Rh') <= 100)) and (J.leggi(v_E, 'E') > 0)):
                _o.append('\n      ')
                v_Dp = (((-430.22) + (237.7 * J.log(J.leggi(v_E, 'E')))) / ((-J.log(J.leggi(v_E, 'E'))) + 19.08))
                _o.extend(('\n      ', J.testo(J.f_round(J.leggi(v_Dp, 'Dp'), 2)), '\n    '))
            else:
                _o.append('\n      [Non Calcolabile]\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1130(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_PdRi = V.get('PdRi', J.MANCANTE)
    v_PdRe = V.get('PdRe', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_PdRi = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno'))
        _o.append('\n  ')
        v_PdRe = c.states(c.N('sensor.vmc_master_punto_di_rugiada_esterno'))
        _o.append('\n  \n  ')
        if ((J.leggi(v_PdRi, 'PdRi') == '[Non Calcolabile]') or (J.leggi(v_PdRe, 'PdRe') == '[Non Calcolabile]')):
            _o.append('\n    [Non Calcolabile]\n  ')
        elif ((J.leggi(v_PdRi, 'PdRi') in ['Non disponibile', '[Non Disponibile]']) or (J.leggi(v_PdRe, 'PdRe') in ['Non disponibile', '[Non Disponibile]'])):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.append('\n    Si può impiegare\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1131(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_PdRi = V.get('PdRi', J.MANCANTE)
    v_PdRe = V.get('PdRe', J.MANCANTE)
    v_Delta = V.get('Delta', J.MANCANTE)
    v_calcolabile = V.get('calcolabile', J.MANCANTE)
    v_PdRi_val = V.get('PdRi_val', J.MANCANTE)
    v_PdRe_val = V.get('PdRe_val', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_PdRi = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno'))
        _o.append('\n  ')
        v_PdRe = c.states(c.N('sensor.vmc_master_punto_di_rugiada_esterno'))
        _o.append('\n  ')
        v_Delta = J.f_float(c.states(c.N('number.vmc_master_offset_verifica_impiego_vmc')), default=None)
        _o.append('\n  ')
        v_calcolabile = c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno_esterno_non_calcolabile'))
        _o.append('\n  ')
        if (J.leggi(v_calcolabile, 'calcolabile') == '[Non Calcolabile]'):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.append('\n    ')
            v_PdRi_val = J.f_float(J.leggi(v_PdRi, 'PdRi'), default=None)
            _o.append('\n    ')
            v_PdRe_val = J.f_float(J.leggi(v_PdRe, 'PdRe'), default=None)
            _o.append('\n    ')
            if ((J.t_none(J.leggi(v_PdRi_val, 'PdRi_val')) or J.t_none(J.leggi(v_PdRe_val, 'PdRe_val'))) or J.t_none(J.leggi(v_Delta, 'Delta'))):
                _o.append('\n      [Non Disponibile]\n    ')
            else:
                if (J.f_round((J.leggi(v_PdRe_val, 'PdRe_val') - J.leggi(v_PdRi_val, 'PdRi_val')), 2) < J.leggi(v_Delta, 'Delta')):
                    _o.append('\n        Si può impiegare\n      ')
                else:
                    _o.append("\n        Se ne sconsiglia l'impiego\n      ")
                _o.append('\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1132(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_h_str = V.get('h_str', J.MANCANTE)
    v_t_str = V.get('t_str', J.MANCANTE)
    v_h_val = V.get('h_val', J.MANCANTE)
    v_t_val = V.get('t_val', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_h_str = c.states(c.N('sensor.vmc_master_umidita_interna_status'))
        _o.append('\n  ')
        v_t_str = c.states(c.N('sensor.vmc_master_temp_interna_status'))
        _o.extend(('\n\n  ', '\n  '))
        if ((J.leggi(v_h_str, 'h_str') == 'Non disponibile') or (J.leggi(v_t_str, 't_str') == 'Non disponibile')):
            _o.append('\n    Non disponibile\n  ')
        elif ((J.leggi(v_h_str, 'h_str') == '[Non Calcolabile]') or (J.leggi(v_t_str, 't_str') == '[Non Calcolabile]')):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.extend(('\n    ', '\n    '))
            v_h_val = J.f_float(J.leggi(v_h_str, 'h_str'), default=None)
            _o.append('\n    ')
            v_t_val = J.f_float(J.leggi(v_t_str, 't_str'), default=None)
            _o.extend(('\n\n    ', '\n    '))
            if ((J.t_none(J.leggi(v_h_val, 'h_val')) or J.t_none(J.leggi(v_t_val, 't_val'))) or (J.leggi(v_h_val, 'h_val') <= 0)):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.extend(('\n      ', '\n      ', J.testo(J.f_round(((((J.leggi(v_h_val, 'h_val') * 6.112) * 2.1674) * (2.718281828459045 ** ((17.67 * J.leggi(v_t_val, 't_val')) / (J.leggi(v_t_val, 't_val') + 243.5)))) / (J.leggi(v_t_val, 't_val') + 273.15)), 2)), '\n    '))
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1133(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_h_str = V.get('h_str', J.MANCANTE)
    v_t_str = V.get('t_str', J.MANCANTE)
    v_h_val = V.get('h_val', J.MANCANTE)
    v_t_val = V.get('t_val', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_h_str = c.states(c.N('sensor.vmc_master_umidita_esterna_status'))
        _o.append('\n  ')
        v_t_str = c.states(c.N('sensor.vmc_master_temp_esterna_status'))
        _o.extend(('\n\n  ', '\n  '))
        if ((J.leggi(v_h_str, 'h_str') == 'Non disponibile') or (J.leggi(v_t_str, 't_str') == 'Non disponibile')):
            _o.extend(('\n    Non disponibile\n  ', '\n  '))
        elif ((J.leggi(v_h_str, 'h_str') == '[Non Calcolabile]') or (J.leggi(v_t_str, 't_str') == '[Non Calcolabile]')):
            _o.append('\n    [Non Calcolabile]\n  ')
        else:
            _o.extend(('\n    ', '\n    '))
            v_h_val = J.f_float(J.leggi(v_h_str, 'h_str'), default=None)
            _o.append('\n    ')
            v_t_val = J.f_float(J.leggi(v_t_str, 't_str'), default=None)
            _o.extend(('\n\n    ', '\n    '))
            if ((J.t_none(J.leggi(v_h_val, 'h_val')) or J.t_none(J.leggi(v_t_val, 't_val'))) or (J.leggi(v_h_val, 'h_val') <= 0)):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.extend(('\n      ', '\n      ', J.testo(J.f_round(((((J.leggi(v_h_val, 'h_val') * 6.112) * 2.1674) * (2.718281828459045 ** ((17.67 * J.leggi(v_t_val, 't_val')) / (J.leggi(v_t_val, 't_val') + 243.5)))) / (J.leggi(v_t_val, 't_val') + 273.15)), 2)), '\n    '))
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1134(c, V):
    # {%- set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] ...
    v_dp_raw = V.get('dp_raw', J.MANCANTE)
    v_dp = V.get('dp', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('Non disponibile\n')
    else:
        v_dp_raw = J.f_trim(c.states(c.N('sensor.vmc_master_punto_di_rugiada_interno')))
        if ((J.leggi(v_dp_raw, 'dp_raw') in J.leggi(v_stati, 'stati')) or J.chiama(J.attributo(J.leggi(v_dp_raw, 'dp_raw'), 'startswith'), '[')):
            _o.extend((J.testo(J.leggi(v_dp_raw, 'dp_raw')), '\n  '))
        else:
            v_dp = J.f_float(J.leggi(v_dp_raw, 'dp_raw'), default=None)
            if J.t_none(J.leggi(v_dp, 'dp')):
                _o.append('[Non Calcolabile]')
            else:
                if (J.leggi(v_dp, 'dp') >= 29):
                    _o.append('–')
                elif (J.leggi(v_dp, 'dp') >= 25):
                    _o.append('Molto fastidioso, Liv. 2')
                elif (J.leggi(v_dp, 'dp') >= 22):
                    _o.append('Molto fastidioso, Liv. 1')
                elif (J.leggi(v_dp, 'dp') >= 19):
                    _o.append('Fastidioso')
                elif (J.leggi(v_dp, 'dp') >= 16):
                    _o.append('Accettabile')
                elif (J.leggi(v_dp, 'dp') >= 13):
                    _o.append('Confortevole, Liv. 2')
                elif (J.leggi(v_dp, 'dp') >= 10):
                    _o.append('Confortevole, Liv. 1')
                elif (J.leggi(v_dp, 'dp') >= 7):
                    _o.append('Secco')
                else:
                    _o.append('–')
    return ''.join(_o)


def m1135(c, V):
    # {%- set invalidi = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile...
    v_congelamento = V.get('congelamento', J.MANCANTE)
    v_delta = V.get('delta', J.MANCANTE)
    v_pdr = V.get('pdr', J.MANCANTE)
    v_free = V.get('free', J.MANCANTE)
    v_free_bloccata = V.get('free_bloccata', J.MANCANTE)
    v_invalidi = v_vel = J.MANCANTE
    _o = []
    v_invalidi = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    v_vel = c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'))
    if ((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) != 'ON-Line') or (J.leggi(v_vel, 'vel') in J.leggi(v_invalidi, 'invalidi'))):
        _o.append('grigio')
    else:
        v_congelamento = (c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'on') or c.is_state(c.N('sensor.vmc_master_congelamento_verifica_soglia'), 'Si'))
        v_delta = c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'on')
        v_pdr = (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego"))
        v_free = c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi'))
        v_free_bloccata = ((('Arrestato' in J.leggi(v_free, 'free')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'on'))
        if (J.leggi(v_vel, 'vel') == 'Velocità 0'):
            if (((J.leggi(v_congelamento, 'congelamento') or J.leggi(v_delta, 'delta')) or J.leggi(v_pdr, 'pdr')) or J.leggi(v_free_bloccata, 'free_bloccata')):
                _o.append('giallo')
            elif c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_totale'), 'Allerta'):
                _o.append('giallo lento')
            else:
                _o.append('bianco')
        elif (J.leggi(v_delta, 'delta') or J.leggi(v_congelamento, 'congelamento')):
            _o.append('giallo')
        elif c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on'):
            _o.append('rosso')
        elif c.is_state(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia'), 'on'):
            _o.append('blu')
        else:
            _o.append('bianco')
    return ''.join(_o)


def m1136(c, V):
    # {#- Alert = PdR sfavorevole (interruttore PdR ON) o Congelamento: tutti i tasti di velo...
    v_congelamento = V.get('congelamento', J.MANCANTE)
    v_delta = V.get('delta', J.MANCANTE)
    v_pdr = V.get('pdr', J.MANCANTE)
    v_free = V.get('free', J.MANCANTE)
    v_free_alert = V.get('free_alert', J.MANCANTE)
    v_invalidi = v_vel = J.MANCANTE
    _o = []
    v_invalidi = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    v_vel = c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'))
    if ((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) != 'ON-Line') or (J.leggi(v_vel, 'vel') in J.leggi(v_invalidi, 'invalidi'))):
        _o.append('Nessuna')
    else:
        v_congelamento = (c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'on') or c.is_state(c.N('sensor.vmc_master_congelamento_verifica_soglia'), 'Si'))
        v_delta = (c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'on') or c.is_state(c.N('sensor.vmc_master_delta_temp_verifica_soglia'), 'Si'))
        v_pdr = (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego"))
        v_free = c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi'))
        v_free_alert = (J.chiama(J.attributo(J.leggi(v_free, 'free'), 'startswith'), 'Allerta Free') or J.chiama(J.attributo(J.leggi(v_free, 'free'), 'startswith'), 'Non Avviare in Velocità Free'))
        if (J.leggi(v_pdr, 'pdr') or J.leggi(v_congelamento, 'congelamento')):
            _o.append('Alert')
        elif J.leggi(v_delta, 'delta'):
            _o.append('Alert Δ Temp.')
        elif J.leggi(v_free_alert, 'free_alert'):
            _o.append('Alert Free')
        else:
            _o.append('Nessuna')
    return ''.join(_o)


def m1137(c, V):
    # {% set v = states('sensor.vmc_master_temp_interna_status') | float(none) %} {{ v if v i...
    v_v = J.MANCANTE
    _o = []
    v_v = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_status')), None)
    _o.extend((' ', J.testo((J.leggi(v_v, 'v') if (not J.t_none(J.leggi(v_v, 'v'))) else None))))
    return ''.join(_o)


def m1138(c, V):
    # {% set v = states('sensor.vmc_master_umidita_interna_status') | float(none) %} {{ v if ...
    v_v = J.MANCANTE
    _o = []
    v_v = J.f_float(c.states(c.N('sensor.vmc_master_umidita_interna_status')), None)
    _o.extend((' ', J.testo((J.leggi(v_v, 'v') if (not J.t_none(J.leggi(v_v, 'v'))) else None))))
    return ''.join(_o)


def m1139(c, V):
    # {%- set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] ...
    v_c1 = V.get('c1', J.MANCANTE)
    v_c2 = V.get('c2', J.MANCANTE)
    v_c3 = V.get('c3', J.MANCANTE)
    v_stati = v_temp = v_hum = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    v_temp = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_media_4w')), None)
    _o.append('\n  ')
    v_hum = J.f_float(c.states(c.N('sensor.vmc_master_hum_interna_media_4w')), None)
    _o.append('\n  ')
    if (J.t_none(J.leggi(v_temp, 'temp')) or J.t_none(J.leggi(v_hum, 'hum'))):
        _o.append('\n    [Non Calcolabile]\n  ')
    else:
        _o.append('\n    ')
        v_c1 = J.elemento(J.f_sort([72, ((20 * (2.718281828459045 ** ((-0.15) * J.leggi(v_temp, 'temp')))) + 73), 100]), 1)
        _o.append('\n    ')
        v_c2 = J.elemento(J.f_sort([79, ((17 * (2.718281828459045 ** ((-0.11) * J.leggi(v_temp, 'temp')))) + 80), 100]), 1)
        _o.append('\n    ')
        v_c3 = J.elemento(J.f_sort([84, ((15 * (2.718281828459045 ** ((-0.1) * J.leggi(v_temp, 'temp')))) + 85), 100]), 1)
        _o.append('\n\n    ')
        if ((J.leggi(v_temp, 'temp') < 0) or (J.leggi(v_temp, 'temp') > 50)):
            _o.append('\n      Rischio assente (condizioni estreme)\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c1, 'c1')):
            _o.append('\n      Liv.\u202f0: nessuna crescita di muffa\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c2, 'c2')):
            _o.append('\n      Liv.\u202f1: crescita possibile in\u202f>\u202f8\u202fSettimane\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c3, 'c3')):
            _o.append('\n      Liv.\u202f2: crescita possibile in\u202f4–8\u202fSettimane\n    ')
        else:
            _o.append('\n      Liv.\u202f3: crescita possibile in\u202f<\u202f4\u202fSettimane\n    ')
        _o.append('\n  ')
    return ''.join(_o)


def m1140(c, V):
    # {%- set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] ...
    v_c1 = V.get('c1', J.MANCANTE)
    v_c2 = V.get('c2', J.MANCANTE)
    v_c3 = V.get('c3', J.MANCANTE)
    v_stati = v_temp = v_hum = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    v_temp = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_media_8w')), None)
    _o.append('\n  ')
    v_hum = J.f_float(c.states(c.N('sensor.vmc_master_hum_interna_media_8w')), None)
    _o.append('\n  ')
    if (J.t_none(J.leggi(v_temp, 'temp')) or J.t_none(J.leggi(v_hum, 'hum'))):
        _o.append('\n    [Non Calcolabile]\n  ')
    else:
        _o.append('\n    ')
        v_c1 = J.elemento(J.f_sort([72, ((20 * (2.718281828459045 ** ((-0.15) * J.leggi(v_temp, 'temp')))) + 73), 100]), 1)
        _o.append('\n    ')
        v_c2 = J.elemento(J.f_sort([79, ((17 * (2.718281828459045 ** ((-0.11) * J.leggi(v_temp, 'temp')))) + 80), 100]), 1)
        _o.append('\n    ')
        v_c3 = J.elemento(J.f_sort([84, ((15 * (2.718281828459045 ** ((-0.1) * J.leggi(v_temp, 'temp')))) + 85), 100]), 1)
        _o.append('\n\n    ')
        if ((J.leggi(v_temp, 'temp') < 0) or (J.leggi(v_temp, 'temp') > 50)):
            _o.append('\n      Rischio assente (condizioni estreme)\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c1, 'c1')):
            _o.append('\n      Liv.\u202f0: nessuna crescita di muffa\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c2, 'c2')):
            _o.append('\n      Liv.\u202f1: crescita possibile in\u202f>\u202f8\u202fSettimane\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c3, 'c3')):
            _o.append('\n      Liv.\u202f2: crescita possibile in\u202f4–8\u202fSettimane\n    ')
        else:
            _o.append('\n      Liv.\u202f3: crescita possibile in\u202f<\u202f4\u202fSettimane\n    ')
        _o.append('\n  ')
    return ''.join(_o)


def m1141(c, V):
    # {%- set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] ...
    v_c1 = V.get('c1', J.MANCANTE)
    v_c2 = V.get('c2', J.MANCANTE)
    v_c3 = V.get('c3', J.MANCANTE)
    v_stati = v_temp = v_hum = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    v_temp = J.f_float(c.states(c.N('sensor.vmc_master_temp_interna_media_12w')), None)
    _o.append('\n  ')
    v_hum = J.f_float(c.states(c.N('sensor.vmc_master_hum_interna_media_12w')), None)
    _o.append('\n  ')
    if (J.t_none(J.leggi(v_temp, 'temp')) or J.t_none(J.leggi(v_hum, 'hum'))):
        _o.append('\n    [Non Calcolabile]\n  ')
    else:
        _o.append('\n    ')
        v_c1 = J.elemento(J.f_sort([72, ((20 * (2.718281828459045 ** ((-0.15) * J.leggi(v_temp, 'temp')))) + 73), 100]), 1)
        _o.append('\n    ')
        v_c2 = J.elemento(J.f_sort([79, ((17 * (2.718281828459045 ** ((-0.11) * J.leggi(v_temp, 'temp')))) + 80), 100]), 1)
        _o.append('\n    ')
        v_c3 = J.elemento(J.f_sort([84, ((15 * (2.718281828459045 ** ((-0.1) * J.leggi(v_temp, 'temp')))) + 85), 100]), 1)
        _o.append('\n\n    ')
        if ((J.leggi(v_temp, 'temp') < 0) or (J.leggi(v_temp, 'temp') > 50)):
            _o.append('\n      Rischio assente (condizioni estreme)\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c1, 'c1')):
            _o.append('\n      Liv.\u202f0: nessuna crescita di muffa\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c2, 'c2')):
            _o.append('\n      Liv.\u202f1: crescita possibile in\u202f>\u202f8\u202fSettimane\n    ')
        elif (J.leggi(v_hum, 'hum') <= J.leggi(v_c3, 'c3')):
            _o.append('\n      Liv.\u202f2: crescita possibile in\u202f4–8\u202fSettimane\n    ')
        else:
            _o.append('\n      Liv.\u202f3: crescita possibile in\u202f<\u202f4\u202fSettimane\n    ')
        _o.append('\n  ')
    return ''.join(_o)


def m1142(c, V):
    # {%- set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] ...
    v_stati = v_map = v_s12 = v_s8 = v_s4 = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    v_map = {'Rischio assente (condizioni estreme)': 0, 'Liv.\u202f0: nessuna crescita di muffa': 0, 'Liv.\u202f1: crescita possibile in\u202f>\u202f8\u202fSettimane': 1, 'Liv.\u202f2: crescita possibile in\u202f4–8\u202fSettimane': 2, 'Liv.\u202f3: crescita possibile in\u202f<\u202f4\u202fSettimane': 3}
    _o.append('\n  ')
    v_s12 = J.chiama(J.attributo(J.leggi(v_map, 'map'), 'get'), c.states(c.N('sensor.vmc_master_calcolo_rischio_muffa_12w')), None)
    _o.append('\n  ')
    v_s8 = J.chiama(J.attributo(J.leggi(v_map, 'map'), 'get'), c.states(c.N('sensor.vmc_master_calcolo_rischio_muffa_8w')), None)
    _o.append('\n  ')
    v_s4 = J.chiama(J.attributo(J.leggi(v_map, 'map'), 'get'), c.states(c.N('sensor.vmc_master_calcolo_rischio_muffa_4w')), None)
    _o.append('\n\n  ')
    if ((J.t_none(J.leggi(v_s12, 's12')) or J.t_none(J.leggi(v_s8, 's8'))) or J.t_none(J.leggi(v_s4, 's4'))):
        _o.append('\n    [Non Calcolabile]\n  ')
    elif ((J.leggi(v_s4, 's4') == J.leggi(v_s12, 's12')) and (J.leggi(v_s4, 's4') != J.leggi(v_s8, 's8'))):
        _o.extend(('\n    Stabile a Liv. ', J.testo(J.leggi(v_s4, 's4')), ' con Oscillazione\n  '))
    elif (J.leggi(v_s4, 's4') > J.leggi(v_s8, 's8')):
        _o.extend(('\n    Peggioramento - Rischio Aumentato a Liv. ', J.testo(J.leggi(v_s4, 's4')), '\n  '))
    elif (J.leggi(v_s4, 's4') < J.leggi(v_s8, 's8')):
        _o.extend(('\n    Miglioramento - Rischio Diminuito a Liv. ', J.testo(J.leggi(v_s4, 's4')), '\n  '))
    else:
        _o.extend(('\n    Stabile a Liv. ', J.testo(J.leggi(v_s4, 's4')), '\n  '))
    return ''.join(_o)


def m1143(c, V):
    # {%- set stati = ["sconosciuto","unknown","","unavailable",none,"Non disponibile", "[Non...
    v_m = V.get('m', J.MANCANTE)
    v_stati = v_txt = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', 'unavailable', None, 'Non disponibile', '[Non Calcolabile]']
    v_txt = c.states(c.N('sensor.vmc_master_trend_muffa'))
    if (J.leggi(v_txt, 'txt') in J.leggi(v_stati, 'stati')):
        _o.append('[Non Calcolabile]')
    else:
        v_m = {'Stabile a Liv. 0': 0, 'Stabile a Liv. 0 con Oscillazione': 0, 'Stabile a Liv. 1': 1, 'Stabile a Liv. 1 con Oscillazione': 1, 'Stabile a Liv. 2': 2, 'Stabile a Liv. 2 con Oscillazione': 2, 'Stabile a Liv. 3': 3, 'Stabile a Liv. 3 con Oscillazione': 3, 'Peggioramento - Rischio Aumentato a Liv. 1': 1, 'Peggioramento - Rischio Aumentato a Liv. 2': 2, 'Peggioramento - Rischio Aumentato a Liv. 3': 3, 'Miglioramento - Rischio Diminuito a Liv. 0': 0, 'Miglioramento - Rischio Diminuito a Liv. 1': 1, 'Miglioramento - Rischio Diminuito a Liv. 2': 2}
        _o.append(J.testo(J.chiama(J.attributo(J.leggi(v_m, 'm'), 'get'), J.leggi(v_txt, 'txt'), '[Non Calcolabile]')))
    return ''.join(_o)


def m1144(c, V):
    # {% set v = states('sensor.vmc_master_trend_muffa_level') | float(none) %} {{ v if v is ...
    v_v = J.MANCANTE
    _o = []
    v_v = J.f_float(c.states(c.N('sensor.vmc_master_trend_muffa_level')), None)
    _o.extend((' ', J.testo((J.leggi(v_v, 'v') if (not J.t_none(J.leggi(v_v, 'v'))) else None))))
    return ''.join(_o)


def m1145(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_componenti = V.get('componenti', J.MANCANTE)
    v_codice = V.get('codice', J.MANCANTE)
    v_codici = V.get('codici', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_componenti = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',')
        _o.append('\n  ')
        if (J.f_length(J.leggi(v_componenti, 'componenti')) > 1):
            _o.append('\n    ')
            v_codice = J.elemento(J.leggi(v_componenti, 'componenti'), 1)
            _o.append('\n    ')
            v_codici = {'00000': '-', '00001': '10', '00002': '17', '00003': '26', '00004': '37', '00005': '42', '00006': '10', '00007': '26'}
            _o.extend(('\n    ', J.testo(J.chiama(J.attributo(J.leggi(v_codici, 'codici'), 'get'), J.leggi(v_codice, 'codice'), 'Non disponibile')), '\n  '))
        else:
            _o.append('\n    -\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1146(c, V):
    # {% set stati_invalidi = ["sconosciuto", "unknown", "", none, "unavailable", "Non dispon...
    v_portata = V.get('portata', J.MANCANTE)
    v_volume = V.get('volume', J.MANCANTE)
    v_tempo_sec = V.get('tempo_sec', J.MANCANTE)
    v_ore = V.get('ore', J.MANCANTE)
    v_minuti = V.get('minuti', J.MANCANTE)
    v_secondi = V.get('secondi', J.MANCANTE)
    v_stati_invalidi = v_portata_str = v_volume_str = J.MANCANTE
    _o = []
    v_stati_invalidi = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_portata_str = c.states(c.N('sensor.vmc_master_status_portata_ventola_lettura_codice_interpretato'))
    _o.append(' ')
    v_volume_str = c.states(c.N('number.vmc_master_volume_da_inserire'))
    _o.append(' ')
    if ((J.leggi(v_portata_str, 'portata_str') in J.leggi(v_stati_invalidi, 'stati_invalidi')) or (J.leggi(v_volume_str, 'volume_str') in J.leggi(v_stati_invalidi, 'stati_invalidi'))):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_portata = J.f_float(J.leggi(v_portata_str, 'portata_str'), 0)
        _o.append('\n  ')
        v_volume = J.f_float(J.leggi(v_volume_str, 'volume_str'), 0)
        _o.append('\n  ')
        if ((J.leggi(v_portata, 'portata') <= 0) or (J.leggi(v_volume, 'volume') <= 0)):
            _o.append('\n    -\n  ')
        else:
            _o.append('\n    ')
            v_tempo_sec = J.f_round(((J.leggi(v_volume, 'volume') / J.leggi(v_portata, 'portata')) * 3600), 0)
            _o.append('\n    ')
            v_ore = (J.leggi(v_tempo_sec, 'tempo_sec') // 3600)
            _o.append('\n    ')
            v_minuti = ((J.leggi(v_tempo_sec, 'tempo_sec') % 3600) // 60)
            _o.append('\n    ')
            v_secondi = (J.leggi(v_tempo_sec, 'tempo_sec') % 60)
            _o.append('\n    ')
            if (J.leggi(v_ore, 'ore') > 0):
                _o.extend(('\n      ', J.testo(J.leggi(v_ore, 'ore')), ' ', J.testo(('ora' if (J.leggi(v_ore, 'ore') == 1) else 'ore')), J.testo((', ' if ((J.leggi(v_minuti, 'minuti') > 0) or (J.leggi(v_secondi, 'secondi') > 0)) else '')), J.testo((J.concat(J.leggi(v_minuti, 'minuti'), (' minuto' if (J.leggi(v_minuti, 'minuti') == 1) else ' minuti')) if (J.leggi(v_minuti, 'minuti') > 0) else '')), J.testo((' e ' if ((J.leggi(v_secondi, 'secondi') > 0) and (J.leggi(v_minuti, 'minuti') > 0)) else '')), J.testo((J.concat(J.leggi(v_secondi, 'secondi'), (' secondo' if (J.leggi(v_secondi, 'secondi') == 1) else ' secondi')) if (J.leggi(v_secondi, 'secondi') > 0) else '')), '\n    '))
            elif (J.leggi(v_minuti, 'minuti') > 0):
                _o.extend(('\n      ', J.testo(J.leggi(v_minuti, 'minuti')), ' ', J.testo(('minuto' if (J.leggi(v_minuti, 'minuti') == 1) else 'minuti')), J.testo((' e ' if (J.leggi(v_secondi, 'secondi') > 0) else '')), J.testo((J.concat(J.leggi(v_secondi, 'secondi'), (' secondo' if (J.leggi(v_secondi, 'secondi') == 1) else ' secondi')) if (J.leggi(v_secondi, 'secondi') > 0) else '')), '\n    '))
            else:
                _o.extend(('\n      ', J.testo(J.leggi(v_secondi, 'secondi')), ' ', J.testo(('secondo' if (J.leggi(v_secondi, 'secondi') == 1) else 'secondi')), '\n    '))
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1147(c, V):
    # {{ ( states('input_number.vmc_master_aria_scambiata_v1') | float(0) + states('input_num...
    _o = []
    _o.append(J.testo(J.f_round(((((((J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_v1')), 0) + J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_v2')), 0)) + J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_v3')), 0)) + J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_v4')), 0)) + J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_iperventilazione')), 0)) + J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_notte')), 0)) + J.f_float(c.states(c.N('input_number.vmc_master_aria_scambiata_freecooling')), 0)), 3)))
    return ''.join(_o)


def m1148(c, V):
    # {% set volume = states('input_number.vmc_master_volume_da_inserire') | float(1) %} {% s...
    v_volume = v_aria_totale = J.MANCANTE
    _o = []
    v_volume = J.f_float(c.states(c.N('number.vmc_master_volume_da_inserire')), 1)
    _o.append(' ')
    v_aria_totale = J.f_float(c.states(c.N('sensor.vmc_master_status_calcolo_aria_scambiata_totale')), 0)
    _o.append(' ')
    if (J.leggi(v_volume, 'volume') > 0):
        _o.extend(('\n  ', J.testo(J.f_round((J.leggi(v_aria_totale, 'aria_totale') / J.leggi(v_volume, 'volume')), 2)), '\n'))
    else:
        _o.append('\n  0\n')
    return ''.join(_o)


def m1149(c, V):
    # {% set portata_str = states('sensor.vmc_master_status_portata_ventola_lettura_codice_in...
    v_portata = V.get('portata', J.MANCANTE)
    v_volume = V.get('volume', J.MANCANTE)
    v_ricambiato = V.get('ricambiato', J.MANCANTE)
    v_residuo = V.get('residuo', J.MANCANTE)
    v_tempo_sec_float = V.get('tempo_sec_float', J.MANCANTE)
    v_tempo_sec = V.get('tempo_sec', J.MANCANTE)
    v_ore = V.get('ore', J.MANCANTE)
    v_minuti = V.get('minuti', J.MANCANTE)
    v_secondi = V.get('secondi', J.MANCANTE)
    v_portata_str = v_volume_str = v_ricambiato_str = v_reset = v_invalidi = J.MANCANTE
    _o = []
    v_portata_str = c.states(c.N('sensor.vmc_master_status_portata_ventola_lettura_codice_interpretato'))
    _o.append(' ')
    v_volume_str = c.states(c.N('number.vmc_master_volume_da_inserire'))
    _o.append(' ')
    v_ricambiato_str = c.states(c.N('input_number.vmc_master_aria_scambiata_ricomincio'))
    _o.append(' ')
    v_reset = (c.states(c.N('input_text.vmc_master_tempo_mancante_reset')) == 'reset')
    _o.append(' ')
    v_invalidi = ['unknown', 'unavailable', '', 'none', None, 'Non disponibile']
    _o.append('\n')
    if (((J.leggi(v_portata_str, 'portata_str') in J.leggi(v_invalidi, 'invalidi')) or (J.leggi(v_volume_str, 'volume_str') in J.leggi(v_invalidi, 'invalidi'))) or (J.leggi(v_ricambiato_str, 'ricambiato_str') in J.leggi(v_invalidi, 'invalidi'))):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_portata = J.f_float(J.leggi(v_portata_str, 'portata_str'), 0)
        _o.append('\n  ')
        v_volume = J.f_float(J.leggi(v_volume_str, 'volume_str'), 0)
        _o.append('\n  ')
        v_ricambiato = J.f_float(J.leggi(v_ricambiato_str, 'ricambiato_str'), 0)
        _o.append('\n  ')
        v_residuo = (J.leggi(v_volume, 'volume') - J.leggi(v_ricambiato, 'ricambiato'))
        _o.append('\n  ')
        if (J.leggi(v_residuo, 'residuo') < 0):
            _o.append('\n    ')
            v_residuo = 0
            _o.append('\n  ')
        _o.append('\n\n  ')
        if ((J.leggi(v_portata, 'portata') <= 0) or (J.leggi(v_volume, 'volume') <= 0)):
            _o.append('\n    -\n  ')
        else:
            _o.append('\n    ')
            if (J.leggi(v_reset, 'reset') or (J.leggi(v_residuo, 'residuo') == 0)):
                _o.append('\n      ')
                v_tempo_sec_float = ((J.leggi(v_volume, 'volume') / J.leggi(v_portata, 'portata')) * 3600)
                _o.append('\n    ')
            else:
                _o.append('\n      ')
                v_tempo_sec_float = ((J.leggi(v_residuo, 'residuo') / J.leggi(v_portata, 'portata')) * 3600)
                _o.append('\n    ')
            _o.append('\n\n    ')
            v_tempo_sec = J.f_int(J.f_round(J.leggi(v_tempo_sec_float, 'tempo_sec_float'), 0))
            _o.append('\n    ')
            v_ore = (J.leggi(v_tempo_sec, 'tempo_sec') // 3600)
            _o.append('\n    ')
            v_minuti = ((J.leggi(v_tempo_sec, 'tempo_sec') % 3600) // 60)
            _o.append('\n    ')
            v_secondi = (J.leggi(v_tempo_sec, 'tempo_sec') % 60)
            _o.append('\n\n    ')
            if ((J.leggi(v_ore, 'ore') == 0) and (J.leggi(v_minuti, 'minuti') == 0)):
                _o.extend(('\n      ', J.testo(J.leggi(v_secondi, 'secondi')), ' ', J.testo(('secondo' if (J.leggi(v_secondi, 'secondi') == 1) else 'secondi')), '\n    '))
            elif (J.leggi(v_ore, 'ore') == 0):
                _o.extend(('\n      ', J.testo(J.leggi(v_minuti, 'minuti')), ' ', J.testo(('minuto' if (J.leggi(v_minuti, 'minuti') == 1) else 'minuti')), '\n    '))
            elif (J.leggi(v_minuti, 'minuti') == 0):
                _o.extend(('\n      ', J.testo(J.leggi(v_ore, 'ore')), ' ', J.testo(('ora' if (J.leggi(v_ore, 'ore') == 1) else 'ore')), '\n    '))
            else:
                _o.extend(('\n      ', J.testo(J.leggi(v_ore, 'ore')), ' ', J.testo(('ora' if (J.leggi(v_ore, 'ore') == 1) else 'ore')), ' e ', J.testo(J.leggi(v_minuti, 'minuti')), ' ', J.testo(('minuto' if (J.leggi(v_minuti, 'minuti') == 1) else 'minuti')), '\n    '))
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1150(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_umidità = V.get('umidità', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_umidità = c.states(c.N('sensor.vmc_master_umidita_interna_status_verifica_soglia'))
        _o.append('\n  ')
        if ((J.leggi(v_umidità, 'umidità') == 'Possibile Secchezza, Disidratazione') or (J.leggi(v_umidità, 'umidità') == 'Possibile Muffe, Batteri')):
            _o.append('\n    Allerta\n  ')
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1151(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_co2 = V.get('co2', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_co2 = c.states(c.N('sensor.vmc_master_co2_status_verifica_soglia'))
        _o.append('\n  ')
        if (((J.leggi(v_co2, 'co2') == 'Moderata Concentrazione') or (J.leggi(v_co2, 'co2') == 'Alta Concentrazione')) or (J.leggi(v_co2, 'co2') == 'Pessima Concentrazione')):
            _o.append('\n    Allerta\n  ')
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1152(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_voc = V.get('voc', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_voc = c.states(c.N('sensor.vmc_master_voc_status_verifica_soglia'))
        _o.append('\n  ')
        if ((J.leggi(v_voc, 'voc') == 'Moderata Concentrazione') or (J.leggi(v_voc, 'voc') == 'Pessima Concentrazione')):
            _o.append('\n    Allerta\n  ')
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1153(c, V):
    # {% set stati_non_validi = ["sconosciuto", "unknown", "", none, "unavailable", "Non disp...
    v_stati_non_validi = v_PdRvc = J.MANCANTE
    _o = []
    v_stati_non_validi = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_PdRvc = c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto'))
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati_non_validi, 'stati_non_validi')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        if (J.leggi(v_PdRvc, 'PdRvc') == "Se ne sconsiglia l'impiego"):
            _o.append('\n    Allerta\n  ')
        elif (J.leggi(v_PdRvc, 'PdRvc') in ['[Non Calcolabile]', '[Non Disponibile]']):
            _o.extend(('\n    ', J.testo(J.leggi(v_PdRvc, 'PdRvc')), '\n  '))
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1154(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_congelamento = V.get('congelamento', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_congelamento = c.states(c.N('sensor.vmc_master_congelamento_verifica_soglia'))
        _o.append('            \n  ')
        if (J.leggi(v_congelamento, 'congelamento') == 'Si'):
            _o.append('\n    Allerta\n  ')
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1155(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_delta = V.get('delta', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_delta = c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia'))
        _o.append('\n  ')
        if (J.leggi(v_delta, 'delta') == 'Si'):
            _o.append('\n    Allerta\n  ')
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1156(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_automazione_free_cooling = V.get('automazione_free_cooling', J.MANCANTE)
    v_automazione_free_heating = V.get('automazione_free_heating', J.MANCANTE)
    v_tipologia = V.get('tipologia', J.MANCANTE)
    v_velocita = V.get('velocita', J.MANCANTE)
    v_temp_interna_str = V.get('temp_interna_str', J.MANCANTE)
    v_temp_esterna_str = V.get('temp_esterna_str', J.MANCANTE)
    v_temp_interna = V.get('temp_interna', J.MANCANTE)
    v_temp_esterna = V.get('temp_esterna', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_automazione_free_cooling = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'))
        _o.append('\n  ')
        v_automazione_free_heating = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'))
        _o.append('\n  ')
        v_tipologia = c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'))
        _o.append('\n  ')
        v_velocita = c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))
        _o.append('\n  ')
        v_temp_interna_str = c.states(c.N('sensor.vmc_master_temp_interna_status'))
        _o.append('\n  ')
        v_temp_esterna_str = c.states(c.N('sensor.vmc_master_temp_esterna_status'))
        _o.extend(('\n\n  ', '\n  '))
        if ((J.leggi(v_tipologia, 'tipologia') == 'Non disponibile') or (J.leggi(v_velocita, 'velocita') == 'Non disponibile')):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.extend(('\n    ', '\n    ', '\n    '))
            if ((J.leggi(v_temp_interna_str, 'temp_interna_str') in ['Non disponibile', '[Non Calcolabile]']) or (J.leggi(v_temp_esterna_str, 'temp_esterna_str') in ['Non disponibile', '[Non Calcolabile]'])):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.extend(('\n      ', '\n      '))
                v_temp_interna = J.f_float(J.leggi(v_temp_interna_str, 'temp_interna_str'), default=None)
                _o.append('\n      ')
                v_temp_esterna = J.f_float(J.leggi(v_temp_esterna_str, 'temp_esterna_str'), default=None)
                _o.append('\n\n      ')
                if (J.t_none(J.leggi(v_temp_interna, 'temp_interna')) or J.t_none(J.leggi(v_temp_esterna, 'temp_esterna'))):
                    _o.append('\n        [Non Calcolabile]\n      ')
                else:
                    _o.extend(('\n        ', '\n        '))
                    if ((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.leggi(v_temp_esterna, 'temp_esterna'))):
                        _o.append('\n          Allerta Free Heating Programmato (Raffrescamento in atto)\n        ')
                    elif (((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') > J.leggi(v_temp_esterna, 'temp_esterna'))):
                        _o.append('\n          Allerta Raffrescamento in atto\n        ')
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.leggi(v_temp_interna, 'temp_interna'))):
                        _o.append('\n          Allerta Free Cooling Programmato (Riscaldamento in atto)\n        ')
                    elif (((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.leggi(v_temp_interna, 'temp_interna'))):
                        _o.append('\n          Allerta Riscaldamento in atto\n        ')
                    elif (((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') > J.leggi(v_temp_esterna, 'temp_esterna'))):
                        _o.append('\n          Raffrescamento in atto\n        ')
                    elif (((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.leggi(v_temp_interna, 'temp_interna'))):
                        _o.append('\n          Riscaldamento in atto\n        ')
                    else:
                        _o.append('\n          Nessuna Allerta\n        ')
                    _o.append('\n      ')
                _o.append('\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1157(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_spia_free_cooling = V.get('spia_free_cooling', J.MANCANTE)
    v_spia_free_heating = V.get('spia_free_heating', J.MANCANTE)
    v_co2 = V.get('co2', J.MANCANTE)
    v_voc = V.get('voc', J.MANCANTE)
    v_automazione_free_cooling = V.get('automazione_free_cooling', J.MANCANTE)
    v_automazione_free_heating = V.get('automazione_free_heating', J.MANCANTE)
    v_tipologia = V.get('tipologia', J.MANCANTE)
    v_velocita = V.get('velocita', J.MANCANTE)
    v_temp_interna_str = V.get('temp_interna_str', J.MANCANTE)
    v_temp_esterna_str = V.get('temp_esterna_str', J.MANCANTE)
    v_temp_interna = V.get('temp_interna', J.MANCANTE)
    v_temp_esterna = V.get('temp_esterna', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_spia_free_cooling = c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'))
        _o.append('\n  ')
        v_spia_free_heating = c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'))
        _o.append('\n  ')
        v_co2 = c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2'))
        _o.append('\n  ')
        v_voc = c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc'))
        _o.append('\n  ')
        v_automazione_free_cooling = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'))
        _o.append('\n  ')
        v_automazione_free_heating = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'))
        _o.append('\n  ')
        v_tipologia = c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'))
        _o.append('\n  ')
        v_velocita = c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))
        _o.append('\n  ')
        v_temp_interna_str = c.states(c.N('sensor.vmc_master_temp_interna_status'))
        _o.append('\n  ')
        v_temp_esterna_str = c.states(c.N('sensor.vmc_master_temp_esterna_status'))
        _o.extend(('\n\n  ', '\n  '))
        if ((J.leggi(v_tipologia, 'tipologia') in ['Non disponibile']) or (J.leggi(v_velocita, 'velocita') in ['Non disponibile'])):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.extend(('\n    ', '\n    '))
            if ((J.leggi(v_temp_interna_str, 'temp_interna_str') in ['Non disponibile', '[Non Calcolabile]']) or (J.leggi(v_temp_esterna_str, 'temp_esterna_str') in ['Non disponibile', '[Non Calcolabile]'])):
                _o.append('\n      [Non Calcolabile]\n    ')
            else:
                _o.append('\n      ')
                v_temp_interna = J.f_float(J.leggi(v_temp_interna_str, 'temp_interna_str'), default=None)
                _o.append('\n      ')
                v_temp_esterna = J.f_float(J.leggi(v_temp_esterna_str, 'temp_esterna_str'), default=None)
                _o.append('\n\n      ')
                if (J.t_none(J.leggi(v_temp_interna, 'temp_interna')) or J.t_none(J.leggi(v_temp_esterna, 'temp_esterna'))):
                    _o.append('\n        [Non Calcolabile]\n      ')
                else:
                    _o.extend(('\n      \n        ', '\n        ', '\n        '))
                    if ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'on')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento Arrestato)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'on')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'on')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'on')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento in atto)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'off')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'off')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento in atto)\n        ', '\n        '))
                    elif (((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'on')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento Arrestato)\n        ', '\n        '))
                    elif (((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'on')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') <= J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Heating Programmato\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') <= J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') <= J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Heating Programmato\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') <= J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'off')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and (J.leggi(v_spia_free_heating, 'spia_free_heating') == 'off')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') <= J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Heating Programmato\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Heating') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_heating, 'automazione_free_heating') == 'on')) and (J.leggi(v_temp_interna, 'temp_interna') <= J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti\n\n        ', '\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'on')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento Arrestato)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'on')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'on')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'on')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento in atto)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'off')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'off')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento in atto)\n        ', '\n        '))
                    elif (((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'on')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento Arrestato)\n        ', '\n        '))
                    elif (((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'on')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') <= J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Cooling Programmato\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') <= J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') <= J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Cooling Programmato\n        ', '\n        '))
                    elif (((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') == 'Velocità 0')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') <= J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'off')) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and (J.leggi(v_spia_free_cooling, 'spia_free_cooling') == 'off')) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') <= J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Cooling Programmato\n        ', '\n        '))
                    elif ((((((J.leggi(v_tipologia, 'tipologia') == 'Free Cooling') and (J.leggi(v_velocita, 'velocita') != 'Velocità 0')) and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_automazione_free_cooling, 'automazione_free_cooling') == 'on')) and (J.leggi(v_temp_esterna, 'temp_esterna') <= J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti\n\n\n        ', '\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Raffrescamento in atto\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Raffrescamento in atto, Presenza di Inquinanti\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Allerta Riscaldamento in atto\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Allerta Riscaldamento in atto, Presenza di Inquinanti\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') == J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') == 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') == J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta, Presenza di Inquinanti\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento)\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_temp_interna, 'temp_interna') > J.f_float(J.leggi(v_temp_esterna, 'temp_esterna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento)\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') > J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.extend(('\n          Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento, Presenza di Inquinanti)\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') == J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') != 'Allerta') and (J.leggi(v_voc, 'voc') != 'Allerta'))):
                        _o.extend(('\n          Nessuna Allerta\n        ', '\n        '))
                    elif ((((J.leggi(v_tipologia, 'tipologia') == 'Disabilitata') and (J.leggi(v_velocita, 'velocita') != 'Free Cooling')) and (J.leggi(v_temp_esterna, 'temp_esterna') == J.f_float(J.leggi(v_temp_interna, 'temp_interna'), 0))) and ((J.leggi(v_co2, 'co2') == 'Allerta') or (J.leggi(v_voc, 'voc') == 'Allerta'))):
                        _o.append('\n          Nessuna Allerta, Presenza di Inquinanti\n        ')
                    else:
                        _o.append('\n          Nessuna Allerta\n        ')
                    _o.append('\n      ')
                _o.append('\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1158(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_avviso_disabilitato = V.get('avviso_disabilitato', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_avviso_disabilitato = c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi'))
        _o.append('\n  ')
        if ((((((((((((((((((((J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Heating Programmato (Raffrescamento Arrestato)') or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Heating Programmato (Raffrescamento in atto)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Cooling Programmato (Riscaldamento in atto)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Raffrescamento in atto')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Riscaldamento in atto')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Riscaldamento in atto, Presenza di Inquinanti')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Allerta Raffrescamento in atto, Presenza di Inquinanti')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento, Presenza di Inquinanti)')) or (J.leggi(v_avviso_disabilitato, 'avviso_disabilitato') == 'Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento, Presenza di Inquinanti)')):
            _o.append('\n    OK\n  ')
        else:
            _o.append('\n    NOT OK\n  ')
        _o.append('   \n')
    return ''.join(_o)


def m1159(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_valore_minimo_temp_esterna = V.get('valore_minimo_temp_esterna', J.MANCANTE)
    v_valore_minimo_temp_interna = V.get('valore_minimo_temp_interna', J.MANCANTE)
    v_valore_minimo_umidita_esterna = V.get('valore_minimo_umidita_esterna', J.MANCANTE)
    v_valore_minimo_umidita_interna = V.get('valore_minimo_umidita_interna', J.MANCANTE)
    v_valore_minimo_co2 = V.get('valore_minimo_co2', J.MANCANTE)
    v_valore_minimo_voc = V.get('valore_minimo_voc', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_valore_minimo_temp_esterna = J.f_float(c.state_attr(c.N('number.vmc_master_offset_temp_esterna'), 'min'), (-50))
        _o.append('\n  ')
        v_valore_minimo_temp_interna = J.f_float(c.state_attr(c.N('number.vmc_master_offset_temp_interna'), 'min'), (-50))
        _o.append('\n  ')
        v_valore_minimo_umidita_esterna = J.f_float(c.state_attr(c.N('number.vmc_master_offset_umidita_esterna'), 'min'), (-50))
        _o.append('\n  ')
        v_valore_minimo_umidita_interna = J.f_float(c.state_attr(c.N('number.vmc_master_offset_umidita_interna'), 'min'), (-50))
        _o.append('\n  ')
        v_valore_minimo_co2 = J.f_float(c.state_attr(c.N('number.vmc_master_offset_co2'), 'min'), (-50))
        _o.append('\n  ')
        v_valore_minimo_voc = J.f_float(c.state_attr(c.N('number.vmc_master_offset_voc'), 'min'), (-50))
        _o.append('\n  ')
        if ((((((J.f_float(c.states(c.N('number.vmc_master_offset_temp_interna')), 0) == J.leggi(v_valore_minimo_temp_interna, 'valore_minimo_temp_interna')) and (J.f_float(c.states(c.N('number.vmc_master_offset_temp_esterna')), 0) == J.leggi(v_valore_minimo_temp_esterna, 'valore_minimo_temp_esterna'))) and (J.f_float(c.states(c.N('number.vmc_master_offset_umidita_interna')), 0) == J.leggi(v_valore_minimo_umidita_interna, 'valore_minimo_umidita_interna'))) and (J.f_float(c.states(c.N('number.vmc_master_offset_umidita_esterna')), 0) == J.leggi(v_valore_minimo_umidita_esterna, 'valore_minimo_umidita_esterna'))) and (J.f_float(c.states(c.N('number.vmc_master_offset_co2')), 0) == J.leggi(v_valore_minimo_co2, 'valore_minimo_co2'))) and (J.f_float(c.states(c.N('number.vmc_master_offset_voc')), 0) == J.leggi(v_valore_minimo_voc, 'valore_minimo_voc'))):
            _o.append('\n    NOT OK\n  ')
        else:
            _o.append('\n    OK\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1160(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        if (((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_0'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_3'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_4'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_notturna'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), 'on')):
            _o.append('\n    Rilevato\n  ')
        else:
            _o.append('\n    Non Rilevato\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1161(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_umidità = V.get('umidità', J.MANCANTE)
    v_umidità_non_calcolabile = V.get('umidità_non_calcolabile', J.MANCANTE)
    v_umidità_esterna_non_calcolabile = V.get('umidità_esterna_non_calcolabile', J.MANCANTE)
    v_co2 = V.get('co2', J.MANCANTE)
    v_voc = V.get('voc', J.MANCANTE)
    v_PdRvc = V.get('PdRvc', J.MANCANTE)
    v_congelamento = V.get('congelamento', J.MANCANTE)
    v_limite_congelamento = V.get('limite_congelamento', J.MANCANTE)
    v_delta = V.get('delta', J.MANCANTE)
    v_limite_delta = V.get('limite_delta', J.MANCANTE)
    v_offset = V.get('offset', J.MANCANTE)
    v_freeheating_freecooling = V.get('freeheating_freecooling', J.MANCANTE)
    v_black_out = V.get('black_out', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_umidità = c.states(c.N('sensor.vmc_master_alert_monitoraggio_umidita'))
        _o.append('\n  ')
        v_umidità_non_calcolabile = c.states(c.N('sensor.vmc_master_umidita_interna_status'))
        _o.append('\n  ')
        v_umidità_esterna_non_calcolabile = c.states(c.N('sensor.vmc_master_umidita_esterna_status'))
        _o.append('\n  ')
        v_co2 = c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2'))
        _o.append('\n  ')
        v_voc = c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc'))
        _o.append('            \n  ')
        v_PdRvc = c.states(c.N('sensor.vmc_master_alert_monitoraggio_pdr'))
        _o.append('\n  ')
        v_congelamento = c.states(c.N('sensor.vmc_master_alert_monitoraggio_congelamento'))
        _o.append('\n  ')
        v_limite_congelamento = c.states(c.N('sensor.vmc_master_congelamento_verifica_soglia'))
        _o.append('\n  ')
        v_delta = c.states(c.N('sensor.vmc_master_alert_monitoraggio_delta'))
        _o.append('\n  ')
        v_limite_delta = c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia'))
        _o.append('\n  ')
        v_offset = c.states(c.N('sensor.vmc_master_alert_monitoraggio_offset_tutti_min'))
        _o.append('\n  ')
        v_freeheating_freecooling = c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_disabilitato'))
        _o.append('\n  ')
        v_black_out = c.states(c.N('sensor.vmc_master_alert_monitoraggio_black_out'))
        _o.append('\n  ')
        if (((((((((((((J.leggi(v_black_out, 'black_out') == 'Rilevato') or (J.leggi(v_umidità, 'umidità') == 'Allerta')) or (J.leggi(v_umidità_non_calcolabile, 'umidità_non_calcolabile') == '[Non Calcolabile]')) or (J.leggi(v_umidità_esterna_non_calcolabile, 'umidità_esterna_non_calcolabile') == '[Non Calcolabile]')) or (J.leggi(v_co2, 'co2') == 'Allerta')) or (J.leggi(v_voc, 'voc') == 'Allerta')) or (J.leggi(v_PdRvc, 'PdRvc') == 'Allerta')) or (J.leggi(v_congelamento, 'congelamento') == 'Allerta')) or (J.leggi(v_limite_congelamento, 'limite_congelamento') == '[No ma Prossimo]')) or (J.leggi(v_delta, 'delta') == 'Allerta')) or (J.leggi(v_limite_delta, 'limite_delta') == '[No ma Prossimo]')) or (J.leggi(v_freeheating_freecooling, 'freeheating_freecooling') == 'OK')) or (J.leggi(v_offset, 'offset') == 'NOT OK')):
            _o.append('\n    Allerta\n  ')
        else:
            _o.append('\n    Nessuna Allerta\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1162(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_monitoraggio = V.get('monitoraggio', J.MANCANTE)
    v_spia_avvisi = V.get('spia_avvisi', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_monitoraggio = c.states(c.N('sensor.vmc_master_alert_monitoraggio_totale'))
        _o.append('\n  ')
        v_spia_avvisi = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_avvisi'))
        _o.append('\n  ')
        if (J.leggi(v_monitoraggio, 'monitoraggio') == 'Nessuna Allerta'):
            _o.append('\n    Non Presenti\n  ')
        elif ((J.leggi(v_monitoraggio, 'monitoraggio') == 'Allerta') and (J.leggi(v_spia_avvisi, 'spia_avvisi') == 'on')):
            _o.append('\n    Presenti\n  ')
        elif ((J.leggi(v_monitoraggio, 'monitoraggio') == 'Allerta') and (J.leggi(v_spia_avvisi, 'spia_avvisi') == 'off')):
            _o.append('\n    Presenti ma Disabilitati\n  ')
        _o.append('\n')
    return ''.join(_o)
