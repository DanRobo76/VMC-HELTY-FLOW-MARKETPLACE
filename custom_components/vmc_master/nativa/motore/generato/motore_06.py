"""Automazioni e script del package, tradotti in Python (parte 6 di 8).

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
    k0167, k0168, k0172, k0173, k0178, k0179, k0203, k0214, k0227, k0539,
    k0541, k0543, k0701, k0702, k0703, k0704, k0705, k0706, k0707, k0708,
    k0709, k0710, k0711, k0712, k0713, k0714, k0715, k0716, k0717, k0718,
    k0719, k0720, k0721, k0722, k0723, k0724, k0725, k0726, k0727, k0728,
    k0729, k0730, k0731, k0732, k0733, k0734, k0735, k0736, k0737, k0738,
    k0739, k0740, k0741, k0742, k0743, k0744, k0745, k0746, k0747, k0748,
    k0749, k0750, k0753, k0755, k0757, k0758, k0761, k0763, k0764, k0766,
    k0767, k0769, k0770, k0772, k0773, k0775, k0776, k0778, k0792, k0793,
)
from .motore_07 import (
    s1650, s1652, s1661, s1670, s1830,
)


async def s1303(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 4 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1304(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 5
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0539, )):
        await r.sotto(s1305)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1306, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s1307)
    else:
        await r.sotto(s1308)
    r.verifica()
    if r.prova((k0214, )):
        await r.sotto(s1309)


async def s1305(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 5 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1306(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 5 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1307(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 5 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1308(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 5 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1309(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 5 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1310(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 6
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0541, )):
        await r.sotto(s1311)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1312, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s1313)
    else:
        await r.sotto(s1314)
    r.verifica()
    if r.prova((k0203, )):
        await r.sotto(s1315)


async def s1311(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 6 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1312(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 6 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1313(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 6 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1314(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 6 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1315(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 6 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s1316(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 7
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0543, )):
        await r.sotto(s1317)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s1318, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s1319)
    else:
        await r.sotto(s1320)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s1321)


async def s1317(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 7 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})


async def s1318(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 7 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1319(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 7 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s1320(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 7 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s1321(r):
    # automazione Automazione VMC Master > 2 choose 195 > 3 choose 7 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})


async def s1322(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0897)}, {'entity_id': [c.N('input_select.vmc_master_selected_temp_external_entity')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0705, )):
        await r.sotto(s1323)
    elif r.prova((k0704, )):
        await r.sotto(s1328)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_temp_external_entity'), c.N('input_text.vmc_master_last_temp_external_entity')]})


async def s1323(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0701, )):
        await r.sotto(s1324)
    r.verifica()
    if r.prova((k0703, )):
        await r.sotto(s1325)
    r.verifica()
    if r.prova((k0704, )):
        await r.sotto(s1327)


async def s1324(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0898)}, {'entity_id': [c.N('input_select.vmc_master_selected_temp_external_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_temperatura_esterna')})


async def s1325(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Entità Temperatura Esterna'}, {'entity_id': [c.N('input_select.vmc_master_selected_temp_external_entity')]})
    r.verifica()
    if r.prova((k0702, )):
        await r.sotto(s1326)


async def s1326(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna > 2 choose 0 > 1 choose 0 > 1 then
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_temperatura_esterna'), 'title': Modello(M.m0721), 'message': "Aggiornare Manualmente l'Entità Temperatura Esterna"})


async def s1327(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0902)}, {'entity_id': [c.N('input_text.vmc_master_last_temp_external_entity')]})


async def s1328(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_esterna > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0902)}, {'entity_id': [c.N('input_text.vmc_master_last_temp_external_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_temperatura_esterna')})


async def s1329(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0905)}, {'entity_id': [c.N('input_select.vmc_master_selected_temp_internal_entity')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0710, )):
        await r.sotto(s1330)
    elif r.prova((k0709, )):
        await r.sotto(s1335)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_temp_internal_entity'), c.N('input_text.vmc_master_last_temp_internal_entity')]})


async def s1330(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0706, )):
        await r.sotto(s1331)
    r.verifica()
    if r.prova((k0708, )):
        await r.sotto(s1332)
    r.verifica()
    if r.prova((k0709, )):
        await r.sotto(s1334)


async def s1331(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0906)}, {'entity_id': [c.N('input_select.vmc_master_selected_temp_internal_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_temperatura_interna')})


async def s1332(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Entità Temperatura Interna'}, {'entity_id': [c.N('input_select.vmc_master_selected_temp_internal_entity')]})
    r.verifica()
    if r.prova((k0707, )):
        await r.sotto(s1333)


async def s1333(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna > 2 choose 0 > 1 choose 0 > 1 then
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_temperatura_interna'), 'title': Modello(M.m0721), 'message': "Aggiornare Manualmente l'Entità Temperatura Interna"})


async def s1334(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0910)}, {'entity_id': [c.N('input_text.vmc_master_last_temp_internal_entity')]})


async def s1335(r):
    # script vmc_master_aggiorna_elenco_entita_temperatura_interna > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0910)}, {'entity_id': [c.N('input_text.vmc_master_last_temp_internal_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_temperatura_interna')})


async def s1336(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0913)}, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_external_entity')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0715, )):
        await r.sotto(s1337)
    elif r.prova((k0714, )):
        await r.sotto(s1342)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_external_entity'), c.N('input_text.vmc_master_last_humidity_external_entity')]})


async def s1337(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0711, )):
        await r.sotto(s1338)
    r.verifica()
    if r.prova((k0713, )):
        await r.sotto(s1339)
    r.verifica()
    if r.prova((k0714, )):
        await r.sotto(s1341)


async def s1338(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0914)}, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_external_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_umidita_esterna')})


async def s1339(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Entità Umidità Esterna'}, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_external_entity')]})
    r.verifica()
    if r.prova((k0712, )):
        await r.sotto(s1340)


async def s1340(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna > 2 choose 0 > 1 choose 0 > 1 then
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_umidita_esterna'), 'title': Modello(M.m0721), 'message': "Aggiornare Manualmente l'Entità Umidità Esterna"})


async def s1341(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0918)}, {'entity_id': [c.N('input_text.vmc_master_last_humidity_external_entity')]})


async def s1342(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_esterna > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0918)}, {'entity_id': [c.N('input_text.vmc_master_last_humidity_external_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_umidita_esterna')})


async def s1343(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0921)}, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_internal_entity')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0720, )):
        await r.sotto(s1344)
    elif r.prova((k0719, )):
        await r.sotto(s1349)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_internal_entity'), c.N('input_text.vmc_master_last_humidity_internal_entity')]})


async def s1344(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0716, )):
        await r.sotto(s1345)
    r.verifica()
    if r.prova((k0718, )):
        await r.sotto(s1346)
    r.verifica()
    if r.prova((k0719, )):
        await r.sotto(s1348)


async def s1345(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0922)}, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_internal_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_umidita_interna')})


async def s1346(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Entità Umidità Interna'}, {'entity_id': [c.N('input_select.vmc_master_selected_humidity_internal_entity')]})
    r.verifica()
    if r.prova((k0717, )):
        await r.sotto(s1347)


async def s1347(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna > 2 choose 0 > 1 choose 0 > 1 then
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_umidita_interna'), 'title': Modello(M.m0721), 'message': "Aggiornare Manualmente l'Entità Umidità Interna"})


async def s1348(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0926)}, {'entity_id': [c.N('input_text.vmc_master_last_humidity_internal_entity')]})


async def s1349(r):
    # script vmc_master_aggiorna_elenco_entita_umidita_interna > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0926)}, {'entity_id': [c.N('input_text.vmc_master_last_humidity_internal_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_umidita_interna')})


async def s1350(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0929)}, {'entity_id': [c.N('input_select.vmc_master_selected_co2_internal_entity')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0725, )):
        await r.sotto(s1351)
    elif r.prova((k0724, )):
        await r.sotto(s1356)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_co2_internal_entity'), c.N('input_text.vmc_master_last_co2_internal_entity')]})


async def s1351(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0721, )):
        await r.sotto(s1352)
    r.verifica()
    if r.prova((k0723, )):
        await r.sotto(s1353)
    r.verifica()
    if r.prova((k0724, )):
        await r.sotto(s1355)


async def s1352(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0930)}, {'entity_id': [c.N('input_select.vmc_master_selected_co2_internal_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_co2_interna')})


async def s1353(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Entità CO₂ Interna'}, {'entity_id': [c.N('input_select.vmc_master_selected_co2_internal_entity')]})
    r.verifica()
    if r.prova((k0722, )):
        await r.sotto(s1354)


async def s1354(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna > 2 choose 0 > 1 choose 0 > 1 then
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_co2_interna'), 'title': Modello(M.m0721), 'message': "Aggiornare Manualmente l'Entità CO2 Interna"})


async def s1355(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0934)}, {'entity_id': [c.N('input_text.vmc_master_last_co2_internal_entity')]})


async def s1356(r):
    # script vmc_master_aggiorna_elenco_entita_co2_interna > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0934)}, {'entity_id': [c.N('input_text.vmc_master_last_co2_internal_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_co2_interna')})


async def s1357(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0937)}, {'entity_id': [c.N('input_select.vmc_master_selected_notification_device')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0731, )):
        await r.sotto(s1358)
    elif r.prova((k0730, )):
        await r.sotto(s1365)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_notification_device'), c.N('input_text.vmc_master_last_notification_device')]})


async def s1358(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0726, )):
        await r.sotto(s1359)
    r.verifica()
    if r.prova((k0729, )):
        await r.sotto(s1360)
    r.verifica()
    if r.prova((k0730, )):
        await r.sotto(s1364)


async def s1359(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0938)}, {'entity_id': [c.N('input_select.vmc_master_selected_notification_device')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_dispositivo_notifica')})


async def s1360(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Dispositivi per Invio Notifica'}, {'entity_id': [c.N('input_select.vmc_master_selected_notification_device')]})
    r.verifica()
    if r.prova((k0728, )):
        await r.sotto(s1361)


async def s1361(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0 > 1 choose 0 > 1 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0727, )):
        await r.sotto(s1362)
    else:
        await r.sotto(s1363)


async def s1362(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0 > 1 choose 0 > 1 then > 0 then
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_dispositivo_notifica'), 'title': Modello(M.m0721), 'message': "Aggiornare Manualmente l'Entità Dispositivo di Notifica"})


async def s1363(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0 > 1 choose 0 > 1 then > 0 else
    c, V = r.c, r.V
    await r.servizio('persistent_notification.create', {'notification_id': c.N('vmc_master_aggiorna_entita_dispositivo_notifica'), 'title': Modello(M.m0721), 'message': "Nessun cellulare con l'app Home Assistant: installare l'app sul cellulare, accedere a Home Assistant e poi scegliere il cellulare in Opzioni, «Seleziona Dispositivo per Invio Notifica»"})


async def s1364(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0943)}, {'entity_id': [c.N('input_text.vmc_master_last_notification_device')]})


async def s1365(r):
    # script vmc_master_aggiorna_elenco_entita_notifica_dispositivo > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0943)}, {'entity_id': [c.N('input_text.vmc_master_last_notification_device')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_dispositivo_notifica')})


async def s1366(r):
    # script vmc_master_aggiorna_elenco_entita_media_player
    c, V = r.c, r.V
    await r.servizio('input_select.set_options', {'options': Modello(M.m0946)}, {'entity_id': [c.N('input_select.vmc_master_selected_media_player_entity')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    r.verifica()
    if r.prova((k0735, )):
        await r.sotto(s1367)
    elif r.prova((k0734, )):
        await r.sotto(s1371)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_selected_media_player_entity'), c.N('input_text.vmc_master_last_media_player_entity')]})


async def s1367(r):
    # script vmc_master_aggiorna_elenco_entita_media_player > 2 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0732, )):
        await r.sotto(s1368)
    r.verifica()
    if r.prova((k0733, )):
        await r.sotto(s1369)
    r.verifica()
    if r.prova((k0734, )):
        await r.sotto(s1370)


async def s1368(r):
    # script vmc_master_aggiorna_elenco_entita_media_player > 2 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': Modello(M.m0947)}, {'entity_id': [c.N('input_select.vmc_master_selected_media_player_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_media_player')})


async def s1369(r):
    # script vmc_master_aggiorna_elenco_entita_media_player > 2 choose 0 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_select.select_option', {'option': 'Aggiorna Elenco Media Player'}, {'entity_id': [c.N('input_select.vmc_master_selected_media_player_entity')]})


async def s1370(r):
    # script vmc_master_aggiorna_elenco_entita_media_player > 2 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0950)}, {'entity_id': [c.N('input_text.vmc_master_last_media_player_entity')]})


async def s1371(r):
    # script vmc_master_aggiorna_elenco_entita_media_player > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0950)}, {'entity_id': [c.N('input_text.vmc_master_last_media_player_entity')]})
    await r.servizio('persistent_notification.dismiss', {'notification_id': c.N('vmc_master_aggiorna_entita_media_player')})


async def s1372(r):
    # script vmc_master_notifica_errore_temp_esterna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0736, )):
        await r.sotto(s1373)


async def s1373(r):
    # script vmc_master_notifica_errore_temp_esterna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0955)})


async def s1374(r):
    # script vmc_master_notifica_errore_temp_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0736, )):
        await r.sotto(s1375)


async def s1375(r):
    # script vmc_master_notifica_errore_temp_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0957)})


async def s1376(r):
    # script vmc_master_notifica_errore_umidita_esterna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0736, )):
        await r.sotto(s1377)


async def s1377(r):
    # script vmc_master_notifica_errore_umidita_esterna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0958)})


async def s1378(r):
    # script vmc_master_notifica_errore_umidita_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0736, )):
        await r.sotto(s1379)


async def s1379(r):
    # script vmc_master_notifica_errore_umidita_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0959)})


async def s1380(r):
    # script vmc_master_notifica_errore_co2_interna
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0736, )):
        await r.sotto(s1381)


async def s1381(r):
    # script vmc_master_notifica_errore_co2_interna > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0960)})


async def s1382(r):
    # script vmc_master_notifica_cambio_filtro
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0736, )):
        await r.sotto(s1383)


async def s1383(r):
    # script vmc_master_notifica_cambio_filtro > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0961)})


async def s1384(r):
    # script vmc_master_notifica_velocita_0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0737, )):
        await r.sotto(s1385)


async def s1385(r):
    # script vmc_master_notifica_velocita_0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0962)})


async def s1386(r):
    # script vmc_master_notifica_velocita_diversa_da_0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0738, )):
        await r.sotto(s1387)


async def s1387(r):
    # script vmc_master_notifica_velocita_diversa_da_0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0962)})


async def s1388(r):
    # script vmc_master_notifica_errore_media_player
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0739, )):
        await r.sotto(s1389)


async def s1389(r):
    # script vmc_master_notifica_errore_media_player > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0953), {'title': Modello(M.m0954), 'message': Modello(M.m0965)})


async def s1390(r):
    # script vmc_master_reset_filtro_vmc
    c, V = r.c, r.V
    await r.servizio('timer.start', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_reset_filtro')]})
    await r.servizio(c.N('shell_command.vmc_master_reset_filtro'))
    await r.pausa(timedelta(days=0, seconds=5, microseconds=0))
    await r.servizio('timer.cancel', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_reset_filtro')]})


async def s1391(r):
    # script vmc_master_pulisci_cronologia_audio
    c, V = r.c, r.V
    await r.servizio('tts.clear_cache')
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))


async def s1392(r):
    # script vmc_master_pulisci_cronologia_entita
    c, V = r.c, r.V
    await r.servizio('recorder.purge_entities', {'keep_days': 0, 'entity_id': [c.N('automation.vmc_master_aggiorna_aria_scambiata_e_gestisci_countdown'), c.N('automation.automazione_vmc_master'), c.N('automation.vmc_master_riepilogo_audio_avvio'), c.N('automation.vmc_master_audio_allerte_e_stato'), c.N('automation.vmc_master_riallineamento_allerte_al_riavvio'), c.N('automation.vmc_master_cambio_ip_vmc_riavvio_di_h_a'), c.N('automation.vmc_master_countdown_attese_automazione'), c.N('automation.vmc_master_inizializza_tempi_di_attesa'), c.N('automation.vmc_master_countdown_letture_vmc'), c.N('automation.vmc_master_esclusivita_finestre_opzioni'), c.N('automation.vmc_master_registro_comandi_e_scelte'), c.N('automation.vmc_master_rimando_della_scelta'), c.N('automation.vmc_master_letture_ravvicinate'), c.N('automation.vmc_master_ripartenza_della_vmc'), c.N('input_boolean.vmc_master_opzione_finestra_prossime_letture'), c.N('timer.vmc_master_lettura_ping'), c.N('timer.vmc_master_lettura_ventilazione'), c.N('timer.vmc_master_lettura_ambientali'), c.N('timer.vmc_master_lettura_lan'), c.N('timer.vmc_master_lettura_nome'), c.N('timer.vmc_master_countdown_script_agg_sensori'), c.N('timer.vmc_master_countdown_script_panic_button'), c.N('timer.vmc_master_countdown_script_inizializzazione'), c.N('timer.vmc_master_countdown_script_reset_filtro'), c.N('timer.vmc_master_countdown_avvio_home_assistant'), c.N('timer.vmc_master_countdown_riattivazione_allerte'), c.N('timer.vmc_master_countdown_fase_allerte'), c.N('script.vmc_master_ripristina_tempi_attesa'), c.N('sensor.vmc_master_velocita_registrata'), c.N('binary_sensor.vmc_master_tasto_velocita_0'), c.N('binary_sensor.vmc_master_tasto_velocita_1'), c.N('binary_sensor.vmc_master_tasto_velocita_2'), c.N('binary_sensor.vmc_master_tasto_velocita_3'), c.N('binary_sensor.vmc_master_tasto_velocita_4'), c.N('binary_sensor.vmc_master_tasto_notturna'), c.N('binary_sensor.vmc_master_tasto_iperventilazione'), c.N('binary_sensor.vmc_master_tasto_free_heating'), c.N('binary_sensor.vmc_master_tasto_free_cooling'), c.N('binary_sensor.vmc_master_tasto_free_cool_heat'), c.N('binary_sensor.vmc_master_tasto_sensori_on'), c.N('binary_sensor.vmc_master_tasto_sensori_off'), c.N('binary_sensor.vmc_master_tasto_led_pannello_on'), c.N('binary_sensor.vmc_master_tasto_led_pannello_off'), c.N('binary_sensor.vmc_master_black_out_rilevato'), c.N('input_boolean.vmc_master_attese_inizializzate'), c.N('input_boolean.vmc_master_opzione_finestra_tempi_attesa'), c.N('timer.vmc_master_countdown_pdr_cambio'), c.N('timer.vmc_master_countdown_pdr_ripristino'), c.N('timer.vmc_master_countdown_free_heating_annullamento'), c.N('timer.vmc_master_countdown_free_heating_sospensione'), c.N('timer.vmc_master_countdown_free_heating_ripristino'), c.N('timer.vmc_master_countdown_free_cooling_annullamento'), c.N('timer.vmc_master_countdown_free_cooling_sospensione'), c.N('timer.vmc_master_countdown_free_cooling_ripristino'), c.N('timer.vmc_master_countdown_inquinanti_avvio'), c.N('timer.vmc_master_countdown_inquinanti_fine'), c.N('timer.vmc_master_countdown_inquinanti_memoria'), c.N('timer.vmc_master_countdown_umidita_avvio'), c.N('timer.vmc_master_countdown_umidita_fine'), c.N('timer.vmc_master_countdown_umidita_memoria'), c.N('timer.vmc_master_countdown_delta_avvio'), c.N('timer.vmc_master_countdown_delta_fine'), c.N('timer.vmc_master_countdown_delta_memoria'), c.N('timer.vmc_master_countdown_blackout_rilevazione'), c.N('timer.vmc_master_countdown_blackout_ripristino'), c.N('timer.vmc_master_countdown_calendario_inizio'), c.N('timer.vmc_master_countdown_calendario_fine'), c.N('timer.vmc_master_countdown_avvisi'), c.N('input_text.vmc_master_countdown_pdr_cambio'), c.N('input_text.vmc_master_countdown_pdr_ripristino'), c.N('input_text.vmc_master_countdown_free_heating_annullamento'), c.N('input_text.vmc_master_countdown_free_heating_sospensione'), c.N('input_text.vmc_master_countdown_free_heating_ripristino'), c.N('input_text.vmc_master_countdown_free_cooling_annullamento'), c.N('input_text.vmc_master_countdown_free_cooling_sospensione'), c.N('input_text.vmc_master_countdown_free_cooling_ripristino'), c.N('input_text.vmc_master_countdown_inquinanti_avvio'), c.N('input_text.vmc_master_countdown_inquinanti_fine'), c.N('input_text.vmc_master_countdown_inquinanti_memoria'), c.N('input_text.vmc_master_countdown_umidita_avvio'), c.N('input_text.vmc_master_countdown_umidita_fine'), c.N('input_text.vmc_master_countdown_umidita_memoria'), c.N('input_text.vmc_master_countdown_delta_avvio'), c.N('input_text.vmc_master_countdown_delta_fine'), c.N('input_text.vmc_master_countdown_delta_memoria'), c.N('input_text.vmc_master_countdown_blackout_rilevazione'), c.N('input_text.vmc_master_countdown_blackout_ripristino'), c.N('input_text.vmc_master_countdown_calendario_inizio'), c.N('input_text.vmc_master_countdown_calendario_fine'), c.N('input_text.vmc_master_countdown_avvisi'), c.N('input_text.vmc_master_ultima_scelta_utente'), c.N('input_text.vmc_master_ultimi_comandi_automazione'), c.N('input_text.vmc_master_ultime_letture_velocita'), c.N('input_text.vmc_master_comando_non_eseguito'), c.N('input_number.vmc_master_attesa_pdr_cambio'), c.N('input_number.vmc_master_attesa_pdr_cambio_inquinanti'), c.N('input_number.vmc_master_attesa_pdr_ripristino'), c.N('input_number.vmc_master_attesa_pdr_ripristino_inquinanti'), c.N('input_number.vmc_master_attesa_free_sospensione'), c.N('input_number.vmc_master_attesa_free_sospensione_inquinanti'), c.N('input_number.vmc_master_attesa_free_ripristino'), c.N('input_number.vmc_master_attesa_free_ripristino_inquinanti'), c.N('input_number.vmc_master_attesa_blackout_rilevazione'), c.N('input_number.vmc_master_attesa_blackout_ripristino'), c.N('input_number.vmc_master_attesa_calendario_inizio'), c.N('input_number.vmc_master_attesa_calendario_fine'), c.N('input_number.vmc_master_attesa_avvisi'), c.N('input_number.vmc_master_attesa_inquinanti_avvio'), c.N('input_number.vmc_master_attesa_inquinanti_avvio_spia_pdr'), c.N('input_number.vmc_master_attesa_inquinanti_fine'), c.N('input_number.vmc_master_attesa_inquinanti_memoria'), c.N('input_number.vmc_master_attesa_free_annullamento'), c.N('input_number.vmc_master_attesa_umidita_avvio'), c.N('input_number.vmc_master_attesa_umidita_fine'), c.N('input_number.vmc_master_attesa_umidita_memoria'), c.N('input_number.vmc_master_attesa_delta_avvio'), c.N('input_number.vmc_master_attesa_delta_fine'), c.N('input_number.vmc_master_attesa_delta_memoria'), c.N('sensor.vmc_master_temperatura_esterna_selezionata'), c.N('sensor.vmc_master_temperatura_interna_selezionata'), c.N('sensor.vmc_master_umidita_esterna_selezionata'), c.N('sensor.vmc_master_umidita_interna_selezionata'), c.N('sensor.vmc_master_co2_interna_selezionata'), c.N('sensor.vmc_master_status_ip'), c.N('sensor.vmc_master_status_ventola'), c.N('sensor.vmc_master_sensori'), c.N('sensor.vmc_master_nome'), c.N('sensor.vmc_master_lan'), c.N('sensor.vmc_master_status_ventola_memorizzata'), c.N('sensor.vmc_master_sensori_memorizzata'), c.N('sensor.vmc_master_nome_memorizzata'), c.N('sensor.vmc_master_versione_repository'), c.N('sensor.vmc_master_versione_corrente'), c.N('sensor.vmc_master_verifica_ip_inserito'), c.N('sensor.vmc_master_ip'), c.N('sensor.vmc_master_status_ip_interfaccia'), c.N('sensor.vmc_master_nome_status'), c.N('sensor.vmc_master_status_ventola_lettura_codice'), c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato'), c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia'), c.N('sensor.vmc_master_status_sensori_lettura_codice_interpretato'), c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato'), c.N('sensor.vmc_master_temp_esterna_positivo_negativo'), c.N('sensor.vmc_master_temp_interna_positivo_negativo'), c.N('sensor.vmc_master_temp_esterna_status'), c.N('sensor.vmc_master_temp_esterna_status_senza_offset'), c.N('sensor.vmc_master_temp_interna_status'), c.N('sensor.vmc_master_temp_interna_status_senza_offset'), c.N('sensor.vmc_master_umidita_esterna_status'), c.N('sensor.vmc_master_umidita_interna_status'), c.N('sensor.vmc_master_umidita_interna_status_senza_offset'), c.N('sensor.vmc_master_co2_status'), c.N('sensor.vmc_master_co2_status_senza_offset'), c.N('sensor.vmc_master_voc_status'), c.N('sensor.vmc_master_voc_status_senza_offset'), c.N('sensor.vmc_master_umidita_interna_status_verifica_soglia_valore'), c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto_valore'), c.N('sensor.vmc_master_punto_di_rugiada_valore'), c.N('sensor.vmc_master_umidita_interna_status_verifica_soglia'), c.N('sensor.vmc_master_co2_status_verifica_soglia'), c.N('sensor.vmc_master_voc_status_verifica_soglia'), c.N('sensor.vmc_master_congelamento_verifica_soglia'), c.N('sensor.vmc_master_delta_temp_verifica_soglia'), c.N('sensor.vmc_master_punto_di_rugiada_interno'), c.N('sensor.vmc_master_punto_di_rugiada_esterno'), c.N('sensor.vmc_master_punto_di_rugiada_interno_esterno_non_calcolabile'), c.N('sensor.vmc_master_punto_di_rugiada_verifica_confronto'), c.N('sensor.vmc_master_umidita_assoluta_interna'), c.N('sensor.vmc_master_umidita_assoluta_esterna'), c.N('sensor.vmc_master_temp_esterna_status_grafico'), c.N('sensor.vmc_master_temp_interna_status_grafico'), c.N('sensor.vmc_master_umidita_esterna_status_grafico'), c.N('sensor.vmc_master_umidita_interna_status_grafico'), c.N('sensor.vmc_master_co2_status_grafico'), c.N('sensor.vmc_master_voc_status_grafico'), c.N('sensor.vmc_master_punto_di_rugiada_esterno_grafico'), c.N('sensor.vmc_master_punto_di_rugiada_interno_grafico'), c.N('sensor.vmc_master_punto_di_rugiada_valore_grafico'), c.N('sensor.vmc_master_umidita_assoluta_esterna_grafico'), c.N('sensor.vmc_master_umidita_assoluta_interna_grafico'), c.N('sensor.vmc_master_temp_esterna_status_senza_offset_grafico'), c.N('sensor.vmc_master_temp_interna_status_senza_offset_grafico'), c.N('sensor.vmc_master_umidita_interna_status_senza_offset_grafico'), c.N('sensor.vmc_master_co2_status_senza_offset_grafico'), c.N('sensor.vmc_master_voc_status_senza_offset_grafico'), c.N('sensor.vmc_master_calcolo_confort_interno'), c.N('sensor.vmc_master_status_portata_ventola_lettura_codice_interpretato'), c.N('sensor.vmc_master_status_calcolo_portata_ventola'), c.N('sensor.vmc_master_alert_monitoraggio_umidita'), c.N('sensor.vmc_master_alert_monitoraggio_co2'), c.N('sensor.vmc_master_alert_monitoraggio_voc'), c.N('sensor.vmc_master_alert_monitoraggio_pdr'), c.N('sensor.vmc_master_alert_monitoraggio_congelamento'), c.N('sensor.vmc_master_alert_monitoraggio_delta'), c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling'), c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi'), c.N('sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_disabilitato'), c.N('sensor.vmc_master_alert_monitoraggio_offset_tutti_min'), c.N('sensor.vmc_master_alert_monitoraggio_black_out'), c.N('sensor.vmc_master_alert_monitoraggio_totale'), c.N('sensor.vmc_master_spia_pannello_alert_monitoraggio_totale'), c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_interfaccia'), c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2_interfaccia'), c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_interfaccia'), c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2_interfaccia'), c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario'), c.N('sensor.vmc_master_status_accensione_vmc_tramite_calendario_2'), c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario'), c.N('sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2'), c.N('sensor.vmc_master_status_check_freeheating_freecooling'), c.N('sensor.vmc_master_status_freeheating'), c.N('sensor.vmc_master_status_freecooling'), c.N('sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling'), c.N('sensor.vmc_master_speed_1_fascia_calendario'), c.N('sensor.vmc_master_speed_2_fascia_calendario'), c.N('sensor.vmc_master_mese_1_fascia_freeheating'), c.N('sensor.vmc_master_mese_2_fascia_freeheating'), c.N('sensor.vmc_master_mese_1_fascia_freecooling'), c.N('sensor.vmc_master_mese_2_fascia_freecooling'), c.N('sensor.vmc_master_status_calcolo_aria_scambiata_totale'), c.N('sensor.vmc_master_cicli_ricambio_aria'), c.N('sensor.vmc_master_tempo_mancante_ricambio'), c.N('sensor.vmc_master_temp_interna_numeric'), c.N('sensor.vmc_master_hum_interna_numeric'), c.N('sensor.vmc_master_calcolo_rischio_muffa_4w'), c.N('sensor.vmc_master_calcolo_rischio_muffa_8w'), c.N('sensor.vmc_master_calcolo_rischio_muffa_12w'), c.N('sensor.vmc_master_temp_interna_media_4w'), c.N('sensor.vmc_master_temp_interna_media_8w'), c.N('sensor.vmc_master_temp_interna_media_12w'), c.N('sensor.vmc_master_hum_interna_media_4w'), c.N('sensor.vmc_master_hum_interna_media_8w'), c.N('sensor.vmc_master_hum_interna_media_12w'), c.N('sensor.vmc_master_rischio_muffa_giorni_dati'), c.N('sensor.vmc_master_stato_led_interfaccia'), c.N('sensor.vmc_master_alert_avvio_interfaccia'), c.N('sensor.vmc_master_trend_muffa'), c.N('sensor.vmc_master_trend_muffa_level'), c.N('sensor.vmc_master_trend_muffa_level_numeric'), c.N('input_text.vmc_master_nome_da_inserire'), c.N('input_text.vmc_master_ip_insert'), c.N('input_text.vmc_master_ip_insert_esito'), c.N('input_text.vmc_master_last_temp_external_entity'), c.N('input_text.vmc_master_last_temp_internal_entity'), c.N('input_text.vmc_master_last_humidity_external_entity'), c.N('input_text.vmc_master_last_humidity_internal_entity'), c.N('input_text.vmc_master_last_co2_internal_entity'), c.N('input_text.vmc_master_last_notification_device'), c.N('input_text.vmc_master_tempo_mancante_reset'), c.N('input_text.vmc_master_velocita_precedente'), c.N('input_text.vmc_master_last_media_player_entity'), c.N('input_select.vmc_master_speed_1_fascia_calendario'), c.N('input_select.vmc_master_speed_2_fascia_calendario'), c.N('input_select.vmc_master_mese_1_fascia_freeheating'), c.N('input_select.vmc_master_mese_2_fascia_freeheating'), c.N('input_select.vmc_master_mese_1_fascia_freecooling'), c.N('input_select.vmc_master_mese_2_fascia_freecooling'), c.N('input_select.vmc_master_selected_temp_external_entity'), c.N('input_select.vmc_master_selected_temp_internal_entity'), c.N('input_select.vmc_master_selected_humidity_external_entity'), c.N('input_select.vmc_master_selected_humidity_internal_entity'), c.N('input_select.vmc_master_selected_co2_internal_entity'), c.N('input_select.vmc_master_selected_notification_device'), c.N('input_select.vmc_master_speed_umidita'), c.N('input_select.vmc_master_selected_media_player_entity'), c.N('input_number.vmc_master_offset_temp_interna'), c.N('input_number.vmc_master_offset_temp_esterna'), c.N('input_number.vmc_master_offset_umidita_interna'), c.N('input_number.vmc_master_offset_umidita_esterna'), c.N('input_number.vmc_master_offset_co2'), c.N('input_number.vmc_master_offset_voc'), c.N('input_number.vmc_master_offset_verifica_impiego_vmc'), c.N('input_number.vmc_master_volume_da_inserire'), c.N('input_number.vmc_master_umidita_avvio'), c.N('input_number.vmc_master_fase_riallineamento_al_riavvio'), c.N('input_number.vmc_master_aria_scambiata_v1'), c.N('input_number.vmc_master_aria_scambiata_v2'), c.N('input_number.vmc_master_aria_scambiata_v3'), c.N('input_number.vmc_master_aria_scambiata_v4'), c.N('input_number.vmc_master_aria_scambiata_iperventilazione'), c.N('input_number.vmc_master_aria_scambiata_notte'), c.N('input_number.vmc_master_aria_scambiata_freecooling'), c.N('input_number.vmc_master_aria_scambiata_ricomincio'), c.N('input_number.vmc_master_audio_volume'), c.N('input_datetime.vmc_master_accensione_lunedi'), c.N('input_datetime.vmc_master_spegnimento_lunedi'), c.N('input_datetime.vmc_master_accensione_lunedi_2'), c.N('input_datetime.vmc_master_spegnimento_lunedi_2'), c.N('input_datetime.vmc_master_accensione_martedi'), c.N('input_datetime.vmc_master_spegnimento_martedi'), c.N('input_datetime.vmc_master_accensione_martedi_2'), c.N('input_datetime.vmc_master_spegnimento_martedi_2'), c.N('input_datetime.vmc_master_accensione_mercoledi'), c.N('input_datetime.vmc_master_spegnimento_mercoledi'), c.N('input_datetime.vmc_master_accensione_mercoledi_2'), c.N('input_datetime.vmc_master_spegnimento_mercoledi_2'), c.N('input_datetime.vmc_master_accensione_giovedi'), c.N('input_datetime.vmc_master_spegnimento_giovedi'), c.N('input_datetime.vmc_master_accensione_giovedi_2'), c.N('input_datetime.vmc_master_spegnimento_giovedi_2'), c.N('input_datetime.vmc_master_accensione_venerdi'), c.N('input_datetime.vmc_master_spegnimento_venerdi'), c.N('input_datetime.vmc_master_accensione_venerdi_2'), c.N('input_datetime.vmc_master_spegnimento_venerdi_2'), c.N('input_datetime.vmc_master_accensione_sabato'), c.N('input_datetime.vmc_master_spegnimento_sabato'), c.N('input_datetime.vmc_master_accensione_sabato_2'), c.N('input_datetime.vmc_master_spegnimento_sabato_2'), c.N('input_datetime.vmc_master_accensione_domenica'), c.N('input_datetime.vmc_master_spegnimento_domenica'), c.N('input_datetime.vmc_master_accensione_domenica_2'), c.N('input_datetime.vmc_master_spegnimento_domenica_2'), c.N('input_datetime.vmc_master_audio_start_time'), c.N('input_datetime.vmc_master_audio_end_time'), c.N('input_boolean.vmc_master_opzioni_avvisi'), c.N('input_boolean.vmc_master_opzioni_avvisi_grafici'), c.N('input_boolean.vmc_master_opzioni_vmc'), c.N('input_boolean.vmc_master_opzioni_offset_sensori'), c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori'), c.N('input_boolean.vmc_master_opzioni_monitoraggio_sensori'), c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('input_boolean.vmc_master_opzioni_calendario_main'), c.N('input_boolean.vmc_master_opzioni_calendario'), c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada'), c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('input_boolean.vmc_master_opzioni_interruttore_calendario'), c.N('input_boolean.vmc_master_opzioni_lettura_sensori'), c.N('input_boolean.vmc_master_opzioni_scelta_sensori'), c.N('input_boolean.vmc_master_opzioni_elementi_chimici'), c.N('input_boolean.vmc_master_opzione_finestra_audio'), c.N('input_boolean.vmc_master_conferma_pulizia_cronologia'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_avvisi'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_avvisi_spia'), c.N('input_boolean.vmc_master_popup_versione_corrente_vs_repository'), c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling'), c.N('input_boolean.vmc_master_spia_calendario_lunedi_1'), c.N('input_boolean.vmc_master_spia_calendario_lunedi_2'), c.N('input_boolean.vmc_master_spia_calendario_martedi_1'), c.N('input_boolean.vmc_master_spia_calendario_martedi_2'), c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1'), c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2'), c.N('input_boolean.vmc_master_spia_calendario_giovedi_1'), c.N('input_boolean.vmc_master_spia_calendario_giovedi_2'), c.N('input_boolean.vmc_master_spia_calendario_venerdi_1'), c.N('input_boolean.vmc_master_spia_calendario_venerdi_2'), c.N('input_boolean.vmc_master_spia_calendario_sabato_1'), c.N('input_boolean.vmc_master_spia_calendario_sabato_2'), c.N('input_boolean.vmc_master_spia_calendario_domenica_1'), c.N('input_boolean.vmc_master_spia_calendario_domenica_2'), c.N('input_boolean.vmc_master_spia_calendario_black_out'), c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento'), c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_notifica_status_vmc'), c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling'), c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio'), c.N('input_boolean.vmc_master_notifica_audio'), c.N('input_boolean.vmc_master_notifica_allerta_congelamento'), c.N('input_boolean.vmc_master_notifica_allerta_differenza_temp_int_est'), c.N('input_boolean.vmc_master_notifica_allerta_inquinanti'), c.N('input_boolean.vmc_master_notifica_allerta_pdr'), c.N('input_boolean.vmc_master_notifica_allerta_freecooling_heating'), c.N('input_boolean.vmc_master_notifica_allerta_umidita'), c.N('input_boolean.vmc_master_notifica_allerta_black_out'), c.N('input_boolean.vmc_master_notifica_allerta_status_velocita'), c.N('input_boolean.vmc_master_notifica_allerta_riepilogo'), c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_esterna'), c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_umidita_esterna'), c.N('script.vmc_master_aggiorna_elenco_entita_umidita_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_co2_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo'), c.N('script.vmc_master_aggiorna_elenco_entita_media_player'), c.N('script.vmc_master_notifica_errore_temp_esterna'), c.N('script.vmc_master_notifica_errore_temp_interna'), c.N('script.vmc_master_notifica_errore_umidita_esterna'), c.N('script.vmc_master_notifica_errore_umidita_interna'), c.N('script.vmc_master_notifica_errore_co2_interna'), c.N('script.vmc_master_notifica_cambio_filtro'), c.N('script.vmc_master_notifica_velocita_0'), c.N('script.vmc_master_notifica_velocita_diversa_da_0'), c.N('script.vmc_master_notifica_errore_media_player'), c.N('script.vmc_master_azzera_booleans'), c.N('script.vmc_master_azzera_offset_sensors'), c.N('script.vmc_master_upgrade_sensors'), c.N('script.vmc_master_profilo_calendario'), c.N('script.vmc_master_profilo_free_heating_cooling'), c.N('script.vmc_master_profilo_pdr'), c.N('script.vmc_master_profilo_umidita'), c.N('script.vmc_master_reset_filtro_vmc'), c.N('script.vmc_master_profilo_inizializzazione'), c.N('script.vmc_master_audio_profilo'), c.N('script.vmc_master_bottone_panico'), c.N('script.vmc_master_calendario_fascia_1_o_2_off'), c.N('script.vmc_master_calendario_fascia_1_on'), c.N('script.vmc_master_calendario_fascia_2_on'), c.N('script.vmc_master_azzera_aria_scambiata'), c.N('script.vmc_master_pulisci_cronologia_audio'), c.N('script.vmc_master_audio_status_velocita'), c.N('script.vmc_master_audio_allerta_umidita_interna'), c.N('script.vmc_master_audio_nessuna_allerta_umidita_interna'), c.N('script.vmc_master_audio_allerta_co2'), c.N('script.vmc_master_audio_nessuna_allerta_co2'), c.N('script.vmc_master_audio_allerta_voc'), c.N('script.vmc_master_audio_nessuna_allerta_voc'), c.N('script.vmc_master_audio_allerta_pdr'), c.N('script.vmc_master_audio_nessuna_allerta_pdr'), c.N('script.vmc_master_audio_allerta_black_out'), c.N('script.vmc_master_audio_nessuna_allerta_black_out'), c.N('script.vmc_master_audio_free_heating_o_free_cooling'), c.N('script.vmc_master_audio_allerta_congelamento'), c.N('script.vmc_master_audio_nessuna_allerta_congelamento'), c.N('script.vmc_master_audio_allerta_diff_temp'), c.N('script.vmc_master_audio_nessuna_allerta_diff_temp'), c.N('script.vmc_master_azzera_aria_scambiata_puntuale')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_conferma_pulizia_cronologia')]})


async def s1393(r):
    # script vmc_master_azzera_booleans
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0740, )):
        await r.sotto(s1394)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_avvisi_spia'), c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling'), c.N('input_boolean.vmc_master_spia_calendario_lunedi_1'), c.N('input_boolean.vmc_master_spia_calendario_lunedi_2'), c.N('input_boolean.vmc_master_spia_calendario_martedi_1'), c.N('input_boolean.vmc_master_spia_calendario_martedi_2'), c.N('input_boolean.vmc_master_spia_calendario_mercoledi_1'), c.N('input_boolean.vmc_master_spia_calendario_mercoledi_2'), c.N('input_boolean.vmc_master_spia_calendario_giovedi_1'), c.N('input_boolean.vmc_master_spia_calendario_giovedi_2'), c.N('input_boolean.vmc_master_spia_calendario_venerdi_1'), c.N('input_boolean.vmc_master_spia_calendario_venerdi_2'), c.N('input_boolean.vmc_master_spia_calendario_sabato_1'), c.N('input_boolean.vmc_master_spia_calendario_sabato_2'), c.N('input_boolean.vmc_master_spia_calendario_domenica_1'), c.N('input_boolean.vmc_master_spia_calendario_domenica_2'), c.N('input_boolean.vmc_master_spia_calendario_black_out'), c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento'), c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_3_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_4_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_notturna_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_delta_temp_verifica_soglia_valore'), c.N('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_umidita_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0'), c.N('input_boolean.vmc_master_spia_umidita_velocita_1'), c.N('input_boolean.vmc_master_spia_umidita_velocita_2'), c.N('input_boolean.vmc_master_spia_umidita_velocita_3'), c.N('input_boolean.vmc_master_spia_umidita_velocita_4'), c.N('input_boolean.vmc_master_spia_umidita_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_umidita_velocita_notturna'), c.N('input_boolean.vmc_master_spia_umidita_velocita_freecooling'), c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio')]})


async def s1394(r):
    # script vmc_master_azzera_booleans > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_avvisi'), c.N('input_boolean.vmc_master_opzioni_avvisi_grafici'), c.N('input_boolean.vmc_master_opzioni_vmc'), c.N('input_boolean.vmc_master_opzioni_offset_sensori'), c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori'), c.N('input_boolean.vmc_master_opzioni_monitoraggio_sensori'), c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('input_boolean.vmc_master_opzione_finestra_prossime_letture'), c.N('input_boolean.vmc_master_opzioni_calendario_main'), c.N('input_boolean.vmc_master_opzioni_calendario'), c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada'), c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('input_boolean.vmc_master_opzioni_interruttore_calendario'), c.N('input_boolean.vmc_master_opzioni_lettura_sensori'), c.N('input_boolean.vmc_master_opzioni_scelta_sensori'), c.N('input_boolean.vmc_master_opzioni_elementi_chimici'), c.N('input_boolean.vmc_master_opzione_finestra_audio')]})


async def s1395(r):
    # script vmc_master_azzera_offset_sensors
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': [c.N('input_number.vmc_master_offset_temp_esterna'), c.N('input_number.vmc_master_offset_temp_interna'), c.N('input_number.vmc_master_offset_umidita_esterna'), c.N('input_number.vmc_master_offset_umidita_interna'), c.N('input_number.vmc_master_offset_co2'), c.N('input_number.vmc_master_offset_voc')], 'value': 0})


async def s1396(r):
    # script vmc_master_audio_profilo
    c, V = r.c, r.V
    await r.servizio('input_datetime.set_datetime', {'time': '08:00'}, {'entity_id': [c.N('input_datetime.vmc_master_audio_start_time')]})
    await r.servizio('input_datetime.set_datetime', {'time': '21:00'}, {'entity_id': [c.N('input_datetime.vmc_master_audio_end_time')]})
    await r.servizio('input_number.set_value', {'entity_id': [c.N('input_number.vmc_master_audio_volume')], 'value': 0.3})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_notifica_audio'), c.N('input_boolean.vmc_master_notifica_allerta_congelamento'), c.N('input_boolean.vmc_master_notifica_allerta_differenza_temp_int_est'), c.N('input_boolean.vmc_master_notifica_allerta_inquinanti'), c.N('input_boolean.vmc_master_notifica_allerta_pdr'), c.N('input_boolean.vmc_master_notifica_allerta_freecooling_heating'), c.N('input_boolean.vmc_master_notifica_allerta_umidita'), c.N('input_boolean.vmc_master_notifica_allerta_black_out'), c.N('input_boolean.vmc_master_notifica_allerta_status_velocita'), c.N('input_boolean.vmc_master_notifica_allerta_riepilogo')]})


async def s1397(r):
    # script vmc_master_azzera_aria_scambiata_puntuale
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'entity_id': c.N('input_text.vmc_master_tempo_mancante_reset'), 'value': ''})


async def s1398(r):
    # script vmc_master_azzera_aria_scambiata
    c, V = r.c, r.V
    await r.servizio('recorder.purge_entities', {'keep_days': 0, 'entity_id': [c.N('sensor.vmc_master_status_calcolo_aria_scambiata_totale'), c.N('sensor.vmc_master_cicli_ricambio_aria'), c.N('sensor.vmc_master_tempo_mancante_ricambio'), c.N('input_number.vmc_master_aria_scambiata_v1'), c.N('input_number.vmc_master_aria_scambiata_v2'), c.N('input_number.vmc_master_aria_scambiata_v3'), c.N('input_number.vmc_master_aria_scambiata_v4'), c.N('input_number.vmc_master_aria_scambiata_iperventilazione'), c.N('input_number.vmc_master_aria_scambiata_notte'), c.N('input_number.vmc_master_aria_scambiata_freecooling'), c.N('input_number.vmc_master_aria_scambiata_ricomincio')]})
    await r.servizio('input_number.set_value', {'entity_id': [c.N('input_number.vmc_master_aria_scambiata_v1'), c.N('input_number.vmc_master_aria_scambiata_v2'), c.N('input_number.vmc_master_aria_scambiata_v3'), c.N('input_number.vmc_master_aria_scambiata_v4'), c.N('input_number.vmc_master_aria_scambiata_iperventilazione'), c.N('input_number.vmc_master_aria_scambiata_notte'), c.N('input_number.vmc_master_aria_scambiata_freecooling'), c.N('input_number.vmc_master_aria_scambiata_ricomincio')], 'value': 0})
    await r.servizio('input_text.set_value', {'entity_id': c.N('input_text.vmc_master_tempo_mancante_reset'), 'value': 'reset'})


async def s1399(r):
    # script vmc_master_upgrade_sensors
    c, V = r.c, r.V
    await r.servizio('timer.start', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_agg_sensori')]})
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ip')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola'), c.N('sensor.vmc_master_status_sensori_lettura_codice_interpretato'), c.N('sensor.vmc_master_status_led_pannello_lettura_codice_interpretato'), c.N('sensor.vmc_master_status_calcolo_portata_ventola'), c.N('sensor.vmc_master_status_portata_ventola_lettura_codice_interpretato'), c.N('sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_sensori')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_nome'), c.N('sensor.vmc_master_nome_status')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_lan')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_versione_repository')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_co2_status')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_voc_status')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_esterna'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_interna'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_umidita_esterna'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_umidita_interna'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_co2_interna'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio(c.N('script.vmc_master_aggiorna_elenco_entita_media_player'), {})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_esterna')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_interna')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_umidita_esterna')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_umidita_interna')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_co2_interna')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_media_player')]})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_spia_pannello_alert_monitoraggio_totale'), c.N('sensor.vmc_master_temperatura_esterna_selezionata'), c.N('sensor.vmc_master_temperatura_interna_selezionata'), c.N('sensor.vmc_master_umidita_esterna_selezionata'), c.N('sensor.vmc_master_umidita_interna_selezionata'), c.N('sensor.vmc_master_co2_interna_selezionata'), c.N('input_select.vmc_master_selected_temp_external_entity'), c.N('input_select.vmc_master_selected_temp_internal_entity'), c.N('input_select.vmc_master_selected_humidity_external_entity'), c.N('input_select.vmc_master_selected_humidity_internal_entity'), c.N('input_select.vmc_master_selected_co2_internal_entity'), c.N('input_select.vmc_master_selected_notification_device'), c.N('input_select.vmc_master_selected_media_player_entity'), c.N('input_text.vmc_master_last_temp_external_entity'), c.N('input_text.vmc_master_last_temp_internal_entity'), c.N('input_text.vmc_master_last_humidity_external_entity'), c.N('input_text.vmc_master_last_humidity_internal_entity'), c.N('input_text.vmc_master_last_co2_internal_entity'), c.N('input_text.vmc_master_last_notification_device'), c.N('input_text.vmc_master_last_media_player_entity')]})
    await r.servizio('timer.cancel', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_agg_sensori')]})


async def s1400(r):
    # script vmc_master_profilo_calendario
    c, V = r.c, r.V
    await r.servizio('input_datetime.set_datetime', {'time': '00:30'}, {'entity_id': [c.N('input_datetime.vmc_master_accensione_lunedi'), c.N('input_datetime.vmc_master_accensione_martedi'), c.N('input_datetime.vmc_master_accensione_mercoledi'), c.N('input_datetime.vmc_master_accensione_giovedi'), c.N('input_datetime.vmc_master_accensione_venerdi'), c.N('input_datetime.vmc_master_accensione_sabato'), c.N('input_datetime.vmc_master_accensione_domenica')]})
    await r.servizio('input_datetime.set_datetime', {'time': '06:00'}, {'entity_id': [c.N('input_datetime.vmc_master_spegnimento_lunedi'), c.N('input_datetime.vmc_master_spegnimento_martedi'), c.N('input_datetime.vmc_master_spegnimento_mercoledi'), c.N('input_datetime.vmc_master_spegnimento_giovedi'), c.N('input_datetime.vmc_master_spegnimento_venerdi'), c.N('input_datetime.vmc_master_spegnimento_sabato'), c.N('input_datetime.vmc_master_spegnimento_domenica')]})
    await r.servizio('input_datetime.set_datetime', {'time': '20:00'}, {'entity_id': [c.N('input_datetime.vmc_master_accensione_lunedi_2'), c.N('input_datetime.vmc_master_accensione_martedi_2'), c.N('input_datetime.vmc_master_accensione_mercoledi_2'), c.N('input_datetime.vmc_master_accensione_giovedi_2'), c.N('input_datetime.vmc_master_accensione_venerdi_2'), c.N('input_datetime.vmc_master_accensione_sabato_2'), c.N('input_datetime.vmc_master_accensione_domenica_2')]})
    await r.servizio('input_datetime.set_datetime', {'time': '23:30'}, {'entity_id': [c.N('input_datetime.vmc_master_spegnimento_lunedi_2'), c.N('input_datetime.vmc_master_spegnimento_martedi_2'), c.N('input_datetime.vmc_master_spegnimento_mercoledi_2'), c.N('input_datetime.vmc_master_spegnimento_giovedi_2'), c.N('input_datetime.vmc_master_spegnimento_venerdi_2'), c.N('input_datetime.vmc_master_spegnimento_sabato_2'), c.N('input_datetime.vmc_master_spegnimento_domenica_2')]})
    await r.servizio('input_select.select_option', {'option': 'Velocità 1'}, {'entity_id': [c.N('input_select.vmc_master_speed_1_fascia_calendario')]})
    await r.servizio('input_select.select_option', {'option': 'Velocità 1'}, {'entity_id': [c.N('input_select.vmc_master_speed_2_fascia_calendario')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')]})


async def s1401(r):
    # script vmc_master_profilo_free_heating_cooling
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling')]})
    await r.servizio('input_select.select_option', {'entity_id': c.N('input_select.vmc_master_mese_1_fascia_freeheating'), 'option': 'Ottobre'})
    await r.servizio('input_select.select_option', {'entity_id': c.N('input_select.vmc_master_mese_2_fascia_freeheating'), 'option': 'Giugno'})
    await r.servizio('input_select.select_option', {'entity_id': c.N('input_select.vmc_master_mese_1_fascia_freecooling'), 'option': 'Luglio'})
    await r.servizio('input_select.select_option', {'entity_id': c.N('input_select.vmc_master_mese_2_fascia_freecooling'), 'option': 'Settembre'})
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('input_select.vmc_master_mese_1_fascia_freeheating'), c.N('input_select.vmc_master_mese_2_fascia_freeheating'), c.N('input_select.vmc_master_mese_1_fascia_freecooling'), c.N('input_select.vmc_master_mese_2_fascia_freecooling')]})


async def s1402(r):
    # script vmc_master_profilo_pdr
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': [c.N('input_number.vmc_master_offset_verifica_impiego_vmc')], 'value': 0})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')]})


async def s1403(r):
    # script vmc_master_profilo_umidita
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': [c.N('input_number.vmc_master_umidita_avvio')], 'value': 75})
    await r.servizio('input_select.select_option', {'option': 'Iperventilazione'}, {'entity_id': [c.N('input_select.vmc_master_speed_umidita')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')]})


async def s1404(r):
    # script vmc_master_profilo_inizializzazione
    c, V = r.c, r.V
    await r.servizio('timer.start', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_inizializzazione')]})
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')]})
    await r.servizio(c.N('script.vmc_master_azzera_booleans'), {})
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_offset_sensori')]})
    await r.servizio(c.N('script.vmc_master_azzera_offset_sensors'), {})
    await r.servizio(c.N('script.vmc_master_profilo_calendario'), {})
    await r.servizio(c.N('script.vmc_master_profilo_free_heating_cooling'), {})
    await r.servizio(c.N('script.vmc_master_profilo_pdr'), {})
    await r.servizio(c.N('script.vmc_master_profilo_umidita'), {})
    await r.servizio(c.N('script.vmc_master_audio_profilo'), {})
    await r.servizio(c.N('script.vmc_master_ripristina_tempi_attesa'), {})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'))
    await r.pausa(timedelta(days=0, seconds=5, microseconds=0))
    await r.servizio(c.N('shell_command.vmc_master_sensori_off'))
    await r.pausa(timedelta(days=0, seconds=5, microseconds=0))
    await r.servizio(c.N('shell_command.vmc_master_pannello_led_on'))
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_avvisi'), c.N('input_boolean.vmc_master_notifica_status_vmc'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc')]})
    await r.servizio('timer.cancel', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_inizializzazione')]})


async def s1405(r):
    # script vmc_master_bottone_panico
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'))
    await r.servizio('timer.start', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_panic_button')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_avvisi'), c.N('input_boolean.vmc_master_notifica_status_vmc'), c.N('input_boolean.vmc_master_notifica_audio'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freeheating'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_freecooling'), c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc'), c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio')]})
    await r.attendi(M.m0968, timeout=timedelta(days=0, seconds=60, microseconds=0))
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'))
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]})
    r.variabili({'delta_in_corso': Modello(M.m0969), 'congelamento_in_corso': Modello(M.m0970)})
    await r.servizio(c.N('script.vmc_master_azzera_booleans'), {})
    r.verifica()
    if r.prova((k0741, )):
        await r.sotto(s1406)
    r.verifica()
    if r.prova((k0742, )):
        await r.sotto(s1407)
    await r.attendi(M.m0973, timeout=timedelta(days=0, seconds=10, microseconds=0))
    r.verifica()
    if r.prova((k0743, )):
        await r.sotto(s1408)
    await r.servizio('timer.cancel', None, {'entity_id': [c.N('timer.vmc_master_countdown_script_panic_button')]})


async def s1406(r):
    # script vmc_master_bottone_panico > 9 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_delta_temp_verifica_soglia_valore')]})


async def s1407(r):
    # script vmc_master_bottone_panico > 10 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento')]})


async def s1408(r):
    # script vmc_master_bottone_panico > 12 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})


async def s1409(r):
    # script vmc_master_calendario_fascia_1_o_2_off
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_azzera_booleans'), {'mantieni_pannelli': True})


async def s1410(r):
    # script vmc_master_calendario_fascia_1_on
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]}, alias='La Fascia prevale sul ripristino di un Black-Out rilevato prima della Fascia (memoria del Black-Out spenta) [Foglio Logiche A23 e A25]')
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')]}, alias='Ogni avvio della Fascia decide di nuovo se il comando viene eseguito (Spia Comando non eseguito del Calendario OFF)')
    await r.pausa(timedelta(days=0, seconds=5, microseconds=0))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    if not r.passo_condizione(k0744, 'Ritorno della VMC dopo un comando non eseguito: la Fascia riparte solo se la velocità della VMC non è cambiata nel frattempo (una velocità scelta, per esempio con il telecomando, si rispetta); controllo fatto dopo i 5 s, con le letture già aggiornate'):
        return
    r.verifica()
    if r.prova((k0761, )):
        await r.sotto(s1411)
    elif r.prova((k0763, )):
        await r.sotto(s1448)
    elif r.prova((k0766, )):
        await r.sotto(s1485)
    elif r.prova((k0769, )):
        await r.sotto(s1522)
    elif r.prova((k0772, )):
        await r.sotto(s1559)
    elif r.prova((k0775, )):
        await r.sotto(s1596)
    elif r.prova((k0778, )):
        await r.sotto(s1633)
    elif r.prova((k0792, )):
        await r.sotto(s1670)
    r.verifica()
    if r.prova((k0793, )):
        await r.sotto(s1830)


async def s1411(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1412)
    elif r.prova((k0755, )):
        await r.sotto(s1421)
    elif r.prova((k0757, )):
        await r.sotto(s1430)
    elif r.prova((k0758, )):
        await r.sotto(s1439)


async def s1412(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1413)
    elif r.prova((k0748, )):
        await r.sotto(s1415)
    elif r.prova((k0749, )):
        await r.sotto(s1417)
    elif r.prova((k0750, )):
        await r.sotto(s1419)


async def s1413(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1414, (k0745, ))


async def s1414(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1415(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1416, (k0747, ))


async def s1416(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1417(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1418, (k0745, ))


async def s1418(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1419(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1420, (k0747, ))


async def s1420(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1421(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1422)
    elif r.prova((k0748, )):
        await r.sotto(s1424)
    elif r.prova((k0749, )):
        await r.sotto(s1426)
    elif r.prova((k0750, )):
        await r.sotto(s1428)


async def s1422(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1423, (k0747, ))


async def s1423(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1424(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1425, (k0747, ))


async def s1425(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1426(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1427, (k0747, ))


async def s1427(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1428(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1429, (k0747, ))


async def s1429(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1430(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1431)
    elif r.prova((k0748, )):
        await r.sotto(s1433)
    elif r.prova((k0749, )):
        await r.sotto(s1435)
    elif r.prova((k0750, )):
        await r.sotto(s1437)


async def s1431(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1432, (k0745, ))


async def s1432(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1433(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1434, (k0747, ))


async def s1434(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1435(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1436, (k0745, ))


async def s1436(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1437(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1438, (k0747, ))


async def s1438(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1439(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1440)
    elif r.prova((k0748, )):
        await r.sotto(s1442)
    elif r.prova((k0749, )):
        await r.sotto(s1444)
    elif r.prova((k0750, )):
        await r.sotto(s1446)


async def s1440(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1441, (k0747, ))


async def s1441(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1442(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1443, (k0747, ))


async def s1443(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1444(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1445, (k0747, ))


async def s1445(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1446(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1447, (k0747, ))


async def s1447(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 0 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1448(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1449)
    elif r.prova((k0755, )):
        await r.sotto(s1458)
    elif r.prova((k0757, )):
        await r.sotto(s1467)
    elif r.prova((k0758, )):
        await r.sotto(s1476)


async def s1449(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1450)
    elif r.prova((k0748, )):
        await r.sotto(s1452)
    elif r.prova((k0749, )):
        await r.sotto(s1454)
    elif r.prova((k0750, )):
        await r.sotto(s1456)


async def s1450(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1451, (k0745, ))


async def s1451(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1452(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1453, (k0747, ))


async def s1453(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1454(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1455, (k0745, ))


async def s1455(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1456(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1457, (k0745, ))


async def s1457(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1458(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1459)
    elif r.prova((k0748, )):
        await r.sotto(s1461)
    elif r.prova((k0749, )):
        await r.sotto(s1463)
    elif r.prova((k0750, )):
        await r.sotto(s1465)


async def s1459(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1460, (k0747, ))


async def s1460(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1461(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1462, (k0747, ))


async def s1462(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1463(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1464, (k0745, ))


async def s1464(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1465(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1466, (k0745, ))


async def s1466(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1467(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1468)
    elif r.prova((k0748, )):
        await r.sotto(s1470)
    elif r.prova((k0749, )):
        await r.sotto(s1472)
    elif r.prova((k0750, )):
        await r.sotto(s1474)


async def s1468(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1469, (k0745, ))


async def s1469(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1470(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1471, (k0745, ))


async def s1471(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1472(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1473, (k0745, ))


async def s1473(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1474(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1475, (k0745, ))


async def s1475(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1476(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1477)
    elif r.prova((k0748, )):
        await r.sotto(s1479)
    elif r.prova((k0749, )):
        await r.sotto(s1481)
    elif r.prova((k0750, )):
        await r.sotto(s1483)


async def s1477(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1478, (k0745, ))


async def s1478(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1479(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1480, (k0745, ))


async def s1480(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1481(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1482, (k0745, ))


async def s1482(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1483(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1484, (k0745, ))


async def s1484(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 1 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1485(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1486)
    elif r.prova((k0755, )):
        await r.sotto(s1495)
    elif r.prova((k0757, )):
        await r.sotto(s1504)
    elif r.prova((k0758, )):
        await r.sotto(s1513)


async def s1486(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1487)
    elif r.prova((k0748, )):
        await r.sotto(s1489)
    elif r.prova((k0749, )):
        await r.sotto(s1491)
    elif r.prova((k0750, )):
        await r.sotto(s1493)


async def s1487(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1488, (k0764, ))


async def s1488(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1489(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1490, (k0747, ))


async def s1490(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1491(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1492, (k0764, ))


async def s1492(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1493(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1494, (k0764, ))


async def s1494(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1495(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1496)
    elif r.prova((k0748, )):
        await r.sotto(s1498)
    elif r.prova((k0749, )):
        await r.sotto(s1500)
    elif r.prova((k0750, )):
        await r.sotto(s1502)


async def s1496(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1497, (k0747, ))


async def s1497(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1498(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1499, (k0747, ))


async def s1499(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1500(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1501, (k0764, ))


async def s1501(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1502(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1503, (k0764, ))


async def s1503(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1504(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1505)
    elif r.prova((k0748, )):
        await r.sotto(s1507)
    elif r.prova((k0749, )):
        await r.sotto(s1509)
    elif r.prova((k0750, )):
        await r.sotto(s1511)


async def s1505(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1506, (k0764, ))


async def s1506(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1507(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1508, (k0764, ))


async def s1508(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1509(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1510, (k0764, ))


async def s1510(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1511(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1512, (k0764, ))


async def s1512(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1513(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1514)
    elif r.prova((k0748, )):
        await r.sotto(s1516)
    elif r.prova((k0749, )):
        await r.sotto(s1518)
    elif r.prova((k0750, )):
        await r.sotto(s1520)


async def s1514(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1515, (k0764, ))


async def s1515(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1516(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1517, (k0764, ))


async def s1517(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1518(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1519, (k0764, ))


async def s1519(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1520(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1521, (k0764, ))


async def s1521(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 2 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1522(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1523)
    elif r.prova((k0755, )):
        await r.sotto(s1532)
    elif r.prova((k0757, )):
        await r.sotto(s1541)
    elif r.prova((k0758, )):
        await r.sotto(s1550)


async def s1523(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1524)
    elif r.prova((k0748, )):
        await r.sotto(s1526)
    elif r.prova((k0749, )):
        await r.sotto(s1528)
    elif r.prova((k0750, )):
        await r.sotto(s1530)


async def s1524(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1525, (k0767, ))


async def s1525(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1526(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1527, (k0747, ))


async def s1527(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1528(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1529, (k0767, ))


async def s1529(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1530(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1531, (k0767, ))


async def s1531(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1532(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1533)
    elif r.prova((k0748, )):
        await r.sotto(s1535)
    elif r.prova((k0749, )):
        await r.sotto(s1537)
    elif r.prova((k0750, )):
        await r.sotto(s1539)


async def s1533(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1534, (k0747, ))


async def s1534(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1535(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1536, (k0747, ))


async def s1536(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1537(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1538, (k0767, ))


async def s1538(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1539(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1540, (k0767, ))


async def s1540(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1541(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1542)
    elif r.prova((k0748, )):
        await r.sotto(s1544)
    elif r.prova((k0749, )):
        await r.sotto(s1546)
    elif r.prova((k0750, )):
        await r.sotto(s1548)


async def s1542(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1543, (k0767, ))


async def s1543(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1544(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1545, (k0767, ))


async def s1545(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1546(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1547, (k0767, ))


async def s1547(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1548(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1549, (k0767, ))


async def s1549(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1550(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1551)
    elif r.prova((k0748, )):
        await r.sotto(s1553)
    elif r.prova((k0749, )):
        await r.sotto(s1555)
    elif r.prova((k0750, )):
        await r.sotto(s1557)


async def s1551(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1552, (k0767, ))


async def s1552(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1553(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1554, (k0767, ))


async def s1554(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1555(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1556, (k0767, ))


async def s1556(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1557(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1558, (k0767, ))


async def s1558(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 3 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1559(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1560)
    elif r.prova((k0755, )):
        await r.sotto(s1569)
    elif r.prova((k0757, )):
        await r.sotto(s1578)
    elif r.prova((k0758, )):
        await r.sotto(s1587)


async def s1560(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1561)
    elif r.prova((k0748, )):
        await r.sotto(s1563)
    elif r.prova((k0749, )):
        await r.sotto(s1565)
    elif r.prova((k0750, )):
        await r.sotto(s1567)


async def s1561(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1562, (k0770, ))


async def s1562(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1563(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1564, (k0747, ))


async def s1564(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1565(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1566, (k0770, ))


async def s1566(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1567(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1568, (k0770, ))


async def s1568(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1569(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1570)
    elif r.prova((k0748, )):
        await r.sotto(s1572)
    elif r.prova((k0749, )):
        await r.sotto(s1574)
    elif r.prova((k0750, )):
        await r.sotto(s1576)


async def s1570(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1571, (k0747, ))


async def s1571(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1572(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1573, (k0747, ))


async def s1573(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1574(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1575, (k0770, ))


async def s1575(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1576(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1577, (k0770, ))


async def s1577(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1578(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1579)
    elif r.prova((k0748, )):
        await r.sotto(s1581)
    elif r.prova((k0749, )):
        await r.sotto(s1583)
    elif r.prova((k0750, )):
        await r.sotto(s1585)


async def s1579(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1580, (k0770, ))


async def s1580(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1581(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1582, (k0770, ))


async def s1582(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1583(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1584, (k0770, ))


async def s1584(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1585(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1586, (k0770, ))


async def s1586(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1587(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1588)
    elif r.prova((k0748, )):
        await r.sotto(s1590)
    elif r.prova((k0749, )):
        await r.sotto(s1592)
    elif r.prova((k0750, )):
        await r.sotto(s1594)


async def s1588(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1589, (k0770, ))


async def s1589(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1590(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1591, (k0770, ))


async def s1591(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1592(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1593, (k0770, ))


async def s1593(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1594(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1595, (k0770, ))


async def s1595(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 4 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1596(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1597)
    elif r.prova((k0755, )):
        await r.sotto(s1606)
    elif r.prova((k0757, )):
        await r.sotto(s1615)
    elif r.prova((k0758, )):
        await r.sotto(s1624)


async def s1597(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1598)
    elif r.prova((k0748, )):
        await r.sotto(s1600)
    elif r.prova((k0749, )):
        await r.sotto(s1602)
    elif r.prova((k0750, )):
        await r.sotto(s1604)


async def s1598(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1599, (k0773, ))


async def s1599(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1600(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1601, (k0747, ))


async def s1601(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1602(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1603, (k0773, ))


async def s1603(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1604(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1605, (k0773, ))


async def s1605(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1606(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1607)
    elif r.prova((k0748, )):
        await r.sotto(s1609)
    elif r.prova((k0749, )):
        await r.sotto(s1611)
    elif r.prova((k0750, )):
        await r.sotto(s1613)


async def s1607(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1608, (k0747, ))


async def s1608(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1609(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1610, (k0747, ))


async def s1610(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1611(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1612, (k0773, ))


async def s1612(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1613(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1614, (k0773, ))


async def s1614(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 1 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1615(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1616)
    elif r.prova((k0748, )):
        await r.sotto(s1618)
    elif r.prova((k0749, )):
        await r.sotto(s1620)
    elif r.prova((k0750, )):
        await r.sotto(s1622)


async def s1616(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1617, (k0773, ))


async def s1617(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1618(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1619, (k0773, ))


async def s1619(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1620(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1621, (k0773, ))


async def s1621(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1622(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1623, (k0773, ))


async def s1623(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 2 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1624(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1625)
    elif r.prova((k0748, )):
        await r.sotto(s1627)
    elif r.prova((k0749, )):
        await r.sotto(s1629)
    elif r.prova((k0750, )):
        await r.sotto(s1631)


async def s1625(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1626, (k0773, ))


async def s1626(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1627(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1628, (k0773, ))


async def s1628(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1629(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1630, (k0773, ))


async def s1630(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1631(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1632, (k0773, ))


async def s1632(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 5 > 1 choose 3 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1633(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    if r.prova((k0753, )):
        await r.sotto(s1634)
    elif r.prova((k0755, )):
        await r.sotto(s1643)
    elif r.prova((k0757, )):
        await r.sotto(s1652)
    elif r.prova((k0758, )):
        await r.sotto(s1661)


async def s1634(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1635)
    elif r.prova((k0748, )):
        await r.sotto(s1637)
    elif r.prova((k0749, )):
        await r.sotto(s1639)
    elif r.prova((k0750, )):
        await r.sotto(s1641)


async def s1635(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1636, (k0776, ))


async def s1636(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1637(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1638, (k0747, ))


async def s1638(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1639(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    r.verifica()
    await r.ripeti_finche(s1640, (k0776, ))


async def s1640(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1641(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1642, (k0776, ))


async def s1642(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 0 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1643(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0746, )):
        await r.sotto(s1644)
    elif r.prova((k0748, )):
        await r.sotto(s1646)
    elif r.prova((k0749, )):
        await r.sotto(s1648)
    elif r.prova((k0750, )):
        await r.sotto(s1650)


async def s1644(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1645, (k0747, ))


async def s1645(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1646(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    await r.ripeti_finche(s1647, (k0747, ))


async def s1647(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s1648(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s1649, (k0776, ))


async def s1649(r):
    # script vmc_master_calendario_fascia_1_on > 5 choose 6 > 1 choose 1 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))
