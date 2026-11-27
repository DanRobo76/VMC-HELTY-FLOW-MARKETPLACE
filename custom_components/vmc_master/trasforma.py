"""Trasformazioni testuali identiche a quelle degli script della release 8.6.0.

Ogni funzione riproduce, riga per riga, i comandi sed di vmc_script_clona.sh
e di vmc_master_script_cambio_ip.sh, cosi' i file generati dall'integrazione
sono identici a quelli che gli script avrebbero creato.
"""

from __future__ import annotations

import re

from .const import NOME_MASTER

_RE_IP = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
_RE_NC = re.compile(r"nc -w 3 [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ 5001")

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


# Parole che non vanno rinominate:
# - il nome del file del video nel repository VMC-HELTY-FLOW: altrimenti nelle VMC
#   clonate il link punta a «VMC_‹nome›_promo_IT.mp4», che non esiste;
# - la cartella dei backup della beta (vmc_master_backup), che era una sola per tutte
#   le VMC: il Pannello Informazioni della beta indicava sempre «vmc_master_backup»;
# - il servizio dell'integrazione chiamato dall'Automazione Cambio IP (dominio
#   «vmc_master», uno solo per tutte le VMC): «vmc_‹nome›.verifica_ip» non esiste;
# - il nome dell'integrazione nell'intestazione della licenza dei file (righe
#   «… CON L'INTEGRAZIONE VMC MASTER»): l'integrazione e' una sola per tutte le VMC;
# - i nomi con il trattino della scheda nativa: i tipi delle schede personalizzate
#   («custom:vmc-master-conto-alla-rovescia», «vmc-master-card»), definiti una volta
#   sola dal JavaScript della scheda (gli entity_id hanno solo trattini bassi);
# - il nome del repository dell'integrazione nativa (VMC-HELTY-FLOW-MASTER) nei link
#   e nella pagina del Marketplace.
# Nei file della beta (cartella «package») le ultime due non ci sono: restano identici.
_VIDEO_PROMO = "VMC_MASTER_promo_"
_CARTELLA_BACKUP = "vmc_master_backup"
_SERVIZIO_VERIFICA_IP = "vmc_master.verifica_ip"
_INTEGRAZIONE = "INTEGRAZIONE VMC MASTER"
_ELEMENTI_SCHEDA = "vmc-master-"
_REPOSITORY_NATIVA = "HELTY-FLOW-MASTER"
_PROTETTE = (
    _VIDEO_PROMO,
    _CARTELLA_BACKUP,
    _SERVIZIO_VERIFICA_IP,
    _INTEGRAZIONE,
    _ELEMENTI_SCHEDA,
    _REPOSITORY_NATIVA,
)


def rinomina(testo: str, nome: str) -> str:
    """s/master/nome/g, poi s/Master/nome/g, poi s/MASTER/nome/g (come vmc_script_clona.sh),
    lasciando intatte le parole di _PROTETTE (video promozionale, cartella dei backup,
    servizio verifica_ip, nome dell'integrazione nella licenza, tipi delle schede
    personalizzate e repository dell'integrazione nativa)."""
    for indice, parola in enumerate(_PROTETTE):
        testo = testo.replace(parola, f"\x00PROTETTA{indice}\x00")
    testo = testo.replace("master", nome).replace("Master", nome).replace("MASTER", nome)
    for indice, parola in enumerate(_PROTETTE):
        testo = testo.replace(f"\x00PROTETTA{indice}\x00", parola)
    return testo


def sostituisci_ip(testo: str, ip: str) -> str:
    """s/[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+/ip/g (riga per riga, come sed)."""
    return "".join(
        _ricomponi(_RE_IP.sub(ip, _corpo(riga)), riga) for riga in _dividi_righe(testo)
    )


def sostituisci_ip_nc(testo: str, ip: str) -> str:
    """s/nc -w 3 [0-9]\\+\\.[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+ 5001/nc -w 3 ip 5001/ (prima occorrenza di ogni riga)."""
    return "".join(
        _ricomponi(_RE_NC.sub(f"nc -w 3 {ip} 5001", _corpo(riga), count=1), riga)
        for riga in _dividi_righe(testo)
    )


_RE_VERSIONE = re.compile(r'^(\s+state: )"v\.8\.6\.0"(\s*)$')


def adatta_versione(yaml_vmc: str, versione: str) -> str:
    """Il sensore «Package Ver.» mostra la versione dell'integrazione, cosi' l'avviso di
    aggiornamento confronta versioni dello stesso prodotto. Cambia solo questa riga
    del package (il link delle release lo cambia adatta_link_repository).
    """
    return "".join(
        _ricomponi(
            _RE_VERSIONE.sub(lambda m: f'{m.group(1)}"v.{versione}"{m.group(2)}', _corpo(riga)),
            riga,
        )
        for riga in _dividi_righe(yaml_vmc)
    )


# Ogni link al repository della release manuale (pagina, release, immagini, video)
# punta al repository dell'integrazione, che contiene gli stessi file negli stessi
# percorsi. Il nome «VMC-HELTY-FLOW» senza «DanRobo76/» (testo, nomi delle
# automazioni) resta com'e'.
_RE_LINK_REPOSITORY_8 = re.compile(r"DanRobo76/VMC-HELTY-FLOW(?![-\w])")
# Il repository della beta: solo per rifare i file che la beta scriveva (installatore,
# per riconoscere i suoi elementi e per le prove); la scheda servita dall'integrazione
# usa const.REPOSITORY (VMC-HELTY-FLOW-MASTER)
REPOSITORY_INTEGRAZIONE = "DanRobo76/VMC-HELTY-FLOW-MARKETPLACE"


def adatta_link_repository(testo: str, repository: str = REPOSITORY_INTEGRAZIONE) -> str:
    """Tutti i link a github.com/DanRobo76/VMC-HELTY-FLOW (anche api.github.com e
    raw.githubusercontent.com) diventano link a ``repository`` (di norma
    VMC-HELTY-FLOW-MARKETPLACE, quello della beta; la scheda dell'integrazione nativa
    passa VMC-HELTY-FLOW-MASTER)."""
    return _RE_LINK_REPOSITORY_8.sub(repository, testo)


def per_vmc(testo_master: str, nome: str, ip: str) -> str:
    """Scheda o automazione della VMC indicata, come la produce la release 8.6.0,
    ma senza la Finestra Clona (sostituita da «Aggiungi dispositivo» dell'integrazione)
    e senza la Finestra Prima Installazione VMC (il collegamento al Wi-Fi si fa da
    «Aggiungi dispositivo», con lo stesso motore).

    - VMC Master: rimozione delle due sezioni (Cambia IP non tocca questi file);
    - altre VMC: stessa sequenza di vmc_script_clona.sh (rimozione sezioni, nome, IP).
    """
    testo = rimuovi_sezioni_solo_master(testo_master)
    if nome == NOME_MASTER:
        return testo
    testo = rinomina(testo, nome)
    return sostituisci_ip(testo, ip)


def package_per_vmc(yaml_master: str, nome: str, ip: str) -> str:
    """vmc_<nome>.yaml: come per_vmc, ma per la Master anche l'IP (script Cambia IP)."""
    if nome == NOME_MASTER:
        return sostituisci_ip(rimuovi_sezioni_solo_master(yaml_master), ip)
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
