"""I comandi di shell del package come comandi del motore: stessi pacchetti per la VMC.

- I 13 comandi ``printf '<comando>\\n' | timeout 5 nc -w 3 IP 5001`` girano davvero con
  ``sh`` e un ``nc`` finto che annota i byte ricevuti; il client del motore
  (``ClientVMC.comanda``) manda gli stessi byte a una VMC finta in TCP.
- Il cambio del nome e il cambio dell'IP: i file .sh del package girano davvero con bash
  su molti testi; il motore (``nome_valido``, ``ip_valido`` e ``ComandiVMC``) decide come
  loro se e cosa mandare alla VMC, e il nome valido arriva alla VMC con gli stessi byte
  di ``echo "VMNM <nome>" | nc``.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pytest
from homeassistant.core import Context, HomeAssistant

from custom_components.vmc_master.nativa.client import ClientVMC
from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.definizioni import (
    COMANDO_NOME,
    COMANDO_VMC,
    Comando,
)
from custom_components.vmc_master.nativa.motore.esecuzione import Modello
from custom_components.vmc_master.nativa.motore.interni import (
    ComandiVMC,
    ip_valido,
    nome_valido,
)

from ..test_client import VmcFinta
from .traduci import PACKAGE, _comando, leggi_comandi

NOMI = [
    "Cucina", "1234567890", "12345678901", "a", "", " ", "con spazio", "Àrea", "ñ",
    "a-b_c", "-n", "-e", "--", "a\tb", "a;b", "a$b", "`id`", "$(id)", "x'y", "*",
    "a*", "?", "[a]", "Z9", "_", "abc\n", "UPPER", "lower12", "a.b", "a/b",
]  # fmt: skip
INDIRIZZI = [
    "192.168.1.50", "10.0.0.300", "127.0.0.1", "", "169.254.1.1", "0.1.2.3", "224.0.0.1",
    "192.168.01.5", "8.8.8.8", "169.253.0.1", "169.255.0.1", "223.255.255.255",
    "255.255.255.255", "1.2.3", "1.2.3.4.5", "1.2.3.4 ", "a.b.c.d", "001.2.3.4",
    "1.2.3.04", "250.250.250.250", "256.1.1.1", "1.1.1.256", "09.1.1.1", "9.9.9.9",
    "126.255.255.255", "128.0.0.0", "1.2.3.4\n5.6.7.8", "1..2.3", "100.100.100.100",
]  # fmt: skip


class Shell:
    """Comandi e file .sh veri con un ``nc`` finto che annota i byte ricevuti."""

    def __init__(self, cartella: Path) -> None:
        self.cartella = cartella
        nc = cartella / "nc"
        nc.write_text('#!/bin/sh\ncat >> "$NC_USCITA"\n', encoding="utf-8")
        nc.chmod(0o755)
        self.uscita = cartella / "uscita_nc"
        self.ambiente = {
            "PATH": f"{cartella}:{os.environ['PATH']}",
            "NC_USCITA": str(self.uscita),
        }

    def esegui(self, argomenti: list[str]) -> tuple[int, bytes]:
        self.uscita.write_bytes(b"")
        esito = subprocess.run(
            argomenti, env=self.ambiente, capture_output=True, check=False, timeout=30
        )
        return esito.returncode, self.uscita.read_bytes()


@pytest.fixture
def shell(tmp_path: Path) -> Shell:
    return Shell(tmp_path)


@pytest.fixture
async def vmc() -> AsyncIterator[VmcFinta]:
    """Una VMC finta in TCP su 127.0.0.1 (quella di test_client.py)."""
    finta = VmcFinta()
    finta.porta = await finta.avvia()  # type: ignore[attr-defined]
    yield finta
    await finta.ferma()


@pytest.mark.usefixtures("socket_enabled")
async def test_comandi_vmc_stessi_byte(shell: Shell, vmc: VmcFinta) -> None:
    """I 13 comandi per la VMC: i byte di printf | nc sono quelli del client."""
    comandi = {
        nome: riga
        for nome, riga in leggi_comandi().items()
        if _comando(riga)[0] == COMANDO_VMC
    }
    assert len(comandi) == 13
    client = ClientVMC("127.0.0.1", vmc.porta)
    for riga in comandi.values():
        codice, ricevuto = shell.esegui(["sh", "-c", riga])
        assert codice == 0
        vmc.ricevuti.clear()
        await client.comanda(_comando(riga)[1])
        assert vmc.ricevuti == [ricevuto]


def _cambio_nome(shell: Shell, valore: str) -> tuple[int, bytes]:
    """Il cambio del nome come lo fa oggi shell_command: la riga del package con il
    modello reso (il nome da inserire senza virgolette e senza barre rovesciate),
    divisa con shlex.split, e il file .sh vero."""
    riga = leggi_comandi()["vmc_master_cambia_nome"]
    _, argomenti = riga.split(" ", 1)
    pulito = valore.replace('"', "").replace("\\", "")
    reso = argomenti.replace(
        "{{ states('input_text.vmc_master_nome_da_inserire') "
        "| replace('\"', '') | replace('\\\\', '') }}",
        pulito,
    ).strip()
    parti = shlex.split(reso)
    file = shell.cartella / "cambio_nome.sh"
    shutil.copy(PACKAGE / "vmc_master_script_cambio_nome.sh", file)
    return shell.esegui(["bash", str(file), *parti[1:]])


@pytest.mark.usefixtures("socket_enabled")
@pytest.mark.parametrize("valore", NOMI)
async def test_cambio_nome_come_il_file_sh(
    shell: Shell, vmc: VmcFinta, valore: str
) -> None:
    """Il motore manda il nome alla VMC quando lo manda il file .sh, con gli stessi
    byte; altrimenti nulla (il file .sh esce con 1)."""
    codice, ricevuto = _cambio_nome(shell, valore)
    pulito = valore.replace('"', "").replace("\\", "")
    nuovo = nome_valido(shlex.split(f'"{pulito}"'))
    if nuovo is None:
        assert (codice, ricevuto) == (1, b"")
        return
    assert codice == 0
    await ClientVMC("127.0.0.1", vmc.porta).comanda(f"VMNM {nuovo}")
    assert vmc.ricevuti == [ricevuto]


def _cambio_ip(shell: Shell, argomenti: list[str]) -> str | None:
    """Il file .sh vero dell'IP sui file di una cartella di prova: l'indirizzo scritto,
    o None se non ha cambiato nulla."""
    testo = (PACKAGE / "vmc_master_script_cambio_ip.sh").read_text("utf-8")
    cartella_package = "/config/packages/vmc_helty_flow/master/"
    yaml = shell.cartella / "vmc.yaml"
    nome = shell.cartella / "nome.sh"
    testo = testo.replace(cartella_package + "vmc_master.yaml", str(yaml)).replace(
        cartella_package + "vmc_master_script_cambio_nome.sh", str(nome)
    )
    file = shell.cartella / "cambio_ip.sh"
    file.write_text(testo, encoding="utf-8")
    yaml.write_text("host: 10.9.8.7\n", encoding="utf-8")
    nome.write_text("nc -w 3 10.9.8.7 5001\n", encoding="utf-8")
    codice, _ = shell.esegui(["bash", str(file), *argomenti])
    scritto = yaml.read_text("utf-8")
    if scritto == "host: 10.9.8.7\n":
        assert codice != 0
        return None
    assert codice == 0
    assert nome.read_text("utf-8") == scritto.replace("host: ", "nc -w 3 ").replace(
        "\n", " 5001\n"
    )
    return scritto.removeprefix("host: ").strip()


@pytest.mark.parametrize("valore", INDIRIZZI)
def test_cambio_ip_come_il_file_sh(shell: Shell, valore: str) -> None:
    """Il motore accetta un indirizzo quando lo accetta il file .sh (argomenti divisi
    come li divide shell_command)."""
    reso = f"/percorso/cambio_ip.sh   {valore}".strip()
    argomenti = shlex.split(reso)[1:]
    assert ip_valido(argomenti) == _cambio_ip(shell, argomenti)


def test_cambio_ip_con_piu_argomenti(shell: Shell) -> None:
    assert ip_valido(["1.2.3.4", "5.6.7.8"]) is None
    assert _cambio_ip(shell, ["1.2.3.4", "5.6.7.8"]) is None
    assert ip_valido([]) is None
    assert _cambio_ip(shell, []) is None


async def test_comandi_errori_e_risposta(hass: HomeAssistant) -> None:
    """Un comando non ricevuto dalla VMC si annota (come nc che esce con 1) e la
    risposta, se chiesta, ha la forma di quella di shell_command; senza collegamento
    con la VMC il comando è un errore."""
    c = Contesto(hass)
    inviati: list[str] = []

    async def invia(testo: str) -> str:
        inviati.append(testo)
        if testo == "VMWH0000002":
            raise TimeoutError
        return "OK\n"

    def modello(c: Any, V: Any) -> str:
        return str(V.get("nome", ""))

    comandi = ComandiVMC(
        c,
        [
            Comando(nome="uno", tipo=COMANDO_VMC, testo="VMWH0000001"),
            Comando(nome="due", tipo=COMANDO_VMC, testo="VMWH0000002"),
            Comando(nome="nome", tipo=COMANDO_NOME, argomenti=Modello(modello)),
            Comando(nome="strano", tipo="altro"),
        ],
        invia=invia,
    )
    contesto = Context()
    assert await comandi.esegui("uno", {}, {}, contesto, risposta=True) == {
        "stdout": "OK",
        "stderr": "",
        "returncode": 0,
    }
    assert await comandi.esegui("due", {}, {}, contesto) is None
    assert await comandi.esegui("due", {}, {}, contesto, risposta=True) == {
        "stdout": "",
        "stderr": "",
        "returncode": 1,
    }
    assert await comandi.esegui("nome", {"nome": "no no"}, {}, contesto) is None
    assert await comandi.esegui("nome", {}, {"nome": "Si"}, contesto) is None
    assert inviati == ["VMWH0000001", "VMWH0000002", "VMWH0000002", "VMNM Si"]
    with pytest.raises(Exception, match="tipo sconosciuto"):
        await comandi.esegui("strano", {}, {}, contesto)
    senza = ComandiVMC(c, [Comando(nome="uno", tipo=COMANDO_VMC, testo="X")])
    with pytest.raises(Exception, match="nessun collegamento"):
        await senza.esegui("uno", {}, {}, contesto)
