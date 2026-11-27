"""Automazioni e script del package, tradotti in Python (parte 1 di 8).

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off

from datetime import time, timedelta

from .. import condizioni as C
from ..definizioni import Automazione, Script
from ..esecuzione import Annulla, Ferma, Modello
from . import modelli as M


def k0001(c, V):
    return C.modello(c, M.m0004, V)


def k0002(c, V):
    return C.modello(c, M.m0005, V)


def k0003(c, V):
    return C.stato(c, V, [c.N('input_text.vmc_master_tempo_mancante_reset')], ['reset'])


def k0004(c, V):
    return C.modello(c, M.m0013, V)


def k0005(c, V):
    return C.modello(c, M.m0016, V)


def k0006(c, V):
    return C.modello(c, M.m0018, V)


def k0007(c, V):
    return C.modello(c, M.m0019, V)


def k0008(c, V):
    return C.modello(c, M.m0020, V)


def k0009(c, V):
    return C.modello(c, M.m0021, V)


def k0010(c, V):
    return C.modello(c, M.m0022, V)


def k0011(c, V):
    return C.modello(c, M.m0023, V)


def k0012(c, V):
    return C.modello(c, M.m0024, V)


def k0013(c, V):
    return C.modello(c, M.m0025, V)


def k0014(c, V):
    return C.modello(c, M.m0026, V)


def k0015(c, V):
    return C.modello(c, M.m0027, V)


def k0016(c, V):
    return C.modello(c, M.m0028, V)


def k0017(c, V):
    return C.modello(c, M.m0029, V)


def k0018(c, V):
    return C.modello(c, M.m0030, V)


def k0019(c, V):
    return C.modello(c, M.m0031, V)


def k0020(c, V):
    return C.modello(c, M.m0032, V)


def k0021(c, V):
    return C.modello(c, M.m0033, V)


def k0022(c, V):
    return C.modello(c, M.m0034, V)


def k0023(c, V):
    return C.modello(c, M.m0035, V)


def k0024(c, V):
    return C.modello(c, M.m0036, V)


def k0025(c, V):
    return C.modello(c, M.m0037, V)


def k0026(c, V):
    return C.trigger(V, ['spia_avvio_rimasta_accesa'])


def k0027(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_notifica_audio')], ['on'])


def k0028(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_notifica_allerta_riepilogo')], ['on'])


def k0029(c, V):
    return C.e(c, V, (k0027, k0028, ))


def k0030(c, V):
    return C.o(c, V, (k0026, k0029, ))


def k0031(c, V):
    return C.modello(c, M.m0038, V)


def k0032(c, V):
    return C.modello(c, M.m0039, V)


def k0033(c, V):
    return C.modello(c, M.m0040, V)


def k0034(c, V):
    return C.modello(c, M.m0041, V)


def k0035(c, V):
    return C.modello(c, M.m0042, V)


def k0036(c, V):
    return C.modello(c, M.m0043, V)


def k0037(c, V):
    return C.modello(c, M.m0044, V)


def k0038(c, V):
    return C.modello(c, M.m0045, V)


def k0039(c, V):
    return C.modello(c, M.m0046, V)


def k0040(c, V):
    return C.modello(c, M.m0047, V)


def k0041(c, V):
    return C.modello(c, M.m0048, V)


def k0042(c, V):
    return C.modello(c, M.m0049, V)


def k0043(c, V):
    return C.modello(c, M.m0050, V)


def k0044(c, V):
    return C.modello(c, M.m0051, V)


def k0045(c, V):
    return C.modello(c, M.m0052, V)


def k0046(c, V):
    return C.modello(c, M.m0053, V)


def k0047(c, V):
    return C.modello(c, M.m0054, V)


def k0048(c, V):
    return C.modello(c, M.m0055, V)


def k0049(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_avvio_home_assistant_in_corso_per_audio')], ['off'])


def k0050(c, V):
    return C.modello(c, M.m0063, V)


def k0051(c, V):
    return C.modello(c, M.m0064, V)


def k0052(c, V):
    return C.modello(c, M.m0074, V)


def k0053(c, V):
    return C.modello(c, M.m0077, V)


def k0054(c, V):
    return C.modello(c, M.m0343, V)


def k0055(c, V):
    return C.modello(c, M.m0353, V)


def k0056(c, V):
    return C.modello(c, M.m0357, V)


def k0057(c, V):
    return C.modello(c, M.m0359, V)


def k0058(c, V):
    return C.modello(c, M.m0361, V)


def k0059(c, V):
    return C.modello(c, M.m0363, V)


def k0060(c, V):
    return C.modello(c, M.m0369, V)


def k0061(c, V):
    return C.modello(c, M.m0370, V)


def k0062(c, V):
    return C.modello(c, M.m0371, V)


def k0063(c, V):
    return C.modello(c, M.m0373, V)


def k0064(c, V):
    return C.modello(c, M.m0375, V)


def k0065(c, V):
    return C.modello(c, M.m0376, V)


def k0066(c, V):
    return C.modello(c, M.m0382, V)


def k0067(c, V):
    return C.modello(c, M.m0383, V)


def k0068(c, V):
    return C.modello(c, M.m0384, V)


def k0069(c, V):
    return C.modello(c, M.m0386, V)


def k0070(c, V):
    return C.modello(c, M.m0387, V)


def k0071(c, V):
    return C.modello(c, M.m0388, V)


def k0072(c, V):
    return C.modello(c, M.m0389, V)


def k0073(c, V):
    return C.modello(c, M.m0390, V)


def k0074(c, V):
    return C.trigger(V, ['nuova_timer'])


def k0075(c, V):
    return C.modello(c, M.m0396, V)


def k0076(c, V):
    return C.trigger(V, ['esistente_sensori', 'pannello_sensori'])


def k0077(c, V):
    return C.trigger(V, ['nuova'])


def k0078(c, V):
    return C.trigger(V, ['esistente', 'pannello'])


def k0079(c, V):
    return C.modello(c, M.m0400, V)


def k0080(c, V):
    return C.modello(c, M.m0401, V)


def k0081(c, V):
    return C.modello(c, M.m0402, V)


def k0082(c, V):
    return C.modello(c, M.m0403, V)


def k0083(c, V):
    return C.trigger(V, ['Opzioni Telecomando On'])


def k0084(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_vmc')], ['on'])


def k0085(c, V):
    return C.trigger(V, ['Opzioni Telecomando Off'])


def k0086(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_vmc')], ['off'])


def k0087(c, V):
    return C.trigger(V, ['Opzioni Monitoraggio On'])


def k0088(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_monitoraggio_sensori')], ['on'])


def k0089(c, V):
    return C.trigger(V, ['Opzioni Monitoraggio Off'])


def k0090(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_monitoraggio_sensori')], ['off'])


def k0091(c, V):
    return C.trigger(V, ['Opzioni Sub Offset On'])


def k0092(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori')], ['on'])


def k0093(c, V):
    return C.trigger(V, ['Opzioni Sub Offset Off'])


def k0094(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_offset_sensori')], ['off'])


def k0095(c, V):
    return C.trigger(V, ['Opzioni Sub Extra Sensori On'])


def k0096(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra')], ['on'])


def k0097(c, V):
    return C.trigger(V, ['Opzioni Sub Extra Sensori Off'])


def k0098(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra')], ['off'])


def k0099(c, V):
    return C.trigger(V, ['Opzioni Sub VMC Interni On'])


def k0100(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni')], ['on'])


def k0101(c, V):
    return C.trigger(V, ['Opzioni Sub VMC Interni Off'])


def k0102(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_sensori_vmc_interni')], ['off'])


def k0103(c, V):
    return C.trigger(V, ['Opzioni Sub Programmazione Giornaliera On'])


def k0104(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_calendario')], ['on'])


def k0105(c, V):
    return C.trigger(V, ['Opzioni Sub Programmazione Giornaliera Off'])


def k0106(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_interruttore_calendario')], ['off'])


def k0107(c, V):
    return C.trigger(V, [' Opzioni On'])


def k0108(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_offset_sensori')], ['on'])


def k0109(c, V):
    return C.trigger(V, ['Opzioni Off'])


def k0110(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_offset_sensori')], ['off'])


def k0111(c, V):
    return C.trigger(V, ['Opzioni Sub Lim. Δ P. di Rugiada On'])


def k0112(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada')], ['on'])


def k0113(c, V):
    return C.trigger(V, ['Opzioni Sub Lim. Δ P. di Rugiada Off'])


def k0114(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_punto_di_rugiada')], ['off'])


def k0115(c, V):
    return C.trigger(V, ['Opzioni Sub Calendario Main On'])


def k0116(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_calendario_main')], ['on'])


def k0117(c, V):
    return C.trigger(V, ['Opzioni Sub Calendario Main Off'])


def k0118(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_calendario_main')], ['off'])


def k0119(c, V):
    return C.trigger(V, ['Opzioni Sub Calendario On'])


def k0120(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_calendario')], ['on'])


def k0121(c, V):
    return C.trigger(V, ['Opzioni Sub Calendario Off'])


def k0122(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_calendario')], ['off'])


def k0123(c, V):
    return C.trigger(V, ['Opzioni Sub Calendario Free H/C On'])


def k0124(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling')], ['on'])


def k0125(c, V):
    return C.trigger(V, ['Opzioni Sub Calendario Free H/C Off'])


def k0126(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_free_heating_o_free_cooling')], ['off'])


def k0127(c, V):
    return C.trigger(V, ['Opzioni Avvisi On'])


def k0128(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_avvisi')], ['on'])


def k0129(c, V):
    return C.trigger(V, ['Opzioni Avvisi Off'])


def k0130(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_avvisi')], ['off'])


def k0131(c, V):
    return C.trigger(V, ['Opzioni Informazioni On'])


def k0132(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_lettura_sensori')], ['on'])


def k0133(c, V):
    return C.trigger(V, ['Opzioni Informazioni Off'])


def k0134(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_lettura_sensori')], ['off'])


def k0135(c, V):
    return C.modello(c, M.m0417, V)


def k0136(c, V):
    return C.modello(c, M.m0418, V)


def k0137(c, V):
    return C.modello(c, M.m0420, V)


def k0138(c, V):
    return C.modello(c, M.m0421, V)


def k0139(c, V):
    return C.trigger(V, ['PdR Vel. 1-> Imposta Velocità 0'])


def k0140(c, V):
    return C.modello(c, M.m0422, V)


def k0141(c, V):
    return C.trigger(V, ['PdR Vel. 2-> Imposta Velocità 0'])


def k0142(c, V):
    return C.modello(c, M.m0423, V)


def k0143(c, V):
    return C.trigger(V, ['PdR Vel. 3-> Imposta Velocità 0'])


def k0144(c, V):
    return C.modello(c, M.m0424, V)


def k0145(c, V):
    return C.trigger(V, ['PdR Vel. 4-> Imposta Velocità 0'])


def k0146(c, V):
    return C.modello(c, M.m0425, V)


def k0147(c, V):
    return C.trigger(V, ['PdR Notturna -> Imposta Velocità 0'])


def k0148(c, V):
    return C.trigger(V, ['PdR Free-Cooling -> Imposta Velocità 0', 'PdR Spia Free Heating OFF e Spia FreeCooling ON -> Imposta Velocità 0', 'PdR Spia Free Heating ON e Spia FreeCooling OFF -> Imposta Velocità 0'])


def k0149(c, V):
    return C.modello(c, M.m0426, V)


def k0150(c, V):
    return C.trigger(V, ['PdR Iperventilazione -> Imposta Velocità 0'])


def k0151(c, V):
    return C.modello(c, M.m0427, V)


def k0152(c, V):
    return C.modello(c, M.m0429, V)


def k0153(c, V):
    return C.modello(c, M.m0430, V)


def k0154(c, V):
    return C.modello(c, M.m0431, V)


def k0155(c, V):
    return C.modello(c, M.m0432, V)


def k0156(c, V):
    return C.modello(c, M.m0433, V)


def k0157(c, V):
    return C.trigger(V, ['PdR Vel. 1 se Spia Inquinanti ON'])


def k0158(c, V):
    return C.modello(c, M.m0434, V)


def k0159(c, V):
    return C.modello(c, M.m0436, V)


def k0160(c, V):
    return C.trigger(V, ['PdR Vel. 2 se Spia Inquinanti ON'])


def k0161(c, V):
    return C.modello(c, M.m0437, V)


def k0162(c, V):
    return C.modello(c, M.m0439, V)


def k0163(c, V):
    return C.trigger(V, ['PdR Vel. 3 se Spia Inquinanti ON'])


def k0164(c, V):
    return C.modello(c, M.m0440, V)


def k0165(c, V):
    return C.modello(c, M.m0442, V)


def k0166(c, V):
    return C.trigger(V, ['PdR Vel. 4 se Spia Inquinanti ON'])


def k0167(c, V):
    return C.modello(c, M.m0443, V)


def k0168(c, V):
    return C.modello(c, M.m0445, V)


def k0169(c, V):
    return C.trigger(V, ['PdR Notturna se Spia Inquinanti ON'])


def k0170(c, V):
    return C.modello(c, M.m0446, V)


def k0171(c, V):
    return C.modello(c, M.m0447, V)


def k0172(c, V):
    return C.modello(c, M.m0448, V)


def k0173(c, V):
    return C.modello(c, M.m0450, V)


def k0174(c, V):
    return C.modello(c, M.m0451, V)


def k0175(c, V):
    return C.modello(c, M.m0452, V)


def k0176(c, V):
    return C.modello(c, M.m0453, V)


def k0177(c, V):
    return C.trigger(V, ['PdR Free-Cooling se Spia Inquinanti ON', 'PdR Spia Free Heating OFF e Spia FreeCooling ON -> Imposta Velocità 1 se Spia Inquinanti ON', 'PdR Spia Free Heating ON e Spia FreeCooling OFF -> Imposta Velocità 1 se Spia Inquinanti ON'])


def k0178(c, V):
    return C.modello(c, M.m0454, V)


def k0179(c, V):
    return C.modello(c, M.m0456, V)


def k0180(c, V):
    return C.trigger(V, ['PdR Iperventilazione se Spia Inquinanti ON'])


def k0181(c, V):
    return C.trigger(V, ['PdR Vel. 0 -> Spia PdR Velocità 0'])


def k0182(c, V):
    return C.modello(c, M.m0457, V)


def k0183(c, V):
    return C.modello(c, M.m0458, V)


def k0184(c, V):
    return C.trigger(V, ['Rip. Vel. 0 No PdR -> Spia PdR Velocità 0 OFF'])


def k0185(c, V):
    return C.modello(c, M.m0459, V)


def k0186(c, V):
    return C.trigger(V, ['Inquinanti con Spia PdR Velocità 0 -> Spia PdR Velocità 0 OFF'])


def k0187(c, V):
    return C.modello(c, M.m0460, V)


def k0188(c, V):
    return C.trigger(V, ['Rip. Vel. 0 No PdR'])


def k0189(c, V):
    return C.modello(c, M.m0461, V)


def k0190(c, V):
    return C.modello(c, M.m0462, V)


def k0191(c, V):
    return C.trigger(V, ['Rip. Vel. 1 No PdR'])


def k0192(c, V):
    return C.modello(c, M.m0463, V)


def k0193(c, V):
    return C.modello(c, M.m0464, V)


def k0194(c, V):
    return C.modello(c, M.m0465, V)


def k0195(c, V):
    return C.trigger(V, ['Rip. Vel. 2 No PdR'])


def k0196(c, V):
    return C.modello(c, M.m0466, V)


def k0197(c, V):
    return C.modello(c, M.m0467, V)


def k0198(c, V):
    return C.trigger(V, ['Rip. Vel. 3 No PdR'])


def k0199(c, V):
    return C.modello(c, M.m0468, V)


def k0200(c, V):
    return C.modello(c, M.m0469, V)


def k0201(c, V):
    return C.trigger(V, ['Rip. Vel. 4 No PdR'])


def k0202(c, V):
    return C.modello(c, M.m0470, V)


def k0203(c, V):
    return C.modello(c, M.m0471, V)


def k0204(c, V):
    return C.trigger(V, ['Rip. Notturno No PdR'])


def k0205(c, V):
    return C.modello(c, M.m0472, V)


def k0206(c, V):
    return C.modello(c, M.m0473, V)


def k0207(c, V):
    return C.modello(c, M.m0474, V)


def k0208(c, V):
    return C.modello(c, M.m0475, V)


def k0209(c, V):
    return C.modello(c, M.m0476, V)


def k0210(c, V):
    return C.modello(c, M.m0478, V)


def k0211(c, V):
    return C.modello(c, M.m0482, V)


def k0212(c, V):
    return C.trigger(V, ['Rip. Free Cool./Heat. No PdR'])


def k0213(c, V):
    return C.modello(c, M.m0483, V)


def k0214(c, V):
    return C.modello(c, M.m0484, V)


def k0215(c, V):
    return C.trigger(V, ['Rip. Iperventilazione No PdR'])


def k0216(c, V):
    return C.modello(c, M.m0485, V)


def k0217(c, V):
    return C.trigger(V, ['Rip. Vel. 1 No PdR se Spia Inquinanti ON'])


def k0218(c, V):
    return C.modello(c, M.m0486, V)


def k0219(c, V):
    return C.trigger(V, ['Rip. Vel. 2 No PdR se Spia Inquinanti ON'])


def k0220(c, V):
    return C.modello(c, M.m0487, V)


def k0221(c, V):
    return C.trigger(V, ['Rip. Vel. 3 No PdR  se Spia Inquinanti ON'])


def k0222(c, V):
    return C.modello(c, M.m0488, V)


def k0223(c, V):
    return C.trigger(V, ['Rip. Vel. 4 No PdR se Spia Inquinanti ON'])


def k0224(c, V):
    return C.modello(c, M.m0489, V)


def k0225(c, V):
    return C.trigger(V, ['Rip. Notturno No PdR se Spia Inquinanti ON'])


def k0226(c, V):
    return C.modello(c, M.m0490, V)


def k0227(c, V):
    return C.modello(c, M.m0491, V)


def k0228(c, V):
    return C.modello(c, M.m0492, V)


def k0229(c, V):
    return C.modello(c, M.m0493, V)


def k0230(c, V):
    return C.modello(c, M.m0494, V)


def k0231(c, V):
    return C.modello(c, M.m0495, V)


def k0232(c, V):
    return C.modello(c, M.m0496, V)


def k0233(c, V):
    return C.trigger(V, ['Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON'])


def k0234(c, V):
    return C.modello(c, M.m0497, V)


def k0235(c, V):
    return C.trigger(V, ['Rip. Iperventilazione No PdR se Spia Inquinanti ON'])


def k0236(c, V):
    return C.modello(c, M.m0498, V)


def k0237(c, V):
    return C.modello(c, M.m0499, V)


def k0238(c, V):
    return C.modello(c, M.m0500, V)


def k0239(c, V):
    return C.trigger(V, [' Disattivazione Lim. Δ P. di Rugiada, precedentemente Armato ed Attivato'])


def k0240(c, V):
    return C.trigger(V, [' Disattivazione Lim. Δ P. di Rugiada, precedentemente Armato ed Attivato e Spia Inquinanti ON'])


def k0241(c, V):
    return C.modello(c, M.m0501, V)


def k0242(c, V):
    return C.trigger(V, [' Disattivazione Lim. Δ P. di Rugiada, precedentemente Armato ed Attivato', ' Disattivazione Lim. Δ P. di Rugiada, precedentemente Armato ed Attivato e Spia Inquinanti ON'])


def k0243(c, V):
    return C.modello(c, M.m0502, V)


def k0244(c, V):
    return C.modello(c, M.m0503, V)


def k0245(c, V):
    return C.modello(c, M.m0504, V)


def k0246(c, V):
    return C.modello(c, M.m0505, V)


def k0247(c, V):
    return C.modello(c, M.m0507, V)


def k0248(c, V):
    return C.trigger(V, ['TeVsTi Free-Heating -> Imposta Velocità 0'])


def k0249(c, V):
    return C.trigger(V, ['TeVsTi Free-Heating e Spia Inquinanti ON'])


def k0250(c, V):
    return C.trigger(V, ['TeVsTi Free-Cooling -> Imposta Velocità 0'])


def k0251(c, V):
    return C.modello(c, M.m0508, V)


def k0252(c, V):
    return C.modello(c, M.m0509, V)


def k0253(c, V):
    return C.trigger(V, ['TeVsTi Free-Cooling e Spia Inquinanti ON'])


def k0254(c, V):
    return C.modello(c, M.m0510, V)


def k0255(c, V):
    return C.trigger(V, ['Rip. Free Cooling No TeVsTi '])


def k0256(c, V):
    return C.trigger(V, ['Rip. Free Heating No TeVsTi '])


def k0257(c, V):
    return C.modello(c, M.m0511, V)


def k0258(c, V):
    return C.trigger(V, ['Rip. Free Heating No TeVsTi e Spia Inquinanti ON'])


def k0259(c, V):
    return C.modello(c, M.m0512, V)


def k0260(c, V):
    return C.trigger(V, ['Rip. Free Cooling No TeVsTi e Spia Inquinanti ON'])


def k0261(c, V):
    return C.modello(c, M.m0518, V)


def k0262(c, V):
    return C.modello(c, M.m0520, V)


def k0263(c, V):
    return C.modello(c, M.m0522, V)


def k0264(c, V):
    return C.modello(c, M.m0525, V)


def k0265(c, V):
    return C.modello(c, M.m0526, V)


def k0266(c, V):
    return C.trigger(V, ['Disattivazione VMC ON/OFF, in Funzione della Vel. Free Heating precedentemente Armato'])


def k0267(c, V):
    return C.trigger(V, [' Disattivazione VMC ON/OFF, in Funzione della Vel. Free Heating precedentemente Armato e Spia Inquinanti ON'])


def k0268(c, V):
    return C.modello(c, M.m0528, V)


def k0269(c, V):
    return C.trigger(V, ['Disattivazione VMC ON/OFF, in Funzione della Vel. Free Cooling precedentemente Armato'])


def k0270(c, V):
    return C.trigger(V, [' Disattivazione VMC ON/OFF, in Funzione della Vel. Free Cooling precedentemente Armato e Spia Inquinanti ON'])


def k0271(c, V):
    return C.trigger(V, [' Disattivazione VMC per Inquinanti CO2 e/o VOC, precedentemente Armato ed Attivato'])


def k0272(c, V):
    return C.modello(c, M.m0529, V)


def k0273(c, V):
    return C.modello(c, M.m0530, V)


def k0274(c, V):
    return C.modello(c, M.m0531, V)


def k0275(c, V):
    return C.trigger(V, ['Calendario Off tra Fascie e Spia Inquinanti ON'])


def k0276(c, V):
    return C.modello(c, M.m0532, V)


def k0277(c, V):
    return C.modello(c, M.m0533, V)


def k0278(c, V):
    return C.modello(c, M.m0534, V)


def k0279(c, V):
    return C.trigger(V, ['Calendario Off tra Fascie'])


def k0280(c, V):
    return C.modello(c, M.m0535, V)


def k0281(c, V):
    return C.trigger(V, [' Disattivazione Umidità Limite, precedentemente Armato ed Attivato'])


def k0282(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita')], ['off'])


def k0283(c, V):
    return C.modello(c, M.m0536, V)


def k0284(c, V):
    return C.modello(c, M.m0537, V)


def k0285(c, V):
    return C.modello(c, M.m0538, V)


def k0286(c, V):
    return C.modello(c, M.m0539, V)


def k0287(c, V):
    return C.trigger(V, ['Black-Out a Velocità 0'])


def k0288(c, V):
    return C.modello(c, M.m0540, V)


def k0289(c, V):
    return C.modello(c, M.m0541, V)


def k0290(c, V):
    return C.trigger(V, ['Black-Out Scelta Vel. 1'])


def k0291(c, V):
    return C.modello(c, M.m0542, V)


def k0292(c, V):
    return C.modello(c, M.m0543, V)


def k0293(c, V):
    return C.modello(c, M.m0544, V)


def k0294(c, V):
    return C.modello(c, M.m0545, V)


def k0295(c, V):
    return C.modello(c, M.m0546, V)


def k0296(c, V):
    return C.modello(c, M.m0547, V)


def k0297(c, V):
    return C.modello(c, M.m0548, V)


def k0298(c, V):
    return C.modello(c, M.m0549, V)


def k0299(c, V):
    return C.modello(c, M.m0550, V)


def k0300(c, V):
    return C.modello(c, M.m0551, V)


def k0301(c, V):
    return C.modello(c, M.m0552, V)


def k0302(c, V):
    return C.modello(c, M.m0553, V)


def k0303(c, V):
    return C.modello(c, M.m0554, V)


def k0304(c, V):
    return C.modello(c, M.m0555, V)


def k0305(c, V):
    return C.modello(c, M.m0556, V)


def k0306(c, V):
    return C.modello(c, M.m0557, V)


def k0307(c, V):
    return C.modello(c, M.m0558, V)


def k0308(c, V):
    return C.modello(c, M.m0559, V)


def k0309(c, V):
    return C.modello(c, M.m0560, V)


def k0310(c, V):
    return C.modello(c, M.m0561, V)


def k0311(c, V):
    return C.modello(c, M.m0562, V)


def k0312(c, V):
    return C.modello(c, M.m0563, V)


def k0313(c, V):
    return C.modello(c, M.m0565, V)


def k0314(c, V):
    return C.trigger(V, ['Black-Out Off Vel. 0'])


def k0315(c, V):
    return C.trigger(V, ['Black-Out a Velocità 1', 'Black-Out a Velocità 1 caso [SPIE INQUINANTI OFF] e [SPIE FREECOOLING ON o FREEHEATING ON o MEMORIE INQUINANTI ON]'])


def k0316(c, V):
    return C.trigger(V, ['Black-Out a Velocità 1 caso [SPIE INQUINANTI ON] e [SPIE FREECOOLING ON o FREEHEAING ON]'])


def k0317(c, V):
    return C.modello(c, M.m0566, V)


def k0318(c, V):
    return C.trigger(V, ['Black-Out a Velocità 1 caso [SPIE INQUINANTI ON] e [SPIE FREECOOLING OFF e FREEHEAING OFF]'])


def k0319(c, V):
    return C.trigger(V, ['Black-Out Off Vel. 1'])


def k0320(c, V):
    return C.trigger(V, ['Black-Out a Velocità 2'])


def k0321(c, V):
    return C.trigger(V, ['Black-Out Off Vel. 2'])


def k0322(c, V):
    return C.trigger(V, ['Black-Out a Velocità 3'])


def k0323(c, V):
    return C.trigger(V, ['Black-Out Off Vel. 3'])


def k0324(c, V):
    return C.trigger(V, ['Black-Out a Velocità 4'])


def k0325(c, V):
    return C.trigger(V, ['Black-Out Off Vel. 4'])


def k0326(c, V):
    return C.trigger(V, ['Black-Out Notturna'])


def k0327(c, V):
    return C.trigger(V, ['Black-Out Off Notturna'])


def k0328(c, V):
    return C.trigger(V, ['Black-Out Iperventilazione'])


def k0329(c, V):
    return C.trigger(V, ['Black-Out Off Iperventilazione'])


def k0330(c, V):
    return C.trigger(V, ['Black-Out Free Cool./Heat.'])


def k0331(c, V):
    return C.modello(c, M.m0567, V)


def k0332(c, V):
    return C.modello(c, M.m0568, V)


def k0333(c, V):
    return C.modello(c, M.m0569, V)


def k0334(c, V):
    return C.modello(c, M.m0570, V)


def k0335(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_spia_co2_o_voc')], ['on'])


def k0336(c, V):
    return C.trigger(V, ['Black-Out Off Free Cool./Heat.'])


def k0337(c, V):
    return C.trigger(V, ['calendario_black_out_memoria'])


def k0338(c, V):
    return C.modello(c, M.m0571, V)


def k0339(c, V):
    return C.modello(c, M.m0572, V)


def k0340(c, V):
    return C.modello(c, M.m0573, V)


def k0341(c, V):
    return C.modello(c, M.m0574, V)


def k0342(c, V):
    return C.trigger(V, ['calendario_ritorno_da_black_out'])


def k0343(c, V):
    return C.modello(c, M.m0575, V)


def k0344(c, V):
    return C.trigger(V, ['calendario_ritorno_da_black_out_riallineamento'])


def k0345(c, V):
    return C.modello(c, M.m0576, V)


def k0346(c, V):
    return C.modello(c, M.m0578, V)


def k0347(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario')], ['on'])


def k0348(c, V):
    return C.modello(c, M.m0580, V)


def k0349(c, V):
    return C.modello(c, M.m0581, V)


def k0350(c, V):
    return C.modello(c, M.m0582, V)


def k0351(c, V):
    return C.modello(c, M.m0583, V)


def k0352(c, V):
    return C.modello(c, M.m0584, V)


def k0353(c, V):
    return C.trigger(V, ['calendario_ritorno_comando'])


def k0354(c, V):
    return C.modello(c, M.m0589, V)


def k0355(c, V):
    return C.modello(c, M.m0590, V)


def k0356(c, V):
    return C.modello(c, M.m0592, V)


def k0357(c, V):
    return C.trigger(V, ['comando_non_eseguito_ritorno'])


def k0358(c, V):
    return C.trigger(V, ['1° Lunedì On'])


def k0359(c, V):
    return C.modello(c, M.m0594, V)


def k0360(c, V):
    return C.modello(c, M.m0595, V)


def k0361(c, V):
    return C.trigger(V, ['1° Lunedì Off'])


def k0362(c, V):
    return C.trigger(V, ['2° Lunedì On'])


def k0363(c, V):
    return C.trigger(V, ['2° Lunedì Off'])


def k0364(c, V):
    return C.trigger(V, ['1° Martedì On'])


def k0365(c, V):
    return C.modello(c, M.m0596, V)


def k0366(c, V):
    return C.trigger(V, ['1° Martedì Off'])


def k0367(c, V):
    return C.trigger(V, ['2° Martedì On'])


def k0368(c, V):
    return C.trigger(V, ['2° Martedì Off'])


def k0369(c, V):
    return C.trigger(V, ['1° Mercoledì On'])


def k0370(c, V):
    return C.modello(c, M.m0597, V)


def k0371(c, V):
    return C.trigger(V, ['1° Mercoledì Off'])


def k0372(c, V):
    return C.trigger(V, ['2° Mercoledì On'])


def k0373(c, V):
    return C.trigger(V, ['2° Mercoledì Off'])


def k0374(c, V):
    return C.trigger(V, ['1° Giovedì On'])


def k0375(c, V):
    return C.modello(c, M.m0598, V)


def k0376(c, V):
    return C.trigger(V, ['1° Giovedì Off'])


def k0377(c, V):
    return C.trigger(V, ['2° Giovedì On'])


def k0378(c, V):
    return C.trigger(V, ['2° Giovedì Off'])


def k0379(c, V):
    return C.trigger(V, ['1° Venerdì On'])


def k0380(c, V):
    return C.modello(c, M.m0599, V)


def k0381(c, V):
    return C.trigger(V, ['1° Venerdì Off'])


def k0382(c, V):
    return C.trigger(V, ['2° Venerdì On'])


def k0383(c, V):
    return C.trigger(V, ['2° Venerdì Off'])


def k0384(c, V):
    return C.trigger(V, ['1° Sabato On'])


def k0385(c, V):
    return C.modello(c, M.m0600, V)


def k0386(c, V):
    return C.trigger(V, ['1° Sabato Off'])


def k0387(c, V):
    return C.trigger(V, ['2° Sabato On'])


def k0388(c, V):
    return C.trigger(V, ['2° Sabato Off'])


def k0389(c, V):
    return C.trigger(V, ['1° Domenica On'])


def k0390(c, V):
    return C.modello(c, M.m0601, V)


def k0391(c, V):
    return C.trigger(V, ['1° Domenica Off'])


def k0392(c, V):
    return C.trigger(V, ['2° Domenica On'])


def k0393(c, V):
    return C.trigger(V, ['2° Domenica Off'])


def k0394(c, V):
    return C.trigger(V, ['Cambio Nome VMC'])


def k0395(c, V):
    return C.modello(c, M.m0602, V)


def k0396(c, V):
    return C.trigger(V, ['Spia Avvisi On'])


def k0397(c, V):
    return C.trigger(V, ['Spia Avvisi Off'])


def k0398(c, V):
    return C.trigger(V, ['Repository Update ON'])


def k0399(c, V):
    return C.trigger(V, ['Repository Update OFF'])


def k0400(c, V):
    return C.modello(c, M.m0603, V)


def k0401(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr')], ['on'])


def k0402(c, V):
    return C.modello(c, M.m0604, V)


def k0403(c, V):
    return C.modello(c, M.m0605, V)


def k0404(c, V):
    return C.modello(c, M.m0606, V)


def k0405(c, V):
    return C.modello(c, M.m0607, V)


def k0406(c, V):
    return C.modello(c, M.m0608, V)


def k0407(c, V):
    return C.modello(c, M.m0609, V)


def k0408(c, V):
    return C.modello(c, M.m0610, V)


def k0409(c, V):
    return C.modello(c, M.m0611, V)


def k0410(c, V):
    return C.modello(c, M.m0612, V)


def k0411(c, V):
    return C.modello(c, M.m0613, V)


def k0412(c, V):
    return C.modello(c, M.m0614, V)


def k0413(c, V):
    return C.modello(c, M.m0615, V)


def k0414(c, V):
    return C.modello(c, M.m0616, V)


def k0415(c, V):
    return C.modello(c, M.m0617, V)


def k0416(c, V):
    return C.modello(c, M.m0618, V)


def k0417(c, V):
    return C.modello(c, M.m0619, V)


def k0418(c, V):
    return C.modello(c, M.m0620, V)


def k0419(c, V):
    return C.modello(c, M.m0621, V)


def k0420(c, V):
    return C.modello(c, M.m0622, V)


def k0421(c, V):
    return C.modello(c, M.m0623, V)


def k0422(c, V):
    return C.modello(c, M.m0624, V)


def k0423(c, V):
    return C.trigger(V, ['inquinanti_co2_voc_on'])


def k0424(c, V):
    return C.modello(c, M.m0626, V)


def k0425(c, V):
    return C.modello(c, M.m0627, V)


def k0426(c, V):
    return C.modello(c, M.m0628, V)


def k0427(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_spia_velocita_1_delta_temp_verifica_soglia_valore')], ['on'])


def k0428(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_spia_velocita_1_congelamento')], ['on'])


def k0429(c, V):
    return C.modello(c, M.m0629, V)


def k0430(c, V):
    return C.modello(c, M.m0630, V)


def k0431(c, V):
    return C.modello(c, M.m0631, V)


def k0432(c, V):
    return C.modello(c, M.m0632, V)


def k0433(c, V):
    return C.modello(c, M.m0633, V)


def k0434(c, V):
    return C.modello(c, M.m0634, V)


def k0435(c, V):
    return C.modello(c, M.m0635, V)


def k0436(c, V):
    return C.modello(c, M.m0636, V)


def k0437(c, V):
    return C.modello(c, M.m0637, V)


def k0438(c, V):
    return C.modello(c, M.m0638, V)


def k0439(c, V):
    return C.modello(c, M.m0640, V)


def k0440(c, V):
    return C.modello(c, M.m0642, V)


def k0441(c, V):
    return C.trigger(V, ['inquinanti_co2_voc_off'])


def k0442(c, V):
    return C.modello(c, M.m0643, V)


def k0443(c, V):
    return C.modello(c, M.m0644, V)


def k0444(c, V):
    return C.e(c, V, (k0442, k0443, ))


def k0445(c, V):
    return C.modello(c, M.m0645, V)


def k0446(c, V):
    return C.modello(c, M.m0646, V)


def k0447(c, V):
    return C.e(c, V, (k0443, k0445, k0446, ))


def k0448(c, V):
    return C.modello(c, M.m0647, V)


def k0449(c, V):
    return C.modello(c, M.m0648, V)


def k0450(c, V):
    return C.modello(c, M.m0649, V)


def k0451(c, V):
    return C.modello(c, M.m0650, V)


def k0452(c, V):
    return C.modello(c, M.m0651, V)


def k0453(c, V):
    return C.modello(c, M.m0652, V)


def k0454(c, V):
    return C.modello(c, M.m0653, V)


def k0455(c, V):
    return C.modello(c, M.m0654, V)


def k0456(c, V):
    return C.modello(c, M.m0655, V)


def k0457(c, V):
    return C.modello(c, M.m0656, V)


def k0458(c, V):
    return C.modello(c, M.m0657, V)


def k0459(c, V):
    return C.modello(c, M.m0658, V)


def k0460(c, V):
    return C.modello(c, M.m0659, V)


def k0461(c, V):
    return C.modello(c, M.m0660, V)


def k0462(c, V):
    return C.modello(c, M.m0661, V)


def k0463(c, V):
    return C.modello(c, M.m0662, V)


def k0464(c, V):
    return C.modello(c, M.m0663, V)


def k0465(c, V):
    return C.trigger(V, ['spia_velocita_0_inquinanti_co2_voc'])


def k0466(c, V):
    return C.modello(c, M.m0664, V)


def k0467(c, V):
    return C.modello(c, M.m0665, V)


def k0468(c, V):
    return C.modello(c, M.m0666, V)


def k0469(c, V):
    return C.modello(c, M.m0667, V)


def k0470(c, V):
    return C.modello(c, M.m0668, V)


def k0471(c, V):
    return C.modello(c, M.m0669, V)


def k0472(c, V):
    return C.modello(c, M.m0670, V)


def k0473(c, V):
    return C.trigger(V, ['spia_velocita_1_inquinanti_co2_voc'])


def k0474(c, V):
    return C.modello(c, M.m0671, V)


def k0475(c, V):
    return C.trigger(V, ['spia_velocita_2_inquinanti_co2_voc'])


def k0476(c, V):
    return C.modello(c, M.m0672, V)


def k0477(c, V):
    return C.trigger(V, ['spia_velocita_3_inquinanti_co2_voc'])


def k0478(c, V):
    return C.modello(c, M.m0673, V)


def k0479(c, V):
    return C.trigger(V, ['spia_velocita_4_inquinanti_co2_voc'])


def k0480(c, V):
    return C.modello(c, M.m0674, V)


def k0481(c, V):
    return C.trigger(V, ['spia_velocita_notturna_inquinanti_co2_voc'])


def k0482(c, V):
    return C.modello(c, M.m0675, V)


def k0483(c, V):
    return C.trigger(V, ['spia_velocita_iperventilazione_inquinanti_co2_voc'])


def k0484(c, V):
    return C.modello(c, M.m0676, V)


def k0485(c, V):
    return C.modello(c, M.m0677, V)


def k0486(c, V):
    return C.trigger(V, ['spia_velocita_freecooling_inquinanti_co2_voc'])


def k0487(c, V):
    return C.modello(c, M.m0678, V)


def k0488(c, V):
    return C.modello(c, M.m0679, V)


def k0489(c, V):
    return C.trigger(V, ['spia_velocita_0_congelamento'])


def k0490(c, V):
    return C.modello(c, M.m0680, V)


def k0491(c, V):
    return C.o(c, V, (k0489, k0490, ))


def k0492(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')], ['off'])


def k0493(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0')], ['on'])


def k0494(c, V):
    return C.modello(c, M.m0681, V)


def k0495(c, V):
    return C.modello(c, M.m0682, V)


def k0496(c, V):
    return C.e(c, V, (k0494, k0495, ))


def k0497(c, V):
    return C.modello(c, M.m0683, V)


def k0498(c, V):
    return C.e(c, V, (k0494, k0497, ))


def k0499(c, V):
    return C.modello(c, M.m0684, V)


def k0500(c, V):
    return C.e(c, V, (k0499, k0495, ))


def k0501(c, V):
    return C.e(c, V, (k0499, k0497, ))


def k0502(c, V):
    return C.modello(c, M.m0685, V)


def k0503(c, V):
    return C.modello(c, M.m0686, V)


def k0504(c, V):
    return C.trigger(V, ['spia_velocita_1_congelamento'])


def k0505(c, V):
    return C.modello(c, M.m0687, V)


def k0506(c, V):
    return C.o(c, V, (k0504, k0505, ))


def k0507(c, V):
    return C.trigger(V, ['spia_velocita_2_congelamento'])


def k0508(c, V):
    return C.modello(c, M.m0688, V)


def k0509(c, V):
    return C.o(c, V, (k0507, k0508, ))


def k0510(c, V):
    return C.trigger(V, ['spia_velocita_3_congelamento'])


def k0511(c, V):
    return C.modello(c, M.m0689, V)


def k0512(c, V):
    return C.o(c, V, (k0510, k0511, ))


def k0513(c, V):
    return C.trigger(V, ['spia_velocita_4_congelamento'])


def k0514(c, V):
    return C.modello(c, M.m0690, V)


def k0515(c, V):
    return C.o(c, V, (k0513, k0514, ))


def k0516(c, V):
    return C.trigger(V, ['spia_velocita_iperventilazione_congelamento'])


def k0517(c, V):
    return C.modello(c, M.m0691, V)


def k0518(c, V):
    return C.o(c, V, (k0516, k0517, ))


def k0519(c, V):
    return C.trigger(V, ['spia_velocita_notturna_congelamento'])


def k0520(c, V):
    return C.modello(c, M.m0692, V)


def k0521(c, V):
    return C.o(c, V, (k0519, k0520, ))


def k0522(c, V):
    return C.trigger(V, ['spia_velocita_Free Cooling_congelamento'])


def k0523(c, V):
    return C.modello(c, M.m0693, V)


def k0524(c, V):
    return C.o(c, V, (k0522, k0523, ))


def k0525(c, V):
    return C.trigger(V, ['Congelamento ON'])


def k0526(c, V):
    return C.o(c, V, (k0525, k0489, k0504, k0507, k0510, k0513, k0516, k0519, k0522, ))


def k0527(c, V):
    return C.modello(c, M.m0694, V)


def k0528(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_spia_calendario_comando_non_eseguito')], ['on'])


def k0529(c, V):
    return C.modello(c, M.m0695, V)


def k0530(c, V):
    return C.modello(c, M.m0696, V)


def k0531(c, V):
    return C.modello(c, M.m0697, V)


def k0532(c, V):
    return C.modello(c, M.m0698, V)


def k0533(c, V):
    return C.modello(c, M.m0699, V)


def k0534(c, V):
    return C.modello(c, M.m0700, V)


def k0535(c, V):
    return C.modello(c, M.m0701, V)


def k0536(c, V):
    return C.modello(c, M.m0702, V)


def k0537(c, V):
    return C.modello(c, M.m0703, V)


def k0538(c, V):
    return C.modello(c, M.m0704, V)


def k0539(c, V):
    return C.modello(c, M.m0705, V)


def k0540(c, V):
    return C.modello(c, M.m0706, V)


def k0541(c, V):
    return C.modello(c, M.m0707, V)


def k0542(c, V):
    return C.modello(c, M.m0708, V)


def k0543(c, V):
    return C.modello(c, M.m0709, V)


def k0544(c, V):
    return C.modello(c, M.m0710, V)


def k0545(c, V):
    return C.trigger(V, ['Congelamento OFF'])


def k0546(c, V):
    return C.modello(c, M.m0711, V)


def k0547(c, V):
    return C.modello(c, M.m0712, V)


def k0548(c, V):
    return C.trigger(V, ['Cambio Velocità quanto Spia FreeHeating o FreeCooling è ON - Inquinanti OFF'])


def k0549(c, V):
    return C.trigger(V, ['PdR Vel. 0 con Spia FreeHeating On -> Imposta Velocità 0'])


def k0550(c, V):
    return C.trigger(V, ['PdR Vel. 0 con Spia FreeCooling On -> Imposta Velocità 0'])


def k0551(c, V):
    return C.modello(c, M.m0713, V)


def k0552(c, V):
    return C.modello(c, M.m0714, V)


def k0553(c, V):
    return C.trigger(V, ['PdR Vel. 0 con Spia FreeHeating On e Inquinanti Vel. 1 ON  -> Imposta Velocità 1'])


def k0554(c, V):
    return C.modello(c, M.m0715, V)


def k0555(c, V):
    return C.modello(c, M.m0716, V)


def k0556(c, V):
    return C.trigger(V, ['PdR Vel. 0 con Spia FreeCooling On e Inquinanti Vel. 1 ON  -> Imposta Velocità 1'])


def k0557(c, V):
    return C.trigger(V, [c.N('VMC Master Elenco Entità Temperatura e Umidità installate in H.A.'), c.N('VMC Master Elenco Entità con VMC di nuovo ON-Line'), c.N('VMC Master Elenco Entità con Invio Notifica acceso')])


def k0558(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected Temperatura Esterna Entity')])


def k0559(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected Temperatura Interna Entity')])


def k0560(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected Umidità Esterna Entity')])


def k0561(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected Umidità Interna Entity')])


def k0562(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected CO2 Interna Entity')])


def k0563(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected Dispositivo Interna Entity')])


def k0564(c, V):
    return C.trigger(V, [c.N('VMC Master Save Selected Media Player Interna Entity')])


def k0565(c, V):
    return C.trigger(V, ['Opzioni Sub Sensori Opzionati On'])


def k0566(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_scelta_sensori')], ['on'])


def k0567(c, V):
    return C.trigger(V, ['Opzioni Sub Sensori Opzionati Off'])


def k0568(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_scelta_sensori')], ['off'])


def k0569(c, V):
    return C.trigger(V, ['Opzioni Sub Elementi Chimici On'])


def k0570(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_elementi_chimici')], ['on'])


def k0571(c, V):
    return C.trigger(V, ['Opzioni Sub Elementi Chimici Off'])


def k0572(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzioni_elementi_chimici')], ['off'])


def k0573(c, V):
    return C.trigger(V, ['Opzioni Sub Elementi Audio On'])


def k0574(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzione_finestra_audio')], ['on'])


def k0575(c, V):
    return C.trigger(V, ['Opzioni Sub Elementi Audio Off'])


def k0576(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_opzione_finestra_audio')], ['off'])


def k0577(c, V):
    return C.trigger(V, ['Opzioni Sub Conferma Pulizia On'])


def k0578(c, V):
    return C.stato(c, V, [c.N('input_boolean.vmc_master_conferma_pulizia_cronologia')], ['on'])


def k0579(c, V):
    return C.trigger(V, ['Entità Temperatura Esterna Errore [Interfaccia]'])


def k0580(c, V):
    return C.trigger(V, ['Entità Temperatura Interna Errore [Interfaccia]'])


def k0581(c, V):
    return C.trigger(V, ['Entità Umidità Esterna Errore [Interfaccia]'])


def k0582(c, V):
    return C.trigger(V, ['Entità Umidità Interna Errore [Interfaccia]'])


def k0583(c, V):
    return C.trigger(V, ['Entità CO2 Interna Errore [Interfaccia]'])


def k0584(c, V):
    return C.trigger(V, ['Dispositivo Notifica Errore [Interfaccia]'])


def k0585(c, V):
    return C.trigger(V, ['Avviso Cambio Filtro'])


def k0586(c, V):
    return C.modello(c, M.m0729, V)


def k0587(c, V):
    return C.trigger(V, ['Avviso Cambio Filtro [Mobile]'])


def k0588(c, V):
    return C.modello(c, M.m0730, V)


def k0589(c, V):
    return C.e(c, V, (k0587, k0588, ))


def k0590(c, V):
    return C.trigger(V, ['VMC Velocità 0 da Notificare'])


def k0591(c, V):
    return C.trigger(V, ['VMC Velocità in Funzione da Notificare'])


def k0592(c, V):
    return C.trigger(V, ['Entità Temperatura Esterno Errore [Mobile]'])


def k0593(c, V):
    return C.trigger(V, ['Entità Temperatura Interna Errore [Mobile]'])


def k0594(c, V):
    return C.trigger(V, ['Entità Umidità Esterna Errore [Mobile]'])


def k0595(c, V):
    return C.trigger(V, ['Entità Umidità Interna Errore [Mobile]'])


def k0596(c, V):
    return C.trigger(V, ['Entità CO2 Interna Errore [Mobile]'])


def k0597(c, V):
    return C.trigger(V, ['pannello_avvisi_problema'])


def k0598(c, V):
    return C.modello(c, M.m0731, V)


def k0599(c, V):
    return C.modello(c, M.m0732, V)


def k0600(c, V):
    return C.modello(c, M.m0733, V)


def k0601(c, V):
    return C.modello(c, M.m0734, V)


def k0602(c, V):
    return C.modello(c, M.m0735, V)


def k0603(c, V):
    return C.modello(c, M.m0736, V)


def k0604(c, V):
    return C.modello(c, M.m0737, V)


def k0605(c, V):
    return C.modello(c, M.m0738, V)


def k0606(c, V):
    return C.modello(c, M.m0514, V)


def k0607(c, V):
    return C.modello(c, M.m0739, V)


def k0608(c, V):
    return C.modello(c, M.m0740, V)


def k0609(c, V):
    return C.modello(c, M.m0741, V)


def k0610(c, V):
    return C.modello(c, M.m0742, V)


def k0611(c, V):
    return C.modello(c, M.m0743, V)


def k0612(c, V):
    return C.modello(c, M.m0744, V)


def k0613(c, V):
    return C.modello(c, M.m0745, V)


def k0614(c, V):
    return C.modello(c, M.m0746, V)


def k0615(c, V):
    return C.modello(c, M.m0747, V)


def k0616(c, V):
    return C.trigger(V, ['spia_umidita_on'])


def k0617(c, V):
    return C.modello(c, M.m0748, V)


def k0618(c, V):
    return C.trigger(V, ['umidita_off_con_inquinanti_partenza_velocita_0'])


def k0619(c, V):
    return C.modello(c, M.m0749, V)


def k0620(c, V):
    return C.modello(c, M.m0750, V)


def k0621(c, V):
    return C.modello(c, M.m0751, V)


def k0622(c, V):
    return C.modello(c, M.m0752, V)


def k0623(c, V):
    return C.modello(c, M.m0753, V)


def k0624(c, V):
    return C.modello(c, M.m0754, V)


def k0625(c, V):
    return C.modello(c, M.m0755, V)


def k0626(c, V):
    return C.modello(c, M.m0756, V)


def k0627(c, V):
    return C.modello(c, M.m0757, V)


def k0628(c, V):
    return C.modello(c, M.m0758, V)


def k0629(c, V):
    return C.modello(c, M.m0759, V)


def k0630(c, V):
    return C.modello(c, M.m0760, V)


def k0631(c, V):
    return C.modello(c, M.m0761, V)


def k0632(c, V):
    return C.modello(c, M.m0762, V)


def k0633(c, V):
    return C.modello(c, M.m0763, V)


def k0634(c, V):
    return C.modello(c, M.m0764, V)


def k0635(c, V):
    return C.modello(c, M.m0765, V)


def k0636(c, V):
    return C.modello(c, M.m0766, V)


def k0637(c, V):
    return C.modello(c, M.m0767, V)


def k0638(c, V):
    return C.modello(c, M.m0768, V)


def k0639(c, V):
    return C.modello(c, M.m0769, V)


def k0640(c, V):
    return C.modello(c, M.m0770, V)


def k0641(c, V):
    return C.modello(c, M.m0771, V)


def k0642(c, V):
    return C.modello(c, M.m0772, V)


def k0643(c, V):
    return C.modello(c, M.m0773, V)


def k0644(c, V):
    return C.trigger(V, ['spia_umidita_off'])


def k0645(c, V):
    return C.modello(c, M.m0776, V)


def k0646(c, V):
    return C.modello(c, M.m0777, V)


def k0647(c, V):
    return C.modello(c, M.m0778, V)


def k0648(c, V):
    return C.trigger(V, ['umidita_velocita_0'])


def k0649(c, V):
    return C.modello(c, M.m0779, V)


def k0650(c, V):
    return C.modello(c, M.m0780, V)


def k0651(c, V):
    return C.modello(c, M.m0781, V)


def k0652(c, V):
    return C.trigger(V, ['umidita_velocita_1'])


def k0653(c, V):
    return C.trigger(V, ['umidita_velocita_2'])


def k0654(c, V):
    return C.trigger(V, ['umidita_velocita_3'])


def k0655(c, V):
    return C.trigger(V, ['umidita_velocita_4'])


def k0656(c, V):
    return C.trigger(V, ['umidita_velocita_notturna'])


def k0657(c, V):
    return C.trigger(V, ['umidita_velocita_iperventilazione'])


def k0658(c, V):
    return C.modello(c, M.m0782, V)


def k0659(c, V):
    return C.trigger(V, ['umidita_velocita_free_cooling'])


def k0660(c, V):
    return C.modello(c, M.m0783, V)


def k0661(c, V):
    return C.modello(c, M.m0784, V)


def k0662(c, V):
    return C.trigger(V, ['spia_velocita_0_delta_temp'])


def k0663(c, V):
    return C.modello(c, M.m0785, V)


def k0664(c, V):
    return C.o(c, V, (k0662, k0663, ))


def k0665(c, V):
    return C.modello(c, M.m0786, V)


def k0666(c, V):
    return C.trigger(V, ['spia_velocita_1_delta_temp'])


def k0667(c, V):
    return C.modello(c, M.m0787, V)


def k0668(c, V):
    return C.o(c, V, (k0666, k0667, ))


def k0669(c, V):
    return C.trigger(V, ['spia_velocita_2_delta_temp'])


def k0670(c, V):
    return C.modello(c, M.m0788, V)


def k0671(c, V):
    return C.o(c, V, (k0669, k0670, ))


def k0672(c, V):
    return C.trigger(V, ['spia_velocita_3_delta_temp'])


def k0673(c, V):
    return C.modello(c, M.m0789, V)


def k0674(c, V):
    return C.o(c, V, (k0672, k0673, ))


def k0675(c, V):
    return C.trigger(V, ['spia_velocita_4_delta_temp'])


def k0676(c, V):
    return C.modello(c, M.m0790, V)


def k0677(c, V):
    return C.o(c, V, (k0675, k0676, ))


def k0678(c, V):
    return C.trigger(V, ['spia_velocita_iperventilazione_delta_temp'])


def k0679(c, V):
    return C.modello(c, M.m0791, V)


def k0680(c, V):
    return C.o(c, V, (k0678, k0679, ))


def k0681(c, V):
    return C.trigger(V, ['spia_velocita_notturna_delta_temp'])


def k0682(c, V):
    return C.modello(c, M.m0792, V)


def k0683(c, V):
    return C.o(c, V, (k0681, k0682, ))


def k0684(c, V):
    return C.trigger(V, ['spia_velocita_Free Cooling_delta_temp'])


def k0685(c, V):
    return C.modello(c, M.m0793, V)


def k0686(c, V):
    return C.o(c, V, (k0684, k0685, ))


def k0687(c, V):
    return C.trigger(V, ['delta_temp_ON'])


def k0688(c, V):
    return C.o(c, V, (k0687, k0662, k0666, k0669, k0672, k0675, k0678, k0681, k0684, ))


def k0689(c, V):
    return C.modello(c, M.m0797, V)


def k0690(c, V):
    return C.modello(c, M.m0798, V)


def k0691(c, V):
    return C.modello(c, M.m0799, V)


def k0692(c, V):
    return C.modello(c, M.m0800, V)


def k0693(c, V):
    return C.modello(c, M.m0801, V)


def k0694(c, V):
    return C.modello(c, M.m0802, V)


def k0695(c, V):
    return C.modello(c, M.m0803, V)


def k0696(c, V):
    return C.modello(c, M.m0804, V)


def k0697(c, V):
    return C.modello(c, M.m0805, V)


def k0698(c, V):
    return C.modello(c, M.m0806, V)


def k0699(c, V):
    return C.modello(c, M.m0807, V)


def k0700(c, V):
    return C.trigger(V, ['delta_temp_OFF'])


def k0701(c, V):
    return C.modello(c, M.m0899, V)


def k0702(c, V):
    return C.modello(c, M.m0900, V)


def k0703(c, V):
    return C.modello(c, M.m0901, V)


def k0704(c, V):
    return C.modello(c, M.m0903, V)


def k0705(c, V):
    return C.modello(c, M.m0904, V)


def k0706(c, V):
    return C.modello(c, M.m0907, V)


def k0707(c, V):
    return C.modello(c, M.m0908, V)


def k0708(c, V):
    return C.modello(c, M.m0909, V)


def k0709(c, V):
    return C.modello(c, M.m0911, V)


def k0710(c, V):
    return C.modello(c, M.m0912, V)


def k0711(c, V):
    return C.modello(c, M.m0915, V)


def k0712(c, V):
    return C.modello(c, M.m0916, V)


def k0713(c, V):
    return C.modello(c, M.m0917, V)


def k0714(c, V):
    return C.modello(c, M.m0919, V)


def k0715(c, V):
    return C.modello(c, M.m0920, V)


def k0716(c, V):
    return C.modello(c, M.m0923, V)


def k0717(c, V):
    return C.modello(c, M.m0924, V)


def k0718(c, V):
    return C.modello(c, M.m0925, V)


def k0719(c, V):
    return C.modello(c, M.m0927, V)


def k0720(c, V):
    return C.modello(c, M.m0928, V)


def k0721(c, V):
    return C.modello(c, M.m0931, V)


def k0722(c, V):
    return C.modello(c, M.m0932, V)


def k0723(c, V):
    return C.modello(c, M.m0933, V)


def k0724(c, V):
    return C.modello(c, M.m0935, V)


def k0725(c, V):
    return C.modello(c, M.m0936, V)


def k0726(c, V):
    return C.modello(c, M.m0939, V)


def k0727(c, V):
    return C.modello(c, M.m0940, V)


def k0728(c, V):
    return C.modello(c, M.m0941, V)


def k0729(c, V):
    return C.modello(c, M.m0943, V)


def k0730(c, V):
    return C.modello(c, M.m0944, V)


def k0731(c, V):
    return C.modello(c, M.m0947, V)


def k0732(c, V):
    return C.modello(c, M.m0948, V)


def k0733(c, V):
    return C.modello(c, M.m0950, V)


def k0734(c, V):
    return C.modello(c, M.m0951, V)


def k0735(c, V):
    return C.modello(c, M.m0955, V)


def k0736(c, V):
    return C.modello(c, M.m0962, V)


def k0737(c, V):
    return C.modello(c, M.m0963, V)


def k0738(c, V):
    return C.modello(c, M.m0965, V)


def k0739(c, V):
    return C.modello(c, M.m0966, V)


def k0740(c, V):
    return C.modello(c, M.m0970, V)


def k0741(c, V):
    return C.modello(c, M.m0971, V)


def k0742(c, V):
    return C.modello(c, M.m0973, V)


def k0743(c, V):
    return C.modello(c, M.m0974, V)


def k0744(c, V):
    return C.modello(c, M.m0975, V)


def k0745(c, V):
    return C.modello(c, M.m0976, V)


def k0746(c, V):
    return C.modello(c, M.m0977, V)


def k0747(c, V):
    return C.modello(c, M.m0978, V)


def k0748(c, V):
    return C.modello(c, M.m0979, V)


def k0749(c, V):
    return C.modello(c, M.m0980, V)


def k0750(c, V):
    return C.modello(c, M.m0981, V)


def k0751(c, V):
    return C.modello(c, M.m0982, V)


def k0752(c, V):
    return C.e(c, V, (k0750, k0751, ))


def k0753(c, V):
    return C.modello(c, M.m0983, V)


def k0754(c, V):
    return C.e(c, V, (k0750, k0753, ))


def k0755(c, V):
    return C.modello(c, M.m0984, V)


def k0756(c, V):
    return C.e(c, V, (k0755, k0751, ))


def k0757(c, V):
    return C.e(c, V, (k0755, k0753, ))


def k0758(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Velocità 0'])


def k0759(c, V):
    return C.modello(c, M.m0985, V)


def k0760(c, V):
    return C.e(c, V, (k0758, k0759, ))


def k0761(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Velocità 1'])


def k0762(c, V):
    return C.e(c, V, (k0761, k0759, ))


def k0763(c, V):
    return C.modello(c, M.m0986, V)


def k0764(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Velocità 2'])


def k0765(c, V):
    return C.e(c, V, (k0764, k0759, ))


def k0766(c, V):
    return C.modello(c, M.m0987, V)


def k0767(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Velocità 3'])


def k0768(c, V):
    return C.e(c, V, (k0767, k0759, ))


def k0769(c, V):
    return C.modello(c, M.m0988, V)


def k0770(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Velocità 4'])


def k0771(c, V):
    return C.e(c, V, (k0770, k0759, ))


def k0772(c, V):
    return C.modello(c, M.m0989, V)


def k0773(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Notturna'])


def k0774(c, V):
    return C.e(c, V, (k0773, k0759, ))


def k0775(c, V):
    return C.modello(c, M.m0990, V)


def k0776(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Iperventilazione'])


def k0777(c, V):
    return C.e(c, V, (k0776, k0759, ))


def k0778(c, V):
    return C.modello(c, M.m0991, V)


def k0779(c, V):
    return C.modello(c, M.m0992, V)


def k0780(c, V):
    return C.modello(c, M.m0993, V)


def k0781(c, V):
    return C.modello(c, M.m0994, V)


def k0782(c, V):
    return C.modello(c, M.m0995, V)


def k0783(c, V):
    return C.modello(c, M.m0996, V)


def k0784(c, V):
    return C.modello(c, M.m0997, V)


def k0785(c, V):
    return C.modello(c, M.m0998, V)


def k0786(c, V):
    return C.modello(c, M.m0999, V)


def k0787(c, V):
    return C.modello(c, M.m1000, V)


def k0788(c, V):
    return C.modello(c, M.m1001, V)


def k0789(c, V):
    return C.modello(c, M.m1002, V)


def k0790(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_1_fascia_calendario')], ['Free Cool./Heat.'])


def k0791(c, V):
    return C.e(c, V, (k0790, k0759, ))


def k0792(c, V):
    return C.modello(c, M.m1003, V)


def k0793(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Velocità 0'])


def k0794(c, V):
    return C.e(c, V, (k0793, k0759, ))


def k0795(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Velocità 1'])


def k0796(c, V):
    return C.e(c, V, (k0795, k0759, ))


def k0797(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Velocità 2'])


def k0798(c, V):
    return C.e(c, V, (k0797, k0759, ))


def k0799(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Velocità 3'])


def k0800(c, V):
    return C.e(c, V, (k0799, k0759, ))


def k0801(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Velocità 4'])


def k0802(c, V):
    return C.e(c, V, (k0801, k0759, ))


def k0803(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Notturna'])


def k0804(c, V):
    return C.e(c, V, (k0803, k0759, ))


def k0805(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Iperventilazione'])


def k0806(c, V):
    return C.e(c, V, (k0805, k0759, ))


def k0807(c, V):
    return C.stato(c, V, [c.N('sensor.vmc_master_speed_2_fascia_calendario')], ['Free Cool./Heat.'])


def k0808(c, V):
    return C.e(c, V, (k0807, k0759, ))


def k0809(c, V):
    return C.modello(c, M.m1006, V)


def k0810(c, V):
    return C.modello(c, M.m1008, V)


def k0811(c, V):
    return C.modello(c, M.m1010, V)


def k0812(c, V):
    return C.modello(c, M.m1012, V)


def k0813(c, V):
    return C.modello(c, M.m1014, V)


def k0814(c, V):
    return C.modello(c, M.m1016, V)


def k0815(c, V):
    return C.modello(c, M.m1019, V)


def k0816(c, V):
    return C.modello(c, M.m1022, V)


def k0817(c, V):
    return C.modello(c, M.m1025, V)


def k0818(c, V):
    return C.modello(c, M.m1027, V)


def k0819(c, V):
    return C.modello(c, M.m1030, V)


def k0820(c, V):
    return C.modello(c, M.m1032, V)
