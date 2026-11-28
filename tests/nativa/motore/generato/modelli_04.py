"""Modelli Jinja del package, tradotti in Python (parte 4 di 9).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from custom_components.vmc_master.nativa.motore import jinja as J


def m0313(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0314(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_status_ventola_lettura_codi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0315(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Velocità...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0316(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_status_ventola_lettura_codi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0317(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Notturna...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0318(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_status_ventola_lettura_codi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0319(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Ipervent...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0320(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_status_ventola_lettura_codi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0321(c, V):
    # {{ ( states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')== 'Free Coo...
    _o = []
    _o.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    return ''.join(_o)


def m0322(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_status_ventola_lettura_codi...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling') and (c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (((((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')) == 'off'))) and ((((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off'))) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')) == 'off')) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 4)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0323(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and (states('sensor...
    _o = []
    _o.append(J.testo(((((((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0324(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo(((((((((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0325(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') != 'Si' and ( states('input...
    _o = []
    _o.append(J.testo((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) != 'Si') and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'on') or (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'on'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0326(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((((((((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) != 'Si') and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')) == 'on') or (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')) == 'on'))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off')) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0327(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0328(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 0')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0329(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0330(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 1')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0331(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0332(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 2')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0333(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0334(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 3')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0335(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0336(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Velocità 4')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0337(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0338(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Notturna')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0339(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0340(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Iperventilazione')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0341(c, V):
    # {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia') == 'Si' and states('sensor....
    _o = []
    _o.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    return ''.join(_o)


def m0342(c, V):
    # {%- set vmc_master_esito -%} {{ ( states('sensor.vmc_master_delta_temp_verifica_soglia'...
    v_vmc_master_esito = J.MANCANTE
    _o = []
    _b1 = []
    _b1.append(J.testo((((((((((c.states(c.N('sensor.vmc_master_delta_temp_verifica_soglia')) == 'Si') and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato')) == 'Free Cooling')) and ((J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status')), 0) > (-18)) and (J.f_float(c.states(c.N('sensor.vmc_master_temp_esterna_status_senza_offset')), 0) > (-18)))) and (c.states(c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')) == 'on')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')) != 'Non disponibile')) and ((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')) == 'off'))) and (((((((((c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))) and ((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) == 0) or (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 2)))))
    v_vmc_master_esito = ''.join(_b1)
    v_vmc_master_esito = J.f_lower(J.f_trim(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))))
    _o.append(J.testo((not ((J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')) in ['true', 'yes', 'on', 'enable']) or (J.f_is_number(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito'))) and (J.f_float(J.leggi(v_vmc_master_esito, c.N('vmc_master_esito')), 0) != 0))))))
    return ''.join(_o)


def m0343(c, V):
    # {{ not trigger.id.startswith('ON|blackout_ripristino|blackout_ripristino|Calendario') o...
    _o = []
    _o.append(J.testo(((not J.chiama(J.attributo(J.attributo(V['trigger'], 'id'), 'startswith'), 'ON|blackout_ripristino|blackout_ripristino|Calendario')) or (((c.states(c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on') and ((J.attributo(V['trigger'], 'platform') != 'state') or (((J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) >= 1) and (J.f_float(c.states(c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')), 0) <= 3)) and (J.chiama(J.attributo((J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed') - J.attributo(J.attributo(V['trigger'], 'from_state'), 'last_changed')), 'total_seconds')) >= J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_rilevazione')), 32))))) and ((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'on'))))))
    return ''.join(_o)


def m0344(c, V):
    # {%- if trigger.id == 'allinea' -%}{{ letture.keys() | list }} {%- elif trigger.event.da...
    _o = []
    if (J.attributo(V['trigger'], 'id') == 'allinea'):
        _o.append(J.testo(J.f_list(J.chiama(J.attributo(V['letture'], 'keys')))))
    elif J.t_match(J.f_default(J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'data'), 'entity_id'), ''), c.N('timer\\.vmc_master_lettura_')):
        _o.append(J.testo([J.f_replace(J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'data'), 'entity_id'), c.N('timer.vmc_master_lettura_'), '')]))
    else:
        _o.append(J.testo([]))
    return ''.join(_o)


def m0345(c, V):
    # {{ letture[repeat.item][1] | int(1) }}
    _o = []
    _o.append(J.testo(J.f_int(J.elemento(J.elemento(V['letture'], J.attributo(V['repeat'], 'item')), 1), 1)))
    return ''.join(_o)


def m0346(c, V):
    # timer.vmc_master_lettura_{{ repeat.item }}
    _o = []
    _o.extend((c.N('timer.vmc_master_lettura_'), J.testo(J.attributo(V['repeat'], 'item'))))
    return ''.join(_o)


def m0347(c, V):
    # {{ as_timestamp(states[letture[repeat.item][0]].last_reported, as_timestamp(now())) if ...
    _o = []
    _o.append(J.testo((J.as_timestamp(J.attributo(J.elemento(c.states, J.elemento(J.elemento(V['letture'], J.attributo(V['repeat'], 'item')), 0)), 'last_reported'), J.as_timestamp(c.now())) if (not J.t_none(J.elemento(c.states, J.elemento(J.elemento(V['letture'], J.attributo(V['repeat'], 'item')), 0)))) else J.as_timestamp(c.now()))))
    return ''.join(_o)


def m0348(c, V):
    # {{ ((as_timestamp(now()) - (ultima | float(0))) % intervallo) | round(3) }}
    _o = []
    _o.append(J.testo(J.f_round(((J.as_timestamp(c.now()) - J.f_float(V['ultima'], 0)) % V['intervallo']), 3)))
    return ''.join(_o)


def m0349(c, V):
    # {{ (intervallo - (trascorsi | float(0))) | round(0, 'ceil') | int if (intervallo - (tra...
    _o = []
    _o.append(J.testo((J.f_int(J.f_round((V['intervallo'] - J.f_float(V['trascorsi'], 0)), 0, 'ceil')) if ((V['intervallo'] - J.f_float(V['trascorsi'], 0)) >= 1) else V['intervallo'])))
    return ''.join(_o)


def m0350(c, V):
    # {{ ((as_timestamp(state_attr(timer_lettura, 'finishes_at'), 0) - (as_timestamp(now()) +...
    _o = []
    _o.append(J.testo((J.f_round(J.f_abs((J.as_timestamp(c.state_attr(V['timer_lettura'], 'finishes_at'), 0) - (J.as_timestamp(c.now()) + J.f_int(V['mancano'], 0)))), 3) if c.is_state(V['timer_lettura'], 'active') else 9999)))
    return ''.join(_o)


def m0351(c, V):
    # {{ intervallo if trigger.id == 'scaduto' else mancano }}
    _o = []
    _o.append(J.testo((V['intervallo'] if (J.attributo(V['trigger'], 'id') == 'scaduto') else V['mancano'])))
    return ''.join(_o)


def m0352(c, V):
    # {{ timer_lettura }}
    _o = []
    _o.append(J.testo(V['timer_lettura']))
    return ''.join(_o)


def m0353(c, V):
    # {{ trigger.id == 'scaduto' or (scarto | float(9999)) > 2 }}
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'scaduto') or (J.f_float(V['scarto'], 9999) > 2))))
    return ''.join(_o)


def m0354(c, V):
    # {{ chiavi }}
    _o = []
    _o.append(J.testo(V['chiavi']))
    return ''.join(_o)


def m0355(c, V):
    # {{ {'ping': ['sensor.vmc_master_status_ip', 10], 'ventilazione': ['sensor.vmc_master_st...
    _o = []
    _o.append(J.testo({'ping': [c.N('sensor.vmc_master_status_ip'), 10], 'ventilazione': [c.N('sensor.vmc_master_status_ventola'), 5], 'ambientali': [c.N('sensor.vmc_master_sensori'), 1227], 'lan': [c.N('sensor.vmc_master_lan'), 57641], 'nome': [c.N('sensor.vmc_master_nome'), 43227]}))
    return ''.join(_o)


def m0356(c, V):
    # {%- set i = trigger.to_state.state.split(',')[1] | int -%} {%- set ns = namespace(l=[])...
    v_i = v_ns = J.MANCANTE
    _o = []
    v_i = J.f_int(J.elemento(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), ','), 1))
    v_ns = J.namespace(l=[])
    for v_t_1, v_loop_1 in J.LoopContext(V['letture'], J.Indefinito):
        J.imposta_ns(J.leggi(v_ns, 'ns'), 'l', (J.attributo(J.leggi(v_ns, 'ns'), 'l') + [J.f_string((V['ora'] if (J.attributo(v_loop_1, 'index0') == J.leggi(v_i, 'i')) else v_t_1))]))
    _o.append(J.testo(J.f_join(J.attributo(J.leggi(v_ns, 'ns'), 'l'), '|')))
    return ''.join(_o)


def m0357(c, V):
    # {%- set da = trigger.from_state.state.split(',') if trigger.id == 'lettura' and trigger...
    v_da = v_a = J.MANCANTE
    _o = []
    v_da = (J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'from_state'), 'state'), 'split'), ',') if ((J.attributo(V['trigger'], 'id') == 'lettura') and (not J.t_none(J.attributo(V['trigger'], 'from_state')))) else [])
    v_a = (J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), ',') if ((J.attributo(V['trigger'], 'id') == 'lettura') and (not J.t_none(J.attributo(V['trigger'], 'to_state')))) else [])
    _o.append(J.testo(((((J.f_length(J.leggi(v_da, 'da')) > 1) and (J.f_length(J.leggi(v_a, 'a')) > 1)) and (J.elemento(J.leggi(v_a, 'a'), 1) != J.elemento(J.leggi(v_da, 'da'), 1))) and (J.elemento(J.leggi(v_a, 'a'), 1) in ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007']))))
    return ''.join(_o)


def m0358(c, V):
    # 0000{{ codici[trigger.event.data.service] }}|{{ ora }}|scheda
    _o = []
    _o.extend(('0000', J.testo(J.elemento(V['codici'], J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'data'), 'service'))), '|', J.testo(V['ora']), '|scheda'))
    return ''.join(_o)


def m0359(c, V):
    # {{ trigger.id == 'comando' and trigger.event.context.user_id is not none }}
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'id') == 'comando') and (not J.t_none(J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'context'), 'user_id'))))))
    return ''.join(_o)


def m0360(c, V):
    # {%- set i = codici[trigger.event.data.service] -%} {%- set ns = namespace(l=[]) -%} {%-...
    v_i = v_ns = J.MANCANTE
    _o = []
    v_i = J.elemento(V['codici'], J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'data'), 'service'))
    v_ns = J.namespace(l=[])
    for v_t_1, v_loop_1 in J.LoopContext(V['comandi'], J.Indefinito):
        J.imposta_ns(J.leggi(v_ns, 'ns'), 'l', (J.attributo(J.leggi(v_ns, 'ns'), 'l') + [J.f_string((V['ora'] if (J.attributo(v_loop_1, 'index0') == J.leggi(v_i, 'i')) else v_t_1))]))
    _o.append(J.testo(J.f_join(J.attributo(J.leggi(v_ns, 'ns'), 'l'), '|')))
    return ''.join(_o)


def m0361(c, V):
    # {{ trigger.id == 'comando' }}
    _o = []
    _o.append(J.testo((J.attributo(V['trigger'], 'id') == 'comando')))
    return ''.join(_o)


def m0362(c, V):
    # {{ trigger.to_state.state.split(',')[1] }}|{{ ora }}|lettura
    _o = []
    _o.extend((J.testo(J.elemento(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), ','), 1)), '|', J.testo(V['ora']), '|lettura'))
    return ''.join(_o)


def m0363(c, V):
    # {%- set da = trigger.from_state.state.split(',') if trigger.id == 'lettura' and trigger...
    v_da = v_a = J.MANCANTE
    _o = []
    v_da = (J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'from_state'), 'state'), 'split'), ',') if ((J.attributo(V['trigger'], 'id') == 'lettura') and (not J.t_none(J.attributo(V['trigger'], 'from_state')))) else [])
    v_a = (J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), ',') if ((J.attributo(V['trigger'], 'id') == 'lettura') and (not J.t_none(J.attributo(V['trigger'], 'to_state')))) else [])
    if ((((J.f_length(J.leggi(v_da, 'da')) > 1) and (J.f_length(J.leggi(v_a, 'a')) > 1)) and (J.elemento(J.leggi(v_a, 'a'), 1) != J.elemento(J.leggi(v_da, 'da'), 1))) and (J.elemento(J.leggi(v_a, 'a'), 1) in ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007'])):
        _o.append(J.testo((((V['ora'] - J.elemento(V['comandi'], J.f_int(J.elemento(J.leggi(v_a, 'a'), 1)))) >= 20) and (not (((J.elemento(V['scelta'], 0) == J.elemento(J.leggi(v_a, 'a'), 1)) and (J.elemento(V['scelta'], 2) == 'scheda')) and ((V['ora'] - J.f_float(J.elemento(V['scelta'], 1), 0)) < 20))))))
    else:
        _o.append('false')
    return ''.join(_o)


def m0364(c, V):
    # {{ {'vmc_master_velocita_0': 0, 'vmc_master_velocita_1': 1, 'vmc_master_velocita_2': 2,...
    _o = []
    _o.append(J.testo({c.N('vmc_master_velocita_0'): 0, c.N('vmc_master_velocita_1'): 1, c.N('vmc_master_velocita_2'): 2, c.N('vmc_master_velocita_3'): 3, c.N('vmc_master_velocita_4'): 4, c.N('vmc_master_iperventilazione'): 5, c.N('vmc_master_notturna'): 6, c.N('vmc_master_freecooling'): 7}))
    return ''.join(_o)


def m0365(c, V):
    # {{ as_timestamp(now()) | round(1) }}
    _o = []
    _o.append(J.testo(J.f_round(J.as_timestamp(c.now()), 1)))
    return ''.join(_o)


def m0366(c, V):
    # {%- set c = states('input_text.vmc_master_ultimi_comandi_automazione').split('|') -%} {...
    v_c = J.MANCANTE
    _o = []
    v_c = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultimi_comandi_automazione')), 'split'), '|')
    _o.append(J.testo(J.f_list(J.f_map((J.leggi(v_c, 'c') if (J.f_length(J.leggi(v_c, 'c')) == 8) else ['0', '0', '0', '0', '0', '0', '0', '0']), 'float', 0))))
    return ''.join(_o)


def m0367(c, V):
    # {{ (states('input_text.vmc_master_ultima_scelta_utente').split('|') + ['', '0', ''])[:3...
    _o = []
    _o.append(J.testo(J.elemento((J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultima_scelta_utente')), 'split'), '|') + ['', '0', '']), slice(None, 3, None))))
    return ''.join(_o)


def m0368(c, V):
    # {%- set r = states('input_text.vmc_master_ultime_letture_velocita').split('|') -%} {{ (...
    v_r = J.MANCANTE
    _o = []
    v_r = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultime_letture_velocita')), 'split'), '|')
    _o.append(J.testo(J.f_list(J.f_map((J.leggi(v_r, 'r') if (J.f_length(J.leggi(v_r, 'r')) == 8) else ['0', '0', '0', '0', '0', '0', '0', '0']), 'float', 0))))
    return ''.join(_o)


def m0369(c, V):
    # {{ in_viaggio | length > 0 }}
    _o = []
    _o.append(J.testo((J.f_length(V['in_viaggio']) > 0)))
    return ''.join(_o)


def m0370(c, V):
    # {%- set c = states('input_text.vmc_master_ultimi_comandi_automazione').split('|') -%} {...
    v_c = v_ns = J.MANCANTE
    _o = []
    v_c = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultimi_comandi_automazione')), 'split'), '|')
    v_ns = J.namespace(ultimo=0, nuovo=False)
    for v_t_1, v_loop_1 in J.LoopContext((J.leggi(v_c, 'c') if (J.f_length(J.leggi(v_c, 'c')) == 8) else []), J.Indefinito):
        if (J.attributo(v_loop_1, 'index0') in V['in_viaggio']):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'ultimo', J.f_max([J.attributo(J.leggi(v_ns, 'ns'), 'ultimo'), J.f_float(v_t_1, 0)]))
        elif ((J.attributo(v_loop_1, 'index0') != V['indice']) and (J.f_float(v_t_1, 0) > V['ts_scelta'])):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'nuovo', True)
    _o.append(J.testo(((J.attributo(J.leggi(v_ns, 'ns'), 'nuovo') or ((J.as_timestamp(c.now()) - J.attributo(J.leggi(v_ns, 'ns'), 'ultimo')) >= 8)) or (J.attributo(V['repeat'], 'index') >= 30))))
    return ''.join(_o)


def m0371(c, V):
    # {%- set c = states('input_text.vmc_master_ultimi_comandi_automazione').split('|') -%} {...
    v_c = v_ns = J.MANCANTE
    _o = []
    v_c = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultimi_comandi_automazione')), 'split'), '|')
    v_ns = J.namespace(ultimo=0, nuovo=False)
    for v_t_1, v_loop_1 in J.LoopContext((J.leggi(v_c, 'c') if (J.f_length(J.leggi(v_c, 'c')) == 8) else []), J.Indefinito):
        if (J.attributo(v_loop_1, 'index0') in V['in_viaggio']):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'ultimo', J.f_max([J.attributo(J.leggi(v_ns, 'ns'), 'ultimo'), J.f_float(v_t_1, 0)]))
        elif ((J.attributo(v_loop_1, 'index0') != V['indice']) and (J.f_float(v_t_1, 0) > V['ts_scelta'])):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'nuovo', True)
    _o.append(J.testo(((not J.attributo(J.leggi(v_ns, 'ns'), 'nuovo')) and ((J.as_timestamp(c.now()) - J.attributo(J.leggi(v_ns, 'ns'), 'ultimo')) >= 8))))
    return ''.join(_o)


def m0372(c, V):
    # {{ states('sensor.vmc_master_status_ventola') in ['unavailable', 'unknown', ''] or stat...
    _o = []
    _o.append(J.testo(((c.states(c.N('sensor.vmc_master_status_ventola')) in ['unavailable', 'unknown', '']) or (c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')) == c.states(c.N('sensor.vmc_master_status_ventola'))))))
    return ''.join(_o)


def m0373(c, V):
    # {%- set letta = (states('sensor.vmc_master_status_ventola').split(',') + ['', ''])[1] -...
    v_letta = J.MANCANTE
    _o = []
    v_letta = J.elemento((J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola')), 'split'), ',') + ['', '']), 1)
    _o.append(J.testo((((((J.leggi(v_letta, 'letta') in ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007']) and (J.f_int(J.leggi(v_letta, 'letta')) in V['in_viaggio'])) and c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line')) and c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'off')) and (c.states(c.N('input_text.vmc_master_ultima_scelta_utente')) == J.attributo(J.attributo(V['trigger'], 'to_state'), 'state')))))
    return ''.join(_o)


def m0374(c, V):
    # {{ servizi[indice] }}
    _o = []
    _o.append(J.testo(J.elemento(V['servizi'], V['indice'])))
    return ''.join(_o)


def m0375(c, V):
    # {%- set c = states('input_text.vmc_master_ultimi_comandi_automazione').split('|') -%} {...
    v_c = v_ns = J.MANCANTE
    _o = []
    v_c = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultimi_comandi_automazione')), 'split'), '|')
    v_ns = J.namespace(nuovo=False)
    for v_t_1, v_loop_1 in J.LoopContext((J.leggi(v_c, 'c') if (J.f_length(J.leggi(v_c, 'c')) == 8) else []), J.Indefinito):
        if ((J.attributo(v_loop_1, 'index0') != V['indice']) and (J.f_float(v_t_1, 0) > V['inizio'])):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'nuovo', True)
    _o.append(J.testo((((((J.elemento((J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola')), 'split'), ',') + ['', '']), 1) == V['codice']) or c.is_state(c.N('binary_sensor.vmc_master_black_out_rilevato'), 'on')) or (not c.is_state(c.N('sensor.vmc_master_status_ip_interfaccia'), 'ON-Line'))) or J.attributo(J.leggi(v_ns, 'ns'), 'nuovo')) or (J.attributo(V['repeat'], 'index') >= 5))))
    return ''.join(_o)


def m0376(c, V):
    # {{ trigger.to_state is not none and trigger.to_state.state.split('|') | length == 3 and...
    _o = []
    _o.append(J.testo((((not J.t_none(J.attributo(V['trigger'], 'to_state'))) and (J.f_length(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), '|')) == 3)) and (J.elemento(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), '|'), 0) in ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007']))))
    return ''.join(_o)


def m0377(c, V):
    # {{ ['shell_command.vmc_master_velocita_0', 'shell_command.vmc_master_velocita_1', 'shel...
    _o = []
    _o.append(J.testo([c.N('shell_command.vmc_master_velocita_0'), c.N('shell_command.vmc_master_velocita_1'), c.N('shell_command.vmc_master_velocita_2'), c.N('shell_command.vmc_master_velocita_3'), c.N('shell_command.vmc_master_velocita_4'), c.N('shell_command.vmc_master_iperventilazione'), c.N('shell_command.vmc_master_notturna'), c.N('shell_command.vmc_master_freecooling')]))
    return ''.join(_o)


def m0378(c, V):
    # {{ trigger.to_state.state.split('|')[0] }}
    _o = []
    _o.append(J.testo(J.elemento(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), '|'), 0)))
    return ''.join(_o)


def m0379(c, V):
    # {{ codice | int }}
    _o = []
    _o.append(J.testo(J.f_int(V['codice'])))
    return ''.join(_o)


def m0380(c, V):
    # {{ trigger.to_state.state.split('|')[1] | float(0) }}
    _o = []
    _o.append(J.testo(J.f_float(J.elemento(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), '|'), 1), 0)))
    return ''.join(_o)


def m0381(c, V):
    # {%- set c = states('input_text.vmc_master_ultimi_comandi_automazione').split('|') -%} {...
    v_c = v_finestra = v_ns = J.MANCANTE
    _o = []
    v_c = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultimi_comandi_automazione')), 'split'), '|')
    v_finestra = (8 if (J.elemento(J.chiama(J.attributo(J.attributo(J.attributo(V['trigger'], 'to_state'), 'state'), 'split'), '|'), 2) == 'scheda') else 13)
    v_ns = J.namespace(l=[])
    for v_t_1, v_loop_1 in J.LoopContext((J.leggi(v_c, 'c') if (J.f_length(J.leggi(v_c, 'c')) == 8) else []), J.Indefinito):
        if ((J.attributo(v_loop_1, 'index0') != V['indice']) and ((V['ts_scelta'] - J.leggi(v_finestra, 'finestra')) <= J.f_float(v_t_1, 0) <= V['ts_scelta'])):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'l', (J.attributo(J.leggi(v_ns, 'ns'), 'l') + [J.attributo(v_loop_1, 'index0')]))
    _o.append(J.testo(J.attributo(J.leggi(v_ns, 'ns'), 'l')))
    return ''.join(_o)


def m0382(c, V):
    # {{ repeat.index <= 7 and states('sensor.vmc_master_status_ip_interfaccia') == 'ON-Line' }}
    _o = []
    _o.append(J.testo(((J.attributo(V['repeat'], 'index') <= 7) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line'))))
    return ''.join(_o)


def m0383(c, V):
    # {{ trigger.event.context.user_id is none and states('sensor.vmc_master_status_ip_interf...
    _o = []
    _o.append(J.testo((J.t_none(J.attributo(J.attributo(J.attributo(V['trigger'], 'event'), 'context'), 'user_id')) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line'))))
    return ''.join(_o)


def m0384(c, V):
    # {{ states('input_boolean.vmc_master_spia_calendario_lunedi_1') == 'on' or states('input...
    _o = []
    _o.append(J.testo(((((((((((((((c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_1')) == 'on') or (c.states(c.N('input_boolean.vmc_master_spia_calendario_lunedi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_martedi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_giovedi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_venerdi_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_sabato_2')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_1')) == 'on')) or (c.states(c.N('input_boolean.vmc_master_spia_calendario_domenica_2')) == 'on'))))
    return ''.join(_o)


def m0385(c, V):
    # {{ {0: 'input_boolean.vmc_master_spia_velocita_0', 2: 'input_boolean.vmc_master_spia_ve...
    _o = []
    _o.append(J.testo(J.elemento({0: c.N('input_boolean.vmc_master_spia_velocita_0'), 2: c.N('input_boolean.vmc_master_spia_velocita_2'), 3: c.N('input_boolean.vmc_master_spia_velocita_3'), 4: c.N('input_boolean.vmc_master_spia_velocita_4'), 5: c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), 6: c.N('input_boolean.vmc_master_spia_velocita_notturna'), 7: c.N('input_boolean.vmc_master_spia_velocita_freecooling')}, V['codice_prima'])))
    return ''.join(_o)


def m0386(c, V):
    # {{ codice_prima in [0, 2, 3, 4, 5, 6, 7] }}
    _o = []
    _o.append(J.testo((V['codice_prima'] in [0, 2, 3, 4, 5, 6, 7])))
    return ''.join(_o)


def m0387(c, V):
    # {%- set m = states.sensor.vmc_master_status_ventola_memorizzata -%} {{ codice_letto == ...
    v_m = J.MANCANTE
    _o = []
    v_m = c.oggetto(c.N('sensor.vmc_master_status_ventola_memorizzata'))
    _o.append(J.testo(((((V['codice_letto'] == 1) and (J.f_length(V['prima']) == 2)) and (not J.t_none(J.leggi(v_m, 'm')))) and ((J.as_timestamp(c.now()) - J.as_timestamp(J.attributo(J.leggi(v_m, 'm'), 'last_changed'))) < J.f_int(c.states(c.N('input_number.vmc_master_attesa_blackout_ripristino')), 32)))))
    return ''.join(_o)


def m0388(c, V):
    # {%- set ns = namespace(comando=false) -%} {%- for t in comandi -%}{%- if loop.index0 !=...
    v_ns = J.MANCANTE
    _o = []
    v_ns = J.namespace(comando=False)
    for v_t_1, v_loop_1 in J.LoopContext(V['comandi'], J.Indefinito):
        if ((J.attributo(v_loop_1, 'index0') != V['codice_prima']) and (v_t_1 > V['prima_dalle'])):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'comando', True)
    _o.append(J.testo(((not J.attributo(J.leggi(v_ns, 'ns'), 'comando')) and (not (((J.elemento(V['scelta'], 2) == 'scheda') and (J.f_int(J.elemento(V['scelta'], 0), (-1)) != V['codice_prima'])) and (J.f_float(J.elemento(V['scelta'], 1), 0) > V['prima_dalle']))))))
    return ''.join(_o)


def m0389(c, V):
    # {{ states('binary_sensor.vmc_master_black_out_rilevato') != 'on' and states('input_bool...
    _o = []
    _o.append(J.testo(((((((((((c.states(c.N('binary_sensor.vmc_master_black_out_rilevato')) != 'on') and (c.states(c.N('input_boolean.vmc_master_spia_velocita_0')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_1')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_2')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_3')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_4')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_notturna')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_velocita_freecooling')) == 'off')) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_black_out')) == 'off'))))
    return ''.join(_o)


def m0390(c, V):
    # {{ states('input_text.vmc_master_comando_non_eseguito') in ['', 'unknown', 'unavailable...
    _o = []
    _o.append(J.testo(((c.states(c.N('input_text.vmc_master_comando_non_eseguito')) in ['', 'unknown', 'unavailable']) and (c.states(c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')) != 'on'))))
    return ''.join(_o)


def m0391(c, V):
    # {{ (states('sensor.vmc_master_status_ventola_memorizzata').split(',') + ['', ''])[1] | ...
    _o = []
    _o.append(J.testo(J.f_int(J.elemento((J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola_memorizzata')), 'split'), ',') + ['', '']), 1), (-1))))
    return ''.join(_o)


def m0392(c, V):
    # {{ ((state_attr('sensor.vmc_master_status_ventola_memorizzata', 'lettura_prima_dell_int...
    _o = []
    _o.append(J.testo(J.chiama(J.attributo(J.f_string((c.state_attr(c.N('sensor.vmc_master_status_ventola_memorizzata'), 'lettura_prima_dell_interruzione') or '')), 'split'), '|')))
    return ''.join(_o)


def m0393(c, V):
    # {{ prima[0] | int(-1) if prima | length == 2 and prima[0] in ['00000', '00001', '00002'...
    _o = []
    _o.append(J.testo((J.f_int(J.elemento(V['prima'], 0), (-1)) if ((J.f_length(V['prima']) == 2) and (J.elemento(V['prima'], 0) in ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007'])) else (-1))))
    return ''.join(_o)


def m0394(c, V):
    # {{ prima[1] | float(0) if prima | length == 2 else 0 }}
    _o = []
    _o.append(J.testo((J.f_float(J.elemento(V['prima'], 1), 0) if (J.f_length(V['prima']) == 2) else 0)))
    return ''.join(_o)


def m0395(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra',...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0396(c, V):
    # {{ trigger.to_state is not none and is_state(trigger.entity_id, trigger.to_state.state) }}
    _o = []
    _o.append(J.testo(((not J.t_none(J.attributo(V['trigger'], 'to_state'))) and c.is_state(J.attributo(V['trigger'], 'entity_id'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'state')))))
    return ''.join(_o)


def m0397(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzione_finestra_prossime_letture', ]) | selectat...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('input_boolean.vmc_master_opzione_finestra_prossime_letture')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0398(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzioni_calendario_main', 'input_boolean.vmc_mast...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('input_boolean.vmc_master_opzioni_calendario_main'), c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('input_boolean.vmc_master_opzioni_calendario'), c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada'), c.N('input_boolean.vmc_master_opzioni_scelta_sensori'), c.N('input_boolean.vmc_master_opzioni_elementi_chimici'), c.N('input_boolean.vmc_master_opzione_finestra_audio'), c.N('input_boolean.vmc_master_conferma_pulizia_cronologia')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0399(c, V):
    # {{ expand([ 'input_boolean.vmc_master_opzione_finestra_tempi_attesa', ]) | selectattr('...
    _o = []
    _o.append(J.testo(J.f_list(J.f_map(J.f_selectattr(J.f_selectattr(c.expand([c.N('input_boolean.vmc_master_opzione_finestra_tempi_attesa')]), 'state', c.test('eq'), 'on'), 'last_changed', c.test('le'), J.attributo(J.attributo(V['trigger'], 'to_state'), 'last_changed')), attribute='entity_id'))))
    return ''.join(_o)


def m0400(c, V):
    # {{ trigger.platform == 'homeassistant' or is_state('input_boolean.vmc_master_attese_ini...
    _o = []
    _o.append(J.testo(((J.attributo(V['trigger'], 'platform') == 'homeassistant') or c.is_state(c.N('input_boolean.vmc_master_attese_inizializzate'), 'off'))))
    return ''.join(_o)


def m0401(c, V):
    # {%- set scelta = (states('input_text.vmc_master_ultima_scelta_utente').split('|') + [''...
    v_scelta = v_c = v_r = v_ns = v_letta = J.MANCANTE
    _o = []
    v_scelta = J.elemento((J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultima_scelta_utente')), 'split'), '|') + ['', '0', '']), slice(None, 3, None))
    v_c = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultimi_comandi_automazione')), 'split'), '|')
    v_c = J.f_list(J.f_map((J.leggi(v_c, 'c') if (J.f_length(J.leggi(v_c, 'c')) == 8) else ['0', '0', '0', '0', '0', '0', '0', '0']), 'float', 0))
    v_r = J.chiama(J.attributo(c.states(c.N('input_text.vmc_master_ultime_letture_velocita')), 'split'), '|')
    v_r = J.f_list(J.f_map((J.leggi(v_r, 'r') if (J.f_length(J.leggi(v_r, 'r')) == 8) else ['0', '0', '0', '0', '0', '0', '0', '0']), 'float', 0))
    v_ns = J.namespace(i=(-1), ts=0)
    for v_t_1, v_loop_1 in J.LoopContext(J.leggi(v_c, 'c'), J.Indefinito):
        if (v_t_1 > J.attributo(J.leggi(v_ns, 'ns'), 'ts')):
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'i', J.attributo(v_loop_1, 'index0'))
            J.imposta_ns(J.leggi(v_ns, 'ns'), 'ts', v_t_1)
    if (((J.elemento(J.leggi(v_scelta, 'scelta'), 2) == 'scheda') and (J.elemento(J.leggi(v_scelta, 'scelta'), 0) in ['00000', '00001', '00002', '00003', '00004', '00005', '00006', '00007'])) and (J.f_float(J.elemento(J.leggi(v_scelta, 'scelta'), 1), 0) > J.attributo(J.leggi(v_ns, 'ns'), 'ts'))):
        J.imposta_ns(J.leggi(v_ns, 'ns'), 'i', J.f_int(J.elemento(J.leggi(v_scelta, 'scelta'), 0)))
        J.imposta_ns(J.leggi(v_ns, 'ns'), 'ts', J.f_float(J.elemento(J.leggi(v_scelta, 'scelta'), 1), 0))
    v_letta = J.elemento((J.chiama(J.attributo(c.states(c.N('sensor.vmc_master_status_ventola')), 'split'), ',') + ['', '']), 1)
    _o.append(J.testo(((((((J.attributo(V['repeat'], 'index') <= 6) and (J.attributo(J.leggi(v_ns, 'ns'), 'i') >= 0)) and (J.concat('0000', J.attributo(J.leggi(v_ns, 'ns'), 'i')) != J.leggi(v_letta, 'letta'))) and (J.elemento(J.leggi(v_r, 'r'), J.attributo(J.leggi(v_ns, 'ns'), 'i')) < J.attributo(J.leggi(v_ns, 'ns'), 'ts'))) and ((J.as_timestamp(c.now()) - J.attributo(J.leggi(v_ns, 'ns'), 'ts')) < 12)) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line'))))
    return ''.join(_o)


def m0402(c, V):
    # {{ trigger.platform == 'template' and trigger.for is not none and states('sensor.vmc_ma...
    _o = []
    _o.append(J.testo(((((J.attributo(V['trigger'], 'platform') == 'template') and (not J.t_none(J.attributo(V['trigger'], 'for')))) and (c.states(c.N('sensor.vmc_master_status_ip_interfaccia')) == 'ON-Line')) and (c.states(c.N('sensor.vmc_master_status_ventola')) not in ['unavailable', 'unknown', '']))))
    return ''.join(_o)
