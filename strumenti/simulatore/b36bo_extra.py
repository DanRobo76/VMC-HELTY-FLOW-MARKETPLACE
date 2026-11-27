"""b36 agente B, lotto 2: Black-Out che arriva mentre un'allerta sta finendo (o mentre una fascia inizia/finisce).
L'allerta finisce (o la fascia cambia) con la VMC gia' senza corrente ma prima che il Black-Out sia rilevato.
Uso: python b36bo_extra.py OUT.jsonl CFG [filtro] [nproc]"""
import sys, re, alerts
import b36bo
from b36bo import mk, bo, fin, UMI_SET, SETOPT, HUM_ON, HUM_OFF, V0, N0
from gen import cal_setup, CAL_SW


def scen():
    out = []
    AF = 'Alert Free'
    for vmc in 'FL':
        for mod in 'BR':
            # Umidita' partita da V0 (Set 2 / Free) o VMC gia' in moto (V3): fine Umidita' a 120 s (comando a ~148 s),
            # Black-Out a 120+d: a fine allerta la VMC deve tornare alla velocita' di fine allerta
            for al in ('UMIDA', 'UMIDS'):
                for s0, S in ((0, 2), (0, 7), (3, 2)):
                    for d in (10, 20, 26, 29):
                        sc = mk(f'E|U|{al}|s{s0}|S{S}|d{d}|{vmc}|{mod}', vmc, mod, s0, [('select', UMI_SET, SETOPT[S])])
                        sc['timeline'] = [(10, ('env', HUM_ON[al])), (120, ('env', HUM_OFF[al]))]
                        bo(sc, 120 + d, 240)
                        fin(sc, 420, {'c340': (s0, N0, N0), 'final': (s0, N0, N0)}); out.append(sc)
            for M in 'HC':
                UNF = alerts.FREE_UNFAV[M][0][1]; FAV = alerts.FREE_FAV[M][0][1]
                # ripresa Free (24 s) con il Black-Out che arriva durante l'attesa o col comando di ripresa
                for d in (10, 18, 23, 25):
                    sc = mk(f'E|FR|{M}|d{d}|{vmc}|{mod}', vmc, mod, 7, alerts.free_setup(M)); sc['meta']['mode'] = M
                    sc['timeline'] = [(10, ('env', UNF)), (120, ('env', FAV))]; bo(sc, 120 + d, 240)
                    fin(sc, 420, {'c345': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
                # sospensione Free (24 s) con il Black-Out che arriva durante l'attesa o col comando Velocita' 0
                for d in (18, 23, 25):
                    sc = mk(f'E|FS|{M}|d{d}|{vmc}|{mod}', vmc, mod, 7, alerts.free_setup(M)); sc['meta']['mode'] = M
                    sc['timeline'] = [(10, ('env', UNF)), (330, ('env', FAV))]; bo(sc, 10 + d, 140)
                    fin(sc, 440, {'c250': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # Free sospesa + Umidita' (V1, Nota 3): fine Umidita' a 200 s con il Black-Out durante l'attesa
                for d in (20, 26, 29):
                    sc = mk(f'E|F4|{M}|d{d}|{vmc}|{mod}', vmc, mod, 7, alerts.free_setup(M) + [('select', UMI_SET, SETOPT[2])]); sc['meta']['mode'] = M
                    sc['timeline'] = [(10, ('env', UNF)), (40, ('env', {'ui': 80.0})), (200, ('env', {'ui': 50.0})), (420, ('env', FAV))]
                    bo(sc, 200 + d, 320)
                    fin(sc, 520, {'c400': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # Free sospesa + Umidita' (V1): Black-Out mentre la Free torna favorevole (ripresa)
                for d in (18, 25):
                    sc = mk(f'E|F4r|{M}|d{d}|{vmc}|{mod}', vmc, mod, 7, alerts.free_setup(M) + [('select', UMI_SET, SETOPT[2])]); sc['meta']['mode'] = M
                    sc['timeline'] = [(10, ('env', UNF)), (40, ('env', {'ui': 80.0})), (120, ('env', FAV)), (400, ('env', {'ui': 50.0}))]
                    bo(sc, 120 + d, 240)
                    fin(sc, 520, {'c380': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
            # Free: condizioni sfavorevoli durante il Black-Out (VMC in Free prima); Umidita' che sale durante il Black-Out
            for M in 'HC':
                UNF = alerts.FREE_UNFAV[M][0][1]; FAV = alerts.FREE_FAV[M][0][1]
                sc = mk(f'E|F6|{M}|{vmc}|{mod}', vmc, mod, 7, alerts.free_setup(M)); sc['meta']['mode'] = M
                sc['timeline'] = [(90, ('env', UNF)), (300, ('env', FAV))]; bo(sc, 30, 130)
                fin(sc, 420, {'c250': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
            for S in (0, 2, 7):
                sc = mk(f'E|Ua2|s0|S{S}|{vmc}|{mod}', vmc, mod, 0, [('select', UMI_SET, SETOPT[S])])
                sc['timeline'] = [(70, ('env', HUM_ON['UMIDA'])), (300, ('env', HUM_OFF['UMIDA']))]; bo(sc, 20, 110)
                fin(sc, 420, {'c240': (S, N0 if S == 0 else V0, N0), 'final': (0, N0, N0)}); out.append(sc)
            # Calendario: Black-Out proprio mentre la fascia finisce (300 s, +3) o inizia (60 s, +3 +5)
            for v1 in (2, 6, 7):
                for t in (290, 296, 300, 302):
                    setup, t0a, _ = cal_setup(v1, 3, True)
                    sc = mk(f'E|CF|v{v1}|t{t}|{vmc}|{mod}', vmc, mod, 0, setup)
                    sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
                    bo(sc, t, 400)
                    fin(sc, 760, {'c470': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                for t in (55, 61, 64, 67):
                    for s0 in (0, 4):
                        setup, t0a, _ = cal_setup(v1, 3, True)
                        sc = mk(f'E|CI|v{v1}|s{s0}|t{t}|{vmc}|{mod}', vmc, mod, s0, setup)
                        sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
                        bo(sc, t, 160)
                        fin(sc, 760, {'c250': (v1, N0, N0), 'c400': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
            # Calendario con l'Umidita' fuori soglia: fascia finita durante il Black-Out (CU1) e Black-Out a cavallo dell'inizio
            # della fascia con l'Umidita' gia' in corso (CU2): a fine fascia la VMC si ferma e l'Umidita' riparte alla [Set] (2)
            setup, t0a, _ = cal_setup(3, 3, True)
            sc = mk(f'E|CU1|{vmc}|{mod}', vmc, mod, 0, setup)
            sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
            sc['timeline'] = [(100, ('env', HUM_ON['UMIDA'])), (650, ('env', HUM_OFF['UMIDA']))]; bo(sc, 200, 350)
            fin(sc, 790, {'c460': (2, V0, N0), 'c600': (3, (N0, V0), N0), 'final': (0, N0, N0)}); out.append(sc)
            sc = mk(f'E|CU2|{vmc}|{mod}', vmc, mod, 0, setup)
            sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
            sc['timeline'] = [(1, ('env', HUM_ON['UMIDA'])), (400, ('env', HUM_OFF['UMIDA']))]; bo(sc, 40, 120)
            fin(sc, 475, {'c200': (3, (N0, V0), N0), 'c370': (2, V0, N0), 'final': (0, N0, N0)}); out.append(sc)
            # Calendario con Inquinanti che finiscono durante il Black-Out (dentro la fascia e dopo la fine della fascia)
            for v1 in (0, 2):
                setup, t0a, _ = cal_setup(v1, 3, True)
                sc = mk(f'E|CQ|v{v1}|in|{vmc}|{mod}', vmc, mod, 0, setup)
                sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
                sc['timeline'] = [(90, ('env', {'co2': 1500.0})), (160, ('env', {'co2': 500.0}))]; bo(sc, 130, 220)
                fin(sc, 470, {'c280': (v1, N0, N0), 'c400': (0, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                sc = mk(f'E|CQ|v{v1}|out|{vmc}|{mod}', vmc, mod, 0, setup)
                sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
                sc['timeline'] = [(90, ('env', {'co2': 1500.0})), (330, ('env', {'co2': 500.0}))]; bo(sc, 310, 400)
                fin(sc, 760, {'c470': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
    return out


if __name__ == '__main__':
    import runner
    scs = scen()
    ids = [s['id'] for s in scs]; assert len(ids) == len(set(ids))
    if len(sys.argv) > 3 and sys.argv[3] != '-':
        pat = re.compile(sys.argv[3]); scs = [s for s in scs if pat.search(s['id'])]
    print('scenari', len(scs), flush=True)
    runner.run_all(scs, sys.argv[1], nproc=int(sys.argv[4]) if len(sys.argv) > 4 else 1, cfg=sys.argv[2])
