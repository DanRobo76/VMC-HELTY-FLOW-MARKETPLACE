"""I sensori calcolati in Python danno gli stessi stati dei modelli del package.

I modelli del package girano nel vero Home Assistant (integrazione template). A ogni giro
si cambiano a caso alcuni ingressi (spie, impostazioni, letture della VMC, sensori scelti,
ora) e si confrontano stato, disponibilita' e icona di ogni modello portato.
"""

from __future__ import annotations

import os
import random
from datetime import datetime, timedelta

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util

from custom_components.vmc_master.nativa.lettore import Lettore
from custom_components.vmc_master.nativa.modelli import MODELLI, Calcolo

from . import confronto as c

GIRI = int(os.environ.get("VMC_GIRI", "400"))
SEME = int(os.environ.get("VMC_SEME", "20261125"))


def _ora(rng: random.Random, stati: dict[str, str]) -> datetime:
    """Un'ora a caso; meta' delle volte vicina (-1, 0, +1 minuto) a un orario del Calendario."""
    giorno = datetime(2026, 1, 1, tzinfo=dt_util.get_default_time_zone()) + timedelta(days=rng.randrange(365))
    orari = [v for e, v in stati.items() if e.startswith("input_datetime.") and v.count(":") == 2]
    if orari and rng.random() < 0.5:
        h, m, s = (int(x) for x in rng.choice(orari).split(":"))
        return giorno.replace(hour=h, minute=m, second=s) + timedelta(minutes=rng.choice((-1, 0, 0, 1)))
    return giorno + timedelta(minutes=rng.randrange(1440), seconds=rng.choice((0, 0, 30)))


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_modelli_uguali_al_package(hass: HomeAssistant, freezer) -> None:
    await hass.config.async_set_time_zone("Europe/Rome")
    assert await async_setup_component(hass, "homeassistant", {})
    rng = random.Random(SEME)
    stati = c.base_iniziale(rng)
    freezer.move_to(_ora(rng, stati))
    esterni_attr = {eid: c.attributi_esterni(rng, eid) for eid in c.ESTERNI}

    def imposta(eid: str, valore: str) -> None:
        hass.states.async_set(eid, valore, c.attributi_fissi(eid) or esterni_attr.get(eid, {}))

    for eid, valore in stati.items():
        imposta(eid, valore)
    assert await async_setup_component(
        hass, "template", {"template": [b for b in c.package()["template"] if "triggers" not in b]}
    )
    await hass.async_block_till_done()
    portati = sorted(MODELLI)
    tutti = [eid for eid, d in c.modelli().items() if "triggers" not in d["blocco"]]
    differenze: list[str] = []
    visti: dict[str, set[str]] = {k: set() for k in portati}
    memoria: dict = {}  # ultimo risultato di ogni modello, da un giro all'altro
    for giro in range(GIRI):
        if giro:
            stati = c.campione(rng, stati, rng.randint(1, 10))
            if c.extra.SCENARI and rng.random() < 0.2:
                # combinazione da imporre insieme (extra/<gruppo>.py, SCENARI), a volte quasi
                nome = sorted(c.extra.SCENARI)[giro % len(c.extra.SCENARI)]
                stati.update(c.extra.SCENARI[nome])
                if rng.random() < 0.4:
                    for eid in rng.sample(sorted(c.extra.SCENARI[nome]), rng.randint(1, 2)):
                        stati[eid] = rng.choice(c.candidati(eid))
            freezer.move_to(_ora(rng, stati))
            if rng.random() < 0.2:
                eid = rng.choice(c.ESTERNI)
                esterni_attr[eid] = c.attributi_esterni(rng, eid)
                imposta(eid, stati[eid])
        for eid, valore in stati.items():
            attuale = hass.states.get(eid)
            if attuale is None or attuale.state != valore:
                imposta(eid, valore)
        await hass.async_block_till_done()
        await hass.services.async_call("homeassistant", "update_entity", {"entity_id": tutti}, blocking=True)
        await hass.async_block_till_done()

        def ingresso(chiave: str) -> str | None:
            s = hass.states.get(lettore.entity_id(chiave))
            return None if s is None else s.state

        calcolo = Calcolo(ingresso)
        def attributo(eid: str, nome: str):
            s = hass.states.get(eid)
            return None if s is None else s.attributes.get(nome)

        lettore = Lettore(
            c.NOME,
            calcolo.valore,
            lambda eid: (s.state if (s := hass.states.get(eid)) else None),
            dt_util.now,
            lambda chiave, nome: attributo(lettore.entity_id(chiave), nome),
            attributo,
            ip=c.IP,
            elenca=hass.states.async_all,
            memoria=memoria,
        )
        calcolo.lettore = lettore
        for chiave in portati:
            eid = lettore.entity_id(chiave)
            atteso = hass.states.get(eid)
            m = MODELLI[chiave]
            if m.ritardo_on is not None:
                # «delay_on»: si confrontano la condizione e il ritardo, resi dal modello del package
                conf = c.modelli()[eid]["conf"]
                cond = "on" if result_as_boolean(Template(conf["state"], hass).async_render(parse_result=False)) else "off"
                ottenuto = calcolo.condizione(chiave)
                visti[chiave].add(ottenuto)
                if cond != ottenuto:
                    differenze.append(f"giro {giro} {eid} condizione: package {cond!r}, Python {ottenuto!r}")
                if m.icona is not None:
                    # l'icona del sensore vero dipende dal ritardo: si confronta il suo template
                    icona_pkg = Template(str(conf["icon"]), hass).async_render(parse_result=False).strip()
                    if icona_pkg != calcolo.icona(chiave):
                        differenze.append(
                            f"giro {giro} {eid} icona: package {icona_pkg!r}, Python {calcolo.icona(chiave)!r}"
                        )
                rit = int(Template(str(conf["delay_on"]), hass).async_render(parse_result=False))
                if rit != m.ritardo_on(lettore):
                    differenze.append(f"giro {giro} {eid} ritardo: package {rit}, Python {m.ritardo_on(lettore)}")
                continue
            ottenuto = calcolo.valore(chiave)
            visti[chiave].add(ottenuto)
            if atteso.state != ottenuto:
                differenze.append(f"giro {giro} {eid}: package {atteso.state!r}, Python {ottenuto!r}")
            if m.icona is not None:
                icona = calcolo.icona(chiave)
                if atteso.attributes.get("icon") != icona:
                    differenze.append(f"giro {giro} {eid} icona: package {atteso.attributes.get('icon')!r}, Python {icona!r}")
    assert not differenze, "\n".join(differenze[:40])
    # ogni modello portato deve essere passato da piu' di un risultato
    poveri = {k: v for k, v in visti.items() if len(v) < 2 and k not in c.extra.UN_SOLO_RISULTATO}
    assert not poveri, f"modelli provati con un solo risultato: {poveri}"
