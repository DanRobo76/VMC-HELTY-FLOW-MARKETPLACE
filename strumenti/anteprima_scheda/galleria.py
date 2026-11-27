"""Galleria dell'anteprima per il proprietario (fase 4).

Dalle fotografie di ``banco.py`` (``anteprima/scene``) e da ``anteprima/risultati.json``:

- per ogni scena un JPEG con la scheda di oggi a sinistra e quella nativa a destra, largo al
  massimo 1400 px; le scene più alte di 4000 px sono divise in parti;
- per ogni scena dove si vedono testi aggiornati un JPEG in più con i ritagli intorno a ogni
  testo (oggi a sinistra, nativa a destra) e, sopra ogni ritaglio, il testo di prima e quello
  nuovo;
- ``index.json`` con i file, il titolo della scena, i pixel diversi e i testi aggiornati che
  si vedono.

Tutto in ``anteprima/galleria`` (fuori da git).

/home/user/hav/bin/python strumenti/anteprima_scheda/galleria.py
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None  # le schede aperte sono alte decine di migliaia di pixel

RADICE = Path(__file__).resolve().parents[2]
ANTEPRIMA = RADICE / "anteprima"
SCENE_DIR = ANTEPRIMA / "scene"
GALLERIA = ANTEPRIMA / "galleria"
CARATTERI = Path("/usr/share/fonts/truetype/dejavu")

LARGHEZZA_MASSIMA = 1400
ALTEZZA_MASSIMA = 4000
QUALITA = 80
MARGINE = 16
SPAZIO = 24
# Larghezza di ogni scheda: nelle scene intere 1 px per px CSS (le foto, a 2 px per px CSS,
# sono larghe 960), 0,75 px nella scena altissima di Informazioni (tutta aperta è alta 41000
# px CSS: a 1 px la galleria supererebbe i 12 MB), nei ritagli un po' più grande
LATO_SCENA = 480
LATO_SCENA_ALTA = 360
ALTA = 40000  # px della foto
LATO_RITAGLIO = 520
ATTORNO = 80  # px (della foto) sopra e sotto ogni testo nei ritagli
SFONDO = (236, 236, 236)
INTESTAZIONE = 64
BYTE_MASSIMI = 12_000_000
# Perché le due schede di queste scene non sono identiche
NOTE = {
    "14_pulisci_cronologia": (
        "Oggi l'elenco mostra le 50 entità registrate dal Recorder (le altre 425 sono "
        "escluse dal file vmc_master.yaml), la scheda nativa tutte le 355 entità della VMC "
        "con la tabella per tipo; più le etichette dei tipi aggiornate."
    ),
    "17_informazioni": (
        "Solo i testi aggiornati: dove un testo nuovo occupa meno righe tutto quello che "
        "segue sale (la foto nativa è più corta di 44 px), e quei pixel contano come "
        "diversi."
    ),
}


def carattere(dimensione: int, grassetto: bool = False) -> ImageFont.FreeTypeFont:
    nome = "DejaVuSans-Bold.ttf" if grassetto else "DejaVuSans.ttf"
    return ImageFont.truetype(str(CARATTERI / nome), dimensione)


def piano(testo: str) -> str:
    """Il testo senza tag HTML e senza gli apici delle etichette."""
    testo = re.sub(r"<[^>]+>", "", testo)
    return testo[1:-1] if len(testo) > 1 and testo[0] == testo[-1] == "'" else testo


def intestazione(larghezza: int, lato: int, titolo: str, nota: str) -> Image.Image:
    tela = Image.new("RGB", (larghezza, INTESTAZIONE), "white")
    disegno = ImageDraw.Draw(tela)
    disegno.text((MARGINE, 8), titolo, fill=(20, 20, 20), font=carattere(20, True))
    piccolo = carattere(14)
    larghezza_nota = disegno.textlength(nota, font=piccolo)
    disegno.text(
        (larghezza - MARGINE - larghezza_nota, 13),
        nota,
        fill=(90, 90, 90),
        font=piccolo,
    )
    colonne = carattere(15, True)
    disegno.text((MARGINE, 40), "Oggi", fill=(60, 60, 60), font=colonne)
    disegno.text(
        (MARGINE + lato + SPAZIO, 40), "Nativa", fill=(60, 60, 60), font=colonne
    )
    return tela


def affianca(
    oggi: Image.Image | None, nativa: Image.Image | None, lato: int
) -> Image.Image:
    """Due pezzi (già in scala) uno accanto all'altro; quello che manca resta grigio."""
    altezza = max(i.height for i in (oggi, nativa) if i is not None)
    tela = Image.new("RGB", (2 * MARGINE + 2 * lato + SPAZIO, altezza), "white")
    for x, pezzo in ((MARGINE, oggi), (MARGINE + lato + SPAZIO, nativa)):
        tela.paste(SFONDO, (x, 0, x + lato, altezza))
        if pezzo is not None:
            tela.paste(pezzo, (x, 0))
    return tela


def in_scala(
    foto: Image.Image, sopra: int, sotto: int, lato: int
) -> Image.Image | None:
    """Le righe [sopra, sotto) della foto, larghe ``lato``."""
    sopra, sotto = max(sopra, 0), min(sotto, foto.height)
    if sotto <= sopra:
        return None
    pezzo = foto.crop((0, sopra, foto.width, sotto))
    altezza = max(round(pezzo.height * lato / foto.width), 1)
    return pezzo.resize((lato, altezza), Image.LANCZOS)


def salva(tela: Image.Image, nome: str) -> str:
    assert tela.width <= LARGHEZZA_MASSIMA, (nome, tela.width)
    tela.save(GALLERIA / nome, "JPEG", quality=QUALITA, optimize=True, progressive=True)
    return nome


def scena_intera(nome: str, esito: dict[str, Any]) -> tuple[list[str], float]:
    """La scena affiancata, in parti alte al massimo ALTEZZA_MASSIMA; con la scala (px
    dell'immagine per px CSS)."""
    oggi = Image.open(SCENE_DIR / f"{nome}_oggi.png").convert("RGB")
    nativa = Image.open(SCENE_DIR / f"{nome}_nativa.png").convert("RGB")
    righe = max(oggi.height, nativa.height)
    lato = LATO_SCENA_ALTA if righe > ALTA else LATO_SCENA
    scala = lato / oggi.width
    per_parte = int((ALTEZZA_MASSIMA - INTESTAZIONE) / scala)
    parti = -(-righe // per_parte)
    larghezza = 2 * MARGINE + 2 * lato + SPAZIO
    file = []
    for parte in range(parti):
        sopra, sotto = parte * per_parte, min((parte + 1) * per_parte, righe)
        nota = f"pixel diversi: {esito['pixel_diversi']:,}".replace(",", ".")
        if parti > 1:
            nota = f"parte {parte + 1} di {parti} · {nota}"
        testa = intestazione(larghezza, lato, esito["titolo"], nota)
        corpo = affianca(
            in_scala(oggi, sopra, sotto, lato),
            in_scala(nativa, sopra, sotto, lato),
            lato,
        )
        tela = Image.new("RGB", (larghezza, testa.height + corpo.height), "white")
        tela.paste(testa, (0, 0))
        tela.paste(corpo, (0, testa.height))
        file.append(
            salva(
                tela, f"{nome}.jpg" if parti == 1 else f"{nome}_parte_{parte + 1}.jpg"
            )
        )
    return file, lato / oggi.width * 2


def finestre(testi: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Le zone da ritagliare: intorno a ogni testo che si vede (la k-esima volta oggi con la
    k-esima nativa), unite quando si toccano. Righe in px della foto (2 per px CSS)."""
    zone = []
    for testo in testi:
        for k in range(max(len(testo["oggi"]), len(testo["nativa"]))):
            zona: dict[str, Any] = {"testi": [testo["testo"]]}
            for quale in ("oggi", "nativa"):
                if k < len(testo[quale]):
                    sopra, sotto = testo[quale][k][:2]
                    zona[quale] = [
                        round(sopra * 2) - ATTORNO,
                        round(sotto * 2) + ATTORNO,
                    ]
                else:
                    zona[quale] = None
            zone.append(zona)
    zone.sort(key=lambda z: (z["nativa"] or z["oggi"])[0])
    unite: list[dict[str, Any]] = []
    for zona in zone:
        ultima = unite[-1] if unite else None
        if ultima is not None and all(
            (ultima[q] is None) == (zona[q] is None)
            and (zona[q] is None or zona[q][0] <= ultima[q][1])
            for q in ("oggi", "nativa")
        ):
            for q in ("oggi", "nativa"):
                if zona[q] is not None:
                    ultima[q] = [ultima[q][0], max(ultima[q][1], zona[q][1])]
            ultima["testi"] += [t for t in zona["testi"] if t not in ultima["testi"]]
        else:
            unite.append(zona)
    return unite


def didascalia(testi: list[dict[str, Any]], larghezza: int) -> Image.Image:
    """Sopra ogni ritaglio: il testo di oggi e quello nativo di ogni testo aggiornato."""
    normale, grassetto = carattere(14), carattere(14, True)
    colonne = max(int((larghezza - 2 * MARGINE - 70) / 7.9), 40)
    righe: list[tuple[str, str, tuple[int, int, int]]] = []
    for testo in testi:
        for etichetta, chiave, colore in (
            ("Oggi:", "prima", (150, 30, 30)),
            ("Nativa:", "dopo", (20, 110, 40)),
        ):
            pezzi = textwrap.wrap(piano(testo[chiave]), colonne) or [""]
            righe += [
                (etichetta if i == 0 else "", p, colore) for i, p in enumerate(pezzi)
            ]
    tela = Image.new("RGB", (larghezza, 10 + 19 * len(righe)), (248, 248, 244))
    disegno = ImageDraw.Draw(tela)
    for i, (etichetta, riga, colore) in enumerate(righe):
        y = 6 + 19 * i
        disegno.text((MARGINE, y), etichetta, fill=colore, font=grassetto)
        disegno.text((MARGINE + 70, y), riga, fill=(30, 30, 30), font=normale)
    return tela


def ritagli(nome: str, esito: dict[str, Any]) -> list[str]:
    """I ritagli intorno ai testi aggiornati della scena (in parti, se serve)."""
    oggi = Image.open(SCENE_DIR / f"{nome}_oggi.png").convert("RGB")
    nativa = Image.open(SCENE_DIR / f"{nome}_nativa.png").convert("RGB")
    per_numero = {t["testo"]: t for t in esito["testi"]}
    larghezza = 2 * MARGINE + 2 * LATO_RITAGLIO + SPAZIO
    blocchi = []
    for zona in finestre(esito["testi"]):
        corpo = affianca(
            in_scala(oggi, *zona["oggi"], LATO_RITAGLIO) if zona["oggi"] else None,
            in_scala(nativa, *zona["nativa"], LATO_RITAGLIO)
            if zona["nativa"]
            else None,
            LATO_RITAGLIO,
        )
        sopra = didascalia([per_numero[t] for t in zona["testi"]], larghezza)
        blocco = Image.new(
            "RGB", (larghezza, sopra.height + corpo.height + 20), "white"
        )
        blocco.paste(sopra, (0, 0))
        blocco.paste(corpo, (0, sopra.height + 6))
        blocchi.append(blocco)
    # parti alte al massimo ALTEZZA_MASSIMA, senza spezzare un ritaglio
    parti: list[list[Image.Image]] = [[]]
    altezza = INTESTAZIONE
    for blocco in blocchi:
        if parti[-1] and altezza + blocco.height > ALTEZZA_MASSIMA:
            parti.append([])
            altezza = INTESTAZIONE
        parti[-1].append(blocco)
        altezza += blocco.height
    file = []
    for numero, blocchi_parte in enumerate(parti, 1):
        nota = f"{len(esito['testi'])} testi aggiornati"
        if len(parti) > 1:
            nota = f"parte {numero} di {len(parti)} · {nota}"
        testa = intestazione(
            larghezza, LATO_RITAGLIO, f"{esito['titolo']} - testi aggiornati", nota
        )
        tela = Image.new(
            "RGB",
            (larghezza, testa.height + sum(b.height for b in blocchi_parte)),
            "white",
        )
        tela.paste(testa, (0, 0))
        y = testa.height
        for blocco in blocchi_parte:
            tela.paste(blocco, (0, y))
            y += blocco.height
        file.append(
            salva(
                tela,
                f"{nome}_testi.jpg"
                if len(parti) == 1
                else f"{nome}_testi_{numero}.jpg",
            )
        )
    return file


def principale() -> int:
    risultati = json.loads((ANTEPRIMA / "risultati.json").read_text(encoding="utf-8"))
    shutil.rmtree(GALLERIA, ignore_errors=True)
    GALLERIA.mkdir(parents=True)
    indice = []
    for nome, esito in risultati["scene"].items():
        file, scala = scena_intera(nome, esito)
        voce = {
            "scena": nome,
            "titolo": esito["titolo"],
            "file": file,
            "scala_px_per_px_css": scala,
            "pixel_diversi": esito["pixel_diversi"],
            "pixel_confrontati": esito["su"],
            "altezza_oggi": esito["oggi"][1],
            "altezza_nativa": esito["nativa"][1],
            "nota": NOTE.get(nome, ""),
            "testi_aggiornati": [
                {
                    "prima": piano(t["prima"]),
                    "dopo": piano(t["dopo"]),
                    "volte_oggi": len(t["oggi"]),
                    "volte_nativa": len(t["nativa"]),
                }
                for t in esito["testi"]
            ],
            "ritagli": ritagli(nome, esito) if esito["testi"] else [],
        }
        indice.append(voce)
        print(nome, voce["file"], voce["ritagli"], flush=True)
    byte = sum(f.stat().st_size for f in GALLERIA.glob("*.jpg"))
    (GALLERIA / "index.json").write_text(
        json.dumps(
            {
                "descrizione": (
                    "Scheda «VMC Master» di oggi (a sinistra) e tradotta ai nomi delle "
                    "entità native (a destra), nello stesso Home Assistant con le stesse "
                    "situazioni; pixel diversi contati sulle fotografie intere (2 px per "
                    "px CSS, larghe 480 px CSS). Nei ritagli, sopra ogni pezzo, il testo di "
                    "oggi e quello nuovo."
                ),
                "scene": indice,
                "file_jpeg": len(list(GALLERIA.glob("*.jpg"))),
                "byte_jpeg": byte,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"{len(indice)} scene, {byte} byte", flush=True)
    return 0 if byte <= BYTE_MASSIMI else 1


if __name__ == "__main__":
    sys.exit(principale())
