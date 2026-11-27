"""Prova su una copia della configurazione: il passaggio dalla beta (b41) all'integrazione
nativa, fatto come lo farà il proprietario, su una casa di prova con 3 VMC.

Uso (dalla radice del repository, in primo piano; ogni passo sta sotto i 10 minuti):

    /home/user/hav/bin/python strumenti/copia_configurazione/banco.py <passi> \\
        [--uscita DIR] [--nativa RIF|CARTELLA] [--beta RIF|CARTELLA]

Passi (nell'ordine; ognuno riusa quello che i precedenti hanno lasciato in ``--uscita``):

- ``costruisci``: la configurazione «prima», come quella di un utente della beta: Home
  Assistant 2026.11 nuovo (onboarding), la b41 pubblicata (``custom_components/vmc_master``
  del commit 268bf6c, uguale alla release del Marketplace), 3 VMC aggiunte dal flusso di
  configurazione (``master``, ``nord``, ``sud``), ognuna con la sua VMC finta sulla porta
  5001, la scheda nella plancia, il Profilo Inizializzazione, molte impostazioni a valori
  non predefiniti, un po' di storico vero nel registro SQLite. Copia finale in
  ``<uscita>/prima/config``;
- ``passaggio``: su una copia di «prima»: avvio della beta, conti alla rovescia avviati
  dalla scheda, istantanea, riavvio di controllo (beta -> beta, per sapere cosa fa un
  riavvio qualunque), istantanea; poi il passaggio: codice nativo al posto di
  ``custom_components/vmc_master`` (con Home Assistant acceso, come un download dal
  Marketplace), riavvio, riparazione confermata, riavvio; istantanee, fotografie della
  scheda di ogni VMC (della beta dopo il riavvio di controllo, al primo avvio nativo
  prima della conferma e dopo il passaggio), controlli;
- ``senza_conferma``: come ``passaggio``, ma dopo il primo avvio nativo l'utente riavvia
  senza confermare la riparazione; poi conferma;
- ``riaggiungi``: dopo il passaggio, la VMC ``sud`` eliminata e aggiunta di nuovo;
- ``rapporto``: ``<uscita>/rapporto.md`` (in italiano) da tutti i risultati;
- ``tutto``: tutti i passi (più di 10 minuti: solo a mano);
- ``ricontrolla``: rifà i controlli dei passi già fatti dalle istantanee salvate, senza
  Home Assistant (per cambiare un controllo senza rifare il passo).

``--nativa``: il codice da provare, un riferimento git del repository principale (di
norma ``fase5-passaggio``) o una cartella ``custom_components/vmc_master``.

``--beta``: la beta installata da ``costruisci`` (di norma la b41, commit 268bf6c), un
riferimento git del repository principale o una cartella ``custom_components/vmc_master``
(per esempio quella della b42 pubblicata, estratta dal repository del Marketplace).

Il banco gira in uno spazio di rete suo (``rete.py``: si rilancia da solo con
``unshare -n``); Home Assistant è un processo vero per ogni avvio (``ha.py``). Ogni passo
scrive ``<uscita>/<passo>/esito.json``; il codice di uscita è 0 solo se tutti i controlli
del passo sono passati.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
import time
import traceback
from pathlib import Path
from typing import Any

QUI = Path(__file__).resolve().parent
RADICE = QUI.parents[1]
sys.path.insert(0, str(QUI))

import controlli
import istantanea
import rapporto
import rete
import utente
from ha import (
    BASE,
    CODICE_RIAVVIO,
    LIMITE_MEMORIA_MB,
    PAROLA,
    UTENTE,
    ClientHA,
    ErroreHA,
    ProcessoHA,
    attendi_avvio,
    memoria_mb,
    onboarding,
)
from vmc_finte import VMCFinta, VMCFinte

REPOSITORY = Path("/home/user/vmc-helty-flow-nativa")
COMMIT_BETA = "268bf6c"
"""«Base: VMC Master 9.0.0b41»: custom_components/vmc_master identico alla release b41
del Marketplace (origin/main di VMC-HELTY-FLOW-MARKETPLACE, e79387f)."""
USCITA = RADICE / "copia_configurazione"
NATIVA = "fase5-passaggio"
ASSESTAMENTO = 15
"""Secondi di attesa dopo che le entità delle VMC ci sono (automazioni dell'avvio)."""
SENTINELLA = "sensor.vmc_{nome}_status_ventola_lettura_codice_interpretato_interfaccia"
"""Un sensore di ogni VMC, uguale nella beta e nella nativa: c'è quando la VMC è avviata."""

SONDA_STATISTICHE = "sensor.sonda_co2"
"""Una sonda della casa con state_class: le sue statistiche dicono che il registro ha
compilato."""

REGISTRO_DEBUG = """
# banco: registro dell'integrazione in debug (ha.out del passo, tutti gli avvii)
logger:
  default: warning
  logs:
    custom_components.vmc_master: debug
"""

CONFIGURAZIONE_UTENTE = """
homeassistant:
  packages: !include_dir_named packages/

# Sonde della casa (sensori dell'utente, scelti nella finestra «Sensori Opzionati»)
template:
  - sensor:
      - name: Sonda Temperatura Esterna
        unique_id: sonda_temperatura_esterna
        unit_of_measurement: "°C"
        device_class: temperature
        state_class: measurement
        state: "{{ 8.4 }}"
      - name: Sonda Umidita Esterna
        unique_id: sonda_umidita_esterna
        unit_of_measurement: "%"
        device_class: humidity
        state_class: measurement
        state: "{{ 81 }}"
      - name: Sonda Temperatura Interna
        unique_id: sonda_temperatura_interna
        unit_of_measurement: "°C"
        device_class: temperature
        state_class: measurement
        state: "{{ 20.6 }}"
      - name: Sonda Umidita Interna
        unique_id: sonda_umidita_interna
        unit_of_measurement: "%"
        device_class: humidity
        state_class: measurement
        state: "{{ 55 }}"
      - name: Sonda CO2
        unique_id: sonda_co2
        unit_of_measurement: "ppm"
        device_class: carbon_dioxide
        state_class: measurement
        state: "{{ 640 }}"
"""


class Banco:
    """La casa di prova di un passo: cartella, VMC finte, Home Assistant, client."""

    def __init__(self, uscita: Path, passo: str) -> None:
        self.uscita = uscita
        self.cartella = uscita / passo
        self.config = self.cartella / "config"
        self.passi: list[dict[str, Any]] = []
        self.finte = VMCFinte([VMCFinta(v.nome_vmc, v.ip) for v in utente.CASA])
        self.processo: ProcessoHA | None = None
        self.client: ClientHA | None = None
        self.inizio = time.monotonic()

    # --- registro dei passi ----------------------------------------------------------
    def annota(self, cosa: str, **dettagli: Any) -> None:
        voce = {"t": round(time.monotonic() - self.inizio, 1), "cosa": cosa, **dettagli}
        processo = self.processo.processo if self.processo else None
        rss = (
            memoria_mb(processo.pid)
            if processo and processo.returncode is None
            else None
        )
        if rss is not None:
            voce["memoria_ha_mb"] = round(rss)
        self.passi.append(voce)
        memoria = f" ({rss:.0f} MB)" if rss is not None else ""
        print(f"[{voce['t']:7.1f}] {cosa}{memoria}", flush=True)

    # --- Home Assistant --------------------------------------------------------------
    async def prepara(self, gettone: str | None) -> None:
        rete.prepara_indirizzi([v.ip for v in utente.CASA])
        ping = rete.prepara_ping(self.cartella / "bin")
        await self.finte.avvia()
        self.processo = ProcessoHA(self.config, self.cartella / "ha.out", ping)
        self.processo.allarme = self._in_corsa
        self.client = ClientHA(gettone)

    async def _in_corsa(self, rss: float) -> None:
        """Memoria di Home Assistant oltre l'allarme: annota gli script e le automazioni
        che stanno girando (attributo ``current``), per sapere chi la fa crescere."""
        assert self.client is not None
        stati = [
            s
            for s in await self.client.stati()
            if s["entity_id"].split(".")[0] in ("script", "automation")
            and s["attributes"].get("current")
        ]
        in_corsa = {s["entity_id"]: s["attributes"]["current"] for s in stati}
        passi: dict[str, list[str]] = {}
        for s in stati:
            dominio, oggetto = s["entity_id"].split(".", 1)
            with contextlib.suppress(Exception):
                tracce = await self.client.ws_comando(
                    "trace/list",
                    domain=dominio,
                    item_id=s["attributes"].get("id", oggetto),
                )
                passi[s["entity_id"]] = [
                    str(traccia.get("last_step"))
                    for traccia in tracce
                    if traccia.get("state") == "running"
                ]
        self.annota(
            f"memoria di Home Assistant a {rss:.0f} MB, in corsa: "
            + (
                ", ".join(f"{e} ({n})" for e, n in sorted(in_corsa.items())) or "niente"
            ),
            in_corsa=in_corsa,
            ultimo_passo=passi,
        )
        for entita, ultimi in sorted(passi.items()):
            print(f"          {entita}: {ultimi}", flush=True)

    async def avvia(self, attese: bool = True) -> float:
        assert self.processo is not None and self.client is not None
        await self.processo.avvia()
        secondi = await attendi_avvio(self.processo, self.client)
        self.annota(
            "Home Assistant avviato",
            avvio=self.processo.avvii,
            secondi=round(secondi, 1),
        )
        if attese and self.client.gettone:
            await self.attendi_vmc()
        return secondi

    async def attendi_vmc(self, secondi: float = 90) -> dict[str, Any]:
        """Aspetta il sensore sentinella di ogni VMC (non sconosciuto), poi l'assestamento."""
        assert self.client is not None
        fine = time.monotonic() + secondi
        mancanti = [v.nome for v in utente.CASA]
        while time.monotonic() < fine and mancanti:
            stati = {s["entity_id"]: s["state"] for s in await self.client.stati()}
            mancanti = [
                v.nome
                for v in utente.CASA
                if stati.get(SENTINELLA.format(nome=v.nome))
                in (None, "unknown", "unavailable")
            ]
            if mancanti:
                await asyncio.sleep(1)
        await asyncio.sleep(ASSESTAMENTO)
        esito = {"vmc_senza_sentinella": mancanti}
        self.annota("VMC avviate", **esito)
        return esito

    async def riavvia(self, momento: str | None = None) -> None:
        """«Riavvia» dall'interfaccia: homeassistant.restart, poi il nuovo processo."""
        assert self.processo is not None and self.client is not None
        await self.client.scollega_ws()
        with contextlib.suppress(ErroreHA, OSError):
            await self.client.servizio("homeassistant", "restart")
        codice = await self.processo.attendi_uscita()
        self.annota("Home Assistant fermato per il riavvio", codice=codice)
        if momento:
            istantanea.salva(
                self.cartella,
                momento,
                istantanea.istantanea_ferma(self.config, momento),
            )
        await self.avvia()

    async def attendi_riavvio_da_solo(self, secondi: float = 20) -> bool:
        """True se Home Assistant esce da solo per un riavvio entro ``secondi``."""
        assert self.processo is not None and self.processo.processo is not None
        try:
            codice = await asyncio.wait_for(self.processo.processo.wait(), secondi)
        except TimeoutError:
            return False
        await self.processo.attendi_uscita(1)
        self.annota("Home Assistant uscito da solo", codice=codice)
        if codice != CODICE_RIAVVIO:
            raise ErroreHA(f"Home Assistant è uscito con il codice {codice}")
        return True

    async def ferma(self, momento: str | None = None) -> None:
        assert self.processo is not None
        if self.client is not None:
            await self.client.scollega_ws()
        codice = await self.processo.termina()
        self.annota("Home Assistant fermato", codice=codice)
        if momento:
            istantanea.salva(
                self.cartella,
                momento,
                istantanea.istantanea_ferma(self.config, momento),
            )

    async def istantanea(self, momento: str) -> dict[str, Any]:
        assert self.client is not None
        dati = await istantanea.istantanea_viva(self.client, momento)
        istantanea.salva(self.cartella, momento, dati)
        self.annota(f"istantanea {momento}", entita=len(dati["stati"]))
        return dati

    def errore(self, errore: BaseException) -> str:
        """Il testo dell'errore di un passo, con il codice di uscita di Home Assistant se
        il processo non c'è più (-9: ucciso, per esempio per mancanza di memoria)."""
        testo = f"{type(errore).__name__}: {errore}"
        processo = self.processo.processo if self.processo else None
        if self.processo is not None and self.processo.oltre_il_limite:
            testo = (
                "Home Assistant fermato dal banco: memoria oltre "
                f"{LIMITE_MEMORIA_MB} MB ({self.processo.oltre_il_limite}). {testo}"
            )
        elif processo is not None and (
            processo.returncode is not None or memoria_mb(processo.pid) is None
        ):
            codice = processo.returncode
            testo = (
                f"Home Assistant non è più acceso (codice di uscita {codice}"
                f"{': ucciso, per esempio dal kernel per mancanza di memoria' if codice in (None, -9) else ''}"
                f"). {testo}"
            )
        return testo

    async def chiudi(self) -> None:
        if self.client is not None:
            await self.client.chiudi()
        if self.processo is not None and self.processo.vivo:
            with contextlib.suppress(Exception):
                await self.processo.termina(60)
            self.processo.uccidi()
        await self.finte.ferma()

    def salva_esito(self, esito: dict[str, Any]) -> Path:
        esito = {
            **esito,
            "memoria_massima_ha_mb": round(self.processo.picco_mb)
            if self.processo
            else None,
            "passi": self.passi,
            "secondi": round(time.monotonic() - self.inizio, 1),
        }
        file = self.cartella / "esito.json"
        file.write_text(
            json.dumps(esito, ensure_ascii=False, indent=1, default=str), "utf-8"
        )
        return file


# ------------------------------------------------------------------------ codice
def estrai_codice(riferimento: str, destinazione: Path) -> dict[str, str]:
    """Mette ``custom_components/vmc_master`` di ``riferimento`` (commit o cartella) in
    ``destinazione``, come lo scrive un download dal Marketplace (cartella sostituita)."""
    sorgente = Path(riferimento)
    temporanea = destinazione.with_name(f".{destinazione.name}.nuova")
    shutil.rmtree(temporanea, ignore_errors=True)
    if sorgente.is_dir():
        shutil.copytree(
            sorgente, temporanea, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
        )
        descrizione = {"cartella": str(sorgente)}
        with contextlib.suppress(subprocess.CalledProcessError, FileNotFoundError):
            descrizione["commit"] = subprocess.run(
                ["git", "-C", str(sorgente), "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            descrizione["modifiche_non_registrate"] = subprocess.run(
                ["git", "-C", str(sorgente), "status", "--short", "."],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
    else:
        commit = subprocess.run(
            ["git", "-C", str(REPOSITORY), "rev-parse", riferimento],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        archivio = subprocess.run(
            [
                "git",
                "-C",
                str(REPOSITORY),
                "archive",
                commit,
                "custom_components/vmc_master",
            ],
            capture_output=True,
            check=True,
        ).stdout
        cartella_tar = temporanea.with_name(f".{destinazione.name}.tar")
        shutil.rmtree(cartella_tar, ignore_errors=True)
        with tarfile.open(fileobj=io.BytesIO(archivio)) as tar:
            tar.extractall(cartella_tar, filter="data")
        shutil.move(cartella_tar / "custom_components" / "vmc_master", temporanea)
        shutil.rmtree(cartella_tar)
        descrizione = {"riferimento": riferimento, "commit": commit}
    manifest = json.loads((temporanea / "manifest.json").read_text("utf-8"))
    descrizione["versione"] = manifest.get("version", "")
    shutil.rmtree(destinazione, ignore_errors=True)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporanea.rename(destinazione)
    return descrizione


# --------------------------------------------------------------------- costruisci
async def costruisci(uscita: Path, beta: str = COMMIT_BETA) -> int:
    banco = Banco(uscita, "costruzione")
    shutil.rmtree(banco.cartella, ignore_errors=True)
    banco.config.mkdir(parents=True)
    esito: dict[str, Any] = {"passo": "costruisci"}
    try:
        await banco.prepara(None)
        client = banco.client
        assert client is not None
        await banco.avvia(attese=False)
        gettone = await onboarding(client)
        (uscita / "gettone.txt").write_text(gettone, "utf-8")
        await client.ws_comando(
            "config/core/update",
            language="it",
            time_zone="Europe/Rome",
            country="IT",
            currency="EUR",
            unit_system="metric",
            latitude=45.07,
            longitude=7.69,
            elevation=240,
        )
        banco.annota("onboarding fatto")
        # Home Assistant risponde all'onboarding prima di finire l'avvio: fermato a quel
        # punto esce senza salvare (codice -15, nessun gestore di SIGTERM ancora) e il
        # gettone di lunga durata va perso. Si aspetta «RUNNING», col gettone.
        await attendi_avvio(banco.processo, client)
        # Installazione, passo 1: configuration.yaml (packages); le sonde della casa
        with (banco.config / "configuration.yaml").open("a", encoding="utf-8") as file:
            file.write(CONFIGURAZIONE_UTENTE)
        # Installazione, passo 2: il download dal Marketplace (b41)
        esito["beta"] = estrai_codice(
            beta, banco.config / "custom_components" / "vmc_master"
        )
        await banco.ferma()
        await banco.avvia(attese=False)
        voci: dict[str, str] = {}
        for vmc in utente.CASA:
            passi = await utente.aggiungi_vmc(client, vmc)
            banco.annota(f"VMC {vmc.nome} aggiunta", passi=[p.__dict__ for p in passi])
        for voce in await client.ws_comando("config_entries/get", domain="vmc_master"):
            voci[voce["title"].removeprefix("VMC ").lower()] = voce["entry_id"]
        esito["voci"] = voci
        # Installazione, passo 3: la riparazione «VMC Master: riavviare Home Assistant»
        problemi = [
            p
            for p in await utente.riparazioni(client)
            if p["domain"] == "vmc_master" and p["issue_id"] == "riavvio_necessario"
        ]
        if not problemi:
            raise ErroreHA("manca la riparazione «riavviare Home Assistant» della beta")
        await client.scollega_ws()
        with contextlib.suppress(ErroreHA, OSError):
            passi = await utente.segui_riparazione(
                client, "vmc_master", "riavvio_necessario"
            )
            banco.annota(
                "riparazione riavvio seguita", passi=[p.__dict__ for p in passi]
            )
        assert banco.processo is not None
        codice = await banco.processo.attendi_uscita()
        banco.annota("Home Assistant fermato dalla riparazione", codice=codice)
        await banco.avvia()
        # Installazione, passo 4: la scheda nella plancia
        risorse = await client.ws_comando("lovelace/resources")
        esito["risorse_dopo_installazione"] = risorse
        await client.ws_comando(
            "lovelace/config/save", config=utente.plancia_con_le_schede(voci)
        )
        await client.richiesta(
            "POST",
            f"/api/config/automation/config/{utente.AUTOMAZIONE_PERSONALE['id']}",
            utente.AUTOMAZIONE_PERSONALE,
        )
        banco.annota("scheda nella plancia e automazione personale")
        # Configurazione: Profilo Inizializzazione per ogni VMC, poi le impostazioni
        for vmc in utente.CASA:
            await utente.profilo_inizializzazione(client, vmc)
        await asyncio.sleep(14)
        banco.annota("Profilo Inizializzazione fatto")
        scritti: dict[str, Any] = {}
        for indice, vmc in enumerate(utente.CASA):
            await utente.scegli_velocita(client, vmc, utente.VELOCITA_SCELTA[indice])
            scritti |= await utente.imposta_vmc(client, vmc, indice)
            banco.annota(f"impostazioni di {vmc.nome}")
        esito["impostazioni_scritte"] = scritti
        banco.annota("impostazioni non predefinite", quante=len(scritti))
        # Storico: le sonde della VMC cambiano, letture e cambi di velocità dalla scheda
        for giro in range(4):
            for indice, vmc in enumerate(utente.CASA):
                finta = banco.finte.vmc[vmc.ip].stato
                finta.sens.update(
                    t_int=205 + 3 * giro + indice,
                    t_ext=90 - 4 * giro + 2 * indice,
                    rh=480 + 15 * giro + 10 * indice,
                    co2=620 + 40 * giro + 25 * indice,
                    voc=45 + 5 * giro,
                )
                await utente.tocca(
                    client,
                    "homeassistant",
                    "update_entity",
                    f"sensor.vmc_{vmc.nome}_sensori",
                )
            await asyncio.sleep(8)
            vmc = utente.CASA[giro % 3]
            velocita = (utente.VELOCITA_SCELTA[giro % 3] + giro) % 4
            await utente.scegli_velocita(client, vmc, velocita)
            await asyncio.sleep(8)
            banco.annota(f"storico, giro {giro + 1}: {vmc.nome} a velocità {velocita}")
        for indice, vmc in enumerate(utente.CASA):
            await utente.scegli_velocita(client, vmc, utente.VELOCITA_SCELTA[indice])
        await asyncio.sleep(10)
        banco.annota("storico")
        await _attendi_statistiche(banco)
        await banco.istantanea("costruzione_fine")
        await banco.ferma("costruzione_fine_ferma")
        prima = uscita / "prima"
        shutil.rmtree(prima, ignore_errors=True)
        shutil.copytree(banco.config, prima / "config", symlinks=True)
        (prima / "voci.json").write_text(json.dumps(voci, indent=1), "utf-8")
        esito["ok"] = True
    except Exception as errore:  # noqa: BLE001 - il banco scrive sempre il suo esito
        esito["ok"] = False
        esito["errore"] = banco.errore(errore)
        esito["traccia"] = traceback.format_exc()
        print(esito["traccia"], flush=True)
    finally:
        await banco.chiudi()
        banco.salva_esito(esito)
    return 0 if esito.get("ok") else 1


async def _attendi_statistiche(banco: Banco, secondi: float = 330) -> None:
    """Aspetta le prime statistiche brevi (il registro le compila ogni 5 minuti, ai
    minuti :00, :05...): senza, il controllo delle statistiche dopo il passaggio non
    avrebbe niente da confrontare."""
    assert banco.client is not None
    inizio = time.time() - 3600
    fine = time.monotonic() + secondi
    while time.monotonic() < fine:
        risposta = await banco.client.ws_comando(
            "recorder/statistics_during_period",
            start_time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(inizio)),
            statistic_ids=[SONDA_STATISTICHE],
            period="5minute",
            types=["mean"],
        )
        if risposta.get(SONDA_STATISTICHE):
            banco.annota("statistiche brevi compilate")
            return
        await asyncio.sleep(10)
    raise ErroreHA(f"nessuna statistica breve di {SONDA_STATISTICHE} in {secondi} s")


# ---------------------------------------------------------------- passaggio
def _copia_prima(uscita: Path, banco: Banco) -> dict[str, str]:
    prima = uscita / "prima"
    if not (prima / "config").exists():
        raise ErroreHA(
            f"manca la configurazione «prima» ({prima}): lanciare «costruisci»"
        )
    shutil.rmtree(banco.cartella, ignore_errors=True)
    banco.cartella.mkdir(parents=True)
    shutil.copytree(prima / "config", banco.config, symlinks=True)
    configurazione = banco.config / "configuration.yaml"
    configurazione.write_text(
        configurazione.read_text("utf-8") + REGISTRO_DEBUG, "utf-8"
    )
    return json.loads((prima / "voci.json").read_text("utf-8"))


async def _conti_alla_rovescia(banco: Banco) -> None:
    assert banco.client is not None
    for indice, vmc in enumerate(utente.CASA):
        await utente.avvia_conti_alla_rovescia(banco.client, vmc, indice)
    await asyncio.sleep(3)


async def _riparazioni_del_passaggio(banco: Banco) -> list[dict[str, Any]]:
    """Le riparazioni di VMC Master da confermare per il passaggio: quelle che si possono
    «riparare», tranne il riavvio chiesto dalla beta."""
    assert banco.client is not None
    return [
        p
        for p in await utente.riparazioni(banco.client)
        if p["domain"] == "vmc_master"
        and p.get("is_fixable")
        and p["issue_id"] != "riavvio_necessario"
        and not p.get("dismissed_version")
    ]


async def _primo_avvio_nativo(
    banco: Banco, nativa: str, esito: dict[str, Any], fotografie: bool = True
) -> None:
    """Il passaggio fino al primo avvio con il codice nativo (riparazione non ancora
    confermata)."""
    await banco.avvia()
    await _conti_alla_rovescia(banco)
    await banco.istantanea("P0_prima")
    await banco.riavvia("F0_fermata_controllo")
    await banco.istantanea("R_riavvio_di_controllo")
    if fotografie:
        esito["fotografie_beta"] = await _fotografie(
            banco, esito["voci_prima"], "fotografie_beta"
        )
    await _conti_alla_rovescia(banco)
    await banco.istantanea("P_prima_del_passaggio")
    esito["nativa"] = estrai_codice(
        nativa, banco.config / "custom_components" / "vmc_master"
    )
    banco.annota("codice nativo al posto della beta", **esito["nativa"])
    await banco.riavvia("FP_fermata_beta")
    await banco.istantanea("M_primo_avvio_nativo")
    istantanea.salva(
        banco.cartella, "M_file", istantanea.istantanea_file(banco.config, "M_file")
    )
    if fotografie:
        esito["fotografie_in_attesa"] = await _fotografie(
            banco, esito["voci_prima"], "fotografie_in_attesa"
        )


async def _conferma(banco: Banco, esito: dict[str, Any], momento: str) -> bool:
    """Conferma le riparazioni del passaggio e riavvia; False se non ce ne sono."""
    assert banco.client is not None
    da_confermare = await _riparazioni_del_passaggio(banco)
    esito["riparazioni_da_confermare"] = da_confermare
    if not da_confermare:
        esito["primo_passo_mancante"] = (
            "passo 3 del passaggio: dopo il primo avvio con il codice nativo non c'è "
            "nessuna riparazione di VMC Master da confermare"
        )
        banco.annota("NESSUNA riparazione da confermare")
        return False
    seguite = []
    for problema in da_confermare:
        await banco.client.scollega_ws()
        passi = await utente.segui_riparazione(
            banco.client, "vmc_master", problema["issue_id"]
        )
        seguite.append(
            {"issue_id": problema["issue_id"], "passi": [p.__dict__ for p in passi]}
        )
        banco.annota(f"riparazione {problema['issue_id']} confermata")
    esito["riparazioni_seguite"] = seguite
    if await banco.attendi_riavvio_da_solo():
        istantanea.salva(
            banco.cartella,
            f"F{momento}",
            istantanea.istantanea_ferma(banco.config, f"F{momento}"),
        )
        await banco.avvia()
        esito["riavvio_dopo_la_conferma"] = "da solo"
    else:
        await banco.riavvia(f"F{momento}")
        esito["riavvio_dopo_la_conferma"] = "dall'utente"
    return True


async def _fotografie(
    banco: Banco, voci: dict[str, str], nome: str
) -> list[dict[str, Any]]:
    cartella = banco.cartella / nome
    cartella.mkdir(parents=True, exist_ok=True)
    viste = [f"vmc-{n}" for n in voci] + ["personale"]
    processo = await asyncio.create_subprocess_exec(
        "node",
        str(QUI / "scatta.js"),
        BASE,
        UTENTE,
        PAROLA,
        str(cartella),
        *viste,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**__import__("os").environ, "NODE_PATH": "/opt/node-tools/node_modules"},
    )
    uscita, errori = await asyncio.wait_for(processo.communicate(), 300)
    risultati = []
    for riga in uscita.decode().splitlines():
        with contextlib.suppress(ValueError):
            risultati.append(json.loads(riga))
    if processo.returncode:
        risultati.append({"errore": errori.decode()[-2000:]})
    for risultato in risultati:
        if "pezzi" in risultato:
            risultato["immagine"] = str(
                rapporto.unisci_pezzi(cartella, risultato["vista"], risultato["pezzi"])
            )
    banco.annota(f"fotografie {nome}", viste=len(risultati))
    return risultati


async def passaggio(uscita: Path, nativa: str, senza_conferma: bool = False) -> int:
    nome_passo = "senza_conferma" if senza_conferma else "passaggio"
    banco = Banco(uscita, nome_passo)
    esito: dict[str, Any] = {"passo": nome_passo}
    try:
        voci = esito["voci_prima"] = _copia_prima(uscita, banco)
        await banco.prepara((uscita / "gettone.txt").read_text("utf-8"))
        # le fotografie della beta e di prima della conferma solo nel passaggio (il passo
        # senza conferma resta sotto i 10 minuti)
        await _primo_avvio_nativo(banco, nativa, esito, fotografie=not senza_conferma)
        if senza_conferma:
            await banco.riavvia("FS_fermata_senza_conferma")
            await banco.istantanea("S_riavvio_senza_conferma")
        if await _conferma(banco, esito, "C_fermata_dopo_conferma"):
            await banco.istantanea("A_dopo")
            esito["fotografie"] = await _fotografie(banco, voci, "fotografie")
        await banco.ferma("FA_fermata_finale")
        shutil.rmtree(banco.cartella / "config_dopo", ignore_errors=True)
        shutil.copytree(banco.config, banco.cartella / "config_dopo", symlinks=True)
        esito["voci"] = voci
    except Exception as errore:  # noqa: BLE001 - il banco scrive sempre il suo esito
        esito["errore"] = banco.errore(errore)
        esito["traccia"] = traceback.format_exc()
        print(esito["traccia"], flush=True)
    finally:
        await banco.chiudi()
    esito["controlli"] = controlli.controlla_passaggio(banco.cartella, esito)
    banco.salva_esito(esito)
    return (
        0
        if controlli.tutti_passati(esito["controlli"]) and "errore" not in esito
        else 1
    )


# ---------------------------------------------------------------- riaggiungi
async def riaggiungi(uscita: Path) -> int:
    banco = Banco(uscita, "riaggiungi")
    esito: dict[str, Any] = {"passo": "riaggiungi"}
    try:
        dopo = uscita / "passaggio" / "config_dopo"
        esito_passaggio = istantanea.leggi(uscita / "passaggio", "esito") or {}
        if esito_passaggio.get("primo_passo_mancante") or esito_passaggio.get("errore"):
            raise ErroreHA(
                "il passaggio non è arrivato in fondo (vedi il passo «passaggio»): "
                "niente da eliminare e aggiungere di nuovo"
            )
        if not dopo.exists():
            raise ErroreHA(
                "manca la configurazione dopo il passaggio: lanciare «passaggio»"
            )
        shutil.rmtree(banco.cartella, ignore_errors=True)
        banco.cartella.mkdir(parents=True)
        shutil.copytree(dopo, banco.config, symlinks=True)
        voci = json.loads((uscita / "prima" / "voci.json").read_text("utf-8"))
        await banco.prepara((uscita / "gettone.txt").read_text("utf-8"))
        client = banco.client
        assert client is not None
        await banco.avvia()
        await banco.istantanea("A0_prima_di_eliminare")
        vmc = utente.CASA[2]
        risposta = await client.richiesta(
            "DELETE", f"/api/config/config_entries/entry/{voci[vmc.nome]}"
        )
        esito["eliminazione"] = risposta
        banco.annota(f"VMC {vmc.nome} eliminata", risposta=risposta)
        await asyncio.sleep(5)
        await banco.istantanea("E_eliminata")
        if (risposta or {}).get("require_restart"):
            await banco.riavvia("FE_fermata_dopo_eliminazione")
            await banco.istantanea("E2_eliminata_dopo_riavvio")
        passi = await utente.aggiungi_vmc(client, vmc)
        esito["aggiunta"] = [p.__dict__ for p in passi]
        banco.annota(f"VMC {vmc.nome} aggiunta di nuovo")
        await asyncio.sleep(10)
        riavvii = [
            p
            for p in await utente.riparazioni(client)
            if p["domain"] == "vmc_master" and p.get("is_fixable")
        ]
        esito["riparazioni_dopo_aggiunta"] = riavvii
        if riavvii:
            await banco.riavvia("FZ_fermata_dopo_aggiunta")
        else:
            await banco.attendi_vmc()
        await banco.istantanea("Z_riaggiunta")
        nuove = {
            v["title"].removeprefix("VMC ").lower(): v["entry_id"]
            for v in await client.ws_comando("config_entries/get", domain="vmc_master")
        }
        esito["voci_nuove"] = nuove
        esito["fotografie"] = await _fotografie(banco, nuove, "fotografie")
        await banco.ferma("FZ_fermata_finale")
        esito["voci"] = voci
    except Exception as errore:  # noqa: BLE001
        esito["errore"] = banco.errore(errore)
        esito["traccia"] = traceback.format_exc()
        print(esito["traccia"], flush=True)
    finally:
        await banco.chiudi()
    esito["controlli"] = controlli.controlla_riaggiunta(banco.cartella, esito)
    banco.salva_esito(esito)
    return (
        0
        if controlli.tutti_passati(esito["controlli"]) and "errore" not in esito
        else 1
    )


# ---------------------------------------------------------------- ricontrolla
def ricontrolla(uscita: Path) -> int:
    """I controlli rifatti dalle istantanee già salvate di ogni passo fatto."""
    codice = 0
    for passo, controlla in (
        ("passaggio", controlli.controlla_passaggio),
        ("senza_conferma", controlli.controlla_passaggio),
        ("riaggiungi", controlli.controlla_riaggiunta),
    ):
        cartella = uscita / passo
        esito = istantanea.leggi(cartella, "esito")
        if esito is None:
            continue
        esito["controlli"] = controlla(cartella, esito)
        (cartella / "esito.json").write_text(
            json.dumps(esito, ensure_ascii=False, indent=1, default=str), "utf-8"
        )
        ok = controlli.tutti_passati(esito["controlli"]) and "errore" not in esito
        print(f"{passo}: {'passato' if ok else 'non passato'}")
        codice |= 0 if ok else 1
    return codice


# ---------------------------------------------------------------------- main
PASSI = ("costruisci", "passaggio", "senza_conferma", "riaggiungi", "rapporto")
SENZA_HA = ("rapporto", "ricontrolla")


async def principale(argomenti: argparse.Namespace) -> int:
    uscita = Path(argomenti.uscita).resolve()
    uscita.mkdir(parents=True, exist_ok=True)
    passi = list(PASSI) if "tutto" in argomenti.passi else argomenti.passi
    codice = 0
    for passo in passi:
        if passo == "costruisci":
            codice |= await costruisci(uscita, argomenti.beta)
        elif passo == "passaggio":
            codice |= await passaggio(uscita, argomenti.nativa)
        elif passo == "senza_conferma":
            codice |= await passaggio(uscita, argomenti.nativa, senza_conferma=True)
        elif passo == "riaggiungi":
            codice |= await riaggiungi(uscita)
        elif passo == "ricontrolla":
            codice |= ricontrolla(uscita)
        elif passo == "rapporto":
            print(rapporto.scrivi(uscita))
    return codice


def main() -> int:
    analizzatore = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    analizzatore.add_argument(
        "passi", nargs="+", choices=(*PASSI, "ricontrolla", "tutto")
    )
    analizzatore.add_argument("--uscita", default=str(USCITA))
    analizzatore.add_argument("--nativa", default=NATIVA)
    analizzatore.add_argument("--beta", default=COMMIT_BETA)
    argomenti = analizzatore.parse_args()
    if not set(argomenti.passi) <= set(SENZA_HA) and not rete.nello_spazio_del_banco():
        return rete.rilancia_nello_spazio_del_banco()
    return asyncio.run(principale(argomenti))


if __name__ == "__main__":
    sys.exit(main())
