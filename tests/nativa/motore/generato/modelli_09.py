"""Modelli Jinja del package, tradotti in Python (parte 9 di 9).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from custom_components.vmc_master.nativa.motore import jinja as J


def m1031(c, V):
    # {% set mp = states('input_select.vmc_master_selected_media_player_entity') %} {% set in...
    v_mp = v_invalid = v_audio_interruttore = v_now_time = v_start_raw = v_end_raw = v_start_time = v_end_time = J.MANCANTE
    _o = []
    v_mp = c.states(c.N('input_select.vmc_master_selected_media_player_entity'))
    _o.append(' ')
    v_invalid = ['Aggiorna Elenco Media Player', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_audio_interruttore = c.states(c.N('input_boolean.vmc_master_notifica_audio'))
    _o.append(' ')
    v_now_time = J.chiama(J.attributo(c.now(), 'time'))
    _o.extend(('\n', ' '))
    v_start_raw = J.elemento(c.states(c.N('input_datetime.vmc_master_audio_start_time')), slice(None, 5, None))
    _o.append(' ')
    v_end_raw = J.elemento(c.states(c.N('input_datetime.vmc_master_audio_end_time')), slice(None, 5, None))
    _o.append('\n')
    v_start_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_start_raw, 'start_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_start_raw, 'start_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append(' ')
    v_end_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_end_raw, 'end_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_end_raw, 'end_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append('\n')
    if (J.leggi(v_start_time, 'start_time') and J.leggi(v_end_time, 'end_time')):
        _o.append('\n  ')
        if (J.leggi(v_start_time, 'start_time') <= J.leggi(v_end_time, 'end_time')):
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_black_out')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_black_out')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1032(c, V):
    # VMC {{ states('sensor.vmc_master_nome_status') }} in Linea
    _o = []
    _o.extend(('VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  in Linea'))
    return ''.join(_o)


def m1033(c, V):
    # {% set mp = states('input_select.vmc_master_selected_media_player_entity') %} {% set in...
    v_mp = v_invalid = v_audio_interruttore = v_now_time = v_start_raw = v_end_raw = v_start_time = v_end_time = J.MANCANTE
    _o = []
    v_mp = c.states(c.N('input_select.vmc_master_selected_media_player_entity'))
    _o.append(' ')
    v_invalid = ['Aggiorna Elenco Media Player', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_audio_interruttore = c.states(c.N('input_boolean.vmc_master_notifica_audio'))
    _o.append(' ')
    v_now_time = J.chiama(J.attributo(c.now(), 'time'))
    _o.extend(('\n', ' '))
    v_start_raw = J.elemento(c.states(c.N('input_datetime.vmc_master_audio_start_time')), slice(None, 5, None))
    _o.append(' ')
    v_end_raw = J.elemento(c.states(c.N('input_datetime.vmc_master_audio_end_time')), slice(None, 5, None))
    _o.append('\n')
    v_start_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_start_raw, 'start_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_start_raw, 'start_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append(' ')
    v_end_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_end_raw, 'end_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_end_raw, 'end_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append('\n')
    if (J.leggi(v_start_time, 'start_time') and J.leggi(v_end_time, 'end_time')):
        _o.append('\n  ')
        if (J.leggi(v_start_time, 'start_time') <= J.leggi(v_end_time, 'end_time')):
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_black_out')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_black_out')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)
