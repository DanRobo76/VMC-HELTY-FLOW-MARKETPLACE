"""Genera l'elenco dei nomi che cambiano nella versione nativa.

Scrive, da ``tabelle.DOMANI`` e dalla colonna «Domani» della fase 1
(``tests/nativa/motore/aiutanti_fase1.csv``), che devono dire la stessa cosa:

- ``NOMI_NATIVI.md``, la pagina con l'elenco completo per ogni VMC (‹nome› al posto del nome
  della VMC): impostazioni che cambiano dominio, timer che diventano sensori con l'ora di
  fine, script e comandi che diventano pulsanti, voci che diventano interne
  all'integrazione;
- dalla 9.0.0b45 i due README non hanno più il riepilogo (la sezione «Passaggio dalla beta»
  è stata tolta): l'elenco resta solo in questa pagina, aperta da «Ulteriori informazioni»
  della riparazione del passaggio dalla beta.

Il test test_elenco_nomi.py controlla che la pagina sia uguale a quella che il programma
scrive e che nei README non sia rimasto un riepilogo. ``voci()`` dà le stesse voci a chi le vuole usare altrove (per esempio
il testo di una riparazione: ``Voce.per_vmc``).

Uso (dalla cartella del repository):
    /home/user/hat/bin/python -m tests.nativa.genera_elenco_nomi
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from custom_components.vmc_master.nativa.tabelle import DOMANI, IMPOSTAZIONI, PULSANTI

from .confronto import RADICE

FASE_1 = RADICE / "tests" / "nativa" / "motore" / "aiutanti_fase1.csv"
PAGINA = RADICE / "NOMI_NATIVI.md"
README = (RADICE / "README.md", RADICE / ".github" / "README.md")
URL_PAGINA = (
    "https://github.com/DanRobo76/VMC-HELTY-FLOW-MASTER/blob/main/NOMI_NATIVI.md"
)
INTERNA = "interna"
# La colonna «Entità oggi» della fase 1 è quella della VMC master
NOME_FASE_1 = "master"
SEGNAPOSTO = "‹nome›"
INIZIO = "<!-- inizio riepilogo dei nomi (generato da tests/nativa/genera_elenco_nomi.py) -->"
FINE = "<!-- fine riepilogo dei nomi -->"
_AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
)


@dataclass(frozen=True)
class Voce:
    """Una voce del package di oggi: ``chiave`` come in tabelle.py (es.
    «input_boolean.opzioni_vmc»), ``domani`` il dominio della versione nativa o «interna»,
    ``nome`` il nome visibile con {nome}/{Nome}/{NOME} al posto del nome della VMC."""

    chiave: str
    domani: str
    nome: str

    @property
    def dominio(self) -> str:
        return self.chiave.split(".", 1)[0]

    @property
    def oggetto(self) -> str:
        return self.chiave.split(".", 1)[1]

    @property
    def interna(self) -> bool:
        return self.domani == INTERNA

    def oggi_per_vmc(self, nome: str) -> str:
        """L'entity_id di oggi della VMC ``nome``."""
        return f"{self.dominio}.vmc_{nome}_{self.oggetto}"

    def domani_per_vmc(self, nome: str) -> str | None:
        """L'entity_id nativo della VMC ``nome`` (None: non è più un'entità)."""
        return None if self.interna else f"{self.domani}.vmc_{nome}_{self.oggetto}"

    def per_vmc(self, nome: str) -> tuple[str, str | None]:
        """(entity_id di oggi, entity_id nativo o None) della VMC ``nome``."""
        return self.oggi_per_vmc(nome), self.domani_per_vmc(nome)

    @property
    def oggi(self) -> str:
        return self.oggi_per_vmc(SEGNAPOSTO)

    @property
    def nativa(self) -> str | None:
        return self.domani_per_vmc(SEGNAPOSTO)

    @property
    def nome_visibile(self) -> str:
        testo = self.nome
        for segno in ("{nome}", "{Nome}", "{NOME}"):
            testo = testo.replace(segno, SEGNAPOSTO)
        return testo


def _segnaposto(testo: str) -> str:
    """Il nome della VMC master dentro un nome della fase 1 diventa {nome}/{Nome}/{NOME},
    come in genera_tabelle.py."""
    return (
        testo.replace(NOME_FASE_1, "{nome}")
        .replace(NOME_FASE_1.capitalize(), "{Nome}")
        .replace(NOME_FASE_1.upper(), "{NOME}")
    )


def _nome(chiave: str, domani: str, nome_fase_1: str) -> str:
    """Il nome visibile: quello degli aiutanti e dei pulsanti in tabelle.py, altrimenti
    quello della fase 1 (script e comandi interni; i comandi di shell non ne hanno)."""
    if chiave in IMPOSTAZIONI:
        return IMPOSTAZIONI[chiave]["name"].strip()
    if domani == "button":
        return PULSANTI[f"button.{chiave.split('.', 1)[1]}"]["nome"]
    return _segnaposto(nome_fase_1.strip())


def voci() -> list[Voce]:
    """Le 342 voci del package nell'ordine della fase 1, con il dominio di domani.

    Ferma con ValueError se la colonna «Domani» della fase 1 e tabelle.DOMANI non dicono la
    stessa cosa (dominio e oggetto dopo il punto) o non hanno le stesse voci."""
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        righe = list(csv.DictReader(flusso, delimiter=";"))
    uscita: list[Voce] = []
    for riga in righe:
        dominio, entita = riga["Entità oggi"].split(".", 1)
        if dominio != riga["Tipo oggi"] or not entita.startswith(f"vmc_{NOME_FASE_1}_"):
            raise ValueError(f"{riga['Entità oggi']}: tipo o nome non validi")
        oggetto = entita.removeprefix(f"vmc_{NOME_FASE_1}_")
        chiave = f"{dominio}.{oggetto}"
        colonna = riga["Domani"]
        domani = INTERNA if colonna.startswith(INTERNA) else colonna.split(".", 1)[0]
        if DOMANI.get(chiave) != domani:
            raise ValueError(
                f"{chiave}: fase 1 {colonna!r}, tabelle.DOMANI {DOMANI.get(chiave)!r}"
            )
        if domani != INTERNA and colonna != f"{domani}.vmc_{NOME_FASE_1}_{oggetto}":
            raise ValueError(f"{chiave}: domani cambia anche l'oggetto ({colonna})")
        uscita.append(Voce(chiave, domani, _nome(chiave, domani, riga["Nome"])))
    chiavi = [v.chiave for v in uscita]
    if len(set(chiavi)) != len(chiavi) or set(chiavi) != set(DOMANI):
        raise ValueError("la fase 1 e tabelle.DOMANI non hanno le stesse voci")
    return uscita


# ------------------------------------------------------------------------------- gruppi
@dataclass(frozen=True)
class Gruppo:
    """Un gruppo dell'elenco, con i titoli in italiano e in inglese."""

    titolo: str
    title: str
    voci: tuple[Voce, ...]


def gruppi(tutte: list[Voce] | None = None) -> list[Gruppo]:
    """I 4 gruppi dell'elenco: impostazioni, timer, pulsanti, voci interne."""
    tutte = voci() if tutte is None else tutte

    def scegli(prova) -> tuple[Voce, ...]:
        return tuple(
            sorted(
                (v for v in tutte if prova(v)),
                key=lambda v: (v.dominio, v.domani, v.oggetto),
            )
        )

    return [
        Gruppo(
            "Impostazioni che cambiano dominio",
            "Settings that change domain",
            scegli(lambda v: v.dominio in _AIUTANTI and not v.interna),
        ),
        Gruppo(
            "Timer che diventano sensori con l'ora di fine",
            "Timers that become end-time sensors",
            scegli(lambda v: v.dominio == "timer"),
        ),
        Gruppo(
            "Script e comandi che diventano pulsanti",
            "Scripts and commands that become buttons",
            scegli(lambda v: v.domani == "button"),
        ),
        Gruppo(
            "Voci che diventano interne all'integrazione (non più entità)",
            "Items that become internal to the integration (no longer entities)",
            scegli(lambda v: v.interna),
        ),
    ]


def _coppie(gruppo: Gruppo) -> list[tuple[tuple[str, str], list[Voce]]]:
    """Le voci del gruppo divise per dominio di oggi e di domani, nell'ordine del gruppo."""
    uscita: dict[tuple[str, str], list[Voce]] = {}
    for voce in gruppo.voci:
        uscita.setdefault((voce.dominio, voce.domani), []).append(voce)
    return list(uscita.items())


def _cella(testo: str) -> str:
    return testo.replace("|", "\\|") if testo else "–"


# ------------------------------------------------------------------------------- pagina
def pagina() -> str:
    """Il testo di NOMI_NATIVI.md."""
    elenco = gruppi()
    righe = [
        "# VMC Master: nomi cambiati / Changed names",
        "",
        "<!-- File generato da tests/nativa/genera_elenco_nomi.py: non modificarlo a mano. -->",
        "",
        (
            f"🇮🇹 Nomi che cambiano nella versione nativa, uguali per ogni VMC. {SEGNAPOSTO} è il"
            " nome della VMC (per la prima VMC: `master`). Cambia solo la parte prima del punto."
        ),
        "",
        (
            f"🇺🇸 Names that change in the native version, the same for every unit. {SEGNAPOSTO}"
            " is the unit's name (for the first unit: `master`). Only the part before the dot"
            " changes."
        ),
        "",
        "| Gruppo / Group | Voci / Items |",
        "|---|---|",
    ]
    righe += [f"| {g.titolo} / {g.title} | {len(g.voci)} |" for g in elenco]
    for numero, gruppo in enumerate(elenco, 1):
        interne = gruppo.voci[0].interna
        righe += [
            "",
            f"## {numero}. {gruppo.titolo} / {gruppo.title} ({len(gruppo.voci)})",
        ]
        for (dominio, domani), voci_coppia in _coppie(gruppo):
            arrivo = "–" if interne else f"`{domani}`"
            righe += ["", f"### `{dominio}` → {arrivo} ({len(voci_coppia)})", ""]
            if interne:
                righe += ["| Oggi / Today | Nome / Name |", "|---|---|"]
                righe += [
                    f"| `{v.oggi}` | {_cella(v.nome_visibile)} |" for v in voci_coppia
                ]
            else:
                righe += [
                    "| Oggi / Today | Versione nativa / Native | Nome / Name |",
                    "|---|---|---|",
                ]
                righe += [
                    f"| `{v.oggi}` | `{v.nativa}` | {_cella(v.nome_visibile)} |"
                    for v in voci_coppia
                ]
    return "\n".join(righe) + "\n"


# ----------------------------------------------------------------------------- riepilogo
def riepiloghi_nel_testo(testo: str) -> list[str]:
    """I riepiloghi di un README, segni compresi, nell'ordine in cui compaiono."""
    trovati: list[str] = []
    resto = testo
    while INIZIO in resto:
        _prima, dopo = resto.split(INIZIO, 1)
        if FINE not in dopo:
            raise ValueError("riepilogo dei nomi senza il segno di fine")
        dentro, resto = dopo.split(FINE, 1)
        trovati.append(INIZIO + dentro + FINE)
    return trovati


def conteggi() -> Counter[tuple[str, str]]:
    """Quante voci per (dominio di oggi, dominio di domani)."""
    return Counter((v.dominio, v.domani) for v in voci())


def scrivi() -> list[Path]:
    PAGINA.write_text(pagina(), encoding="utf-8")
    return [PAGINA]


if __name__ == "__main__":
    for percorso in scrivi():
        print(percorso)
