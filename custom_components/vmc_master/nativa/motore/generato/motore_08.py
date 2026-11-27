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
    k0744, k0745, k0746, k0747, k0748, k0749, k0752, k0754, k0756, k0757,
    k0779, k0782, k0783, k0784, k0785, k0786, k0787, k0809, k0810, k0811,
    k0812, k0813, k0814, k0815, k0816, k0817, k0818, k0819, k0820,
)


async def s2092(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s2093)
    elif r.prova((k0754, )):
        await r.sotto(s2102)
    elif r.prova((k0756, )):
        await r.sotto(s2111)
    elif r.prova((k0757, )):
        await r.sotto(s2120)


async def s2093(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2094)
    elif r.prova((k0747, )):
        await r.sotto(s2096)
    elif r.prova((k0748, )):
        await r.sotto(s2098)
    elif r.prova((k0749, )):
        await r.sotto(s2100)


async def s2094(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2095, (k0744, ))


async def s2095(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2096(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2097, (k0746, ))


async def s2097(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2098(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2099, (k0744, ))


async def s2099(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2100(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2101, (k0746, ))


async def s2101(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2102(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2103)
    elif r.prova((k0747, )):
        await r.sotto(s2105)
    elif r.prova((k0748, )):
        await r.sotto(s2107)
    elif r.prova((k0749, )):
        await r.sotto(s2109)


async def s2103(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2104, (k0746, ))


async def s2104(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2105(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2106, (k0746, ))


async def s2106(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2107(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2108, (k0746, ))


async def s2108(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2109(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2110, (k0746, ))


async def s2110(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2111(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2112)
    elif r.prova((k0747, )):
        await r.sotto(s2114)
    elif r.prova((k0748, )):
        await r.sotto(s2116)
    elif r.prova((k0749, )):
        await r.sotto(s2118)


async def s2112(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2113, (k0744, ))


async def s2113(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2114(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2115, (k0746, ))


async def s2115(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2116(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2117, (k0744, ))


async def s2117(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2118(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2119, (k0746, ))


async def s2119(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2120(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2121)
    elif r.prova((k0747, )):
        await r.sotto(s2123)
    elif r.prova((k0748, )):
        await r.sotto(s2125)
    elif r.prova((k0749, )):
        await r.sotto(s2127)


async def s2121(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2122, (k0746, ))


async def s2122(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2123(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2124, (k0746, ))


async def s2124(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2125(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2126, (k0746, ))


async def s2126(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2127(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s2128, (k0746, ))


async def s2128(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2129(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s2130)
    elif r.prova((k0754, )):
        await r.sotto(s2139)
    elif r.prova((k0756, )):
        await r.sotto(s2148)
    elif r.prova((k0757, )):
        await r.sotto(s2157)


async def s2130(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2131)
    elif r.prova((k0747, )):
        await r.sotto(s2133)
    elif r.prova((k0748, )):
        await r.sotto(s2135)
    elif r.prova((k0749, )):
        await r.sotto(s2137)


async def s2131(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2132, (k0779, ))


async def s2132(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2133(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2134, (k0746, ))


async def s2134(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2135(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2136, (k0779, ))


async def s2136(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2137(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2138, (k0779, ))


async def s2138(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2139(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2140)
    elif r.prova((k0747, )):
        await r.sotto(s2142)
    elif r.prova((k0748, )):
        await r.sotto(s2144)
    elif r.prova((k0749, )):
        await r.sotto(s2146)


async def s2140(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2141, (k0746, ))


async def s2141(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2142(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2143, (k0746, ))


async def s2143(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2144(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2145, (k0779, ))


async def s2145(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2146(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2147, (k0779, ))


async def s2147(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2148(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2149)
    elif r.prova((k0747, )):
        await r.sotto(s2151)
    elif r.prova((k0748, )):
        await r.sotto(s2153)
    elif r.prova((k0749, )):
        await r.sotto(s2155)


async def s2149(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2150, (k0779, ))


async def s2150(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2151(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2152, (k0779, ))


async def s2152(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2153(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2154, (k0779, ))


async def s2154(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2155(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2156, (k0779, ))


async def s2156(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2157(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2158)
    elif r.prova((k0747, )):
        await r.sotto(s2160)
    elif r.prova((k0748, )):
        await r.sotto(s2162)
    elif r.prova((k0749, )):
        await r.sotto(s2164)


async def s2158(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2159, (k0779, ))


async def s2159(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2160(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2161, (k0779, ))


async def s2161(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2162(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2163, (k0779, ))


async def s2163(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2164(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2165, (k0779, ))


async def s2165(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2166(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0786, )):
        await r.sotto(s2167)
    elif r.prova((k0787, )):
        await r.sotto(s2176)


async def s2167(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0782, )):
        await r.sotto(s2168)
    elif r.prova((k0783, )):
        await r.sotto(s2170)
    elif r.prova((k0784, )):
        await r.sotto(s2172)
    elif r.prova((k0785, )):
        await r.sotto(s2174)


async def s2168(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s2169, (k0744, ))


async def s2169(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2170(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2171, (k0746, ))


async def s2171(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2172(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2173, (k0744, ))


async def s2173(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2174(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s2175, (k0746, ))


async def s2175(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2176(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s2177)
    elif r.prova((k0754, )):
        await r.sotto(s2186)
    elif r.prova((k0756, )):
        await r.sotto(s2195)
    elif r.prova((k0757, )):
        await r.sotto(s2204)


async def s2177(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2178)
    elif r.prova((k0747, )):
        await r.sotto(s2180)
    elif r.prova((k0748, )):
        await r.sotto(s2182)
    elif r.prova((k0749, )):
        await r.sotto(s2184)


async def s2178(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2179, (k0779, ))


async def s2179(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2180(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2181, (k0746, ))


async def s2181(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2182(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2183, (k0779, ))


async def s2183(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2184(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2185, (k0779, ))


async def s2185(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2186(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2187)
    elif r.prova((k0747, )):
        await r.sotto(s2189)
    elif r.prova((k0748, )):
        await r.sotto(s2191)
    elif r.prova((k0749, )):
        await r.sotto(s2193)


async def s2187(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2188, (k0746, ))


async def s2188(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2189(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2190, (k0746, ))


async def s2190(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2191(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2192, (k0779, ))


async def s2192(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2193(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2194, (k0779, ))


async def s2194(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2195(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2196)
    elif r.prova((k0747, )):
        await r.sotto(s2198)
    elif r.prova((k0748, )):
        await r.sotto(s2200)
    elif r.prova((k0749, )):
        await r.sotto(s2202)


async def s2196(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2197, (k0779, ))


async def s2197(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2198(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2199, (k0779, ))


async def s2199(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2200(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2201, (k0779, ))


async def s2201(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2202(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2203, (k0779, ))


async def s2203(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2204(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2205)
    elif r.prova((k0747, )):
        await r.sotto(s2207)
    elif r.prova((k0748, )):
        await r.sotto(s2209)
    elif r.prova((k0749, )):
        await r.sotto(s2211)


async def s2205(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2206, (k0779, ))


async def s2206(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2207(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2208, (k0779, ))


async def s2208(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2209(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2210, (k0779, ))


async def s2210(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2211(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2212, (k0779, ))


async def s2212(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2213(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s2214)
    elif r.prova((k0754, )):
        await r.sotto(s2223)
    elif r.prova((k0756, )):
        await r.sotto(s2232)
    elif r.prova((k0757, )):
        await r.sotto(s2241)


async def s2214(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2215)
    elif r.prova((k0747, )):
        await r.sotto(s2217)
    elif r.prova((k0748, )):
        await r.sotto(s2219)
    elif r.prova((k0749, )):
        await r.sotto(s2221)


async def s2215(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2216, (k0779, ))


async def s2216(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2217(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2218, (k0746, ))


async def s2218(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2219(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2220, (k0779, ))


async def s2220(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2221(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2222, (k0779, ))


async def s2222(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2223(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2224)
    elif r.prova((k0747, )):
        await r.sotto(s2226)
    elif r.prova((k0748, )):
        await r.sotto(s2228)
    elif r.prova((k0749, )):
        await r.sotto(s2230)


async def s2224(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2225, (k0746, ))


async def s2225(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2226(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2227, (k0746, ))


async def s2227(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2228(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2229, (k0779, ))


async def s2229(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2230(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2231, (k0779, ))


async def s2231(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2232(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2233)
    elif r.prova((k0747, )):
        await r.sotto(s2235)
    elif r.prova((k0748, )):
        await r.sotto(s2237)
    elif r.prova((k0749, )):
        await r.sotto(s2239)


async def s2233(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2234, (k0779, ))


async def s2234(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2235(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2236, (k0779, ))


async def s2236(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2237(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2238, (k0779, ))


async def s2238(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2239(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2240, (k0779, ))


async def s2240(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2241(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2242)
    elif r.prova((k0747, )):
        await r.sotto(s2244)
    elif r.prova((k0748, )):
        await r.sotto(s2246)
    elif r.prova((k0749, )):
        await r.sotto(s2248)


async def s2242(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2243, (k0779, ))


async def s2243(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2244(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2245, (k0779, ))


async def s2245(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2246(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2247, (k0779, ))


async def s2247(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2248(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2249, (k0779, ))


async def s2249(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2250(r):
    # script vmc_master_calendario_fascia_2_on > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s2251(r):
    # script vmc_master_audio_status_velocita
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0809, )):
        await r.sotto(s2252)


async def s2252(r):
    # script vmc_master_audio_status_velocita > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1005), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2253(r):
    # script vmc_master_audio_allerta_congelamento
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0810, )):
        await r.sotto(s2254)


async def s2254(r):
    # script vmc_master_audio_allerta_congelamento > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1007), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2255(r):
    # script vmc_master_audio_nessuna_allerta_congelamento
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0811, )):
        await r.sotto(s2256)


async def s2256(r):
    # script vmc_master_audio_nessuna_allerta_congelamento > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1009), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2257(r):
    # script vmc_master_audio_allerta_diff_temp
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0812, )):
        await r.sotto(s2258)


async def s2258(r):
    # script vmc_master_audio_allerta_diff_temp > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1011), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2259(r):
    # script vmc_master_audio_nessuna_allerta_diff_temp
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0813, )):
        await r.sotto(s2260)


async def s2260(r):
    # script vmc_master_audio_nessuna_allerta_diff_temp > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1013), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2261(r):
    # script vmc_master_audio_allerta_co2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0814, )):
        await r.sotto(s2262)


async def s2262(r):
    # script vmc_master_audio_allerta_co2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1015), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2263(r):
    # script vmc_master_audio_nessuna_allerta_co2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0814, )):
        await r.sotto(s2264)


async def s2264(r):
    # script vmc_master_audio_nessuna_allerta_co2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1017), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2265(r):
    # script vmc_master_audio_allerta_voc
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0815, )):
        await r.sotto(s2266)


async def s2266(r):
    # script vmc_master_audio_allerta_voc > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1018), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2267(r):
    # script vmc_master_audio_nessuna_allerta_voc
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0815, )):
        await r.sotto(s2268)


async def s2268(r):
    # script vmc_master_audio_nessuna_allerta_voc > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1020), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2269(r):
    # script vmc_master_audio_allerta_pdr
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0816, )):
        await r.sotto(s2270)


async def s2270(r):
    # script vmc_master_audio_allerta_pdr > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1021), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2271(r):
    # script vmc_master_audio_nessuna_allerta_pdr
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0816, )):
        await r.sotto(s2272)


async def s2272(r):
    # script vmc_master_audio_nessuna_allerta_pdr > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1023), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2273(r):
    # script vmc_master_audio_free_heating_o_free_cooling
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0817, )):
        await r.sotto(s2274)


async def s2274(r):
    # script vmc_master_audio_free_heating_o_free_cooling > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1024), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2275(r):
    # script vmc_master_audio_allerta_umidita_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0818, )):
        await r.sotto(s2276)


async def s2276(r):
    # script vmc_master_audio_allerta_umidita_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1026), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=20, microseconds=0))


async def s2277(r):
    # script vmc_master_audio_nessuna_allerta_umidita_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0818, )):
        await r.sotto(s2278)


async def s2278(r):
    # script vmc_master_audio_nessuna_allerta_umidita_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1028), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2279(r):
    # script vmc_master_audio_allerta_black_out
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0819, )):
        await r.sotto(s2280)


async def s2280(r):
    # script vmc_master_audio_allerta_black_out > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1029), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2281(r):
    # script vmc_master_audio_nessuna_allerta_black_out
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0820, )):
        await r.sotto(s2282)


async def s2282(r):
    # script vmc_master_audio_nessuna_allerta_black_out > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('media_player.volume_set', {'volume_level': Modello(M.m1004)}, {'entity_id': Modello(M.m0949)})
    await r.servizio('tts.google_translate_say', {'message': Modello(M.m1031), 'language': 'it'}, {'entity_id': Modello(M.m0949)})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))


async def s2283(r):
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
