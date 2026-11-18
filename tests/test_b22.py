"""Prove della 9.0.0b22: un solo riavvio anche se cambia l'elenco escluse del recorder."""

from custom_components.vmc_master.installatore import genera_file, ricariche_necessarie

ESCLUSA = "\r\n      - binary_sensor.vmc_master_black_out_rilevato\r\n"


def _package_senza_esclusa() -> tuple[str, str]:
    nuovo = genera_file("master", "192.168.1.50", "9.0.0b22")["vmc_master.yaml"]
    assert nuovo.count(ESCLUSA) == 1
    return nuovo.replace(ESCLUSA, "\r\n", 1), nuovo


def test_entita_esclusa_aggiunta_senza_riavvio() -> None:
    """Un'entita' aggiunta alle escluse del recorder (come nella b21) non chiede il riavvio:
    l'elenco vale dal riavvio successivo; l'elenco della scheda si ricarica."""
    vecchio, nuovo = _package_senza_esclusa()
    assert ricariche_necessarie(vecchio, nuovo) == {"input_select.reload"}
    assert ricariche_necessarie(nuovo, vecchio) == {"input_select.reload"}


def test_altro_cambio_del_recorder_chiede_il_riavvio() -> None:
    nuovo = genera_file("master", "192.168.1.50", "9.0.0b22")["vmc_master.yaml"]
    assert "\r\nrecorder:\r\n" in nuovo
    vecchio = nuovo.replace("\r\nrecorder:\r\n", "\r\nrecorder:\r\n  purge_keep_days: 3\r\n", 1)
    assert ricariche_necessarie(vecchio, nuovo) is None
