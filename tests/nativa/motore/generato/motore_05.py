"""Automazioni e script del package, tradotti in Python (parte 5 di 8).

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
    k0136, k0137, k0151, k0152, k0158, k0159, k0161, k0162, k0164, k0165,
    k0167, k0168, k0172, k0173, k0178, k0179, k0183, k0190, k0194, k0197,
    k0200, k0203, k0208, k0214, k0227, k0293, k0296, k0298, k0300, k0302,
    k0304, k0306, k0308, k0496, k0498, k0500, k0501, k0527, k0528, k0529,
    k0530, k0531, k0532, k0533, k0534, k0535, k0536, k0537, k0538, k0539,
    k0540, k0541, k0542, k0543, k0544, k0546, k0547, k0551, k0552, k0554,
    k0555, k0598, k0599, k0600, k0601, k0602, k0603, k0604, k0605, k0606,
    k0607, k0608, k0609, k0610, k0611, k0612, k0613, k0614, k0615, k0617,
    k0619, k0620, k0621, k0622, k0623, k0624, k0625, k0626, k0627, k0628,
    k0629, k0630, k0631, k0632, k0633, k0634, k0635, k0636, k0637, k0638,
    k0639, k0640, k0641, k0642, k0643, k0645, k0646, k0647, k0649, k0650,
    k0651, k0658, k0660, k0661, k0664, k0665, k0668, k0671, k0674, k0677,
    k0680, k0683, k0686, k0689, k0690, k0691, k0692, k0693, k0694, k0695,
    k0696, k0697, k0698, k0699,
)
from .motore_06 import (
    s1303, s1304, s1310, s1316,
)


async def s0991(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0992(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0993(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 0 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0994(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0496, )):
        await r.sotto(s0995)
    elif r.prova((k0498, )):
        await r.sotto(s0996)
    elif r.prova((k0500, )):
        await r.sotto(s0997)
    elif r.prova((k0501, )):
        await r.sotto(s0998)


async def s0995(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0996(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0997(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 1 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')


async def s0998(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 2 choose 1 > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Spie Inquinanti OFF')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias='Spie PdR OFF')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})


async def s0999(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1000(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1001(r):
    # automazione Automazione VMC Master > 2 choose 145 > 2 choose 7 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1002(r):
    # automazione Automazione VMC Master > 2 choose 146
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0527, )):
        await r.sotto(s1003)
    else:
        await r.sotto(s1004)
    r.verifica()
    if r.prova((k0530, )):
        await r.sotto(s1006)
    elif r.prova((k0532, )):
        await r.sotto(s1012)
    elif r.prova((k0534, )):
        await r.sotto(s1019)
    elif r.prova((k0536, )):
        await r.sotto(s1026)
    elif r.prova((k0538, )):
        await r.sotto(s1033)
    elif r.prova((k0540, )):
        await r.sotto(s1040)
    elif r.prova((k0542, )):
        await r.sotto(s1047)
    elif r.prova((k0544, )):
        await r.sotto(s1054)


async def s1003(r):
    # automazione Automazione VMC Master > 2 choose 146 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]}, alias='Spia Comando non eseguito del Calendario OFF: il comando lo rifà il Calendario (la fascia finita o iniziata comanda da sé la VMC)')
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    r.verifica()
    raise Ferma('Ripresa lasciata al Calendario')


async def s1004(r):
    # automazione Automazione VMC Master > 2 choose 146 > 0 else
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0528, )):
        await r.sotto(s1005)


async def s1005(r):
    # automazione Automazione VMC Master > 2 choose 146 > 0 else > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})
    r.verifica()
    raise Ferma('Ripresa lasciata al Calendario (comando del Calendario in sospeso)')


async def s1006(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1007, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1008, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s1009)
    else:
        await r.sotto(s1010)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s1011)


async def s1007(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1008(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 0 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1009(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1010(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 0 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1011(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1012(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0531, )):
        await r.sotto(s1013)
    r.verifica()
    await r.ripeti_finche(s1014, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1015, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1016)
    else:
        await r.sotto(s1017)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s1018)


async def s1013(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1014(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1015(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1016(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1017(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1018(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 1 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1019(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0533, )):
        await r.sotto(s1020)
    r.verifica()
    await r.ripeti_finche(s1021, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1022, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s1023)
    else:
        await r.sotto(s1024)
    r.verifica()
    if r.prova((k0194, )):
        await r.sotto(s1025)


async def s1020(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1021(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1022(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1023(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1024(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1025(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 2 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1026(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0535, )):
        await r.sotto(s1027)
    r.verifica()
    await r.ripeti_finche(s1028, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1029, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s1030)
    else:
        await r.sotto(s1031)
    r.verifica()
    if r.prova((k0197, )):
        await r.sotto(s1032)


async def s1027(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1028(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1029(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1030(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1031(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1032(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 3 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1033(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0537, )):
        await r.sotto(s1034)
    r.verifica()
    await r.ripeti_finche(s1035, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1036, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s1037)
    else:
        await r.sotto(s1038)
    r.verifica()
    if r.prova((k0200, )):
        await r.sotto(s1039)


async def s1034(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1035(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1036(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1037(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1038(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1039(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 4 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1040(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0539, )):
        await r.sotto(s1041)
    r.verifica()
    await r.ripeti_finche(s1042, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1043, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s1044)
    else:
        await r.sotto(s1045)
    r.verifica()
    if r.prova((k0214, )):
        await r.sotto(s1046)


async def s1041(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1042(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1043(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1044(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1045(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1046(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 5 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1047(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0541, )):
        await r.sotto(s1048)
    r.verifica()
    await r.ripeti_finche(s1049, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1050, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s1051)
    else:
        await r.sotto(s1052)
    r.verifica()
    if r.prova((k0203, )):
        await r.sotto(s1053)


async def s1048(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1049(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1050(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1051(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1052(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1053(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 6 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1054(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0543, )):
        await r.sotto(s1055)
    r.verifica()
    await r.ripeti_finche(s1056, (k0529, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1057, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s1058)
    else:
        await r.sotto(s1059)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s1060)


async def s1055(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1056(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento')]})


async def s1057(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1058(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1059(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1060(r):
    # automazione Automazione VMC Master > 2 choose 146 > 1 choose 7 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})


async def s1061(r):
    # automazione Automazione VMC Master > 2 choose 147
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0546, )):
        await r.sotto(s1062)
    elif r.prova((k0547, )):
        await r.sotto(s1063)


async def s1062(r):
    # automazione Automazione VMC Master > 2 choose 147 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s1063(r):
    # automazione Automazione VMC Master > 2 choose 147 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s1064(r):
    # automazione Automazione VMC Master > 2 choose 148
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1065, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s1066)
    else:
        await r.sotto(s1067)


async def s1065(r):
    # automazione Automazione VMC Master > 2 choose 148 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1066(r):
    # automazione Automazione VMC Master > 2 choose 148 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1067(r):
    # automazione Automazione VMC Master > 2 choose 148 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1068(r):
    # automazione Automazione VMC Master > 2 choose 149
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1069, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s1070)
    else:
        await r.sotto(s1071)


async def s1069(r):
    # automazione Automazione VMC Master > 2 choose 149 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1070(r):
    # automazione Automazione VMC Master > 2 choose 149 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1071(r):
    # automazione Automazione VMC Master > 2 choose 149 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1072(r):
    # automazione Automazione VMC Master > 2 choose 150
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0551, )):
        await r.sotto(s1073)
    elif r.prova((k0552, )):
        await r.sotto(s1077)


async def s1073(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1074, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1075)
    else:
        await r.sotto(s1076)


async def s1074(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]}, alias="PdR con memoria Free, Free sfavorevole e attesa Free spenta -> riaccende l'attesa Free (come le opzioni 139/140) e memoria Inquinanti 1 senza «partiti da 0», come il ramo gemello c1 (correzione O6)")
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1075(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1076(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1077(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1078, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1079)
    else:
        await r.sotto(s1080)


async def s1078(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1079(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1080(r):
    # automazione Automazione VMC Master > 2 choose 150 > 0 choose 1 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1081(r):
    # automazione Automazione VMC Master > 2 choose 151
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0554, )):
        await r.sotto(s1082)
    elif r.prova((k0555, )):
        await r.sotto(s1086)


async def s1082(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1083, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1084)
    else:
        await r.sotto(s1085)


async def s1083(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1084(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1085(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1086(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1087, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1088)
    else:
        await r.sotto(s1089)


async def s1087(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]}, alias="PdR con memoria Free, Free sfavorevole e attesa Free spenta -> riaccende l'attesa Free (come le opzioni 139/140) e memoria Inquinanti 1 senza «partiti da 0», come il ramo gemello c0 (correzione O6)")
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1088(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1089(r):
    # automazione Automazione VMC Master > 2 choose 151 > 0 choose 1 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1090(r):
    # automazione Automazione VMC Master > 2 choose 152
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_esterna'), c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_umidita_esterna'), c.N('script.vmc_master_aggiorna_elenco_entita_umidita_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_co2_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo'), c.N('script.vmc_master_aggiorna_elenco_entita_media_player')]})


async def s1091(r):
    # automazione Automazione VMC Master > 2 choose 153
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_esterna')]})


async def s1092(r):
    # automazione Automazione VMC Master > 2 choose 154
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_interna')]})


async def s1093(r):
    # automazione Automazione VMC Master > 2 choose 155
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_umidita_esterna')]})


async def s1094(r):
    # automazione Automazione VMC Master > 2 choose 156
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_umidita_interna')]})


async def s1095(r):
    # automazione Automazione VMC Master > 2 choose 157
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_co2_interna')]})


async def s1096(r):
    # automazione Automazione VMC Master > 2 choose 158
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo')]})


async def s1097(r):
    # automazione Automazione VMC Master > 2 choose 159
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_media_player')]})


async def s1098(r):
    # automazione Automazione VMC Master > 2 choose 160
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_scelta_sensori')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0717)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s1099(r):
    # automazione Automazione VMC Master > 2 choose 161
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_scelta_sensori')]})


async def s1100(r):
    # automazione Automazione VMC Master > 2 choose 162
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_elementi_chimici')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0718)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s1101(r):
    # automazione Automazione VMC Master > 2 choose 163
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_elementi_chimici')]})


async def s1102(r):
    # automazione Automazione VMC Master > 2 choose 164
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzione_finestra_audio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0719)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s1103(r):
    # automazione Automazione VMC Master > 2 choose 165
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzione_finestra_audio')]})


async def s1104(r):
    # automazione Automazione VMC Master > 2 choose 166
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0720)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s1105(r):
    # automazione Automazione VMC Master > 2 choose 167
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_entita_non_disponibile_temperatura_esterna'), 'title': Modello(M.m0721), 'message': Modello(M.m0722)})


async def s1106(r):
    # automazione Automazione VMC Master > 2 choose 168
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_entita_non_disponibile_temperatura_interna'), 'title': Modello(M.m0721), 'message': Modello(M.m0723)})


async def s1107(r):
    # automazione Automazione VMC Master > 2 choose 169
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_entita_non_disponibile_umidita_esterna'), 'title': Modello(M.m0721), 'message': Modello(M.m0724)})


async def s1108(r):
    # automazione Automazione VMC Master > 2 choose 170
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_entita_non_disponibile_umidita_interna'), 'title': Modello(M.m0721), 'message': Modello(M.m0725)})


async def s1109(r):
    # automazione Automazione VMC Master > 2 choose 171
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_entita_non_disponibile_co2_interna'), 'title': Modello(M.m0721), 'message': Modello(M.m0726)})


async def s1110(r):
    # automazione Automazione VMC Master > 2 choose 172
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_entita_non_disponibile_dispositivo_notifica'), 'title': Modello(M.m0721), 'message': Modello(M.m0727)})


async def s1111(r):
    # automazione Automazione VMC Master > 2 choose 173
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_verifica_filtro'), 'title': Modello(M.m0721), 'message': Modello(M.m0728)})


async def s1112(r):
    # automazione Automazione VMC Master > 2 choose 174
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_cambio_filtro')]})


async def s1113(r):
    # automazione Automazione VMC Master > 2 choose 175
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_velocita_0')]})


async def s1114(r):
    # automazione Automazione VMC Master > 2 choose 176
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_velocita_diversa_da_0')]})


async def s1115(r):
    # automazione Automazione VMC Master > 2 choose 177
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_errore_temp_esterna')]})


async def s1116(r):
    # automazione Automazione VMC Master > 2 choose 178
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_errore_temp_interna')]})


async def s1117(r):
    # automazione Automazione VMC Master > 2 choose 179
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_errore_umidita_esterna')]})


async def s1118(r):
    # automazione Automazione VMC Master > 2 choose 180
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_errore_umidita_interna')]})


async def s1119(r):
    # automazione Automazione VMC Master > 2 choose 181
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_notifica_errore_co2_interna')]})


async def s1120(r):
    # automazione Automazione VMC Master > 2 choose 182
    c, V = r.c, r.V
    await r.servizio('script.turn_on', {}, {'entity_id': [c.N('script.vmc_master_upgrade_sensors')]}, alias='Avvia Agg. Sensori senza attenderne la fine (79 s), così le allerte e il Black-Out non restano in coda')


async def s1121(r):
    # automazione Automazione VMC Master > 2 choose 183
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')]})
    r.verifica()
    if r.prova((k0608, )):
        await r.sotto(s1122)
    else:
        await r.sotto(s1143)


async def s1122(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0598, )):
        await r.sotto(s1123)
    elif r.prova((k0599, )):
        await r.sotto(s1125)
    elif r.prova((k0600, )):
        await r.sotto(s1127)
    elif r.prova((k0601, )):
        await r.sotto(s1129)
    elif r.prova((k0602, )):
        await r.sotto(s1131)
    elif r.prova((k0603, )):
        await r.sotto(s1133)
    elif r.prova((k0604, )):
        await r.sotto(s1135)
    elif r.prova((k0605, )):
        await r.sotto(s1137)
    elif r.prova((k0606, )):
        await r.sotto(s1139)
    elif r.prova((k0607, )):
        await r.sotto(s1141)


async def s1123(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1124, (k0296, ))


async def s1124(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'))
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1125(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1126, (k0293, ))


async def s1126(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1127(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1128, (k0296, ))


async def s1128(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1129(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1130, (k0298, ))


async def s1130(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1131(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1132, (k0300, ))


async def s1132(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 4 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1133(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1134, (k0302, ))


async def s1134(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 5 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1135(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1136, (k0304, ))


async def s1136(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 6 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1137(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1138, (k0306, ))


async def s1138(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 7 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1139(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 8
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1140, (k0296, ))


async def s1140(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 8 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1141(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 9
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1142, (k0308, ))


async def s1142(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 then > 0 choose 9 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (lo 0 non ancora aggiornato non va preso per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1143(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0609, )):
        await r.sotto(s1144)
    elif r.prova((k0610, )):
        await r.sotto(s1146)
    elif r.prova((k0611, )):
        await r.sotto(s1148)
    elif r.prova((k0612, )):
        await r.sotto(s1150)
    elif r.prova((k0613, )):
        await r.sotto(s1152)
    elif r.prova((k0614, )):
        await r.sotto(s1154)
    elif r.prova((k0615, )):
        await r.sotto(s1156)


async def s1144(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1145, (k0296, ))


async def s1145(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1146(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1147, (k0298, ))


async def s1147(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1148(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1149, (k0300, ))


async def s1149(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1150(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1151, (k0302, ))


async def s1151(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1152(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1153, (k0304, ))


async def s1153(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 4 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1154(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1155, (k0306, ))


async def s1155(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 5 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1156(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1157, (k0308, ))


async def s1157(r):
    # automazione Automazione VMC Master > 2 choose 183 > 1 else > 0 choose 6 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1158(r):
    # automazione Automazione VMC Master > 2 choose 184
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]}, alias="Fine Umidità -> spegne la Spia Umidità e le memorie di velocità dell'Umidità")
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1159, (k0296, ))
    r.verifica()
    if r.prova((k0617, )):
        await r.sotto(s1160)


async def s1159(r):
    # automazione Automazione VMC Master > 2 choose 184 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]}, alias='Inquinanti come partiti da Velocità 0 -> memoria Partenza e Ritorno a Velocità 0')
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]}, alias="Spegne le memorie Inquinanti della velocità alzata dall'Umidità")
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1160(r):
    # automazione Automazione VMC Master > 2 choose 184 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1161(r):
    # automazione Automazione VMC Master > 2 choose 185
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia')]})
    r.verifica()
    if r.prova((k0622, )):
        await r.sotto(s1162)
    elif r.prova((k0624, )):
        await r.sotto(s1167)
    elif r.prova((k0627, )):
        await r.sotto(s1171)
    elif r.prova((k0630, )):
        await r.sotto(s1175)
    elif r.prova((k0633, )):
        await r.sotto(s1179)
    elif r.prova((k0636, )):
        await r.sotto(s1183)
    elif r.prova((k0640, )):
        await r.sotto(s1187)
    elif r.prova((k0643, )):
        await r.sotto(s1193)


async def s1162(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0619, )):
        await r.sotto(s1163)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0620, )):
        await r.sotto(s1164)
    r.verifica()
    await r.ripeti_finche(s1165, (k0293, ))
    r.verifica()
    if r.prova((k0621, )):
        await r.sotto(s1166)


async def s1163(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 0 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s1164(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 0 > 3 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1165(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 0 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1166(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1167(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0623, )):
        await r.sotto(s1168)
    r.verifica()
    await r.ripeti_finche(s1169, (k0296, ))
    r.verifica()
    if r.prova((k0617, )):
        await r.sotto(s1170)


async def s1168(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 1 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1169(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1170(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 1 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1171(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0625, )):
        await r.sotto(s1172)
    r.verifica()
    await r.ripeti_finche(s1173, (k0298, ))
    r.verifica()
    if r.prova((k0626, )):
        await r.sotto(s1174)


async def s1172(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 2 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1173(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1174(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 2 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1175(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0628, )):
        await r.sotto(s1176)
    r.verifica()
    await r.ripeti_finche(s1177, (k0300, ))
    r.verifica()
    if r.prova((k0629, )):
        await r.sotto(s1178)


async def s1176(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 3 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1177(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1178(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 3 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1179(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0631, )):
        await r.sotto(s1180)
    r.verifica()
    await r.ripeti_finche(s1181, (k0302, ))
    r.verifica()
    if r.prova((k0632, )):
        await r.sotto(s1182)


async def s1180(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 4 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1181(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 4 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1182(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 4 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1183(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0634, )):
        await r.sotto(s1184)
    r.verifica()
    await r.ripeti_finche(s1185, (k0304, ))
    r.verifica()
    if r.prova((k0635, )):
        await r.sotto(s1186)


async def s1184(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 5 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1185(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 5 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1186(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 5 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1187(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0637, )):
        await r.sotto(s1188)
    r.verifica()
    await r.ripeti_finche(s1189, (k0638, ))
    r.variabili({'velocita_fine_allerta': Modello(M.m0479)}, alias='Velocità di fine allerta (per il ripristino dopo un Black-Out)')
    r.verifica()
    if r.prova((k0639, )):
        await r.sotto(s1192)


async def s1188(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 6 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1189(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 6 > 3 repeat
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0208, )):
        await r.sotto(s1190)
    else:
        await r.sotto(s1191)
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1190(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 6 > 3 repeat > 0 then
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})


async def s1191(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 6 > 3 repeat > 0 else
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})


async def s1192(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 6 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': Modello(M.m0480)})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0481)})


async def s1193(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0641, )):
        await r.sotto(s1194)
    r.verifica()
    await r.ripeti_finche(s1195, (k0308, ))
    r.verifica()
    if r.prova((k0642, )):
        await r.sotto(s1196)


async def s1194(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 7 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Umidità mantenuta")


async def s1195(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 7 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1196(r):
    # automazione Automazione VMC Master > 2 choose 185 > 1 choose 7 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1197(r):
    # automazione Automazione VMC Master > 2 choose 186
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0646, )):
        await r.sotto(s1198)
    else:
        await r.sotto(s1200)


async def s1198(r):
    # automazione Automazione VMC Master > 2 choose 186 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0')]}, alias="La Velocità 0 non è più mantenuta (la VMC riparte con la velocità dell'Umidità)")
    r.variabili({'vel_prima_del_comando': Modello(M.m0001), 'free_con_allerte': Modello(M.m0514), 'vel_avvio': Modello(M.m0515), 'comando_avvio': Modello(M.m0774)}, alias="Velocità di avvio come nell'opzione 175 (programmata; Velocità 1 se è programmata Free Cool./Heat. con allerte Free)")
    r.verifica()
    await r.ripeti_finche(s1199, (k0645, ))


async def s1199(r):
    # automazione Automazione VMC Master > 2 choose 186 > 0 then > 2 repeat
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0775), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1200(r):
    # automazione Automazione VMC Master > 2 choose 186 > 0 else
    c, V = r.c, r.V
    if not r.passo_condizione(k0647, "Solo con uno stato precedente valido, cioè Velocità 0 scelta dall'utente - con la lettura appena tornata disponibile (stato precedente OFF-Line o Non disponibile) nessuna memoria cambiata (B4-4); vale anche a Umidità finita con la Spia Umidità ancora accesa, per esempio la Velocità 0 scelta dall'utente durante gli Inquinanti o il Δ Temp. e ripristinata alla loro fine (la Velocità 0 resta)"):
        return
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1201, (k0293, ))


async def s1201(r):
    # automazione Automazione VMC Master > 2 choose 186 > 0 else > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1202(r):
    # automazione Automazione VMC Master > 2 choose 187
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0649, )):
        await r.sotto(s1203)
    elif r.prova((k0650, )):
        await r.sotto(s1205)
    elif r.prova((k0651, )):
        await r.sotto(s1207)


async def s1203(r):
    # automazione Automazione VMC Master > 2 choose 187 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1204, (k0296, ))


async def s1204(r):
    # automazione Automazione VMC Master > 2 choose 187 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1205(r):
    # automazione Automazione VMC Master > 2 choose 187 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1206, (k0296, ))


async def s1206(r):
    # automazione Automazione VMC Master > 2 choose 187 > 0 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1207(r):
    # automazione Automazione VMC Master > 2 choose 187 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1208(r):
    # automazione Automazione VMC Master > 2 choose 188
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0650, )):
        await r.sotto(s1209)
    else:
        await r.sotto(s1211)


async def s1209(r):
    # automazione Automazione VMC Master > 2 choose 188 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1210, (k0298, ))


async def s1210(r):
    # automazione Automazione VMC Master > 2 choose 188 > 0 then > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1211(r):
    # automazione Automazione VMC Master > 2 choose 188 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1212(r):
    # automazione Automazione VMC Master > 2 choose 189
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0650, )):
        await r.sotto(s1213)
    else:
        await r.sotto(s1215)


async def s1213(r):
    # automazione Automazione VMC Master > 2 choose 189 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1214, (k0300, ))


async def s1214(r):
    # automazione Automazione VMC Master > 2 choose 189 > 0 then > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1215(r):
    # automazione Automazione VMC Master > 2 choose 189 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1216(r):
    # automazione Automazione VMC Master > 2 choose 190
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0650, )):
        await r.sotto(s1217)
    else:
        await r.sotto(s1219)


async def s1217(r):
    # automazione Automazione VMC Master > 2 choose 190 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1218, (k0302, ))


async def s1218(r):
    # automazione Automazione VMC Master > 2 choose 190 > 0 then > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1219(r):
    # automazione Automazione VMC Master > 2 choose 190 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1220(r):
    # automazione Automazione VMC Master > 2 choose 191
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0650, )):
        await r.sotto(s1221)
    else:
        await r.sotto(s1223)


async def s1221(r):
    # automazione Automazione VMC Master > 2 choose 191 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1222, (k0304, ))


async def s1222(r):
    # automazione Automazione VMC Master > 2 choose 191 > 0 then > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1223(r):
    # automazione Automazione VMC Master > 2 choose 191 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1224(r):
    # automazione Automazione VMC Master > 2 choose 192
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0650, )):
        await r.sotto(s1225)
    else:
        await r.sotto(s1227)


async def s1225(r):
    # automazione Automazione VMC Master > 2 choose 192 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1226, (k0308, ))


async def s1226(r):
    # automazione Automazione VMC Master > 2 choose 192 > 0 then > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1227(r):
    # automazione Automazione VMC Master > 2 choose 192 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1228(r):
    # automazione Automazione VMC Master > 2 choose 193
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0658, )):
        await r.sotto(s1229)
    else:
        await r.sotto(s1230)


async def s1229(r):
    # automazione Automazione VMC Master > 2 choose 193 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})


async def s1230(r):
    # automazione Automazione VMC Master > 2 choose 193 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1231, (k0306, ))


async def s1231(r):
    # automazione Automazione VMC Master > 2 choose 193 > 0 else > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s1232(r):
    # automazione Automazione VMC Master > 2 choose 194
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0660, )):
        await r.sotto(s1233)
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')]}, alias='Attivazione Spia Δ Temp. > 23 [°C]')
    r.verifica()
    if r.prova((k0664, )):
        await r.sotto(s1234)
    elif r.prova((k0668, )):
        await r.sotto(s1239)
    elif r.prova((k0671, )):
        await r.sotto(s1244)
    elif r.prova((k0674, )):
        await r.sotto(s1248)
    elif r.prova((k0677, )):
        await r.sotto(s1252)
    elif r.prova((k0680, )):
        await r.sotto(s1256)
    elif r.prova((k0683, )):
        await r.sotto(s1260)
    elif r.prova((k0686, )):
        await r.sotto(s1264)


async def s1233(r):
    # automazione Automazione VMC Master > 2 choose 194 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1234(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0661, )):
        await r.sotto(s1235)
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1236, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1237)
    else:
        await r.sotto(s1238)


async def s1235(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 0 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s1236(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 0 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1237(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1238(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 0 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1239(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0665, )):
        await r.sotto(s1240)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1241, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1242)
    else:
        await r.sotto(s1243)


async def s1240(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 1 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})


async def s1241(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 1 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1242(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 1 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1243(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 1 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1244(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1245, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1246)
    else:
        await r.sotto(s1247)


async def s1245(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1246(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 2 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1247(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 2 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1248(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1249, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1250)
    else:
        await r.sotto(s1251)


async def s1249(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1250(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 3 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1251(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 3 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1252(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1253, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1254)
    else:
        await r.sotto(s1255)


async def s1253(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 4 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1254(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 4 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1255(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 4 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1256(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1257, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1258)
    else:
        await r.sotto(s1259)


async def s1257(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 5 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1258(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 5 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1259(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 5 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1260(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1261, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1262)
    else:
        await r.sotto(s1263)


async def s1261(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 6 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1262(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 6 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1263(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 6 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1264(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1265, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1266)
    else:
        await r.sotto(s1267)


async def s1265(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 7 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1266(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 7 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1267(r):
    # automazione Automazione VMC Master > 2 choose 194 > 2 choose 7 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1268(r):
    # automazione Automazione VMC Master > 2 choose 195
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0527, )):
        await r.sotto(s1269)
    else:
        await r.sotto(s1270)
    r.variabili({'vel_fine_delta': Modello(M.m0001), 'memoria_inquinanti_fine_delta': Modello(M.m0794)}, alias='Velocità letta a fine allerta Δ Temp. e memoria Inquinanti della stessa velocità')
    r.verifica()
    if r.prova((k0691, )):
        await r.sotto(s1272)
    r.verifica()
    if r.prova((k0692, )):
        await r.sotto(s1275)
    elif r.prova((k0693, )):
        await r.sotto(s1280)
    elif r.prova((k0694, )):
        await r.sotto(s1286)
    elif r.prova((k0695, )):
        await r.sotto(s1292)
    elif r.prova((k0696, )):
        await r.sotto(s1298)
    elif r.prova((k0697, )):
        await r.sotto(s1304)
    elif r.prova((k0698, )):
        await r.sotto(s1310)
    elif r.prova((k0699, )):
        await r.sotto(s1316)


async def s1269(r):
    # automazione Automazione VMC Master > 2 choose 195 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]}, alias='Spia Comando non eseguito del Calendario OFF: il comando lo rifà il Calendario (la fascia finita o iniziata comanda da sé la VMC)')
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.verifica()
    raise Ferma('Ripresa lasciata al Calendario')


async def s1270(r):
    # automazione Automazione VMC Master > 2 choose 195 > 0 else
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0528, )):
        await r.sotto(s1271)


async def s1271(r):
    # automazione Automazione VMC Master > 2 choose 195 > 0 else > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.verifica()
    raise Ferma('Ripresa lasciata al Calendario (comando del Calendario in sospeso)')


async def s1272(r):
    # automazione Automazione VMC Master > 2 choose 195 > 2 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0689, )):
        await r.sotto(s1273)
    r.verifica()
    if r.prova((k0690, )):
        await r.sotto(s1274)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta Δ Temp. mantenuta")


async def s1273(r):
    # automazione Automazione VMC Master > 2 choose 195 > 2 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': Modello(M.m0795)})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': Modello(M.m0796)})


async def s1274(r):
    # automazione Automazione VMC Master > 2 choose 195 > 2 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s1275(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1276, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s1277)
    else:
        await r.sotto(s1278)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s1279)


async def s1276(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 0 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1277(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1278(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 0 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1279(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1280(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0531, )):
        await r.sotto(s1281)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1282, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s1283)
    else:
        await r.sotto(s1284)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s1285)


async def s1281(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 1 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1282(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1283(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 1 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1284(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 1 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1285(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 1 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1286(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0533, )):
        await r.sotto(s1287)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1288, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s1289)
    else:
        await r.sotto(s1290)
    r.verifica()
    if r.prova((k0194, )):
        await r.sotto(s1291)


async def s1287(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 2 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1288(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1289(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 2 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1290(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 2 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1291(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 2 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1292(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0535, )):
        await r.sotto(s1293)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1294, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s1295)
    else:
        await r.sotto(s1296)
    r.verifica()
    if r.prova((k0197, )):
        await r.sotto(s1297)


async def s1293(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 3 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1294(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1295(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 3 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1296(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 3 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1297(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 3 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1298(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 4
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0537, )):
        await r.sotto(s1299)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1300, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s1301)
    else:
        await r.sotto(s1302)
    r.verifica()
    if r.prova((k0200, )):
        await r.sotto(s1303)


async def s1299(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 4 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1300(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 4 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1301(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 4 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1302(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 4 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")
