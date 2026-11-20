"""Prove della 9.0.0b32: testi e commenti corretti dalla verifica profonda 1:1 (licenza, nome VMC)."""

from __future__ import annotations

from pathlib import Path

from custom_components.vmc_master import trasforma

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def test_licenza_con_il_nome_dell_integrazione() -> None:
    """La riga della licenza nomina l'integrazione (una sola per tutte le VMC), non la VMC."""
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt", "vmc_master_scheda_manuale_interfaccia.txt",
                 "vmc_master_script_cambio_ip.sh", "vmc_master_script_cambio_nome.sh"):
        riscritto = trasforma.rinomina(_testo(nome), "prova")
        assert riscritto.count("L'INTEGRAZIONE VMC MASTER") == 2, nome
        assert "INTEGRAZIONE VMC PROVA" not in riscritto, nome
        assert ("vmc_prova" in riscritto) == ("vmc_master" in _testo(nome)), nome


def test_script_cambio_nome() -> None:
    script = _testo("vmc_master_script_cambio_nome.sh")
    assert "RELEASE [VER. 9.0.0b32]" in script[:1000]
    assert "NE AMMETTE FINO A 12, LA SCHEDA 10" in script
    assert "pattern: '^[A-Za-z0-9_-]{0,10}$'" in _testo("vmc_master.yaml")


def _scheda() -> str:
    return _testo("vmc_master_scheda_manuale_interfaccia.txt").replace("\r\n", "\n")


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


def test_black_out_velocita_salvata_e_fascia() -> None:
    """A4-4, A4-7: la scheda ridotta e le note dicono anche la velocita' dell'allerta in corso e la fascia finita."""
    scheda = _scheda()
    assert "torna alla velocità salvata (o a quella memorizzata dall'allerta in corso). Non serve fare nulla." in scheda
    assert "riparte con la velocità della fascia (se nel frattempo la fascia è finita, si arresta). Non serve" in scheda
    piatto = _piatto(scheda)
    assert "che la VMC riprende al ritorno della corrente (o la velocità memorizzata dall'allerta in corso)." in piatto
    assert ("compare invece subito la scheda completa, con il countdown «Ripristino dopo Black-Out» (32 secondi): dopo "
            "altri 5 secondi la VMC riparte con la velocità della fascia") in piatto
    assert 'name: "Ripristino dopo Black-Out"' in scheda


def test_calendario_cinque_secondi_all_ingresso() -> None:
    """A4-8, A5-11: la voce 12 (Calendario) dice i 5 secondi dello script della Fascia, come il Foglio."""
    piatto = _piatto(_scheda())
    assert ("L'ingresso e l'uscita dalla Fascia avvengono dopo 3 secondi; all'ingresso il comando alla VMC parte dopo "
            "ulteriori 5 secondi (attesa dello script della Fascia); all'uscita la VMC si arresta.") in piatto
    pacchetto = _testo("vmc_master.yaml")
    assert pacchetto.count("seconds: 5") >= 2


def test_sezione_17_black_out_come_la_descrizione() -> None:
    """A5-9: la voce Black-Out della sezione 17 e' uguale a quella della descrizione dell'automazione."""
    descrizione = _piatto(_testo("vmc_master_automazione.txt").split("\n  - Black-Out: ", 1)[1].split(";\n\n", 1)[0])
    assert "Spia Black-Out del Calendario" in descrizione
    assert "- Black-Out: " + descrizione + ";<br>" in _piatto(_scheda())


def test_scheda_delta_e_congelamento() -> None:
    """A1-8: nessun «NON APPENA:» senza seguito; nella scheda Δ la VMC (a Velocita' 1) «SARÀ» a Velocita' 0."""
    righe = _scheda().split("\n")
    for i, riga in enumerate(righe):
        if "{% if cal_uscita %}AL TERMINE DELL'ALLERTA" in riga:
            con_seguito = "NON APPENA" in righe[i + 1][:60]
            assert ("NON APPENA:{% elif cal_ingresso" in riga) == con_seguito, i + 1
    assert sum("LA VMC SARÀ A <strong>VELOCITÀ 0</strong>" in r for r in righe) == 6
    assert sum("LA VMC RESTERÀ A <strong>VELOCITÀ 0</strong>" in r for r in righe) == 12


def test_grassetti_chiusi_nelle_schede_inquinanti() -> None:
    """A2-7: «[VMC ON/OFF, in Funzione del Lim. Δ P. di Rugiada]» chiude il grassetto nelle 3 schede inquinanti."""
    scheda = _scheda()
    assert "Funzione del Lim. Δ P. di Rugiada]<strong>" not in scheda
    assert scheda.count("Funzione del Lim. Δ P. di Rugiada]</strong>") >= 3


def test_free_tempi_di_ripresa() -> None:
    """A3-12: la voce 14 dice i tempi di ripresa in Free (24 secondi, 20 con Inquinanti)."""
    assert "riparte in Free Cool./Heat. quando la condizione torna favorevole (dopo 24 secondi; 20 con Inquinanti)." in (
        _piatto(_scheda()))


async def test_avvio_inquinanti_con_memoria_pdr(hass) -> None:
    """A2-4: il Msg 6 delle 3 schede inquinanti annuncia la velocita' a cui la VMC partira' davvero (la memoria PdR
    2, 3, 4, Notturna, Iperventilazione o Free senza programmazione; altrimenti Velocita' 1)."""
    from homeassistant.helpers.template import Template

    righe = _scheda().split("\n")
    pezzi = [righe[i] + "\n" + righe[i + 1] + "\n" + righe[i + 2] for i, r in enumerate(righe)
             if "{% set velocita_avvio = \"2\" %}" in r]
    assert len(pezzi) == 3 and len(set(pezzi)) == 1
    spia = "input_boolean.vmc_master_spia_velocita_"
    casi = [({}, "1"), ({"2": "on"}, "2"), ({"notturna": "on"}, "NOTTURNA"), ({"1": "on"}, "1"),
            ({"freecooling": "on"}, "FREE COOL./HEAT."),
            ({"freecooling": "on", "freecooling_un_solo_avvio_per_programmazione_freeheating": "on"}, "1")]
    for accese, atteso in casi:
        for k in ("1", "2", "3", "4", "notturna", "iperventilazione", "freecooling"):
            hass.states.async_set(f"{spia}{k}_un_solo_avvio", accese.get(k, "off"))
        for k in ("freecooling", "freeheating"):
            nome = f"freecooling_un_solo_avvio_per_programmazione_{k}"
            hass.states.async_set(f"{spia}{nome}", accese.get(nome, "off"))
        reso = Template("{% set attendere_avvio = 'ATTENDERE..' %}" + pezzi[0], hass).async_render(parse_result=False)
        assert f"AVVIO VMC A VELOCITA' {atteso} PER DARE PRIORITA'" in reso, (accese, reso)


async def test_umidita_rientrata_con_inquinanti(hass) -> None:
    """A3-6: a Umidita' rientrata con Inquinanti in corso la scheda Umidita' annuncia la Velocita' 1 fino al rientro
    degli Inquinanti, come fa il codice (anche con avvio in Free Cool./Heat., A3-1); altrimenti la Velocita' 0."""
    from homeassistant.helpers.template import Template

    scheda = _scheda()
    inizio = scheda.index("          {% if is_state('input_boolean.vmc_master_spia_umidita_velocita_0', 'on') %}\n"
                          "        {% if is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on')")
    pezzo = scheda[inizio : scheda.index("{% endif %}\n\n        {% endif %}", inizio) + len("{% endif %}\n\n        {% endif %}")]
    base = {
        "input_boolean.vmc_master_spia_umidita_velocita_0": "on",
        "input_boolean.vmc_master_spia_co2_o_voc": "on",
        "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc": "on",
        "sensor.vmc_master_alert_monitoraggio_co2": "Allerta",
        "sensor.vmc_master_alert_monitoraggio_voc": "Nessuna Allerta",
        "sensor.vmc_master_status_ventola_lettura_codice_interpretato": "Velocità 2",
        "input_select.vmc_master_speed_umidita": "Velocità 2",
    }
    casi = [({}, "PASSAGGIO"), ({"input_boolean.vmc_master_spia_co2_o_voc": "off"}, "RIPRISTINO"),
            ({"sensor.vmc_master_status_ventola_lettura_codice_interpretato": "Velocità 3"}, "RIPRISTINO"),
            ({"input_select.vmc_master_speed_umidita": "Free Cool./Heat.",
              "sensor.vmc_master_status_ventola_lettura_codice_interpretato": "Free Cooling"}, "PASSAGGIO")]
    for diversi, atteso in casi:
        for entita, stato in {**base, **diversi}.items():
            hass.states.async_set(entita, stato)
        reso = Template(pezzo, hass).async_render(parse_result=False)
        assert f"PROGRAMMATO IL {atteso} DELLA VMC" in reso, (diversi, reso)


def test_free_msg_7_e_15() -> None:
    """A3-5: Msg 7 della scheda Free dice che la ripresa verra' annullata se la velocita' scelta resta 20 secondi, e
    con l'Umidita' in corso spiega la Velocita' 1 (Nota 3); i Msg 15 e 15.1 annunciano il ripristino in Free."""
    scheda = _scheda()
    for tipo in ("HEATING", "COOLING"):
        assert f"LA RIPRESA AUTOMATICA\n        DELLA VMC SULLA VELOCITÀ FREE {tipo}" in scheda
        assert scheda.count(f"VELOCITÀ 1 PER L'ALLERTA UMIDITÀ [NOTA 3]: LA RIPRESA AUTOMATICA DELLA VMC SULLA VELOCITÀ FREE {tipo}") == 1
        assert scheda.count(f"RIPRISTINO SULLA VELOCITA' FREE {tipo}, {{{{ attendere }}}}") == 6
    assert scheda.count("SE MANTENUTA PER 20 SECONDI, LA RIPRESA AUTOMATICA") == 2
    assert "VIENE ANNULLATA.</strong>" not in scheda


def test_umidita_note_con_free_e_free_msg_14_1_1() -> None:
    """A3-11: con Set Free Cool./Heat. e VMC a Velocita' 1 per le allerte Free la NOTA di Msg 1 nomina la Velocita' 1;
    nel mese non programmato (stati «Se Avviata …») Msg 3 non consiglia la Velocita' 1, che resterebbe a fine Umidita'.
    A3-12: Msg 14.1.1 (VMC a 0, Inquinanti con interruttore acceso) dice cosa succede, uguale in Free Heating e Cooling."""
    scheda = _scheda()
    i = scheda.index("Velocità 1 O Free Cool./Heat.{% else %}")
    assert scheda.count("Velocità 1 O Free Cool./Heat.{% else %}") == 1
    assert scheda[i : scheda.index("Msg.", i)].endswith("{% endif %}\n\n\n        ")
    assert scheda[scheda.index("Msg.", i) :].startswith("Msg. 1\n")
    i = scheda.index("SI CONSIGLIA DI AVVIARE LA VMC SU <strong>Velocità 1</strong> ANZICHE'")
    lista = scheda[scheda.rindex("in [", 0, i) : i]
    assert "Se Avviata" not in lista
    assert lista.count('"') == 32
    for tipo in ("Heating", "Cooling"):
        fine = scheda.index(f"Msg. 14.1.1 Free {tipo}")
        corpo = scheda[scheda.rindex("<!------------------14.1.1", 0, fine) : fine]
        assert "AVVIO VMC A VELOCITA' 1 FINO AL RIENTRO DEGLI INQUINANTI, POI ARRESTO DELLA VMC" in corpo
        assert "DIVERSAMENTE" not in corpo
