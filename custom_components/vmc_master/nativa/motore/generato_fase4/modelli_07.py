"""Modelli Jinja del package, tradotti in Python (parte 7 di 10).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from .. import jinja as J


def m0625(c, V):
    # {{ 'Velocità 0' if (is_state('input_boolean.vmc_master_spia_velocita_0_co2_o_voc', 'on'...
    _o = []
    _o.append(J.testo(('Velocità 0' if (c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), 'on')) else ('Velocità 1' if ((((c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), 'on') and c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'off')) else ('Velocità 2' if c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), 'on') else ('Velocità 3' if c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), 'on') else ('Velocità 4' if c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), 'on') else ('Notturna' if c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), 'on') else ('Iperventilazione' if c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), 'on') else ('Free Cooling' if ((c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), 'on') and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'off')) else ''))))))))))
    return ''.join(_o)


def m0626(c, V):
    # {{ vel_ripristino_inquinanti == 'Velocità 0' }}
    _o = []
    _o.append(J.testo((V['vel_ripristino_inquinanti'] == 'Velocità 0')))
    return ''.join(_o)


def m0627(c, V):
    # {{ vel_fine_inquinanti == 'Velocità 0' and (is_state('input_boolean.vmc_master_spia_vel...
    _o = []
    _o.append(J.testo(((((V['vel_fine_inquinanti'] == 'Velocità 0') and (c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'on'))) and c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), 'off'))))
    return ''.join(_o)


def m0628(c, V):
    # {{ is_state('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia', 'off')...
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off') and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((((V['vel_ripristino_inquinanti'] != '') and (V['vel_fine_inquinanti'] in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione', 'Free Cooling'])) and (V['vel_fine_inquinanti'] != V['vel_ripristino_inquinanti'])) and (not ((V['vel_ripristino_inquinanti'] == 'Velocità 0') and (V['vel_fine_inquinanti'] == 'Velocità 1')))) and (not ((V['vel_fine_inquinanti'] == 'Velocità 1') and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), 'on')))) or ((((V['vel_fine_inquinanti'] == 'Velocità 0') and (c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'on'))) and c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), 'off'))))))
    return ''.join(_o)


def m0629(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')=='on' or states('input_b...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on'))))
    return ''.join(_o)


def m0630(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')=='on' and states('input_...
    _o = []
    _o.append(J.testo((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0631(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')))
    return ''.join(_o)


def m0632(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')))
    return ''.join(_o)


def m0633(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')))
    return ''.join(_o)


def m0634(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')))
    return ''.join(_o)


def m0635(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')))
    return ''.join(_o)


def m0636(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 0'))))
    return ''.join(_o)


def m0637(c, V):
    # {{ is_state('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia', 'on') and s...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia'), 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0'))))
    return ''.join(_o)


def m0638(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == (('Velocit...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == (('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0') if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0639(c, V):
    # {{ (('Velocità 1' if (states('input_boolean.vmc_master_umidita_verifica_soglia_valore_s...
    _o = []
    _o.extend((J.testo((('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0') if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')), '|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0640(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == (('Ve...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == (('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0') if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0641(c, V):
    # {{ (('Velocità 1' if (states('input_boolean.vmc_master_umidita_verifica_soglia_valore_s...
    _o = []
    _o.append(J.testo((('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0') if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')))
    return ''.join(_o)


def m0642(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')=='on' or (stat...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on') or ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')))))
    return ''.join(_o)


def m0643(c, V):
    # {{( states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')== 'on' or states('inpu...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')))))
    return ''.join(_o)


def m0644(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')=='off' and states('i...
    _o = []
    _o.append(J.testo(((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off'))))
    return ''.join(_o)


def m0645(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')== 'off' and states('in...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off'))))
    return ''.join(_o)


def m0646(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))))
    return ''.join(_o)


def m0647(c, V):
    # {{ states.sensor.vmc_master_status_ventola_lettura_codice_interpretato is not none and ...
    _o = []
    _o.append(J.testo((((not J.t_none(c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')))) and (not J.t_none(c.oggetto(c.N('binary_sensor.vmc_master_spia_co2_o_voc'))))) and (J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')), 'last_changed') <= J.attributo(c.oggetto(c.N('binary_sensor.vmc_master_spia_co2_o_voc')), 'last_changed')))))
    return ''.join(_o)


def m0648(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')== 'on' or states('inpu...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) or ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))))
    return ''.join(_o)


def m0649(c, V):
    # {{( states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')== 'off' and states('in...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and (((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) or ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))))
    return ''.join(_o)


def m0650(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0651(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0652(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0653(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0654(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0655(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0656(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0657(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0658(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0659(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0660(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0661(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0662(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0663(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')))))
    return ''.join(_o)


def m0664(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')=='off' and states('input...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off'))))
    return ''.join(_o)


def m0665(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')))
    return ''.join(_o)


def m0666(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')=='off' and states('input...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off'))))
    return ''.join(_o)


def m0667(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on'))))
    return ''.join(_o)


def m0668(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0669(c, V):
    # {{ ((states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progr...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) or ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0670(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))))
    return ''.join(_o)


def m0671(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0672(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0673(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0674(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0675(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0676(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')=='off' ...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off'))))
    return ''.join(_o)


def m0677(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0678(c, V):
    # {{ trigger.id not in ['Congelamento ON', 'spia_velocita_0_congelamento'] and is_state('...
    _o = []
    _o.append(J.testo((((J.attributo(V['trigger'], 'id') not in ['Congelamento ON', 'spia_velocita_0_congelamento']) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on'))))
    return ''.join(_o)


def m0679(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_1_congelamento')== 'off' and states('i...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))))
    return ''.join(_o)


def m0680(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0'))))
    return ''.join(_o)


def m0681(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')=='on' or states('input_boolean.vmc...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on'))))
    return ''.join(_o)


def m0682(c, V):
    # {{ not(states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')=='on' or states...
    _o = []
    _o.append(J.testo((not ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0683(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')=='on' or states('in...
    _o = []
    _o.append(J.testo(((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on'))))
    return ''.join(_o)


def m0684(c, V):
    # {{ not(states('input_boolean.vmc_master_spia_co2_o_voc')=='on' or states('input_boolean...
    _o = []
    _o.append(J.testo((not (((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')))))
    return ''.join(_o)


def m0685(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off'))))
    return ''.join(_o)


def m0686(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on'))))
    return ''.join(_o)


def m0687(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1'))))
    return ''.join(_o)


def m0688(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2'))))
    return ''.join(_o)


def m0689(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3'))))
    return ''.join(_o)


def m0690(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4'))))
    return ''.join(_o)


def m0691(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione'))))
    return ''.join(_o)


def m0692(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna'))))
    return ''.join(_o)


def m0693(c, V):
    # {{ trigger.id == 'Congelamento ON' and states('sensor.vmc_master_status_ventola_lettura...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'Congelamento ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling'))))
    return ''.join(_o)


def m0694(c, V):
    # {% set g = ['lunedi','martedi','mercoledi','giovedi','venerdi','sabato','domenica'][now...
    v_g = v_G = v_n = v_in1 = v_in2 = v_sp1 = v_sp2 = v_cal = v_ok1 = v_ok2 = v_altro = J.MANCANTE
    _o = []
    v_g = J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday')))
    _o.append(' ')
    v_G = J.elemento(['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica'], J.chiama(J.attributo(c.now(), 'weekday')))
    _o.append(' ')
    v_n = J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M')
    _o.append(' ')
    v_in1 = ((J.leggi(v_n, 'n') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.leggi(v_g, 'g'))), slice(0, 5, None))) and (J.leggi(v_n, 'n') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.leggi(v_g, 'g'))), slice(0, 5, None))))
    _o.append(' ')
    v_in2 = ((J.leggi(v_n, 'n') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.leggi(v_g, 'g'), '_2')), slice(0, 5, None))) and (J.leggi(v_n, 'n') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.leggi(v_g, 'g'), '_2')), slice(0, 5, None))))
    _o.append(' ')
    v_sp1 = c.is_state(J.concat(c.N('binary_sensor.vmc_master_spia_calendario_'), J.leggi(v_g, 'g'), '_1'), 'on')
    _o.append(' ')
    v_sp2 = c.is_state(J.concat(c.N('binary_sensor.vmc_master_spia_calendario_'), J.leggi(v_g, 'g'), '_2'), 'on')
    _o.append(' ')
    v_cal = c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')
    _o.append(' ')
    v_ok1 = (c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.leggi(v_G, 'G'))
    _o.append(' ')
    v_ok2 = (c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.leggi(v_G, 'G'))
    _o.append(' ')
    v_altro = J.namespace(sp=False)
    _o.append(' ')
    for v_d_1 in (_x for _x in ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'] for v_d_1 in [_x] if (v_d_1 != J.leggi(v_g, 'g'))):
        J.imposta_ns(J.leggi(v_altro, 'altro'), 'sp', ((J.attributo(J.leggi(v_altro, 'altro'), 'sp') or c.is_state(J.concat(c.N('binary_sensor.vmc_master_spia_calendario_'), v_d_1, '_1'), 'on')) or c.is_state(J.concat(c.N('binary_sensor.vmc_master_spia_calendario_'), v_d_1, '_2'), 'on')))
    _o.extend((' ', J.testo(((((J.attributo(J.leggi(v_altro, 'altro'), 'sp') or (J.leggi(v_sp1, 'sp1') and (not J.leggi(v_in1, 'in1')))) or (J.leggi(v_sp2, 'sp2') and (not J.leggi(v_in2, 'in2')))) or (((J.leggi(v_cal, 'cal') and J.leggi(v_ok1, 'ok1')) and J.leggi(v_in1, 'in1')) and (not J.leggi(v_sp1, 'sp1')))) or (((J.leggi(v_cal, 'cal') and J.leggi(v_ok2, 'ok2')) and J.leggi(v_in2, 'in2')) and (not J.leggi(v_sp2, 'sp2')))))))
    return ''.join(_o)


def m0695(c, V):
    # {{ states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')== 'off' ...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))))
    return ''.join(_o)


def m0696(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento')) == 'on')))
    return ''.join(_o)


def m0697(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), 'on'))) and (not c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), 'on'))) and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), 'on')))))
    return ''.join(_o)


def m0698(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_1_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'on')))
    return ''.join(_o)


def m0699(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), 'on')))))
    return ''.join(_o)


def m0700(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_2_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'on')))
    return ''.join(_o)


def m0701(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), 'on')))))
    return ''.join(_o)


def m0702(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_3_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'on')))
    return ''.join(_o)


def m0703(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), 'on')))))
    return ''.join(_o)


def m0704(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_4_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'on')))
    return ''.join(_o)


def m0705(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), 'on')))))
    return ''.join(_o)


def m0706(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'on')))
    return ''.join(_o)


def m0707(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), 'on')))))
    return ''.join(_o)


def m0708(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_notturna_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'on')))
    return ''.join(_o)


def m0709(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state('input_bo...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), 'on')))))
    return ''.join(_o)


def m0710(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')== 'on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'on')))
    return ''.join(_o)


def m0711(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programm...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))
    return ''.join(_o)


def m0712(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programm...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0713(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')))
    return ''.join(_o)


def m0714(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')))
    return ''.join(_o)


def m0715(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')))
    return ''.join(_o)


def m0716(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')))
    return ''.join(_o)


def m0717(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0718(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0719(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0720(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0721(c, V):
    # VMC "{{ states('sensor.vmc_master_nome_status') }}"
    _o = []
    _o.extend(('VMC "', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '"'))
    return ''.join(_o)


def m0722(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_temp_external_entity') }} Impieg...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_temp_external_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_temp_esterna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_temp_esterna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_temp_esterna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_temp_esterna_status'))), ' °C\nData ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0723(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_temp_internal_entity') }} Impieg...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_temp_internal_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_temp_interna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_temp_interna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_temp_interna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_temp_interna_status'))), ' °C\nData ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0724(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_humidity_external_entity') }} Im...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_humidity_external_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_umidita_esterna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_umidita_esterna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_umidita_esterna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nData ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0725(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_humidity_internal_entity') }} Im...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_humidity_internal_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_umidita_interna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_umidita_interna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_umidita_interna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status'))), ' %\nData ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0726(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_co2_internal_entity') }} Impiega...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_co2_internal_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_co2_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_co2_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_co2_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_co2_status'))), ' ppm\nData ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0727(c, V):
    # Non Disponibile: {{ states('input_select.vmc_master_selected_notification_device') }} I...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('select.vmc_master_selected_notification_device'))), "\nImpiegato per l'Invio delle Notifiche sul cellulare: le notifiche non vengono inviate. Scegliere di nuovo il dispositivo in Opzioni - Sensori da Selezionare, voce «Seleziona Dispositivo per Invio Notifica».\nData ", J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0728(c, V):
    # Avviso ogni 24 ore: Verificare Filtro, data {{ now().strftime('%d-%m-%Y') }}, ore {{ no...
    _o = []
    _o.extend(('Avviso ogni 24 ore: Verificare Filtro, data ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ', ore ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0729(c, V):
    # {{ ( states('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')=='Veri...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')) == 'Verificare Filtro') and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line'))))
    return ''.join(_o)


def m0730(c, V):
    # {{ states('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')=='Verifi...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato')) == 'Verificare Filtro') and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on'))))
    return ''.join(_o)


def m0731(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0'))))
    return ''.join(_o)


def m0732(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Velocità 0' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 0')))
    return ''.join(_o)


def m0733(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Velocità 1' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 1')))
    return ''.join(_o)


def m0734(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Velocità 2' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 2')))
    return ''.join(_o)


def m0735(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Velocità 3' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 3')))
    return ''.join(_o)


def m0736(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Velocità 4' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 4')))
    return ''.join(_o)


def m0737(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Notturna' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Notturna')))
    return ''.join(_o)


def m0738(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Free Cool./Heat.' and not ( stat...
    _o = []
    _o.append(J.testo(((c.states(c.N('select.vmc_master_speed_umidita')) == 'Free Cool./Heat.') and (not (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento Arrestato)', 'Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)', 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)', 'Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)', 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)', 'Allerta Raffrescamento in atto', 'Allerta Riscaldamento in atto', 'Allerta Riscaldamento in atto, Presenza di Inquinanti', 'Allerta Raffrescamento in atto, Presenza di Inquinanti', 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)', 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)', 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)', 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)'])))))
    return ''.join(_o)


def m0739(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Iperventilazione' }}
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == 'Iperventilazione')))
    return ''.join(_o)


def m0740(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')))
    return ''.join(_o)


def m0741(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')))
    return ''.join(_o)


def m0742(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')))
    return ''.join(_o)


def m0743(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')))
    return ''.join(_o)


def m0744(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')))
    return ''.join(_o)


def m0745(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Notturna'}}
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')))
    return ''.join(_o)


def m0746(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Free Cool...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')))
    return ''.join(_o)


def m0747(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Iperventi...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')))
    return ''.join(_o)


def m0748(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 1'))))
    return ''.join(_o)


def m0749(c, V):
    # {{ not (states('input_select.vmc_master_speed_umidita') == 'Velocità 0' and is_state('i...
    _o = []
    _o.append(J.testo((not ((c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 0') and c.is_state(c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), 'off')))))
    return ''.join(_o)


def m0750(c, V):
    # {{ vel_prima_del_comando in ['Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'N...
    _o = []
    _o.append(J.testo(((V['vel_prima_del_comando'] in ['Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione', 'Free Cooling']) and (V['vel_prima_del_comando'] not in (['Free Cooling', 'Velocità 1'] if (c.states(c.N('select.vmc_master_speed_umidita')) == 'Free Cool./Heat.') else [c.states(c.N('select.vmc_master_speed_umidita'))])))))
    return ''.join(_o)


def m0751(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0'))))
    return ''.join(_o)


def m0752(c, V):
    # {{states('input_boolean.vmc_master_spia_umidita_velocita_0')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')) == 'on')))
    return ''.join(_o)


def m0753(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'N...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione', 'Free Cooling'])))
    return ''.join(_o)


def m0754(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_1') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_1')) == 'on')))
    return ''.join(_o)


def m0755(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 3', 'Velocità 4', 'N...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 1', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione', 'Free Cooling'])))
    return ''.join(_o)


def m0756(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 2'))))
    return ''.join(_o)


def m0757(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_2') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_2')) == 'on')))
    return ''.join(_o)


def m0758(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 4', 'N...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 4', 'Notturna', 'Iperventilazione', 'Free Cooling'])))
    return ''.join(_o)


def m0759(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 3'))))
    return ''.join(_o)


def m0760(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_3') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_3')) == 'on')))
    return ''.join(_o)


def m0761(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'N...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'Notturna', 'Iperventilazione', 'Free Cooling'])))
    return ''.join(_o)


def m0762(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 4'))))
    return ''.join(_o)


def m0763(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_4') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_4')) == 'on')))
    return ''.join(_o)


def m0764(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'V...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Iperventilazione', 'Free Cooling'])))
    return ''.join(_o)


def m0765(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Notturna'))))
    return ''.join(_o)


def m0766(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_notturna') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna')) == 'on')))
    return ''.join(_o)


def m0767(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'V...
    _o = []
    _o.append(J.testo((((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione']) and (not ((V['vel_prima_del_comando'] == 'Velocità 0') and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))) and (not ((V['vel_prima_del_comando'] == 'Velocità 1') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0'))))))
    return ''.join(_o)


def m0768(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == ('Velocità...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == ('Velocità 0' if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0769(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != V['velocita_fine_allerta']))))
    return ''.join(_o)


def m0770(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_freecooling') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')) == 'on')))
    return ''.join(_o)


def m0771(c, V):
    # {{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'V...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Free Cooling'])))
    return ''.join(_o)


def m0772(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None))))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Iperventilazione'))))
    return ''.join(_o)


def m0773(c, V):
    # {{ states('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione')) == 'on')))
    return ''.join(_o)


def m0774(c, V):
    # {{ {'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3',...
    _o = []
    _o.append(J.testo(J.chiama(J.attributo({'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'notturna', 'Iperventilazione': 'iperventilazione', 'Free Cool./Heat.': 'freecooling'}, 'get'), V['vel_avvio'], 'velocita_1')))
    return ''.join(_o)


def m0775(c, V):
    # shell_command.vmc_master_{{ comando_avvio }}
    _o = []
    _o.extend((c.N('shell_command.vmc_master_'), J.testo(V['comando_avvio'])))
    return ''.join(_o)


def m0776(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') not in [vel_p...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0777(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_umidita_velocita_0', 'on') and is_state('inp...
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), 'on') and c.is_state(c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), 'off')) and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0'))))
    return ''.join(_o)


def m0778(c, V):
    # {{ not (trigger.from_state is defined and trigger.from_state is not none and trigger.fr...
    _o = []
    _o.append(J.testo((not ((J.t_defined(J.attributo(V['trigger'], 'from_state')) and (not J.t_none(J.attributo(V['trigger'], 'from_state')))) and (J.attributo(J.attributo(V['trigger'], 'from_state'), 'state') in ['Non disponibile', 'sconosciuto', 'unknown', 'unavailable', '', 'OFF-Line'])))))
    return ''.join(_o)


def m0779(c, V):
    # {{ (states('input_select.vmc_master_speed_umidita') == 'Free Cool./Heat.' and ( states(...
    _o = []
    _o.append(J.testo((((((c.states(c.N('select.vmc_master_speed_umidita')) == 'Free Cool./Heat.') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento Arrestato)', 'Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)', 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)', 'Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)', 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)', 'Allerta Raffrescamento in atto', 'Allerta Riscaldamento in atto', 'Allerta Riscaldamento in atto, Presenza di Inquinanti', 'Allerta Raffrescamento in atto, Presenza di Inquinanti', 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)', 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)', 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)', 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)', 'Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento)', 'Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento)', 'Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento, Presenza di Inquinanti)', 'Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento, Presenza di Inquinanti)'])) and (c.states(c.N('select.vmc_master_speed_umidita')) != c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')))) and c.is_state(c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), 'on')) and (c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) in ['Free Heating', 'Free Cooling']))))
    return ''.join(_o)


def m0780(c, V):
    # {{states('input_select.vmc_master_speed_umidita')!=states('sensor.vmc_master_status_ven...
    _o = []
    _o.append(J.testo(((c.states(c.N('select.vmc_master_speed_umidita')) != c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))) or (not c.is_state(c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), 'on')))))
    return ''.join(_o)


def m0781(c, V):
    # {{states('input_select.vmc_master_speed_umidita')==states('sensor.vmc_master_status_ven...
    _o = []
    _o.append(J.testo((c.states(c.N('select.vmc_master_speed_umidita')) == c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')))))
    return ''.join(_o)


def m0782(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') i...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) in ['Free Cooling', 'Free Heating', 'Free Cool./Heat.']) and (c.states(c.N('select.vmc_master_speed_umidita')) == 'Free Cool./Heat.')) and c.is_state(c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), 'on'))))
    return ''.join(_o)


def m0783(c, V):
    # {{ trigger.id not in ['delta_temp_ON', 'spia_velocita_1_delta_temp'] and is_state('inpu...
    _o = []
    _o.append(J.testo((((J.attributo(V['trigger'], 'id') not in ['delta_temp_ON', 'spia_velocita_1_delta_temp']) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on'))))
    return ''.join(_o)


def m0784(c, V):
    # {{ trigger.id == 'spia_velocita_0_delta_temp' and (is_state('input_boolean.vmc_master_s...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'spia_velocita_0_delta_temp') and (c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'on')))))
    return ''.join(_o)


def m0785(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0'))))
    return ''.join(_o)


def m0786(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')=...
    _o = []
    _o.append(J.testo(((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))))
    return ''.join(_o)


def m0787(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1'))))
    return ''.join(_o)


def m0788(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2'))))
    return ''.join(_o)


def m0789(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3'))))
    return ''.join(_o)


def m0790(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4'))))
    return ''.join(_o)


def m0791(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione'))))
    return ''.join(_o)


def m0792(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna'))))
    return ''.join(_o)


def m0793(c, V):
    # {{ trigger.id == 'delta_temp_ON' and states('sensor.vmc_master_status_ventola_lettura_c...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'delta_temp_ON') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling'))))
    return ''.join(_o)


def m0794(c, V):
    # {{ {'Velocità 0': 'input_boolean.vmc_master_spia_velocita_0_co2_o_voc', 'Velocità 2': '...
    _o = []
    _o.append(J.testo(J.chiama(J.attributo({'Velocità 0': c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), 'Velocità 2': c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), 'Velocità 3': c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), 'Velocità 4': c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), 'Notturna': c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), 'Iperventilazione': c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), 'Free Cooling': c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')}, 'get'), V['vel_fine_delta'], '')))
    return ''.join(_o)


def m0795(c, V):
    # {{ memoria_inquinanti_fine_delta }}
    _o = []
    _o.append(J.testo(V['memoria_inquinanti_fine_delta']))
    return ''.join(_o)


def m0796(c, V):
    # {{ (['input_boolean.vmc_master_spia_velocita_0_co2_o_voc', 'input_boolean.vmc_master_sp...
    _o = []
    _o.append(J.testo(J.f_join((J.f_list(J.f_reject([c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')], c.test('eq'), V['memoria_inquinanti_fine_delta'])) + [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')]), ',')))
    return ''.join(_o)


def m0797(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and not is_state(memoria_i...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (not c.timer.is_state(V['memoria_inquinanti_fine_delta'], 'on')))))
    return ''.join(_o)


def m0798(c, V):
    # {{ vel_fine_delta == 'Velocità 0' and (is_state('input_boolean.vmc_master_spia_velocita...
    _o = []
    _o.append(J.testo(((V['vel_fine_delta'] == 'Velocità 0') and (c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'on')))))
    return ''.join(_o)


def m0799(c, V):
    # {%- set non_eseguito = states('input_text.vmc_master_comando_non_eseguito') -%} {%- set...
    v_non_eseguito = v_vel = J.MANCANTE
    _o = []
    v_non_eseguito = c.states(c.N('sensor.vmc_master_comando_non_eseguito'))
    v_vel = c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))
    _o.append(J.testo(((V['vel_fine_delta'] in ['Velocità 0', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione', 'Free Cooling']) and (not ((((J.leggi(v_non_eseguito, 'non_eseguito') not in ['', 'unknown', 'unavailable']) and ('|' in J.leggi(v_non_eseguito, 'non_eseguito'))) and (not J.t_none(J.leggi(v_vel, 'vel')))) and (J.as_timestamp(J.attributo(J.leggi(v_vel, 'vel'), 'last_changed'), 0) <= J.f_float(J.elemento(J.chiama(J.attributo(J.leggi(v_non_eseguito, 'non_eseguito'), 'split'), '|'), 1), 0)))))))
    return ''.join(_o)


def m0800(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')=...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0801(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')=...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0802(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')=...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0803(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')=...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0804(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')=...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0805(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_s...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0806(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_va...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0807(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia...
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'on')))
    return ''.join(_o)


def m0808(c, V):
    # {{ states('input_number.vmc_master_attesa_pdr_cambio') | int(16) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_pdr_cambio')), 16)))
    return ''.join(_o)


def m0809(c, V):
    # {{ states('input_number.vmc_master_attesa_pdr_cambio_inquinanti') | int(12) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_pdr_cambio_inquinanti')), 12)))
    return ''.join(_o)


def m0810(c, V):
    # {{ states('input_number.vmc_master_attesa_pdr_ripristino') | int(16) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_pdr_ripristino')), 16)))
    return ''.join(_o)


def m0811(c, V):
    # {{ states('input_number.vmc_master_attesa_pdr_ripristino_inquinanti') | int(12) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_pdr_ripristino_inquinanti')), 12)))
    return ''.join(_o)


def m0812(c, V):
    # {{ ( ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')!="Se ne sconsig...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0813(c, V):
    # {{ states('input_number.vmc_master_attesa_free_sospensione') | int(24) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_free_sospensione')), 24)))
    return ''.join(_o)


def m0814(c, V):
    # {{ states('input_number.vmc_master_attesa_free_sospensione_inquinanti') | int(20) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_free_sospensione_inquinanti')), 20)))
    return ''.join(_o)


def m0815(c, V):
    # {{ states('input_number.vmc_master_attesa_free_ripristino') | int(24) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_free_ripristino')), 24)))
    return ''.join(_o)


def m0816(c, V):
    # {{ states('input_number.vmc_master_attesa_free_ripristino_inquinanti') | int(20) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_free_ripristino_inquinanti')), 20)))
    return ''.join(_o)


def m0817(c, V):
    # {{ ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc') == 'off...
    _o = []
    _o.append(J.testo((((((((((((((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'off') and (((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0818(c, V):
    # {{ ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr') == 'off' and ...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'off') and ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on'))) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0819(c, V):
    # {{ ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr') == 'off' and ...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'off') and ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on'))) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0820(c, V):
    # {{ ( states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') in ['Di...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) in ['Disabilitata', 'Free Cooling']) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0821(c, V):
    # {{ ( states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') in ['Di...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) in ['Disabilitata', 'Free Cooling']) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0822(c, V):
    # {{ ( states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') in ['Di...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) in ['Disabilitata', 'Free Heating']) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0823(c, V):
    # {{ ( states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') in ['Di...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) in ['Disabilitata', 'Free Heating']) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0824(c, V):
    # {{ ( ( ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario') ==...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'off') and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'on'))) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0825(c, V):
    # {{ ( ( ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario') ==...
    _o = []
    _o.append(J.testo((((((((((((((((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'off') and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'on'))) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0826(c, V):
    # {{ states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))
    return ''.join(_o)


def m0827(c, V):
    # {{ ( states('sensor.vmc_master_status_ip_interfaccia') == "OFF-Line" and states('sensor...
    _o = []
    _o.append(J.testo((((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0828(c, V):
    # {{ ( states('sensor.vmc_master_status_ip_interfaccia') == "OFF-Line" and states('sensor...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0829(c, V):
    # {{ ( states('sensor.vmc_master_status_ip_interfaccia') == "OFF-Line" and states('sensor...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'OFF-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off'))) and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0830(c, V):
    # {{ states('input_number.vmc_master_attesa_blackout_ripristino') | int(32) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_ripristino')), 32)))
    return ''.join(_o)


def m0831(c, V):
    # {{ ( states('input_boolean.vmc_master_spia_calendario_comando_non_eseguito') == 'on' an...
    _o = []
    _o.append(J.testo((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola')) not in ['unavailable', 'unknown', ''])) and (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0832(c, V):
    # {{ ( states('input_text.vmc_master_comando_non_eseguito') not in ['', 'unknown', 'unava...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_comando_non_eseguito')) not in ['', 'unknown', 'unavailable']) and (c.states(c.N('sensor.vmc_master_status_ventola')) not in ['unavailable', 'unknown', ''])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (((c.states(c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')) == 'off') or (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on'))) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0833(c, V):
    # {{ states('input_number.vmc_master_attesa_calendario_inizio') | int(3) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_calendario_inizio')), 3)))
    return ''.join(_o)


def m0834(c, V):
    # {{ states('input_number.vmc_master_attesa_calendario_fine') | int(3) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_calendario_fine')), 3)))
    return ''.join(_o)


def m0835(c, V):
    # {{ ( states('input_text.vmc_master_nome_da_inserire') is match('^[A-Za-z0-9_-]{1,10}$')...
    _o = []
    _o.append(J.testo(((((((((((J.t_match(c.states(c.N('text.vmc_master_nome_da_inserire')), '^[A-Za-z0-9_-]{1,10}$') and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0836(c, V):
    # {{ states('input_number.vmc_master_attesa_avvisi') | int(5) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_avvisi')), 5)))
    return ''.join(_o)


def m0837(c, V):
    # {%- set _i = states('sensor.vmc_master_versione_corrente') | trim | regex_replace('^[^0...
    v__i = v__r = v__nuova = v__valida = J.MANCANTE
    _o = []
    v__i = J.f_regex_replace(J.f_trim(c.states(c.N('sensor.vmc_master_versione_corrente'))), '^[^0-9]*', '')
    v__r = J.f_regex_replace(J.f_trim(c.states(c.N('sensor.vmc_master_versione_repository'))), '^[^0-9]*', '')
    v__nuova = ((J.t_match(J.leggi(v__i, '_i'), '^[0-9]+([.][0-9]+)*(b[0-9]+)?$') and J.t_match(J.leggi(v__r, '_r'), '^[0-9]+([.][0-9]+)*(b[0-9]+)?$')) and (((J.f_list(J.f_map(J.chiama(J.attributo(J.elemento(J.chiama(J.attributo(J.leggi(v__r, '_r'), 'split'), 'b'), 0), 'split'), '.'), 'int')) + J.elemento([0, 0], slice(J.chiama(J.attributo(J.elemento(J.chiama(J.attributo(J.leggi(v__r, '_r'), 'split'), 'b'), 0), 'count'), '.'), None, None))) + ([0, J.f_int(J.elemento(J.chiama(J.attributo(J.leggi(v__r, '_r'), 'split'), 'b'), 1))] if ('b' in J.leggi(v__r, '_r')) else [1, 0])) > ((J.f_list(J.f_map(J.chiama(J.attributo(J.elemento(J.chiama(J.attributo(J.leggi(v__i, '_i'), 'split'), 'b'), 0), 'split'), '.'), 'int')) + J.elemento([0, 0], slice(J.chiama(J.attributo(J.elemento(J.chiama(J.attributo(J.leggi(v__i, '_i'), 'split'), 'b'), 0), 'count'), '.'), None, None))) + ([0, J.f_int(J.elemento(J.chiama(J.attributo(J.leggi(v__i, '_i'), 'split'), 'b'), 1))] if ('b' in J.leggi(v__i, '_i')) else [1, 0]))))
    v__valida = (J.t_match(J.leggi(v__i, '_i'), '^[0-9]+([.][0-9]+)*(b[0-9]+)?$') and J.t_match(J.leggi(v__r, '_r'), '^[0-9]+([.][0-9]+)*(b[0-9]+)?$'))
    _o.append(J.testo(((((((((((((J.leggi(v__valida, '_valida') and (not J.leggi(v__nuova, '_nuova'))) and (c.states(c.N('sensor.vmc_master_versione_repository')) != 'Errore Connessione')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0838(c, V):
    # {{ states('input_number.vmc_master_attesa_inquinanti_avvio') | int(8) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_inquinanti_avvio')), 8)))
    return ''.join(_o)


def m0839(c, V):
    # {{ states('input_number.vmc_master_attesa_inquinanti_avvio_spia_pdr') | int(8) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_inquinanti_avvio_spia_pdr')), 8)))
    return ''.join(_o)


def m0840(c, V):
    # {{ states('input_number.vmc_master_attesa_inquinanti_fine') | int(8) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_inquinanti_fine')), 8)))
    return ''.join(_o)


def m0841(c, V):
    # {{ states('input_number.vmc_master_attesa_inquinanti_memoria') | int(8) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_inquinanti_memoria')), 8)))
    return ''.join(_o)


def m0842(c, V):
    # {{ ( states('sensor.vmc_master_congelamento_verifica_soglia') == 'Si' and states('senso...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('sensor.vmc_master_congelamento_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0843(c, V):
    # {{ ( states('sensor.vmc_master_congelamento_verifica_soglia') != 'Si' and states('senso...
    _o = []
    _o.append(J.testo(((((((c.states(c.N('sensor.vmc_master_congelamento_verifica_soglia')) != 'Si') and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'on'))) and (((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0844(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocit...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0845(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocit...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0846(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocit...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0847(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocit...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0848(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocit...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0849(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Iperven...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0850(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Notturn...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0851(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Free Co...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) <= (-18)) or (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) <= (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0852(c, V):
    # {{ ( ( ( (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) or ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione'])) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'off') or (c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 0')) or (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 1'))) and (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0853(c, V):
    # {{ states('input_number.vmc_master_attesa_free_annullamento') | int(20) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_free_annullamento')), 20)))
    return ''.join(_o)


def m0854(c, V):
    # {{ ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')=="Se ne sconsigli...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) and ((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento in atto)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Velocità 1', 'Free Cooling'])) and ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta'))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)) or ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on'))))))
    return ''.join(_o)


def m0855(c, V):
    # {{ ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')=="Se ne sconsigli...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento in atto)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)')) or ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Nessuna Allerta Free Heating Programmato', 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')))) and ((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling']) or (((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')))) and (not (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on') and ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) != 'on') or (c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 0'))) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')))) and (((c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Nessuna Allerta') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Nessuna Allerta')) or (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'off'))) and (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0856(c, V):
    # {{ ( (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsig...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and ((((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento in atto)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Velocità 1', 'Free Cooling'])) and ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta'))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)) or ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on'))))))
    return ''.join(_o)


def m0857(c, V):
    # {{ states('sensor.vmc_master_temperatura_esterna_selezionata') == '-100' and not states...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_temperatura_esterna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_temp_external_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0858(c, V):
    # {{ states('sensor.vmc_master_temperatura_interna_selezionata') == '-100' and not states...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_temperatura_interna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_temp_internal_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0859(c, V):
    # {{ states('sensor.vmc_master_umidita_esterna_selezionata') == '-100' and not states('in...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_umidita_esterna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_humidity_external_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0860(c, V):
    # {{ states('sensor.vmc_master_umidita_interna_selezionata') == '-100' and not states('in...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_umidita_interna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_humidity_internal_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0861(c, V):
    # {{ states('sensor.vmc_master_co2_interna_selezionata') == '-100' and not states('input_...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_co2_interna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_co2_internal_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0862(c, V):
    # {{ not states('input_select.vmc_master_selected_notification_device').startswith('Aggio...
    _o = []
    _o.append(J.testo((((((((((((((not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_notification_device')), 'startswith'), 'Aggiorna Elenco')) and (c.states(c.N('select.vmc_master_selected_notification_device')) not in ['unknown', 'unavailable', ''])) and (c.states(c.N('select.vmc_master_selected_notification_device')) not in J.f_list(J.f_map(J.f_select(J.f_map(J.f_reject(J.f_select(c.integration_entities('mobile_app'), 'match', 'device_tracker'), c.test('is_state'), 'unavailable'), c.filtro('device_attr'), 'name'), c.test('string')), 'slugify')))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0863(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0864(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') != 'Velocità ...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0') and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0865(c, V):
    # {{ states('sensor.vmc_master_temperatura_esterna_selezionata') == '-100' and not states...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_temperatura_esterna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_temp_external_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0866(c, V):
    # {{ states('sensor.vmc_master_temperatura_interna_selezionata') == '-100' and not states...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_temperatura_interna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_temp_internal_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0867(c, V):
    # {{ states('sensor.vmc_master_umidita_esterna_selezionata') == '-100' and not states('in...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_umidita_esterna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('select.vmc_master_selected_humidity_external_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('switch.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)
