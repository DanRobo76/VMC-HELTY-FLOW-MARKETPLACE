"""Prove della 9.0.0b33 (Free Cool./Heat.): A3-7 (cambio del mese programmato con la Free sospesa e l'allerta Umidita'
in corso) e A3-10 (velocita' scelta dall'utente durante l'attesa della ripresa in Free). Confermate dalle prove
dinamiche (simulatore con Home Assistant reale, scenari a3_7.py e a3_10.py)."""

from __future__ import annotations

import re
from pathlib import Path

from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
LETTURA = "states('sensor.vmc_master_status_ventola_lettura_codice_interpretato')"
SPIA_UMIDITA = "states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')"
SET_UMIDITA = "states('input_select.vmc_master_speed_umidita')"
# b36: con [Set Velocità Umidità di Avvio] su Velocità 0 la Velocità 1 con l'Umidità accesa è una scelta dell'utente
RIPRESA_SENZA_INQUINANTI = (
    f"and ({LETTURA} in ['Velocità 0', 'Free Cooling'] or ({SPIA_UMIDITA} == 'on' and {SET_UMIDITA} != 'Velocità 0' "
    f"and {LETTURA} == 'Velocità 1'))"
)
RIPRESA_CON_INQUINANTI = f"and {LETTURA} in ['Velocità 0', 'Velocità 1', 'Free Cooling']"
ANNULLAMENTO_A3_2 = f"and ({SPIA_UMIDITA} == 'off' or {SET_UMIDITA} == 'Velocità 0' or {LETTURA} != 'Velocità 1')"
RIPRESE = {
    "Rip. Free Heating No TeVsTi ": RIPRESA_SENZA_INQUINANTI,
    "Rip. Free Cooling No TeVsTi ": RIPRESA_SENZA_INQUINANTI,
    "Rip. Free Heating No TeVsTi e Spia Inquinanti ON": RIPRESA_CON_INQUINANTI,
    "Rip. Free Cooling No TeVsTi e Spia Inquinanti ON": RIPRESA_CON_INQUINANTI,
}
DISATTIVAZIONI = [
    "Disattivazione VMC ON/OFF, in Funzione della Vel. Free Heating precedentemente Armato",
    " Disattivazione VMC ON/OFF, in Funzione della Vel. Free Heating precedentemente Armato e Spia Inquinanti ON",
    "Disattivazione VMC ON/OFF, in Funzione della Vel. Free Cooling precedentemente Armato",
    " Disattivazione VMC ON/OFF, in Funzione della Vel. Free Cooling precedentemente Armato e Spia Inquinanti ON",
]


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


def _automazione() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _trigger(id_: str) -> dict:
    return next(t for t in _automazione()["triggers"] if t.get("id") == id_)


def _copia_trigger_id(id_: str) -> str:
    """La copia della condizione nel blocco «Evento ancora valido» ({%- elif trigger.id == '…' -%})."""
    testo = _testo("vmc_master_automazione.txt")
    testa = "{%- elif trigger.id == '" + id_ + "' -%}"
    assert testo.count(testa) == 1, id_
    i = testo.index(testa) + len(testa)
    return testo[i : testo.index("{%-", i)]


def _ramo(alias_inizio: str, chiave: str = "sequence") -> dict:
    """Il passo delle azioni con questo inizio di alias e con questa chiave (sequence o then)."""
    trovati = []

    def cerca(nodo) -> None:
        if isinstance(nodo, dict):
            if _norm(str(nodo.get("alias", ""))).startswith(alias_inizio) and chiave in nodo:
                trovati.append(nodo)
            for valore in nodo.values():
                cerca(valore)
        elif isinstance(nodo, list):
            for valore in nodo:
                cerca(valore)

    cerca(_automazione()["actions"])
    assert len(trovati) == 1, alias_inizio
    return trovati[0]


def test_ripresa_free_solo_senza_velocita_scelta() -> None:
    """A3-10: la ripresa in Free (24 s; 20 s con Inquinanti) parte solo con la VMC a Velocita' 0, in Free o alla
    Velocita' 1 di Nota 3: una velocita' scelta dall'utente azzera il «for:» e vince l'annullamento (Foglio A29),
    anche quando le condizioni sono gia' tornate favorevoli. Trigger, copia trigger.id e 2 copie del Countdown."""
    automazione = _testo("vmc_master_automazione.txt")
    pacchetto = _testo("vmc_master.yaml")
    # b36 (C4-3): +2 copie della condizione senza Inquinanti nel trigger PdR 154 (trigger e guardia, ON e OFF)
    for nuova, copie in ((RIPRESA_SENZA_INQUINANTI, 6), (RIPRESA_CON_INQUINANTI, 4)):
        assert automazione.count(nuova) == copie
        assert pacchetto.count(nuova) == copie
    for id_, nuova in RIPRESE.items():
        trigger = _trigger(id_)
        assert nuova in trigger["value_template"], id_
        assert nuova in _copia_trigger_id(id_), id_
        assert "A3-10" in trigger["alias"]


def test_ripresa_e_annullamento_complementari() -> None:
    """A3-10 non tocca A3-2: senza Inquinanti la ripresa e l'annullamento (20 s) non sono mai veri insieme."""
    automazione = _testo("vmc_master_automazione.txt")
    assert automazione.count(ANNULLAMENTO_A3_2) == 2
    assert _testo("vmc_master.yaml").count(ANNULLAMENTO_A3_2) == 2
    for lettura in ("Velocità 0", "Velocità 1", "Velocità 2", "Velocità 3", "Velocità 4", "Notturna",
                    "Iperventilazione", "Free Cooling"):
        for umidita in ("on", "off"):
            for set_0 in (True, False):
                ripresa = lettura in ("Velocità 0", "Free Cooling") or (
                    umidita == "on" and not set_0 and lettura == "Velocità 1")
                annullamento = lettura not in ("Velocità 0", "Free Cooling") and (
                    umidita == "off" or set_0 or lettura != "Velocità 1")
                assert ripresa != annullamento, (lettura, umidita, set_0)


def test_copie_trigger_id_uguali_ai_trigger() -> None:
    for id_ in [*RIPRESE, *DISATTIVAZIONI]:
        assert _norm(_copia_trigger_id(id_)) == _norm(_trigger(id_)["value_template"]), id_


def test_cambio_mese_con_umidita_va_alla_velocita_di_avvio() -> None:
    """A3-7: al cambio del mese programmato con la Free sospesa e l'allerta Umidita' in corso la VMC va alla velocita'
    di avvio dell'Umidita' (come all'avvio: Set; con Set Free Cool./Heat. Velocita' 1 se ci sono allerte Free,
    altrimenti Free) e la memoria Umidita' diventa «avviata da Velocita' 0» (fine Umidita' a 0, ripresa annullata).
    Con l'interruttore spento dall'utente resta la Velocita' 0 (Foglio A27); con gli Inquinanti resta la Velocita' 1."""
    avvio_u3 = _ramo("Umidità che ha avviato la VMC da Velocità 0 e VMC ancora (o di nuovo) a 0", "then")
    regola_175 = next(p["variables"] for p in avvio_u3["then"] if "variables" in p and "free_con_allerte" in p["variables"])
    for tipo, chiave in (("Heating", "freeheating"), ("Cooling", "freecooling")):
        ramo = _ramo(f"Disattivazione VMC ON/OFF, in Funzione della Vel. Free {tipo} precedentemente Armato -> Vel. 0")
        passi = ramo["sequence"][0]["choose"][0]["sequence"]  # senza Congelamento e senza Δ Temp.
        corpo = str(passi)
        variabili = next(p["variables"] for p in passi if "variables" in p and "velocita_finale" in p["variables"])
        assert variabili["umidita_al_cambio_mese"] == (
            "{{ is_state('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia', 'on') and "
            f"is_state('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_{chiave}', 'on') }}}}")
        assert variabili["free_con_allerte"] == regola_175["free_con_allerte"]
        assert variabili["vel_avvio"] == regola_175["vel_avvio"] == (
            "{{ 'Velocità 1' if free_con_allerte else states('input_select.vmc_master_speed_umidita') }}")
        assert variabili["velocita_finale"] == (
            "{{ ('Free Cooling' if vel_avvio == 'Free Cool./Heat.' else vel_avvio) if umidita_al_cambio_mese "
            "else 'Velocità 0' }}")
        assert "'Free Cooling': 'freecooling'}.get(velocita_finale, 'velocita_0')" in variabili["comando_vmc"]
        assert "shell_command.vmc_master_{{ comando_vmc }}" in corpo
        assert "shell_command.vmc_master_velocita_0'" not in corpo
        assert "== velocita_finale" in _norm(corpo)
        inquinanti = _ramo(f"Disattivazione VMC ON/OFF, in Funzione della Vel. Free {tipo} precedentemente Armato -> Vel. 1")
        passi_inquinanti = inquinanti["sequence"][0]["choose"][0]["sequence"]
        assert "velocita_finale" not in str(passi_inquinanti)
        assert "shell_command.vmc_master_velocita_1" in str(passi_inquinanti)
        assert next(p["variables"]["umidita_al_cambio_mese"] for p in passi_inquinanti
                    if "umidita_al_cambio_mese" in p.get("variables", {})) == variabili["umidita_al_cambio_mese"]
        for r in (passi, passi_inquinanti):
            memoria = next(p for p in r if "if" in p and "{{ umidita_al_cambio_mese }}" in str(p["if"]))
            assert memoria["then"][0]["target"]["entity_id"] == "input_boolean.vmc_master_spia_umidita_velocita_0"
            spente = memoria["then"][1]["target"]["entity_id"]
            assert "input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0" in spente and len(spente) == 8


def test_scheda_msg_15_ripristino_solo_con_umidita() -> None:
    """Msg 15 e 15.1: con la velocita' scelta dall'utente la ripresa non avviene piu' (A3-10)."""
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    for tipo in ("HEATING", "COOLING"):
        assert scheda.count(
            f"È STATA SCELTA LA {{{{ velocita | upper }}}}: SE MANTENUTA PER 20 SECONDI, LA RIPRESA IN FREE {tipo} "
            "VERRÀ ANNULLATA{% endif %}") == 2
        assert scheda.count(
            "and is_state('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia', 'on') and not "
            "is_state('input_select.vmc_master_speed_umidita', 'Velocità 0') and velocita == "
            f"\"Velocità 1\" %}}RIPRISTINO SULLA VELOCITA' FREE {tipo}") == 2
    piatta = _norm(scheda)
    assert "<b>Cambio del mese programmato.</b>" in piatta
    # b36 (C5-4): la riga prosegue con le due frasi del Foglio (Inquinanti e Free scelta con condizioni sfavorevoli)
    assert ("anche con le condizioni già tornate favorevoli (ripresa in attesa); con Inquinanti la Velocità scelta viene "
            "memorizzata dall'allerta Inquinanti dopo 8 Secondi; scegliendo Free Cool./Heat. con le condizioni ancora "
            "sfavorevoli la VMC torna a Velocità 0 dopo 24 Secondi</td>") in piatta


def test_descrizione_e_voce_17_uguali() -> None:
    descrizione = _norm(_testo("vmc_master_automazione.txt").split("\n  - Free Cool./Heat.: 24 Secondi. ", 1)[1]
                        .split(";\n\n", 1)[0])
    assert "esce dalla Fascia" in descrizione and "anche se le condizioni sono già tornate favorevoli" in descrizione
    assert "- Free Cool./Heat.: 24 Secondi. " + descrizione + ";<br>" in _norm(_testo("vmc_master_scheda_manuale_interfaccia.txt"))
