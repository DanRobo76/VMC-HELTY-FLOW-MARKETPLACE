"""Trasformazioni testuali identiche a quelle degli script della release 8.6.0.

Ogni funzione riproduce, riga per riga, i comandi sed di vmc_script_clona.sh
e di vmc_master_script_cambio_ip.sh, cosi' i file generati dall'integrazione
sono identici a quelli che gli script avrebbero creato.
"""

from __future__ import annotations

import re

from .const import NOME_MASTER

_RE_IP = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
_RE_NC = re.compile(r"nc [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ 5001")

_INIZIO_CLONA = ">>> INIZIO SEZIONE CLONA VMC"
_FINE_CLONA = ">>> FINE SEZIONE CLONA VMC"
_INIZIO_INSTALLA = ">>> INIZIO SEZIONE INSTALLA VMC"
_FINE_INSTALLA = ">>> FINE SEZIONE INSTALLA VMC"
_VOCE_FINESTRA_CLONA = "'input_boolean.vmc_master_opzione_finestra_clona', "


def _dividi_righe(testo: str) -> list[str]:
    """Divide il testo in righe come fa sed: il terminatore resta attaccato alla riga."""
    return testo.splitlines(keepends=True)


def _corpo(riga: str) -> str:
    """Riga senza il solo carattere di fine riga (\\n), come la vede sed."""
    return riga[:-1] if riga.endswith("\n") else riga


def _ricomponi(corpo: str, riga_originale: str) -> str:
    return corpo + "\n" if riga_originale.endswith("\n") else corpo


_IS_STATE_FINESTRA_CLONA = "is_state('input_boolean.vmc_master_opzione_finestra_clona'"


def rimuovi_clona(testo: str) -> str:
    """Prima meta' dello script sed del ciclo «for file_clone» di vmc_script_clona.sh.

    Comandi, nell'ordine, applicati a ogni riga:
      /INIZIO CLONA/,/FINE CLONA/d
      /is_state('input_boolean.vmc_master_opzione_finestra_clona'/d   (correzione, vedi sotto)
      s/'input_boolean.vmc_master_opzione_finestra_clona', //g
      /vmc_master_opzione_finestra_clona/d
      /vmc_master_clona_/d

    Correzione rispetto alla 8.6.0: la riga «or is_state('input_boolean.vmc_master_opzione_
    finestra_clona', 'on')» della scheda si toglie intera. Con la sola sostituzione restava
    «or is_state('on')», che fa fallire il modello del Pannello Informazioni.
    """
    uscita: list[str] = []
    in_clona = False
    for riga in _dividi_righe(testo):
        corpo = _corpo(riga)
        # la fine dell'intervallo si cerca solo dalla riga successiva all'inizio (come sed)
        if in_clona:
            if _FINE_CLONA in corpo:
                in_clona = False
            continue
        if _INIZIO_CLONA in corpo:
            in_clona = True
            continue
        if _IS_STATE_FINESTRA_CLONA in corpo:
            continue
        corpo = corpo.replace(_VOCE_FINESTRA_CLONA, "")
        if "vmc_master_opzione_finestra_clona" in corpo or "vmc_master_clona_" in corpo:
            continue
        uscita.append(_ricomponi(corpo, riga))
    return "".join(uscita)


_CLONATE = "states('input_text.vmc_master_clona_vmc_clonate')"


def neutralizza_clonate_in_installa(testo: str) -> str:
    """Solo VMC Master dell'integrazione (Prima Installazione presente, Clona assente).

    Nella sezione Installa VMC i controlli dell'IP leggono anche l'elenco delle VMC clonate
    in attesa di riavvio (input_text.vmc_master_clona_vmc_clonate). Senza la Finestra Clona
    quell'elenco non esiste piu': al suo posto si mette l'elenco vuoto '' cosi' la riga
    non viene cancellata da rimuovi_clona e i modelli Jinja restano completi.
    Le VMC aggiunte dall'integrazione sono controllate dalla configurazione (IP gia' in uso).
    """
    uscita: list[str] = []
    in_installa = False
    for riga in _dividi_righe(testo):
        corpo = _corpo(riga)
        if _INIZIO_INSTALLA in corpo:
            in_installa = True
        elif _FINE_INSTALLA in corpo:
            in_installa = False
        elif in_installa and _CLONATE in corpo:
            corpo = corpo.replace(_CLONATE, "''")
        uscita.append(_ricomponi(corpo, riga))
    return "".join(uscita)


def rimuovi_installa(testo: str) -> str:
    """Seconda meta' dello stesso script sed:
      /INIZIO INSTALLA/,/FINE INSTALLA/d
      /vmc_master_installa_vmc_/d
    Applicata dopo rimuovi_clona da' lo stesso risultato dell'unico passaggio di sed:
    le righe cancellate dalla prima meta' non arrivano mai alla seconda.
    """
    uscita: list[str] = []
    in_installa = False
    for riga in _dividi_righe(testo):
        corpo = _corpo(riga)
        if in_installa:
            if _FINE_INSTALLA in corpo:
                in_installa = False
            continue
        if _INIZIO_INSTALLA in corpo:
            in_installa = True
            continue
        if "vmc_master_installa_vmc_" in corpo:
            continue
        uscita.append(riga)
    return "".join(uscita)


def rimuovi_sezioni_solo_master(testo: str) -> str:
    """Tutto lo script sed del ciclo «for file_clone» di vmc_script_clona.sh."""
    return rimuovi_installa(rimuovi_clona(testo))


# Nome del file del video nel repository VMC-HELTY-FLOW: non va rinominato, altrimenti
# nelle VMC clonate il link punta a «VMC_‹nome›_promo_IT.mp4», che non esiste
_VIDEO_PROMO = "VMC_MASTER_promo_"
_SEGNAPOSTO_VIDEO = "\x00VIDEO_PROMO\x00"


def rinomina(testo: str, nome: str) -> str:
    """s/master/nome/g, poi s/Master/nome/g, poi s/MASTER/nome/g (come vmc_script_clona.sh),
    lasciando intatto il nome del file del video promozionale."""
    testo = testo.replace(_VIDEO_PROMO, _SEGNAPOSTO_VIDEO)
    testo = testo.replace("master", nome).replace("Master", nome).replace("MASTER", nome)
    return testo.replace(_SEGNAPOSTO_VIDEO, _VIDEO_PROMO)


def sostituisci_ip(testo: str, ip: str) -> str:
    """s/[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+/ip/g (riga per riga, come sed)."""
    return "".join(
        _ricomponi(_RE_IP.sub(ip, _corpo(riga)), riga) for riga in _dividi_righe(testo)
    )


def sostituisci_ip_nc(testo: str, ip: str) -> str:
    """s/nc [0-9]\\+\\.[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+ 5001/nc ip 5001/ (prima occorrenza di ogni riga)."""
    return "".join(
        _ricomponi(_RE_NC.sub(f"nc {ip} 5001", _corpo(riga), count=1), riga)
        for riga in _dividi_righe(testo)
    )


_URL_RELEASE_8 = "https://api.github.com/repos/DanRobo76/VMC-HELTY-FLOW/releases/latest"
_URL_RELEASE_9 = "https://api.github.com/repos/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/releases/latest"
_RE_VERSIONE = re.compile(r'^(\s+state: )"v\.8\.6\.0"(\s*)$')


def adatta_versione(yaml_vmc: str, versione: str) -> str:
    """Il sensore «Package Ver.» mostra la versione dell'integrazione e il sensore
    «versione repository» legge le release del repository dell'integrazione,
    cosi' l'avviso di aggiornamento confronta versioni dello stesso prodotto.
    Cambiano solo queste due righe del package.
    """
    uscita: list[str] = []
    for riga in _dividi_righe(yaml_vmc):
        corpo = _corpo(riga)
        if _URL_RELEASE_8 in corpo:
            corpo = corpo.replace(_URL_RELEASE_8, _URL_RELEASE_9)
        else:
            corpo = _RE_VERSIONE.sub(lambda m: f'{m.group(1)}"v.{versione}"{m.group(2)}', corpo)
        uscita.append(_ricomponi(corpo, riga))
    return "".join(uscita)


_LINK_AGGIORNAMENTO_8 = "[Link](https://github.com/DanRobo76/VMC-HELTY-FLOW)"
_LINK_AGGIORNAMENTO_9 = "[Link](https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE)"


def adatta_link_aggiornamento(automazione: str) -> str:
    """La notifica «nuova revisione rilasciata» dell'automazione apre il repository
    dell'integrazione. Cambia solo la riga del link."""
    return automazione.replace(_LINK_AGGIORNAMENTO_8, _LINK_AGGIORNAMENTO_9)


_LINK_GITHUB_8 = 'href="https://github.com/DanRobo76/VMC-HELTY-FLOW">GitHub</a>'
_LINK_GITHUB_9 = 'href="https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE">GitHub</a>'


def adatta_link_github(scheda: str) -> str:
    """Il link «GitHub» del Pannello Informazioni apre il repository dell'integrazione.
    Cambia solo quella riga della scheda (i link del video restano sul repository
    VMC-HELTY-FLOW, dove si trovano i file)."""
    return scheda.replace(_LINK_GITHUB_8, _LINK_GITHUB_9)


def per_vmc(testo_master: str, nome: str, ip: str) -> str:
    """Scheda o automazione della VMC indicata, come la produce la release 8.6.0,
    ma senza la Finestra Clona (sostituita da «Aggiungi voce» dell'integrazione).

    - VMC Master: solo la rimozione della sezione Clona (Cambia IP non tocca questi file);
    - altre VMC: stessa sequenza di vmc_script_clona.sh (rimozione sezioni, nome, IP).
    """
    if nome == NOME_MASTER:
        return rimuovi_clona(neutralizza_clonate_in_installa(testo_master))
    testo = rimuovi_sezioni_solo_master(testo_master)
    testo = rinomina(testo, nome)
    return sostituisci_ip(testo, ip)


def package_per_vmc(yaml_master: str, nome: str, ip: str) -> str:
    """vmc_<nome>.yaml: come per_vmc, ma per la Master anche l'IP (script Cambia IP)."""
    if nome == NOME_MASTER:
        return sostituisci_ip(rimuovi_clona(neutralizza_clonate_in_installa(yaml_master)), ip)
    return per_vmc(yaml_master, nome, ip)


def script_cambio_ip_per_vmc(script_master: str, nome: str, ip: str) -> str:
    """vmc_<nome>_script_cambio_ip.sh (lo script Cambia IP non modifica se stesso)."""
    if nome == NOME_MASTER:
        return script_master
    return sostituisci_ip(rinomina(script_master, nome), ip)


def script_cambio_nome_per_vmc(script_master: str, nome: str, ip: str) -> str:
    """vmc_<nome>_script_cambio_nome.sh (Clona e Cambia IP cambiano solo l'IP dopo «nc»)."""
    if nome != NOME_MASTER:
        script_master = rinomina(script_master, nome)
    return sostituisci_ip_nc(script_master, ip)
