"""Automazioni e script del package, tradotti in Python (parte 7 di 8).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from datetime import time, timedelta

from custom_components.vmc_master.nativa.motore import condizioni as C
from custom_components.vmc_master.nativa.motore.definizioni import Automazione, Script
from custom_components.vmc_master.nativa.motore.esecuzione import Annulla, Ferma, Modello
from . import modelli as M
from .motore_01 import (
    k0744, k0745, k0746, k0747, k0748, k0749, k0750, k0753, k0755, k0757,
    k0758, k0764, k0767, k0770, k0773, k0776, k0779, k0780, k0781, k0782,
    k0783, k0784, k0785, k0786, k0787, k0788, k0789, k0790, k0793, k0795,
    k0797, k0799, k0801, k0803, k0805, k0807, k0809,
)
from .motore_08 import (
    s2093, s2130, s2167, s2214, s2251,
)


async def s1650(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1651, (k0776, ))


async def s1651(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1652(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1653)
    elif r.prova((k0748, )):
        await r.sotto(s1655)
    elif r.prova((k0749, )):
        await r.sotto(s1657)
    elif r.prova((k0750, )):
        await r.sotto(s1659)


async def s1653(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1654, (k0776, ))


async def s1654(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1655(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1656, (k0776, ))


async def s1656(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1657(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1658, (k0776, ))


async def s1658(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1659(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1660, (k0776, ))


async def s1660(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1661(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1662)
    elif r.prova((k0748, )):
        await r.sotto(s1664)
    elif r.prova((k0749, )):
        await r.sotto(s1666)
    elif r.prova((k0750, )):
        await r.sotto(s1668)


async def s1662(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1663, (k0776, ))


async def s1663(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1664(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1665, (k0776, ))


async def s1665(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1666(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1667, (k0776, ))


async def s1667(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1668(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1669, (k0776, ))


async def s1669(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1670(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0782, )):
        await r.sotto(s1671)
    elif r.prova((k0789, )):
        await r.sotto(s1746)
    elif r.prova((k0790, )):
        await r.sotto(s1793)


async def s1671(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0779, )):
        await r.sotto(s1672)
    elif r.prova((k0781, )):
        await r.sotto(s1709)


async def s1672(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1673)
    elif r.prova((k0755, )):
        await r.sotto(s1682)
    elif r.prova((k0757, )):
        await r.sotto(s1691)
    elif r.prova((k0758, )):
        await r.sotto(s1700)


async def s1673(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1674)
    elif r.prova((k0748, )):
        await r.sotto(s1676)
    elif r.prova((k0749, )):
        await r.sotto(s1678)
    elif r.prova((k0750, )):
        await r.sotto(s1680)


async def s1674(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1675, (k0745, ))


async def s1675(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1676(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1677, (k0747, ))


async def s1677(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1678(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1679, (k0745, ))


async def s1679(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1680(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1681, (k0747, ))


async def s1681(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1682(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1683)
    elif r.prova((k0748, )):
        await r.sotto(s1685)
    elif r.prova((k0749, )):
        await r.sotto(s1687)
    elif r.prova((k0750, )):
        await r.sotto(s1689)


async def s1683(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1684, (k0747, ))


async def s1684(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1685(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1686, (k0747, ))


async def s1686(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1687(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1688, (k0747, ))


async def s1688(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1689(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1690, (k0747, ))


async def s1690(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1691(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1692)
    elif r.prova((k0748, )):
        await r.sotto(s1694)
    elif r.prova((k0749, )):
        await r.sotto(s1696)
    elif r.prova((k0750, )):
        await r.sotto(s1698)


async def s1692(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1693, (k0745, ))


async def s1693(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1694(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1695, (k0747, ))


async def s1695(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1696(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1697, (k0745, ))


async def s1697(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1698(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1699, (k0747, ))


async def s1699(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1700(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1701)
    elif r.prova((k0748, )):
        await r.sotto(s1703)
    elif r.prova((k0749, )):
        await r.sotto(s1705)
    elif r.prova((k0750, )):
        await r.sotto(s1707)


async def s1701(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1702, (k0747, ))


async def s1702(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1703(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1704, (k0747, ))


async def s1704(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1705(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1706, (k0747, ))


async def s1706(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1707(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1708, (k0747, ))


async def s1708(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1709(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1710)
    elif r.prova((k0755, )):
        await r.sotto(s1719)
    elif r.prova((k0757, )):
        await r.sotto(s1728)
    elif r.prova((k0758, )):
        await r.sotto(s1737)


async def s1710(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1711)
    elif r.prova((k0748, )):
        await r.sotto(s1713)
    elif r.prova((k0749, )):
        await r.sotto(s1715)
    elif r.prova((k0750, )):
        await r.sotto(s1717)


async def s1711(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1712, (k0780, ))


async def s1712(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1713(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1714, (k0747, ))


async def s1714(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1715(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1716, (k0780, ))


async def s1716(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1717(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1718, (k0780, ))


async def s1718(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1719(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1720)
    elif r.prova((k0748, )):
        await r.sotto(s1722)
    elif r.prova((k0749, )):
        await r.sotto(s1724)
    elif r.prova((k0750, )):
        await r.sotto(s1726)


async def s1720(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1721, (k0747, ))


async def s1721(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1722(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1723, (k0747, ))


async def s1723(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1724(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1725, (k0780, ))


async def s1725(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1726(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1727, (k0780, ))


async def s1727(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1728(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1729)
    elif r.prova((k0748, )):
        await r.sotto(s1731)
    elif r.prova((k0749, )):
        await r.sotto(s1733)
    elif r.prova((k0750, )):
        await r.sotto(s1735)


async def s1729(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1730, (k0780, ))


async def s1730(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1731(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1732, (k0780, ))


async def s1732(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1733(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1734, (k0780, ))


async def s1734(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1735(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1736, (k0780, ))


async def s1736(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1737(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1738)
    elif r.prova((k0748, )):
        await r.sotto(s1740)
    elif r.prova((k0749, )):
        await r.sotto(s1742)
    elif r.prova((k0750, )):
        await r.sotto(s1744)


async def s1738(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1739, (k0780, ))


async def s1739(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1740(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1741, (k0780, ))


async def s1741(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1742(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1743, (k0780, ))


async def s1743(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1744(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1745, (k0780, ))


async def s1745(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1746(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0787, )):
        await r.sotto(s1747)
    elif r.prova((k0788, )):
        await r.sotto(s1756)


async def s1747(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0783, )):
        await r.sotto(s1748)
    elif r.prova((k0784, )):
        await r.sotto(s1750)
    elif r.prova((k0785, )):
        await r.sotto(s1752)
    elif r.prova((k0786, )):
        await r.sotto(s1754)


async def s1748(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s1749, (k0745, ))


async def s1749(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1750(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1751, (k0747, ))


async def s1751(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1752(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1753, (k0745, ))


async def s1753(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1754(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s1755, (k0747, ))


async def s1755(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1756(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1757)
    elif r.prova((k0755, )):
        await r.sotto(s1766)
    elif r.prova((k0757, )):
        await r.sotto(s1775)
    elif r.prova((k0758, )):
        await r.sotto(s1784)


async def s1757(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1758)
    elif r.prova((k0748, )):
        await r.sotto(s1760)
    elif r.prova((k0749, )):
        await r.sotto(s1762)
    elif r.prova((k0750, )):
        await r.sotto(s1764)


async def s1758(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1759, (k0780, ))


async def s1759(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1760(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1761, (k0747, ))


async def s1761(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1762(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1763, (k0780, ))


async def s1763(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1764(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1765, (k0780, ))


async def s1765(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1766(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1767)
    elif r.prova((k0748, )):
        await r.sotto(s1769)
    elif r.prova((k0749, )):
        await r.sotto(s1771)
    elif r.prova((k0750, )):
        await r.sotto(s1773)


async def s1767(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1768, (k0747, ))


async def s1768(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1769(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1770, (k0747, ))


async def s1770(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1771(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1772, (k0780, ))


async def s1772(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1773(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1774, (k0780, ))


async def s1774(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1775(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1776)
    elif r.prova((k0748, )):
        await r.sotto(s1778)
    elif r.prova((k0749, )):
        await r.sotto(s1780)
    elif r.prova((k0750, )):
        await r.sotto(s1782)


async def s1776(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1777, (k0780, ))


async def s1777(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1778(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1779, (k0780, ))


async def s1779(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1780(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1781, (k0780, ))


async def s1781(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1782(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1783, (k0780, ))


async def s1783(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1784(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1785)
    elif r.prova((k0748, )):
        await r.sotto(s1787)
    elif r.prova((k0749, )):
        await r.sotto(s1789)
    elif r.prova((k0750, )):
        await r.sotto(s1791)


async def s1785(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1786, (k0780, ))


async def s1786(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1787(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1788, (k0780, ))


async def s1788(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1789(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1790, (k0780, ))


async def s1790(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1791(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1792, (k0780, ))


async def s1792(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1793(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1794)
    elif r.prova((k0755, )):
        await r.sotto(s1803)
    elif r.prova((k0757, )):
        await r.sotto(s1812)
    elif r.prova((k0758, )):
        await r.sotto(s1821)


async def s1794(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1795)
    elif r.prova((k0748, )):
        await r.sotto(s1797)
    elif r.prova((k0749, )):
        await r.sotto(s1799)
    elif r.prova((k0750, )):
        await r.sotto(s1801)


async def s1795(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1796, (k0780, ))


async def s1796(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1797(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1798, (k0747, ))


async def s1798(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1799(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1800, (k0780, ))


async def s1800(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1801(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1802, (k0780, ))


async def s1802(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1803(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1804)
    elif r.prova((k0748, )):
        await r.sotto(s1806)
    elif r.prova((k0749, )):
        await r.sotto(s1808)
    elif r.prova((k0750, )):
        await r.sotto(s1810)


async def s1804(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1805, (k0747, ))


async def s1805(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1806(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1807, (k0747, ))


async def s1807(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1808(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1809, (k0780, ))


async def s1809(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1810(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1811, (k0780, ))


async def s1811(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1812(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1813)
    elif r.prova((k0748, )):
        await r.sotto(s1815)
    elif r.prova((k0749, )):
        await r.sotto(s1817)
    elif r.prova((k0750, )):
        await r.sotto(s1819)


async def s1813(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1814, (k0780, ))


async def s1814(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1815(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1816, (k0780, ))


async def s1816(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1817(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1818, (k0780, ))


async def s1818(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1819(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1820, (k0780, ))


async def s1820(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1821(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1822)
    elif r.prova((k0748, )):
        await r.sotto(s1824)
    elif r.prova((k0749, )):
        await r.sotto(s1826)
    elif r.prova((k0750, )):
        await r.sotto(s1828)


async def s1822(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1823, (k0780, ))


async def s1823(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1824(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1825, (k0780, ))


async def s1825(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1826(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1827, (k0780, ))


async def s1827(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1828(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1829, (k0780, ))


async def s1829(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1830(r):
    # script vmc_master_calendario_fascia_1_on > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s1831(r):
    # script vmc_master_calendario_fascia_2_on
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]}, alias='La Fascia prevale sul ripristino di un Black-Out rilevato prima della Fascia (memoria del Black-Out spenta) [Foglio Logiche A23 e A25]')
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]}, alias='Ogni avvio della Fascia decide di nuovo se il comando viene eseguito (Spia Comando non eseguito del Calendario OFF)')
    await r.pausa(timedelta(days=0, seconds=5, microseconds=0))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    if not r.passo_condizione(k0744, 'Ritorno della VMC dopo un comando non eseguito: la Fascia riparte solo se la velocità della VMC non è cambiata nel frattempo (una velocità scelta, per esempio con il telecomando, si rispetta); controllo fatto dopo i 5 s, con le letture già aggiornate'):
        return
    r.verifica()
    if r.prova((k0795, )):
        await r.sotto(s1832)
    elif r.prova((k0797, )):
        await r.sotto(s1869)
    elif r.prova((k0799, )):
        await r.sotto(s1906)
    elif r.prova((k0801, )):
        await r.sotto(s1943)
    elif r.prova((k0803, )):
        await r.sotto(s1980)
    elif r.prova((k0805, )):
        await r.sotto(s2017)
    elif r.prova((k0807, )):
        await r.sotto(s2054)
    elif r.prova((k0809, )):
        await r.sotto(s2091)
    r.verifica()
    if r.prova((k0793, )):
        await r.sotto(s2251)


async def s1832(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1833)
    elif r.prova((k0755, )):
        await r.sotto(s1842)
    elif r.prova((k0757, )):
        await r.sotto(s1851)
    elif r.prova((k0758, )):
        await r.sotto(s1860)


async def s1833(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1834)
    elif r.prova((k0748, )):
        await r.sotto(s1836)
    elif r.prova((k0749, )):
        await r.sotto(s1838)
    elif r.prova((k0750, )):
        await r.sotto(s1840)


async def s1834(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1835, (k0745, ))


async def s1835(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1836(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1837, (k0747, ))


async def s1837(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1838(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1839, (k0745, ))


async def s1839(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1840(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1841, (k0747, ))


async def s1841(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1842(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1843)
    elif r.prova((k0748, )):
        await r.sotto(s1845)
    elif r.prova((k0749, )):
        await r.sotto(s1847)
    elif r.prova((k0750, )):
        await r.sotto(s1849)


async def s1843(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1844, (k0747, ))


async def s1844(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1845(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1846, (k0747, ))


async def s1846(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1847(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1848, (k0747, ))


async def s1848(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1849(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1850, (k0747, ))


async def s1850(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1851(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1852)
    elif r.prova((k0748, )):
        await r.sotto(s1854)
    elif r.prova((k0749, )):
        await r.sotto(s1856)
    elif r.prova((k0750, )):
        await r.sotto(s1858)


async def s1852(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1853, (k0745, ))


async def s1853(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1854(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1855, (k0747, ))


async def s1855(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1856(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1857, (k0745, ))


async def s1857(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1858(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1859, (k0747, ))


async def s1859(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1860(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1861)
    elif r.prova((k0748, )):
        await r.sotto(s1863)
    elif r.prova((k0749, )):
        await r.sotto(s1865)
    elif r.prova((k0750, )):
        await r.sotto(s1867)


async def s1861(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1862, (k0747, ))


async def s1862(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1863(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1864, (k0747, ))


async def s1864(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1865(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1866, (k0747, ))


async def s1866(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1867(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1868, (k0747, ))


async def s1868(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1869(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1870)
    elif r.prova((k0755, )):
        await r.sotto(s1879)
    elif r.prova((k0757, )):
        await r.sotto(s1888)
    elif r.prova((k0758, )):
        await r.sotto(s1897)


async def s1870(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1871)
    elif r.prova((k0748, )):
        await r.sotto(s1873)
    elif r.prova((k0749, )):
        await r.sotto(s1875)
    elif r.prova((k0750, )):
        await r.sotto(s1877)


async def s1871(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1872, (k0745, ))


async def s1872(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1873(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1874, (k0747, ))


async def s1874(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1875(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1876, (k0745, ))


async def s1876(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1877(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1878, (k0745, ))


async def s1878(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1879(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1880)
    elif r.prova((k0748, )):
        await r.sotto(s1882)
    elif r.prova((k0749, )):
        await r.sotto(s1884)
    elif r.prova((k0750, )):
        await r.sotto(s1886)


async def s1880(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1881, (k0747, ))


async def s1881(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1882(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1883, (k0747, ))


async def s1883(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1884(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1885, (k0745, ))


async def s1885(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1886(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1887, (k0745, ))


async def s1887(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1888(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1889)
    elif r.prova((k0748, )):
        await r.sotto(s1891)
    elif r.prova((k0749, )):
        await r.sotto(s1893)
    elif r.prova((k0750, )):
        await r.sotto(s1895)


async def s1889(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1890, (k0745, ))


async def s1890(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1891(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1892, (k0745, ))


async def s1892(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1893(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1894, (k0745, ))


async def s1894(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1895(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1896, (k0745, ))


async def s1896(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1897(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1898)
    elif r.prova((k0748, )):
        await r.sotto(s1900)
    elif r.prova((k0749, )):
        await r.sotto(s1902)
    elif r.prova((k0750, )):
        await r.sotto(s1904)


async def s1898(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1899, (k0745, ))


async def s1899(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1900(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1901, (k0745, ))


async def s1901(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1902(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1903, (k0745, ))


async def s1903(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1904(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1905, (k0745, ))


async def s1905(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1906(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1907)
    elif r.prova((k0755, )):
        await r.sotto(s1916)
    elif r.prova((k0757, )):
        await r.sotto(s1925)
    elif r.prova((k0758, )):
        await r.sotto(s1934)


async def s1907(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1908)
    elif r.prova((k0748, )):
        await r.sotto(s1910)
    elif r.prova((k0749, )):
        await r.sotto(s1912)
    elif r.prova((k0750, )):
        await r.sotto(s1914)


async def s1908(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1909, (k0764, ))


async def s1909(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1910(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1911, (k0747, ))


async def s1911(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1912(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1913, (k0764, ))


async def s1913(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1914(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1915, (k0764, ))


async def s1915(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1916(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1917)
    elif r.prova((k0748, )):
        await r.sotto(s1919)
    elif r.prova((k0749, )):
        await r.sotto(s1921)
    elif r.prova((k0750, )):
        await r.sotto(s1923)


async def s1917(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1918, (k0747, ))


async def s1918(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1919(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1920, (k0747, ))


async def s1920(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1921(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1922, (k0764, ))


async def s1922(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1923(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1924, (k0764, ))


async def s1924(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1925(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1926)
    elif r.prova((k0748, )):
        await r.sotto(s1928)
    elif r.prova((k0749, )):
        await r.sotto(s1930)
    elif r.prova((k0750, )):
        await r.sotto(s1932)


async def s1926(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1927, (k0764, ))


async def s1927(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1928(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1929, (k0764, ))


async def s1929(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1930(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1931, (k0764, ))


async def s1931(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1932(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1933, (k0764, ))


async def s1933(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1934(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1935)
    elif r.prova((k0748, )):
        await r.sotto(s1937)
    elif r.prova((k0749, )):
        await r.sotto(s1939)
    elif r.prova((k0750, )):
        await r.sotto(s1941)


async def s1935(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1936, (k0764, ))


async def s1936(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1937(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1938, (k0764, ))


async def s1938(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1939(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1940, (k0764, ))


async def s1940(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1941(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1942, (k0764, ))


async def s1942(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1943(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1944)
    elif r.prova((k0755, )):
        await r.sotto(s1953)
    elif r.prova((k0757, )):
        await r.sotto(s1962)
    elif r.prova((k0758, )):
        await r.sotto(s1971)


async def s1944(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1945)
    elif r.prova((k0748, )):
        await r.sotto(s1947)
    elif r.prova((k0749, )):
        await r.sotto(s1949)
    elif r.prova((k0750, )):
        await r.sotto(s1951)


async def s1945(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1946, (k0767, ))


async def s1946(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1947(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1948, (k0747, ))


async def s1948(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1949(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1950, (k0767, ))


async def s1950(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1951(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1952, (k0767, ))


async def s1952(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1953(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1954)
    elif r.prova((k0748, )):
        await r.sotto(s1956)
    elif r.prova((k0749, )):
        await r.sotto(s1958)
    elif r.prova((k0750, )):
        await r.sotto(s1960)


async def s1954(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1955, (k0747, ))


async def s1955(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1956(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1957, (k0747, ))


async def s1957(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1958(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1959, (k0767, ))


async def s1959(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1960(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1961, (k0767, ))


async def s1961(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1962(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1963)
    elif r.prova((k0748, )):
        await r.sotto(s1965)
    elif r.prova((k0749, )):
        await r.sotto(s1967)
    elif r.prova((k0750, )):
        await r.sotto(s1969)


async def s1963(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1964, (k0767, ))


async def s1964(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1965(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1966, (k0767, ))


async def s1966(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1967(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1968, (k0767, ))


async def s1968(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1969(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1970, (k0767, ))


async def s1970(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1971(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1972)
    elif r.prova((k0748, )):
        await r.sotto(s1974)
    elif r.prova((k0749, )):
        await r.sotto(s1976)
    elif r.prova((k0750, )):
        await r.sotto(s1978)


async def s1972(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1973, (k0767, ))


async def s1973(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1974(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1975, (k0767, ))


async def s1975(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1976(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1977, (k0767, ))


async def s1977(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1978(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1979, (k0767, ))


async def s1979(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1980(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1981)
    elif r.prova((k0755, )):
        await r.sotto(s1990)
    elif r.prova((k0757, )):
        await r.sotto(s1999)
    elif r.prova((k0758, )):
        await r.sotto(s2008)


async def s1981(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1982)
    elif r.prova((k0748, )):
        await r.sotto(s1984)
    elif r.prova((k0749, )):
        await r.sotto(s1986)
    elif r.prova((k0750, )):
        await r.sotto(s1988)


async def s1982(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1983, (k0770, ))


async def s1983(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1984(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1985, (k0747, ))


async def s1985(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1986(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1987, (k0770, ))


async def s1987(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1988(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1989, (k0770, ))


async def s1989(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1990(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1991)
    elif r.prova((k0748, )):
        await r.sotto(s1993)
    elif r.prova((k0749, )):
        await r.sotto(s1995)
    elif r.prova((k0750, )):
        await r.sotto(s1997)


async def s1991(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1992, (k0747, ))


async def s1992(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1993(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1994, (k0747, ))


async def s1994(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1995(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1996, (k0770, ))


async def s1996(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1997(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1998, (k0770, ))


async def s1998(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1999(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2000)
    elif r.prova((k0748, )):
        await r.sotto(s2002)
    elif r.prova((k0749, )):
        await r.sotto(s2004)
    elif r.prova((k0750, )):
        await r.sotto(s2006)


async def s2000(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2001, (k0770, ))


async def s2001(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2002(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2003, (k0770, ))


async def s2003(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2004(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2005, (k0770, ))


async def s2005(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2006(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2007, (k0770, ))


async def s2007(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2008(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2009)
    elif r.prova((k0748, )):
        await r.sotto(s2011)
    elif r.prova((k0749, )):
        await r.sotto(s2013)
    elif r.prova((k0750, )):
        await r.sotto(s2015)


async def s2009(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2010, (k0770, ))


async def s2010(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2011(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2012, (k0770, ))


async def s2012(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2013(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2014, (k0770, ))


async def s2014(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2015(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2016, (k0770, ))


async def s2016(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2017(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s2018)
    elif r.prova((k0755, )):
        await r.sotto(s2027)
    elif r.prova((k0757, )):
        await r.sotto(s2036)
    elif r.prova((k0758, )):
        await r.sotto(s2045)


async def s2018(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2019)
    elif r.prova((k0748, )):
        await r.sotto(s2021)
    elif r.prova((k0749, )):
        await r.sotto(s2023)
    elif r.prova((k0750, )):
        await r.sotto(s2025)


async def s2019(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2020, (k0773, ))


async def s2020(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2021(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2022, (k0747, ))


async def s2022(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2023(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2024, (k0773, ))


async def s2024(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2025(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2026, (k0773, ))


async def s2026(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2027(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2028)
    elif r.prova((k0748, )):
        await r.sotto(s2030)
    elif r.prova((k0749, )):
        await r.sotto(s2032)
    elif r.prova((k0750, )):
        await r.sotto(s2034)


async def s2028(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2029, (k0747, ))


async def s2029(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2030(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2031, (k0747, ))


async def s2031(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2032(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2033, (k0773, ))


async def s2033(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2034(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2035, (k0773, ))


async def s2035(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2036(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2037)
    elif r.prova((k0748, )):
        await r.sotto(s2039)
    elif r.prova((k0749, )):
        await r.sotto(s2041)
    elif r.prova((k0750, )):
        await r.sotto(s2043)


async def s2037(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2038, (k0773, ))


async def s2038(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2039(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2040, (k0773, ))


async def s2040(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2041(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2042, (k0773, ))


async def s2042(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2043(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2044, (k0773, ))


async def s2044(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2045(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2046)
    elif r.prova((k0748, )):
        await r.sotto(s2048)
    elif r.prova((k0749, )):
        await r.sotto(s2050)
    elif r.prova((k0750, )):
        await r.sotto(s2052)


async def s2046(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2047, (k0773, ))


async def s2047(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2048(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2049, (k0773, ))


async def s2049(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2050(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2051, (k0773, ))


async def s2051(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2052(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2053, (k0773, ))


async def s2053(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2054(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s2055)
    elif r.prova((k0755, )):
        await r.sotto(s2064)
    elif r.prova((k0757, )):
        await r.sotto(s2073)
    elif r.prova((k0758, )):
        await r.sotto(s2082)


async def s2055(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2056)
    elif r.prova((k0748, )):
        await r.sotto(s2058)
    elif r.prova((k0749, )):
        await r.sotto(s2060)
    elif r.prova((k0750, )):
        await r.sotto(s2062)


async def s2056(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2057, (k0776, ))


async def s2057(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2058(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2059, (k0747, ))


async def s2059(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2060(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2061, (k0776, ))


async def s2061(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2062(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2063, (k0776, ))


async def s2063(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2064(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2065)
    elif r.prova((k0748, )):
        await r.sotto(s2067)
    elif r.prova((k0749, )):
        await r.sotto(s2069)
    elif r.prova((k0750, )):
        await r.sotto(s2071)


async def s2065(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2066, (k0747, ))


async def s2066(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2067(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2068, (k0747, ))


async def s2068(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2069(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2070, (k0776, ))


async def s2070(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2071(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2072, (k0776, ))


async def s2072(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2073(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2074)
    elif r.prova((k0748, )):
        await r.sotto(s2076)
    elif r.prova((k0749, )):
        await r.sotto(s2078)
    elif r.prova((k0750, )):
        await r.sotto(s2080)


async def s2074(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2075, (k0776, ))


async def s2075(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2076(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2077, (k0776, ))


async def s2077(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2078(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2079, (k0776, ))


async def s2079(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2080(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2081, (k0776, ))


async def s2081(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2082(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s2083)
    elif r.prova((k0748, )):
        await r.sotto(s2085)
    elif r.prova((k0749, )):
        await r.sotto(s2087)
    elif r.prova((k0750, )):
        await r.sotto(s2089)


async def s2083(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2084, (k0776, ))


async def s2084(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2085(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2086, (k0776, ))


async def s2086(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2087(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2088, (k0776, ))


async def s2088(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2089(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2090, (k0776, ))


async def s2090(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2091(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0782, )):
        await r.sotto(s2092)
    elif r.prova((k0789, )):
        await r.sotto(s2167)
    elif r.prova((k0790, )):
        await r.sotto(s2214)


async def s2092(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0779, )):
        await r.sotto(s2093)
    elif r.prova((k0781, )):
        await r.sotto(s2130)
