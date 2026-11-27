"""Il package che la beta scriveva per ogni VMC in /config/packages/vmc_helty_flow/<nome>,
rifatto in memoria: nessun file si scrive.

Serve al passaggio dalla beta (riconoscere gli elementi del package, passaggio.py) e alle
prove e agli strumenti che confrontano la VMC nativa con il package. I file sono generati
da quelli della release 8.6.0 contenuti nella cartella «package» dell'integrazione, con
le stesse trasformazioni degli script Clona e Cambia IP (vedere trasforma.py).
L'automazione principale, che nella release 8.6.0 si incollava a mano, diventa il file
vmc_<nome>_automazione.yaml dello stesso package.
"""

from __future__ import annotations

from pathlib import Path

from .trasforma import (
    adatta_link_repository,
    adatta_versione,
    package_per_vmc,
    per_vmc,
    script_cambio_ip_per_vmc,
    script_cambio_nome_per_vmc,
)

_SORGENTI = Path(__file__).parent / "package"


def _leggi(percorso: Path) -> str:
    # newline="" mantiene CRLF e LF esattamente come nei file originali
    with open(percorso, encoding="utf-8", newline="") as file:
        return file.read()


def automazione_come_package(testo: str, nome: str) -> str:
    """L'automazione incollata a mano diventa un elemento della lista «automation:».

    Il testo resta identico: ogni riga e' solo spostata di 4 spazi a destra.
    L'id serve a Home Assistant per conservare le tracce (trace) dell'automazione.
    """
    a_capo = "\r\n" if "\r\n" in testo else "\n"
    righe = testo.splitlines(keepends=True)
    # Anche le righe di soli spazi vanno spostate: nei blocchi di testo (|, >) gli spazi contano
    corpo = "".join(r if r in ("\n", "\r\n") else "    " + r for r in righe)
    if not corpo.endswith(("\n", "\r\n")):
        corpo += a_capo
    return (
        f"# AUTOMAZIONE VMC {nome.upper()}: GENERATA DALL'INTEGRAZIONE VMC MASTER, NON MODIFICARE{a_capo}"
        f"automation:{a_capo}"
        f"  - id: automazione_vmc_{nome}{a_capo}"
        f"{corpo}"
    )


def genera_file(nome: str, ip: str, versione: str) -> dict[str, str]:
    """Contenuto di tutti i file del package della VMC indicata."""
    yaml_master = _leggi(_SORGENTI / "vmc_master.yaml")
    automazione = _leggi(_SORGENTI / "vmc_master_automazione.txt")
    # Gli script .sh vanno sempre scritti con fine riga LF (come dopo «rimuovi caratteri di ritorno»)
    script_ip = _leggi(_SORGENTI / "vmc_master_script_cambio_ip.sh").replace(
        "\r\n", "\n"
    )
    script_nome = _leggi(_SORGENTI / "vmc_master_script_cambio_nome.sh").replace(
        "\r\n", "\n"
    )
    return {
        f"vmc_{nome}.yaml": adatta_link_repository(
            adatta_versione(package_per_vmc(yaml_master, nome, ip), versione)
        ),
        f"vmc_{nome}_automazione.yaml": automazione_come_package(
            adatta_link_repository(per_vmc(automazione, nome, ip)), nome
        ),
        f"vmc_{nome}_script_cambio_ip.sh": script_cambio_ip_per_vmc(
            script_ip, nome, ip
        ),
        f"vmc_{nome}_script_cambio_nome.sh": script_cambio_nome_per_vmc(
            script_nome, nome, ip
        ),
    }
