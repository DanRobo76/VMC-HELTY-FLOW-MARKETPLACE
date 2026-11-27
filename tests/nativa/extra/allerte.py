"""Valori in piu' per il banco: gruppo «allerte» (Black-Out rilevato e monitoraggi).

La condizione di ``binary_sensor.black_out_rilevato`` e' vera solo con la VMC OFF-Line, un
codice di velocita' preciso e una ventina di spie tutte ``off`` insieme (tasti di velocita'
e 14 Fasce del Calendario): cambiando gli ingressi a caso il banco non ci arriva mai, e
aggiungere candidati agli ingressi (``EXTRA``) non aiuta. ``SCENARI`` raccoglie le
combinazioni che rendono vera ciascuna delle undici condizioni (t1…t11) e quella con tutti
gli offset al minimo: il banco le impone in alcuni giri, a volte cambiandone uno o due
ingressi (casi vicini).
"""

from __future__ import annotations

_P = "input_boolean.vmc_master_"
_VELOCITA = ("0", "1", "2", "3", "4", "notturna", "freecooling", "iperventilazione")
_GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")
_CALENDARIO_SPENTO = {f"{_P}spia_calendario_{g}_{n}": "off" for g in _GIORNI for n in (1, 2)}
# codice di velocita' letto (secondo campo di status_ventola_memorizzata) e spia del tasto
_CODICI = {
    "t1": ("00000", "0"),
    "t5": ("00002", "2"),
    "t6": ("00003", "3"),
    "t7": ("00004", "4"),
    "t8": ("00006", "notturna"),
    "t9": ("00005", "iperventilazione"),
    "t10": ("00007", "freecooling"),
}
_V1 = {  # spie in piu' dei casi «Velocità 1» (t2, t3, t4, t11)
    "t2": {"co2_o_voc": "off", "co2_o_voc_partenza_ritorno_velocita_0": "off", "velocita_1_co2_o_voc_pdr": "off",
           "velocita_1_co2_o_voc": "off", "velocita_freecooling_un_solo_avvio_per_programmazione_freecooling": "off",
           "velocita_freecooling_un_solo_avvio_per_programmazione_freeheating": "off"},
    "t3": {"co2_o_voc": "on", "velocita_freecooling_un_solo_avvio_per_programmazione_freecooling": "off",
           "velocita_freecooling_un_solo_avvio_per_programmazione_freeheating": "off"},
    "t4": {"co2_o_voc": "on", "velocita_freecooling_un_solo_avvio_per_programmazione_freeheating": "on"},
    "t11": {"co2_o_voc": "off", "velocita_1_co2_o_voc_pdr": "on"},
}


def _black_out(codice: str, spia: str, altre: dict[str, str] | None = None) -> dict[str, str]:
    scenario = {
        "sensor.vmc_master_status_ip": "OFF-Line",
        "sensor.vmc_master_status_ventola_memorizzata": f"VMGO,{codice}" + ",00000" * 13,
        **{f"{_P}spia_velocita_{s}": "off" for s in _VELOCITA if s != spia},
        **_CALENDARIO_SPENTO,
    }
    scenario.update({f"{_P}spia_{k}": v for k, v in (altre or {}).items()})
    return scenario


# {nome: stati da imporre insieme}; nome = condizione del Black-Out che il caso rende vera
SCENARI: dict[str, dict[str, str]] = {
    **{t: _black_out(codice, spia) for t, (codice, spia) in _CODICI.items()},
    **{t: _black_out("00001", "1", altre) for t, altre in _V1.items()},
    # alert_monitoraggio_offset_tutti_min → «NOT OK»: ogni offset al suo minimo
    "offset_tutti_min": {
        "sensor.vmc_master_sensori_memorizzata": "VMGI,00210,00100,00500,00600,00000,00000,00000,00000,00000,00000,00050,00000,00000,00000",
        "input_number.vmc_master_offset_temp_interna": "-50.0",
        "input_number.vmc_master_offset_temp_esterna": "-50.0",
        "input_number.vmc_master_offset_umidita_interna": "-100.0",
        "input_number.vmc_master_offset_umidita_esterna": "-100.0",
        "input_number.vmc_master_offset_co2": "-1500.0",
        "input_number.vmc_master_offset_voc": "-1000.0",
    },
}
