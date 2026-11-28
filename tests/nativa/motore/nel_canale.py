"""Le prove che confrontano il motore con Home Assistant, con il canale del motore (b48).

Il motore vede gli eventi di Home Assistant nel suo canale (``seguire.CambiInterni``): un
ascoltatore del bus per tipo di evento li mette nel canale, nell'ordine del bus. Il registro
del motore li annota lì (``osserva_nel_canale``), cioè nell'ordine in cui li vede il motore,
come il registro di Home Assistant (un ascoltatore di tutti gli eventi) li annota nell'ordine in
cui li vedono le automazioni.

Gli annunci interni del motore (gli stati delle logiche, i valori della memoria interna, i
timer del motore) non passano dal bus. Le scritture delle entità dell'integrazione fatte mentre
Home Assistant consegna un evento tengono il loro posto anche nel canale
(``CambiInterni.scrivi``); gli eventi lanciati da altri (le chiamate di servizio e i cambi
delle entità di altre integrazioni) Home Assistant li mette nella sua coda, e con le sole
funzioni pubbliche il canale non vede quella coda: un annuncio interno può passare prima di
loro. Per questo il confronto (``ordine_esterno``) chiede le voci che si vedono fuori dal
motore nello stesso ordine e le voci interne nella stessa sequenza tra loro; cambia solo il posto
delle voci interne tra le altre (come ``--ordine-esterno`` del simulatore).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Event, HomeAssistant, callback

from custom_components.vmc_master.nativa.motore.seguire import cambi_interni


def osserva_nel_canale(
    hass: HomeAssistant, tipi: Iterable[str], annota: Callable[[Event[Any]], None]
) -> Callable[[], None]:
    """``annota`` per ogni evento dei ``tipi`` nel canale del motore, dopo chi lo segue;
    restituisce come smettere."""
    canale = cambi_interni(hass)
    osservati = [canale.osserva(tipo, callback(annota)) for tipo in sorted(set(tipi))]

    def togli() -> None:
        for smetti in osservati:
            smetti()

    return togli


def stato_di_logica(voce: Any) -> bool:
    """Una voce ``(istante, tipo, dati, ...)`` (tupla o lista) con lo stato di una logica
    del motore (una delle automazioni del package): un annuncio interno."""
    return (
        isinstance(voce, (tuple, list))
        and len(voce) > 2
        and voce[1] == EVENT_STATE_CHANGED
        and isinstance(voce[2], dict)
        and str(voce[2].get("entity_id", "")).startswith("automation.")
    )


def voce_interna(voce: Any) -> bool:
    """Lo stato di una logica (``stato_di_logica``) o un annuncio della memoria interna nel
    formato di ``banco_memoria.Smistatore`` (cambio, chiamata o ``state_reported`` di un
    valore interno)."""
    return stato_di_logica(voce) or (
        isinstance(voce, tuple)
        and len(voce) == 4
        and voce[1] in ("cambio", "chiamata", "rapporto")
    )


def ordine_esterno(
    voci: list[Any],
    interna: Callable[[Any], bool],
    confine: Callable[[Any], bool] | None = None,
) -> list[Any]:
    """Prima le voci esterne nel loro ordine, poi quelle interne nel loro ordine. Con
    ``confine`` tratto per tratto: le voci di confine (i passi del banco, dopo che il
    ciclo degli eventi ha finito) restano al loro posto e nessuna voce le passa."""
    uscita: list[Any] = []
    tratto: list[Any] = []

    def chiudi() -> None:
        uscita.extend(voce for voce in tratto if not interna(voce))
        uscita.extend(voce for voce in tratto if interna(voce))
        tratto.clear()

    for voce in voci:
        if confine is not None and confine(voce):
            chiudi()
            uscita.append(voce)
        else:
            tratto.append(voce)
    chiudi()
    return uscita


def rinumera_contesti(
    voci: list[Any],
    *elenchi: list[Any],
    posti: Callable[[Any], Iterable[int]] | None = None,
) -> list[list[Any]]:
    """``voci`` e gli altri ``elenchi`` con i contesti rinumerati nell'ordine in cui
    compaiono in ``voci``: dopo ``ordine_esterno`` i numeri non dipendono più dal posto
    delle voci interne. ``posti(voce)`` dice dove sono i contesti di una voce (un numero o
    una tupla di numeri, come ``Normalizzatore``: numero e numero del genitore); senza,
    in ``voce[3]``."""

    def dove(voce: Any) -> Iterable[int]:
        if posti is not None:
            return posti(voce)
        return (3,) if isinstance(voce, tuple) and len(voce) > 3 else ()

    nuovi: dict[Any, Any] = {None: None}

    def nuovo(numero: Any) -> Any:
        return nuovi.setdefault(numero, len(nuovi) - 1)

    def rinumera(voce: Any) -> Any:
        posizioni = set(dove(voce))
        if not posizioni:
            return voce
        return tuple(
            (
                (tuple(nuovo(n) for n in valore) if isinstance(valore, tuple) else nuovo(valore))
                if posto in posizioni
                else valore
            )
            for posto, valore in enumerate(voce)
        )

    rinumerate = [rinumera(voce) for voce in voci]
    return [rinumerate, *([rinumera(voce) for voce in elenco] for elenco in elenchi)]


class CoppiaContesto(tuple):
    """Un contesto normalizzato (``Normalizzatore``): numero d'ordine e numero del
    genitore. È una tupla (uguale e scritta come una tupla), riconoscibile per
    ``rinumera_ovunque``."""


def rinumera_ovunque(*elenchi: Any) -> list[Any]:
    """Gli ``elenchi`` con ogni ``CoppiaContesto`` (anche dentro tuple, liste e dizionari)
    rinumerata nell'ordine in cui compare, elenco dopo elenco: dopo ``ordine_esterno`` i
    numeri non dipendono più dal posto delle voci interne."""
    nuovi: dict[Any, Any] = {None: None}

    def nuovo(numero: Any) -> Any:
        return nuovi.setdefault(numero, len(nuovi) - 1)

    def rinumera(valore: Any) -> Any:
        if isinstance(valore, CoppiaContesto):
            return CoppiaContesto(nuovo(numero) for numero in valore)
        if isinstance(valore, tuple):
            return tuple(rinumera(v) for v in valore)
        if isinstance(valore, list):
            return [rinumera(v) for v in valore]
        if isinstance(valore, dict):
            return {k: rinumera(v) for k, v in valore.items()}
        return valore

    return [rinumera(elenco) for elenco in elenchi]
