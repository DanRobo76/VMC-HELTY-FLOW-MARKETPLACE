"""Prove della 9.0.0b33: testi della scheda, delle descrizioni e dei commenti corretti dalla verifica profonda 1:1
(A1-8, A2-2, A3-4, A3-12, A4-9, A4-10, A5-3, A5-4). Solo testi: la logica non cambia."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"

PDR_ECC = ("SE IL PUNTO DI RUGIADA INTERNO O ESTERNO DIVENTA [NON CALCOLABILE] O [NON DISPONIBILE], L'ALLERTA TERMINA "
           "E LA VMC RIPRENDE COMUNQUE DOPO 16 SECONDI (12 CON INQUINANTI)")
FREE_ECC = ("salvo la sospensione Free Cool./Heat.: l'Umidità parte comunque a Velocità 1 [Nota 3] e il suo "
            "interruttore non si spegne fino alla ripresa o all'annullamento della Free")
INQ_ECC = "(un'allerta Inquinanti già in corso prima del riavvio può riprendere prima)"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _scheda() -> str:
    return _testo("vmc_master_scheda_manuale_interfaccia.txt")


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


def _contenuti(nodo: object) -> Iterator[str]:
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k == "content" and isinstance(v, str):
                yield v
            else:
                yield from _contenuti(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _contenuti(v)


def _markdown(segno: str) -> str:
    trovati = [c for c in _contenuti(hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt")))
               if segno in c]
    assert len(trovati) == 1, segno
    return trovati[0]


def _rendi(hass, contenuto: str, stati: dict[str, str]) -> str:
    for entita, stato in stati.items():
        hass.states.async_set(entita, stato)
    return _piatto(Template(contenuto, hass).async_render(parse_result=False))


# ------------------------------------------------------------------------------------------------ A2-2
def test_pdr_non_calcolabile_nelle_condizioni_di_ripresa() -> None:
    """A2-2: le condizioni di ripresa della scheda PdR non promettono piu' di aspettare un PdR calcolabile: con PdR
    [Non Calcolabile] / [Non Disponibile] l'allerta termina e la VMC riprende dopo 16 s (12 s con Inquinanti)."""
    scheda = _scheda()
    assert "DIVERSO DA [NON CALCOLABILE]" not in scheda
    assert scheda.count(PDR_ECC) == 8
    automazione = _testo("vmc_master_automazione.txt")
    # i tempi scritti sono quelli dei trigger di ripristino (che usano != «Se ne sconsiglia l'impiego»)
    assert automazione.count("states('input_number.vmc_master_attesa_pdr_ripristino') | int(16)") == 9
    assert automazione.count("states('input_number.vmc_master_attesa_pdr_ripristino_inquinanti') | int(12)") == 7


async def test_pdr_msg_24_ripresa_con_memoria(hass) -> None:
    """A2-2: il Msg 24 (PdR non calcolabile) dice la ripresa quando una memoria PdR e' accesa."""
    pdr = _markdown("LIM. Δ PUNTO DI RUGIADA NON CALCOLABILE")
    spia = "input_boolean.vmc_master_spia_velocita_"
    base = {
        "sensor.vmc_master_punto_di_rugiada_verifica_confronto": "[Non Calcolabile]",
        "sensor.vmc_master_status_ip_interfaccia": "ON-Line",
        "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr": "on",
        "input_boolean.vmc_master_spia_co2_o_voc": "off",
        "input_number.vmc_master_fase_riallineamento_al_riavvio": "0",
        "sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling": "Free Heating",
        f"{spia}1_co2_o_voc_pdr": "off",
        **{f"{spia}{k}_un_solo_avvio": "off"
           for k in ("0", "1", "2", "3", "4", "notturna", "freecooling", "iperventilazione")},
    }
    casi = [
        ({f"{spia}2_un_solo_avvio": "on"}, "SULLA VELOCITA' 2 DOPO 16 SECONDI (12 CON INQUINANTI), ATTENDERE.."),
        ({f"{spia}freecooling_un_solo_avvio": "on"}, "SULLA VELOCITA' FREE HEATING DOPO 16 SECONDI"),
        ({f"{spia}1_co2_o_voc_pdr": "on"}, "SULLA VELOCITA' 0 DOPO 16 SECONDI"),
        ({f"{spia}3_un_solo_avvio": "on", "sensor.vmc_master_punto_di_rugiada_verifica_confronto": "[Non Disponibile]",
          "input_number.vmc_master_fase_riallineamento_al_riavvio": "3"},
         "SULLA VELOCITA' 3 DOPO 16 SECONDI (12 CON INQUINANTI), ATTENDERE LA RIATTIVAZIONE DEL 3° GRUPPO"),
    ]
    for diversi, atteso in casi:
        reso = _rendi(hass, pdr, {**base, **diversi})
        assert "LIM. Δ PUNTO DI RUGIADA NON CALCOLABILE" in reso, diversi
        assert "L'ALLERTA PER IL LIM. Δ PUNTO DI RUGIADA TERMINA COMUNQUE: RIPRESA AUTOMATICA DELLA VMC" in reso
        assert atteso in reso.replace("<strong>", "").replace("</strong>", ""), (diversi, reso)
    # nessuna memoria, interruttore spento o memoria 1 (Inquinanti) con Inquinanti ancora in corso: nessuna ripresa
    for diversi in ({}, {f"{spia}2_un_solo_avvio": "on", "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr": "off"},
                    {f"{spia}1_co2_o_voc_pdr": "on", "input_boolean.vmc_master_spia_co2_o_voc": "on"}):
        reso = _rendi(hass, pdr, {**base, **diversi})
        assert "LIM. Δ PUNTO DI RUGIADA NON CALCOLABILE" in reso
        assert "RIPRESA AUTOMATICA" not in reso, diversi


# ------------------------------------------------------------------------------------------- A4-9, A4-10
def test_gruppi_del_riavvio_come_il_foglio() -> None:
    """A4-9: nomi dei gruppi come nel Foglio A27 nel pannello, nella Nota e nella descrizione del riallineamento;
    A4-10: «Inquinanti dopo 100 secondi» con l'eccezione dell'allerta gia' in corso prima del riavvio."""
    scheda = _scheda()
    g1 = "1° gruppo: Black-Out, Congelamento, Δ Temp."
    g3 = "3° gruppo: Lim. Δ Punto di Rugiada, Free Cool./Heat., Calendario, Umidità"
    assert f'label: "{g1}"' in scheda and f'label: "{g3}"' in scheda
    # telefono stretto: etichette non piu' lunghe di 3 caratteri rispetto alla b32
    assert len(g1) <= len("1° gruppo: Black-Out, Congelamento, Diff. Temp.")
    assert len(g3) <= len("3° gruppo: Punto di Rugiada, Free Heating/Cooling, Calendario, Umidità") + 3
    i = scheda.index("<strong>Nota Avvio di Home Assistant</strong>")
    nota = _piatto(scheda[i : scheda.index("<br>", i)])
    assert ("dopo 60 secondi Black-Out, Congelamento e Δ Temp.; dopo 100 secondi Inquinanti " + INQ_ECC
            + "; dopo 140 secondi Lim. Δ Punto di Rugiada, Free Cool./Heat., Calendario e Umidità.") in nota
    automazioni = hay.load_yaml(str(PKG / "vmc_master.yaml"))["automation"]
    riallineamento = next(a for a in automazioni if a["id"] == "vmc_master_riallineamento_allerte_al_riavvio")
    descrizione = _piatto(riallineamento["description"])
    assert ("Black-Out, Congelamento e Δ Temp.; dopo 40 s Inquinanti " + INQ_ECC
            + "; dopo altri 40 s Lim. Δ Punto di Rugiada, Free Cool./Heat., Calendario e Umidità.") in descrizione
    assert "60 s per Black-Out, Congelamento e Δ Temp., poi 40 s per Inquinanti" in descrizione
    for testo in (nota, descrizione, scheda[:10000]):
        assert "Diff. Temp." not in testo
        assert "Free Heating/Cooling" not in testo


# ------------------------------------------------------------------------------------------------ A1-8
def test_fonte_delle_allerte_congelamento_e_delta() -> None:
    """A1-8.1: le schede Congelamento e Δ Temp. nominano la sonda della VMC e l'entita' selezionata."""
    scheda = _scheda()
    assert "NEI SENSORI" not in scheda
    # b34 (B5-2, B5-3): gli 8 titoli «… E NELL'ENTITÀ SELEZIONATA» prendono la coda da {{ e_entita }} (sonda di riserva:
    # «(ENTITÀ SCELTA NON DISPONIBILE)»); il ramo 0 del Δ non nomina piu' la sonda e dice la fonte del Congelamento
    # con {{ dove_congelamento }} (2 volte la sonda e 2 l'entita' nelle variabili, 3 «… E NELL'ENTITÀ» in e_entita)
    assert scheda.count("NELLA SONDA DELLA VMC E NELL'ENTITÀ SELEZIONATA") == 0
    assert scheda.count("NELLA SONDA DELLA VMC{{ e_entita }}") == 8
    assert scheda.count("NELLA SONDA DELLA VMC") == 8 + 10 + 2
    assert scheda.count("NELL'ENTITÀ SELEZIONATA") == 10 + 3 + 2
    assert "ALLERTA CONGELAMENTO NELL'ENTITÀ SELEZIONATA</strong>" in scheda
    assert "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C] NELLA SONDA DELLA VMC</strong>" in scheda
    assert "NESSUNA ALLERTA CONGELAMENTO NELLA SONDA DELLA VMC{{ e_entita }} </strong>" in scheda


# ------------------------------------------------------------------------------------------- A5-3, A5-4
def test_commenti_non_richiamato() -> None:
    """A5-3, A5-4: lo script di notifica del Media Player e il codice della velocita' non sono richiamati."""
    pacchetto = _testo("vmc_master.yaml")
    script = re.search(r"\n  vmc_master_notifica_errore_media_player: +# (.+)", pacchetto).group(1)
    sensore = re.search(r"default_entity_id: sensor\.vmc_master_status_ventola_lettura_codice +# (.+)", pacchetto).group(1)
    for commento in (script, sensore):
        assert re.match(r"\[CONFIGURAZIONE, \d+ RICHIAM[OI]\] \[INTERFACCIA, \d+ RICHIAM[OI]\] "
                        r"\[AUTOMAZIONE, 0 RICHIAMI\] NON RICHIAMATO: ", commento), commento
    assert "NESSUNA NOTIFICA PER IL MEDIA PLAYER NON DISPONIBILE" in script
    assert "NESSUN TEMPLATE, AUTOMAZIONE O SCHEDA NE LEGGE LO STATO" in sensore


# ------------------------------------------------------------------------------------------------ A3-4
def test_umidita_con_free_sospesa() -> None:
    """A3-4: descrizione dell'automazione, sezione 17 e Informazioni 7 dicono l'eccezione della sospensione Free."""
    descrizione = _piatto(hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))["description"])
    assert f"Free Cooling/Heating), finché quell'allerta non è finita ({FREE_ECC}). Esempio:" in descrizione
    assert f"l'allerta Umidità non scatta e l'interruttore si spegne normalmente ({FREE_ECC});" in descrizione
    scheda = _piatto(_scheda())
    # la sezione 17 della scheda ripete la descrizione
    assert scheda.count(FREE_ECC) == 4
    assert f"Free Cooling/Heating), finché quell'allerta non è finita ({FREE_ECC}). Esempio:" in scheda
    assert f"l'interruttore si spegne normalmente ({FREE_ECC});<br>" in scheda
    # Informazioni 7
    assert f"su ON e senza altre allerte in corso ({FREE_ECC}), comandano l'avvio e l'arresto" in scheda
    assert f"l'allerta Umidità non scatta e l'interruttore si spegne normalmente ({FREE_ECC})." in scheda


# ----------------------------------------------------------------------------------------------- A3-12
def test_free_annullamento_dopo_la_terza_condizione() -> None:
    """A3-12 (a): nei Msg 1, 2.1, 2.2, 3, 5, 8.1, 8.2 la frase «DIVERSAMENTE / ALTRIMENTI … ANNULLATA» segue la 3ª
    condizione (mese corrente programmato), non sta piu' tra la 2ª e la 3ª."""
    scheda = _scheda()
    for tipo in ("HEATING", "COOLING"):
        for numero in ("1,", "2.1,", "2.2,", "3,", "5", "8.1,", "8.2,"):
            fine = scheda.index(f"Msg. {numero} Free {tipo.title()}")
            inizio = scheda.rindex("RIMARRÀ IMPOSTATA SU ACCESO\n", 0, fine)
            corpo = scheda[inizio:fine]
            mese = corpo.index(f"IMPOSTATO SU FREE {tipo}\n")
            frase = re.search(r"<strong> ?(DIVERSAMENTE|ALTRIMENTI)", corpo)
            assert frase and frase.start() > mese, (tipo, numero, corpo)
    assert not re.search(r"IMPOSTATA SU ACCESO\n        <strong> ?(DIVERSAMENTE|ALTRIMENTI)[^\n]*\n[^\n]*\n            e \n"
                         r"          - IL MESE", scheda)


async def test_free_msg_3_e_5_con_interruttore_inquinanti(hass) -> None:
    """A3-12 (b): con l'interruttore CO₂/VOC acceso i Msg 3 e 5 non dicono l'arresto: la VMC va a Velocita' 1 (dopo
    circa 8 s nel Msg 3, dopo circa 20 s nel Msg 5) e l'annullamento della ripresa la porta a Velocita' 1."""
    free = _markdown("Msg. 3, Free Heating Allarmato")
    for tipo, mese, ti, te in (("Heating", "Free Heating", "22", "10"), ("Cooling", "Free Cooling", "22", "26")):
        base = {
            "sensor.vmc_master_status_ip_interfaccia": "ON-Line",
            "sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling": mese,
            f"input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_free{tipo.lower()}": "on",
            "sensor.vmc_master_temp_interna_status": ti,
            "sensor.vmc_master_temp_esterna_status": te,
            "sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_disabilitato": "OK",
            "sensor.vmc_master_alert_monitoraggio_co2": "Allerta",
            "sensor.vmc_master_alert_monitoraggio_voc": "Nessuna Allerta",
            "input_number.vmc_master_fase_riallineamento_al_riavvio": "0",
        }
        spia = f"input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_free{tipo.lower()}"
        msg3 = {**base, "sensor.vmc_master_status_ventola_lettura_codice_interpretato": "Velocità 0", spia: "on"}
        msg5 = {**base, "sensor.vmc_master_status_ventola_lettura_codice_interpretato": "Free Cooling", spia: "off"}
        for stati, numero in ((msg3, f"Msg. 3, Free {tipo} Allarmato"), (msg5, f"Msg. 5 Free {tipo}")):
            acceso = _rendi(hass, free, {**stati, "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc": "on"})
            spento = _rendi(hass, free, {**stati, "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc": "off"})
            assert numero in acceso and numero in spento, (numero, acceso, spento)
            assert "DIVERSAMENTE VERRÀ ANNULLATA LA RIPRESA AUTOMATICA, IMPOSTANDO LA VELOCITÀ DELLA VMC A 1." in acceso
            assert "CONFERMANDO L'ARRESTO" not in acceso and "VMC ARRESTATA" not in acceso, acceso
            assert "DIVERSAMENTE VERRÀ ANNULLATA LA RIPRESA AUTOMATICA, CONFERMANDO L'ARRESTO DELLA VMC." in spento
            assert "VELOCITÀ DELLA VMC A 1" not in spento and "PASSERÀ A VELOCITÀ 1" not in spento
            if numero.startswith("Msg. 3"):
                assert "AVVIO VMC A VELOCITA' 1 PER LA PRESENZA DI INQUINANTI (DOPO CIRCA 8 SECONDI)" in acceso
                assert "VMC ARRESTATA" in spento and "AVVIO VMC" not in spento
            else:
                assert "IN ALTERNATIVA, PER LA PRESENZA DI INQUINANTI, DOPO CIRCA 20 SECONDI LA VMC PASSERÀ A VELOCITÀ 1" in acceso


def test_opzioni_free_secondary_info_uguale() -> None:
    """A3-12 (c): le righe dei mesi nelle Opzioni Free hanno tutte la stessa secondary_info."""
    scheda = _scheda()
    for mese in ("mese_1_fascia_freeheating", "mese_2_fascia_freeheating", "mese_1_fascia_freecooling",
                 "mese_2_fascia_freecooling"):
        assert (f"                        - entity: input_select.vmc_master_{mese}\n"
                "                          secondary_info: last-updated\n") in scheda, mese
