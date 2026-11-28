"""Automazioni e script del package, tradotti in Python (parte 4 di 8).

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
    k0136, k0137, k0151, k0152, k0153, k0154, k0158, k0159, k0161, k0162,
    k0164, k0165, k0167, k0168, k0172, k0173, k0178, k0179, k0183, k0190,
    k0194, k0197, k0200, k0203, k0208, k0211, k0214, k0236, k0237, k0401,
    k0402, k0407, k0409, k0411, k0418, k0424, k0425, k0426, k0427, k0428,
    k0429, k0430, k0431, k0432, k0433, k0434, k0435, k0436, k0437, k0438,
    k0439, k0440, k0444, k0447, k0448, k0449, k0450, k0451, k0452, k0453,
    k0454, k0455, k0456, k0457, k0458, k0459, k0460, k0461, k0462, k0463,
    k0464, k0466, k0467, k0468, k0469, k0470, k0471, k0472, k0474, k0476,
    k0478, k0480, k0482, k0484, k0485, k0487, k0488, k0491, k0492, k0493,
    k0496, k0498, k0500, k0501, k0502, k0503, k0506, k0509, k0512, k0515,
    k0518, k0521, k0524,
)
from .motore_05 import (
    s0991, s0992, s0993, s0994, s0999, s1000, s1001,
)


async def s0697(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0698(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0699, (k0407, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0702, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s0703)
    else:
        await r.sotto(s0704)


async def s0699(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    if r.prova((k0401, k0402, )):
        await r.sotto(s0700)
    else:
        await r.sotto(s0701)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0700(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3 > 0 repeat > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})


async def s0701(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3 > 0 repeat > 1 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})


async def s0702(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0703(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0704(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 3 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0705(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0706, (k0409, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0709, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s0710)
    else:
        await r.sotto(s0711)


async def s0706(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    if r.prova((k0401, k0402, )):
        await r.sotto(s0707)
    else:
        await r.sotto(s0708)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0707(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4 > 0 repeat > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})


async def s0708(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4 > 0 repeat > 1 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})


async def s0709(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0710(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0711(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 4 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0712(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0713, (k0411, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0716, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s0717)
    else:
        await r.sotto(s0718)


async def s0713(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    if r.prova((k0401, k0402, )):
        await r.sotto(s0714)
    else:
        await r.sotto(s0715)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0714(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5 > 0 repeat > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})


async def s0715(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5 > 0 repeat > 1 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})


async def s0716(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0717(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0718(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 5 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0719(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 6
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0720, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0721)
    else:
        await r.sotto(s0722)


async def s0720(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 6 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0721(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 6 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0722(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 6 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0723(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 7
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0724, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0725)
    else:
        await r.sotto(s0726)


async def s0724(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 7 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0725(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 7 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0726(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 7 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0727(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 8
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})


async def s0728(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 9
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})


async def s0729(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 10
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})


async def s0730(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 11
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})
    r.verifica()
    if r.prova((k0418, )):
        await r.sotto(s0731)


async def s0731(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 11 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0732(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 12
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0733, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0734)
    else:
        await r.sotto(s0735)


async def s0733(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 12 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0734(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 12 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0735(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 12 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0736(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 13
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0737, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0738)
    else:
        await r.sotto(s0739)


async def s0737(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 13 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0738(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 13 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0739(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 13 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0740(r):
    # automazione Automazione VMC Master > 2 choose 136
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc')]})
    r.variabili({'vel_fine_inquinanti': Modello(M.m0001), 'vel_ripristino_inquinanti': Modello(M.m0625)}, alias="Velocità letta a fine allerta Inquinanti e velocità che il ripristino qui sotto rimanderebbe (stesso ordine delle opzioni; Free Cooling per la Free Cool./Heat. memorizzata con le spie «per programmazione» spente; vuota per la Free Cool./Heat. sospesa da un'allerta, che ha la sua ripresa, e quando nessuna opzione vale)")
    r.verifica()
    if r.prova((k0426, )):
        await r.sotto(s0741)
    r.verifica()
    if r.prova((k0429, )):
        await r.sotto(s0744)
    elif r.prova((k0430, )):
        await r.sotto(s0753)
    elif r.prova((k0431, )):
        await r.sotto(s0760)
    elif r.prova((k0432, )):
        await r.sotto(s0767)
    elif r.prova((k0433, )):
        await r.sotto(s0774)
    elif r.prova((k0434, )):
        await r.sotto(s0781)
    elif r.prova((k0435, )):
        await r.sotto(s0788)
    elif r.prova((k0440, )):
        await r.sotto(s0795)


async def s0741(r):
    # automazione Automazione VMC Master > 2 choose 136 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0424, )):
        await r.sotto(s0742)
    r.verifica()
    if r.prova((k0425, )):
        await r.sotto(s0743)
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'attesa della fine dell'allerta Inquinanti mantenuta")


async def s0742(r):
    # automazione Automazione VMC Master > 2 choose 136 > 2 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0743(r):
    # automazione Automazione VMC Master > 2 choose 136 > 2 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0744(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0745)
    elif r.prova((k0237, )):
        await r.sotto(s0750)


async def s0745(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0746, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0747)
    else:
        await r.sotto(s0748)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s0749)


async def s0746(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {}, alias='Fine Inquinanti -> prima il comando Velocità 0, poi spegne le memorie di velocità scelta e le memorie Inquinanti (correzione O5)')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0747(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0748(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0749(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0750(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    if r.prova((k0427, )):
        await r.sotto(s0751)
    r.verifica()
    if r.prova((k0428, )):
        await r.sotto(s0752)


async def s0751(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 1 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')]})


async def s0752(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 0 > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')]})


async def s0753(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0754)
    elif r.prova((k0237, )):
        await r.sotto(s0759)


async def s0754(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0755, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0756)
    else:
        await r.sotto(s0757)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s0758)


async def s0755(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0756(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0757(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0758(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0759(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0760(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0761)
    elif r.prova((k0237, )):
        await r.sotto(s0766)


async def s0761(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0762, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s0763)
    else:
        await r.sotto(s0764)
    r.verifica()
    if r.prova((k0194, )):
        await r.sotto(s0765)


async def s0762(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0763(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0764(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0765(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0766(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 2 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})


async def s0767(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0768)
    elif r.prova((k0237, )):
        await r.sotto(s0773)


async def s0768(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0769, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s0770)
    else:
        await r.sotto(s0771)
    r.verifica()
    if r.prova((k0197, )):
        await r.sotto(s0772)


async def s0769(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0770(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0771(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0772(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0773(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 3 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})


async def s0774(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0775)
    elif r.prova((k0237, )):
        await r.sotto(s0780)


async def s0775(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0776, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s0777)
    else:
        await r.sotto(s0778)
    r.verifica()
    if r.prova((k0200, )):
        await r.sotto(s0779)


async def s0776(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0777(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0778(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0779(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0780(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 4 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})


async def s0781(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0782)
    elif r.prova((k0237, )):
        await r.sotto(s0787)


async def s0782(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0783, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s0784)
    else:
        await r.sotto(s0785)
    r.verifica()
    if r.prova((k0203, )):
        await r.sotto(s0786)


async def s0783(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0784(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0785(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0786(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0787(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 5 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})


async def s0788(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0789)
    elif r.prova((k0237, )):
        await r.sotto(s0794)


async def s0789(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0790, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s0791)
    else:
        await r.sotto(s0792)
    r.verifica()
    if r.prova((k0214, )):
        await r.sotto(s0793)


async def s0790(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0791(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0792(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0793(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0794(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 6 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})


async def s0795(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0796)
    elif r.prova((k0237, )):
        await r.sotto(s0806)


async def s0796(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0436, )):
        await r.sotto(s0797)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0798, (k0438, ))
    r.verifica()
    if r.prova((k0439, )):
        await r.sotto(s0803)
    else:
        await r.sotto(s0804)
    r.variabili({'velocita_fine_allerta': Modello(M.m0641)}, alias='Velocità di fine allerta (per il ripristino dopo un Black-Out)')
    r.verifica()
    if r.prova((k0211, )):
        await r.sotto(s0805)


async def s0797(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0798(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    if r.prova((k0208, )):
        await r.sotto(s0799)
    else:
        await r.sotto(s0802)
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0799(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 2 repeat > 1 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0437, )):
        await r.sotto(s0800)
    else:
        await r.sotto(s0801)


async def s0800(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 2 repeat > 1 then > 0 then
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0801(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 2 repeat > 1 then > 0 else
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})


async def s0802(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 2 repeat > 1 else
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})


async def s0803(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0639)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0804(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0805(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': Modello(M.m0480)})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0481)})


async def s0806(r):
    # automazione Automazione VMC Master > 2 choose 136 > 3 choose 7 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0807(r):
    # automazione Automazione VMC Master > 2 choose 137
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0444, )):
        await r.sotto(s0808)
    elif r.prova((k0447, )):
        await r.sotto(s0812)
    elif r.prova((k0449, )):
        await r.sotto(s0816)
    elif r.prova((k0450, )):
        await r.sotto(s0825)
    elif r.prova((k0451, )):
        await r.sotto(s0829)
    elif r.prova((k0452, )):
        await r.sotto(s0833)
    elif r.prova((k0453, )):
        await r.sotto(s0837)
    elif r.prova((k0454, )):
        await r.sotto(s0841)
    elif r.prova((k0455, )):
        await r.sotto(s0845)
    elif r.prova((k0456, )):
        await r.sotto(s0849)
    elif r.prova((k0457, )):
        await r.sotto(s0853)
    elif r.prova((k0458, )):
        await r.sotto(s0857)
    elif r.prova((k0459, )):
        await r.sotto(s0861)
    elif r.prova((k0460, )):
        await r.sotto(s0865)
    elif r.prova((k0461, )):
        await r.sotto(s0869)
    elif r.prova((k0462, )):
        await r.sotto(s0873)
    elif r.prova((k0463, )):
        await r.sotto(s0877)
    elif r.prova((k0464, )):
        await r.sotto(s0881)
    else:
        await r.sotto(s0885)


async def s0808(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0809, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0810)
    else:
        await r.sotto(s0811)


async def s0809(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0810(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0811(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0812(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0813, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0814)
    else:
        await r.sotto(s0815)


async def s0813(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0814(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0815(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 1 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0816(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0448, )):
        await r.sotto(s0817)
    else:
        await r.sotto(s0821)


async def s0817(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0818, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0819)
    else:
        await r.sotto(s0820)


async def s0818(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0819(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0820(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0821(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 else
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0822, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0823)
    else:
        await r.sotto(s0824)


async def s0822(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 else > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0823(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 else > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0824(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 2 > 0 else > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0825(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 3
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0826, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0827)
    else:
        await r.sotto(s0828)


async def s0826(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]}, alias="Inquinanti con la VMC in attesa del Free e memorie Inquinanti spente -> memoria Inquinanti 1, l'attesa Free resta come nel ramo c2 (correzione O4)")
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0827(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 3 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0828(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 3 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0829(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 4
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0830, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0831)
    else:
        await r.sotto(s0832)


async def s0830(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 4 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0831(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 4 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0832(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 4 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0833(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 5
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0834, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0835)
    else:
        await r.sotto(s0836)


async def s0834(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 5 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0835(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 5 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0836(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 5 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0837(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 6
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0838, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0839)
    else:
        await r.sotto(s0840)


async def s0838(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 6 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0839(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 6 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0840(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 6 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0841(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 7
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0842, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s0843)
    else:
        await r.sotto(s0844)


async def s0842(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 7 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0843(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 7 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0844(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 7 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0845(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 8
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0846, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0847)
    else:
        await r.sotto(s0848)


async def s0846(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 8 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0847(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 8 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0848(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 8 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0849(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 9
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0850, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s0851)
    else:
        await r.sotto(s0852)


async def s0850(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 9 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0851(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 9 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0852(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 9 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0853(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 10
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0854, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0855)
    else:
        await r.sotto(s0856)


async def s0854(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 10 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0855(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 10 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0856(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 10 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0857(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 11
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0858, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s0859)
    else:
        await r.sotto(s0860)


async def s0858(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 11 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0859(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 11 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0860(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 11 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0861(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 12
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0862, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0863)
    else:
        await r.sotto(s0864)


async def s0862(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 12 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0863(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 12 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0864(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 12 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0865(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 13
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0866, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s0867)
    else:
        await r.sotto(s0868)


async def s0866(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 13 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0867(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 13 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0868(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 13 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0869(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 14
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0870, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0871)
    else:
        await r.sotto(s0872)


async def s0870(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 14 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0871(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 14 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0872(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 14 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0873(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 15
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0874, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s0875)
    else:
        await r.sotto(s0876)


async def s0874(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 15 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0875(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 15 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0876(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 15 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0877(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 16
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0878, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0879)
    else:
        await r.sotto(s0880)


async def s0878(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 16 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0879(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 16 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0880(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 16 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0881(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 17
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0882, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0883)
    else:
        await r.sotto(s0884)


async def s0882(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 17 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0883(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 17 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0884(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 choose 17 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0885(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 default
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias='Nessun ramo riconosciuto: la VMC è ferma con Inquinanti in corso -> Velocità 1 (R2, 03-11-2026)')
    r.verifica()
    await r.ripeti_finche(s0886, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0887)
    else:
        await r.sotto(s0888)


async def s0886(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 default > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0887(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 default > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0888(r):
    # automazione Automazione VMC Master > 2 choose 137 > 0 default > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0889(r):
    # automazione Automazione VMC Master > 2 choose 138
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0467, )):
        await r.sotto(s0890)
    elif r.prova((k0469, )):
        await r.sotto(s0892)
    elif r.prova((k0471, )):
        await r.sotto(s0894)
    elif r.prova((k0472, )):
        await r.sotto(s0896)


async def s0890(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})
    r.verifica()
    await r.ripeti_finche(s0891, (k0466, ))
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0891(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0892(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]}, alias="Velocità 1 scelta dall'utente con PdR e VMC in Free Cool./Heat. -> resta la Velocità 1 (prima la VMC tornava in Free Cool./Heat.)")
    r.verifica()
    await r.ripeti_finche(s0893, (k0468, ))
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0893(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})


async def s0894(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0895, (k0470, ))
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0895(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0896(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0897, (k0466, ))
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0897(r):
    # automazione Automazione VMC Master > 2 choose 138 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0898(r):
    # automazione Automazione VMC Master > 2 choose 139
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0899, (k0474, ))


async def s0899(r):
    # automazione Automazione VMC Master > 2 choose 139 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0900(r):
    # automazione Automazione VMC Master > 2 choose 140
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0901, (k0476, ))


async def s0901(r):
    # automazione Automazione VMC Master > 2 choose 140 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0902(r):
    # automazione Automazione VMC Master > 2 choose 141
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0903, (k0478, ))


async def s0903(r):
    # automazione Automazione VMC Master > 2 choose 141 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0904(r):
    # automazione Automazione VMC Master > 2 choose 142
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0905, (k0480, ))


async def s0905(r):
    # automazione Automazione VMC Master > 2 choose 142 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0906(r):
    # automazione Automazione VMC Master > 2 choose 143
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0907, (k0482, ))


async def s0907(r):
    # automazione Automazione VMC Master > 2 choose 143 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0908(r):
    # automazione Automazione VMC Master > 2 choose 144
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0153, )):
        await r.sotto(s0909)
    elif r.prova((k0485, )):
        await r.sotto(s0914)
    elif r.prova((k0154, )):
        await r.sotto(s0919)


async def s0909(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0910, (k0484, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0911, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0912)
    else:
        await r.sotto(s0913)


async def s0910(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})


async def s0911(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0912(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0913(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 0 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0914(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0915, (k0470, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0916, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0917)
    else:
        await r.sotto(s0918)


async def s0915(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0916(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0917(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 1 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0918(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 1 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0919(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s0920, (k0470, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0921, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0922)
    else:
        await r.sotto(s0923)


async def s0920(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0921(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0922(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 2 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0923(r):
    # automazione Automazione VMC Master > 2 choose 144 > 0 choose 2 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0924(r):
    # automazione Automazione VMC Master > 2 choose 145
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0487, )):
        await r.sotto(s0925)
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')]}, alias='Attivazione Spia Congelamento ≤ -18 [°C] Temp. Esterna')
    r.verifica()
    if r.prova((k0491, )):
        await r.sotto(s0926)
    elif r.prova((k0506, )):
        await r.sotto(s0932)
    elif r.prova((k0509, )):
        await r.sotto(s0948)
    elif r.prova((k0512, )):
        await r.sotto(s0956)
    elif r.prova((k0515, )):
        await r.sotto(s0964)
    elif r.prova((k0518, )):
        await r.sotto(s0972)
    elif r.prova((k0521, )):
        await r.sotto(s0980)
    elif r.prova((k0524, )):
        await r.sotto(s0988)


async def s0925(r):
    # automazione Automazione VMC Master > 2 choose 145 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s0926(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0488, )):
        await r.sotto(s0927)
    else:
        await r.sotto(s0928)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0929, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0930)
    else:
        await r.sotto(s0931)


async def s0927(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 0 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')]})


async def s0928(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 0 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')]})


async def s0929(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 0 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0930(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0931(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 0 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0932(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    r.verifica()
    if r.prova((k0502, )):
        await r.sotto(s0933)
    elif r.prova((k0503, )):
        await r.sotto(s0940)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0945, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0946)
    else:
        await r.sotto(s0947)


async def s0933(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0496, )):
        await r.sotto(s0934)
    elif r.prova((k0498, )):
        await r.sotto(s0937)
    elif r.prova((k0500, )):
        await r.sotto(s0938)
    elif r.prova((k0501, )):
        await r.sotto(s0939)


async def s0934(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0492, )):
        await r.sotto(s0935)
    elif r.prova((k0493, )):
        await r.sotto(s0936)


async def s0935(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0 > 0 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0936(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0 > 0 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0937(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0938(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0939(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0940(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0496, )):
        await r.sotto(s0941)
    elif r.prova((k0498, )):
        await r.sotto(s0942)
    elif r.prova((k0500, )):
        await r.sotto(s0943)
    elif r.prova((k0501, )):
        await r.sotto(s0944)


async def s0941(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0942(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0943(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 1 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0944(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 2 choose 1 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]}, alias="Velocità 1 scelta dall'utente durante il PdR -> annulla la Ripresa Free (correzione R6)")


async def s0945(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0946(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0947(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 1 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0948(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0498, )):
        await r.sotto(s0949)
    elif r.prova((k0496, )):
        await r.sotto(s0950)
    elif r.prova((k0501, )):
        await r.sotto(s0951)
    elif r.prova((k0500, )):
        await r.sotto(s0952)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0953, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0954)
    else:
        await r.sotto(s0955)


async def s0949(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})


async def s0950(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 3 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})


async def s0951(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 3 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})


async def s0952(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 3 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0953(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 5 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0954(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0955(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 2 > 6 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0956(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0498, )):
        await r.sotto(s0957)
    elif r.prova((k0496, )):
        await r.sotto(s0958)
    elif r.prova((k0501, )):
        await r.sotto(s0959)
    elif r.prova((k0500, )):
        await r.sotto(s0960)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0961, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0962)
    else:
        await r.sotto(s0963)


async def s0957(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})


async def s0958(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 3 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})


async def s0959(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 3 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})


async def s0960(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 3 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0961(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 5 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0962(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0963(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 3 > 6 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0964(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0498, )):
        await r.sotto(s0965)
    elif r.prova((k0496, )):
        await r.sotto(s0966)
    elif r.prova((k0501, )):
        await r.sotto(s0967)
    elif r.prova((k0500, )):
        await r.sotto(s0968)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0969, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0970)
    else:
        await r.sotto(s0971)


async def s0965(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})


async def s0966(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 3 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})


async def s0967(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 3 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})


async def s0968(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 3 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0969(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 5 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0970(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0971(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 4 > 6 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0972(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0498, )):
        await r.sotto(s0973)
    elif r.prova((k0496, )):
        await r.sotto(s0974)
    elif r.prova((k0501, )):
        await r.sotto(s0975)
    elif r.prova((k0500, )):
        await r.sotto(s0976)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0977, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0978)
    else:
        await r.sotto(s0979)


async def s0973(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})


async def s0974(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 3 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})


async def s0975(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 3 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})


async def s0976(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 3 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0977(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 5 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0978(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0979(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 5 > 6 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0980(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0498, )):
        await r.sotto(s0981)
    elif r.prova((k0496, )):
        await r.sotto(s0982)
    elif r.prova((k0501, )):
        await r.sotto(s0983)
    elif r.prova((k0500, )):
        await r.sotto(s0984)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0985, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0986)
    else:
        await r.sotto(s0987)


async def s0981(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})


async def s0982(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 3 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})


async def s0983(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 3 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})


async def s0984(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 3 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0985(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 5 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0986(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0987(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 6 > 6 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0988(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento')]})
    r.verifica()
    if r.prova((k0502, )):
        await r.sotto(s0989)
    elif r.prova((k0503, )):
        await r.sotto(s0994)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0999, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s1000)
    else:
        await r.sotto(s1001)


async def s0989(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0498, )):
        await r.sotto(s0990)
    elif r.prova((k0496, )):
        await r.sotto(s0991)
    elif r.prova((k0501, )):
        await r.sotto(s0992)
    elif r.prova((k0500, )):
        await r.sotto(s0993)


async def s0990(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
