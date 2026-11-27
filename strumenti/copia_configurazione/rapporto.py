"""Il rapporto del banco in italiano (``<uscita>/rapporto.md``) e le fotografie intere.

Il rapporto si legge dall'alto: per ogni passo l'esito, il primo passo mancante (se c'è),
la tabella dei controlli con i conteggi esatti, poi i dettagli di ogni controllo non
passato. Le fotografie della scheda (una per VMC) sono accanto, in ``<passo>/fotografie``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TITOLI = {
    "costruzione": "Costruzione della configurazione «prima» (beta b41, 3 VMC)",
    "passaggio": "Passaggio dalla beta alla nativa, con la riparazione confermata",
    "senza_conferma": "Passaggio con un riavvio prima di confermare la riparazione",
    "riaggiungi": "Dopo il passaggio: VMC «sud» eliminata e aggiunta di nuovo",
}
SIMBOLI = {
    "passato": "✅ passato",
    "fallito": "❌ fallito",
    "non eseguibile": "⏸ non eseguibile",
    "informazione": "ℹ️ informazione",
}


def unisci_pezzi(cartella: Path, vista: str, pezzi: int) -> Path:
    """Rimette insieme i pezzi della fotografia di una vista in ``<vista>.png``."""
    from PIL import Image

    immagini = [Image.open(cartella / f"{vista}.{i}.png") for i in range(pezzi)]
    larghezza = max(i.width for i in immagini)
    altezza = sum(i.height for i in immagini)
    intera = Image.new("RGB", (larghezza, altezza), "white")
    y = 0
    for immagine in immagini:
        intera.paste(immagine, (0, y))
        y += immagine.height
        immagine.close()
    file = cartella / f"{vista}.png"
    intera.save(file, optimize=True)
    for i in range(pezzi):
        (cartella / f"{vista}.{i}.png").unlink()
    return file


def _valore(v: Any) -> str:
    if isinstance(v, bool):
        return "sì" if v else "no"
    return str(v)


def _passo(uscita: Path, nome: str) -> list[str]:
    file = uscita / nome / "esito.json"
    if not file.exists():
        return [f"## {TITOLI[nome]}", "", "Passo non eseguito.", ""]
    esito = json.loads(file.read_text("utf-8"))
    righe = [f"## {TITOLI[nome]}", ""]
    righe.append(f"Durata: {esito.get('secondi', '?')} s.")
    if "nativa" in esito:
        n = esito["nativa"]
        righe.append(
            "Codice nativo provato: "
            + ", ".join(f"{k} `{v}`" for k, v in n.items() if v)
            + "."
        )
    if esito.get("errore"):
        righe += ["", f"**Errore:** `{esito['errore']}`"]
    if esito.get("primo_passo_mancante"):
        righe += ["", f"**Primo passo mancante:** {esito['primo_passo_mancante']}."]
    controlli = esito.get("controlli")
    if nome == "costruzione":
        righe += _costruzione(esito)
    if controlli:
        conti: dict[str, int] = {}
        for c in controlli:
            conti[c["esito"]] = conti.get(c["esito"], 0) + 1
        righe += [
            "",
            "Controlli: "
            + ", ".join(f"{SIMBOLI[k]} {v}" for k, v in sorted(conti.items()))
            + ".",
            "",
            "| Controllo | Esito | Conteggi |",
            "|---|---|---|",
        ]
        for c in controlli:
            conteggi = "; ".join(f"{k}: {_valore(v)}" for k, v in c["conteggi"].items())
            righe.append(
                f"| {c['nome']} | {SIMBOLI[c['esito']]} | {conteggi or c['spiegazione']} |"
            )
        for c in controlli:
            if c["esito"] == "passato" and not c["dettagli"]:
                continue
            righe += ["", f"### {c['nome']}", "", c["spiegazione"], ""]
            if c["dettagli"]:
                righe.append(
                    "<details><summary>Dettagli ({})</summary>\n".format(
                        len(c["dettagli"])
                    )
                )
                righe += [f"- {_testo(d)}" for d in c["dettagli"][:200]]
                if len(c["dettagli"]) > 200:
                    righe.append(f"- … altri {len(c['dettagli']) - 200}")
                righe.append("\n</details>")
    foto = [f for f in esito.get("fotografie") or [] if f.get("immagine")]
    if foto:
        righe += ["", "Fotografie della plancia:", ""]
        righe += [
            f"- `{Path(f['immagine']).relative_to(uscita)}` ({f['altezza']} px)"
            for f in foto
        ]
    righe.append("")
    return righe


def _testo(d: Any) -> str:
    if isinstance(d, str):
        return d.replace("|", "\\|")
    return "`" + json.dumps(d, ensure_ascii=False)[:600] + "`"


def _costruzione(esito: dict[str, Any]) -> list[str]:
    righe = [""]
    righe.append(f"Esito: {'✅ costruita' if esito.get('ok') else '❌ non costruita'}.")
    if esito.get("beta"):
        righe.append(
            f"Beta installata: commit `{esito['beta'].get('commit')}`, versione `{esito['beta'].get('versione')}`."
        )
    if esito.get("voci"):
        righe.append("VMC: " + ", ".join(f"`{n}`" for n in esito["voci"]) + ".")
    if esito.get("impostazioni_scritte"):
        righe.append(
            f"Impostazioni scritte dalla scheda a valori non predefiniti: {len(esito['impostazioni_scritte'])}."
        )
    return righe


def scrivi(uscita: Path) -> Path:
    righe = [
        "# Prova su una copia della configurazione",
        "",
        (
            "Banco: `strumenti/copia_configurazione/banco.py`. Casa di prova con Home "
            "Assistant 2026.11 vero, 3 VMC finte sulla porta 5001 (`master`, `nord`, "
            "`sud`), la beta b41 pubblicata, poi il passaggio all'integrazione nativa come "
            "lo farà il proprietario."
        ),
        "",
    ]
    for nome in TITOLI:
        righe += _passo(uscita, nome)
    file = uscita / "rapporto.md"
    file.write_text("\n".join(righe), "utf-8")
    return file
