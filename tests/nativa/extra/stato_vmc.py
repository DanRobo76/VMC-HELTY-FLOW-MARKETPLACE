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
    # IP fuori intervallo, riservati, con zeri iniziali o con spazi ai lati (questi ultimi
    # rendono piu' frequenti gli esiti della verifica, che valgono solo per lo stesso IP)
    "input_text.vmc_master_ip_insert": {
        "0.1.2.3",
        "127.0.0.1",
        "224.0.0.1",
        "223.255.255.254",
        "169.254.10.20",
        "169.253.1.1",
        "256.1.1.1",
        "1.2.3",
        " 192.168.1.60 ",
        "192.168.1.60 ",
        "\t192.168.1.60",
        " 10.0.0.7",
        "10.0.0.7\n",
        "192.168.1.50 ",
        "192.168.001.1",
    },
    # esiti della verifica per gli IP provati
    "input_text.vmc_master_ip_insert_esito": {
        "ok 192.168.1.60",
        "ok 10.0.0.7",
        "ok 223.255.255.254",
        "ok 169.253.1.1",
        "non_risponde 192.168.1.60",
        "non_risponde 10.0.0.7",
        "altro_dispositivo 10.0.0.7",
        "altro_dispositivo 192.168.1.60",
        "nome_diverso 192.168.1.60",
        "nome_diverso 223.255.255.254",
        "ok",
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

# sensori IP di altre VMC (per «IP già in uso»): uno con lo stesso IP di un candidato
INGRESSI = {"sensor.vmc_sala_ip", "sensor.vmc_cucina_ip"}
EXTRA.setdefault("sensor.vmc_sala_ip", set()).update({"192.168.1.60", " 192.168.1.61 ", "10.0.0.7"})
EXTRA.setdefault("sensor.vmc_cucina_ip", set()).update({"192.168.1.60", "192.168.1.62"})
EXTRA.setdefault("input_text.vmc_master_ip_insert", set()).update({"192.168.1.60", "192.168.1.61", "10.0.0.7"})
