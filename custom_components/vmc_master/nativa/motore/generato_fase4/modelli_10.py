"""Modelli Jinja del package, tradotti in Python (parte 10 di 10).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from .. import jinja as J


def m1163(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_weekday = V.get('weekday', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('        \n  ')
        v_weekday = J.chiama(J.attributo(c.now(), 'weekday'))
        _o.append('\n  ')
        if ((((((((((((J.leggi(v_weekday, 'weekday') == 0) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) > c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Lunedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_lunedi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 1) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) > c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Martedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_martedi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 2) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) > c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Mercoledi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_mercoledi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 3) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) > c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Giovedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_giovedi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 4) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) > c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Venerdi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_venerdi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 5) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) > c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Sabato, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_sabato')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 6) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) > c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Domenica, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_domenica')), slice(0, 5, None))), '\n    '))
        else:
            _o.append('\n      Disabilitata\n    ')
        _o.append('\n')
    return ''.join(_o)


def m1164(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_weekday = V.get('weekday', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('        \n  ')
        v_weekday = J.chiama(J.attributo(c.now(), 'weekday'))
        _o.append('\n  ')
        if ((((((((((((J.leggi(v_weekday, 'weekday') == 0) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) > c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Lunedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_lunedi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 1) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) > c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Martedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_martedi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 2) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) > c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Mercoledi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_mercoledi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 3) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) > c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Giovedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_giovedi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 4) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) > c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Venerdi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_venerdi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 5) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) > c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Sabato, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_sabato_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 6) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) > c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Domenica, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_accensione_domenica_2')), slice(0, 5, None))), '\n    '))
        else:
            _o.append('\n      Disabilitata\n    ')
        _o.append('\n')
    return ''.join(_o)


def m1165(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_weekday = V.get('weekday', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('        \n  ')
        v_weekday = J.chiama(J.attributo(c.now(), 'weekday'))
        _o.append('\n  ')
        if ((((((((((((J.leggi(v_weekday, 'weekday') == 0) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) > c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Lunedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_lunedi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 1) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) > c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Martedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_martedi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 2) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) > c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Mercoledi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_mercoledi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 3) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) > c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Giovedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_giovedi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 4) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) > c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Venerdi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_venerdi')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 5) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) > c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Sabato, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_sabato')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 6) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) > c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Domenica, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_domenica')), slice(0, 5, None))), '\n    '))
        else:
            _o.append('\n      Disabilitata\n    ')
        _o.append('\n')
    return ''.join(_o)


def m1166(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_weekday = V.get('weekday', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('        \n  ')
        v_weekday = J.chiama(J.attributo(c.now(), 'weekday'))
        _o.append('\n  ')
        if ((((((((((((J.leggi(v_weekday, 'weekday') == 0) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) > c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Lunedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_lunedi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 1) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) > c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Martedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_martedi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 2) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) > c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Mercoledi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 3) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) > c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Giovedi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_giovedi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 4) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) > c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Venerdi, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_venerdi_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 5) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) > c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Sabato, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_sabato_2')), slice(0, 5, None))), '\n  '))
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 6) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) > c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.extend(('\n    Domenica, ', J.testo(J.elemento(c.states(c.N('time.vmc_master_spegnimento_domenica_2')), slice(0, 5, None))), '\n    '))
        else:
            _o.append('\n      Disabilitata\n    ')
        _o.append('\n')
    return ''.join(_o)


def m1167(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_weekday = V.get('weekday', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('        \n  ')
        v_weekday = J.chiama(J.attributo(c.now(), 'weekday'))
        _o.append('\n  ')
        if ((((((((((((J.leggi(v_weekday, 'weekday') == 0) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) < c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) < c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_spegnimento_lunedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_lunedi')) != c.states(c.N('time.vmc_master_accensione_lunedi_2')))) and (c.states(c.N('time.vmc_master_accensione_lunedi_2')) > c.states(c.N('time.vmc_master_spegnimento_lunedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Lunedi\n  ')
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 1) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) < c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) < c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_spegnimento_martedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_martedi')) != c.states(c.N('time.vmc_master_accensione_martedi_2')))) and (c.states(c.N('time.vmc_master_accensione_martedi_2')) > c.states(c.N('time.vmc_master_spegnimento_martedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Martedi\n  ')
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 2) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) < c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) < c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_spegnimento_mercoledi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_mercoledi')) != c.states(c.N('time.vmc_master_accensione_mercoledi_2')))) and (c.states(c.N('time.vmc_master_accensione_mercoledi_2')) > c.states(c.N('time.vmc_master_spegnimento_mercoledi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Mercoledi\n  ')
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 3) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) < c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) < c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_spegnimento_giovedi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_giovedi')) != c.states(c.N('time.vmc_master_accensione_giovedi_2')))) and (c.states(c.N('time.vmc_master_accensione_giovedi_2')) > c.states(c.N('time.vmc_master_spegnimento_giovedi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Giovedi\n  ')
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 4) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) < c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) < c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_spegnimento_venerdi_2')))) and (c.states(c.N('time.vmc_master_spegnimento_venerdi')) != c.states(c.N('time.vmc_master_accensione_venerdi_2')))) and (c.states(c.N('time.vmc_master_accensione_venerdi_2')) > c.states(c.N('time.vmc_master_spegnimento_venerdi')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Venerdi\n  ')
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 5) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) < c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) < c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_spegnimento_sabato_2')))) and (c.states(c.N('time.vmc_master_spegnimento_sabato')) != c.states(c.N('time.vmc_master_accensione_sabato_2')))) and (c.states(c.N('time.vmc_master_accensione_sabato_2')) > c.states(c.N('time.vmc_master_spegnimento_sabato')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Sabato\n  ')
        elif ((((((((((((J.leggi(v_weekday, 'weekday') == 6) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) < c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) < c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_spegnimento_domenica_2')))) and (c.states(c.N('time.vmc_master_spegnimento_domenica')) != c.states(c.N('time.vmc_master_accensione_domenica_2')))) and (c.states(c.N('time.vmc_master_accensione_domenica_2')) > c.states(c.N('time.vmc_master_spegnimento_domenica')))) and (c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')) == 'on')):
            _o.append('\n    Domenica\n    ')
        else:
            _o.append('\n      Disabilitata\n    ')
        _o.append('\n')
    return ''.join(_o)


def m1168(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_input1 = V.get('input1', J.MANCANTE)
    v_input2 = V.get('input2', J.MANCANTE)
    v_input3 = V.get('input3', J.MANCANTE)
    v_input4 = V.get('input4', J.MANCANTE)
    v_month_numbers = V.get('month_numbers', J.MANCANTE)
    v_month_number1 = V.get('month_number1', J.MANCANTE)
    v_month_number2 = V.get('month_number2', J.MANCANTE)
    v_month_number3 = V.get('month_number3', J.MANCANTE)
    v_month_number4 = V.get('month_number4', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_input1 = c.states(c.N('sensor.vmc_master_mese_1_fascia_freeheating'))
        _o.append('\n  ')
        v_input2 = c.states(c.N('sensor.vmc_master_mese_2_fascia_freeheating'))
        _o.append('\n  ')
        v_input3 = c.states(c.N('sensor.vmc_master_mese_1_fascia_freecooling'))
        _o.append('\n  ')
        v_input4 = c.states(c.N('sensor.vmc_master_mese_2_fascia_freecooling'))
        _o.append('\n  ')
        if ((((J.leggi(v_input1, 'input1') in J.leggi(v_stati, 'stati')) or (J.leggi(v_input2, 'input2') in J.leggi(v_stati, 'stati'))) or (J.leggi(v_input3, 'input3') in J.leggi(v_stati, 'stati'))) or (J.leggi(v_input4, 'input4') in J.leggi(v_stati, 'stati'))):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.append('      \n    ')
            if (J.leggi(v_input1, 'input1') == 'Gennaio'):
                _o.append('\n      ')
                v_month_numbers = {'Gennaio': 1, 'Febbraio': 2, 'Marzo': 3, 'Aprile': 4, 'Maggio': 5, 'Giugno': 6, 'Luglio': 7, 'Agosto': 8, 'Settembre': 9, 'Ottobre': 10, 'Novembre': 11, 'Dicembre': 12}
                _o.append('\n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Febbraio'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 12, 'Febbraio': 1, 'Marzo': 2, 'Aprile': 3, 'Maggio': 4, 'Giugno': 5, 'Luglio': 6, 'Agosto': 7, 'Settembre': 8, 'Ottobre': 9, 'Novembre': 10, 'Dicembre': 11}
                _o.append(' \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Marzo'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 11, 'Febbraio': 12, 'Marzo': 1, 'Aprile': 2, 'Maggio': 3, 'Giugno': 4, 'Luglio': 5, 'Agosto': 6, 'Settembre': 7, 'Ottobre': 8, 'Novembre': 9, 'Dicembre': 10}
                _o.append('   \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Aprile'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 10, 'Febbraio': 11, 'Marzo': 12, 'Aprile': 1, 'Maggio': 2, 'Giugno': 3, 'Luglio': 4, 'Agosto': 5, 'Settembre': 6, 'Ottobre': 7, 'Novembre': 8, 'Dicembre': 9}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Maggio'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 9, 'Febbraio': 10, 'Marzo': 11, 'Aprile': 12, 'Maggio': 1, 'Giugno': 2, 'Luglio': 3, 'Agosto': 4, 'Settembre': 5, 'Ottobre': 6, 'Novembre': 7, 'Dicembre': 8}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Giugno'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 8, 'Febbraio': 9, 'Marzo': 10, 'Aprile': 11, 'Maggio': 12, 'Giugno': 1, 'Luglio': 2, 'Agosto': 3, 'Settembre': 4, 'Ottobre': 5, 'Novembre': 6, 'Dicembre': 7}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Luglio'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 7, 'Febbraio': 8, 'Marzo': 9, 'Aprile': 10, 'Maggio': 11, 'Giugno': 12, 'Luglio': 1, 'Agosto': 2, 'Settembre': 3, 'Ottobre': 4, 'Novembre': 5, 'Dicembre': 6}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Agosto'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 6, 'Febbraio': 7, 'Marzo': 8, 'Aprile': 9, 'Maggio': 10, 'Giugno': 11, 'Luglio': 12, 'Agosto': 1, 'Settembre': 2, 'Ottobre': 3, 'Novembre': 4, 'Dicembre': 5}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Settembre'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 5, 'Febbraio': 6, 'Marzo': 7, 'Aprile': 8, 'Maggio': 9, 'Giugno': 10, 'Luglio': 11, 'Agosto': 12, 'Settembre': 1, 'Ottobre': 2, 'Novembre': 3, 'Dicembre': 4}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Ottobre'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 4, 'Febbraio': 5, 'Marzo': 6, 'Aprile': 7, 'Maggio': 8, 'Giugno': 9, 'Luglio': 10, 'Agosto': 11, 'Settembre': 12, 'Ottobre': 1, 'Novembre': 2, 'Dicembre': 3}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Novembre'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 3, 'Febbraio': 4, 'Marzo': 5, 'Aprile': 6, 'Maggio': 7, 'Giugno': 8, 'Luglio': 9, 'Agosto': 10, 'Settembre': 11, 'Ottobre': 12, 'Novembre': 1, 'Dicembre': 2}
                _o.append('  \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            elif (J.leggi(v_input1, 'input1') == 'Dicembre'):
                _o.append('   \n      ')
                v_month_numbers = {'Gennaio': 2, 'Febbraio': 3, 'Marzo': 4, 'Aprile': 5, 'Maggio': 6, 'Giugno': 7, 'Luglio': 8, 'Agosto': 9, 'Settembre': 10, 'Ottobre': 11, 'Novembre': 12, 'Dicembre': 1}
                _o.append(' \n      ')
                v_month_number1 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input1, 'input1')), 0)
                _o.append('\n      ')
                v_month_number2 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input2, 'input2')), 0)
                _o.append('\n      ')
                v_month_number3 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input3, 'input3')), 0)
                _o.append('\n      ')
                v_month_number4 = J.f_int(J.chiama(J.attributo(J.leggi(v_month_numbers, 'month_numbers'), 'get'), J.leggi(v_input4, 'input4')), 0)
                _o.append('\n    ')
            _o.append('\n    ')
            if ((((((J.leggi(v_month_number1, 'month_number1') != J.leggi(v_month_number2, 'month_number2')) and (J.leggi(v_month_number2, 'month_number2') != J.leggi(v_month_number3, 'month_number3'))) and (J.leggi(v_month_number3, 'month_number3') != J.leggi(v_month_number4, 'month_number4'))) and (J.leggi(v_month_number1, 'month_number1') < J.leggi(v_month_number2, 'month_number2'))) and (J.leggi(v_month_number2, 'month_number2') < J.leggi(v_month_number3, 'month_number3'))) and (J.leggi(v_month_number3, 'month_number3') < J.leggi(v_month_number4, 'month_number4'))):
                _o.append('\n      OK\n    ')
            else:
                _o.append('\n      NOT OK\n    ')
            _o.append('\n  ')
        _o.append('\n')
    return ''.join(_o)


def m1169(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_input1_freeheating = V.get('input1_freeheating', J.MANCANTE)
    v_input2_freeheating = V.get('input2_freeheating', J.MANCANTE)
    v_check = V.get('check', J.MANCANTE)
    v_mese_corrente = V.get('mese_corrente', J.MANCANTE)
    v_months_freeheating = V.get('months_freeheating', J.MANCANTE)
    v_interval_1_freeheating = V.get('interval_1_freeheating', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_input1_freeheating = c.states(c.N('sensor.vmc_master_mese_1_fascia_freeheating'))
        _o.append('\n  ')
        v_input2_freeheating = c.states(c.N('sensor.vmc_master_mese_2_fascia_freeheating'))
        _o.append('\n  ')
        v_check = c.states(c.N('sensor.vmc_master_status_check_freeheating_freecooling'))
        _o.append('\n  ')
        v_mese_corrente = J.elemento(['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'], (J.attributo(c.now(), 'month') - 1))
        _o.append('\n  ')
        if (((J.leggi(v_input1_freeheating, 'input1_freeheating') in J.leggi(v_stati, 'stati')) or (J.leggi(v_input2_freeheating, 'input2_freeheating') in J.leggi(v_stati, 'stati'))) or (J.leggi(v_check, 'check') in J.leggi(v_stati, 'stati'))):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.append('      \n    ')
            if (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Gennaio'):
                _o.append('\n      ')
                v_months_freeheating = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Febbraio'):
                _o.append('\n      ')
                v_months_freeheating = ['Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Marzo'):
                _o.append('\n      ')
                v_months_freeheating = ['Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Aprile'):
                _o.append('\n      ')
                v_months_freeheating = ['Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Maggio'):
                _o.append('\n      ')
                v_months_freeheating = ['Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Giugno'):
                _o.append('\n      ')
                v_months_freeheating = ['Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Luglio'):
                _o.append('\n      ')
                v_months_freeheating = ['Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Agosto'):
                _o.append('\n      ')
                v_months_freeheating = ['Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Settembre'):
                _o.append('\n      ')
                v_months_freeheating = ['Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Ottobre'):
                _o.append('\n      ')
                v_months_freeheating = ['Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Novembre'):
                _o.append('\n      ')
                v_months_freeheating = ['Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freeheating, 'input1_freeheating') == 'Dicembre'):
                _o.append('\n      ')
                v_months_freeheating = ['Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre']
                _o.append('\n      ')
                v_interval_1_freeheating = J.elemento(J.leggi(v_months_freeheating, 'months_freeheating'), slice(J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input1_freeheating, 'input1_freeheating')), (J.chiama(J.attributo(J.leggi(v_months_freeheating, 'months_freeheating'), 'index'), J.leggi(v_input2_freeheating, 'input2_freeheating')) + 1), None))
                _o.append('\n    ')
            _o.append('\n    ')
            if (J.leggi(v_check, 'check') == 'OK'):
                _o.append('\n      ')
                if (J.leggi(v_mese_corrente, 'mese_corrente') in J.leggi(v_interval_1_freeheating, 'interval_1_freeheating')):
                    _o.append('\n        OK\n      ')
                else:
                    _o.append('\n        -\n      ')
                _o.append('\n    ')
            else:
                _o.append('\n      NOT OK\n    ')
            _o.append('\n  ')
        _o.append('      \n')
    return ''.join(_o)


def m1170(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_input1_freecooling = V.get('input1_freecooling', J.MANCANTE)
    v_input2_freecooling = V.get('input2_freecooling', J.MANCANTE)
    v_check = V.get('check', J.MANCANTE)
    v_mese_corrente = V.get('mese_corrente', J.MANCANTE)
    v_months_freecooling = V.get('months_freecooling', J.MANCANTE)
    v_interval_1_freecooling = V.get('interval_1_freecooling', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_input1_freecooling = c.states(c.N('sensor.vmc_master_mese_1_fascia_freecooling'))
        _o.append('\n  ')
        v_input2_freecooling = c.states(c.N('sensor.vmc_master_mese_2_fascia_freecooling'))
        _o.append('\n  ')
        v_check = c.states(c.N('sensor.vmc_master_status_check_freeheating_freecooling'))
        _o.append('\n  ')
        v_mese_corrente = J.elemento(['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'], (J.attributo(c.now(), 'month') - 1))
        _o.append('\n  ')
        if (((J.leggi(v_input1_freecooling, 'input1_freecooling') in J.leggi(v_stati, 'stati')) or (J.leggi(v_input2_freecooling, 'input2_freecooling') in J.leggi(v_stati, 'stati'))) or (J.leggi(v_check, 'check') in J.leggi(v_stati, 'stati'))):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.append('      \n    ')
            if (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Gennaio'):
                _o.append('\n      ')
                v_months_freecooling = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Febbraio'):
                _o.append('\n      ')
                v_months_freecooling = ['Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Marzo'):
                _o.append('\n      ')
                v_months_freecooling = ['Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Aprile'):
                _o.append('\n      ')
                v_months_freecooling = ['Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Maggio'):
                _o.append('\n      ')
                v_months_freecooling = ['Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Giugno'):
                _o.append('\n      ')
                v_months_freecooling = ['Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Luglio'):
                _o.append('\n      ')
                v_months_freecooling = ['Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Agosto'):
                _o.append('\n      ')
                v_months_freecooling = ['Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Settembre'):
                _o.append('\n      ')
                v_months_freecooling = ['Settembre', 'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Ottobre'):
                _o.append('\n      ')
                v_months_freecooling = ['Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Novembre'):
                _o.append('\n      ')
                v_months_freecooling = ['Novembre', 'Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            elif (J.leggi(v_input1_freecooling, 'input1_freecooling') == 'Dicembre'):
                _o.append('\n      ')
                v_months_freecooling = ['Dicembre', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre']
                _o.append('\n      ')
                v_interval_1_freecooling = J.elemento(J.leggi(v_months_freecooling, 'months_freecooling'), slice(J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input1_freecooling, 'input1_freecooling')), (J.chiama(J.attributo(J.leggi(v_months_freecooling, 'months_freecooling'), 'index'), J.leggi(v_input2_freecooling, 'input2_freecooling')) + 1), None))
                _o.append('\n    ')
            _o.append('\n    ')
            if (J.leggi(v_check, 'check') == 'OK'):
                _o.append('\n      ')
                if (J.leggi(v_mese_corrente, 'mese_corrente') in J.leggi(v_interval_1_freecooling, 'interval_1_freecooling')):
                    _o.append('\n        OK\n      ')
                else:
                    _o.append('\n        -\n      ')
                _o.append('\n    ')
            else:
                _o.append('\n      NOT OK\n    ')
            _o.append('\n  ')
        _o.append('      \n')
    return ''.join(_o)


def m1171(c, V):
    # {% set stati = ["sconosciuto", "unknown", "", none, "unavailable", "Non disponibile"] %...
    v_input1 = V.get('input1', J.MANCANTE)
    v_input2 = V.get('input2', J.MANCANTE)
    v_interruttore_freecooling = V.get('interruttore_freecooling', J.MANCANTE)
    v_interruttore_freeheating = V.get('interruttore_freeheating', J.MANCANTE)
    v_stati = J.MANCANTE
    _o = []
    v_stati = ['sconosciuto', 'unknown', '', None, 'unavailable', 'Non disponibile']
    _o.append(' ')
    if (c.states(c.N('sensor.vmc_master_sensori_memorizzata')) in J.leggi(v_stati, 'stati')):
        _o.append('\n  Non disponibile\n')
    else:
        _o.append('\n  ')
        v_input1 = c.states(c.N('sensor.vmc_master_status_freeheating'))
        _o.append('\n  ')
        v_input2 = c.states(c.N('sensor.vmc_master_status_freecooling'))
        _o.append('\n  ')
        v_interruttore_freecooling = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'))
        _o.append('\n  ')
        v_interruttore_freeheating = c.states(c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'))
        _o.append('   \n  ')
        if ((J.leggi(v_input1, 'input1') in J.leggi(v_stati, 'stati')) or (J.leggi(v_input2, 'input2') in J.leggi(v_stati, 'stati'))):
            _o.append('\n    Non disponibile\n  ')
        else:
            _o.append('     \n    ')
            if ((J.leggi(v_input1, 'input1') == 'OK') and (J.leggi(v_interruttore_freeheating, 'interruttore_freeheating') == 'on')):
                _o.append('\n      Free Heating\n    ')
            elif ((J.leggi(v_input2, 'input2') == 'OK') and (J.leggi(v_interruttore_freecooling, 'interruttore_freecooling') == 'on')):
                _o.append('\n      Free Cooling\n    ')
            else:
                _o.append('\n      Disabilitata\n    ')
            _o.append('\n  ')
        _o.append('    \n')
    return ''.join(_o)


def m1172(c, V):
    # {{ states('input_select.vmc_master_speed_1_fascia_calendario') | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(c.states(c.N('select.vmc_master_speed_1_fascia_calendario')), '')))
    return ''.join(_o)


def m1173(c, V):
    # {{ states('input_select.vmc_master_speed_2_fascia_calendario') | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(c.states(c.N('select.vmc_master_speed_2_fascia_calendario')), '')))
    return ''.join(_o)


def m1174(c, V):
    # {{ states('input_select.vmc_master_mese_1_fascia_freeheating') | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(c.states(c.N('select.vmc_master_mese_1_fascia_freeheating')), '')))
    return ''.join(_o)


def m1175(c, V):
    # {{ states('input_select.vmc_master_mese_2_fascia_freeheating') | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(c.states(c.N('select.vmc_master_mese_2_fascia_freeheating')), '')))
    return ''.join(_o)


def m1176(c, V):
    # {{ states('input_select.vmc_master_mese_1_fascia_freecooling') | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(c.states(c.N('select.vmc_master_mese_1_fascia_freecooling')), '')))
    return ''.join(_o)


def m1177(c, V):
    # {{ states('input_select.vmc_master_mese_2_fascia_freecooling') | default('') }}
    _o = []
    _o.append(J.testo(J.f_default(c.states(c.N('select.vmc_master_mese_2_fascia_freecooling')), '')))
    return ''.join(_o)
