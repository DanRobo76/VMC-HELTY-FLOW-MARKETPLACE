"""Modelli Jinja del package, tradotti in Python (parte 6 di 10).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from .. import jinja as J


def m0404(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_avvisi', 'input_boolean.vmc_master_opzion...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_avvisi'), c.N('switch.vmc_master_opzioni_avvisi_grafici'), c.N('switch.vmc_master_opzioni_offset_sensori'), c.N('switch.vmc_master_opzioni_monitoraggio_sensori'), c.N('switch.vmc_master_opzioni_lettura_sensori'), c.N('switch.vmc_master_opzioni_interruttore_calendario'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0405(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_avvisi', 'input_boolean.vmc_master_opzion...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_avvisi'), c.N('switch.vmc_master_opzioni_avvisi_grafici'), c.N('switch.vmc_master_opzioni_offset_sensori'), c.N('switch.vmc_master_opzioni_vmc'), c.N('switch.vmc_master_opzioni_lettura_sensori'), c.N('switch.vmc_master_opzioni_interruttore_calendario'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0406(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra',...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0407(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_interruttore_offset_sensori', 'input_bool...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0408(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra',...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0409(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_lettura_sensori', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_lettura_sensori'), c.N('switch.vmc_master_opzioni_avvisi'), c.N('switch.vmc_master_opzioni_avvisi_grafici'), c.N('switch.vmc_master_opzioni_offset_sensori'), c.N('switch.vmc_master_opzioni_vmc'), c.N('switch.vmc_master_opzioni_monitoraggio_sensori'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0410(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_avvisi', 'input_boolean.vmc_master_opzion...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_avvisi'), c.N('switch.vmc_master_opzioni_avvisi_grafici'), c.N('switch.vmc_master_opzioni_vmc'), c.N('switch.vmc_master_opzioni_monitoraggio_sensori'), c.N('switch.vmc_master_opzioni_lettura_sensori'), c.N('switch.vmc_master_opzioni_interruttore_calendario'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0411(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0412(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_free_heating_o_free_cooling', 'input_bool...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0413(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_free_heating_o_free_cooling', 'input_bool...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0414(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0415(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_vmc', 'input_boolean.vmc_master_opzioni_m...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_vmc'), c.N('switch.vmc_master_opzioni_monitoraggio_sensori'), c.N('switch.vmc_master_opzioni_lettura_sensori'), c.N('switch.vmc_master_opzioni_interruttore_calendario'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_offset_sensori'), c.N('switch.vmc_master_opzioni_avvisi_grafici'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0416(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_avvisi', 'input_boolean.vmc_master_opzion...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('switch.vmc_master_opzioni_avvisi'), c.N('switch.vmc_master_opzioni_avvisi_grafici'), c.N('switch.vmc_master_opzioni_offset_sensori'), c.N('switch.vmc_master_opzioni_vmc'), c.N('switch.vmc_master_opzioni_monitoraggio_sensori'), c.N('switch.vmc_master_opzioni_interruttore_calendario'), c.N('switch.vmc_master_opzioni_calendario'), c.N('switch.vmc_master_opzioni_calendario_main'), c.N('switch.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('switch.vmc_master_opzioni_punto_di_rugiada'), c.N('switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('switch.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('switch.vmc_master_opzioni_interruttore_offset_sensori'), c.N('switch.vmc_master_opzioni_scelta_sensori'), c.N('switch.vmc_master_opzioni_elementi_chimici'), c.N('switch.vmc_master_opzione_finestra_audio'), c.N('switch.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0417(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0418(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0419(c, V):
    # Velocità 0|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Velocità 0|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0420(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velo...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0421(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')== 'off'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')))
    return ''.join(_o)


def m0422(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0423(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0424(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0425(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0426(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))))
    return ''.join(_o)


def m0427(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0428(c, V):
    # Velocità 1|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Velocità 1|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0429(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velo...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0430(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0431(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))
    return ''.join(_o)


def m0432(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0433(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')== 'off' and states('...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off'))))
    return ''.join(_o)


def m0434(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0435(c, V):
    # Velocità 2|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Velocità 2|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0436(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velo...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0437(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0438(c, V):
    # Velocità 3|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Velocità 3|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0439(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velo...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0440(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0441(c, V):
    # Velocità 4|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Velocità 4|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0442(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velo...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0443(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Notturna'...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0444(c, V):
    # Notturna|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Notturna|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0445(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Nott...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0446(c, V):
    # {{states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inter...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento in atto)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)'))))
    return ''.join(_o)


def m0447(c, V):
    # {{states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inter...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento in atto)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)')) or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato)'))))
    return ''.join(_o)


def m0448(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Free Cool...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0449(c, V):
    # Free Cooling|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Free Cooling|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0450(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Free...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0451(c, V):
    # {{(states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Cooling Programmato') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti')) and (c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) == 'Free Cooling'))))
    return ''.join(_o)


def m0452(c, V):
    # {{(states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Heating Programmato') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti')) and (c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) == 'Free Heating'))))
    return ''.join(_o)


def m0453(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) == 'Disabilitata'))))
    return ''.join(_o)


def m0454(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Iperventi...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0455(c, V):
    # Iperventilazione|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend(('Iperventilazione|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0456(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Iper...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0457(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Non disponibile', 'unknown', 'unavailab...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0458(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0'))))
    return ''.join(_o)


def m0459(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Free Cool./Heat.')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off'))))
    return ''.join(_o)


def m0460(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Non disponibile', 'unknow...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0461(c, V):
    # {{ is_state('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia', 'on') and i...
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia'), 'on') and c.is_state(c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), 'on')) and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_umidita')) != 'Allerta'))))
    return ''.join(_o)


def m0462(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 1'))))
    return ''.join(_o)


def m0463(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')== 'off' and states(...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0464(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 2', 'Non disponibile', 'unknow...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 2', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0465(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 2'))))
    return ''.join(_o)


def m0466(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 3', 'Non disponibile', 'unknow...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 3', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0467(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 3'))))
    return ''.join(_o)


def m0468(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 4', 'Non disponibile', 'unknow...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 4', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0469(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 4'))))
    return ''.join(_o)


def m0470(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Notturna', 'Non disponibile', 'unknown'...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Notturna', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0471(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Notturna'))))
    return ''.join(_o)


def m0472(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')== 'off' and states(...
    _o = []
    _o.append(J.testo(((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))))
    return ''.join(_o)


def m0473(c, V):
    # {{ vel_prima_del_comando == 'Velocità 1' and states('input_boolean.vmc_master_umidita_v...
    _o = []
    _o.append(J.testo(((((V['vel_prima_del_comando'] == 'Velocità 1') and (c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')))))
    return ''.join(_o)


def m0474(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Free Cooling', 'Non disponibile', 'unkn...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Free Cooling', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0475(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))
    return ''.join(_o)


def m0476(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == ('Velocità...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == ('Velocità 0' if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0477(c, V):
    # {{ ('Velocità 0' if (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo...
    _o = []
    _o.extend((J.testo(('Velocità 0' if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')), '|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0478(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == ('Vel...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == ('Velocità 0' if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0479(c, V):
    # {{ ('Velocità 0' if (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo...
    _o = []
    _o.append(J.testo(('Velocità 0' if ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')) else 'Free Cooling')))
    return ''.join(_o)


def m0480(c, V):
    # input_boolean.vmc_master_spia_{{ {'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1...
    _o = []
    _o.extend((c.N('binary_sensor.vmc_master_spia_'), J.testo(J.elemento({'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'velocita_notturna', 'Iperventilazione': 'velocita_iperventilazione', 'Free Cooling': 'velocita_freecooling'}, V['velocita_fine_allerta']))))
    return ''.join(_o)


def m0481(c, V):
    # {{ ['input_boolean.vmc_master_spia_velocita_0', 'input_boolean.vmc_master_spia_velocita...
    _o = []
    _o.append(J.testo(J.f_join(J.f_reject([c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')], c.test('eq'), J.concat(c.N('binary_sensor.vmc_master_spia_'), J.elemento({'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'velocita_notturna', 'Iperventilazione': 'velocita_iperventilazione', 'Free Cooling': 'velocita_freecooling'}, V['velocita_fine_allerta']))), ',')))
    return ''.join(_o)


def m0482(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != V['velocita_fine_allerta']))))
    return ''.join(_o)


def m0483(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Iperventilazione', 'Non disponibile', '...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Iperventilazione', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0484(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Iperventilazione'))))
    return ''.join(_o)


def m0485(c, V):
    # {{states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')=='off' and states('i...
    _o = []
    _o.append(J.testo(((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off'))))
    return ''.join(_o)


def m0486(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Non disponi...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0487(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Velocità 3', 'Non disponi...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Velocità 3', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0488(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Velocità 4', 'Non disponi...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Velocità 4', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0489(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Notturna', 'Non disponibi...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Notturna', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0490(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Free Cooling', 'Non dispo...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Free Cooling', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0491(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Free Cooling'))))
    return ''.join(_o)


def m0492(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_progra...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0493(c, V):
    # {{(states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Cooling Programmato') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti'))))
    return ''.join(_o)


def m0494(c, V):
    # {{(states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Heating Programmato') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti'))))
    return ''.join(_o)


def m0495(c, V):
    # {{states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inter...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)'))))
    return ''.join(_o)


def m0496(c, V):
    # {{states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inter...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Allerta Free Heating Programmato (Raffrescamento Arrestato)'))))
    return ''.join(_o)


def m0497(c, V):
    # {{ vel_prima_del_comando not in ['Velocità 0', 'Velocità 1', 'Iperventilazione', 'Non d...
    _o = []
    _o.append(J.testo((V['vel_prima_del_comando'] not in ['Velocità 0', 'Velocità 1', 'Iperventilazione', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0498(c, V):
    # {{states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')== 'off' a...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))))
    return ''.join(_o)


def m0499(c, V):
    # {{states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')== 'on' or...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on'))))
    return ''.join(_o)


def m0500(c, V):
    # {{ trigger.entity_id == 'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr' }}
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'entity_id') == c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'))))
    return ''.join(_o)


def m0501(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio') =='on' or states('...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'off'))))
    return ''.join(_o)


def m0502(c, V):
    # {%- set pdr = states.input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr -%} {%-...
    v_pdr = v_memorie = J.MANCANTE
    _o = []
    v_pdr = c.oggetto(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'))
    v_memorie = J.f_list(J.f_selectattr(c.expand([c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]), 'state', c.test('eq'), 'on'))
    _o.append(J.testo(((((J.attributo(V['trigger'], 'entity_id') != c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) and (not J.t_none(J.leggi(v_pdr, 'pdr')))) and (J.f_length(J.leggi(v_memorie, 'memorie')) > 0)) and (J.f_max(J.f_map(J.leggi(v_memorie, 'memorie'), attribute='last_changed')) < J.attributo(J.leggi(v_pdr, 'pdr'), 'last_changed')))))
    return ''.join(_o)


def m0503(c, V):
    # {{ states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'on' and s...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) == 'Velocità 0'))))
    return ''.join(_o)


def m0504(c, V):
    # {{ states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'on' and s...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0'))))
    return ''.join(_o)


def m0505(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == ('Velocità...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == ('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0506(c, V):
    # {{ ('Velocità 1' if (states('input_boolean.vmc_master_umidita_verifica_soglia_valore_sp...
    _o = []
    _o.extend((J.testo(('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0')), '|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0507(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == ('Vel...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == ('Velocità 1' if ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and (c.states(c.N('select.vmc_master_speed_umidita')) != 'Velocità 0')) else 'Velocità 0')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0508(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 1'...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0509(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Veloci...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0510(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')== 'off' and states('input_boolean....
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off'))))
    return ''.join(_o)


def m0511(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0512(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_program...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0513(c, V):
    # {{ is_state('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia', 'on') and i...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia'), 'on') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'), 'on'))))
    return ''.join(_o)


def m0514(c, V):
    # {{ states('input_select.vmc_master_speed_umidita') == 'Free Cool./Heat.' and ( states('...
    _o = []
    _o.append(J.testo(((c.states(c.N('select.vmc_master_speed_umidita')) == 'Free Cool./Heat.') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) in ['Allerta Free Heating Programmato (Raffrescamento Arrestato)', 'Allerta Free Heating Programmato (Raffrescamento in atto)', 'Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)', 'Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)', 'Allerta Free Cooling Programmato (Riscaldamento in atto)', 'Allerta Free Cooling Programmato (Riscaldamento Arrestato)', 'Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)', 'Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)', 'Allerta Raffrescamento in atto', 'Allerta Riscaldamento in atto', 'Allerta Riscaldamento in atto, Presenza di Inquinanti', 'Allerta Raffrescamento in atto, Presenza di Inquinanti', 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)', 'Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)', 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)', 'Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)']))))
    return ''.join(_o)


def m0515(c, V):
    # {{ 'Velocità 1' if free_con_allerte else states('input_select.vmc_master_speed_umidita'...
    _o = []
    _o.append(J.testo(('Velocità 1' if V['free_con_allerte'] else c.states(c.N('select.vmc_master_speed_umidita')))))
    return ''.join(_o)


def m0516(c, V):
    # {{ ('Free Cooling' if vel_avvio == 'Free Cool./Heat.' else vel_avvio) if umidita_al_cam...
    _o = []
    _o.append(J.testo((('Free Cooling' if (V['vel_avvio'] == 'Free Cool./Heat.') else V['vel_avvio']) if V['umidita_al_cambio_mese'] else 'Velocità 0')))
    return ''.join(_o)


def m0517(c, V):
    # {{ {'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2',...
    _o = []
    _o.append(J.testo(J.chiama(J.attributo({'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'notturna', 'Iperventilazione': 'iperventilazione', 'Free Cooling': 'freecooling'}, 'get'), V['velocita_finale'], 'velocita_0')))
    return ''.join(_o)


def m0518(c, V):
    # {{ umidita_al_cambio_mese }}
    _o = []
    _o.append(J.testo(V['umidita_al_cambio_mese']))
    return ''.join(_o)


def m0519(c, V):
    # shell_command.vmc_master_{{ comando_vmc }}
    _o = []
    _o.extend((c.N('shell_command.vmc_master_'), J.testo(V['comando_vmc'])))
    return ''.join(_o)


def m0520(c, V):
    # {{states('input_boolean.vmc_master_spia_co2_o_voc')=='off' and states('input_boolean.vm...
    _o = []
    _o.append(J.testo((((((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == V['velocita_finale'])) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0521(c, V):
    # {{ velocita_finale }}|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend((J.testo(V['velocita_finale']), '|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0522(c, V):
    # {{ not (states('input_boolean.vmc_master_spia_co2_o_voc')=='off' and states('input_bool...
    _o = []
    _o.append(J.testo((not ((((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == V['velocita_finale'])) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0523(c, V):
    # input_boolean.vmc_master_spia_{{ {'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1...
    _o = []
    _o.extend((c.N('binary_sensor.vmc_master_spia_'), J.testo(J.elemento({'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'velocita_notturna', 'Iperventilazione': 'velocita_iperventilazione', 'Free Cooling': 'velocita_freecooling'}, V['velocita_finale']))))
    return ''.join(_o)


def m0524(c, V):
    # {{ ['input_boolean.vmc_master_spia_velocita_0', 'input_boolean.vmc_master_spia_velocita...
    _o = []
    _o.append(J.testo(J.f_join(J.f_reject([c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')], c.test('eq'), J.concat(c.N('binary_sensor.vmc_master_spia_'), J.elemento({'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'velocita_notturna', 'Iperventilazione': 'velocita_iperventilazione', 'Free Cooling': 'velocita_freecooling'}, V['velocita_finale']))), ',')))
    return ''.join(_o)


def m0525(c, V):
    # {{ is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') and states('sensor.vmc...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != V['velocita_finale']))))
    return ''.join(_o)


def m0526(c, V):
    # {{ states('sensor.vmc_master_status_freeheating') != 'OK' }}
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_freeheating')) != 'OK')))
    return ''.join(_o)


def m0527(c, V):
    # {{ is_state('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia', 'on') and i...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia'), 'on') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'), 'on'))))
    return ''.join(_o)


def m0528(c, V):
    # {{ states('sensor.vmc_master_status_freecooling') != 'OK' }}
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_freecooling')) != 'OK')))
    return ''.join(_o)


def m0529(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0530(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 1'))))
    return ''.join(_o)


def m0531(c, V):
    # {{ (is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - states.sen...
    _o = []
    _o.append(J.testo(((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line')) and (not c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 1'))))
    return ''.join(_o)


def m0532(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0533(c, V):
    # {{ (is_state('binary_sensor.vmc_master_black_out_rilevato', 'on') or (is_state('sensor....
    _o = []
    _o.append(J.testo(((c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on') or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0'))))
    return ''.join(_o)


def m0534(c, V):
    # {{ (is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - states.sen...
    _o = []
    _o.append(J.testo(((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line')) and (not c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on'))) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0'))))
    return ''.join(_o)


def m0535(c, V):
    # {{ ( states('input_boolean.vmc_master_spia_co2_o_voc') == 'off' and states('input_boole...
    _o = []
    _o.append(J.testo((((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and ((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')))))
    return ''.join(_o)


def m0536(c, V):
    # {{ states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'on' and (...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and ((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) != 'ON-Line') or (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Non disponibile')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'on')))))
    return ''.join(_o)


def m0537(c, V):
    # {{ states('sensor.vmc_master_status_ip_interfaccia') == 'ON-Line' and states('sensor.vm...
    _o = []
    _o.append(J.testo(((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'off'))) and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off')))))
    return ''.join(_o)


def m0538(c, V):
    # {{ states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'on' }}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')))
    return ''.join(_o)


def m0539(c, V):
    # {{ not (states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'on' ...
    _o = []
    _o.append(J.testo((not ((c.states(c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on') and ((((((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) != 'ON-Line') or (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) == 'Non disponibile')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling')) == 'on'))))))
    return ''.join(_o)


def m0540(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on') and (is_state('sensor.vmc_...
    _o = []
    _o.append(J.testo((c.is_state(c.N('binary_sensor.vmc_master_spia_co2_o_voc'), 'on') and (c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_co2'), 'Allerta') or c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_voc'), 'Allerta')))))
    return ''.join(_o)


def m0541(c, V):
    # {%- set da = trigger.from_state.state.split(',') if trigger.platform == 'state' and tri...
    v_da = v_a = J.MANCANTE
    _o = []
    v_da = (J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'from_state'), 'state'), 'split'), ',') if ((J.attributo(V['trigger'], 'platform') == 'state') and (not J.t_none(J.attributo(V['trigger'], 'from_state')))) else [])
    v_a = (J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), ',') if ((J.attributo(V['trigger'], 'platform') == 'state') and (not J.t_none(J.attributo(V['trigger'], 'to_state')))) else [])
    _o.append(J.testo(((((((J.attributo(V['trigger'], 'platform') == 'event') and (not J.t_none(J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'context'), 'user_id')))) and c.is_state(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'), 'Velocità 1')) or (((((J.attributo(V['trigger'], 'platform') == 'state') and (J.f_length(J.leggi(v_da, 'da')) > 1)) and (J.f_length(J.leggi(v_a, 'a')) > 1)) and (J.elemento(J.leggi(v_a, 'a'), 1) == '00001')) and (J.elemento(J.leggi(v_da, 'da'), 1) in ['00000', '00002', '00003', '00004', '00005', '00006', '00007']))) and (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line') or (c.states(c.N('sensor.vmc_master_status_ventola')) not in ['unavailable', 'unknown', '']))) and (((((((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1'), 'off') and ((((((c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_0'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_3'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_4'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_notturna'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), 'on'))) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'off')) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2))) or ((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_black_out'), 'on') and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))) and ((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))))
    return ''.join(_o)


def m0542(c, V):
    # {{ is_state('sensor.vmc_master_status_ventola_lettura_codice_interpretato', 'Velocità 0...
    _o = []
    _o.append(J.testo(((((((((((c.is_state(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'), 'Velocità 0') and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), 'off'))))
    return ''.join(_o)


def m0543(c, V):
    # {%- set vel = states.sensor.vmc_master_status_ventola_lettura_codice_interpretato -%} {...
    v_vel = v_rete = v_fase = J.MANCANTE
    _o = []
    v_vel = c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))
    v_rete = c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia'))
    v_fase = c.oggetto(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio'))
    _o.append(J.testo((((((not J.t_none(J.leggi(v_vel, 'vel'))) and (not J.t_none(J.leggi(v_rete, 'rete')))) and (J.attributo(J.leggi(v_vel, 'vel'), 'state') not in ['Velocità 1', 'Non disponibile', 'unknown', 'unavailable', ''])) and (J.as_timestamp(J.attributo(J.leggi(v_vel, 'vel'), 'last_changed')) > (J.as_timestamp(J.attributo(J.leggi(v_rete, 'rete'), 'last_changed')) - 20))) and (J.t_none(J.leggi(v_fase, 'fase')) or (J.as_timestamp(J.attributo(J.leggi(v_vel, 'vel'), 'last_changed')) > J.as_timestamp(J.attributo(J.leggi(v_fase, 'fase'), 'last_changed')))))))
    return ''.join(_o)


def m0544(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0545(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0546(c, V):
    # {{ not (states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr') == 'on' an...
    _o = []
    _o.append(J.testo((not ((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")))))
    return ''.join(_o)


def m0547(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0548(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0549(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0550(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0551(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0552(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0553(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0554(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0555(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Notturna'...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0556(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0557(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Free Cool...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0558(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0559(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Iperventi...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0560(c, V):
    # {{ states('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on')))
    return ''.join(_o)


def m0561(c, V):
    # {{ ( ( states('input_boolean.vmc_master_spia_co2_o_voc')== 'on'and states('input_boolea...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')) or ((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')))))
    return ''.join(_o)


def m0562(c, V):
    # {{ is_state('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia', 'off') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')))
    return ''.join(_o)


def m0563(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') not in ['Velo...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in ['Velocità 0', 'Non disponibile', 'unknown', 'unavailable', ''])))
    return ''.join(_o)


def m0564(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') != vel_prima_...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != V['vel_prima_del_comando']) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0565(c, V):
    # {{ not (is_state('sensor.vmc_master_status_ventola', 'unavailable') and is_state('input...
    _o = []
    _o.append(J.testo((not ((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), 'on')) and c.is_state(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), 'off')) and c.is_state(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'off')) and ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))), slice(0, 5, None)))) or (((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == J.f_capitalize(J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.elemento(c.states(J.concat(c.N('time.vmc_master_accensione_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.elemento(c.states(J.concat(c.N('time.vmc_master_spegnimento_'), J.elemento(['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'], J.chiama(J.attributo(c.now(), 'weekday'))), '_2')), slice(0, 5, None)))))))))
    return ''.join(_o)


def m0566(c, V):
    # {{ not( ( states('input_boolean.vmc_master_spia_co2_o_voc')== 'on'and states('input_boo...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on')) or ((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'on'))))))
    return ''.join(_o)


def m0567(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')=='off' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')))))
    return ''.join(_o)


def m0568(c, V):
    # {{ (states('input_boolean.vmc_master_spia_co2_o_voc')=='on' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0569(c, V):
    # {{ (states('input_boolean.vmc_master_spia_co2_o_voc')=='off' and states('input_boolean....
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')))))
    return ''.join(_o)


def m0570(c, V):
    # {{ ( states('input_boolean.vmc_master_spia_co2_o_voc')=='on' and states('input_boolean....
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on')))))
    return ''.join(_o)


def m0571(c, V):
    # {{ states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario') == 'on' ...
    _o = []
    _o.append(J.testo((((c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile'))))
    return ''.join(_o)


def m0572(c, V):
    # {{ (states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia') == 'on'...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'on')))))
    return ''.join(_o)


def m0573(c, V):
    # {{ states('input_boolean.vmc_master_spia_calendario_lunedi_1') == 'on' or states('input...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'on'))))
    return ''.join(_o)


def m0574(c, V):
    # {{ states('input_boolean.vmc_master_spia_calendario_lunedi_2') == 'on' or states('input...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'on'))))
    return ''.join(_o)


def m0575(c, V):
    # {{ states('sensor.vmc_master_status_ventola') in ['unavailable', 'unknown', ''] and ( s...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola')) in ['unavailable', 'unknown', '']) and ((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'on')))))
    return ''.join(_o)


def m0576(c, V):
    # {{ states('input_number.vmc_master_fase_riallineamento_al_riavvio') | float(0) >= 1 and...
    _o = []
    _o.append(J.testo((((J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 1) and (J.f_float(c.states(c.N('sensor.vmc_master_fase_riallineamento_al_riavvio')), 0) <= 3)) and (J.chiama(J.attributo((J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed') - J.attributo(J.attributo(V['trigger'], 'from_state'), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))))
    return ''.join(_o)


def m0577(c, V):
    # {{ as_timestamp(states.input_boolean.vmc_master_spia_calendario_comando_non_eseguito.la...
    _o = []
    _o.append(J.testo((J.as_timestamp(J.attributo(c.oggetto(c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')), 'last_changed'), 0) if (not J.t_none(c.oggetto(c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')))) else 0)))
    return ''.join(_o)


def m0578(c, V):
    # {{ states('sensor.vmc_master_status_ip_interfaccia') == 'ON-Line' and states('input_boo...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile'))))
    return ''.join(_o)


def m0579(c, V):
    # {{ comando_non_eseguito_dalle }}
    _o = []
    _o.append(J.testo(V['comando_non_eseguito_dalle']))
    return ''.join(_o)


def m0580(c, V):
    # {{ states('input_boolean.vmc_master_spia_calendario_lunedi_1') == 'off' and states('inp...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')) == 'off'))))
    return ''.join(_o)


def m0581(c, V):
    # {{ states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia') == 'off'...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))))
    return ''.join(_o)


def m0582(c, V):
    # {% set codici = {'00000': 'Velocità 0', '00001': 'Velocità 1', '00002': 'Velocità 2', '...
    v_codici = v_lettura = J.MANCANTE
    _o = []
    v_codici = {'00000': 'Velocità 0', '00001': 'Velocità 1', '00002': 'Velocità 2', '00003': 'Velocità 3', '00004': 'Velocità 4', '00005': 'Iperventilazione', '00006': 'Notturna', '00007': 'Free Cooling'}
    _o.append(' ')
    v_lettura = J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola')), 'split'), ',')
    _o.extend((' ', J.testo(((((J.f_length(J.leggi(v_lettura, 'lettura')) > 1) and (J.chiama(J.attributo(J.leggi(v_codici, 'codici'), 'get'), J.elemento(J.leggi(v_lettura, 'lettura'), 1), 'Non disponibile') == c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')))) and (not J.t_none(c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))))) and (J.as_timestamp(J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')), 'last_changed'), 0) <= J.f_float(V['comando_non_eseguito_dalle'], 0))))))
    return ''.join(_o)


def m0583(c, V):
    # {{ not (states('input_boolean.vmc_master_spia_co2_o_voc') == 'on' and (states('input_bo...
    _o = []
    _o.append(J.testo((not ((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and ((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on') or (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'off'))))))
    return ''.join(_o)


def m0584(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc') == 'on' and (states('input_boolean...
    _o = []
    _o.append(J.testo(((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and ((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'on') or (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'off')))))
    return ''.join(_o)


def m0585(c, V):
    # {{ (states('input_text.vmc_master_comando_non_eseguito') ~ '|0').split('|') }}
    _o = []
    _o.append(J.testo(J.chiama(J.attributo(J.concat(c.states(c.N('sensor.vmc_master_comando_non_eseguito')), '|0'), 'split'), '|')))
    return ''.join(_o)


def m0586(c, V):
    # {{ comando_non_eseguito[0] }}
    _o = []
    _o.append(J.testo(J.elemento(V['comando_non_eseguito'], 0)))
    return ''.join(_o)


def m0587(c, V):
    # {{ comando_non_eseguito[1] | float(0) }}
    _o = []
    _o.append(J.testo(J.f_float(J.elemento(V['comando_non_eseguito'], 1), 0)))
    return ''.join(_o)


def m0588(c, V):
    # {{ {'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2',...
    _o = []
    _o.append(J.testo(J.chiama(J.attributo({'Velocità 0': 'velocita_0', 'Velocità 1': 'velocita_1', 'Velocità 2': 'velocita_2', 'Velocità 3': 'velocita_3', 'Velocità 4': 'velocita_4', 'Notturna': 'notturna', 'Iperventilazione': 'iperventilazione', 'Free Cooling': 'freecooling'}, 'get'), J.elemento(V['comando_non_eseguito'], 0), '')))
    return ''.join(_o)


def m0589(c, V):
    # {%- set vel = states.sensor.vmc_master_status_ventola_lettura_codice_interpretato -%} {...
    v_vel = J.MANCANTE
    _o = []
    v_vel = c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'))
    _o.append(J.testo((((((((V['comando_vmc'] != '') and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('binary_sensor.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (not J.t_none(J.leggi(v_vel, 'vel')))) and (J.attributo(J.leggi(v_vel, 'vel'), 'state') != V['velocita_del_comando'])) and (J.as_timestamp(J.attributo(J.leggi(v_vel, 'vel'), 'last_changed'), 0) <= V['comando_non_eseguito_dalle']))))
    return ''.join(_o)


def m0590(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == velocita_d...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == V['velocita_del_comando']) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or ((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and (((((((((((((c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), 'on') or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), 'on')) or c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), 'on'))))))
    return ''.join(_o)


def m0591(c, V):
    # {{ velocita_del_comando }}|{{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.extend((J.testo(V['velocita_del_comando']), '|', J.testo(J.f_round(J.as_timestamp(c.now()), 1))))
    return ''.join(_o)


def m0592(c, V):
    # {{ not (states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == veloc...
    _o = []
    _o.append(J.testo((not (((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == V['velocita_del_comando']) or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')))))
    return ''.join(_o)


def m0593(c, V):
    # {{ is_state('input_boolean.vmc_master_spia_calendario_black_out', 'on') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('binary_sensor.vmc_master_spia_calendario_black_out'), 'on')))
    return ''.join(_o)


def m0594(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Lun...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Lunedi') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Lunedi')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_lunedi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_lunedi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0595(c, V):
    # {{ (states('sensor.vmc_master_alert_monitoraggio_co2') == 'Allerta' or states('sensor.v...
    _o = []
    _o.append(J.testo(((((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta')) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'on')) and (not V['black_out_durante_la_fascia']))))
    return ''.join(_o)


def m0596(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Mar...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Martedi') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Martedi')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_martedi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_martedi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0597(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Mer...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Mercoledi') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Mercoledi')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_mercoledi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0598(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Gio...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Giovedi') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Giovedi')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_giovedi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_giovedi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0599(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Ven...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Venerdi') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Venerdi')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_venerdi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_venerdi_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0600(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Sab...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Sabato') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Sabato')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_sabato_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_sabato_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0601(c, V):
    # {{ not ( states('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2') == "Dom...
    _o = []
    _o.append(J.testo((not ((((c.states(c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2')) == 'Domenica') and (c.states(c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2')) == 'Domenica')) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') >= J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_accensione_domenica_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))) and (J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M') < J.chiama(J.attributo(J.strptime(c.states(c.N('time.vmc_master_spegnimento_domenica_2')), '%H:%M:%S'), 'strftime'), '%H:%M'))))))
    return ''.join(_o)


def m0602(c, V):
    # {{ states('sensor.vmc_master_nome_status') not in ["sconosciuto", "unknown", "", none, ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_nome_status')) not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))
    return ''.join(_o)


def m0603(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')=='on' and states...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0604(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == "Se ne sconsiglia...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")))
    return ''.join(_o)


def m0605(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')== 'on' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == ('on' if (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")) else 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0606(c, V):
    # {{ (states('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')=='on' and states('...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0607(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')== 'on' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == ('on' if (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")) else 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0608(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')=='on' and states...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0609(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')== 'on' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == ('on' if (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")) else 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0610(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')=='on' and states...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0611(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')== 'on' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == ('on' if (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")) else 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0612(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')=='on' and...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0613(c, V):
    # {{ states('input_boolean.vmc_master_spia_co2_o_voc')== 'on' and states('input_boolean.v...
    _o = []
    _o.append(J.testo((((((((((((((((((((((c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == ('on' if (c.is_state(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'on') and (c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego")) else 'off'))) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off'))))
    return ''.join(_o)


def m0614(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')==...
    _o = []
    _o.append(J.testo((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'on'))))
    return ''.join(_o)


def m0615(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')=='on' ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling'])) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')))))
    return ''.join(_o)


def m0616(c, V):
    # {{ ( (states('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')=='on' ...
    _o = []
    _o.append(J.testo(((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) in ['Velocità 0', 'Free Cooling'])) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'on')) and (((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) or ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on'))))))
    return ''.join(_o)


def m0617(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')!='Velocità 0'...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off'))))
    return ''.join(_o)


def m0618(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')!='Velocità 0'...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')))))
    return ''.join(_o)


def m0619(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') != 'Velocità ...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0') and ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on'))) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')))))
    return ''.join(_o)


def m0620(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') != 'Free Cool...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Free Cooling')))
    return ''.join(_o)


def m0621(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') != 'Velocità ...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0') and ((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'on')) or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'on'))) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')))))
    return ''.join(_o)


def m0622(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Free Cool./Heat.'))))
    return ''.join(_o)


def m0623(c, V):
    # {{(states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')== 'off' and states('inp...
    _o = []
    _o.append(J.testo((((((((c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')) == 'off') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off'))))
    return ''.join(_o)


def m0624(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')=='Velocità 0'...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and ((c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'on') or (c.states(c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'on')))))
    return ''.join(_o)
