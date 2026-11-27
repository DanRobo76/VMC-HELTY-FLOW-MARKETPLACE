"""Automazioni e script del package, tradotti in Python (parte 7 di 8).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from datetime import time, timedelta

from .. import condizioni as C
from ..definizioni import Automazione, Comando, Script
from ..esecuzione import Annulla, Ferma, Modello
from . import modelli as M
from .motore_01 import (
    k0743, k0744, k0745, k0746, k0747, k0748, k0749, k0752, k0754, k0756,
    k0757, k0763, k0766, k0769, k0772, k0775, k0778, k0779, k0780, k0781,
    k0782, k0783, k0784, k0785, k0786, k0787, k0788, k0789, k0792, k0794,
    k0796, k0798, k0800, k0802, k0804, k0806, k0808,
)
from .motore_08 import (
    s2100, s2102, s2111, s2120, s2129, s2166, s2213, s2250,
)


async def s1659(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1660(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1661)
    elif r.prova((k0747, )):
        await r.sotto(s1663)
    elif r.prova((k0748, )):
        await r.sotto(s1665)
    elif r.prova((k0749, )):
        await r.sotto(s1667)


async def s1661(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1662, (k0775, ))


async def s1662(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1663(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1664, (k0775, ))


async def s1664(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1665(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1666, (k0775, ))


async def s1666(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1667(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1668, (k0775, ))


async def s1668(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1669(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0781, )):
        await r.sotto(s1670)
    elif r.prova((k0788, )):
        await r.sotto(s1745)
    elif r.prova((k0789, )):
        await r.sotto(s1792)


async def s1670(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0778, )):
        await r.sotto(s1671)
    elif r.prova((k0780, )):
        await r.sotto(s1708)


async def s1671(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1672)
    elif r.prova((k0754, )):
        await r.sotto(s1681)
    elif r.prova((k0756, )):
        await r.sotto(s1690)
    elif r.prova((k0757, )):
        await r.sotto(s1699)


async def s1672(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1673)
    elif r.prova((k0747, )):
        await r.sotto(s1675)
    elif r.prova((k0748, )):
        await r.sotto(s1677)
    elif r.prova((k0749, )):
        await r.sotto(s1679)


async def s1673(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1674, (k0744, ))


async def s1674(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1675(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1676, (k0746, ))


async def s1676(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1677(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1678, (k0744, ))


async def s1678(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1679(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1680, (k0746, ))


async def s1680(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1681(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1682)
    elif r.prova((k0747, )):
        await r.sotto(s1684)
    elif r.prova((k0748, )):
        await r.sotto(s1686)
    elif r.prova((k0749, )):
        await r.sotto(s1688)


async def s1682(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1683, (k0746, ))


async def s1683(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1684(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1685, (k0746, ))


async def s1685(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1686(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1687, (k0746, ))


async def s1687(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1688(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1689, (k0746, ))


async def s1689(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 1 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1690(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1691)
    elif r.prova((k0747, )):
        await r.sotto(s1693)
    elif r.prova((k0748, )):
        await r.sotto(s1695)
    elif r.prova((k0749, )):
        await r.sotto(s1697)


async def s1691(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1692, (k0744, ))


async def s1692(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1693(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1694, (k0746, ))


async def s1694(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1695(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1696, (k0744, ))


async def s1696(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1697(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1698, (k0746, ))


async def s1698(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 2 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1699(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1700)
    elif r.prova((k0747, )):
        await r.sotto(s1702)
    elif r.prova((k0748, )):
        await r.sotto(s1704)
    elif r.prova((k0749, )):
        await r.sotto(s1706)


async def s1700(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1701, (k0746, ))


async def s1701(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1702(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1703, (k0746, ))


async def s1703(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1704(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1705, (k0746, ))


async def s1705(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1706(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    await r.ripeti_finche(s1707, (k0746, ))


async def s1707(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 3 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1708(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1709)
    elif r.prova((k0754, )):
        await r.sotto(s1718)
    elif r.prova((k0756, )):
        await r.sotto(s1727)
    elif r.prova((k0757, )):
        await r.sotto(s1736)


async def s1709(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1710)
    elif r.prova((k0747, )):
        await r.sotto(s1712)
    elif r.prova((k0748, )):
        await r.sotto(s1714)
    elif r.prova((k0749, )):
        await r.sotto(s1716)


async def s1710(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1711, (k0779, ))


async def s1711(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1712(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1713, (k0746, ))


async def s1713(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1714(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1715, (k0779, ))


async def s1715(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1716(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1717, (k0779, ))


async def s1717(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1718(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1719)
    elif r.prova((k0747, )):
        await r.sotto(s1721)
    elif r.prova((k0748, )):
        await r.sotto(s1723)
    elif r.prova((k0749, )):
        await r.sotto(s1725)


async def s1719(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1720, (k0746, ))


async def s1720(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1721(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1722, (k0746, ))


async def s1722(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1723(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1724, (k0779, ))


async def s1724(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1725(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1726, (k0779, ))


async def s1726(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1727(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1728)
    elif r.prova((k0747, )):
        await r.sotto(s1730)
    elif r.prova((k0748, )):
        await r.sotto(s1732)
    elif r.prova((k0749, )):
        await r.sotto(s1734)


async def s1728(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1729, (k0779, ))


async def s1729(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1730(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1731, (k0779, ))


async def s1731(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1732(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1733, (k0779, ))


async def s1733(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1734(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1735, (k0779, ))


async def s1735(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1736(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1737)
    elif r.prova((k0747, )):
        await r.sotto(s1739)
    elif r.prova((k0748, )):
        await r.sotto(s1741)
    elif r.prova((k0749, )):
        await r.sotto(s1743)


async def s1737(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1738, (k0779, ))


async def s1738(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1739(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1740, (k0779, ))


async def s1740(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1741(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1742, (k0779, ))


async def s1742(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1743(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1744, (k0779, ))


async def s1744(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 0 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1745(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0786, )):
        await r.sotto(s1746)
    elif r.prova((k0787, )):
        await r.sotto(s1755)


async def s1746(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0782, )):
        await r.sotto(s1747)
    elif r.prova((k0783, )):
        await r.sotto(s1749)
    elif r.prova((k0784, )):
        await r.sotto(s1751)
    elif r.prova((k0785, )):
        await r.sotto(s1753)


async def s1747(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s1748, (k0744, ))


async def s1748(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1749(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1750, (k0746, ))


async def s1750(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1751(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1752, (k0744, ))


async def s1752(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1753(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    await r.ripeti_finche(s1754, (k0746, ))


async def s1754(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 0 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1755(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1756)
    elif r.prova((k0754, )):
        await r.sotto(s1765)
    elif r.prova((k0756, )):
        await r.sotto(s1774)
    elif r.prova((k0757, )):
        await r.sotto(s1783)


async def s1756(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1757)
    elif r.prova((k0747, )):
        await r.sotto(s1759)
    elif r.prova((k0748, )):
        await r.sotto(s1761)
    elif r.prova((k0749, )):
        await r.sotto(s1763)


async def s1757(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1758, (k0779, ))


async def s1758(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1759(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1760, (k0746, ))


async def s1760(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1761(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1762, (k0779, ))


async def s1762(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1763(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1764, (k0779, ))


async def s1764(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1765(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1766)
    elif r.prova((k0747, )):
        await r.sotto(s1768)
    elif r.prova((k0748, )):
        await r.sotto(s1770)
    elif r.prova((k0749, )):
        await r.sotto(s1772)


async def s1766(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1767, (k0746, ))


async def s1767(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1768(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1769, (k0746, ))


async def s1769(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1770(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1771, (k0779, ))


async def s1771(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1772(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1773, (k0779, ))


async def s1773(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1774(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1775)
    elif r.prova((k0747, )):
        await r.sotto(s1777)
    elif r.prova((k0748, )):
        await r.sotto(s1779)
    elif r.prova((k0749, )):
        await r.sotto(s1781)


async def s1775(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1776, (k0779, ))


async def s1776(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1777(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1778, (k0779, ))


async def s1778(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1779(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1780, (k0779, ))


async def s1780(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1781(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1782, (k0779, ))


async def s1782(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1783(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1784)
    elif r.prova((k0747, )):
        await r.sotto(s1786)
    elif r.prova((k0748, )):
        await r.sotto(s1788)
    elif r.prova((k0749, )):
        await r.sotto(s1790)


async def s1784(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1785, (k0779, ))


async def s1785(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1786(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1787, (k0779, ))


async def s1787(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1788(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1789, (k0779, ))


async def s1789(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1790(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1791, (k0779, ))


async def s1791(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 1 > 0 choose 1 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1792(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1793)
    elif r.prova((k0754, )):
        await r.sotto(s1802)
    elif r.prova((k0756, )):
        await r.sotto(s1811)
    elif r.prova((k0757, )):
        await r.sotto(s1820)


async def s1793(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1794)
    elif r.prova((k0747, )):
        await r.sotto(s1796)
    elif r.prova((k0748, )):
        await r.sotto(s1798)
    elif r.prova((k0749, )):
        await r.sotto(s1800)


async def s1794(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1795, (k0779, ))


async def s1795(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1796(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1797, (k0746, ))


async def s1797(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1798(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1799, (k0779, ))


async def s1799(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1800(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1801, (k0779, ))


async def s1801(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1802(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1803)
    elif r.prova((k0747, )):
        await r.sotto(s1805)
    elif r.prova((k0748, )):
        await r.sotto(s1807)
    elif r.prova((k0749, )):
        await r.sotto(s1809)


async def s1803(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1804, (k0746, ))


async def s1804(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1805(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1806, (k0746, ))


async def s1806(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1807(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1808, (k0779, ))


async def s1808(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1809(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1810, (k0779, ))


async def s1810(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1811(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1812)
    elif r.prova((k0747, )):
        await r.sotto(s1814)
    elif r.prova((k0748, )):
        await r.sotto(s1816)
    elif r.prova((k0749, )):
        await r.sotto(s1818)


async def s1812(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1813, (k0779, ))


async def s1813(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1814(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1815, (k0779, ))


async def s1815(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1816(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1817, (k0779, ))


async def s1817(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1818(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1819, (k0779, ))


async def s1819(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1820(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1821)
    elif r.prova((k0747, )):
        await r.sotto(s1823)
    elif r.prova((k0748, )):
        await r.sotto(s1825)
    elif r.prova((k0749, )):
        await r.sotto(s1827)


async def s1821(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1822, (k0779, ))


async def s1822(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1823(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1824, (k0779, ))


async def s1824(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1825(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1826, (k0779, ))


async def s1826(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1827(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1828, (k0779, ))


async def s1828(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 7 > 1 choose 2 > 0 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1829(r):
    # script vmc_master_calendario_fascia_1_on > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s1830(r):
    # script vmc_master_calendario_fascia_2_on
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]}, alias='La Fascia prevale sul ripristino di un Black-Out rilevato prima della Fascia (memoria del Black-Out spenta) [Foglio Logiche A23 e A25]')
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]}, alias='Ogni avvio della Fascia decide di nuovo se il comando viene eseguito (Spia Comando non eseguito del Calendario OFF)')
    await r.pausa(timedelta(days=0, seconds=5, microseconds=0))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    if not r.passo_condizione(k0743, 'Ritorno della VMC dopo un comando non eseguito: la Fascia riparte solo se la velocità della VMC non è cambiata nel frattempo (una velocità scelta, per esempio con il telecomando, si rispetta); controllo fatto dopo i 5 s, con le letture già aggiornate'):
        return
    r.verifica()
    if r.prova((k0794, )):
        await r.sotto(s1831)
    elif r.prova((k0796, )):
        await r.sotto(s1868)
    elif r.prova((k0798, )):
        await r.sotto(s1905)
    elif r.prova((k0800, )):
        await r.sotto(s1942)
    elif r.prova((k0802, )):
        await r.sotto(s1979)
    elif r.prova((k0804, )):
        await r.sotto(s2016)
    elif r.prova((k0806, )):
        await r.sotto(s2053)
    elif r.prova((k0808, )):
        await r.sotto(s2090)
    r.verifica()
    if r.prova((k0792, )):
        await r.sotto(s2250)


async def s1831(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1832)
    elif r.prova((k0754, )):
        await r.sotto(s1841)
    elif r.prova((k0756, )):
        await r.sotto(s1850)
    elif r.prova((k0757, )):
        await r.sotto(s1859)


async def s1832(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1833)
    elif r.prova((k0747, )):
        await r.sotto(s1835)
    elif r.prova((k0748, )):
        await r.sotto(s1837)
    elif r.prova((k0749, )):
        await r.sotto(s1839)


async def s1833(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1834, (k0744, ))


async def s1834(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1835(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1836, (k0746, ))


async def s1836(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1837(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1838, (k0744, ))


async def s1838(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1839(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1840, (k0746, ))


async def s1840(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1841(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1842)
    elif r.prova((k0747, )):
        await r.sotto(s1844)
    elif r.prova((k0748, )):
        await r.sotto(s1846)
    elif r.prova((k0749, )):
        await r.sotto(s1848)


async def s1842(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1843, (k0746, ))


async def s1843(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1844(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1845, (k0746, ))


async def s1845(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1846(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1847, (k0746, ))


async def s1847(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1848(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1849, (k0746, ))


async def s1849(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1850(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1851)
    elif r.prova((k0747, )):
        await r.sotto(s1853)
    elif r.prova((k0748, )):
        await r.sotto(s1855)
    elif r.prova((k0749, )):
        await r.sotto(s1857)


async def s1851(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1852, (k0744, ))


async def s1852(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1853(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1854, (k0746, ))


async def s1854(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1855(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1856, (k0744, ))


async def s1856(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1857(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1858, (k0746, ))


async def s1858(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1859(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1860)
    elif r.prova((k0747, )):
        await r.sotto(s1862)
    elif r.prova((k0748, )):
        await r.sotto(s1864)
    elif r.prova((k0749, )):
        await r.sotto(s1866)


async def s1860(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1861, (k0746, ))


async def s1861(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1862(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1863, (k0746, ))


async def s1863(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1864(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1865, (k0746, ))


async def s1865(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1866(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1867, (k0746, ))


async def s1867(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 0 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1868(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1869)
    elif r.prova((k0754, )):
        await r.sotto(s1878)
    elif r.prova((k0756, )):
        await r.sotto(s1887)
    elif r.prova((k0757, )):
        await r.sotto(s1896)


async def s1869(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1870)
    elif r.prova((k0747, )):
        await r.sotto(s1872)
    elif r.prova((k0748, )):
        await r.sotto(s1874)
    elif r.prova((k0749, )):
        await r.sotto(s1876)


async def s1870(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1871, (k0744, ))


async def s1871(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1872(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1873, (k0746, ))


async def s1873(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1874(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1875, (k0744, ))


async def s1875(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1876(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1877, (k0744, ))


async def s1877(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1878(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1879)
    elif r.prova((k0747, )):
        await r.sotto(s1881)
    elif r.prova((k0748, )):
        await r.sotto(s1883)
    elif r.prova((k0749, )):
        await r.sotto(s1885)


async def s1879(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1880, (k0746, ))


async def s1880(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1881(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1882, (k0746, ))


async def s1882(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1883(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1884, (k0744, ))


async def s1884(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1885(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1886, (k0744, ))


async def s1886(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1887(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1888)
    elif r.prova((k0747, )):
        await r.sotto(s1890)
    elif r.prova((k0748, )):
        await r.sotto(s1892)
    elif r.prova((k0749, )):
        await r.sotto(s1894)


async def s1888(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1889, (k0744, ))


async def s1889(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1890(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1891, (k0744, ))


async def s1891(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1892(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1893, (k0744, ))


async def s1893(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1894(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1895, (k0744, ))


async def s1895(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1896(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1897)
    elif r.prova((k0747, )):
        await r.sotto(s1899)
    elif r.prova((k0748, )):
        await r.sotto(s1901)
    elif r.prova((k0749, )):
        await r.sotto(s1903)


async def s1897(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1898, (k0744, ))


async def s1898(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1899(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1900, (k0744, ))


async def s1900(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1901(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1902, (k0744, ))


async def s1902(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1903(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1904, (k0744, ))


async def s1904(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 1 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1905(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1906)
    elif r.prova((k0754, )):
        await r.sotto(s1915)
    elif r.prova((k0756, )):
        await r.sotto(s1924)
    elif r.prova((k0757, )):
        await r.sotto(s1933)


async def s1906(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1907)
    elif r.prova((k0747, )):
        await r.sotto(s1909)
    elif r.prova((k0748, )):
        await r.sotto(s1911)
    elif r.prova((k0749, )):
        await r.sotto(s1913)


async def s1907(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1908, (k0763, ))


async def s1908(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1909(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1910, (k0746, ))


async def s1910(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1911(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1912, (k0763, ))


async def s1912(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1913(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1914, (k0763, ))


async def s1914(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1915(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1916)
    elif r.prova((k0747, )):
        await r.sotto(s1918)
    elif r.prova((k0748, )):
        await r.sotto(s1920)
    elif r.prova((k0749, )):
        await r.sotto(s1922)


async def s1916(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1917, (k0746, ))


async def s1917(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1918(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1919, (k0746, ))


async def s1919(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1920(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1921, (k0763, ))


async def s1921(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1922(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1923, (k0763, ))


async def s1923(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1924(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1925)
    elif r.prova((k0747, )):
        await r.sotto(s1927)
    elif r.prova((k0748, )):
        await r.sotto(s1929)
    elif r.prova((k0749, )):
        await r.sotto(s1931)


async def s1925(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1926, (k0763, ))


async def s1926(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1927(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1928, (k0763, ))


async def s1928(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1929(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1930, (k0763, ))


async def s1930(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1931(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1932, (k0763, ))


async def s1932(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1933(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1934)
    elif r.prova((k0747, )):
        await r.sotto(s1936)
    elif r.prova((k0748, )):
        await r.sotto(s1938)
    elif r.prova((k0749, )):
        await r.sotto(s1940)


async def s1934(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1935, (k0763, ))


async def s1935(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1936(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1937, (k0763, ))


async def s1937(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1938(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1939, (k0763, ))


async def s1939(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1940(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1941, (k0763, ))


async def s1941(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 2 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1942(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1943)
    elif r.prova((k0754, )):
        await r.sotto(s1952)
    elif r.prova((k0756, )):
        await r.sotto(s1961)
    elif r.prova((k0757, )):
        await r.sotto(s1970)


async def s1943(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1944)
    elif r.prova((k0747, )):
        await r.sotto(s1946)
    elif r.prova((k0748, )):
        await r.sotto(s1948)
    elif r.prova((k0749, )):
        await r.sotto(s1950)


async def s1944(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1945, (k0766, ))


async def s1945(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1946(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1947, (k0746, ))


async def s1947(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1948(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1949, (k0766, ))


async def s1949(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1950(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1951, (k0766, ))


async def s1951(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1952(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1953)
    elif r.prova((k0747, )):
        await r.sotto(s1955)
    elif r.prova((k0748, )):
        await r.sotto(s1957)
    elif r.prova((k0749, )):
        await r.sotto(s1959)


async def s1953(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1954, (k0746, ))


async def s1954(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1955(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1956, (k0746, ))


async def s1956(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1957(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1958, (k0766, ))


async def s1958(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1959(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1960, (k0766, ))


async def s1960(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1961(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1962)
    elif r.prova((k0747, )):
        await r.sotto(s1964)
    elif r.prova((k0748, )):
        await r.sotto(s1966)
    elif r.prova((k0749, )):
        await r.sotto(s1968)


async def s1962(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1963, (k0766, ))


async def s1963(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1964(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1965, (k0766, ))


async def s1965(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1966(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1967, (k0766, ))


async def s1967(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1968(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1969, (k0766, ))


async def s1969(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1970(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1971)
    elif r.prova((k0747, )):
        await r.sotto(s1973)
    elif r.prova((k0748, )):
        await r.sotto(s1975)
    elif r.prova((k0749, )):
        await r.sotto(s1977)


async def s1971(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1972, (k0766, ))


async def s1972(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1973(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1974, (k0766, ))


async def s1974(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1975(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1976, (k0766, ))


async def s1976(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1977(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1978, (k0766, ))


async def s1978(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 3 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1979(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s1980)
    elif r.prova((k0754, )):
        await r.sotto(s1989)
    elif r.prova((k0756, )):
        await r.sotto(s1998)
    elif r.prova((k0757, )):
        await r.sotto(s2007)


async def s1980(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1981)
    elif r.prova((k0747, )):
        await r.sotto(s1983)
    elif r.prova((k0748, )):
        await r.sotto(s1985)
    elif r.prova((k0749, )):
        await r.sotto(s1987)


async def s1981(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1982, (k0769, ))


async def s1982(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1983(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1984, (k0746, ))


async def s1984(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1985(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1986, (k0769, ))


async def s1986(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1987(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1988, (k0769, ))


async def s1988(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1989(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1990)
    elif r.prova((k0747, )):
        await r.sotto(s1992)
    elif r.prova((k0748, )):
        await r.sotto(s1994)
    elif r.prova((k0749, )):
        await r.sotto(s1996)


async def s1990(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1991, (k0746, ))


async def s1991(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1992(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1993, (k0746, ))


async def s1993(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1994(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1995, (k0769, ))


async def s1995(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1996(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1997, (k0769, ))


async def s1997(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1998(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s1999)
    elif r.prova((k0747, )):
        await r.sotto(s2001)
    elif r.prova((k0748, )):
        await r.sotto(s2003)
    elif r.prova((k0749, )):
        await r.sotto(s2005)


async def s1999(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2000, (k0769, ))


async def s2000(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2001(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2002, (k0769, ))


async def s2002(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2003(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2004, (k0769, ))


async def s2004(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2005(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2006, (k0769, ))


async def s2006(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2007(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2008)
    elif r.prova((k0747, )):
        await r.sotto(s2010)
    elif r.prova((k0748, )):
        await r.sotto(s2012)
    elif r.prova((k0749, )):
        await r.sotto(s2014)


async def s2008(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2009, (k0769, ))


async def s2009(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2010(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2011, (k0769, ))


async def s2011(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2012(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2013, (k0769, ))


async def s2013(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2014(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2015, (k0769, ))


async def s2015(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 4 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2016(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s2017)
    elif r.prova((k0754, )):
        await r.sotto(s2026)
    elif r.prova((k0756, )):
        await r.sotto(s2035)
    elif r.prova((k0757, )):
        await r.sotto(s2044)


async def s2017(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2018)
    elif r.prova((k0747, )):
        await r.sotto(s2020)
    elif r.prova((k0748, )):
        await r.sotto(s2022)
    elif r.prova((k0749, )):
        await r.sotto(s2024)


async def s2018(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2019, (k0772, ))


async def s2019(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2020(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2021, (k0746, ))


async def s2021(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2022(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2023, (k0772, ))


async def s2023(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2024(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2025, (k0772, ))


async def s2025(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2026(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2027)
    elif r.prova((k0747, )):
        await r.sotto(s2029)
    elif r.prova((k0748, )):
        await r.sotto(s2031)
    elif r.prova((k0749, )):
        await r.sotto(s2033)


async def s2027(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2028, (k0746, ))


async def s2028(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2029(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2030, (k0746, ))


async def s2030(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2031(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2032, (k0772, ))


async def s2032(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2033(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2034, (k0772, ))


async def s2034(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2035(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2036)
    elif r.prova((k0747, )):
        await r.sotto(s2038)
    elif r.prova((k0748, )):
        await r.sotto(s2040)
    elif r.prova((k0749, )):
        await r.sotto(s2042)


async def s2036(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2037, (k0772, ))


async def s2037(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2038(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2039, (k0772, ))


async def s2039(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2040(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2041, (k0772, ))


async def s2041(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2042(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2043, (k0772, ))


async def s2043(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2044(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2045)
    elif r.prova((k0747, )):
        await r.sotto(s2047)
    elif r.prova((k0748, )):
        await r.sotto(s2049)
    elif r.prova((k0749, )):
        await r.sotto(s2051)


async def s2045(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2046, (k0772, ))


async def s2046(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2047(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2048, (k0772, ))


async def s2048(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2049(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2050, (k0772, ))


async def s2050(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2051(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2052, (k0772, ))


async def s2052(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 5 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2053(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0752, )):
        await r.sotto(s2054)
    elif r.prova((k0754, )):
        await r.sotto(s2063)
    elif r.prova((k0756, )):
        await r.sotto(s2072)
    elif r.prova((k0757, )):
        await r.sotto(s2081)


async def s2054(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2055)
    elif r.prova((k0747, )):
        await r.sotto(s2057)
    elif r.prova((k0748, )):
        await r.sotto(s2059)
    elif r.prova((k0749, )):
        await r.sotto(s2061)


async def s2055(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2056, (k0775, ))


async def s2056(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2057(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2058, (k0746, ))


async def s2058(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2059(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2060, (k0775, ))


async def s2060(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2061(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2062, (k0775, ))


async def s2062(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2063(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2064)
    elif r.prova((k0747, )):
        await r.sotto(s2066)
    elif r.prova((k0748, )):
        await r.sotto(s2068)
    elif r.prova((k0749, )):
        await r.sotto(s2070)


async def s2064(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2065, (k0746, ))


async def s2065(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2066(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s2067, (k0746, ))


async def s2067(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2068(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2069, (k0775, ))


async def s2069(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2070(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2071, (k0775, ))


async def s2071(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2072(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2073)
    elif r.prova((k0747, )):
        await r.sotto(s2075)
    elif r.prova((k0748, )):
        await r.sotto(s2077)
    elif r.prova((k0749, )):
        await r.sotto(s2079)


async def s2073(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2074, (k0775, ))


async def s2074(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2075(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2076, (k0775, ))


async def s2076(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2077(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2078, (k0775, ))


async def s2078(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2079(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2080, (k0775, ))


async def s2080(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2081(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0745, )):
        await r.sotto(s2082)
    elif r.prova((k0747, )):
        await r.sotto(s2084)
    elif r.prova((k0748, )):
        await r.sotto(s2086)
    elif r.prova((k0749, )):
        await r.sotto(s2088)


async def s2082(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2083, (k0775, ))


async def s2083(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2084(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2085, (k0775, ))


async def s2085(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2086(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2087, (k0775, ))


async def s2087(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2088(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s2089, (k0775, ))


async def s2089(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 6 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s2090(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0781, )):
        await r.sotto(s2091)
    elif r.prova((k0788, )):
        await r.sotto(s2166)
    elif r.prova((k0789, )):
        await r.sotto(s2213)


async def s2091(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0778, )):
        await r.sotto(s2092)
    elif r.prova((k0780, )):
        await r.sotto(s2129)


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
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
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
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
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
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s2099, (k0744, ))


async def s2099(r):
    # script vmc_master_calendario_fascia_2_on > 5 choose 7 > 1 choose 0 > 0 choose 0 > 0 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
