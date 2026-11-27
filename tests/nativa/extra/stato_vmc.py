"""Valori in piu' per i modelli dello stato della VMC (nativa/modelli/stato_vmc.py)."""

from __future__ import annotations


def _vmgh(velocita: str, sensori: str, led: str | None, campi: int = 15) -> str:
    """Risposta VMGH? con velocita' (campo 1), stato dei sensori (campo 4) e LED (campo 14)."""
    valori = ["VMGO", velocita, "00000", "00000", sensori] + ["00000"] * 10
    if led is not None:
        valori[14] = led
    return ",".join((valori + ["00000"] * campi)[:campi])


EXTRA: dict[str, set[str]] = {
    # sensori accesi/spenti (campo 4) e LED del pannello (campo 14) diversi da 00000,
    # codici sconosciuti e risposte troncate
    "sensor.vmc_master_status_ventola_memorizzata": {
        _vmgh("00002", "00001", "00032"),
        _vmgh("00004", "00002", "00010"),
        _vmgh("00006", "00003", "00032"),
        _vmgh("00007", "00002", "00001"),
        _vmgh("00005", "00001", "00000"),
        _vmgh("00008", "00009", "00001"),
        _vmgh("00007", "00000", "00032", campi=16),
        _vmgh("00001", "00002", None, campi=14),
        "VMGO,00001,00000,00000,00002",
        "VMGO,00003,00000,00000",
        "VMGO,00006",
        "VMGO",
        "Non disponibile",
        "sconosciuto",
    },
    # nomi senza parte dopo lo spazio, con spazi e nomi che Home Assistant legge come letterali
    "sensor.vmc_master_nome_memorizzata": {
        "VMNM",
        "VMNM ",
        "VMNM  Sala Grande  ",
        "VMNM 1.50",
        "VMNM 42",
        "VMNM 007",
        "VMNM 1e3",
        "VMNM 1_000",
        "VMNM None",
        "VMNM True",
        "VMNM [1, 2]",
        "VMNM ...",
        "VMNM 99999999999999999.5",
        "Non disponibile",
        "sconosciuto",
    },
    # volumi che danno ore, minuti e secondi al singolare e al plurale con ogni portata;
    # i volumi minuscoli portano i ricambi oltre 1e16 (Home Assistant scrive «1.2e+16»)
    "input_number.vmc_master_volume_da_inserire": {
        "0.0001",
        "0.0002",
        "0.0005",
        "0.0028",
        "0.012",
        "0.17",
        "0.3",
        "0.7",
        "1.5",
        "4.2",
        "10",
        "10.003",
        "10.17",
        "10.5",
        "17",
        "20.03",
        "42",
        "-5",
        "none",
    },
    "input_number.vmc_master_aria_scambiata_ricomincio": {"10", "9.5", "4.2", "none"},
}

UN_SOLO_RISULTATO: dict[str, str] = {
    "sensor.versione_corrente": "testo fisso: «v.» e la versione dell'integrazione",
    "sensor.ip": "testo fisso: l'IP configurato della VMC (scritto nel package all'installazione)",
}
