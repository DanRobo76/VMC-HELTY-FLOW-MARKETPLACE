"""Automazioni e script del package, tradotti in Python (parte 2 di 8).

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
    k0001, k0002, k0003, k0004, k0005, k0006, k0007, k0008, k0009, k0010,
    k0011, k0012, k0013, k0014, k0015, k0016, k0017, k0018, k0019, k0020,
    k0021, k0022, k0023, k0024, k0025, k0031, k0032, k0033, k0034, k0035,
    k0036, k0037, k0038, k0039, k0040, k0041, k0042, k0043, k0044, k0045,
    k0046, k0047, k0048, k0050, k0051, k0052, k0053, k0055, k0056, k0057,
    k0058, k0059, k0060, k0061, k0062, k0063, k0064, k0066, k0068, k0069,
    k0074, k0075, k0076, k0077, k0078, k0080, k0081, k0082, k0083, k0084,
    k0085, k0086, k0087, k0088, k0089, k0090, k0091, k0092, k0093, k0094,
    k0095, k0096, k0097, k0098, k0099, k0100, k0101, k0102, k0103, k0104,
    k0105, k0106, k0107, k0108, k0109, k0110, k0111, k0112, k0113, k0114,
    k0115, k0116, k0117, k0118, k0119, k0120, k0121, k0122, k0123, k0124,
    k0125, k0126, k0127, k0128, k0129, k0130, k0131, k0132, k0133, k0134,
    k0135, k0136, k0137, k0138, k0139, k0140, k0141, k0142, k0143, k0144,
    k0145, k0146, k0147, k0148, k0149, k0150, k0151, k0152, k0153, k0154,
    k0155, k0156, k0157, k0158, k0159, k0160, k0161, k0162, k0163, k0164,
    k0165, k0166, k0167, k0168, k0169, k0170, k0171, k0172, k0173, k0174,
    k0175, k0176, k0177, k0178, k0179, k0180, k0181, k0182, k0183, k0184,
    k0185, k0186, k0187, k0188, k0189, k0190, k0191, k0192, k0193, k0194,
    k0195, k0196, k0197, k0198, k0199, k0200, k0201, k0202, k0203, k0204,
    k0205, k0206, k0207, k0208, k0209, k0210, k0211, k0212, k0213, k0214,
    k0215, k0216, k0217, k0218, k0219, k0220, k0221, k0222, k0223, k0224,
    k0225, k0226, k0227, k0228, k0229, k0230, k0231, k0232, k0233, k0234,
    k0235, k0236, k0237, k0238, k0239, k0240, k0241, k0242, k0243, k0248,
    k0249, k0250, k0253, k0255, k0256, k0258, k0260, k0266, k0267, k0269,
    k0270, k0271, k0275, k0279, k0281, k0282, k0283, k0286, k0287, k0290,
    k0314, k0315, k0316, k0318, k0319, k0320, k0321, k0322, k0323, k0324,
    k0325, k0326, k0327, k0328, k0329, k0330, k0336, k0337, k0342, k0344,
    k0345, k0347, k0353, k0357, k0358, k0361, k0362, k0363, k0364, k0366,
    k0367, k0368, k0369, k0371, k0372, k0373, k0374, k0376, k0377, k0378,
    k0379, k0381, k0382, k0383, k0384, k0386, k0387, k0388, k0389, k0391,
    k0392, k0393, k0394, k0395, k0396, k0397, k0398, k0399, k0423, k0441,
    k0465, k0473, k0475, k0477, k0479, k0481, k0483, k0486, k0526, k0545,
    k0548, k0549, k0550, k0553, k0556, k0557, k0558, k0559, k0560, k0561,
    k0562, k0563, k0564, k0565, k0566, k0567, k0568, k0569, k0570, k0571,
    k0572, k0573, k0574, k0575, k0576, k0577, k0578, k0579, k0580, k0581,
    k0582, k0583, k0584, k0585, k0586, k0589, k0590, k0591, k0592, k0593,
    k0594, k0595, k0596, k0597, k0616, k0618, k0644, k0648, k0652, k0653,
    k0654, k0655, k0656, k0657, k0659, k0688, k0700,
)
from .motore_03 import (
    s0359, s0360, s0361, s0362, s0363, s0364, s0365, s0372, s0376, s0383,
    s0387, s0393, s0399, s0405, s0411, s0420, s0429, s0438, s0447, s0454,
    s0460, s0466, s0469, s0477, s0478, s0481, s0506, s0507, s0508, s0511,
    s0516, s0517, s0522, s0523, s0528, s0529, s0534, s0535, s0540, s0541,
    s0546, s0547, s0564, s0565, s0570, s0575, s0586, s0590, s0591, s0596,
    s0597, s0602, s0603, s0608, s0609, s0614, s0615, s0620, s0621, s0626,
    s0627, s0632, s0633, s0638, s0639, s0644, s0645, s0650, s0651, s0656,
    s0657, s0662, s0663, s0668, s0669, s0674, s0675, s0676, s0677, s0678,
    s0679,
)
from .motore_04 import (
    s0740, s0807, s0889, s0898, s0900, s0902, s0904, s0906, s0908, s0924,
)
from .motore_05 import (
    s1002, s1061, s1064, s1068, s1072, s1081, s1090, s1091, s1092, s1093,
    s1094, s1095, s1096, s1097, s1098, s1099, s1100, s1101, s1102, s1103,
    s1104, s1105, s1106, s1107, s1108, s1109, s1110, s1111, s1112, s1113,
    s1114, s1115, s1116, s1117, s1118, s1119, s1120, s1121, s1158, s1161,
    s1197, s1202, s1208, s1212, s1216, s1220, s1224, s1228, s1232, s1268,
)


async def s0001(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown
    c, V = r.c, r.V
    r.variabili({'velocita_corrente': Modello(M.m0001), 'velocita_precedente': Modello(M.m0002)})
    r.verifica()
    if r.prova((k0001, )):
        await r.sotto(s0002)
    r.verifica()
    if r.prova((k0002, )):
        await r.sotto(s0003)
    elif r.prova((k0003, )):
        await r.sotto(s0004)
    elif r.prova((k0006, k0007, )):
        await r.sotto(s0005)


async def s0002(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': c.N('input_number.vmc_master_aria_scambiata_ricomincio'), 'value': 0})
    await r.servizio('input_text.set_value', {'entity_id': c.N('input_text.vmc_master_velocita_precedente'), 'value': Modello(M.m0003)})
    await r.servizio('input_text.set_value', {'entity_id': c.N('input_text.vmc_master_tempo_mancante_reset'), 'value': 'reset'})


async def s0003(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 2 choose 0
    c, V = r.c, r.V
    await r.servizio('script.turn_on', None, {'entity_id': [c.N('script.vmc_master_azzera_aria_scambiata')]})


async def s0004(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 2 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_azzera_aria_scambiata_puntuale'), {})


async def s0005(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 2 choose 2
    c, V = r.c, r.V
    r.variabili({'portate': {'Velocità 1': 10, 'Velocità 2': 17, 'Velocità 3': 26, 'Velocità 4': 37, 'Iperventilazione': 42, 'Notturna': 10, 'Free Cooling': 26}, 'incremento': Modello(M.m0006), 'totale_entity': Modello(M.m0007), 'ricomincio_entity': c.N('input_number.vmc_master_aria_scambiata_ricomincio'), 'tempo_mancante': Modello(M.m0008), 'volume': Modello(M.m0009), 'ricomincio_val': Modello(M.m0010), 'nuovo_valore': Modello(M.m0011)})
    r.verifica()
    if r.prova((k0004, )):
        await r.sotto(s0006)
    elif r.prova((k0005, )):
        await r.sotto(s0007)
    elif r.prova(()):
        await r.sotto(s0008)


async def s0006(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 2 choose 2 > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': Modello(M.m0012), 'value': 0})


async def s0007(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 2 choose 2 > 1 choose 1
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': Modello(M.m0014), 'value': Modello(M.m0015)})
    await r.servizio('input_number.set_value', {'entity_id': Modello(M.m0012), 'value': 0})


async def s0008(r):
    # automazione VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown > 2 choose 2 > 1 choose 2
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'entity_id': Modello(M.m0014), 'value': Modello(M.m0015)})
    await r.servizio('input_number.set_value', {'entity_id': Modello(M.m0012), 'value': Modello(M.m0017)})


async def s0009(r):
    # automazione VMC Master - Riepilogo Audio Avvio
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0008, )):
        await r.sotto(s0010)
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio')]})
    await r.pausa(timedelta(days=0, seconds=10, microseconds=0))
    r.verifica()
    if r.prova((k0009, )):
        await r.sotto(s0011)
    elif r.prova((k0010, )):
        await r.sotto(s0012)
    await r.servizio(c.N('script.vmc_master_audio_status_velocita'))
    r.verifica()
    if r.prova((k0011, )):
        await r.sotto(s0013)
    elif r.prova((k0012, )):
        await r.sotto(s0014)
    elif r.prova((k0013, )):
        await r.sotto(s0015)
    r.verifica()
    if r.prova((k0014, )):
        await r.sotto(s0016)
    elif r.prova((k0015, )):
        await r.sotto(s0017)
    elif r.prova((k0016, )):
        await r.sotto(s0018)
    r.verifica()
    if r.prova((k0017, )):
        await r.sotto(s0019)
    elif r.prova((k0018, )):
        await r.sotto(s0020)
    r.verifica()
    if r.prova((k0019, )):
        await r.sotto(s0021)
    elif r.prova((k0020, )):
        await r.sotto(s0022)
    r.verifica()
    if r.prova((k0021, )):
        await r.sotto(s0023)
    elif r.prova((k0022, )):
        await r.sotto(s0024)
    r.verifica()
    if r.prova((k0023, )):
        await r.sotto(s0025)
    r.verifica()
    if r.prova((k0024, )):
        await r.sotto(s0026)
    elif r.prova((k0025, )):
        await r.sotto(s0027)
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio')]})


async def s0010(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': [c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio')]})
    r.verifica()
    raise Ferma("Spia dell'audio all'avvio spenta")


async def s0011(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 3 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_black_out'))


async def s0012(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 3 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_black_out'))


async def s0013(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 5 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_congelamento'))


async def s0014(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 5 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_congelamento'))


async def s0015(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 5 choose 2
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_congelamento'))


async def s0016(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 6 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_diff_temp'))


async def s0017(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 6 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_diff_temp'))


async def s0018(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 6 choose 2
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_diff_temp'))


async def s0019(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 7 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_co2'))


async def s0020(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 7 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_co2'))


async def s0021(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 8 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_voc'))


async def s0022(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 8 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_voc'))


async def s0023(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 9 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_pdr'))


async def s0024(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 9 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_pdr'))


async def s0025(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 10 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_free_heating_o_free_cooling'))


async def s0026(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 11 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_umidita_interna'))


async def s0027(r):
    # automazione VMC Master - Riepilogo Audio Avvio > 11 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_umidita_interna'))


async def s0028(r):
    # automazione VMC Master - Audio Allerte e Stato
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0031, )):
        await r.sotto(s0029)
    elif r.prova((k0032, )):
        await r.sotto(s0030)
    elif r.prova((k0033, )):
        await r.sotto(s0031)
    elif r.prova((k0034, )):
        await r.sotto(s0032)
    elif r.prova((k0035, )):
        await r.sotto(s0033)
    elif r.prova((k0036, )):
        await r.sotto(s0034)
    elif r.prova((k0037, )):
        await r.sotto(s0035)
    elif r.prova((k0038, )):
        await r.sotto(s0036)
    elif r.prova((k0039, )):
        await r.sotto(s0037)
    elif r.prova((k0040, )):
        await r.sotto(s0038)
    elif r.prova((k0041, )):
        await r.sotto(s0039)
    elif r.prova((k0042, )):
        await r.sotto(s0040)
    elif r.prova((k0043, )):
        await r.sotto(s0041)
    elif r.prova((k0044, )):
        await r.sotto(s0042)
    elif r.prova((k0045, )):
        await r.sotto(s0043)
    elif r.prova((k0046, )):
        await r.sotto(s0044)
    elif r.prova((k0047, )):
        await r.sotto(s0045)
    elif r.prova((k0048, )):
        await r.sotto(s0046)


async def s0029(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 0
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_status_velocita'))


async def s0030(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 1
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_umidita_interna'))


async def s0031(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 2
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_umidita_interna'))


async def s0032(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 3
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_co2'))


async def s0033(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 4
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_co2'))


async def s0034(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 5
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_voc'))


async def s0035(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 6
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_voc'))


async def s0036(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 7
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_pdr'))


async def s0037(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 8
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_pdr'))


async def s0038(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 9
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_black_out'))


async def s0039(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 10
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_black_out'))


async def s0040(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 11
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_free_heating_o_free_cooling'))


async def s0041(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 12
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_congelamento'))


async def s0042(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 13
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_congelamento'))


async def s0043(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 14
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_congelamento'))


async def s0044(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 15
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_diff_temp'))


async def s0045(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 16
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_allerta_diff_temp'))


async def s0046(r):
    # automazione VMC Master - Audio Allerte e Stato > 0 choose 17
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_audio_nessuna_allerta_diff_temp'))


async def s0047(r):
    # automazione VMC Master - Riallineamento Allerte al Riavvio
    c, V = r.c, r.V
    await r.servizio('input_number.set_value', {'value': 1}, {'entity_id': [c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')]})
    await r.servizio('timer.start', None, {'entity_id': [c.N('timer.vmc_master_countdown_avvio_home_assistant')]})
    await r.servizio('timer.start', None, {'entity_id': [c.N('timer.vmc_master_countdown_riattivazione_allerte')]})
    await r.servizio('timer.cancel', None, {'entity_id': [c.N('timer.vmc_master_countdown_fase_allerte')]})
    await r.pausa(timedelta(days=0, seconds=60, microseconds=0))
    await r.servizio('timer.start', {'duration': '00:00:40'}, {'entity_id': [c.N('timer.vmc_master_countdown_fase_allerte')]})
    await r.servizio('input_number.set_value', {'value': 2}, {'entity_id': [c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')]})
    await r.pausa(timedelta(days=0, seconds=40, microseconds=0))
    await r.servizio('timer.start', {'duration': '00:00:40'}, {'entity_id': [c.N('timer.vmc_master_countdown_fase_allerte')]})
    await r.servizio('input_number.set_value', {'value': 3}, {'entity_id': [c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')]})
    await r.pausa(timedelta(days=0, seconds=40, microseconds=0))
    await r.servizio('input_number.set_value', {'value': 4}, {'entity_id': [c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')]})
    await r.pausa(timedelta(days=0, seconds=60, microseconds=0))
    await r.servizio('input_number.set_value', {'value': 0}, {'entity_id': [c.N('input_number.vmc_master_fase_riallineamento_al_riavvio')]})


async def s0048(r):
    # automazione VMC Master - Cambio IP VMC (Riavvio di H.A.)
    c, V = r.c, r.V
    r.variabili({'ip': Modello(M.m0056), 'ip_valido': Modello(M.m0057), 'ip_libero': Modello(M.m0058)})
    r.verifica()
    if r.prova((k0051, )):
        await r.sotto(s0049)


async def s0049(r):
    # automazione VMC Master - Cambio IP VMC (Riavvio di H.A.) > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0059)}, {'entity_id': [c.N('input_text.vmc_master_ip_insert_esito')]})
    await r.servizio(c.N('vmc_master.verifica_ip'), {'ip': Modello(M.m0060), 'nome': Modello(M.m0061)}, None, risposta='verifica')
    await r.servizio('input_text.set_value', {'value': Modello(M.m0062)}, {'entity_id': [c.N('input_text.vmc_master_ip_insert_esito')]})
    if not r.passo_condizione(k0050, 'template'):
        return
    await r.servizio(c.N('shell_command.vmc_master_rimuovi_caratteri_di_ritorno'))
    await r.servizio(c.N('shell_command.vmc_master_aggiorna_indirizzo_ip'), {'ip': Modello(M.m0060)})
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.restart')


async def s0050(r):
    # automazione VMC Master - Countdown Attese Automazione
    c, V = r.c, r.V
    r.variabili({'parti': Modello(M.m0065), 'secondi': Modello(M.m0066), 'testo': Modello(M.m0067), 'famiglia': Modello(M.m0068), 'famiglie_off': Modello(M.m0069)})
    r.verifica()
    if r.prova((k0052, )):
        await r.sotto(s0051)
    else:
        await r.sotto(s0052)


async def s0051(r):
    # automazione VMC Master - Countdown Attese Automazione > 1 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0070)}, {'entity_id': Modello(M.m0071)})
    await r.servizio('timer.start', {'duration': Modello(M.m0072)}, {'entity_id': Modello(M.m0073)})


async def s0052(r):
    # automazione VMC Master - Countdown Attese Automazione > 1 else
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_per_ogni(s0053, Modello(M.m0078))


async def s0053(r):
    # automazione VMC Master - Countdown Attese Automazione > 1 else > 0 repeat
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0053, )):
        await r.sotto(s0054)


async def s0054(r):
    # automazione VMC Master - Countdown Attese Automazione > 1 else > 0 repeat > 0 then
    c, V = r.c, r.V
    await r.servizio('timer.cancel', None, {'entity_id': Modello(M.m0075)})
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': Modello(M.m0076)})


async def s0055(r):
    # automazione VMC Master - Countdown Letture VMC
    c, V = r.c, r.V
    r.variabili({'chiavi': Modello(M.m0344)})
    r.verifica()
    await r.ripeti_per_ogni(s0056, Modello(M.m0354))


async def s0056(r):
    # automazione VMC Master - Countdown Letture VMC > 1 repeat
    c, V = r.c, r.V
    r.variabili({'intervallo': Modello(M.m0345), 'timer_lettura': Modello(M.m0346), 'ultima': Modello(M.m0347), 'trascorsi': Modello(M.m0348), 'mancano': Modello(M.m0349), 'scarto': Modello(M.m0350), 'secondi': Modello(M.m0351)})
    r.verifica()
    if r.prova((k0055, )):
        await r.sotto(s0057)


async def s0057(r):
    # automazione VMC Master - Countdown Letture VMC > 1 repeat > 1 then
    c, V = r.c, r.V
    await r.servizio('timer.start', {'duration': Modello(M.m0072)}, {'entity_id': Modello(M.m0352)})


async def s0058(r):
    # automazione VMC Master - Registro Comandi e Scelte
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0056, )):
        await r.sotto(s0059)
    r.verifica()
    if r.prova((k0057, )):
        await r.sotto(s0060)
    elif r.prova((k0058, )):
        await r.sotto(s0061)
    elif r.prova((k0059, )):
        await r.sotto(s0062)


async def s0059(r):
    # automazione VMC Master - Registro Comandi e Scelte > 0 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0356)}, {'entity_id': [c.N('input_text.vmc_master_ultime_letture_velocita')]})


async def s0060(r):
    # automazione VMC Master - Registro Comandi e Scelte > 1 choose 0
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0358)}, {'entity_id': [c.N('input_text.vmc_master_ultima_scelta_utente')]})


async def s0061(r):
    # automazione VMC Master - Registro Comandi e Scelte > 1 choose 1
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0360)}, {'entity_id': [c.N('input_text.vmc_master_ultimi_comandi_automazione')]})


async def s0062(r):
    # automazione VMC Master - Registro Comandi e Scelte > 1 choose 2
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0362)}, {'entity_id': [c.N('input_text.vmc_master_ultima_scelta_utente')]})


async def s0063(r):
    # automazione VMC Master - Rimando della Scelta
    c, V = r.c, r.V
    if not r.passo_condizione(k0060, "Nessun comando dell'automazione con un'altra velocità in viaggio al momento della scelta -> niente da rimandare"):
        return
    r.verifica()
    await r.ripeti_finche(s0064, (k0061, ))
    if not r.passo_condizione(k0062, "Comando in viaggio arrivato e nessuna velocità nuova mandata dall'automazione dopo la scelta"):
        return
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, continua_se_errore=True, alias='Rilettura della velocità')
    await r.attendi(M.m0372, timeout=timedelta(days=0, seconds=2, microseconds=0))
    if not r.passo_condizione(k0063, 'La VMC è tornata alla velocità del comando in viaggio (la scelta è stata cancellata), è ON-Line e senza Black-Out'):
        return
    r.variabili({'inizio': Modello(M.m0365)})
    r.verifica()
    await r.ripeti_finche(s0065, (k0064, ))


async def s0064(r):
    # automazione VMC Master - Rimando della Scelta > 1 repeat
    c, V = r.c, r.V
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))


async def s0065(r):
    # automazione VMC Master - Rimando della Scelta > 7 repeat
    c, V = r.c, r.V
    await r.servizio(Modello(M.m0374))
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, continua_se_errore=True)
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0066(r):
    # automazione VMC Master - Letture Ravvicinate
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_mentre(s0067, (k0066, ))


async def s0067(r):
    # automazione VMC Master - Letture Ravvicinate > 0 repeat
    c, V = r.c, r.V
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, continua_se_errore=True)


async def s0068(r):
    # automazione VMC Master - Ripartenza della VMC
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0068, )):
        await r.sotto(s0069)
    elif r.prova((k0069, )):
        await r.sotto(s0070)


async def s0069(r):
    # automazione VMC Master - Ripartenza della VMC > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': [c.N('input_boolean.vmc_master_spia_calendario_black_out')]})


async def s0070(r):
    # automazione VMC Master - Ripartenza della VMC > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', None, {'entity_id': Modello(M.m0385)})


async def s0071(r):
    # automazione VMC Master - Esclusività Finestre Opzioni
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0074, k0075, )):
        await r.sotto(s0072)
    elif r.prova((k0076, k0075, )):
        await r.sotto(s0073)
    elif r.prova((k0077, k0075, )):
        await r.sotto(s0074)
    elif r.prova((k0078, k0075, )):
        await r.sotto(s0075)


async def s0072(r):
    # automazione VMC Master - Esclusività Finestre Opzioni > 0 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': Modello(M.m0395)}, alias="Chiude solo le finestre aperte prima di questo evento [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0073(r):
    # automazione VMC Master - Esclusività Finestre Opzioni > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': Modello(M.m0397)}, alias="Chiude solo le finestre aperte prima di questo evento [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0074(r):
    # automazione VMC Master - Esclusività Finestre Opzioni > 0 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': Modello(M.m0398)}, alias="Chiude solo le finestre aperte prima di questo evento [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0075(r):
    # automazione VMC Master - Esclusività Finestre Opzioni > 0 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', None, {'entity_id': Modello(M.m0399)}, alias="Chiude solo le finestre aperte prima di questo evento [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0076(r):
    # automazione VMC Master - Inizializza Tempi di Attesa
    c, V = r.c, r.V
    await r.servizio(c.N('script.vmc_master_ripristina_tempi_attesa'))


async def s0077(r):
    # automazione Automazione VMC Master
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0081, )):
        await r.sotto(s0078)
    if not r.passo_condizione(k0082, "Evento ancora valido [MODALITA' QUEUED: GLI EVENTI SI ESEGUONO UNO ALLA VOLTA, IN ORDINE; UN TRIGGER TEMPLATE SI ESEGUE SOLO SE LA SUA CONDIZIONE E' ANCORA VERA QUANDO ARRIVA IL SUO TURNO, COME SE FOSSE APPENA SCATTATO] [OGNI CONDIZIONE E' LA COPIA 1:1 DEL value_template DEL TRIGGER CON LO STESSO id: SE SI MODIFICA UN TRIGGER VA MODIFICATA ANCHE LA SUA COPIA QUI]"):
        return
    r.verifica()
    if r.prova((k0083, k0084, )):
        await r.sotto(s0080)
    elif r.prova((k0085, k0086, )):
        await r.sotto(s0081)
    elif r.prova((k0087, k0088, )):
        await r.sotto(s0082)
    elif r.prova((k0089, k0090, )):
        await r.sotto(s0083)
    elif r.prova((k0091, k0092, )):
        await r.sotto(s0084)
    elif r.prova((k0093, k0094, )):
        await r.sotto(s0085)
    elif r.prova((k0095, k0096, )):
        await r.sotto(s0086)
    elif r.prova((k0097, k0098, )):
        await r.sotto(s0087)
    elif r.prova((k0099, k0100, )):
        await r.sotto(s0088)
    elif r.prova((k0101, k0102, )):
        await r.sotto(s0089)
    elif r.prova((k0103, k0104, )):
        await r.sotto(s0090)
    elif r.prova((k0105, k0106, )):
        await r.sotto(s0091)
    elif r.prova((k0107, k0108, )):
        await r.sotto(s0092)
    elif r.prova((k0109, k0110, )):
        await r.sotto(s0093)
    elif r.prova((k0111, k0112, )):
        await r.sotto(s0094)
    elif r.prova((k0113, k0114, )):
        await r.sotto(s0095)
    elif r.prova((k0115, k0116, )):
        await r.sotto(s0096)
    elif r.prova((k0117, k0118, )):
        await r.sotto(s0097)
    elif r.prova((k0119, k0120, )):
        await r.sotto(s0098)
    elif r.prova((k0121, k0122, )):
        await r.sotto(s0099)
    elif r.prova((k0123, k0124, )):
        await r.sotto(s0100)
    elif r.prova((k0125, k0126, )):
        await r.sotto(s0101)
    elif r.prova((k0127, k0128, )):
        await r.sotto(s0102)
    elif r.prova((k0129, k0130, )):
        await r.sotto(s0103)
    elif r.prova((k0131, k0132, )):
        await r.sotto(s0104)
    elif r.prova((k0133, k0134, )):
        await r.sotto(s0105)
    elif r.prova((k0139, )):
        await r.sotto(s0106)
    elif r.prova((k0141, )):
        await r.sotto(s0116)
    elif r.prova((k0143, )):
        await r.sotto(s0122)
    elif r.prova((k0145, )):
        await r.sotto(s0128)
    elif r.prova((k0147, )):
        await r.sotto(s0134)
    elif r.prova((k0148, )):
        await r.sotto(s0140)
    elif r.prova((k0150, )):
        await r.sotto(s0145)
    elif r.prova((k0157, )):
        await r.sotto(s0151)
    elif r.prova((k0160, )):
        await r.sotto(s0165)
    elif r.prova((k0163, )):
        await r.sotto(s0170)
    elif r.prova((k0166, )):
        await r.sotto(s0175)
    elif r.prova((k0169, )):
        await r.sotto(s0180)
    elif r.prova((k0177, )):
        await r.sotto(s0185)
    elif r.prova((k0180, )):
        await r.sotto(s0206)
    elif r.prova((k0181, )):
        await r.sotto(s0211)
    elif r.prova((k0184, )):
        await r.sotto(s0212)
    elif r.prova((k0186, )):
        await r.sotto(s0218)
    elif r.prova((k0188, )):
        await r.sotto(s0223)
    elif r.prova((k0191, )):
        await r.sotto(s0229)
    elif r.prova((k0195, )):
        await r.sotto(s0236)
    elif r.prova((k0198, )):
        await r.sotto(s0244)
    elif r.prova((k0201, )):
        await r.sotto(s0252)
    elif r.prova((k0204, )):
        await r.sotto(s0260)
    elif r.prova((k0212, )):
        await r.sotto(s0268)
    elif r.prova((k0215, )):
        await r.sotto(s0279)
    elif r.prova((k0217, )):
        await r.sotto(s0287)
    elif r.prova((k0219, )):
        await r.sotto(s0289)
    elif r.prova((k0221, )):
        await r.sotto(s0296)
    elif r.prova((k0223, )):
        await r.sotto(s0303)
    elif r.prova((k0225, )):
        await r.sotto(s0310)
    elif r.prova((k0233, )):
        await r.sotto(s0317)
    elif r.prova((k0235, )):
        await r.sotto(s0343)
    elif r.prova((k0238, k0239, )):
        await r.sotto(s0350)
    elif r.prova((k0238, k0240, k0241, )):
        await r.sotto(s0357)
    elif r.prova((k0242, k0243, )):
        await r.sotto(s0364)
    elif r.prova((k0248, )):
        await r.sotto(s0365)
    elif r.prova((k0249, )):
        await r.sotto(s0372)
    elif r.prova((k0250, )):
        await r.sotto(s0376)
    elif r.prova((k0253, )):
        await r.sotto(s0383)
    elif r.prova((k0255, )):
        await r.sotto(s0387)
    elif r.prova((k0256, )):
        await r.sotto(s0393)
    elif r.prova((k0258, )):
        await r.sotto(s0399)
    elif r.prova((k0260, )):
        await r.sotto(s0405)
    elif r.prova((k0266, )):
        await r.sotto(s0411)
    elif r.prova((k0267, )):
        await r.sotto(s0420)
    elif r.prova((k0269, )):
        await r.sotto(s0429)
    elif r.prova((k0270, )):
        await r.sotto(s0438)
    elif r.prova((k0271, )):
        await r.sotto(s0447)
    elif r.prova((k0275, )):
        await r.sotto(s0454)
    elif r.prova((k0279, )):
        await r.sotto(s0460)
    elif r.prova((k0281, k0282, k0283, )):
        await r.sotto(s0466)
    elif r.prova((k0281, k0282, k0286, )):
        await r.sotto(s0469)
    elif r.prova((k0287, )):
        await r.sotto(s0477)
    elif r.prova((k0290, )):
        await r.sotto(s0478)
    elif r.prova((k0314, )):
        await r.sotto(s0481)
    elif r.prova((k0315, )):
        await r.sotto(s0506)
    elif r.prova((k0316, )):
        await r.sotto(s0507)
    elif r.prova((k0318, )):
        await r.sotto(s0508)
    elif r.prova((k0319, )):
        await r.sotto(s0511)
    elif r.prova((k0320, )):
        await r.sotto(s0516)
    elif r.prova((k0321, )):
        await r.sotto(s0517)
    elif r.prova((k0322, )):
        await r.sotto(s0522)
    elif r.prova((k0323, )):
        await r.sotto(s0523)
    elif r.prova((k0324, )):
        await r.sotto(s0528)
    elif r.prova((k0325, )):
        await r.sotto(s0529)
    elif r.prova((k0326, )):
        await r.sotto(s0534)
    elif r.prova((k0327, )):
        await r.sotto(s0535)
    elif r.prova((k0328, )):
        await r.sotto(s0540)
    elif r.prova((k0329, )):
        await r.sotto(s0541)
    elif r.prova((k0330, )):
        await r.sotto(s0546)
    elif r.prova((k0336, )):
        await r.sotto(s0547)
    elif r.prova((k0337, )):
        await r.sotto(s0564)
    elif r.prova((k0342, )):
        await r.sotto(s0565)
    elif r.prova((k0344, k0345, )):
        await r.sotto(s0570)
    elif r.prova((k0353, )):
        await r.sotto(s0575)
    elif r.prova((k0357, )):
        await r.sotto(s0586)
    elif r.prova((k0358, k0347, )):
        await r.sotto(s0590)
    elif r.prova((k0361, k0347, )):
        await r.sotto(s0591)
    elif r.prova((k0362, k0347, )):
        await r.sotto(s0596)
    elif r.prova((k0363, k0347, )):
        await r.sotto(s0597)
    elif r.prova((k0364, k0347, )):
        await r.sotto(s0602)
    elif r.prova((k0366, k0347, )):
        await r.sotto(s0603)
    elif r.prova((k0367, k0347, )):
        await r.sotto(s0608)
    elif r.prova((k0368, k0347, )):
        await r.sotto(s0609)
    elif r.prova((k0369, k0347, )):
        await r.sotto(s0614)
    elif r.prova((k0371, k0347, )):
        await r.sotto(s0615)
    elif r.prova((k0372, k0347, )):
        await r.sotto(s0620)
    elif r.prova((k0373, k0347, )):
        await r.sotto(s0621)
    elif r.prova((k0374, k0347, )):
        await r.sotto(s0626)
    elif r.prova((k0376, k0347, )):
        await r.sotto(s0627)
    elif r.prova((k0377, k0347, )):
        await r.sotto(s0632)
    elif r.prova((k0378, k0347, )):
        await r.sotto(s0633)
    elif r.prova((k0379, k0347, )):
        await r.sotto(s0638)
    elif r.prova((k0381, k0347, )):
        await r.sotto(s0639)
    elif r.prova((k0382, k0347, )):
        await r.sotto(s0644)
    elif r.prova((k0383, k0347, )):
        await r.sotto(s0645)
    elif r.prova((k0384, k0347, )):
        await r.sotto(s0650)
    elif r.prova((k0386, k0347, )):
        await r.sotto(s0651)
    elif r.prova((k0387, k0347, )):
        await r.sotto(s0656)
    elif r.prova((k0388, k0347, )):
        await r.sotto(s0657)
    elif r.prova((k0389, k0347, )):
        await r.sotto(s0662)
    elif r.prova((k0391, k0347, )):
        await r.sotto(s0663)
    elif r.prova((k0392, k0347, )):
        await r.sotto(s0668)
    elif r.prova((k0393, k0347, )):
        await r.sotto(s0669)
    elif r.prova((k0394, k0395, )):
        await r.sotto(s0674)
    elif r.prova((k0396, )):
        await r.sotto(s0675)
    elif r.prova((k0397, )):
        await r.sotto(s0676)
    elif r.prova((k0398, )):
        await r.sotto(s0677)
    elif r.prova((k0399, )):
        await r.sotto(s0678)
    elif r.prova((k0423, )):
        await r.sotto(s0679)
    elif r.prova((k0441, )):
        await r.sotto(s0740)
    elif r.prova((k0465, )):
        await r.sotto(s0807)
    elif r.prova((k0473, )):
        await r.sotto(s0889)
    elif r.prova((k0475, )):
        await r.sotto(s0898)
    elif r.prova((k0477, )):
        await r.sotto(s0900)
    elif r.prova((k0479, )):
        await r.sotto(s0902)
    elif r.prova((k0481, )):
        await r.sotto(s0904)
    elif r.prova((k0483, )):
        await r.sotto(s0906)
    elif r.prova((k0486, )):
        await r.sotto(s0908)
    elif r.prova((k0526, )):
        await r.sotto(s0924)
    elif r.prova((k0545, )):
        await r.sotto(s1002)
    elif r.prova((k0548, )):
        await r.sotto(s1061)
    elif r.prova((k0549, )):
        await r.sotto(s1064)
    elif r.prova((k0550, )):
        await r.sotto(s1068)
    elif r.prova((k0553, )):
        await r.sotto(s1072)
    elif r.prova((k0556, )):
        await r.sotto(s1081)
    elif r.prova((k0557, )):
        await r.sotto(s1090)
    elif r.prova((k0558, )):
        await r.sotto(s1091)
    elif r.prova((k0559, )):
        await r.sotto(s1092)
    elif r.prova((k0560, )):
        await r.sotto(s1093)
    elif r.prova((k0561, )):
        await r.sotto(s1094)
    elif r.prova((k0562, )):
        await r.sotto(s1095)
    elif r.prova((k0563, )):
        await r.sotto(s1096)
    elif r.prova((k0564, )):
        await r.sotto(s1097)
    elif r.prova((k0565, k0566, )):
        await r.sotto(s1098)
    elif r.prova((k0567, k0568, )):
        await r.sotto(s1099)
    elif r.prova((k0569, k0570, )):
        await r.sotto(s1100)
    elif r.prova((k0571, k0572, )):
        await r.sotto(s1101)
    elif r.prova((k0573, k0574, )):
        await r.sotto(s1102)
    elif r.prova((k0575, k0576, )):
        await r.sotto(s1103)
    elif r.prova((k0577, k0578, )):
        await r.sotto(s1104)
    elif r.prova((k0579, )):
        await r.sotto(s1105)
    elif r.prova((k0580, )):
        await r.sotto(s1106)
    elif r.prova((k0581, )):
        await r.sotto(s1107)
    elif r.prova((k0582, )):
        await r.sotto(s1108)
    elif r.prova((k0583, )):
        await r.sotto(s1109)
    elif r.prova((k0584, )):
        await r.sotto(s1110)
    elif r.prova((k0585, k0586, )):
        await r.sotto(s1111)
    elif r.prova((k0589, )):
        await r.sotto(s1112)
    elif r.prova((k0590, )):
        await r.sotto(s1113)
    elif r.prova((k0591, )):
        await r.sotto(s1114)
    elif r.prova((k0592, )):
        await r.sotto(s1115)
    elif r.prova((k0593, )):
        await r.sotto(s1116)
    elif r.prova((k0594, )):
        await r.sotto(s1117)
    elif r.prova((k0595, )):
        await r.sotto(s1118)
    elif r.prova((k0596, )):
        await r.sotto(s1119)
    elif r.prova((k0597, )):
        await r.sotto(s1120)
    elif r.prova((k0616, )):
        await r.sotto(s1121)
    elif r.prova((k0618, )):
        await r.sotto(s1158)
    elif r.prova((k0644, )):
        await r.sotto(s1161)
    elif r.prova((k0648, )):
        await r.sotto(s1197)
    elif r.prova((k0652, )):
        await r.sotto(s1202)
    elif r.prova((k0653, )):
        await r.sotto(s1208)
    elif r.prova((k0654, )):
        await r.sotto(s1212)
    elif r.prova((k0655, )):
        await r.sotto(s1216)
    elif r.prova((k0656, )):
        await r.sotto(s1220)
    elif r.prova((k0657, )):
        await r.sotto(s1224)
    elif r.prova((k0659, )):
        await r.sotto(s1228)
    elif r.prova((k0688, )):
        await r.sotto(s1232)
    elif r.prova((k0700, )):
        await r.sotto(s1268)


async def s0078(r):
    # automazione Automazione VMC Master > 0 then
    c, V = r.c, r.V
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, continua_se_errore=True, alias='Rilettura immediata della velocità')
    r.verifica()
    await r.ripeti_mentre(s0079, (k0080, ))
    await r.attendi(M.m0372, timeout=timedelta(days=0, seconds=2, microseconds=0), alias="Lettura nuova arrivata all'Ultima Lettura Valida (da cui dipende lo Status Ventilazione)")


async def s0079(r):
    # automazione Automazione VMC Master > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.pausa(timedelta(days=0, seconds=2, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, continua_se_errore=True)


async def s0080(r):
    # automazione Automazione VMC Master > 2 choose 0
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_vmc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0404)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0081(r):
    # automazione Automazione VMC Master > 2 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_vmc')]})


async def s0082(r):
    # automazione Automazione VMC Master > 2 choose 2
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_monitoraggio_sensori')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0405)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0083(r):
    # automazione Automazione VMC Master > 2 choose 3
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra'), c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni'), c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori')]}, alias='Chiude le sue sotto-finestre, non la propria, già chiusa [b42: richiusa insieme alle altre arriverebbe un giro dopo la condizione e chiuderebbe la finestra se riaperta subito]')


async def s0084(r):
    # automazione Automazione VMC Master > 2 choose 4
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0406)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0085(r):
    # automazione Automazione VMC Master > 2 choose 5
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori')]})


async def s0086(r):
    # automazione Automazione VMC Master > 2 choose 6
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0407)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0087(r):
    # automazione Automazione VMC Master > 2 choose 7
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra')]})


async def s0088(r):
    # automazione Automazione VMC Master > 2 choose 8
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0408)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0089(r):
    # automazione Automazione VMC Master > 2 choose 9
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni')]})


async def s0090(r):
    # automazione Automazione VMC Master > 2 choose 10
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_calendario')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0409)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0091(r):
    # automazione Automazione VMC Master > 2 choose 11
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_interruttore_calendario')]})


async def s0092(r):
    # automazione Automazione VMC Master > 2 choose 12
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_offset_sensori')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0410)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")
    await r.servizio('script.turn_on', {'variables': {'senza_avvisi': True}}, {'entity_id': [c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_esterna'), c.N('script.vmc_master_aggiorna_elenco_entita_temperatura_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_umidita_esterna'), c.N('script.vmc_master_aggiorna_elenco_entita_umidita_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_co2_interna'), c.N('script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo'), c.N('script.vmc_master_aggiorna_elenco_entita_media_player')]}, alias="Aggiorna gli elenchi delle Entità selezionabili (Temperatura, Umidità, Anidride Carbonica, Dispositivo Mobile, Media Player) senza avvisi: gli avvisi «Aggiornare Manualmente l'Entità…» e «Nessun cellulare…» compaiono all'avvio di Home Assistant, con la VMC di nuovo ON-Line, accendendo Invio Notifica e con Agg. Sensori, non a ogni apertura della finestra Opzioni")


async def s0093(r):
    # automazione Automazione VMC Master > 2 choose 13
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada'), c.N('input_boolean.vmc_master_opzioni_calendario_main'), c.N('input_boolean.vmc_master_opzioni_calendario'), c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling'), c.N('input_boolean.vmc_master_opzioni_scelta_sensori'), c.N('input_boolean.vmc_master_opzioni_elementi_chimici'), c.N('input_boolean.vmc_master_opzione_finestra_audio'), c.N('input_boolean.vmc_master_conferma_pulizia_cronologia')]}, alias='Chiude le sue sotto-finestre, non la propria, già chiusa [b42: richiusa insieme alle altre arriverebbe un giro dopo la condizione e chiuderebbe la finestra se riaperta subito]')


async def s0094(r):
    # automazione Automazione VMC Master > 2 choose 14
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0411)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0095(r):
    # automazione Automazione VMC Master > 2 choose 15
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada')]})


async def s0096(r):
    # automazione Automazione VMC Master > 2 choose 16
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_calendario_main')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0412)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0097(r):
    # automazione Automazione VMC Master > 2 choose 17
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_calendario_main')]})


async def s0098(r):
    # automazione Automazione VMC Master > 2 choose 18
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_calendario')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0413)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0099(r):
    # automazione Automazione VMC Master > 2 choose 19
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_calendario')]})


async def s0100(r):
    # automazione Automazione VMC Master > 2 choose 20
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0414)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0101(r):
    # automazione Automazione VMC Master > 2 choose 21
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling')]})


async def s0102(r):
    # automazione Automazione VMC Master > 2 choose 22
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_avvisi')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0415)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0103(r):
    # automazione Automazione VMC Master > 2 choose 23
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_avvisi_grafici')]}, alias='Chiude le sue sotto-finestre, non la propria, già chiusa [b42: richiusa insieme alle altre arriverebbe un giro dopo la condizione e chiuderebbe la finestra se riaperta subito]')


async def s0104(r):
    # automazione Automazione VMC Master > 2 choose 24
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_lettura_sensori')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0416)}, alias="Chiude le altre finestre solo se sono state aperte prima di questa [b42: una finestra aperta dopo, mentre l'automazione era occupata, resta aperta e vince l'ultimo tocco]")


async def s0105(r):
    # automazione Automazione VMC Master > 2 choose 25
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_lettura_sensori')]})


async def s0106(r):
    # automazione Automazione VMC Master > 2 choose 26
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0135, )):
        await r.sotto(s0107)
    r.verifica()
    if r.prova((k0138, )):
        await r.sotto(s0108)
    else:
        await r.sotto(s0112)


async def s0107(r):
    # automazione Automazione VMC Master > 2 choose 26 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0108(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0109, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0110)
    else:
        await r.sotto(s0111)


async def s0109(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0110(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0111(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0112(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 else
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')]})
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias='Memoria Inquinanti/PdR senza Inquinanti in corso -> spenta la memoria, si arresta la VMC come nel ramo principale (correzione O3)')
    r.verifica()
    await r.ripeti_finche(s0113, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0114)
    else:
        await r.sotto(s0115)


async def s0113(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 else > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0114(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 else > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0115(r):
    # automazione Automazione VMC Master > 2 choose 26 > 1 else > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0116(r):
    # automazione Automazione VMC Master > 2 choose 27
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0140, )):
        await r.sotto(s0117)
    r.verifica()
    if r.prova(()):
        await r.sotto(s0118)


async def s0117(r):
    # automazione Automazione VMC Master > 2 choose 27 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0118(r):
    # automazione Automazione VMC Master > 2 choose 27 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0119, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0120)
    else:
        await r.sotto(s0121)


async def s0119(r):
    # automazione Automazione VMC Master > 2 choose 27 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0120(r):
    # automazione Automazione VMC Master > 2 choose 27 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0121(r):
    # automazione Automazione VMC Master > 2 choose 27 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0122(r):
    # automazione Automazione VMC Master > 2 choose 28
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0142, )):
        await r.sotto(s0123)
    r.verifica()
    if r.prova(()):
        await r.sotto(s0124)


async def s0123(r):
    # automazione Automazione VMC Master > 2 choose 28 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0124(r):
    # automazione Automazione VMC Master > 2 choose 28 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0125, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0126)
    else:
        await r.sotto(s0127)


async def s0125(r):
    # automazione Automazione VMC Master > 2 choose 28 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0126(r):
    # automazione Automazione VMC Master > 2 choose 28 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0127(r):
    # automazione Automazione VMC Master > 2 choose 28 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0128(r):
    # automazione Automazione VMC Master > 2 choose 29
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0144, )):
        await r.sotto(s0129)
    r.verifica()
    if r.prova(()):
        await r.sotto(s0130)


async def s0129(r):
    # automazione Automazione VMC Master > 2 choose 29 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0130(r):
    # automazione Automazione VMC Master > 2 choose 29 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0131, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0132)
    else:
        await r.sotto(s0133)


async def s0131(r):
    # automazione Automazione VMC Master > 2 choose 29 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0132(r):
    # automazione Automazione VMC Master > 2 choose 29 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0133(r):
    # automazione Automazione VMC Master > 2 choose 29 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0134(r):
    # automazione Automazione VMC Master > 2 choose 30
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0146, )):
        await r.sotto(s0135)
    r.verifica()
    if r.prova(()):
        await r.sotto(s0136)


async def s0135(r):
    # automazione Automazione VMC Master > 2 choose 30 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0136(r):
    # automazione Automazione VMC Master > 2 choose 30 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0137, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0138)
    else:
        await r.sotto(s0139)


async def s0137(r):
    # automazione Automazione VMC Master > 2 choose 30 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0138(r):
    # automazione Automazione VMC Master > 2 choose 30 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0139(r):
    # automazione Automazione VMC Master > 2 choose 30 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0140(r):
    # automazione Automazione VMC Master > 2 choose 31
    c, V = r.c, r.V
    r.verifica()
    if r.prova(()):
        await r.sotto(s0141)


async def s0141(r):
    # automazione Automazione VMC Master > 2 choose 31 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0142, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0143)
    else:
        await r.sotto(s0144)


async def s0142(r):
    # automazione Automazione VMC Master > 2 choose 31 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0143(r):
    # automazione Automazione VMC Master > 2 choose 31 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0144(r):
    # automazione Automazione VMC Master > 2 choose 31 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0145(r):
    # automazione Automazione VMC Master > 2 choose 32
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0149, )):
        await r.sotto(s0146)
    r.verifica()
    if r.prova(()):
        await r.sotto(s0147)


async def s0146(r):
    # automazione Automazione VMC Master > 2 choose 32 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0147(r):
    # automazione Automazione VMC Master > 2 choose 32 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0148, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0149)
    else:
        await r.sotto(s0150)


async def s0148(r):
    # automazione Automazione VMC Master > 2 choose 32 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0149(r):
    # automazione Automazione VMC Master > 2 choose 32 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0150(r):
    # automazione Automazione VMC Master > 2 choose 32 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0151(r):
    # automazione Automazione VMC Master > 2 choose 33
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0156, )):
        await r.sotto(s0152)


async def s0152(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0153, )):
        await r.sotto(s0153)
    elif r.prova((k0154, )):
        await r.sotto(s0157)
    elif r.prova((k0155, )):
        await r.sotto(s0161)


async def s0153(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0154, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0155)
    else:
        await r.sotto(s0156)


async def s0154(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0155(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0156(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0157(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0158, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0159)
    else:
        await r.sotto(s0160)


async def s0158(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0159(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0160(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 1 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0161(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 2
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0162, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0163)
    else:
        await r.sotto(s0164)


async def s0162(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0163(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 2 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0164(r):
    # automazione Automazione VMC Master > 2 choose 33 > 0 then > 0 choose 2 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0165(r):
    # automazione Automazione VMC Master > 2 choose 34
    c, V = r.c, r.V
    r.verifica()
    if r.prova(()):
        await r.sotto(s0166)


async def s0166(r):
    # automazione Automazione VMC Master > 2 choose 34 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0167, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s0168)
    else:
        await r.sotto(s0169)


async def s0167(r):
    # automazione Automazione VMC Master > 2 choose 34 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0168(r):
    # automazione Automazione VMC Master > 2 choose 34 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0169(r):
    # automazione Automazione VMC Master > 2 choose 34 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0170(r):
    # automazione Automazione VMC Master > 2 choose 35
    c, V = r.c, r.V
    r.verifica()
    if r.prova(()):
        await r.sotto(s0171)


async def s0171(r):
    # automazione Automazione VMC Master > 2 choose 35 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0172, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s0173)
    else:
        await r.sotto(s0174)


async def s0172(r):
    # automazione Automazione VMC Master > 2 choose 35 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0173(r):
    # automazione Automazione VMC Master > 2 choose 35 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0174(r):
    # automazione Automazione VMC Master > 2 choose 35 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0175(r):
    # automazione Automazione VMC Master > 2 choose 36
    c, V = r.c, r.V
    r.verifica()
    if r.prova(()):
        await r.sotto(s0176)


async def s0176(r):
    # automazione Automazione VMC Master > 2 choose 36 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0177, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s0178)
    else:
        await r.sotto(s0179)


async def s0177(r):
    # automazione Automazione VMC Master > 2 choose 36 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0178(r):
    # automazione Automazione VMC Master > 2 choose 36 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0179(r):
    # automazione Automazione VMC Master > 2 choose 36 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0180(r):
    # automazione Automazione VMC Master > 2 choose 37
    c, V = r.c, r.V
    r.verifica()
    if r.prova(()):
        await r.sotto(s0181)


async def s0181(r):
    # automazione Automazione VMC Master > 2 choose 37 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0182, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s0183)
    else:
        await r.sotto(s0184)


async def s0182(r):
    # automazione Automazione VMC Master > 2 choose 37 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0183(r):
    # automazione Automazione VMC Master > 2 choose 37 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0184(r):
    # automazione Automazione VMC Master > 2 choose 37 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0185(r):
    # automazione Automazione VMC Master > 2 choose 38
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0170, )):
        await r.sotto(s0186)
    elif r.prova((k0171, )):
        await r.sotto(s0190)
    elif r.prova((k0174, )):
        await r.sotto(s0194)
    elif r.prova((k0175, )):
        await r.sotto(s0198)
    elif r.prova((k0176, )):
        await r.sotto(s0202)


async def s0186(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0187, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0188)
    else:
        await r.sotto(s0189)


async def s0187(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0188(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0189(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0190(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 1
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0191, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0192)
    else:
        await r.sotto(s0193)


async def s0191(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 1 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0192(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0193(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 1 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0194(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 2
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0195, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0196)
    else:
        await r.sotto(s0197)


async def s0195(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 2 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0196(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 2 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0197(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 2 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0198(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 3
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0199, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0200)
    else:
        await r.sotto(s0201)


async def s0199(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 3 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0200(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 3 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0201(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 3 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0202(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 4
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0203, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0204)
    else:
        await r.sotto(s0205)


async def s0203(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 4 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc')]})
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0204(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 4 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0205(r):
    # automazione Automazione VMC Master > 2 choose 38 > 0 choose 4 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0206(r):
    # automazione Automazione VMC Master > 2 choose 39
    c, V = r.c, r.V
    r.verifica()
    if r.prova(()):
        await r.sotto(s0207)


async def s0207(r):
    # automazione Automazione VMC Master > 2 choose 39 > 0 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0208, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s0209)
    else:
        await r.sotto(s0210)


async def s0208(r):
    # automazione Automazione VMC Master > 2 choose 39 > 0 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0209(r):
    # automazione Automazione VMC Master > 2 choose 39 > 0 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0210(r):
    # automazione Automazione VMC Master > 2 choose 39 > 0 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0211(r):
    # automazione Automazione VMC Master > 2 choose 40
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')]})


async def s0212(r):
    # automazione Automazione VMC Master > 2 choose 41
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0182, )):
        await r.sotto(s0213)
    r.verifica()
    await r.ripeti_finche(s0214, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0215)
    else:
        await r.sotto(s0216)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s0217)
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')]})


async def s0213(r):
    # automazione Automazione VMC Master > 2 choose 41 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0214(r):
    # automazione Automazione VMC Master > 2 choose 41 > 2 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0215(r):
    # automazione Automazione VMC Master > 2 choose 41 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0216(r):
    # automazione Automazione VMC Master > 2 choose 41 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0217(r):
    # automazione Automazione VMC Master > 2 choose 41 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0218(r):
    # automazione Automazione VMC Master > 2 choose 42
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio')]})
    r.verifica()
    if r.prova((k0185, )):
        await r.sotto(s0219)


async def s0219(r):
    # automazione Automazione VMC Master > 2 choose 42 > 1 then
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0220, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0221)
    else:
        await r.sotto(s0222)


async def s0220(r):
    # automazione Automazione VMC Master > 2 choose 42 > 1 then > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0221(r):
    # automazione Automazione VMC Master > 2 choose 42 > 1 then > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0222(r):
    # automazione Automazione VMC Master > 2 choose 42 > 1 then > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0223(r):
    # automazione Automazione VMC Master > 2 choose 43
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0187, )):
        await r.sotto(s0224)
    r.verifica()
    await r.ripeti_finche(s0225, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0226)
    else:
        await r.sotto(s0227)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s0228)


async def s0224(r):
    # automazione Automazione VMC Master > 2 choose 43 > 1 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0225(r):
    # automazione Automazione VMC Master > 2 choose 43 > 2 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0226(r):
    # automazione Automazione VMC Master > 2 choose 43 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0227(r):
    # automazione Automazione VMC Master > 2 choose 43 > 3 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0228(r):
    # automazione Automazione VMC Master > 2 choose 43 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0229(r):
    # automazione Automazione VMC Master > 2 choose 44
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0230)
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0187, )):
        await r.sotto(s0231)
    r.verifica()
    await r.ripeti_finche(s0232, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0233)
    else:
        await r.sotto(s0234)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s0235)


async def s0230(r):
    # automazione Automazione VMC Master > 2 choose 44 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0231(r):
    # automazione Automazione VMC Master > 2 choose 44 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0232(r):
    # automazione Automazione VMC Master > 2 choose 44 > 3 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_1'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0233(r):
    # automazione Automazione VMC Master > 2 choose 44 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0428)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0234(r):
    # automazione Automazione VMC Master > 2 choose 44 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0235(r):
    # automazione Automazione VMC Master > 2 choose 44 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0236(r):
    # automazione Automazione VMC Master > 2 choose 45
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0237)
    r.verifica()
    await r.ripeti_finche(s0238, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0193, )):
        await r.sotto(s0239)
    r.verifica()
    await r.ripeti_finche(s0240, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s0241)
    else:
        await r.sotto(s0242)
    r.verifica()
    if r.prova((k0194, )):
        await r.sotto(s0243)


async def s0237(r):
    # automazione Automazione VMC Master > 2 choose 45 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0238(r):
    # automazione Automazione VMC Master > 2 choose 45 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0239(r):
    # automazione Automazione VMC Master > 2 choose 45 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0240(r):
    # automazione Automazione VMC Master > 2 choose 45 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0241(r):
    # automazione Automazione VMC Master > 2 choose 45 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0242(r):
    # automazione Automazione VMC Master > 2 choose 45 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0243(r):
    # automazione Automazione VMC Master > 2 choose 45 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0244(r):
    # automazione Automazione VMC Master > 2 choose 46
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0245)
    r.verifica()
    await r.ripeti_finche(s0246, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0196, )):
        await r.sotto(s0247)
    r.verifica()
    await r.ripeti_finche(s0248, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s0249)
    else:
        await r.sotto(s0250)
    r.verifica()
    if r.prova((k0197, )):
        await r.sotto(s0251)


async def s0245(r):
    # automazione Automazione VMC Master > 2 choose 46 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0246(r):
    # automazione Automazione VMC Master > 2 choose 46 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0247(r):
    # automazione Automazione VMC Master > 2 choose 46 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0248(r):
    # automazione Automazione VMC Master > 2 choose 46 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0249(r):
    # automazione Automazione VMC Master > 2 choose 46 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0250(r):
    # automazione Automazione VMC Master > 2 choose 46 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0251(r):
    # automazione Automazione VMC Master > 2 choose 46 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0252(r):
    # automazione Automazione VMC Master > 2 choose 47
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0253)
    r.verifica()
    await r.ripeti_finche(s0254, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0199, )):
        await r.sotto(s0255)
    r.verifica()
    await r.ripeti_finche(s0256, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s0257)
    else:
        await r.sotto(s0258)
    r.verifica()
    if r.prova((k0200, )):
        await r.sotto(s0259)


async def s0253(r):
    # automazione Automazione VMC Master > 2 choose 47 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0254(r):
    # automazione Automazione VMC Master > 2 choose 47 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0255(r):
    # automazione Automazione VMC Master > 2 choose 47 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0256(r):
    # automazione Automazione VMC Master > 2 choose 47 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0257(r):
    # automazione Automazione VMC Master > 2 choose 47 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0258(r):
    # automazione Automazione VMC Master > 2 choose 47 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0259(r):
    # automazione Automazione VMC Master > 2 choose 47 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0260(r):
    # automazione Automazione VMC Master > 2 choose 48
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0261)
    r.verifica()
    await r.ripeti_finche(s0262, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0202, )):
        await r.sotto(s0263)
    r.verifica()
    await r.ripeti_finche(s0264, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s0265)
    else:
        await r.sotto(s0266)
    r.verifica()
    if r.prova((k0203, )):
        await r.sotto(s0267)


async def s0261(r):
    # automazione Automazione VMC Master > 2 choose 48 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0262(r):
    # automazione Automazione VMC Master > 2 choose 48 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0263(r):
    # automazione Automazione VMC Master > 2 choose 48 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0264(r):
    # automazione Automazione VMC Master > 2 choose 48 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0265(r):
    # automazione Automazione VMC Master > 2 choose 48 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0266(r):
    # automazione Automazione VMC Master > 2 choose 48 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0267(r):
    # automazione Automazione VMC Master > 2 choose 48 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0268(r):
    # automazione Automazione VMC Master > 2 choose 49
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0269)
    r.verifica()
    await r.ripeti_finche(s0270, (k0205, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0206, )):
        await r.sotto(s0271)
    r.verifica()
    if r.prova((k0207, )):
        await r.sotto(s0272)
    r.verifica()
    await r.ripeti_finche(s0273, (k0209, ))
    r.verifica()
    if r.prova((k0210, )):
        await r.sotto(s0276)
    else:
        await r.sotto(s0277)
    r.variabili({'velocita_fine_allerta': Modello(M.m0479)}, alias='Velocità di fine allerta (per il ripristino dopo un Black-Out)')
    r.verifica()
    if r.prova((k0211, )):
        await r.sotto(s0278)


async def s0269(r):
    # automazione Automazione VMC Master > 2 choose 49 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0270(r):
    # automazione Automazione VMC Master > 2 choose 49 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0271(r):
    # automazione Automazione VMC Master > 2 choose 49 > 3 then
    c, V = r.c, r.V
    r.verifica()
    raise Ferma("Velocità 1 dell'allerta Umidità con la Free sospesa mantenuta [Nota 3]: la ripresa Free resta in attesa")


async def s0272(r):
    # automazione Automazione VMC Master > 2 choose 49 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0273(r):
    # automazione Automazione VMC Master > 2 choose 49 > 5 repeat
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0208, )):
        await r.sotto(s0274)
    else:
        await r.sotto(s0275)
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0274(r):
    # automazione Automazione VMC Master > 2 choose 49 > 5 repeat > 0 then
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})


async def s0275(r):
    # automazione Automazione VMC Master > 2 choose 49 > 5 repeat > 0 else
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})


async def s0276(r):
    # automazione Automazione VMC Master > 2 choose 49 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0477)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0277(r):
    # automazione Automazione VMC Master > 2 choose 49 > 6 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0278(r):
    # automazione Automazione VMC Master > 2 choose 49 > 8 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': Modello(M.m0480)})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': Modello(M.m0481)})


async def s0279(r):
    # automazione Automazione VMC Master > 2 choose 50
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0189, )):
        await r.sotto(s0280)
    r.verifica()
    await r.ripeti_finche(s0281, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0213, )):
        await r.sotto(s0282)
    r.verifica()
    await r.ripeti_finche(s0283, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s0284)
    else:
        await r.sotto(s0285)
    r.verifica()
    if r.prova((k0214, )):
        await r.sotto(s0286)


async def s0280(r):
    # automazione Automazione VMC Master > 2 choose 50 > 0 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio')]})
    r.verifica()
    raise Ferma('Fine Umidità affidata a spia_umidita_off')


async def s0281(r):
    # automazione Automazione VMC Master > 2 choose 50 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0282(r):
    # automazione Automazione VMC Master > 2 choose 50 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0283(r):
    # automazione Automazione VMC Master > 2 choose 50 > 4 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0284(r):
    # automazione Automazione VMC Master > 2 choose 50 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0285(r):
    # automazione Automazione VMC Master > 2 choose 50 > 5 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0286(r):
    # automazione Automazione VMC Master > 2 choose 50 > 6 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0287(r):
    # automazione Automazione VMC Master > 2 choose 51
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0288, (k0216, ))


async def s0288(r):
    # automazione Automazione VMC Master > 2 choose 51 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio')]})


async def s0289(r):
    # automazione Automazione VMC Master > 2 choose 52
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0290, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0218, )):
        await r.sotto(s0291)
    r.verifica()
    await r.ripeti_finche(s0292, (k0158, ))
    r.verifica()
    if r.prova((k0159, )):
        await r.sotto(s0293)
    else:
        await r.sotto(s0294)
    r.verifica()
    if r.prova((k0194, )):
        await r.sotto(s0295)


async def s0290(r):
    # automazione Automazione VMC Master > 2 choose 52 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0291(r):
    # automazione Automazione VMC Master > 2 choose 52 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0292(r):
    # automazione Automazione VMC Master > 2 choose 52 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_2'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0293(r):
    # automazione Automazione VMC Master > 2 choose 52 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0435)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0294(r):
    # automazione Automazione VMC Master > 2 choose 52 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0295(r):
    # automazione Automazione VMC Master > 2 choose 52 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_2')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0296(r):
    # automazione Automazione VMC Master > 2 choose 53
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0297, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0220, )):
        await r.sotto(s0298)
    r.verifica()
    await r.ripeti_finche(s0299, (k0161, ))
    r.verifica()
    if r.prova((k0162, )):
        await r.sotto(s0300)
    else:
        await r.sotto(s0301)
    r.verifica()
    if r.prova((k0197, )):
        await r.sotto(s0302)


async def s0297(r):
    # automazione Automazione VMC Master > 2 choose 53 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0298(r):
    # automazione Automazione VMC Master > 2 choose 53 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0299(r):
    # automazione Automazione VMC Master > 2 choose 53 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_3'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0300(r):
    # automazione Automazione VMC Master > 2 choose 53 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0438)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0301(r):
    # automazione Automazione VMC Master > 2 choose 53 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0302(r):
    # automazione Automazione VMC Master > 2 choose 53 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_3')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0303(r):
    # automazione Automazione VMC Master > 2 choose 54
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0304, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0222, )):
        await r.sotto(s0305)
    r.verifica()
    await r.ripeti_finche(s0306, (k0164, ))
    r.verifica()
    if r.prova((k0165, )):
        await r.sotto(s0307)
    else:
        await r.sotto(s0308)
    r.verifica()
    if r.prova((k0200, )):
        await r.sotto(s0309)


async def s0304(r):
    # automazione Automazione VMC Master > 2 choose 54 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0305(r):
    # automazione Automazione VMC Master > 2 choose 54 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0306(r):
    # automazione Automazione VMC Master > 2 choose 54 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_velocita_4'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0307(r):
    # automazione Automazione VMC Master > 2 choose 54 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0441)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0308(r):
    # automazione Automazione VMC Master > 2 choose 54 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0309(r):
    # automazione Automazione VMC Master > 2 choose 54 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_4')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0310(r):
    # automazione Automazione VMC Master > 2 choose 55
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0311, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0224, )):
        await r.sotto(s0312)
    r.verifica()
    await r.ripeti_finche(s0313, (k0167, ))
    r.verifica()
    if r.prova((k0168, )):
        await r.sotto(s0314)
    else:
        await r.sotto(s0315)
    r.verifica()
    if r.prova((k0203, )):
        await r.sotto(s0316)


async def s0311(r):
    # automazione Automazione VMC Master > 2 choose 55 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0312(r):
    # automazione Automazione VMC Master > 2 choose 55 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0313(r):
    # automazione Automazione VMC Master > 2 choose 55 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_notturna'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0314(r):
    # automazione Automazione VMC Master > 2 choose 55 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0444)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0315(r):
    # automazione Automazione VMC Master > 2 choose 55 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0316(r):
    # automazione Automazione VMC Master > 2 choose 55 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_notturna')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0317(r):
    # automazione Automazione VMC Master > 2 choose 56
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0228, )):
        await r.sotto(s0318)
    elif r.prova((k0229, )):
        await r.sotto(s0325)
    elif r.prova((k0230, )):
        await r.sotto(s0332)
    elif r.prova((k0231, )):
        await r.sotto(s0339)
    elif r.prova((k0232, )):
        await r.sotto(s0341)


async def s0318(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0319, (k0205, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0226, )):
        await r.sotto(s0320)
    r.verifica()
    await r.ripeti_finche(s0321, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0322)
    else:
        await r.sotto(s0323)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0324)


async def s0319(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0320(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0321(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0322(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0323(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0324(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 0 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})


async def s0325(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0326, (k0205, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0226, )):
        await r.sotto(s0327)
    r.verifica()
    await r.ripeti_finche(s0328, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0329)
    else:
        await r.sotto(s0330)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0331)


async def s0326(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0327(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0328(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0329(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0330(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0331(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 1 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})


async def s0332(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0333, (k0205, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0226, )):
        await r.sotto(s0334)
    r.verifica()
    await r.ripeti_finche(s0335, (k0172, ))
    r.verifica()
    if r.prova((k0173, )):
        await r.sotto(s0336)
    else:
        await r.sotto(s0337)
    r.verifica()
    if r.prova((k0227, )):
        await r.sotto(s0338)


async def s0333(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0334(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0335(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_freecooling'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0336(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0449)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0337(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0338(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 2 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})


async def s0339(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 3
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0340, (k0205, ))


async def s0340(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 3 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0341(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 4
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0342, (k0205, ))


async def s0342(r):
    # automazione Automazione VMC Master > 2 choose 56 > 0 choose 4 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio')]})


async def s0343(r):
    # automazione Automazione VMC Master > 2 choose 57
    c, V = r.c, r.V
    r.verifica()
    await r.ripeti_finche(s0344, (k0192, ))
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    if r.prova((k0234, )):
        await r.sotto(s0345)
    r.verifica()
    await r.ripeti_finche(s0346, (k0178, ))
    r.verifica()
    if r.prova((k0179, )):
        await r.sotto(s0347)
    else:
        await r.sotto(s0348)
    r.verifica()
    if r.prova((k0214, )):
        await r.sotto(s0349)


async def s0344(r):
    # automazione Automazione VMC Master > 2 choose 57 > 0 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})


async def s0345(r):
    # automazione Automazione VMC Master > 2 choose 57 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    r.verifica()
    raise Ferma("Velocità scelta dall'utente durante l'allerta PdR mantenuta")


async def s0346(r):
    # automazione Automazione VMC Master > 2 choose 57 > 3 repeat
    c, V = r.c, r.V
    await r.servizio(c.N('shell_command.vmc_master_iperventilazione'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0347(r):
    # automazione Automazione VMC Master > 2 choose 57 > 4 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0455)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0348(r):
    # automazione Automazione VMC Master > 2 choose 57 > 4 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0349(r):
    # automazione Automazione VMC Master > 2 choose 57 > 5 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_iperventilazione')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0350(r):
    # automazione Automazione VMC Master > 2 choose 58
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0351)
    elif r.prova((k0237, )):
        await r.sotto(s0356)


async def s0351(r):
    # automazione Automazione VMC Master > 2 choose 58 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0352, (k0136, ))
    r.verifica()
    if r.prova((k0137, )):
        await r.sotto(s0353)
    else:
        await r.sotto(s0354)
    r.verifica()
    if r.prova((k0183, )):
        await r.sotto(s0355)


async def s0352(r):
    # automazione Automazione VMC Master > 2 choose 58 > 0 choose 0 > 1 repeat
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_co2_o_voc'), c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr'), c.N('input_boolean.vmc_master_spia_velocita_0_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_1_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_2_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_3_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_4_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc'), c.N('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_1_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_2_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_3_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_4_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_notturna_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_un_solo_avvio'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio'), c.N('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia'), c.N('input_boolean.vmc_master_spia_velocita_0_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_1_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_2_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_3_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_4_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_notturna_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_congelamento'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling'), c.N('input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating')]})
    await r.servizio(c.N('shell_command.vmc_master_velocita_0'), {})
    await r.pausa(timedelta(days=0, seconds=1, microseconds=0))
    await r.servizio('homeassistant.update_entity', None, {'entity_id': [c.N('sensor.vmc_master_status_ventola')]}, alias="Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta dell'utente)")
    await r.pausa(timedelta(days=0, seconds=3, microseconds=0))


async def s0353(r):
    # automazione Automazione VMC Master > 2 choose 58 > 0 choose 0 > 2 then
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': Modello(M.m0419)}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]})


async def s0354(r):
    # automazione Automazione VMC Master > 2 choose 58 > 0 choose 0 > 2 else
    c, V = r.c, r.V
    await r.servizio('input_text.set_value', {'value': ''}, {'entity_id': [c.N('input_text.vmc_master_comando_non_eseguito')]}, alias="Comando confermato (o velocità scelta dall'utente) -> un Comando non eseguito più vecchio si annulla")


async def s0355(r):
    # automazione Automazione VMC Master > 2 choose 58 > 0 choose 0 > 3 then
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_0')]})
    await r.servizio('input_boolean.turn_off', {}, {'entity_id': [c.N('input_boolean.vmc_master_spia_velocita_1'), c.N('input_boolean.vmc_master_spia_velocita_2'), c.N('input_boolean.vmc_master_spia_velocita_3'), c.N('input_boolean.vmc_master_spia_velocita_4'), c.N('input_boolean.vmc_master_spia_velocita_notturna'), c.N('input_boolean.vmc_master_spia_velocita_iperventilazione'), c.N('input_boolean.vmc_master_spia_velocita_freecooling')]})


async def s0356(r):
    # automazione Automazione VMC Master > 2 choose 58 > 0 choose 1
    c, V = r.c, r.V
    await r.servizio('input_boolean.turn_on', {}, {'entity_id': [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')]})


async def s0357(r):
    # automazione Automazione VMC Master > 2 choose 59
    c, V = r.c, r.V
    r.verifica()
    if r.prova((k0236, )):
        await r.sotto(s0358)
    elif r.prova((k0237, )):
        await r.sotto(s0363)


async def s0358(r):
    # automazione Automazione VMC Master > 2 choose 59 > 0 choose 0
    c, V = r.c, r.V
    r.variabili({'vel_prima_del_comando': Modello(M.m0001)}, alias="Memorizza la velocità prima del comando (un cambio fatto dall'utente ferma il ciclo di conferma)")
    r.verifica()
    await r.ripeti_finche(s0359, (k0151, ))
    r.verifica()
    if r.prova((k0152, )):
        await r.sotto(s0360)
    else:
        await r.sotto(s0361)
    r.verifica()
    if r.prova((k0190, )):
        await r.sotto(s0362)
