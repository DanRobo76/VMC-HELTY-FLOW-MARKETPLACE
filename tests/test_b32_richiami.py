"""Prova della 9.0.0b32: TUTTI i commenti «[CONFIGURAZIONE, n] [INTERFACCIA, n] [AUTOMAZIONE, n]» di vmc_master.yaml
corrispondono ai richiami reali (regola dell'intestazione, la stessa di tests/test_b30._conta_configurazione):
- CONFIGURAZIONE: occorrenze in vmc_master.yaml; la riga di definizione conta 1 (se non contiene gia' l'id, come
  default_entity_id), non si contano le righe di commento ne' la sezione recorder:;
- INTERFACCIA: occorrenze nella scheda; AUTOMAZIONE: occorrenze nell'automazione.
Un'occorrenza e' l'entity_id completo non seguito da [A-Za-z0-9_]."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

from homeassistant.util import slugify

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
RICHIAMI = re.compile(
    r"\[CONFIGURAZIONE, (\d+) (RICHIAM[OI])\] \[INTERFACCIA, (\d+) (RICHIAM[OI])\] \[AUTOMAZIONE, (\d+) (RICHIAM[OI])\]"
)
HELPER = ("input_text", "input_select", "input_number", "input_boolean", "input_datetime", "timer", "script",
          "shell_command", "counter")


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _conta(entita: str, testo: str) -> int:
    """Occorrenze di entita non seguite da [A-Za-z0-9_] (piu' veloce di una regex per 500 entita')."""
    n, i = 0, testo.find(entita)
    while i != -1:
        dopo = testo[i + len(entita) : i + len(entita) + 1]
        if not (dopo.isascii() and (dopo.isalnum() or dopo == "_")):
            n += 1
        i = testo.find(entita, i + 1)
    return n


def _entita(righe: list[str]) -> Iterator[tuple[int, str, tuple[int, int, int], tuple[str, str, str]]]:
    sezione = sotto = None
    for i, riga in enumerate(righe):
        primo = re.match(r"^([a-z_]+):", riga)
        if primo:
            sezione = primo.group(1)
        if sezione in ("command_line", "template"):
            m = re.match(r"^  - ([a-z_]+):\s*$", riga)
            if m:
                sotto = m.group(1)
        m = RICHIAMI.search(riga)
        if not m or riga.lstrip().startswith("#"):
            continue
        numeri = (int(m.group(1)), int(m.group(3)), int(m.group(5)))
        parole = (m.group(2), m.group(4), m.group(6))
        definita = re.search(r"default_entity_id: ([a-z_]+\.[a-z0-9_]+)", riga)
        if definita:
            entita = definita.group(1)
        elif sezione == "command_line":
            entita = f"{sotto}." + re.match(r"^\s+name: ([a-z0-9_]+)", riga).group(1)
        elif sezione == "sensor":
            entita = "sensor." + re.match(r"^\s+name: ([a-z0-9_]+)", riga).group(1)
        elif sezione == "automation":
            # l'entity_id di un'automazione viene dall'alias (riga successiva), non dall'id
            entita = "automation." + slugify(re.match(r'^    alias: "(.+)"', righe[i + 1]).group(1))
        else:
            assert sezione in HELPER, (i + 1, sezione)
            entita = f"{sezione}." + re.match(r"^  ([a-z0-9_]+):", riga).group(1)
        yield i, entita, numeri, parole


def test_tutti_i_richiami() -> None:
    righe = _testo("vmc_master.yaml").split("\n")
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    automazione = _testo("vmc_master_automazione.txt")
    # righe contate per CONFIGURAZIONE: niente commenti, niente sezione recorder
    contate, recorder = [], False
    for riga in righe:
        if riga.startswith("recorder:"):
            recorder = True
            continue
        if recorder and riga[:1] not in ("", " ", "#"):
            recorder = False
        if recorder or riga.lstrip().startswith("#"):
            continue
        contate.append(riga.split("#", 1)[0])
    configurazione = "\n".join(contate)

    controllate, sbagliate = 0, []
    for i, entita, numeri, parole in _entita(righe):
        definizione = 0 if _conta(entita, righe[i].split("#", 1)[0]) else 1
        reali = (_conta(entita, configurazione) + definizione, _conta(entita, scheda), _conta(entita, automazione))
        controllate += 1
        if reali != numeri:
            sbagliate.append((i + 1, entita, numeri, reali))
        # singolare per 1, plurale altrimenti
        assert parole == tuple("RICHIAMO" if n == 1 else "RICHIAMI" for n in numeri), (i + 1, entita)
    assert controllate > 500
    assert not sbagliate, sbagliate
