"""b36 agente B: Black-Out e ritorno della corrente con Umidita', Free Cooling/Heating, Calendario e velocita' dell'utente.
Uso: python b36bo.py OUT.jsonl CFG [filtro] [nproc]
Ogni scenario ha meta['exp'] = {check: (velocita' attesa, Velocita' Registrata attesa, Alert Avvio atteso)}:
velocita' = int o tupla di int (0-4, 5 Iper, 6 Nott, 7 Free); registrata = str o tupla ('FREE' = nome Free del mese);
alert = str o None (non controllato). meta['x'] = True: caso esplorativo (non contato nei giusti/sbagliati)."""
import sys, re, alerts
from gen import base, cal_setup, CAL_SW, SPEED_OPT

UMI_SET = 'input_select.vmc_master_speed_umidita'
SETOPT = {0: 'Velocità 0', 1: 'Velocità 1', 2: 'Velocità 2', 7: 'Free Cool./Heat.'}
HUM_ON = {'UMIDA': {'ui': 80.0}, 'UMIDS': {'ui': 30.0, 'ue': 30.0}}
HUM_OFF = {'UMIDA': {'ui': 50.0}, 'UMIDS': {'ui': 50.0}}
MODELS = {'B': False, 'R': True}          # B = modello base (al ritorno V1 se non era ferma), R = riparte alla velocita' di prima
V0, N0 = 'Velocità 0', 'Nessuna'


def mk(id_, vmc, mod, s0, setup=()):
    sc = base(id_, vmc, s0, list(setup))
    if MODELS[mod]: sc['setup'] = [('resume', True)] + sc['setup']
    sc['meta'] = dict(exp={}, mode=None, x=False)
    return sc


def bo(sc, t_off, t_on):
    sc['timeline'] += [(t_off, ('online', False)), (t_on, ('online', True))]


def fin(sc, end, exp):
    sc['end'] = end
    sc['checks'] = sorted([(t, n) for n, t in ((n, int(n[1:])) for n in exp if n != 'final')])
    sc['meta']['exp'].update(exp)


# ---------------------------------------------------------------- Umidita'
def fam_umid():
    out = []
    for al in ('UMIDA', 'UMIDS'):
        for vmc in 'FL':
            for mod in 'BR':
                # VMC ferma: l'Umidita' la avvia alla [Set]
                for S in (0, 1, 2, 7):
                    regA = N0 if S == 0 else V0
                    cases = ['ref', 'a', 'b', 'c', 'd1', 'd2', 'd3'] + (['d1v1'] if S == 0 else ['d0'])
                    for cs in cases:
                        if cs == 'ref' and mod == 'R': continue
                        sc = mk(f'U|{al}|s0|S{S}|{cs}|{vmc}|{mod}', vmc, mod, 0, [('select', UMI_SET, SETOPT[S])])
                        hoff = 120 if cs == 'c' else 300
                        sc['timeline'] = [(10, ('env', HUM_ON[al])), (hoff, ('env', HUM_OFF[al]))]
                        e = {}
                        if cs == 'ref':
                            e = {'c100': (S, regA, N0), 'c240': (S, regA, N0)}
                        elif cs == 'a':
                            bo(sc, 20, 110); e = {'c240': (S, regA, N0)}
                        elif cs == 'b':
                            bo(sc, 80, 160); e = {'c120': (S, regA, None), 'c240': (S, regA, N0)}
                        elif cs == 'c':
                            bo(sc, 80, 200); e = {'c300': (0, N0, N0)}
                        elif cs in ('d1', 'd1v1', 'd0'):
                            P = {'d1': 3, 'd1v1': 1, 'd0': 0}[cs]
                            sc['timeline'].append((60, ('press', P))); bo(sc, 90, 170)
                            e = {'c240': (S, regA, N0)} if P == 0 else {'c240': (P, N0, N0)}
                        elif cs == 'd2':
                            bo(sc, 80, 160); sc['timeline'].append((230, ('press', 3))); e = {'c280': (3, N0, N0)}
                        elif cs == 'd3':
                            bo(sc, 80, 160); sc['timeline'].append((175, ('press', 3))); e = {'c240': (3, N0, N0)}
                            # (simfull/blackout) non piu' esplorativo: decisione del proprietario 21-11-2026 12:11Z e Foglio A23
                            # (seconda revisione 12:12Z) «UNA VELOCITA' SCELTA PRIMA DEL RIPRISTINO RESTA E IL RIPRISTINO NON AVVIENE»
                        Pf = {'d1': 3, 'd1v1': 1, 'd2': 3, 'd3': 3}.get(cs, 0)
                        e['final'] = (Pf, N0, N0)
                        fin(sc, 420, e); out.append(sc)
                # VMC gia' in moto: l'Umidita' memorizza la velocita' in uso e non la cambia
                for s0 in (1, 2, 3, 4, 6, 5, 7):
                    for cs in ('ref', 'a', 'b', 'c', 'd1'):
                        if cs == 'ref' and mod == 'R': continue
                        sc = mk(f'U|{al}|s{s0}|S2|{cs}|{vmc}|{mod}', vmc, mod, s0)
                        hoff = 120 if cs == 'c' else 300
                        sc['timeline'] = [(10, ('env', HUM_ON[al])), (hoff, ('env', HUM_OFF[al]))]
                        P = 4 if s0 != 4 else 3
                        if cs == 'ref': e = {'c100': (s0, N0, N0), 'c240': (s0, N0, N0)}
                        elif cs == 'a': bo(sc, 20, 110); e = {'c240': (s0, N0, N0)}
                        elif cs == 'b': bo(sc, 80, 160); e = {'c120': (s0, N0, None), 'c240': (s0, N0, N0)}
                        elif cs == 'c': bo(sc, 80, 200); e = {'c300': (s0, N0, N0)}
                        else:
                            sc['timeline'].append((60, ('press', P))); bo(sc, 90, 170); e = {'c240': (P, N0, N0)}
                        e['final'] = (P if cs == 'd1' else s0, N0, N0)
                        fin(sc, 420, e); out.append(sc)
    return out


# ---------------------------------------------------------------- Free Cooling / Free Heating
def fam_free():
    out = []
    AF = 'Alert Free'
    for M in 'HC':
        UNF = alerts.FREE_UNFAV[M][0][1]; FAV = alerts.FREE_FAV[M][0][1]
        for vmc in 'FL':
            for mod in 'BR':
                def S(id_, setv=None):
                    st = alerts.free_setup(M) + ([('select', UMI_SET, SETOPT[setv])] if setv is not None else [])
                    sc = mk(f'F|{M}|{id_}|{vmc}|{mod}', vmc, mod, 7, st); sc['meta']['mode'] = M; return sc
                # F0: riferimento (Free sospesa, ripresa)
                if mod == 'B':
                    sc = S('F0'); sc['timeline'] = [(10, ('env', UNF)), (250, ('env', FAV))]
                    fin(sc, 360, {'c100': (0, 'FREE', AF), 'c240': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # F1: VMC in Free con condizioni favorevoli
                sc = S('F1'); bo(sc, 30, 110)
                fin(sc, 260, {'c200': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
                # F2a: Black-Out prima della sospensione (24 s)
                sc = S('F2a'); sc['timeline'] = [(10, ('env', UNF)), (250, ('env', FAV))]; bo(sc, 20, 110)
                fin(sc, 360, {'c200': (0, 'FREE', AF), 'c240': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # F2b: Black-Out con la ripresa in attesa, condizioni ancora sfavorevoli al ritorno
                sc = S('F2b'); sc['timeline'] = [(10, ('env', UNF)), (250, ('env', FAV))]; bo(sc, 60, 140)
                fin(sc, 360, {'c100': (0, 'FREE', None), 'c200': (0, 'FREE', AF), 'c240': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # F2c: condizioni favorevoli durante il Black-Out
                sc = S('F2c'); sc['timeline'] = [(10, ('env', UNF)), (100, ('env', FAV))]; bo(sc, 60, 160)
                fin(sc, 320, {'c255': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
                # F2d: condizioni favorevoli dopo il ritorno, prima del ripristino
                sc = S('F2d'); sc['timeline'] = [(10, ('env', UNF)), (150, ('env', FAV))]; bo(sc, 60, 140)
                fin(sc, 320, {'c240': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
                # F3: ripresa annullata (Velocita' 2 scelta durante la sospensione), poi Black-Out
                sc = S('F3'); sc['timeline'] = [(10, ('env', UNF)), (60, ('press', 2)), (250, ('env', FAV))]; bo(sc, 110, 190)
                fin(sc, 360, {'c100': (2, N0, AF), 'c240': (2, N0, AF), 'final': (2, N0, N0)}); out.append(sc)
                # F3b: Black-Out durante i 20 s dell'annullamento
                sc = S('F3b'); sc['timeline'] = [(10, ('env', UNF)), (60, ('press', 2)), (250, ('env', FAV))]; bo(sc, 70, 150)
                fin(sc, 360, {'c240': (2, N0, AF), 'final': (2, N0, N0)}); out.append(sc)
                # F4: Free sospesa con l'Umidita' in corso (Velocita' 1, Nota 3) - caso dello screenshot
                for sv in (0, 1, 2, 7):
                    vh = 0 if sv == 0 else 1
                    for wbo in ((False, True) if mod == 'B' else (True,)):
                        sc = S(f'F4|S{sv}|{"bo" if wbo else "ref"}', sv)
                        sc['timeline'] = [(10, ('env', UNF)), (40, ('env', {'ui': 80.0})), (260, ('env', {'ui': 50.0})), (330, ('env', FAV))]
                        e = {'c90': (vh, 'FREE', AF), 'c250': (vh, 'FREE', AF), 'c320': (0, 'FREE', AF), 'final': (7, N0, N0)}
                        if wbo: bo(sc, 100, 180); e['c150'] = (vh, 'FREE', None)
                        fin(sc, 440, e); out.append(sc)
                # F4b: l'Umidita' finisce durante il Black-Out
                sc = S('F4b', 2)
                sc['timeline'] = [(10, ('env', UNF)), (40, ('env', {'ui': 80.0})), (130, ('env', {'ui': 50.0})), (330, ('env', FAV))]; bo(sc, 100, 200)
                fin(sc, 440, {'c290': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # F4c: la Free torna favorevole durante il Black-Out con l'Umidita' in corso (+ riferimento)
                for wbo in ((False, True) if mod == 'B' else (True,)):
                    sc = S(f'F4c|{"bo" if wbo else "ref"}', 2)
                    sc['timeline'] = [(10, ('env', UNF)), (40, ('env', {'ui': 80.0})), (130, ('env', FAV)), (300, ('env', {'ui': 50.0}))]
                    if wbo: bo(sc, 100, 200)
                    fin(sc, 420, {'c290': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
                # F4d: l'Umidita' sale durante il Black-Out con la Free sospesa
                sc = S('F4d', 2)
                sc['timeline'] = [(10, ('env', UNF)), (60, ('env', {'ui': 80.0})), (300, ('env', {'ui': 50.0})), (370, ('env', FAV))]; bo(sc, 50, 140)
                fin(sc, 480, {'c250': (1, 'FREE', AF), 'c360': (0, 'FREE', AF), 'final': (7, N0, N0)}); out.append(sc)
                # F5: VMC in Free (favorevole) con l'Umidita' in corso, poi Black-Out
                sc = S('F5', 2)
                sc['timeline'] = [(20, ('env', {'ui': 80.0})), (250, ('env', {'ui': 50.0}))]; bo(sc, 80, 160)
                fin(sc, 360, {'c240': (7, N0, N0), 'final': (7, N0, N0)}); out.append(sc)
    return out


# ---------------------------------------------------------------- Calendario (fascia 1 = 60-300 s, fascia 2 = 480-720 s a Velocita' 3)
def fam_cal():
    out = []
    for vmc in 'FL':
        for mod in 'BR':
            def C(id_, v1, s0):
                setup, t0a, _ = cal_setup(v1, 3, True)
                sc = mk(f'C|{id_}|v{v1}|s{s0}|{vmc}|{mod}', vmc, mod, s0, setup)
                sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
                return sc
            for v1 in (0, 1, 2, 4, 6, 5, 7):
                if mod == 'B':
                    sc = C('C0', v1, 0); fin(sc, 760, {'c200': (v1, N0, N0), 'c400': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                sc = C('C1', v1, 0); bo(sc, 120, 200)          # Black-Out e ritorno dentro la fascia
                fin(sc, 760, {'c270': (v1, N0, N0), 'c400': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                sc = C('C2', v1, 0); bo(sc, 200, 380)          # la fascia finisce durante il Black-Out
                fin(sc, 760, {'c440': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                sc = C('C2b', v1, 0); bo(sc, 200, 500)         # ritorno durante la 2a fascia
                fin(sc, 760, {'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                for s0 in (0, 2):                              # Black-Out a cavallo dell'inizio della fascia
                    sc = C('C3', v1, s0); bo(sc, 20, 120)
                    fin(sc, 760, {'c200': (v1, N0, N0), 'c400': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
            # con Inquinanti
            for v1 in (0, 2, 4, 7):
                vin = 1 if v1 == 0 else v1; rin = V0 if v1 == 0 else N0
                for wbo in ((False, True) if mod == 'B' else (True,)):
                    k = 'bo' if wbo else 'ref'
                    sc = C(f'C5a|{k}', v1, 0); sc['timeline'] += [(100, ('env', {'co2': 1500.0})), (280, ('env', {'co2': 500.0}))]
                    if wbo: bo(sc, 140, 210)
                    fin(sc, 470, {'c270': (vin, rin, N0), 'c400': (0, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                    sc = C(f'C5b|{k}', v1, 0); sc['timeline'] += [(100, ('env', {'co2': 1500.0})), (400, ('env', {'co2': 500.0}))]
                    if wbo: bo(sc, 140, 210)
                    fin(sc, 760, {'c270': (vin, rin, N0), 'c350': (1, V0, N0), 'c460': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                    sc = C(f'C5c|{k}', v1, 0); sc['timeline'] += [(100, ('env', {'co2': 1500.0})), (445, ('env', {'co2': 500.0}))]
                    if wbo: bo(sc, 230, 350)
                    fin(sc, 760, {'c200': (vin, rin, N0), 'c425': (1, V0, N0), 'c475': (0, N0, N0), 'c600': (3, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
                    sc = C(f'C5d|{k}', v1, 0); sc['timeline'] += [(10, ('env', {'co2': 1500.0})), (200, ('env', {'co2': 500.0}))]
                    if wbo: bo(sc, 30, 120)
                    fin(sc, 470, {'c180': (vin, (N0, V0), N0), 'c250': (v1, N0, N0), 'c400': (0, N0, N0), 'final': (0, N0, N0)}); out.append(sc)
    return out


# ---------------------------------------------------------------- velocita' scelte dall'utente, nessuna allerta
def fam_user():
    out = []
    for vmc in 'FL':
        for mod in 'BR':
            for s0 in (0, 1, 2, 3, 4, 6, 5, 7):
                sc = mk(f'N|N1|s{s0}|{vmc}|{mod}', vmc, mod, s0); bo(sc, 20, 100)
                fin(sc, 200, {'c60': (s0, N0, None), 'c160': (s0, N0, N0), 'final': (s0, N0, N0)}); out.append(sc)
                sc = mk(f'N|N3|s{s0}|{vmc}|{mod}', vmc, mod, s0); bo(sc, 20, 100); bo(sc, 115, 200)   # 2 Black-Out di fila
                fin(sc, 300, {'c260': (s0, N0, N0), 'final': (s0, N0, N0)}); out.append(sc)
                sc = mk(f'N|N4|s{s0}|{vmc}|{mod}', vmc, mod, s0); bo(sc, 20, 40)     # mancanza corta (< rilevazione)
                fin(sc, 150, {'final': (s0, N0, N0)}); sc['meta']['x'] = True; out.append(sc)
                P = 4 if s0 != 4 else 3                                              # scelta dell'utente prima del ripristino
                sc = mk(f'N|N5|s{s0}|{vmc}|{mod}', vmc, mod, s0); bo(sc, 20, 100); sc['timeline'].append((115, ('press', P)))
                fin(sc, 220, {'final': (P, N0, N0)}); out.append(sc)   # (simfull/blackout) atteso fisso dal 21-11-2026 12:11Z (A23): la scelta resta
    return out


def scen():
    return fam_umid() + fam_free() + fam_cal() + fam_user()


if __name__ == '__main__':
    import runner
    scs = scen()
    ids = [s['id'] for s in scs]; assert len(ids) == len(set(ids))
    if len(sys.argv) > 3 and sys.argv[3] != '-':
        pat = re.compile(sys.argv[3]); scs = [s for s in scs if pat.search(s['id'])]
    print('scenari', len(scs), flush=True)
    runner.run_all(scs, sys.argv[1], nproc=int(sys.argv[4]) if len(sys.argv) > 4 else 1, cfg=sys.argv[2])
