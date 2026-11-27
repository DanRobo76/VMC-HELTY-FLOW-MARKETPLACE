"""Valori in piu' per i modelli della qualita' dell'aria (CO2, VOC, soglie, comfort, muffa)."""

from __future__ import annotations

_MEDIE = ("4w", "8w", "12w")
_ZERI = ",".join(["00000"] * 6)

EXTRA: dict[str, set[str]] = {
    # Rischio Muffa: umidita' medie oltre le curve dei livelli 1, 2 e 3; 93, 97 e 100
    # sono i valori esatti delle curve a 0 °C (confini compresi)
    **{f"sensor.vmc_master_hum_interna_media_{m}": {"73.5", "75", "84", "88", "93", "95", "97", "100"} for m in _MEDIE},
    # Rischio Muffa: temperature medie al confine delle condizioni estreme (0 e 50 compresi)
    **{f"sensor.vmc_master_temp_interna_media_{m}": {"-0.1", "50", "50.5"} for m in _MEDIE},
    # letture della VMC: Temp. Ext. -18,0 °C (Congelamento, confine compreso) e -16,0 °C
    # (vicina), CO2 1400 (confine dell'Alta Concentrazione), CO2 900 e VOC 650; l'ultima
    # ha solo la Temp. Int.: Temp. Ext., CO2 e VOC mancano ([Non Disponibile])
    "sensor.vmc_master_sensori_memorizzata": {
        f"VMGI,00210,10180,00500,01400,{_ZERI},00050,00000,00000,00000",
        f"VMGI,00210,10160,00500,00900,{_ZERI},00650,00000,00000,00000",
        "VMGI,00230",
    },
    # Offset CO2 ai confini delle concentrazioni (800, 1000, 1400) e in mezzo (900)
    "input_number.vmc_master_offset_co2": {"800.0", "900.0", "1000.0", "1400.0"},
    # CO2 Int. Selezionata: un sensore che scrive «-» (sonda assente) vale 0
    "sensor.esterno_due": {"-"},
}
