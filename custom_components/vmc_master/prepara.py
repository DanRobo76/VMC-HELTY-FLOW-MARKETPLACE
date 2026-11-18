"""Prepara i package delle VMC prima del riavvio che segue un aggiornamento.

Home Assistant legge i package all'avvio, prima che l'integrazione li aggiorni: se la
nuova versione cambia parti che non si ricaricano (shell_command, sensori TCP, recorder)
servirebbe un secondo riavvio. Per evitarlo, quando Home Assistant si ferma la versione
in esecuzione controlla se su disco c'e' una versione nuova dell'integrazione (scaricata
dall'aggiornamento) e, in un processo separato, fa scrivere i package a questa funzione
della versione NUOVA. All'avvio i file sono gia' quelli giusti: basta un solo riavvio.

Questo modulo non importa Home Assistant: deve girare da solo, con i soli moduli puri
dell'integrazione (installatore, trasforma, const). Il contratto con le versioni
precedenti e' la riga di comando di ``main``: non va cambiato.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .installatore import (
    FILE_MARCATORE,
    _leggi,
    cartella_vmc,
    genera_file,
    installa,
    ip_nel_package,
    leggi_marcatore,
    modificato_a_mano,
)


def da_preparare(config_dir: str, nome: str, ip: str, versione: str) -> bool:
    """True solo nel caso semplice: package scritto dall'integrazione, versione diversa,
    stesso IP, nessun file modificato a mano. Ogni altro caso (prima installazione,
    installazione manuale, IP cambiato dalla scheda, file modificati) resta all'avvio,
    che lo segnala all'utente come sempre."""
    cartella = cartella_vmc(config_dir, nome)
    if not (cartella / FILE_MARCATORE).is_file():
        return False
    marcatore = leggi_marcatore(config_dir, nome)
    md5 = marcatore.get("md5")
    if (
        marcatore.get("in_corso")
        or not isinstance(md5, dict)
        or marcatore.get("versione") == versione
        or marcatore.get("ip") != ip
        or ip_nel_package(config_dir, nome) != ip
    ):
        return False
    for nome_file in genera_file(nome, ip, versione):
        percorso = cartella / nome_file
        if not percorso.is_file():
            continue
        if modificato_a_mano(_leggi(percorso), md5.get(nome_file), ip, marcatore.get("ip")):
            return False
    return True


def prepara(config_dir: str, voci: list[list[str]], versione: str) -> list[str]:
    """Scrive i package delle VMC (nome, ip) con questa versione; restituisce i nomi."""
    preparate: list[str] = []
    for nome, ip in voci:
        if da_preparare(config_dir, nome, ip, versione):
            installa(config_dir, nome, ip, versione)
            preparate.append(nome)
    return preparate


def main(argomenti: list[str]) -> int:
    """argomenti: config_dir, JSON [[nome, ip], ...]. La versione e' quella del manifest
    della cartella da cui gira questo modulo."""
    config_dir, voci = argomenti[0], json.loads(argomenti[1])
    manifest = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
    print(json.dumps(prepara(config_dir, voci, str(manifest["version"]))))
    return 0


if __name__ == "__main__":  # pragma: no cover - si avvia con il programma di __init__.py
    sys.exit(main(sys.argv[1:]))
