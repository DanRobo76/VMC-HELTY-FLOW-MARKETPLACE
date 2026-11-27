"""Automazioni e script del package, tradotti in Python (parte 3 di 8).

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
    k0136, k0137, k0151, k0152, k0158, k0159, k0161, k0162, k0172, k0173,
    k0183, k0190, k0227, k0236, k0237, k0244, k0245, k0246, k0247, k0251,
    k0252, k0254, k0257, k0259, k0261, k0262, k0263, k0264, k0265, k0268,
    k0272, k0273, k0274, k0276, k0277, k0278, k0280, k0284, k0285, k0288,
    k0289, k0291, k0292, k0293, k0294, k0295, k0296, k0297, k0298, k0299,
    k0300, k0301, k0302, k0303, k0304, k0305, k0306, k0307, k0308, k0309,
    k0310, k0311, k0312, k0313, k0317, k0331, k0332, k0333, k0334, k0335,
    k0338, k0339, k0340, k0341, k0343, k0346, k0347, k0348, k0349, k0350,
    k0351, k0352, k0354, k0355, k0356, k0359, k0360, k0365, k0370, k0375,
    k0380, k0385, k0390, k0400, k0401, k0402, k0403, k0404, k0405, k0406,
    k0408, k0410, k0412, k0413, k0414, k0415, k0416, k0417, k0419, k0420,
    k0421, k0422,
)
from .motore_04 import (
    s0698, s0705, s0712, s0719, s0723, s0727, s0728, s0729, s0730, s0732,
    s0736,
)


async def s0359(r):
    # automazione Automazione VMC Master > 2 choose 59 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]}, alias='Tutte le Spie PdR su OFF ')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {}, alias="Imposta Velocità 1 a Causa dell'Inquinamento presente")
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0360(r):
    # automazione Automazione VMC Master > 2 choose 59 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0361(r):
    # automazione Automazione VMC Master > 2 choose 59 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0362(r):
    # automazione Automazione VMC Master > 2 choose 59 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0363(r):
    # automazione Automazione VMC Master > 2 choose 59 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')]})


async def s0364(r):
    # automazione Automazione VMC Master > 2 choose 60
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')]}, alias="Azzera le memorie PdR, come allo spegnimento dell'interruttore con la VMC ON-Line")


async def s0365(r):
    # automazione Automazione VMC Master > 2 choose 61
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0244, )):
        await r.sotto(s0366)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0367, (k0246, ))
    r.verifica()
    if r.prova((k0247, )):
        await r.sotto(s0370)
    else:
        await r.sotto(s0371)


async def s0366(r):
    # automazione Automazione VMC Master > 2 choose 61 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0367(r):
    # automazione Automazione VMC Master > 2 choose 61 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    r.verifica()
    if r.prova((k0245, )):
        await r.sotto(s0368)
    else:
        await r.sotto(s0369)
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0368(r):
    # automazione Automazione VMC Master > 2 choose 61 > 2 repeat > 2 then
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0369(r):
    # automazione Automazione VMC Master > 2 choose 61 > 2 repeat > 2 else
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})


async def s0370(r):
    # automazione Automazione VMC Master > 2 choose 61 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0506)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0371(r):
    # automazione Automazione VMC Master > 2 choose 61 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0372(r):
    # automazione Automazione VMC Master > 2 choose 62
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0373, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0374)
    else:
        await r.sotto(s0375)


async def s0373(r):
    # automazione Automazione VMC Master > 2 choose 62 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0374(r):
    # automazione Automazione VMC Master > 2 choose 62 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0375(r):
    # automazione Automazione VMC Master > 2 choose 62 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0376(r):
    # automazione Automazione VMC Master > 2 choose 63
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0244, )):
        await r.sotto(s0377)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0378, (k0246, ))
    r.verifica()
    if r.prova((k0247, )):
        await r.sotto(s0381)
    else:
        await r.sotto(s0382)


async def s0377(r):
    # automazione Automazione VMC Master > 2 choose 63 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0378(r):
    # automazione Automazione VMC Master > 2 choose 63 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0245, )):
        await r.sotto(s0379)
    else:
        await r.sotto(s0380)
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0379(r):
    # automazione Automazione VMC Master > 2 choose 63 > 2 repeat > 2 then
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})


async def s0380(r):
    # automazione Automazione VMC Master > 2 choose 63 > 2 repeat > 2 else
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})


async def s0381(r):
    # automazione Automazione VMC Master > 2 choose 63 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0506)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0382(r):
    # automazione Automazione VMC Master > 2 choose 63 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0383(r):
    # automazione Automazione VMC Master > 2 choose 64
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0384, (k0251, ))
    r.verifica()
    if r.prova((k0252, )):
        await r.sotto(s0385)
    else:
        await r.sotto(s0386)


async def s0384(r):
    # automazione Automazione VMC Master > 2 choose 64 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0385(r):
    # automazione Automazione VMC Master > 2 choose 64 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0386(r):
    # automazione Automazione VMC Master > 2 choose 64 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0387(r):
    # automazione Automazione VMC Master > 2 choose 65
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0388, (k0254, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0389, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0390)
    else:
        await r.sotto(s0391)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0392)


async def s0388(r):
    # automazione Automazione VMC Master > 2 choose 65 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0389(r):
    # automazione Automazione VMC Master > 2 choose 65 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0390(r):
    # automazione Automazione VMC Master > 2 choose 65 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0391(r):
    # automazione Automazione VMC Master > 2 choose 65 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0392(r):
    # automazione Automazione VMC Master > 2 choose 65 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0393(r):
    # automazione Automazione VMC Master > 2 choose 66
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0394, (k0254, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0395, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0396)
    else:
        await r.sotto(s0397)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0398)


async def s0394(r):
    # automazione Automazione VMC Master > 2 choose 66 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0395(r):
    # automazione Automazione VMC Master > 2 choose 66 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0396(r):
    # automazione Automazione VMC Master > 2 choose 66 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0397(r):
    # automazione Automazione VMC Master > 2 choose 66 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0398(r):
    # automazione Automazione VMC Master > 2 choose 66 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0399(r):
    # automazione Automazione VMC Master > 2 choose 67
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0400, (k0257, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0401, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0402)
    else:
        await r.sotto(s0403)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0404)


async def s0400(r):
    # automazione Automazione VMC Master > 2 choose 67 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})


async def s0401(r):
    # automazione Automazione VMC Master > 2 choose 67 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0402(r):
    # automazione Automazione VMC Master > 2 choose 67 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0403(r):
    # automazione Automazione VMC Master > 2 choose 67 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0404(r):
    # automazione Automazione VMC Master > 2 choose 67 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0405(r):
    # automazione Automazione VMC Master > 2 choose 68
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0406, (k0259, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0407, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0408)
    else:
        await r.sotto(s0409)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0410)


async def s0406(r):
    # automazione Automazione VMC Master > 2 choose 68 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0407(r):
    # automazione Automazione VMC Master > 2 choose 68 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0408(r):
    # automazione Automazione VMC Master > 2 choose 68 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0409(r):
    # automazione Automazione VMC Master > 2 choose 68 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0410(r):
    # automazione Automazione VMC Master > 2 choose 68 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0411(r):
    # automazione Automazione VMC Master > 2 choose 69
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0412)
    elif r.prova((k0237, )):
        await r.sotto(s0418)


async def s0412(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.variabili({'umidita_al_cambio_mese': Modello(M.m0513), 'free_con_allerte': Modello(M.m0514), 'vel_avvio': Modello(M.m0515), 'velocita_finale': Modello(M.m0516), 'comando_vmc': Modello(M.m0517)}, alias="Velocità finale: Velocità 0; con l'allerta Umidità in corso e il mese programmato cambiato (interruttore ancora acceso) la velocità di avvio dell'Umidità come nell'opzione 175 (A3-7); spegnendo l'interruttore resta la Velocità 0 (Foglio A27)")
    r.verifica()
    if r.prova((k0261, )):
        await r.sotto(s0413)
    r.verifica()
    await r.ripeti_finche(s0414, (k0262, ))
    r.verifica()
    if r.prova((k0263, )):
        await r.sotto(s0415)
    else:
        await r.sotto(s0416)
    r.verifica()
    if r.prova((k0264, )):
        await r.sotto(s0417)


async def s0413(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0414(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(Modello(M.m0519), {}, alias="Imposta Velocità 0 (la velocità di avvio dell'Umidità se il mese programmato è cambiato con l'allerta Umidità in corso)")
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0415(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0521)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0416(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 0 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0417(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': Modello(M.m0523)})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0524)})


async def s0418(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating')]})
    r.verifica()
    if r.prova((k0265, )):
        await r.sotto(s0419)


async def s0419(r):
    # automazione Automazione VMC Master > 2 choose 69 > 0 choose 1 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0420(r):
    # automazione Automazione VMC Master > 2 choose 70
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0421)
    elif r.prova((k0237, )):
        await r.sotto(s0427)


async def s0421(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.variabili({'umidita_al_cambio_mese': Modello(M.m0513)}, alias="Con gli Inquinanti resta la Velocità 1 fino al loro rientro; con l'allerta Umidità in corso e il mese programmato cambiato la memoria Umidità diventa «avviata da Velocità 0» (A3-7)")
    r.verifica()
    if r.prova((k0261, )):
        await r.sotto(s0422)
    r.verifica()
    await r.ripeti_finche(s0423, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0424)
    else:
        await r.sotto(s0425)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s0426)


async def s0422(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0423(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {}, alias="Imposta Velocità 1 a Causa dell'Inquinamento presente")
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0424(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0425(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 0 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0426(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0427(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating')]})
    r.verifica()
    if r.prova((k0265, )):
        await r.sotto(s0428)


async def s0428(r):
    # automazione Automazione VMC Master > 2 choose 70 > 0 choose 1 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0429(r):
    # automazione Automazione VMC Master > 2 choose 71
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0430)
    elif r.prova((k0237, )):
        await r.sotto(s0436)


async def s0430(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.variabili({'umidita_al_cambio_mese': Modello(M.m0527), 'free_con_allerte': Modello(M.m0514), 'vel_avvio': Modello(M.m0515), 'velocita_finale': Modello(M.m0516), 'comando_vmc': Modello(M.m0517)}, alias="Velocità finale: Velocità 0; con l'allerta Umidità in corso e il mese programmato cambiato (interruttore ancora acceso) la velocità di avvio dell'Umidità come nell'opzione 175 (A3-7); spegnendo l'interruttore resta la Velocità 0 (Foglio A27)")
    r.verifica()
    if r.prova((k0261, )):
        await r.sotto(s0431)
    r.verifica()
    await r.ripeti_finche(s0432, (k0262, ))
    r.verifica()
    if r.prova((k0263, )):
        await r.sotto(s0433)
    else:
        await r.sotto(s0434)
    r.verifica()
    if r.prova((k0264, )):
        await r.sotto(s0435)


async def s0431(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0432(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(Modello(M.m0519), {}, alias="Imposta Velocità 0 (la velocità di avvio dell'Umidità se il mese programmato è cambiato con l'allerta Umidità in corso)")
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0433(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0521)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0434(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 0 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0435(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': Modello(M.m0523)})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0524)})


async def s0436(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling')]})
    r.verifica()
    if r.prova((k0268, )):
        await r.sotto(s0437)


async def s0437(r):
    # automazione Automazione VMC Master > 2 choose 71 > 0 choose 1 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})


async def s0438(r):
    # automazione Automazione VMC Master > 2 choose 72
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0439)
    elif r.prova((k0237, )):
        await r.sotto(s0445)


async def s0439(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.variabili({'umidita_al_cambio_mese': Modello(M.m0527)}, alias="Con gli Inquinanti resta la Velocità 1 fino al loro rientro; con l'allerta Umidità in corso e il mese programmato cambiato la memoria Umidità diventa «avviata da Velocità 0» (A3-7)")
    r.verifica()
    if r.prova((k0261, )):
        await r.sotto(s0440)
    r.verifica()
    await r.ripeti_finche(s0441, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0442)
    else:
        await r.sotto(s0443)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s0444)


async def s0440(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0441(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {}, alias="Imposta Velocità 1 a Causa dell'Inquinamento presente")
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0442(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0443(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 0 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0444(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0445(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling')]})
    r.verifica()
    if r.prova((k0268, )):
        await r.sotto(s0446)


async def s0446(r):
    # automazione Automazione VMC Master > 2 choose 72 > 0 choose 1 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})


async def s0447(r):
    # automazione Automazione VMC Master > 2 choose 73
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0448)
    elif r.prova((k0237, )):
        await r.sotto(s0453)


async def s0448(r):
    # automazione Automazione VMC Master > 2 choose 73 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0449, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0450)
    else:
        await r.sotto(s0451)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s0452)


async def s0449(r):
    # automazione Automazione VMC Master > 2 choose 73 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0450(r):
    # automazione Automazione VMC Master > 2 choose 73 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0451(r):
    # automazione Automazione VMC Master > 2 choose 73 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0452(r):
    # automazione Automazione VMC Master > 2 choose 73 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0453(r):
    # automazione Automazione VMC Master > 2 choose 73 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')]})


async def s0454(r):
    # automazione Automazione VMC Master > 2 choose 74
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0455)
    elif r.prova((k0237, )):
        await r.sotto(s0459)


async def s0455(r):
    # automazione Automazione VMC Master > 2 choose 74 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), c.N('binary_sensor.vmc_master_spia_calendario_black_out'), c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]}, alias='Tutte le Spie dei Giorni del Calendario su OFF ')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0456, (k0272, ))
    r.verifica()
    if r.prova((k0273, )):
        await r.sotto(s0457)
    r.verifica()
    if r.prova((k0274, )):
        await r.sotto(s0458)


async def s0456(r):
    # automazione Automazione VMC Master > 2 choose 74 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0457(r):
    # automazione Automazione VMC Master > 2 choose 74 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0458(r):
    # automazione Automazione VMC Master > 2 choose 74 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0459(r):
    # automazione Automazione VMC Master > 2 choose 74 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')]})


async def s0460(r):
    # automazione Automazione VMC Master > 2 choose 75
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0461)
    elif r.prova((k0237, )):
        await r.sotto(s0465)


async def s0461(r):
    # automazione Automazione VMC Master > 2 choose 75 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1'), c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2'), c.N('binary_sensor.vmc_master_spia_calendario_martedi_1'), c.N('binary_sensor.vmc_master_spia_calendario_martedi_2'), c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1'), c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2'), c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1'), c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2'), c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1'), c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2'), c.N('binary_sensor.vmc_master_spia_calendario_sabato_1'), c.N('binary_sensor.vmc_master_spia_calendario_sabato_2'), c.N('binary_sensor.vmc_master_spia_calendario_domenica_1'), c.N('binary_sensor.vmc_master_spia_calendario_domenica_2'), c.N('binary_sensor.vmc_master_spia_calendario_black_out'), c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_0_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_1_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_2_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_3_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_4_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_congelamento'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0462, (k0276, ))
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0463)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0464)


async def s0462(r):
    # automazione Automazione VMC Master > 2 choose 75 > 0 choose 0 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0463(r):
    # automazione Automazione VMC Master > 2 choose 75 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0464(r):
    # automazione Automazione VMC Master > 2 choose 75 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0465(r):
    # automazione Automazione VMC Master > 2 choose 75 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')]})


async def s0466(r):
    # automazione Automazione VMC Master > 2 choose 76
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0280, )):
        await r.sotto(s0467)
    else:
        await r.sotto(s0468)


async def s0467(r):
    # automazione Automazione VMC Master > 2 choose 76 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})


async def s0468(r):
    # automazione Automazione VMC Master > 2 choose 76 > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')]})


async def s0469(r):
    # automazione Automazione VMC Master > 2 choose 77
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0285, )):
        await r.sotto(s0470)


async def s0470(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0284, )):
        await r.sotto(s0471)
    else:
        await r.sotto(s0476)


async def s0471(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_umidita_verifica_soglia_valore_spia')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_1'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_2'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_3'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_4'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_umidita_velocita_freecooling')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0472, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0473)
    else:
        await r.sotto(s0474)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s0475)


async def s0472(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then > 0 then > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))


async def s0473(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then > 0 then > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0474(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then > 0 then > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0475(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then > 0 then > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0476(r):
    # automazione Automazione VMC Master > 2 choose 77 > 0 then > 0 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('switch.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')]})


async def s0477(r):
    # automazione Automazione VMC Master > 2 choose 78
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0478(r):
    # automazione Automazione VMC Master > 2 choose 79
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0289, )):
        await r.sotto(s0479)


async def s0479(r):
    # automazione Automazione VMC Master > 2 choose 79 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0480)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_calendario_black_out')]})
    r.verifica()
    raise Ferma("Velocità 1 scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0480(r):
    # automazione Automazione VMC Master > 2 choose 79 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})


async def s0481(r):
    # automazione Automazione VMC Master > 2 choose 80
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0482)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias='Memorizza la velocità letta alla riaccensione della VMC')
    r.verifica()
    if r.prova((k0294, k0295, )):
        await r.sotto(s0485)
    elif r.prova((k0297, k0295, )):
        await r.sotto(s0487)
    elif r.prova((k0299, k0295, )):
        await r.sotto(s0489)
    elif r.prova((k0301, k0295, )):
        await r.sotto(s0491)
    elif r.prova((k0303, k0295, )):
        await r.sotto(s0493)
    elif r.prova((k0305, k0295, )):
        await r.sotto(s0495)
    elif r.prova((k0307, k0295, )):
        await r.sotto(s0497)
    elif r.prova((k0309, k0295, )):
        await r.sotto(s0499)
    elif r.prova((k0310, k0311, )):
        await r.sotto(s0501)
    else:
        await r.sotto(s0503)
    await r.attendi(M.m0564, timeout=timedelta(days=0, seconds=12, microseconds=0), alias='Ripristino dopo il Black-Out: attende che la VMC esegua il comando (al massimo 12 s) prima di spegnere le spie, così le allerte in attesa della fine del Black-Out memorizzano la velocità ripristinata (non attende se è iniziata una Fascia del Calendario con la velocità della VMC non leggibile)')
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0482(r):
    # automazione Automazione VMC Master > 2 choose 80 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0483)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0483(r):
    # automazione Automazione VMC Master > 2 choose 80 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0484)


async def s0484(r):
    # automazione Automazione VMC Master > 2 choose 80 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0485(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0486, (k0293, ))


async def s0486(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0487(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0488, (k0296, ))


async def s0488(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0489(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 2
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0490, (k0298, ))


async def s0490(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0491(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 3
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0492, (k0300, ))


async def s0492(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0493(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 4
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0494, (k0302, ))


async def s0494(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 4 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0495(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 5
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0496, (k0304, ))


async def s0496(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 5 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0497(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 6
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0498, (k0306, ))


async def s0498(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 6 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0499(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 7
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0500, (k0308, ))


async def s0500(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 7 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0501(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 8
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0502, (k0296, ))
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})


async def s0502(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 choose 8 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0503(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 default
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0312, )):
        await r.sotto(s0504)


async def s0504(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 default > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0505, (k0293, ))


async def s0505(r):
    # automazione Automazione VMC Master > 2 choose 80 > 2 default > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0506(r):
    # automazione Automazione VMC Master > 2 choose 81
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0507(r):
    # automazione Automazione VMC Master > 2 choose 82
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0508(r):
    # automazione Automazione VMC Master > 2 choose 83
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0310, )):
        await r.sotto(s0509)
    elif r.prova((k0317, )):
        await r.sotto(s0510)


async def s0509(r):
    # automazione Automazione VMC Master > 2 choose 83 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0510(r):
    # automazione Automazione VMC Master > 2 choose 83 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0511(r):
    # automazione Automazione VMC Master > 2 choose 84
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0512)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0515, (k0296, ))
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0512(r):
    # automazione Automazione VMC Master > 2 choose 84 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0513)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0513(r):
    # automazione Automazione VMC Master > 2 choose 84 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0514)


async def s0514(r):
    # automazione Automazione VMC Master > 2 choose 84 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0515(r):
    # automazione Automazione VMC Master > 2 choose 84 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0516(r):
    # automazione Automazione VMC Master > 2 choose 85
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0517(r):
    # automazione Automazione VMC Master > 2 choose 86
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0518)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0521, (k0298, ))
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0518(r):
    # automazione Automazione VMC Master > 2 choose 86 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0519)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0519(r):
    # automazione Automazione VMC Master > 2 choose 86 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0520)


async def s0520(r):
    # automazione Automazione VMC Master > 2 choose 86 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0521(r):
    # automazione Automazione VMC Master > 2 choose 86 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0522(r):
    # automazione Automazione VMC Master > 2 choose 87
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0523(r):
    # automazione Automazione VMC Master > 2 choose 88
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0524)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0527, (k0300, ))
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0524(r):
    # automazione Automazione VMC Master > 2 choose 88 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0525)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0525(r):
    # automazione Automazione VMC Master > 2 choose 88 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0526)


async def s0526(r):
    # automazione Automazione VMC Master > 2 choose 88 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0527(r):
    # automazione Automazione VMC Master > 2 choose 88 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0528(r):
    # automazione Automazione VMC Master > 2 choose 89
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0529(r):
    # automazione Automazione VMC Master > 2 choose 90
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0530)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0533, (k0302, ))
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0530(r):
    # automazione Automazione VMC Master > 2 choose 90 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0531)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0531(r):
    # automazione Automazione VMC Master > 2 choose 90 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0532)


async def s0532(r):
    # automazione Automazione VMC Master > 2 choose 90 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0533(r):
    # automazione Automazione VMC Master > 2 choose 90 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0534(r):
    # automazione Automazione VMC Master > 2 choose 91
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0535(r):
    # automazione Automazione VMC Master > 2 choose 92
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0536)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0539, (k0304, ))
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0536(r):
    # automazione Automazione VMC Master > 2 choose 92 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0537)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0537(r):
    # automazione Automazione VMC Master > 2 choose 92 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0538)


async def s0538(r):
    # automazione Automazione VMC Master > 2 choose 92 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0539(r):
    # automazione Automazione VMC Master > 2 choose 92 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0540(r):
    # automazione Automazione VMC Master > 2 choose 93
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0541(r):
    # automazione Automazione VMC Master > 2 choose 94
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0542)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0545, (k0308, ))
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0542(r):
    # automazione Automazione VMC Master > 2 choose 94 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0543)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0543(r):
    # automazione Automazione VMC Master > 2 choose 94 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0544)


async def s0544(r):
    # automazione Automazione VMC Master > 2 choose 94 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0545(r):
    # automazione Automazione VMC Master > 2 choose 94 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0546(r):
    # automazione Automazione VMC Master > 2 choose 95
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0547(r):
    # automazione Automazione VMC Master > 2 choose 96
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0548)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias='Memorizza la velocità letta alla riaccensione della VMC')
    r.verifica()
    if r.prova((k0331, )):
        await r.sotto(s0551)
    elif r.prova((k0332, )):
        await r.sotto(s0553)
    elif r.prova((k0333, )):
        await r.sotto(s0555)
    elif r.prova((k0334, )):
        await r.sotto(s0557)
    else:
        await r.sotto(s0559)
    await r.attendi(M.m0564, timeout=timedelta(days=0, seconds=12, microseconds=0), alias='Ripristino dopo il Black-Out: attende che la VMC esegua il comando (al massimo 12 s) prima di spegnere le spie, così le allerte in attesa della fine del Black-Out memorizzano la velocità ripristinata (non attende se è iniziata una Fascia del Calendario con la velocità della VMC non leggibile)')
    if not r.passo_condizione(k0313, 'Fascia del Calendario iniziata con la velocità della VMC non leggibile (ripristino non confermato): la memoria del Black-Out resta e la spegne lo script della Fascia quando la Fascia parte (subito, se Home Assistant vede ancora la VMC ON-Line, altrimenti al suo ritorno); se la Fascia finisce prima di partire, al ritorno della VMC avviene il ripristino [Foglio Logiche A23 e A25]'):
        return
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})


async def s0548(r):
    # automazione Automazione VMC Master > 2 choose 96 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0288, )):
        await r.sotto(s0549)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)")


async def s0549(r):
    # automazione Automazione VMC Master > 2 choose 96 > 0 then > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    r.verifica()
    if r.prova((k0291, )):
        await r.sotto(s0550)


async def s0550(r):
    # automazione Automazione VMC Master > 2 choose 96 > 0 then > 0 then > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]})


async def s0551(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0552, (k0306, ))


async def s0552(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0553(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0554, (k0306, ))


async def s0554(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0555(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 2
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0556, (k0306, ))


async def s0556(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0557(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 3
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0558, (k0296, ))


async def s0558(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0559(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 default
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0335, )):
        await r.sotto(s0560)
    else:
        await r.sotto(s0562)


async def s0560(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 default > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0561, (k0296, ))


async def s0561(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 default > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0562(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 default > 0 default
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0563, (k0306, ))


async def s0563(r):
    # automazione Automazione VMC Master > 2 choose 96 > 2 default > 0 default > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0564(r):
    # automazione Automazione VMC Master > 2 choose 97
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_black_out')]})


async def s0565(r):
    # automazione Automazione VMC Master > 2 choose 98
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_black_out')]}, alias='Spia Black-Out del Calendario OFF (il ritorno della corrente si gestisce una sola volta)')
    if not r.passo_condizione(k0338, 'Interruttore del Calendario acceso, VMC ON-Line e velocità della VMC disponibile'):
        return
    r.verifica()
    if r.prova((k0292, )):
        await r.sotto(s0566)
    r.verifica()
    if r.prova((k0339, )):
        await r.sotto(s0567)
    r.verifica()
    if r.prova((k0340, )):
        await r.sotto(s0568)
    elif r.prova((k0341, )):
        await r.sotto(s0569)


async def s0566(r):
    # automazione Automazione VMC Master > 2 choose 98 > 2 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (la Fascia non riparte)")


async def s0567(r):
    # automazione Automazione VMC Master > 2 choose 98 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})
    r.verifica()
    raise Ferma("Fascia rimandata alla fine dell'allerta Congelamento o Δ Temp.")


async def s0568(r):
    # automazione Automazione VMC Master > 2 choose 98 > 4 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0569(r):
    # automazione Automazione VMC Master > 2 choose 98 > 4 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0570(r):
    # automazione Automazione VMC Master > 2 choose 99
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_black_out')]}, alias='Spia Black-Out del Calendario OFF (il ritorno della corrente si gestisce una sola volta)')
    r.verifica()
    if r.prova((k0343, )):
        await r.sotto(s0571)
    if not r.passo_condizione(k0338, 'Interruttore del Calendario acceso, VMC ON-Line e velocità della VMC disponibile'):
        return
    r.verifica()
    if r.prova((k0339, )):
        await r.sotto(s0572)
    r.verifica()
    if r.prova((k0340, )):
        await r.sotto(s0573)
    elif r.prova((k0341, )):
        await r.sotto(s0574)


async def s0571(r):
    # automazione Automazione VMC Master > 2 choose 99 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_black_out')]})
    r.verifica()
    raise Ferma('Ritorno della Fascia lasciato alla Spia Black-Out del Calendario (velocità non ancora leggibile)')


async def s0572(r):
    # automazione Automazione VMC Master > 2 choose 99 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})
    r.verifica()
    raise Ferma("Fascia rimandata alla fine dell'allerta Congelamento o Δ Temp.")


async def s0573(r):
    # automazione Automazione VMC Master > 2 choose 99 > 4 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0574(r):
    # automazione Automazione VMC Master > 2 choose 99 > 4 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0575(r):
    # automazione Automazione VMC Master > 2 choose 100
    c, V = r.c, r.V
    r.variabili({'comando_non_eseguito_dalle': Modello(M.m0577)}, alias='Memorizza quando il Calendario non ha potuto comandare la VMC (accensione della Spia Comando non eseguito del Calendario)')
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]}, alias='Spia Comando non eseguito del Calendario OFF (il ritorno della VMC si gestisce una sola volta)')
    if not r.passo_condizione(k0346, "VMC ON-Line senza Black-Out del Calendario e velocità della VMC disponibile (l'interruttore del Calendario serve solo per far ripartire la Fascia: la Velocità 0, o 1, dello spegnimento del Calendario si ripete anche spento)"):
        return
    r.verifica()
    if r.prova((k0340, k0347, )):
        await r.sotto(s0576)
    elif r.prova((k0341, k0347, )):
        await r.sotto(s0577)
    elif r.prova((k0348, k0349, k0350, k0351, )):
        await r.sotto(s0578)
    elif r.prova((k0348, k0349, k0350, k0352, )):
        await r.sotto(s0582)


async def s0576(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {'comando_non_eseguito_dalle': Modello(M.m0579)}, alias='Lo script della Fascia riparte solo se la velocità della VMC non è cambiata da quando la Fascia non ha potuto comandarla (controllo dopo i 5 s dello script, con le letture già aggiornate)')


async def s0577(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {'comando_non_eseguito_dalle': Modello(M.m0579)}, alias='Lo script della Fascia riparte solo se la velocità della VMC non è cambiata da quando la Fascia non ha potuto comandarla (controllo dopo i 5 s dello script, con le letture già aggiornate)')


async def s0578(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 2
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0579, (k0276, ))
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0580)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0581)


async def s0579(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0580(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 2 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0581(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 2 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0582(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc')]}, alias='Memorie di velocità degli Inquinanti OFF (una velocità memorizzata sulla lettura vecchia, mentre la velocità non si leggeva, non vale) come nello spegnimento del Calendario')
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc')]}, alias='Spia Inquinanti, memoria della partenza da Velocità 0 e memorie Velocità 1 Inquinanti e PdR ON come nello spegnimento del Calendario: a fine Inquinanti la VMC torna a Velocità 0')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0583, (k0272, ))
    r.verifica()
    if r.prova((k0273, )):
        await r.sotto(s0584)
    r.verifica()
    if r.prova((k0274, )):
        await r.sotto(s0585)


async def s0583(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 3 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0584(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 3 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0585(r):
    # automazione Automazione VMC Master > 2 choose 100 > 3 choose 3 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0586(r):
    # automazione Automazione VMC Master > 2 choose 101
    c, V = r.c, r.V
    r.variabili({'comando_non_eseguito': Modello(M.m0585), 'velocita_del_comando': Modello(M.m0586), 'comando_non_eseguito_dalle': Modello(M.m0587), 'comando_vmc': Modello(M.m0588)}, alias='Velocità del comando non eseguito e ora in cui il ciclo di conferma si è fermato')
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias='Comando non eseguito cancellato (il ritorno della velocità si gestisce una sola volta)')
    if not r.passo_condizione(k0354, "VMC ON-Line senza Black-Out del Calendario (con il Black-Out la Fascia riparte dal ritorno della corrente e le allerte dopo di lei), velocità disponibile, diversa da quella del comando e non cambiata da quando il comando non è stato eseguito (scelta dell'utente, altro comando o Fascia ripartita prima: il trigger aspetta il comando del Calendario in sospeso, salvo con Congelamento o Δ Temp. in corso, che hanno la precedenza)"):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0587, (k0355, ))
    r.verifica()
    if r.prova((k0356, )):
        await r.sotto(s0588)
    else:
        await r.sotto(s0589)


async def s0587(r):
    # automazione Automazione VMC Master > 2 choose 101 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0519), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0588(r):
    # automazione Automazione VMC Master > 2 choose 101 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0591)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0589(r):
    # automazione Automazione VMC Master > 2 choose 101 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0590(r):
    # automazione Automazione VMC Master > 2 choose 102
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0591(r):
    # automazione Automazione VMC Master > 2 choose 103
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_lunedi_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0359, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Lunedì è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0592, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0593)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0594)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0595)


async def s0592(r):
    # automazione Automazione VMC Master > 2 choose 103 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0593(r):
    # automazione Automazione VMC Master > 2 choose 103 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0594(r):
    # automazione Automazione VMC Master > 2 choose 103 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0595(r):
    # automazione Automazione VMC Master > 2 choose 103 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0596(r):
    # automazione Automazione VMC Master > 2 choose 104
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0597(r):
    # automazione Automazione VMC Master > 2 choose 105
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_lunedi_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0598, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0599)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0600)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0601)


async def s0598(r):
    # automazione Automazione VMC Master > 2 choose 105 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0599(r):
    # automazione Automazione VMC Master > 2 choose 105 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0600(r):
    # automazione Automazione VMC Master > 2 choose 105 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0601(r):
    # automazione Automazione VMC Master > 2 choose 105 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0602(r):
    # automazione Automazione VMC Master > 2 choose 106
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0603(r):
    # automazione Automazione VMC Master > 2 choose 107
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_martedi_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0365, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Martedì è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0604, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0605)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0606)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0607)


async def s0604(r):
    # automazione Automazione VMC Master > 2 choose 107 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0605(r):
    # automazione Automazione VMC Master > 2 choose 107 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0606(r):
    # automazione Automazione VMC Master > 2 choose 107 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0607(r):
    # automazione Automazione VMC Master > 2 choose 107 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0608(r):
    # automazione Automazione VMC Master > 2 choose 108
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0609(r):
    # automazione Automazione VMC Master > 2 choose 109
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_martedi_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0610, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0611)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0612)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0613)


async def s0610(r):
    # automazione Automazione VMC Master > 2 choose 109 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0611(r):
    # automazione Automazione VMC Master > 2 choose 109 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0612(r):
    # automazione Automazione VMC Master > 2 choose 109 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0613(r):
    # automazione Automazione VMC Master > 2 choose 109 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0614(r):
    # automazione Automazione VMC Master > 2 choose 110
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0615(r):
    # automazione Automazione VMC Master > 2 choose 111
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0370, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Mercoledì è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0616, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0617)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0618)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0619)


async def s0616(r):
    # automazione Automazione VMC Master > 2 choose 111 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0617(r):
    # automazione Automazione VMC Master > 2 choose 111 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0618(r):
    # automazione Automazione VMC Master > 2 choose 111 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0619(r):
    # automazione Automazione VMC Master > 2 choose 111 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0620(r):
    # automazione Automazione VMC Master > 2 choose 112
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0621(r):
    # automazione Automazione VMC Master > 2 choose 113
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_mercoledi_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0622, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0623)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0624)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0625)


async def s0622(r):
    # automazione Automazione VMC Master > 2 choose 113 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0623(r):
    # automazione Automazione VMC Master > 2 choose 113 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0624(r):
    # automazione Automazione VMC Master > 2 choose 113 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0625(r):
    # automazione Automazione VMC Master > 2 choose 113 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0626(r):
    # automazione Automazione VMC Master > 2 choose 114
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0627(r):
    # automazione Automazione VMC Master > 2 choose 115
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_giovedi_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0375, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Giovedì è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0628, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0629)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0630)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0631)


async def s0628(r):
    # automazione Automazione VMC Master > 2 choose 115 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0629(r):
    # automazione Automazione VMC Master > 2 choose 115 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0630(r):
    # automazione Automazione VMC Master > 2 choose 115 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0631(r):
    # automazione Automazione VMC Master > 2 choose 115 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0632(r):
    # automazione Automazione VMC Master > 2 choose 116
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0633(r):
    # automazione Automazione VMC Master > 2 choose 117
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_giovedi_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0634, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0635)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0636)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0637)


async def s0634(r):
    # automazione Automazione VMC Master > 2 choose 117 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0635(r):
    # automazione Automazione VMC Master > 2 choose 117 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0636(r):
    # automazione Automazione VMC Master > 2 choose 117 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0637(r):
    # automazione Automazione VMC Master > 2 choose 117 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0638(r):
    # automazione Automazione VMC Master > 2 choose 118
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0639(r):
    # automazione Automazione VMC Master > 2 choose 119
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_venerdi_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0380, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Venerdì è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0640, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0641)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0642)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0643)


async def s0640(r):
    # automazione Automazione VMC Master > 2 choose 119 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0641(r):
    # automazione Automazione VMC Master > 2 choose 119 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0642(r):
    # automazione Automazione VMC Master > 2 choose 119 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0643(r):
    # automazione Automazione VMC Master > 2 choose 119 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0644(r):
    # automazione Automazione VMC Master > 2 choose 120
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0645(r):
    # automazione Automazione VMC Master > 2 choose 121
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_venerdi_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0646, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0647)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0648)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0649)


async def s0646(r):
    # automazione Automazione VMC Master > 2 choose 121 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0647(r):
    # automazione Automazione VMC Master > 2 choose 121 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0648(r):
    # automazione Automazione VMC Master > 2 choose 121 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0649(r):
    # automazione Automazione VMC Master > 2 choose 121 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0650(r):
    # automazione Automazione VMC Master > 2 choose 122
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0651(r):
    # automazione Automazione VMC Master > 2 choose 123
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_sabato_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0385, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Sabato è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0652, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0653)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0654)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0655)


async def s0652(r):
    # automazione Automazione VMC Master > 2 choose 123 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0653(r):
    # automazione Automazione VMC Master > 2 choose 123 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0654(r):
    # automazione Automazione VMC Master > 2 choose 123 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0655(r):
    # automazione Automazione VMC Master > 2 choose 123 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0656(r):
    # automazione Automazione VMC Master > 2 choose 124
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0657(r):
    # automazione Automazione VMC Master > 2 choose 125
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_sabato_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0658, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0659)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0660)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0661)


async def s0658(r):
    # automazione Automazione VMC Master > 2 choose 125 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0659(r):
    # automazione Automazione VMC Master > 2 choose 125 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0660(r):
    # automazione Automazione VMC Master > 2 choose 125 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0661(r):
    # automazione Automazione VMC Master > 2 choose 125 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0662(r):
    # automazione Automazione VMC Master > 2 choose 126
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_on'), {})


async def s0663(r):
    # automazione Automazione VMC Master > 2 choose 127
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_domenica_1')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    if not r.passo_condizione(k0390, 'Allerta a cavallo delle due fasce: se la 2° Fascia di Domenica è già in corso non si ferma la VMC (la comanda la 2° Fascia) e non si azzerano le spie: si evita il comando Velocità 0 subito seguito dalla velocità della 2° Fascia'):
        return
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0664, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0665)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0666)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0667)


async def s0664(r):
    # automazione Automazione VMC Master > 2 choose 127 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0665(r):
    # automazione Automazione VMC Master > 2 choose 127 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0666(r):
    # automazione Automazione VMC Master > 2 choose 127 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0667(r):
    # automazione Automazione VMC Master > 2 choose 127 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0668(r):
    # automazione Automazione VMC Master > 2 choose 128
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')]})
    await r.servizio(c.N('script.vmc_master_calendario_fascia_2_on'), {})


async def s0669(r):
    # automazione Automazione VMC Master > 2 choose 129
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_domenica_2')]})
    r.variabili({'black_out_durante_la_fascia': Modello(M.m0593)}, alias='Memorizza se la Spia Black-Out del Calendario è accesa (Black-Out durante la Fascia, finita prima del ritorno della corrente): la spengono le spie azzerate a fine Fascia')
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0670, (k0276, ))
    await r.servizio(c.N('script.vmc_master_calendario_fascia_1_o_2_off'), {})
    r.verifica()
    if r.prova((k0277, )):
        await r.sotto(s0671)
    r.verifica()
    if r.prova((k0278, )):
        await r.sotto(s0672)
    r.verifica()
    if r.prova((k0360, )):
        await r.sotto(s0673)


async def s0670(r):
    # automazione Automazione VMC Master > 2 choose 129 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0671(r):
    # automazione Automazione VMC Master > 2 choose 129 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_1'), c.N('binary_sensor.vmc_master_spia_velocita_2'), c.N('binary_sensor.vmc_master_spia_velocita_3'), c.N('binary_sensor.vmc_master_spia_velocita_4'), c.N('binary_sensor.vmc_master_spia_velocita_notturna'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling')]})


async def s0672(r):
    # automazione Automazione VMC Master > 2 choose 129 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_calendario_comando_non_eseguito')]})


async def s0673(r):
    # automazione Automazione VMC Master > 2 choose 129 > 7 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})


async def s0674(r):
    # automazione Automazione VMC Master > 2 choose 130
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_rimuovi_caratteri_di_ritorno'), {})
    await r.servizio(c.N('shell_command.vmc_master_cambia_nome'), {}, alias='Chiama il Servizio per Cambiare nome alla VMC')
    await r.pausa(timedelta(days=0, seconds=4, microseconds=0))
    await r.servizio('homeassistant.update_entity', {}, {'entity_id': [c.N('sensor.vmc_master_nome')]})
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('text.vmc_master_nome_da_inserire')]})


async def s0675(r):
    # automazione Automazione VMC Master > 2 choose 131
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_opzioni_accendi_spegni_avvisi_spia')]})


async def s0676(r):
    # automazione Automazione VMC Master > 2 choose 132
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_opzioni_accendi_spegni_avvisi_spia')]})


async def s0677(r):
    # automazione Automazione VMC Master > 2 choose 133
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_popup_versione_corrente_vs_repository')]})


async def s0678(r):
    # automazione Automazione VMC Master > 2 choose 134
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_popup_versione_corrente_vs_repository')]})


async def s0679(r):
    # automazione Automazione VMC Master > 2 choose 135
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc')]})
    r.verifica()
    if r.prova((k0400, )):
        await r.sotto(s0680)
    elif r.prova((k0404, )):
        await r.sotto(s0684)
    elif r.prova((k0406, )):
        await r.sotto(s0691)
    elif r.prova((k0408, )):
        await r.sotto(s0698)
    elif r.prova((k0410, )):
        await r.sotto(s0705)
    elif r.prova((k0412, )):
        await r.sotto(s0712)
    elif r.prova((k0413, )):
        await r.sotto(s0719)
    elif r.prova((k0414, )):
        await r.sotto(s0723)
    elif r.prova((k0415, )):
        await r.sotto(s0727)
    elif r.prova((k0416, )):
        await r.sotto(s0728)
    elif r.prova((k0417, )):
        await r.sotto(s0729)
    elif r.prova((k0419, )):
        await r.sotto(s0730)
    elif r.prova((k0420, k0421, )):
        await r.sotto(s0732)
    elif r.prova((k0422, k0421, )):
        await r.sotto(s0736)


async def s0680(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0681, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0682)
    else:
        await r.sotto(s0683)


async def s0681(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0682(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0683(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0684(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0685, (k0403, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0688, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s0689)
    else:
        await r.sotto(s0690)


async def s0685(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    if r.prova((k0401, k0402, )):
        await r.sotto(s0686)
    else:
        await r.sotto(s0687)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0686(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1 > 0 repeat > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')]})


async def s0687(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1 > 0 repeat > 1 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio')]})


async def s0688(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0689(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0690(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 1 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0691(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0692, (k0405, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0695, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s0696)
    else:
        await r.sotto(s0697)


async def s0692(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    if r.prova((k0401, k0402, )):
        await r.sotto(s0693)
    else:
        await r.sotto(s0694)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('binary_sensor.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('binary_sensor.vmc_master_spia_velocita_0_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_1_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_2_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_4_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('binary_sensor.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('binary_sensor.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0693(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 0 repeat > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')]})


async def s0694(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 0 repeat > 1 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('binary_sensor.vmc_master_spia_velocita_3_un_solo_avvio')]})


async def s0695(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0696(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]})


async def s0697(r):
    # automazione Automazione VMC Master > 2 choose 135 > 1 choose 2 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('sensor.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")
