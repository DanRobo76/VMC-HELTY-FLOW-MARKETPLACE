"""Prova su una copia della configurazione (strumenti/copia_configurazione).

Due gruppi:

- prove veloci del banco stesso: VMC finte sulla porta TCP, piano delle impostazioni
  «prima» (valori validi per gli aiutanti di oggi e non predefiniti), mappa dei nomi,
  controlli su istantanee costruite a mano, rapporto;
- la prova vera (``slow``, diversi minuti): ``banco.py`` con un Home Assistant vero in
  uno spazio di rete suo. Gira solo se scelta: ``pytest -m slow tests/copia_configurazione``.
  Il passo ``passaggio`` deve dare tutti i controlli passati: finché il codice nativo del
  passaggio non c'è, fallisce al primo passo mancante (lo dice il messaggio).
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# La fixture automatica di tests/conftest.py (vmc_nativa_senza_rete) importa
# custom_components.vmc_master dopo che la fixture «hass» ha montato la cartella di
# configurazione delle prove: va importato prima, qui, come fanno gli altri moduli
import custom_components.vmc_master  # noqa: F401

RADICE = Path(__file__).resolve().parents[2]
BANCO = RADICE / "strumenti" / "copia_configurazione"
sys.path.insert(0, str(BANCO))

import controlli
import rapporto
import utente
from vmc_finte import VMCFinta, VMCFinte, risposta_lan

PYTHON_HA = os.environ.get("VMC_BANCO_PYTHON", "/home/user/hav/bin/python")
"""Il Python di Home Assistant con le dipendenze complete di default_config."""


# ----------------------------------------------------------------- VMC finte
async def _chiedi(porta: int, testo: str) -> str:
    lettore, scrittore = await asyncio.open_connection("127.0.0.1", porta)
    scrittore.write(testo.encode())
    await scrittore.drain()
    risposta = await asyncio.wait_for(lettore.read(1024), 3)
    scrittore.close()
    return risposta.decode()


@pytest.mark.usefixtures("socket_enabled")
async def test_vmc_finta_risponde_come_il_simulatore() -> None:
    """Le risposte della VMC finta sulla porta TCP sono quelle di fakevmc del simulatore."""
    vmc = VMCFinta("VMC Nord", "127.0.0.1")
    finte = VMCFinte([vmc], porta=0)
    await finte.avvia()
    try:
        porta = finte.porte["127.0.0.1"]
        assert await _chiedi(porta, "VMGH?") == vmc.stato.status_str()
        assert (await _chiedi(porta, "VMGH?")).startswith("VMGO,00001,")
        assert await _chiedi(porta, "VMGI?") == vmc.stato.sensori_str()
        assert await _chiedi(porta, "VMNM?") == "VMNM VMC Nord"
        assert await _chiedi(porta, "VMSL?") == risposta_lan("127.0.0.1")
        # comando di velocità con l'a capo (come nc): risposta subito, cambio dopo la latenza
        assert await _chiedi(porta, "VMWH0000003\n") == "OK"
        await asyncio.sleep(vmc.stato.latency + 0.2)
        assert (await _chiedi(porta, "VMGH?")).startswith("VMGO,00003,")
        assert [r for _t, r in vmc.richieste].count("VMGH?") == 3
    finally:
        await finte.ferma()


def test_home_assistant_carica_solo_custom_components_della_configurazione(
    tmp_path: Path,
) -> None:
    """Lanciato come lo lancia il banco (``-P``, cartella di lavoro = configurazione),
    un Python dalla radice del repository non vede il suo custom_components: dopo che
    Home Assistant toglie config_dir da sys.path, ``custom_components.__path__`` resta
    quello della configurazione (con la radice in sys.path diventava quello del
    repository e il banco provava il codice del repository al posto della beta)."""
    config = tmp_path / "config"
    (config / "custom_components" / "vmc_master").mkdir(parents=True)
    prova = (
        "import sys; sys.path.insert(0, sys.argv[1]); import custom_components as c; "
        "sys.path.remove(sys.argv[1]); print(list(c.__path__))"
    )
    for argomenti, cartella, attesa in (
        (["-P"], config, [str(config / "custom_components")]),
        ([], RADICE, [str(RADICE / "custom_components")]),
    ):
        uscita = subprocess.run(
            [sys.executable, *argomenti, "-c", prova, str(config)],
            cwd=cartella,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        assert json.loads(uscita.replace("'", '"')) == attesa
    sorgente = (BANCO / "ha.py").read_text("utf-8")
    assert '"-P",' in sorgente and "cwd=self.cartella," in sorgente


def test_risposta_lan_ha_i_campi_della_vmc_vera() -> None:
    """VMSL?: rete 32 + password 32 + IP 15 + porta 5 + gateway 15 + maschera 15 + modalità."""
    testo = risposta_lan("192.168.1.161")
    assert len(testo) == 32 + 32 + 15 + 5 + 15 + 15 + 1
    assert testo[64:79].strip() == "192.168.1.161"
    assert testo[84:99].strip() == "192.168.1.1"


# ------------------------------------------------------------ mappa dei nomi
def test_mappa_dei_nomi_della_fase_1() -> None:
    """Le chiavi lette dalla colonna «Domani» (tabelle.py): 172 impostazioni visibili,
    67 valori interni, 34 timer, 136 sensori per VMC."""
    assert len(controlli.VISIBILI) == 172
    assert len(controlli.INTERNI) == 67
    assert len(controlli.TIMER) == 34
    assert len(controlli.SENSORI) == 136
    assert controlli.nuovo_id("input_boolean.notifica_audio", "nord") == (
        "switch.vmc_nord_notifica_audio"
    )
    assert (
        controlli.nuovo_id("timer.lettura_nome", "sud") == "sensor.vmc_sud_lettura_nome"
    )
    assert controlli.vecchio_id("input_datetime.accensione_lunedi", "master") == (
        "input_datetime.vmc_master_accensione_lunedi"
    )


def test_vmc_di_riconosce_le_tre_vmc() -> None:
    assert controlli.vmc_di("sensor.vmc_nord_sensori") == "nord"
    assert controlli.vmc_di("automation.automazione_vmc_sud") == "sud"
    assert controlli.vmc_di("sensor.vmc_masterx_y") is None
    assert controlli.vmc_di("sensor.sonda_co2") is None


def test_doppioni_solo_con_l_originale() -> None:
    """«_2» è un doppione solo se l'entity_id senza il numero c'è (o è atteso)."""
    stati = [
        "sensor.vmc_master_sensori",
        "sensor.vmc_master_sensori_2",
        "switch.vmc_nord_notifica_audio_2",
        "sensor.vmc_sud_aria_scambiata_v2",
    ]
    assert controlli.doppioni(stati) == [
        "sensor.vmc_master_sensori_2",
        "switch.vmc_nord_notifica_audio_2",
    ]
    # la seconda fascia del Calendario si chiama «_2» di suo
    seconda_fascia = [
        "time.vmc_master_accensione_lunedi",
        "time.vmc_master_accensione_lunedi_2",
        "input_datetime.vmc_master_accensione_lunedi_2",
        "sensor.vmc_nord_status_accensione_vmc_tramite_calendario",
        "sensor.vmc_nord_status_accensione_vmc_tramite_calendario_2",
    ]
    assert controlli.doppioni(seconda_fascia) == []
    assert controlli.doppioni(["time.vmc_master_accensione_lunedi_2_2"]) == [
        "time.vmc_master_accensione_lunedi_2_2"
    ]


def test_uguali_come_valori_di_home_assistant() -> None:
    assert controlli.uguali("5.0", 5)
    assert controlli.uguali(True, "on")
    assert controlli.uguali("off", False)
    assert not controlli.uguali("5.0", "5.1")
    assert controlli.uguali("07:05:00", "07:05:00")
    assert not controlli.uguali("unknown", "")


def test_classe_timer() -> None:
    assert controlli.classe_timer(100.0, "active", 101.5) == "ripreso (stessa fine)"
    assert (
        controlli.classe_timer(100.0, "active", 160.0) == "ripartito (fine più tardi)"
    )
    assert controlli.classe_timer(100.0, "idle", None) == "fermo"
    assert controlli.classe_timer(100.0, "assente", None) == "assente"


def test_controllo_timer_come_dopo_un_riavvio_della_beta() -> None:
    """Un timer attivo prima: fermo dopo il riavvio di controllo, fermo dopo il passaggio
    -> passato; assente dopo il passaggio -> fallito."""
    chiave = controlli.TIMER[0]
    vecchi = {
        controlli.vecchio_id(k, n): "idle"
        for k in controlli.TIMER
        for n in controlli.NOMI
    }
    nuovi = {
        controlli.nuovo_id(k, n): "unknown"
        for k in controlli.TIMER
        for n in controlli.NOMI
    }
    attivo = controlli.vecchio_id(chiave, "master")

    def con_attivo(stati: dict[str, str]) -> dict:
        ist = _istantanea({**stati, attivo: "active"})
        ist["stati"][attivo]["attributes"]["finishes_at"] = "2026-11-26T10:00:00+00:00"
        return ist

    p0, r, p = con_attivo(vecchi), _istantanea(vecchi), con_attivo(vecchi)
    esito = controlli.controlla_timer(p0, r, p, _istantanea(nuovi))
    assert esito["esito"] == "passato", esito
    assert esito["conteggi"]["dopo il passaggio: fermo"] == 1
    del nuovi[controlli.nuovo_id(chiave, "sud")]
    esito = controlli.controlla_timer(p0, r, p, _istantanea(nuovi))
    assert esito["esito"] == "fallito"
    assert esito["conteggi"]["assenti dopo il passaggio"] == 1


def test_controllo_rinominate_vuole_anche_l_azione_dell_automazione() -> None:
    vecchi = [
        e
        for e in utente.ENTITA_PERSONALI
        if e.split(".")[0] not in controlli.DOMINI_SENSORI
    ]
    elenco = "\n".join(f"- lovelace:lovelace: `{e}` → `x`" for e in vecchi)
    a = _istantanea({}, servizi={"shell_command": []})
    a["riparazioni"] = [
        {
            "domain": "vmc_master",
            "issue_id": "impostazioni_rinominate",
            "translation_placeholders": {"elenco": elenco},
        }
    ]
    esito = controlli.controlla_rinominate(a, _istantanea({}))
    assert esito["esito"] == "fallito"
    assert esito["dettagli"] == [f"non elencato: {controlli.AZIONE_PERSONALE}"]
    a["riparazioni"][0]["translation_placeholders"]["elenco"] += (
        f"\n- automations.yaml: `{controlli.AZIONE_PERSONALE}` → `button.x`"
    )
    assert controlli.controlla_rinominate(a, _istantanea({}))["esito"] == "passato"


# --------------------------------------------------------- piano del «prima»
def test_impostazioni_prima_valide_per_gli_aiutanti_di_oggi() -> None:
    """Ogni valore scritto dalla scheda nella costruzione è valido per l'aiutante del
    package (limiti, passo, opzioni, formato dell'ora) e diverso dal predefinito."""
    imp = controlli.IMPOSTAZIONI
    for indice in range(3):
        for oggetto, valore in utente.numeri(indice).items():
            voce = imp[f"input_number.{oggetto}"]
            assert voce["min"] <= valore <= voce["max"], oggetto
            passi = (valore - voce["min"]) / voce["step"]
            assert abs(passi - round(passi)) < 1e-6, oggetto
            assert valore != voce.get("initial", voce["min"]), oggetto
        for oggetto, valore in utente.selezioni(indice).items():
            assert valore in imp[f"input_select.{oggetto}"]["options"], oggetto
        orari = utente.orari(indice)
        assert len(orari) == 30
        for oggetto, valore in orari.items():
            assert f"input_datetime.{oggetto}" in imp, oggetto
            assert re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d:00", valore), (
                oggetto,
                valore,
            )
        for oggetto in utente.INTERRUTTORI_INVERTITI[indice]:
            assert "initial" not in imp[f"input_boolean.{oggetto}"], oggetto
        for oggetto in utente.FINESTRE_APERTE[indice]:
            assert imp[f"input_boolean.{oggetto}"].get("initial") is False, oggetto
        for oggetto in utente.SENSORI_SCELTI[indice]:
            assert f"input_select.{oggetto}" in imp, oggetto


def test_valori_diversi_per_ogni_vmc() -> None:
    """Uno scambio fra due VMC si vede: nessun valore uguale per tutte e tre."""
    for piano in (utente.numeri, utente.selezioni, utente.orari):
        valori = [piano(i) for i in range(3)]
        for chiave in valori[0]:
            assert len({str(v[chiave]) for v in valori}) > 1, (piano.__name__, chiave)


def test_valori_diversi_da_quelli_dei_profili() -> None:
    """Il Profilo Inizializzazione scrive i suoi valori prima delle impostazioni della
    costruzione: un valore uguale a quello del profilo non direbbe se il passaggio l'ha
    portato o se un profilo l'ha riscritto."""
    for indice in range(3):
        scritti = {
            **{f"input_number.{k}": v for k, v in utente.numeri(indice).items()},
            **{f"input_select.{k}": v for k, v in utente.selezioni(indice).items()},
            **{f"input_datetime.{k}": v for k, v in utente.orari(indice).items()},
        }
        comuni = set(scritti) & set(utente.PREDEFINITI_DEI_PROFILI)
        assert len(comuni) == len(utente.PREDEFINITI_DEI_PROFILI)
        for chiave in comuni:
            assert not controlli.uguali(
                scritti[chiave], utente.PREDEFINITI_DEI_PROFILI[chiave]
            ), (indice, chiave)


def test_sensori_con_memoria_della_mappa() -> None:
    assert len(controlli.MEMORIE) == 10
    assert "sensor.status_ventola_memorizzata" in controlli.MEMORIE


def test_plancia_con_una_vista_per_vmc() -> None:
    voci = {"master": "a1", "nord": "b2", "sud": "c3"}
    plancia = utente.plancia_con_le_schede(voci)
    assert [v["path"] for v in plancia["views"]] == [
        "vmc-master",
        "vmc-nord",
        "vmc-sud",
        "personale",
    ]
    assert plancia["views"][1]["cards"] == [
        {"type": "custom:vmc-master-card", "vmc": "b2"}
    ]


# ------------------------------------------------------------- controlli
def _istantanea(stati: dict[str, str], ora: float = 1000.0, **altro) -> dict:
    return {
        "ora": ora,
        "stati": {
            e: {"entity_id": e, "state": s, "attributes": {}} for e, s in stati.items()
        },
        "registro": [],
        "riparazioni": [],
        "risorse": [],
        **altro,
    }


def _ferma(stati: dict[str, str], **altro) -> dict:
    return {
        "storage": {
            "core.restore_state": {
                "data": [
                    {"state": {"entity_id": e, "state": s, "attributes": {}}}
                    for e, s in stati.items()
                ]
            },
            **altro.pop("storage", {}),
        },
        **altro,
    }


def test_controllo_interni_testo_di_un_attesa() -> None:
    """input_text.countdown_‹attesa› con un testo dell'automazione delle attese (la beta
    lo riscrive dopo ogni riavvio, alla fase 2 del riallineamento) -> passato; con un
    altro testo -> diverso."""
    chiave = "input_text.countdown_blackout_ripristino"
    assert chiave in controlli.INTERNI
    testo = "Black-Out Velocità 2 terminato, ripristino"
    assert testo in controlli.TESTI_DELLE_ATTESE["blackout_ripristino"]
    valori = {k: "x" for k in controlli.INTERNI}
    stati = {
        controlli.vecchio_id(k, n): "x"
        for k in controlli.INTERNI
        for n in controlli.NOMI
    }
    stati[controlli.vecchio_id(chiave, "master")] = "unknown"

    def fa(scritto: str) -> dict:
        memorie = {
            f"vmc_master.memoria_interna.{n}": {
                "data": {
                    "valori": {**valori, chiave: scritto if n == "master" else "x"}
                }
            }
            for n in controlli.NOMI
        }
        return _ferma({}, storage=memorie)

    p0 = r = _istantanea({})
    esito = controlli.controlla_interni(p0, r, _ferma(stati), fa(testo))
    assert esito["esito"] == "passato", esito
    classe = "testo di un'attesa, riscritto dal motore come dalla beta dopo un riavvio"
    assert esito["conteggi"][classe] == 1
    esito = controlli.controlla_interni(p0, r, _ferma(stati), fa("un altro testo"))
    assert esito["esito"] == "fallito"
    assert esito["conteggi"]["diverso"] == 1


def test_controllo_impostazioni_classi() -> None:
    """Un valore portato, uno che cambia anche nel riavvio di controllo (initial), uno
    diverso e uno mancante."""
    chiavi = {
        "input_boolean.notifica_audio": "switch",
        "input_boolean.opzioni_vmc": "switch",
        "input_number.umidita_avvio": "number",
        "input_datetime.accensione_lunedi": "time",
    }
    prima = {
        "input_boolean.vmc_master_notifica_audio": "on",
        "input_boolean.vmc_master_opzioni_vmc": "on",
        "input_number.vmc_master_umidita_avvio": "72.5",
        "input_datetime.vmc_master_accensione_lunedi": "06:00:00",
    }
    dopo_riavvio = {**prima, "input_boolean.vmc_master_opzioni_vmc": "off"}
    dopo = {
        "switch.vmc_master_notifica_audio": "on",
        "switch.vmc_master_opzioni_vmc": "off",
        "number.vmc_master_umidita_avvio": "70.0",
    }
    salvati = controlli.VISIBILI
    try:
        controlli.VISIBILI = tuple(chiavi)
        controlli.NOMI = ("master",)
        esito = controlli.controlla_impostazioni(
            _istantanea(prima),
            _istantanea(dopo_riavvio),
            _istantanea(prima),
            _ferma(prima),
            _istantanea(dopo),
        )
    finally:
        controlli.VISIBILI = salvati
        controlli.NOMI = tuple(v.nome for v in utente.CASA)
    assert esito["esito"] == "fallito"
    assert esito["conteggi"]["portato"] == 1
    assert esito["conteggi"]["come dopo un riavvio della beta"] == 1
    assert esito["conteggi"]["diverso"] == 1
    assert esito["conteggi"]["manca"] == 1


def test_controllo_storico_states_meta() -> None:
    p = _istantanea({"sensor.vmc_master_sensori": "x", "sensor.vmc_nord_sensori": "y"})
    fp = {
        "registro_storico": {
            "states_meta": {
                "sensor.vmc_master_sensori": 7,
                "sensor.vmc_nord_sensori": 8,
            },
            "righe": {"7": {"righe": 10}, "8": {"righe": 4}},
        }
    }
    fa = {
        "registro_storico": {
            "states_meta": {
                "sensor.vmc_master_sensori": 7,
                "sensor.vmc_nord_sensori": 31,
                "sensor.vmc_nord_sensori_2": 32,
            },
            "righe": {"7": {"righe": 15}, "31": {"righe": 2}},
        }
    }
    esito = controlli.controlla_storico(fp, fa, p)
    assert esito["esito"] == "fallito"
    assert esito["conteggi"]["metadata_id riusati"] == 1
    assert esito["conteggi"]["metadata_id cambiati o persi"] == 1
    assert esito["conteggi"]["nuove righe states_meta con «_2»"] == 1


def test_controllo_file() -> None:
    fp = {
        "file": {
            "packages": {"vmc_helty_flow/master/vmc_master.yaml": {"md5": "a"}},
            "www": {},
        }
    }
    m = {
        "file": {
            "packages": dict(fp["file"]["packages"]),
            "www": {"x.js": {"md5": "b"}},
        }
    }
    fa = {"file": {"packages": {}, "vmc_master_backup": {}, "www": {}}}
    esiti = {c["nome"]: c for c in controlli.controlla_file(fp, m, fa)}
    assert esiti["niente più in /config/packages/vmc_helty_flow"]["esito"] == "passato"
    assert esiti["niente scritto in /config/vmc_master_backup"]["esito"] == "passato"
    primo = esiti[
        "primo avvio nativo senza scritture in /config/packages e /config/www"
    ]
    assert primo["esito"] == "fallito"
    assert primo["dettagli"] == ["nuovo: www/x.js"]


def test_rapporto_dice_il_primo_passo_mancante(tmp_path: Path) -> None:
    (tmp_path / "passaggio").mkdir()
    esito = {
        "passo": "passaggio",
        "secondi": 12.5,
        "primo_passo_mancante": "passo 3 del passaggio: nessuna riparazione",
        "controlli": [
            controlli.controllo("a", "passato", "spiega", {"n": 3}),
            controlli.non_eseguibile("b", "l'istantanea A_dopo"),
        ],
    }
    (tmp_path / "passaggio" / "esito.json").write_text(json.dumps(esito), "utf-8")
    testo = rapporto.scrivi(tmp_path).read_text("utf-8")
    assert (
        "**Primo passo mancante:** passo 3 del passaggio: nessuna riparazione." in testo
    )
    assert "| a | ✅ passato | n: 3 |" in testo
    assert "⏸ non eseguibile" in testo


# ---------------------------------------------------------- prova vera (slow)
def _scelta_slow(request: pytest.FixtureRequest) -> bool:
    return "slow" in (request.config.getoption("-m") or "") or bool(
        os.environ.get("VMC_BANCO_COPIA")
    )


@pytest.fixture(scope="module")
def uscita_banco(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return Path(os.environ.get("VMC_BANCO_USCITA") or tmp_path_factory.mktemp("copia"))


def _banco(
    uscita: Path, *passi: str, secondi: int = 600
) -> subprocess.CompletedProcess:
    if shutil.which("unshare") is None or not Path(PYTHON_HA).exists():
        pytest.skip("servono unshare e il Python di Home Assistant")
    return subprocess.run(
        [PYTHON_HA, str(BANCO / "banco.py"), *passi, "--uscita", str(uscita)],
        cwd=RADICE,
        capture_output=True,
        text=True,
        timeout=secondi,
        check=False,
    )


def _non_passati(uscita: Path, passo: str) -> list[str]:
    esito = json.loads((uscita / passo / "esito.json").read_text("utf-8"))
    righe = [f"errore: {esito['errore']}"] if esito.get("errore") else []
    if esito.get("primo_passo_mancante"):
        righe.append(f"PRIMO PASSO MANCANTE: {esito['primo_passo_mancante']}")
    righe += [
        f"{c['esito']}: {c['nome']} {c['conteggi']}"
        for c in esito.get("controlli", [])
        if c["esito"] not in ("passato", "informazione")
    ]
    return righe


@pytest.mark.slow
def test_costruisci_la_configurazione_prima(request, uscita_banco: Path) -> None:
    """La beta b41 con 3 VMC, scheda, impostazioni e storico (da 4 a 9 minuti: aspetta
    le prime statistiche brevi del registro)."""
    if not _scelta_slow(request):
        pytest.skip("prova lenta: pytest -m slow")
    esito = _banco(uscita_banco, "costruisci")
    assert esito.returncode == 0, esito.stdout[-3000:]
    assert (uscita_banco / "prima" / "config" / "home-assistant_v2.db").exists()


@pytest.mark.slow
def test_passaggio_dalla_beta(request, uscita_banco: Path) -> None:
    """Il passaggio come lo farà il proprietario: tutti i controlli passati (circa 8 minuti)."""
    if not _scelta_slow(request):
        pytest.skip("prova lenta: pytest -m slow")
    if not (uscita_banco / "prima" / "config").exists():
        _banco(uscita_banco, "costruisci")
    esito = _banco(uscita_banco, "passaggio")
    _banco(uscita_banco, "rapporto")
    assert esito.returncode == 0, "\n".join(_non_passati(uscita_banco, "passaggio"))


@pytest.mark.slow
def test_riavvio_senza_conferma(request, uscita_banco: Path) -> None:
    """Primo avvio nativo, riavvio senza confermare, poi conferma (circa 7 minuti)."""
    if not _scelta_slow(request):
        pytest.skip("prova lenta: pytest -m slow")
    if not (uscita_banco / "prima" / "config").exists():
        _banco(uscita_banco, "costruisci")
    esito = _banco(uscita_banco, "senza_conferma")
    _banco(uscita_banco, "rapporto")
    assert esito.returncode == 0, "\n".join(
        _non_passati(uscita_banco, "senza_conferma")
    )


@pytest.mark.slow
def test_vmc_eliminata_e_aggiunta_di_nuovo(request, uscita_banco: Path) -> None:
    """Dopo il passaggio la VMC «sud» eliminata e aggiunta di nuovo (circa 4 minuti)."""
    if not _scelta_slow(request):
        pytest.skip("prova lenta: pytest -m slow")
    if not (uscita_banco / "passaggio" / "config_dopo").exists():
        pytest.skip("serve il passo «passaggio» (test_passaggio_dalla_beta)")
    esito = _banco(uscita_banco, "riaggiungi")
    _banco(uscita_banco, "rapporto")
    assert esito.returncode == 0, "\n".join(_non_passati(uscita_banco, "riaggiungi"))
