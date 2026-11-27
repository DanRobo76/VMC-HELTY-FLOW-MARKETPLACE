"""Automazioni e script del package, tradotti in Python (parte 8 di 8).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from datetime import time, timedelta

from .. import condizioni as C
from ..definizioni import Automazione, Script
from ..esecuzione import Annulla, Ferma, Modello
from . import modelli as M
from .motore_01 import (
    k0745, k0746, k0747, k0748, k0749, k0750, k0753, k0755, k0757, k0758,
    k0780, k0783, k0784, k0785, k0786, k0787, k0788, k0810, k0811, k0812,
    k0813, k0814, k0815, k0816, k0817, k0818, k0819, k0820, k0821,
)


async def s2093(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s2094)
    elif r.prova((k0755, )):
        await r.sotto(s2103)
    elif r.prova((k0757, )):
        await r.sotto(s2112)
    elif r.prova((k0758, )):
        await r.sotto(s2121)


async def s2094(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2095)
    elif r.prova((k0748, )):
        await r.sotto(s2097)
    elif r.prova((k0749, )):
        await r.sotto(s2099)
    elif r.prova((k0750, )):
        await r.sotto(s2101)


async def s2095(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2096, (k0745, ))


async def s2096(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2097(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2098, (k0747, ))


async def s2098(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2099(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2100, (k0745, ))


async def s2100(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2101(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2102, (k0747, ))


async def s2102(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2103(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2104)
    elif r.prova((k0748, )):
        await r.sotto(s2106)
    elif r.prova((k0749, )):
        await r.sotto(s2108)
    elif r.prova((k0750, )):
        await r.sotto(s2110)


async def s2104(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2105, (k0747, ))


async def s2105(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2106(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2107, (k0747, ))


async def s2107(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2108(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2109, (k0747, ))


async def s2109(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2110(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2111, (k0747, ))


async def s2111(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2112(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2113)
    elif r.prova((k0748, )):
        await r.sotto(s2115)
    elif r.prova((k0749, )):
        await r.sotto(s2117)
    elif r.prova((k0750, )):
        await r.sotto(s2119)


async def s2113(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2114, (k0745, ))


async def s2114(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2115(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2116, (k0747, ))


async def s2116(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2117(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2118, (k0745, ))


async def s2118(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2119(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2120, (k0747, ))


async def s2120(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2121(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2122)
    elif r.prova((k0748, )):
        await r.sotto(s2124)
    elif r.prova((k0749, )):
        await r.sotto(s2126)
    elif r.prova((k0750, )):
        await r.sotto(s2128)


async def s2122(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2123, (k0747, ))


async def s2123(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2124(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2125, (k0747, ))


async def s2125(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2126(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2127, (k0747, ))


async def s2127(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2128(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2129, (k0747, ))


async def s2129(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2130(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s2131)
    elif r.prova((k0755, )):
        await r.sotto(s2140)
    elif r.prova((k0757, )):
        await r.sotto(s2149)
    elif r.prova((k0758, )):
        await r.sotto(s2158)


async def s2131(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2132)
    elif r.prova((k0748, )):
        await r.sotto(s2134)
    elif r.prova((k0749, )):
        await r.sotto(s2136)
    elif r.prova((k0750, )):
        await r.sotto(s2138)


async def s2132(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2133, (k0780, ))


async def s2133(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2134(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2135, (k0747, ))


async def s2135(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2136(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2137, (k0780, ))


async def s2137(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2138(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2139, (k0780, ))


async def s2139(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2140(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2141)
    elif r.prova((k0748, )):
        await r.sotto(s2143)
    elif r.prova((k0749, )):
        await r.sotto(s2145)
    elif r.prova((k0750, )):
        await r.sotto(s2147)


async def s2141(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2142, (k0747, ))


async def s2142(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2143(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2144, (k0747, ))


async def s2144(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2145(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2146, (k0780, ))


async def s2146(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2147(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2148, (k0780, ))


async def s2148(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2149(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2150)
    elif r.prova((k0748, )):
        await r.sotto(s2152)
    elif r.prova((k0749, )):
        await r.sotto(s2154)
    elif r.prova((k0750, )):
        await r.sotto(s2156)


async def s2150(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2151, (k0780, ))


async def s2151(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2152(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2153, (k0780, ))


async def s2153(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2154(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2155, (k0780, ))


async def s2155(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2156(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2157, (k0780, ))


async def s2157(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2158(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2159)
    elif r.prova((k0748, )):
        await r.sotto(s2161)
    elif r.prova((k0749, )):
        await r.sotto(s2163)
    elif r.prova((k0750, )):
        await r.sotto(s2165)


async def s2159(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2160, (k0780, ))


async def s2160(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2161(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2162, (k0780, ))


async def s2162(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2163(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2164, (k0780, ))


async def s2164(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2165(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2166, (k0780, ))


async def s2166(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2167(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0787, )):
        await r.sotto(s2168)
    elif r.prova((k0788, )):
        await r.sotto(s2177)


async def s2168(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0783, )):
        await r.sotto(s2169)
    elif r.prova((k0784, )):
        await r.sotto(s2171)
    elif r.prova((k0785, )):
        await r.sotto(s2173)
    elif r.prova((k0786, )):
        await r.sotto(s2175)


async def s2169(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s2170, (k0745, ))


async def s2170(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2171(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2172, (k0747, ))


async def s2172(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2173(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2174, (k0745, ))


async def s2174(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2175(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s2176, (k0747, ))


async def s2176(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2177(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s2178)
    elif r.prova((k0755, )):
        await r.sotto(s2187)
    elif r.prova((k0757, )):
        await r.sotto(s2196)
    elif r.prova((k0758, )):
        await r.sotto(s2205)


async def s2178(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2179)
    elif r.prova((k0748, )):
        await r.sotto(s2181)
    elif r.prova((k0749, )):
        await r.sotto(s2183)
    elif r.prova((k0750, )):
        await r.sotto(s2185)


async def s2179(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2180, (k0780, ))


async def s2180(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2181(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2182, (k0747, ))


async def s2182(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2183(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2184, (k0780, ))


async def s2184(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2185(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2186, (k0780, ))


async def s2186(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2187(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2188)
    elif r.prova((k0748, )):
        await r.sotto(s2190)
    elif r.prova((k0749, )):
        await r.sotto(s2192)
    elif r.prova((k0750, )):
        await r.sotto(s2194)


async def s2188(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2189, (k0747, ))


async def s2189(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2190(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2191, (k0747, ))


async def s2191(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2192(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2193, (k0780, ))


async def s2193(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2194(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2195, (k0780, ))


async def s2195(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2196(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2197)
    elif r.prova((k0748, )):
        await r.sotto(s2199)
    elif r.prova((k0749, )):
        await r.sotto(s2201)
    elif r.prova((k0750, )):
        await r.sotto(s2203)


async def s2197(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2198, (k0780, ))


async def s2198(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2199(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2200, (k0780, ))


async def s2200(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2201(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2202, (k0780, ))


async def s2202(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2203(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2204, (k0780, ))


async def s2204(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2205(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2206)
    elif r.prova((k0748, )):
        await r.sotto(s2208)
    elif r.prova((k0749, )):
        await r.sotto(s2210)
    elif r.prova((k0750, )):
        await r.sotto(s2212)


async def s2206(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2207, (k0780, ))


async def s2207(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2208(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2209, (k0780, ))


async def s2209(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2210(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2211, (k0780, ))


async def s2211(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2212(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2213, (k0780, ))


async def s2213(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2214(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s2215)
    elif r.prova((k0755, )):
        await r.sotto(s2224)
    elif r.prova((k0757, )):
        await r.sotto(s2233)
    elif r.prova((k0758, )):
        await r.sotto(s2242)


async def s2215(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2216)
    elif r.prova((k0748, )):
        await r.sotto(s2218)
    elif r.prova((k0749, )):
        await r.sotto(s2220)
    elif r.prova((k0750, )):
        await r.sotto(s2222)


async def s2216(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2217, (k0780, ))


async def s2217(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2218(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2219, (k0747, ))


async def s2219(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2220(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2221, (k0780, ))


async def s2221(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2222(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2223, (k0780, ))


async def s2223(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2224(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2225)
    elif r.prova((k0748, )):
        await r.sotto(s2227)
    elif r.prova((k0749, )):
        await r.sotto(s2229)
    elif r.prova((k0750, )):
        await r.sotto(s2231)


async def s2225(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2226, (k0747, ))


async def s2226(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2227(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2228, (k0747, ))


async def s2228(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2229(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2230, (k0780, ))


async def s2230(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2231(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2232, (k0780, ))


async def s2232(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2233(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2234)
    elif r.prova((k0748, )):
        await r.sotto(s2236)
    elif r.prova((k0749, )):
        await r.sotto(s2238)
    elif r.prova((k0750, )):
        await r.sotto(s2240)


async def s2234(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2235, (k0780, ))


async def s2235(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2236(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2237, (k0780, ))


async def s2237(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2238(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2239, (k0780, ))


async def s2239(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2240(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2241, (k0780, ))


async def s2241(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2242(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2243)
    elif r.prova((k0748, )):
        await r.sotto(s2245)
    elif r.prova((k0749, )):
        await r.sotto(s2247)
    elif r.prova((k0750, )):
        await r.sotto(s2249)


async def s2243(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2244, (k0780, ))


async def s2244(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2245(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2246, (k0780, ))


async def s2246(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2247(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2248, (k0780, ))


async def s2248(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2249(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2250, (k0780, ))


async def s2250(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2251(r):
    # script vmc_master_calendario_fascia_2_on > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s2252(r):
    # script vmc_master_audio_status_velocita
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0810, )):
        await r.sotto(s2253)


async def s2253(r):
    # script vmc_master_audio_status_velocita > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1006), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2254(r):
    # script vmc_master_audio_allerta_congelamento
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0811, )):
        await r.sotto(s2255)


async def s2255(r):
    # script vmc_master_audio_allerta_congelamento > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1008), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2256(r):
    # script vmc_master_audio_nessuna_allerta_congelamento
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0812, )):
        await r.sotto(s2257)


async def s2257(r):
    # script vmc_master_audio_nessuna_allerta_congelamento > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1010), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2258(r):
    # script vmc_master_audio_allerta_diff_temp
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0813, )):
        await r.sotto(s2259)


async def s2259(r):
    # script vmc_master_audio_allerta_diff_temp > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1012), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2260(r):
    # script vmc_master_audio_nessuna_allerta_diff_temp
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0814, )):
        await r.sotto(s2261)


async def s2261(r):
    # script vmc_master_audio_nessuna_allerta_diff_temp > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1014), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2262(r):
    # script vmc_master_audio_allerta_co2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0815, )):
        await r.sotto(s2263)


async def s2263(r):
    # script vmc_master_audio_allerta_co2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1016), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2264(r):
    # script vmc_master_audio_nessuna_allerta_co2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0815, )):
        await r.sotto(s2265)


async def s2265(r):
    # script vmc_master_audio_nessuna_allerta_co2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1018), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2266(r):
    # script vmc_master_audio_allerta_voc
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0816, )):
        await r.sotto(s2267)


async def s2267(r):
    # script vmc_master_audio_allerta_voc > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1019), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2268(r):
    # script vmc_master_audio_nessuna_allerta_voc
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0816, )):
        await r.sotto(s2269)


async def s2269(r):
    # script vmc_master_audio_nessuna_allerta_voc > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1021), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2270(r):
    # script vmc_master_audio_allerta_pdr
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0817, )):
        await r.sotto(s2271)


async def s2271(r):
    # script vmc_master_audio_allerta_pdr > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1022), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2272(r):
    # script vmc_master_audio_nessuna_allerta_pdr
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0817, )):
        await r.sotto(s2273)


async def s2273(r):
    # script vmc_master_audio_nessuna_allerta_pdr > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1024), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2274(r):
    # script vmc_master_audio_free_heating_o_free_cooling
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0818, )):
        await r.sotto(s2275)


async def s2275(r):
    # script vmc_master_audio_free_heating_o_free_cooling > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1025), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2276(r):
    # script vmc_master_audio_allerta_umidita_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0819, )):
        await r.sotto(s2277)


async def s2277(r):
    # script vmc_master_audio_allerta_umidita_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1027), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=20, microseconds=0))


async def s2278(r):
    # script vmc_master_audio_nessuna_allerta_umidita_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0819, )):
        await r.sotto(s2279)


async def s2279(r):
    # script vmc_master_audio_nessuna_allerta_umidita_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1029), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2280(r):
    # script vmc_master_audio_allerta_black_out
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0820, )):
        await r.sotto(s2281)


async def s2281(r):
    # script vmc_master_audio_allerta_black_out > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1030), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2282(r):
    # script vmc_master_audio_nessuna_allerta_black_out
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0821, )):
        await r.sotto(s2283)


async def s2283(r):
    # script vmc_master_audio_nessuna_allerta_black_out > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1005)}, {'entity_id': Modello(M.m0950)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1032), 'language': 'it'}, {'entity_id': Modello(M.m0950)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2284(r):
    # script vmc_master_ripristina_tempi_attesa
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'value': 16}, {'entity_id': [c.N('input_number.vmc_master_attesa_pdr_cambio')]})
    await r.servizio('input_number.set_value', {'value': 12}, {'entity_id': [c.N('input_number.vmc_master_attesa_pdr_cambio_inquinanti')]})
    await r.servizio('input_number.set_value', {'value': 16}, {'entity_id': [c.N('input_number.vmc_master_attesa_pdr_ripristino')]})
    await r.servizio('input_number.set_value', {'value': 12}, {'entity_id': [c.N('input_number.vmc_master_attesa_pdr_ripristino_inquinanti')]})
    await r.servizio('input_number.set_value', {'value': 24}, {'entity_id': [c.N('input_number.vmc_master_attesa_free_sospensione')]})
    await r.servizio('input_number.set_value', {'value': 20}, {'entity_id': [c.N('input_number.vmc_master_attesa_free_sospensione_inquinanti')]})
    await r.servizio('input_number.set_value', {'value': 24}, {'entity_id': [c.N('input_number.vmc_master_attesa_free_ripristino')]})
    await r.servizio('input_number.set_value', {'value': 20}, {'entity_id': [c.N('input_number.vmc_master_attesa_free_ripristino_inquinanti')]})
    await r.servizio('input_number.set_value', {'value': 32}, {'entity_id': [c.N('input_number.vmc_master_attesa_blackout_rilevazione')]})
    await r.servizio('input_number.set_value', {'value': 32}, {'entity_id': [c.N('input_number.vmc_master_attesa_blackout_ripristino')]})
    await r.servizio('input_number.set_value', {'value': 3}, {'entity_id': [c.N('input_number.vmc_master_attesa_calendario_inizio')]})
    await r.servizio('input_number.set_value', {'value': 3}, {'entity_id': [c.N('input_number.vmc_master_attesa_calendario_fine')]})
    await r.servizio('input_number.set_value', {'value': 5}, {'entity_id': [c.N('input_number.vmc_master_attesa_avvisi')]})
    await r.servizio('input_number.set_value', {'value': 8}, {'entity_id': [c.N('input_number.vmc_master_attesa_inquinanti_avvio')]})
    await r.servizio('input_number.set_value', {'value': 8}, {'entity_id': [c.N('input_number.vmc_master_attesa_inquinanti_avvio_spia_pdr')]})
    await r.servizio('input_number.set_value', {'value': 8}, {'entity_id': [c.N('input_number.vmc_master_attesa_inquinanti_fine')]})
    await r.servizio('input_number.set_value', {'value': 8}, {'entity_id': [c.N('input_number.vmc_master_attesa_inquinanti_memoria')]})
    await r.servizio('input_number.set_value', {'value': 20}, {'entity_id': [c.N('input_number.vmc_master_attesa_free_annullamento')]})
    await r.servizio('input_number.set_value', {'value': 28}, {'entity_id': [c.N('input_number.vmc_master_attesa_umidita_avvio')]})
    await r.servizio('input_number.set_value', {'value': 28}, {'entity_id': [c.N('input_number.vmc_master_attesa_umidita_fine')]})
    await r.servizio('input_number.set_value', {'value': 4}, {'entity_id': [c.N('input_number.vmc_master_attesa_umidita_memoria')]})
    await r.servizio('input_number.set_value', {'value': 4}, {'entity_id': [c.N('input_number.vmc_master_attesa_delta_avvio')]})
    await r.servizio('input_number.set_value', {'value': 4}, {'entity_id': [c.N('input_number.vmc_master_attesa_delta_fine')]})
    await r.servizio('input_number.set_value', {'value': 4}, {'entity_id': [c.N('input_number.vmc_master_attesa_delta_memoria')]})
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_attese_inizializzate')]})
