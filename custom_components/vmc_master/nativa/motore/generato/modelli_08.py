"""Modelli Jinja del package, tradotti in Python (parte 8 di 9).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from .. import jinja as J


def m0867(c, V):
    # {{ states('sensor.vmc_master_umidita_esterna_selezionata') == '-100' and not states('in...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_umidita_esterna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('input_select.vmc_master_selected_humidity_external_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0868(c, V):
    # {{ states('sensor.vmc_master_umidita_interna_selezionata') == '-100' and not states('in...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_umidita_interna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('input_select.vmc_master_selected_humidity_internal_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0869(c, V):
    # {{ states('sensor.vmc_master_co2_interna_selezionata') == '-100' and not states('input_...
    _o = []
    _o.append(J.testo((((((((((((c.states(c.N('sensor.vmc_master_co2_interna_selezionata')) == '-100') and (not J.chiama(J.attributo(c.states(c.N('input_select.vmc_master_selected_co2_internal_entity')), 'startswith'), 'Aggiorna Elenco'))) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0870(c, V):
    # {{ states('sensor.vmc_master_spia_pannello_alert_monitoraggio_totale') in ['unknown', '...
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_spia_pannello_alert_monitoraggio_totale')) in ['unknown', 'unavailable', '', 'sconosciuto', 'Non disponibile', None]) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off'))))
    return ''.join(_o)


def m0871(c, V):
    # {{ ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita') == 'on' a...
    _o = []
    _o.append(J.testo((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_umidita')) == 'Allerta')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0872(c, V):
    # {{ states('input_number.vmc_master_attesa_umidita_avvio') | int(28) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_umidita_avvio')), 28)))
    return ''.join(_o)


def m0873(c, V):
    # {{ ( states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita') == 'on' a...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_umidita')) != 'Allerta')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0874(c, V):
    # {{ states('input_number.vmc_master_attesa_umidita_fine') | int(28) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_umidita_fine')), 28)))
    return ''.join(_o)


def m0875(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo((((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_umidita')) == 'Allerta') or (c.states(c.N('input_boolean.vmc_master_spia_umidita_velocita_0')) == 'off'))) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and (((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)) or (c.states(c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0')) == 'on')))))
    return ''.join(_o)


def m0876(c, V):
    # {{ states('input_number.vmc_master_attesa_umidita_memoria') | int(4) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_umidita_memoria')), 4)))
    return ''.join(_o)


def m0877(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0878(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0879(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0880(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0881(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Notturna...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0882(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Ipervent...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0883(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Free Coo...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0884(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and (states('sensor...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0885(c, V):
    # {{ states('input_number.vmc_master_attesa_delta_avvio') | int(4) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_delta_avvio')), 4)))
    return ''.join(_o)


def m0886(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') != 'Si' and ( states('input...
    _o = []
    _o.append(J.testo((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) != 'Si') and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'on') or (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'on'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0887(c, V):
    # {{ states('input_number.vmc_master_attesa_delta_fine') | int(4) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_delta_fine')), 4)))
    return ''.join(_o)


def m0888(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0889(c, V):
    # {{ states('input_number.vmc_master_attesa_delta_memoria') | int(4) }}
    _o = []
    _o.append(J.testo(J.f_int(c.states(c.N('input_number.vmc_master_attesa_delta_memoria')), 4)))
    return ''.join(_o)


def m0890(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0891(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0892(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0893(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0894(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0895(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0896(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0897(c, V):
    # {% set temperatura_esterna_sensor_entities = states.sensor | selectattr('attributes.dev...
    v_temperatura_esterna_sensor_entities = v_temperatura_esterna_weather_entities = v_last_temperatura_esterna_entity = v_temperatura_esterna_weather_memorizzata = v_temperatura_esterna_custom_entities = v_temperatura_esterna_entities = J.MANCANTE
    _o = []
    v_temperatura_esterna_sensor_entities = J.f_list(J.f_reject(J.f_reject(J.f_map(J.f_selectattr(J.attributo(c.states, 'sensor'), 'attributes.device_class', c.test('eq'), 'temperature'), attribute='entity_id'), c.test('search'), '_temperatura_esterna_selezionata$'), c.test('search'), '_temperatura_interna_selezionata$'))
    _o.append('\n\n')
    v_temperatura_esterna_weather_entities = J.f_list(J.f_map(J.f_selectattr(J.attributo(c.states, 'weather'), 'attributes.temperature', 'defined'), attribute='entity_id'))
    _o.extend(('\n\n', ' '))
    v_last_temperatura_esterna_entity = c.states(c.N('input_text.vmc_master_last_temp_external_entity'))
    _o.append(' ')
    v_temperatura_esterna_weather_memorizzata = ([J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity')] if ((J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity') in J.f_list(J.f_map(J.attributo(c.states, 'weather'), attribute='entity_id'))) and (J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity') not in J.leggi(v_temperatura_esterna_weather_entities, 'temperatura_esterna_weather_entities'))) else [])
    _o.extend(('\n', ' '))
    v_temperatura_esterna_custom_entities = [c.N('sensor.vmc_master_temp_esterna_status_senza_offset')]
    _o.append('\n')
    v_temperatura_esterna_entities = J.f_list(J.f_unique((((J.leggi(v_temperatura_esterna_sensor_entities, 'temperatura_esterna_sensor_entities') + J.leggi(v_temperatura_esterna_weather_entities, 'temperatura_esterna_weather_entities')) + J.leggi(v_temperatura_esterna_weather_memorizzata, 'temperatura_esterna_weather_memorizzata')) + J.leggi(v_temperatura_esterna_custom_entities, 'temperatura_esterna_custom_entities'))))
    _o.append('\n')
    if ('Aggiorna Elenco Entità Temperatura Esterna' not in J.leggi(v_temperatura_esterna_entities, 'temperatura_esterna_entities')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Entità Temperatura Esterna'] + J.leggi(v_temperatura_esterna_entities, 'temperatura_esterna_entities'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_temperatura_esterna_entities, 'temperatura_esterna_entities')), '\n'))
    return ''.join(_o)


def m0898(c, V):
    # {{ states('input_text.vmc_master_last_temp_external_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_temp_external_entity'))))
    return ''.join(_o)


def m0899(c, V):
    # {% set last_temperatura_esterna_entity = states('input_text.vmc_master_last_temp_extern...
    v_last_temperatura_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_temperatura_esterna_entity = c.states(c.N('input_text.vmc_master_last_temp_external_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_temp_external_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0900(c, V):
    # {{ state_attr('input_select.vmc_master_selected_temp_external_entity', 'options') | rej...
    _o = []
    _o.append(J.testo((J.f_count(J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_temp_external_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Temperatura Esterna'))) > 0)))
    return ''.join(_o)


def m0901(c, V):
    # {% set last_temperatura_esterna_entity = states('input_text.vmc_master_last_temp_extern...
    v_last_temperatura_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_temperatura_esterna_entity = c.states(c.N('input_text.vmc_master_last_temp_external_entity'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_temp_external_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Temperatura Esterna'))
    _o.extend((' ', J.testo(((((J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_temperatura_esterna_entity, 'last_temperatura_esterna_entity') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0902(c, V):
    # {{ states('input_select.vmc_master_selected_temp_external_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_temp_external_entity'))))
    return ''.join(_o)


def m0903(c, V):
    # {% set selected_temperatura_esterna_entity = states('input_select.vmc_master_selected_t...
    v_selected_temperatura_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_temperatura_esterna_entity = c.states(c.N('input_select.vmc_master_selected_temp_external_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_temp_external_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_temperatura_esterna_entity, 'selected_temperatura_esterna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_temperatura_esterna_entity, 'selected_temperatura_esterna_entity') not in ['Aggiorna Elenco Entità Temperatura Esterna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0904(c, V):
    # {% set selected_temperatura_esterna_entity = states('input_select.vmc_master_selected_t...
    v_selected_temperatura_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_temperatura_esterna_entity = c.states(c.N('input_select.vmc_master_selected_temp_external_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_temp_external_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_temperatura_esterna_entity, 'selected_temperatura_esterna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_temperatura_esterna_entity, 'selected_temperatura_esterna_entity') in ['Aggiorna Elenco Entità Temperatura Esterna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0905(c, V):
    # {% set temperatura_interna_sensor_entities = states.sensor | selectattr('attributes.dev...
    v_temperatura_interna_sensor_entities = v_temperatura_interna_custom_entities = v_temperatura_interna_entities = J.MANCANTE
    _o = []
    v_temperatura_interna_sensor_entities = J.f_list(J.f_reject(J.f_reject(J.f_map(J.f_selectattr(J.attributo(c.states, 'sensor'), 'attributes.device_class', c.test('eq'), 'temperature'), attribute='entity_id'), c.test('search'), '_temperatura_esterna_selezionata$'), c.test('search'), '_temperatura_interna_selezionata$'))
    _o.extend(('\n\n', ' '))
    v_temperatura_interna_custom_entities = [c.N('sensor.vmc_master_temp_interna_status_senza_offset')]
    _o.append('\n')
    v_temperatura_interna_entities = J.f_list(J.f_unique((J.leggi(v_temperatura_interna_sensor_entities, 'temperatura_interna_sensor_entities') + J.leggi(v_temperatura_interna_custom_entities, 'temperatura_interna_custom_entities'))))
    _o.append('\n')
    if ('Aggiorna Elenco Entità Temperatura Interna' not in J.leggi(v_temperatura_interna_entities, 'temperatura_interna_entities')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Entità Temperatura Interna'] + J.leggi(v_temperatura_interna_entities, 'temperatura_interna_entities'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_temperatura_interna_entities, 'temperatura_interna_entities')), '\n'))
    return ''.join(_o)


def m0906(c, V):
    # {{ states('input_text.vmc_master_last_temp_internal_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_temp_internal_entity'))))
    return ''.join(_o)


def m0907(c, V):
    # {% set last_temperatura_interna_entity = states('input_text.vmc_master_last_temp_intern...
    v_last_temperatura_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_temperatura_interna_entity = c.states(c.N('input_text.vmc_master_last_temp_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_temp_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_temperatura_interna_entity, 'last_temperatura_interna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_temperatura_interna_entity, 'last_temperatura_interna_entity') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0908(c, V):
    # {{ state_attr('input_select.vmc_master_selected_temp_internal_entity', 'options') | rej...
    _o = []
    _o.append(J.testo((J.f_count(J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_temp_internal_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Temperatura Interna'))) > 0)))
    return ''.join(_o)


def m0909(c, V):
    # {% set last_temperatura_interna_entity = states('input_text.vmc_master_last_temp_intern...
    v_last_temperatura_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_temperatura_interna_entity = c.states(c.N('input_text.vmc_master_last_temp_internal_entity'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_temp_internal_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Temperatura Interna'))
    _o.extend((' ', J.testo(((((J.leggi(v_last_temperatura_interna_entity, 'last_temperatura_interna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_temperatura_interna_entity, 'last_temperatura_interna_entity') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0910(c, V):
    # {{ states('input_select.vmc_master_selected_temp_internal_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_temp_internal_entity'))))
    return ''.join(_o)


def m0911(c, V):
    # {% set selected_temperatura_interna_entity = states('input_select.vmc_master_selected_t...
    v_selected_temperatura_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_temperatura_interna_entity = c.states(c.N('input_select.vmc_master_selected_temp_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_temp_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_temperatura_interna_entity, 'selected_temperatura_interna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_temperatura_interna_entity, 'selected_temperatura_interna_entity') not in ['Aggiorna Elenco Entità Temperatura Interna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0912(c, V):
    # {% set selected_temperatura_interna_entity = states('input_select.vmc_master_selected_t...
    v_selected_temperatura_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_temperatura_interna_entity = c.states(c.N('input_select.vmc_master_selected_temp_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_temp_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_temperatura_interna_entity, 'selected_temperatura_interna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_temperatura_interna_entity, 'selected_temperatura_interna_entity') in ['Aggiorna Elenco Entità Temperatura Interna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0913(c, V):
    # {% set umidita_esterna_sensor_entities = states.sensor | selectattr('attributes.device_...
    v_umidita_esterna_sensor_entities = v_umidita_esterna_weather_entities = v_last_umidita_esterna_entity = v_umidita_esterna_weather_memorizzata = v_umidita_esterna_entities = J.MANCANTE
    _o = []
    v_umidita_esterna_sensor_entities = J.f_list(J.f_reject(J.f_reject(J.f_map(J.f_selectattr(J.attributo(c.states, 'sensor'), 'attributes.device_class', c.test('eq'), 'humidity'), attribute='entity_id'), c.test('search'), '_umidita_esterna_selezionata$'), c.test('search'), '_umidita_interna_selezionata$'))
    _o.append('\n\n')
    v_umidita_esterna_weather_entities = J.f_list(J.f_map(J.f_selectattr(J.attributo(c.states, 'weather'), 'attributes.humidity', 'defined'), attribute='entity_id'))
    _o.extend(('\n\n', ' '))
    v_last_umidita_esterna_entity = c.states(c.N('input_text.vmc_master_last_humidity_external_entity'))
    _o.append(' ')
    v_umidita_esterna_weather_memorizzata = ([J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity')] if ((J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity') in J.f_list(J.f_map(J.attributo(c.states, 'weather'), attribute='entity_id'))) and (J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity') not in J.leggi(v_umidita_esterna_weather_entities, 'umidita_esterna_weather_entities'))) else [])
    _o.append('\n')
    v_umidita_esterna_entities = J.f_list(J.f_unique(((J.leggi(v_umidita_esterna_sensor_entities, 'umidita_esterna_sensor_entities') + J.leggi(v_umidita_esterna_weather_entities, 'umidita_esterna_weather_entities')) + J.leggi(v_umidita_esterna_weather_memorizzata, 'umidita_esterna_weather_memorizzata'))))
    _o.append('\n')
    if ('Aggiorna Elenco Entità Umidità Esterna' not in J.leggi(v_umidita_esterna_entities, 'umidita_esterna_entities')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Entità Umidità Esterna'] + J.leggi(v_umidita_esterna_entities, 'umidita_esterna_entities'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_umidita_esterna_entities, 'umidita_esterna_entities')), '\n'))
    return ''.join(_o)


def m0914(c, V):
    # {{ states('input_text.vmc_master_last_humidity_external_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_humidity_external_entity'))))
    return ''.join(_o)


def m0915(c, V):
    # {% set last_umidita_esterna_entity = states('input_text.vmc_master_last_humidity_extern...
    v_last_umidita_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_umidita_esterna_entity = c.states(c.N('input_text.vmc_master_last_humidity_external_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_humidity_external_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0916(c, V):
    # {{ state_attr('input_select.vmc_master_selected_humidity_external_entity', 'options') |...
    _o = []
    _o.append(J.testo((J.f_count(J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_humidity_external_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Umidità Esterna'))) > 0)))
    return ''.join(_o)


def m0917(c, V):
    # {% set last_umidita_esterna_entity = states('input_text.vmc_master_last_humidity_extern...
    v_last_umidita_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_umidita_esterna_entity = c.states(c.N('input_text.vmc_master_last_humidity_external_entity'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_humidity_external_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Umidità Esterna'))
    _o.extend((' ', J.testo(((((J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_umidita_esterna_entity, 'last_umidita_esterna_entity') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0918(c, V):
    # {{ states('input_select.vmc_master_selected_humidity_external_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_humidity_external_entity'))))
    return ''.join(_o)


def m0919(c, V):
    # {% set selected_umidita_esterna_entity = states('input_select.vmc_master_selected_humid...
    v_selected_umidita_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_umidita_esterna_entity = c.states(c.N('input_select.vmc_master_selected_humidity_external_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_humidity_external_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_umidita_esterna_entity, 'selected_umidita_esterna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_umidita_esterna_entity, 'selected_umidita_esterna_entity') not in ['Aggiorna Elenco Entità Umidità Esterna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0920(c, V):
    # {% set selected_umidita_esterna_entity = states('input_select.vmc_master_selected_humid...
    v_selected_umidita_esterna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_umidita_esterna_entity = c.states(c.N('input_select.vmc_master_selected_humidity_external_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_humidity_external_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_umidita_esterna_entity, 'selected_umidita_esterna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_umidita_esterna_entity, 'selected_umidita_esterna_entity') in ['Aggiorna Elenco Entità Umidità Esterna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0921(c, V):
    # {% set umidita_interna_sensor_entities = states.sensor | selectattr('attributes.device_...
    v_umidita_interna_sensor_entities = v_umidita_interna_custom_entities = v_umidita_interna_entities = J.MANCANTE
    _o = []
    v_umidita_interna_sensor_entities = J.f_list(J.f_reject(J.f_reject(J.f_map(J.f_selectattr(J.attributo(c.states, 'sensor'), 'attributes.device_class', c.test('eq'), 'humidity'), attribute='entity_id'), c.test('search'), '_umidita_esterna_selezionata$'), c.test('search'), '_umidita_interna_selezionata$'))
    _o.extend(('\n\n', ' '))
    v_umidita_interna_custom_entities = [c.N('sensor.vmc_master_umidita_interna_status_senza_offset')]
    _o.append('\n')
    v_umidita_interna_entities = J.f_list(J.f_unique((J.leggi(v_umidita_interna_sensor_entities, 'umidita_interna_sensor_entities') + J.leggi(v_umidita_interna_custom_entities, 'umidita_interna_custom_entities'))))
    _o.append('\n')
    if ('Aggiorna Elenco Entità Umidità Interna' not in J.leggi(v_umidita_interna_entities, 'umidita_interna_entities')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Entità Umidità Interna'] + J.leggi(v_umidita_interna_entities, 'umidita_interna_entities'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_umidita_interna_entities, 'umidita_interna_entities')), '\n'))
    return ''.join(_o)


def m0922(c, V):
    # {{ states('input_text.vmc_master_last_humidity_internal_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_humidity_internal_entity'))))
    return ''.join(_o)


def m0923(c, V):
    # {% set last_umidita_interna_entity = states('input_text.vmc_master_last_humidity_intern...
    v_last_umidita_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_umidita_interna_entity = c.states(c.N('input_text.vmc_master_last_humidity_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_humidity_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_umidita_interna_entity, 'last_umidita_interna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_umidita_interna_entity, 'last_umidita_interna_entity') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0924(c, V):
    # {{ state_attr('input_select.vmc_master_selected_humidity_internal_entity', 'options') |...
    _o = []
    _o.append(J.testo((J.f_count(J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_humidity_internal_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Umidità Interna'))) > 0)))
    return ''.join(_o)


def m0925(c, V):
    # {% set last_umidita_interna_entity = states('input_text.vmc_master_last_humidity_intern...
    v_last_umidita_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_umidita_interna_entity = c.states(c.N('input_text.vmc_master_last_humidity_internal_entity'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_humidity_internal_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità Umidità Interna'))
    _o.extend((' ', J.testo(((((J.leggi(v_last_umidita_interna_entity, 'last_umidita_interna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_umidita_interna_entity, 'last_umidita_interna_entity') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0926(c, V):
    # {{ states('input_select.vmc_master_selected_humidity_internal_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_humidity_internal_entity'))))
    return ''.join(_o)


def m0927(c, V):
    # {% set selected_umidita_interna_entity = states('input_select.vmc_master_selected_humid...
    v_selected_umidita_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_umidita_interna_entity = c.states(c.N('input_select.vmc_master_selected_humidity_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_humidity_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_umidita_interna_entity, 'selected_umidita_interna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_umidita_interna_entity, 'selected_umidita_interna_entity') not in ['Aggiorna Elenco Entità Umidità Interna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0928(c, V):
    # {% set selected_umidita_interna_entity = states('input_select.vmc_master_selected_humid...
    v_selected_umidita_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_umidita_interna_entity = c.states(c.N('input_select.vmc_master_selected_humidity_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_humidity_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_umidita_interna_entity, 'selected_umidita_interna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_umidita_interna_entity, 'selected_umidita_interna_entity') in ['Aggiorna Elenco Entità Umidità Interna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0929(c, V):
    # {% set co2_interna_sensor_entities = states.sensor | selectattr('attributes.device_clas...
    v_co2_interna_sensor_entities = v_co2_interna_custom_entities = v_co2_interna_entities = J.MANCANTE
    _o = []
    v_co2_interna_sensor_entities = J.f_list(J.f_reject(J.f_map(J.f_selectattr(J.attributo(c.states, 'sensor'), 'attributes.device_class', c.test('eq'), 'carbon_dioxide'), attribute='entity_id'), c.test('search'), '_co2_interna_selezionata$'))
    _o.append('\n\n')
    v_co2_interna_custom_entities = [c.N('sensor.vmc_master_co2_status_senza_offset')]
    _o.append('\n')
    v_co2_interna_entities = J.f_list(J.f_unique((J.leggi(v_co2_interna_sensor_entities, 'co2_interna_sensor_entities') + J.leggi(v_co2_interna_custom_entities, 'co2_interna_custom_entities'))))
    _o.append('\n')
    if ('Aggiorna Elenco Entità CO₂ Interna' not in J.leggi(v_co2_interna_entities, 'co2_interna_entities')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Entità CO₂ Interna'] + J.leggi(v_co2_interna_entities, 'co2_interna_entities'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_co2_interna_entities, 'co2_interna_entities')), '\n'))
    return ''.join(_o)


def m0930(c, V):
    # {{ states('input_text.vmc_master_last_co2_internal_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_co2_internal_entity'))))
    return ''.join(_o)


def m0931(c, V):
    # {% set last_co2_interna_entity = states('input_text.vmc_master_last_co2_internal_entity...
    v_last_co2_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_co2_interna_entity = c.states(c.N('input_text.vmc_master_last_co2_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_co2_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_co2_interna_entity, 'last_co2_interna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_co2_interna_entity, 'last_co2_interna_entity') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0932(c, V):
    # {{ state_attr('input_select.vmc_master_selected_co2_internal_entity', 'options') | reje...
    _o = []
    _o.append(J.testo((J.f_count(J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_co2_internal_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità CO₂ Interna'))) > 0)))
    return ''.join(_o)


def m0933(c, V):
    # {% set last_co2_interna_entity = states('input_text.vmc_master_last_co2_internal_entity...
    v_last_co2_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_last_co2_interna_entity = c.states(c.N('input_text.vmc_master_last_co2_internal_entity'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_co2_internal_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Entità CO₂ Interna'))
    _o.extend((' ', J.testo(((((J.leggi(v_last_co2_interna_entity, 'last_co2_interna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_co2_interna_entity, 'last_co2_interna_entity') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0934(c, V):
    # {{ states('input_select.vmc_master_selected_co2_internal_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_co2_internal_entity'))))
    return ''.join(_o)


def m0935(c, V):
    # {% set selected_co2_interna_entity = states('input_select.vmc_master_selected_co2_inter...
    v_selected_co2_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_co2_interna_entity = c.states(c.N('input_select.vmc_master_selected_co2_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_co2_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_co2_interna_entity, 'selected_co2_interna_entity') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_co2_interna_entity, 'selected_co2_interna_entity') not in ['Aggiorna Elenco Entità CO₂ Interna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0936(c, V):
    # {% set selected_co2_interna_entity = states('input_select.vmc_master_selected_co2_inter...
    v_selected_co2_interna_entity = v_valid_options = J.MANCANTE
    _o = []
    v_selected_co2_interna_entity = c.states(c.N('input_select.vmc_master_selected_co2_internal_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_co2_internal_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_co2_interna_entity, 'selected_co2_interna_entity') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_co2_interna_entity, 'selected_co2_interna_entity') in ['Aggiorna Elenco Entità CO₂ Interna', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0937(c, V):
    # {% set mobile_app_notify_entities = integration_entities('mobile_app') | select('match'...
    v_mobile_app_notify_entities = J.MANCANTE
    _o = []
    v_mobile_app_notify_entities = J.f_list(J.f_unique(J.f_map(J.f_map(J.f_select(J.f_map(J.f_select(c.integration_entities('mobile_app'), 'match', 'device_tracker'), c.filtro('device_attr'), 'name'), c.test('string')), 'slugify'), 'regex_replace', '^', '')))
    _o.append('\n\n')
    if ('Aggiorna Elenco Dispositivi per Invio Notifica' not in J.leggi(v_mobile_app_notify_entities, 'mobile_app_notify_entities')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Dispositivi per Invio Notifica'] + J.leggi(v_mobile_app_notify_entities, 'mobile_app_notify_entities'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_mobile_app_notify_entities, 'mobile_app_notify_entities')), '\n'))
    return ''.join(_o)


def m0938(c, V):
    # {{ states('input_text.vmc_master_last_notification_device') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_notification_device'))))
    return ''.join(_o)


def m0939(c, V):
    # {% set last_notification_device = states('input_text.vmc_master_last_notification_devic...
    v_last_notification_device = v_valid_options = J.MANCANTE
    _o = []
    v_last_notification_device = c.states(c.N('input_text.vmc_master_last_notification_device'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_notification_device'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_notification_device, 'last_notification_device') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_notification_device, 'last_notification_device') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0940(c, V):
    # {{ state_attr('input_select.vmc_master_selected_notification_device', 'options') | reje...
    _o = []
    _o.append(J.testo((J.f_count(J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_notification_device'), 'options'), c.test('equalto'), 'Aggiorna Elenco Dispositivi per Invio Notifica'))) > 0)))
    return ''.join(_o)


def m0941(c, V):
    # {% set last_notification_device = states('input_text.vmc_master_last_notification_devic...
    v_last_notification_device = v_valid_options = J.MANCANTE
    _o = []
    v_last_notification_device = c.states(c.N('input_text.vmc_master_last_notification_device'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_notification_device'), 'options'), c.test('equalto'), 'Aggiorna Elenco Dispositivi per Invio Notifica'))
    _o.extend((' ', J.testo(((((J.leggi(v_last_notification_device, 'last_notification_device') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_notification_device, 'last_notification_device') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0942(c, V):
    # {{ states('input_select.vmc_master_selected_notification_device') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_notification_device'))))
    return ''.join(_o)


def m0943(c, V):
    # {% set selected_notification_device = states('input_select.vmc_master_selected_notifica...
    v_selected_notification_device = v_valid_options = J.MANCANTE
    _o = []
    v_selected_notification_device = c.states(c.N('input_select.vmc_master_selected_notification_device'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_notification_device'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_notification_device, 'selected_notification_device') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_notification_device, 'selected_notification_device') not in ['Aggiorna Elenco Dispositivi per Invio Notifica', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0944(c, V):
    # {% set selected_notification_device = states('input_select.vmc_master_selected_notifica...
    v_selected_notification_device = v_valid_options = J.MANCANTE
    _o = []
    v_selected_notification_device = c.states(c.N('input_select.vmc_master_selected_notification_device'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_notification_device'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_notification_device, 'selected_notification_device') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_notification_device, 'selected_notification_device') in ['Aggiorna Elenco Dispositivi per Invio Notifica', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0945(c, V):
    # {% set media_players = states.media_player | map(attribute='entity_id') | unique | list...
    v_media_players = J.MANCANTE
    _o = []
    v_media_players = J.f_default(J.f_list(J.f_unique(J.f_map(J.attributo(c.states, 'media_player'), attribute='entity_id'))), [])
    _o.append(' ')
    if ('Aggiorna Elenco Media Player' not in J.leggi(v_media_players, 'media_players')):
        _o.extend(('\n  ', J.testo((['Aggiorna Elenco Media Player'] + J.leggi(v_media_players, 'media_players'))), '\n'))
    else:
        _o.extend(('\n  ', J.testo(J.leggi(v_media_players, 'media_players')), '\n'))
    return ''.join(_o)


def m0946(c, V):
    # {{ states('input_text.vmc_master_last_media_player_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_text.vmc_master_last_media_player_entity'))))
    return ''.join(_o)


def m0947(c, V):
    # {% set last_mp = states('input_text.vmc_master_last_media_player_entity') %} {% set val...
    v_last_mp = v_valid_options = J.MANCANTE
    _o = []
    v_last_mp = c.states(c.N('input_text.vmc_master_last_media_player_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_media_player_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_last_mp, 'last_mp') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_last_mp, 'last_mp') not in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0948(c, V):
    # {% set last_mp = states('input_text.vmc_master_last_media_player_entity') %} {% set val...
    v_last_mp = v_valid_options = J.MANCANTE
    _o = []
    v_last_mp = c.states(c.N('input_text.vmc_master_last_media_player_entity'))
    _o.append(' ')
    v_valid_options = J.f_list(J.f_reject(c.state_attr(c.N('input_select.vmc_master_selected_media_player_entity'), 'options'), c.test('equalto'), 'Aggiorna Elenco Media Player'))
    _o.extend(('\n', J.testo(((((J.leggi(v_last_mp, 'last_mp') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_last_mp, 'last_mp') in ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile'])) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('input_boolean.vmc_master_notifica_status_vmc')) == 'on')))))
    return ''.join(_o)


def m0949(c, V):
    # {{ states('input_select.vmc_master_selected_media_player_entity') }}
    _o = []
    _o.append(J.testo(c.states(c.N('input_select.vmc_master_selected_media_player_entity'))))
    return ''.join(_o)


def m0950(c, V):
    # {% set selected_mp = states('input_select.vmc_master_selected_media_player_entity') %} ...
    v_selected_mp = v_valid_options = J.MANCANTE
    _o = []
    v_selected_mp = c.states(c.N('input_select.vmc_master_selected_media_player_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_media_player_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_mp, 'selected_mp') in J.leggi(v_valid_options, 'valid_options')) and (J.leggi(v_selected_mp, 'selected_mp') not in ['Aggiorna Elenco Media Player', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0951(c, V):
    # {% set selected_mp = states('input_select.vmc_master_selected_media_player_entity') %} ...
    v_selected_mp = v_valid_options = J.MANCANTE
    _o = []
    v_selected_mp = c.states(c.N('input_select.vmc_master_selected_media_player_entity'))
    _o.append(' ')
    v_valid_options = c.state_attr(c.N('input_select.vmc_master_selected_media_player_entity'), 'options')
    _o.extend((' ', J.testo(((J.leggi(v_selected_mp, 'selected_mp') not in J.leggi(v_valid_options, 'valid_options')) or (J.leggi(v_selected_mp, 'selected_mp') in ['Aggiorna Elenco Media Player', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))))
    return ''.join(_o)


def m0952(c, V):
    # notify.mobile_app_{{ states('input_select.vmc_master_selected_notification_device') }}
    _o = []
    _o.extend(('notify.mobile_app_', J.testo(c.states(c.N('input_select.vmc_master_selected_notification_device')))))
    return ''.join(_o)


def m0953(c, V):
    # VMC {{ states('sensor.vmc_master_nome_status') }}
    _o = []
    _o.extend(('VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status')))))
    return ''.join(_o)


def m0954(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_temp_external_entity') }} Impieg...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_temp_external_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_temp_esterna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_temp_esterna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_temp_esterna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_temp_esterna_status'))), ' °C\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0955(c, V):
    # {% set device = states('input_select.vmc_master_selected_notification_device') %} {% se...
    v_device = v_invalid_device = J.MANCANTE
    _o = []
    v_device = c.states(c.N('input_select.vmc_master_selected_notification_device'))
    _o.append(' ')
    v_invalid_device = ['Aggiorna Elenco Dispositivi per Invio Notifica', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile']
    _o.extend((' ', J.testo((J.leggi(v_device, 'device') not in J.leggi(v_invalid_device, 'invalid_device')))))
    return ''.join(_o)


def m0956(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_temp_internal_entity') }} Impieg...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_temp_internal_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_temp_interna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_temp_interna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_temp_interna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_temp_interna_status'))), ' °C\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0957(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_humidity_external_entity') }} Im...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_humidity_external_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_umidita_esterna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_umidita_esterna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_umidita_esterna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0958(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_humidity_internal_entity') }} Im...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_humidity_internal_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_umidita_interna_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_umidita_interna_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_umidita_interna_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status'))), ' %\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0959(c, V):
    # Non Disponibile: {{ states('input_text.vmc_master_last_co2_internal_entity') }} Impiega...
    _o = []
    _o.extend(('Non Disponibile: ', J.testo(c.states(c.N('input_text.vmc_master_last_co2_internal_entity'))), '\nImpiegato per il rilevamento: ', J.testo((c.state_attr(c.N('sensor.vmc_master_co2_status'), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.N('sensor.vmc_master_co2_status')) or ''), ' ', ((c.entity_name(c.N('sensor.vmc_master_co2_status')) or '') if J.t_defined(c.entity_name) else ''))))), '\nIn sostituzione si usa la sonda della VMC, senza Offset: ', J.testo(c.states(c.N('sensor.vmc_master_co2_status'))), ' ppm\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0960(c, V):
    # Avviso ogni 24 ore: Verificare Filtro Data: {{ now().strftime('%d-%m-%Y') }} Ora: {{ no...
    _o = []
    _o.extend(('Avviso ogni 24 ore: Verificare Filtro\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0961(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia') }...
    _o = []
    _o.extend((J.testo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'))), ': in data ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' alle ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S')), '\nLivello di Concentrazione CO₂: ', J.testo(c.states(c.N('sensor.vmc_master_co2_status_verifica_soglia'))), ', ', J.testo(c.states(c.N('sensor.vmc_master_co2_status'))), ' ppm\nLivello di Concentrazione VOC: ', J.testo(c.states(c.N('sensor.vmc_master_voc_status_verifica_soglia'))), ', ', J.testo(c.states(c.N('sensor.vmc_master_voc_status'))), ' ppb\nSuperamento Lim. Δ Punto di Rugiada: ', J.testo(c.states(c.N('sensor.vmc_master_alert_monitoraggio_pdr'))), '\nLivello di Umidità Interna: ', J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status_verifica_soglia'))), ', ', J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status'))), ' %\nImpiego Free H./C.: ', J.testo(c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi'))), '\nVMC Sensori Int. Δ Temp. > 23 [°C] ?: ', J.testo(c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia'))), '\nVMC Congelamento ≤ -18 [°C] Temp. Esterna ?: ', J.testo(c.states(c.N('sensor.vmc_master_congelamento_verifica_soglia'))), '\nVerifica Black-Out: ', J.testo(c.states(c.N('sensor.vmc_master_alert_monitoraggio_black_out')))))
    return ''.join(_o)


def m0962(c, V):
    # {{ states('input_select.vmc_master_selected_notification_device') not in ["Aggiorna Ele...
    _o = []
    _o.append(J.testo((c.states(c.N('input_select.vmc_master_selected_notification_device')) not in ['Aggiorna Elenco Dispositivi per Invio Notifica', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))
    return ''.join(_o)


def m0963(c, V):
    # {{ states('input_select.vmc_master_selected_notification_device') not in ["Aggiorna Ele...
    _o = []
    _o.append(J.testo((c.states(c.N('input_select.vmc_master_selected_notification_device')) not in ['Aggiorna Elenco Dispositivi per Invio Notifica', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile'])))
    return ''.join(_o)


def m0964(c, V):
    # Errore Media Player: {{ states('input_text.vmc_master_last_media_player_entity') }} non...
    _o = []
    _o.extend(('Errore Media Player: ', J.testo(c.states(c.N('input_text.vmc_master_last_media_player_entity'))), ' non disponibile.\nImpiegato per la riproduzione Audio sul Media Player: ', J.testo((c.state_attr(c.states(c.N('input_select.vmc_master_selected_media_player_entity')), 'friendly_name') or J.f_trim(J.concat((c.device_name(c.states(c.N('input_select.vmc_master_selected_media_player_entity'))) or ''), ' ', ((c.entity_name(c.states(c.N('input_select.vmc_master_selected_media_player_entity'))) or '') if J.t_defined(c.entity_name) else ''))))), '\nData: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%d-%m-%Y')), ' Ora: ', J.testo(J.chiama(J.attributo(c.now(), 'strftime'), '%H:%M:%S'))))
    return ''.join(_o)


def m0965(c, V):
    # {% set mp = states('input_select.vmc_master_selected_media_player_entity') %} {% set in...
    v_mp = v_invalid_mp = v_device = v_invalid_device = J.MANCANTE
    _o = []
    v_mp = c.states(c.N('input_select.vmc_master_selected_media_player_entity'))
    _o.append(' ')
    v_invalid_mp = ['Aggiorna Elenco Media Player', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    v_device = c.states(c.N('input_select.vmc_master_selected_notification_device'))
    _o.append(' ')
    v_invalid_device = ['Aggiorna Elenco Dispositivi per Invio Notifica', '', 'sconosciuto', 'unknown', None, 'unavailable', 'Non disponibile']
    _o.extend((' ', J.testo((J.leggi(v_device, 'device') not in J.leggi(v_invalid_device, 'invalid_device')))))
    return ''.join(_o)


def m0966(c, V):
    # {{ not (mantieni_pannelli | default(false) | bool) }}
    _o = []
    _o.append(J.testo((not J.f_bool(J.f_default(V['mantieni_pannelli'], False)))))
    return ''.join(_o)


def m0967(c, V):
    # {{ state_attr('automation.automazione_vmc_master', 'current') | int(0) == 0 }}
    _o = []
    _o.append(J.testo((J.f_int(c.state_attr(c.N('automation.automazione_vmc_master'), 'current'), 0) == 0)))
    return ''.join(_o)


def m0968(c, V):
    # {{ is_state('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia', 'on') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), 'on')))
    return ''.join(_o)


def m0969(c, V):
    # {{ is_state('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia', 'on') }}
    _o = []
    _o.append(J.testo(c.is_state(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), 'on')))
    return ''.join(_o)


def m0970(c, V):
    # {{ delta_in_corso }}
    _o = []
    _o.append(J.testo(V['delta_in_corso']))
    return ''.join(_o)


def m0971(c, V):
    # {{ congelamento_in_corso }}
    _o = []
    _o.append(J.testo(V['congelamento_in_corso']))
    return ''.join(_o)


def m0972(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')))
    return ''.join(_o)


def m0973(c, V):
    # {{ not delta_in_corso and not congelamento_in_corso and states('sensor.vmc_master_statu...
    _o = []
    _o.append(J.testo((((not V['delta_in_corso']) and (not V['congelamento_in_corso'])) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) != 'Velocità 0'))))
    return ''.join(_o)


def m0974(c, V):
    # {{ (comando_non_eseguito_dalle | default(0) | float(0)) == 0 or (states.sensor.vmc_mast...
    _o = []
    _o.append(J.testo(((J.f_float(J.f_default(V['comando_non_eseguito_dalle'], 0), 0) == 0) or ((not J.t_none(c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')))) and (J.as_timestamp(J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')), 'last_changed'), 0) <= J.f_float(V['comando_non_eseguito_dalle'], 0))))))
    return ''.join(_o)


def m0975(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0976(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')=="Se ne sconsiglia l...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta')))))
    return ''.join(_o)


def m0977(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0978(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')=="Se ne sconsiglia l...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (not ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta'))))))
    return ''.join(_o)


def m0979(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')!="Se ne sconsiglia l...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta')))))
    return ''.join(_o)


def m0980(c, V):
    # {{ states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')!="Se ne sconsiglia l...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") and (not ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta'))))))
    return ''.join(_o)


def m0981(c, V):
    # {{ states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')))
    return ''.join(_o)


def m0982(c, V):
    # {{ states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')=='on'}}
    _o = []
    _o.append(J.testo((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'on')))
    return ''.join(_o)


def m0983(c, V):
    # {{ states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')=='off'}}
    _o = []
    _o.append(J.testo((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'off')))
    return ''.join(_o)


def m0984(c, V):
    # {{ states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')=='off'}}
    _o = []
    _o.append(J.testo((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'off')))
    return ''.join(_o)


def m0985(c, V):
    # {{(states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')== 'off' ...
    _o = []
    _o.append(J.testo(((c.states(c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')) == 'off') and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'off'))))
    return ''.join(_o)


def m0986(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0987(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0988(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Velocità ...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0989(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Notturna'...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0990(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Iperventi...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0991(c, V):
    # {{ states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) != 'Nessuna Allerta Free Heating Programmato') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) != 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti'))))
    return ''.join(_o)


def m0992(c, V):
    # {{ states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') == 'Free Cool...
    _o = []
    _o.append(J.testo((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') or ((V['vel_prima_del_comando'] not in ['Non disponibile', 'unknown', 'unavailable', '']) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) not in [V['vel_prima_del_comando'], 'Non disponibile', 'unknown', 'unavailable', '']))) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'OFF-Line') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ip_interfaccia')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32)))) or (c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))))
    return ''.join(_o)


def m0993(c, V):
    # {{ states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Heating Programmato') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti'))))
    return ''.join(_o)


def m0994(c, V):
    # {{ states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') == "Free ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) == 'Free Heating')))
    return ''.join(_o)


def m0995(c, V):
    # {{ (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')=="Se ne sconsiglia ...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and (((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta')) and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'on')))))
    return ''.join(_o)


def m0996(c, V):
    # {{ (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')=="Se ne sconsiglia ...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) == "Se ne sconsiglia l'impiego") and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'on')) and ((not ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta'))) or (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'off')))))
    return ''.join(_o)


def m0997(c, V):
    # {{ (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')!="Se ne sconsiglia ...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") or (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'off')) and (((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta')) and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'on')))))
    return ''.join(_o)


def m0998(c, V):
    # {{ (states('sensor.vmc_master_punto_di_rugiada_verifica_confronto')!="Se ne sconsiglia ...
    _o = []
    _o.append(J.testo((((c.states(c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto')) != "Se ne sconsiglia l'impiego") or (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')) == 'off')) and ((not ((c.states(c.N('sensor.vmc_master_alert_monitoraggio_co2')) == 'Allerta') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_voc')) == 'Allerta'))) or (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')) == 'off')))))
    return ''.join(_o)


def m0999(c, V):
    # {{ states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) != 'Nessuna Allerta Free Cooling Programmato') and (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) != 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti'))))
    return ''.join(_o)


def m1000(c, V):
    # {{ states('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_inte...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Cooling Programmato') or (c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')) == 'Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti'))))
    return ''.join(_o)


def m1001(c, V):
    # {{ states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') == "Free ...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) == 'Free Cooling')))
    return ''.join(_o)


def m1002(c, V):
    # {{ states('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling') not in ["...
    _o = []
    _o.append(J.testo((c.states(c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling')) not in ['Free Heating', 'Free Cooling'])))
    return ''.join(_o)


def m1003(c, V):
    # {{ (is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - states.sen...
    _o = []
    _o.append(J.testo((((c.is_state(c.N('sensor.vmc_master_status_ventola'), 'unavailable') and (J.chiama(J.attributo((c.now() - J.attributo(c.oggetto(c.N('sensor.vmc_master_status_ventola')), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))) and c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line')) and c.is_state(c.N('input_boolean.vmc_master_spia_calendario_black_out'), 'off'))))
    return ''.join(_o)


def m1004(c, V):
    # {{ states('input_number.vmc_master_audio_volume') | float(0.5) }}
    _o = []
    _o.append(J.testo(J.f_float(c.states(c.N('input_number.vmc_master_audio_volume')), 0.5)))
    return ''.join(_o)


def m1005(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} la Velocità Attuale è: {{states...
    v_registrata = J.MANCANTE
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  la Velocità Attuale è: ', J.testo(c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')))))
    v_registrata = c.states(c.N('sensor.vmc_master_velocita_registrata'))
    if (J.leggi(v_registrata, 'registrata') not in ['Nessuna', 'unknown', 'unavailable', '']):
        _o.extend((', Velocità Memorizzata a fine allerta: ', J.testo(J.f_replace(J.leggi(v_registrata, 'registrata'), ' · ', ', '))))
    return ''.join(_o)


def m1006(c, V):
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
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_status_velocita')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_status_velocita')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1007(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} {% set congelamento = states('s...
    v_congelamento = v_congelamento_vmc = J.MANCANTE
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  '))
    v_congelamento = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), default=None)
    _o.append(' ')
    v_congelamento_vmc = J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), default=None)
    _o.append(' ')
    if (((not J.t_none(J.leggi(v_congelamento, 'congelamento'))) and (J.leggi(v_congelamento, 'congelamento') <= (-18))) or ((not J.t_none(J.leggi(v_congelamento_vmc, 'congelamento_vmc'))) and (J.leggi(v_congelamento_vmc, 'congelamento_vmc') <= (-18)))):
        _o.append('\n  Allerta Congelamento, Arresto della VMC\n')
    else:
        _o.append('\n  Allerta Congelamento Prossimo, si consiglia di Arrestare la VMC o di Non Avviare la VMC\n')
    return ''.join(_o)


def m1008(c, V):
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
    _o.append(' ')
    v_start_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_start_raw, 'start_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_start_raw, 'start_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append(' ')
    v_end_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_end_raw, 'end_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_end_raw, 'end_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append('\n')
    if (J.leggi(v_start_time, 'start_time') and J.leggi(v_end_time, 'end_time')):
        _o.append('\n  ')
        if (J.leggi(v_start_time, 'start_time') <= J.leggi(v_end_time, 'end_time')):
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_congelamento')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_congelamento')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1009(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Nessuna Allerta Congelamento
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Nessuna Allerta Congelamento'))
    return ''.join(_o)


def m1010(c, V):
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
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_congelamento')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_congelamento')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1011(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} {% if states('sensor.vmc_master...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  '))
    if (c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si'):
        _o.append('\n  Allerta Differenza tra temperatura interna ed esterna ha superato i 23 °C\n')
    else:
        _o.append('\n  Allerta Differenza tra temperatura interna ed esterna si sta avvicinando a valori superiori a 23 °C.\n')
    return ''.join(_o)


def m1012(c, V):
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
    _o.append(' ')
    v_start_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_start_raw, 'start_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_start_raw, 'start_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append(' ')
    v_end_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_end_raw, 'end_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_end_raw, 'end_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append('\n')
    if (J.leggi(v_start_time, 'start_time') and J.leggi(v_end_time, 'end_time')):
        _o.append('\n  ')
        if (J.leggi(v_start_time, 'start_time') <= J.leggi(v_end_time, 'end_time')):
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_differenza_temp_int_est')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_differenza_temp_int_est')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1013(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Nessuna Allerta Differenza tra ...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Nessuna Allerta Differenza tra temperatura interna ed esterna superiore ai 23 °C'))
    return ''.join(_o)


def m1014(c, V):
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
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_differenza_temp_int_est')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_differenza_temp_int_est')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1015(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Allerta Anidride Carbonica, {{s...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Allerta Anidride Carbonica,  ', J.testo(c.states(c.N('sensor.vmc_master_co2_status_verifica_soglia'))), ', ', J.testo(c.states(c.N('sensor.vmc_master_co2_status'))), ' ppm'))
    return ''.join(_o)


def m1016(c, V):
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
            _o.extend(('\n    ', J.testo(((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('sensor.vmc_master_co2_status_verifica_soglia')) != '-')) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_inquinanti')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo(((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('sensor.vmc_master_co2_status_verifica_soglia')) != '-')) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_inquinanti')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1017(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Nessuna Allerta Anidride Carbonica
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Nessuna Allerta Anidride Carbonica'))
    return ''.join(_o)


def m1018(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Allerta Composti Organici Volat...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Allerta Composti Organici Volatili,  ', J.testo(c.states(c.N('sensor.vmc_master_voc_status_verifica_soglia'))), ', ', J.testo(c.states(c.N('sensor.vmc_master_voc_status'))), ' ppb'))
    return ''.join(_o)


def m1019(c, V):
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
            _o.extend(('\n    ', J.testo(((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('sensor.vmc_master_voc_status_verifica_soglia')) != '-')) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_inquinanti')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo(((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('sensor.vmc_master_voc_status_verifica_soglia')) != '-')) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_inquinanti')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1020(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Nessuna Allerta Composti Organi...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Nessuna Allerta Composti Organici Volatili'))
    return ''.join(_o)


def m1021(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} {% if is_state('sensor.vmc_mast...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  '))
    if c.is_state(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'), 'Velocità 0'):
        _o.append('\n  Allerta Superamento del Punto di Rugiada, si consiglia di Non Avviare la VMC\n')
    elif c.is_state(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), 'off'):
        _o.append('\n  Allerta Superamento del Punto di Rugiada, si consiglia di Arrestare la VMC\n')
    elif (c.is_state(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc'), 'on') and (c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_co2'), 'Allerta') or c.is_state(c.N('sensor.vmc_master_alert_monitoraggio_voc'), 'Allerta'))):
        _o.append('\n  Allerta Superamento del Punto di Rugiada, la VMC resta in funzione per la presenza di Inquinanti\n')
    else:
        _o.append('\n  Allerta Superamento del Punto di Rugiada, Arresto della VMC\n')
    return ''.join(_o)


def m1022(c, V):
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
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_pdr')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_pdr')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1023(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Nessuna Allerta Superamento del...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Nessuna Allerta Superamento del Punto di Rugiada'))
    return ''.join(_o)


def m1024(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} {{ states('sensor.vmc_master_al...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), ' ', J.testo(c.states(c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi')))))
    return ''.join(_o)


def m1025(c, V):
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
    _o.append(' ')
    v_start_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_start_raw, 'start_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_start_raw, 'start_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append(' ')
    v_end_time = (J.chiama(J.attributo(J.strptime(J.leggi(v_end_raw, 'end_raw'), '%H:%M'), 'time')) if J.t_match(J.leggi(v_end_raw, 'end_raw'), '^[0-9]{2}:[0-9]{2}$') else None)
    _o.append('\n')
    if (J.leggi(v_start_time, 'start_time') and J.leggi(v_end_time, 'end_time')):
        _o.append('\n  ')
        if (J.leggi(v_start_time, 'start_time') <= J.leggi(v_end_time, 'end_time')):
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_freecooling_heating')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_freecooling_heating')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1026(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Allerta {{ states('sensor.vmc_m...
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Allerta ', J.testo(c.states(c.N('sensor.vmc_master_umidita_interna_status_verifica_soglia_valore')))))
    return ''.join(_o)


def m1027(c, V):
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
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and (J.leggi(v_start_time, 'start_time') <= J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time'))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_umidita')) == 'on'))), '\n  '))
        else:
            _o.extend(('\n    ', J.testo((((((c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line') and (J.leggi(v_mp, 'mp') not in J.leggi(v_invalid, 'invalid'))) and (J.leggi(v_audio_interruttore, 'audio_interruttore') == 'on')) and ((J.leggi(v_now_time, 'now_time') >= J.leggi(v_start_time, 'start_time')) or (J.leggi(v_now_time, 'now_time') <= J.leggi(v_end_time, 'end_time')))) and (c.states(c.N('input_boolean.vmc_master_notifica_allerta_umidita')) == 'on'))), '\n  '))
        _o.append('\n')
    else:
        _o.append('\n  false\n')
    return ''.join(_o)


def m1028(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Nessuna Allerta Umidità Interna
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Nessuna Allerta Umidità Interna'))
    return ''.join(_o)


def m1029(c, V):
    # Sulla VMC {{ states('sensor.vmc_master_nome_status') }} Allerta Black-Out
    _o = []
    _o.extend(('Sulla VMC ', J.testo(c.states(c.N('sensor.vmc_master_nome_status'))), '  Allerta Black-Out'))
    return ''.join(_o)
