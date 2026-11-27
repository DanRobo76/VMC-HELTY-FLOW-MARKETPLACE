"""Le famiglie Black-Out della simulazione completa di ogni versione (regola del 21-11-2026): 4.842 scenari di
Black-Out e ritorno della corrente durante le allerte, scritti per la b36 (simulatore-b36/blackout) e copiati qui
senza modifiche, cosi' girano anche nella prova differenziale (targeted.py e differenziale.py con «blackout»).

- bo_a.py (agente A): 3.480 scenari (singoli 1.720, extra g/h/i 360, coppie 1.400);
- b36bo.py (agente B, lotto 1): 982 scenari (i 1.014 meno i 32 esplorativi «N|N4|», come in lancia_blackout.sh);
- b36bo_extra.py (agente B, lotto 2): 380 scenari.

Gli id non coincidono con quelli dei 17.264 scenari di gen.py e della famiglia M. Le verifiche della b36
(bo_a_check.py, b36bo_check.py) restano nel simulatore della b36: qui si confrontano le tracce.
"""
import re

import b36bo
import b36bo_extra
import bo_a

ESPLORATIVI = re.compile(r'N\|N4\|')


def famiglia():
    """I 4.842 scenari Black-Out, nell'ordine di lancia_blackout.sh (bo_a, b36bo, b36bo_extra)."""
    scenari = bo_a.scen()
    scenari += [s for s in b36bo.scen() if not ESPLORATIVI.match(s['id'])]
    scenari += b36bo_extra.scen()
    return scenari
