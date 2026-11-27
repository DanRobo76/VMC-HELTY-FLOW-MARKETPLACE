"""I modelli del package leggono i valori interni dalla memoria come dagli aiutanti.

Lo stesso banco di ``test_modelli_motore`` (ogni modello delle automazioni e degli script
del package, a caso e mirato), con una differenza: il motore non trova i 67 valori interni
nella macchina degli stati ma solo nella vista della memoria interna
(``HassConMemoria``/``StatiConMemoria``), con gli stessi oggetti ``State``. Home
Assistant li legge dalla macchina degli stati. Si confrontano testo, risultato,
``RenderInfo`` (entità lette, domini...: quello che ascoltano trigger e attese) ed esito
come condizione: ogni lettura (``states()``, ``is_state()``, ``state_attr()``,
``states.d.o``, ``expand``, filtri e test...) deve passare dalla vista, anche con i nomi
composti.
"""

from __future__ import annotations

import os
from collections.abc import Iterable, Iterator, Mapping
from types import SimpleNamespace
from typing import Any

from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant, State

from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.generato import modelli as M
from custom_components.vmc_master.nativa.motore.memoria_interna import (
    HassConMemoria,
    StatiConMemoria,
)

from . import valori_package as P
from .test_memoria_interna import IDS
from .test_modelli_motore import (
    SCENARI,
    VARIANTI,
    Banco,
    Confronto,
    _Registrato,
    senza_avvisi,  # noqa: F401
)
from .traduci import traduzione

GIRI = int(os.environ.get("VMC_GIRI_MEMORIA", "10"))
# Pezzi dei nomi composti dai modelli che possono dare un valore interno.
COMPOSTI = (
    "vmc_master_attesa_'",
    "vmc_master_countdown_'",
    "vmc_master_aria_scambiata_'",
    "vmc_master_last_'",
)


class _SenzaInterni:
    """La macchina degli stati di Home Assistant senza i valori interni."""

    def __init__(self, veri: Any, interni: set[str]) -> None:
        self._veri = veri
        self._interni = interni

    def get(self, entity_id: str) -> State | None:
        if entity_id in self._interni or entity_id.lower() in self._interni:
            return None
        return self._veri.get(entity_id)  # type: ignore[no-any-return]

    def async_all(self, domain_filter: Any = None) -> list[State]:
        return [
            s
            for s in self._veri.async_all(domain_filter)
            if s.entity_id not in self._interni
        ]

    def async_entity_ids(self, domain_filter: Any = None) -> list[str]:
        return [s.entity_id for s in self.async_all(domain_filter)]

    def async_entity_ids_count(self, domain_filter: Any = None) -> int:
        return len(self.async_all(domain_filter))

    @property
    def _states(self) -> Mapping[str, State]:
        return {s.entity_id: s for s in self.async_all()}

    def __getattr__(self, nome: str) -> Any:
        raise AttributeError(f"la memoria non deve usare {nome}")


class _Vista(Mapping[str, State]):
    """I valori interni come li ha la memoria: gli stessi oggetti ``State``."""

    def __init__(self, veri: Any, interni: Iterable[str]) -> None:
        self._veri = veri
        self._interni = list(interni)

    def __getitem__(self, chiave: str) -> State:
        if chiave not in self._interni or (stato := self._veri.get(chiave)) is None:
            raise KeyError(chiave)
        return stato  # type: ignore[no-any-return]

    def __iter__(self) -> Iterator[str]:
        return (e for e in self._interni if self._veri.get(e) is not None)

    def __len__(self) -> int:
        return sum(1 for _ in self)


def _legge_interni(sorgente: str) -> bool:
    return any(e in sorgente for e in IDS) or any(p in sorgente for p in COMPOSTI)


async def test_modelli_leggono_la_memoria(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    senza_avvisi: None,  # noqa: F811
) -> None:
    """Stesso testo, risultato, RenderInfo ed esito di condizione per ogni modello che
    legge valori interni, con i valori interni solo nella vista della memoria."""
    package = P.leggi()
    tutti = sorted(set(package.automazioni_di) | package.negli_script)
    sorgenti = [s for s in tutti if _legge_interni(s)]
    modelli = {s: _Registrato(s, hass) for s in tutti}
    for modello in modelli.values():
        modello.ensure_valid()
    jinja, _generatore, _, _ = await traduzione(
        hass, package.automazioni, package.script
    )
    banco = Banco(hass, tutti, package, modelli)
    assert set(IDS) <= set(banco.entita)
    c = Contesto(hass)
    senza: Any = _SenzaInterni(hass.states, set(IDS))
    stati = StatiConMemoria(senza, _Vista(hass.states, IDS))
    memoria: Any = SimpleNamespace(hass_modelli=HassConMemoria(hass, stati))
    c.usa_memoria(memoria)
    confronto = Confronto(
        hass,
        c,
        {s: modelli[s] for s in sorgenti},
        {s: getattr(M, jinja.funzioni[s]) for s in sorgenti},
        jinja.funzioni,
        banco.entita,
    )
    for _ in range(GIRI):
        banco.giro(freezer)
        for sorgente in sorgenti:
            for _ in range(VARIANTI):
                banco.mira_stati(sorgente)
                confronto.confronta(sorgente, banco.variabili(sorgente))
    banco.giro(freezer)
    mirate = 0
    for sorgente in sorgenti:
        for forzato in banco.mirati(sorgente):
            banco.mira_stati(sorgente, forzato)
            confronto.confronta(sorgente, banco.variabili(sorgente, forzato))
            mirate += 1
    for pezzo, valori, variabili in SCENARI:
        for sorgente in (s for s in sorgenti if pezzo in s):
            for entity_id, (stato, attributi) in valori.items():
                hass.states.async_set(entity_id, stato, attributi)
            confronto.confronta(sorgente, banco.variabili(sorgente) | variabili)
            mirate += 1
    rese = confronto.rese
    letti = {e for s in sorgenti for e in IDS if e in s}
    print(
        f"\n{len(sorgenti)} modelli che leggono valori interni ({len(letti)} valori "
        f"scritti per nome), {GIRI} giri, {mirate} rese mirate: {dict(sorted(rese.items()))}"
    )
    assert rese["testo: valore"] > rese["testo: errore"]
    assert not confronto.differenze, "\n".join(confronto.differenze)
