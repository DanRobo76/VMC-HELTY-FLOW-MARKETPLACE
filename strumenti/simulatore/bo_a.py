"""b36 - agente A: Black-Out e ritorno della corrente con le allerte CONG, DELTA, CO2, VOC, PDR (anche a coppie compatibili)
e con una velocita' scelta dall'utente durante l'allerta.
Uso: python bo_a.py OUT.jsonl CFG [filtro_regex|-] [nproc]
Id: B|<allerte>|<caso>|<s0>|<vmc>|<modello>|<tasto>
  caso: N = senza Black-Out (riferimento); a = Black-Out prima della memorizzazione; b = Black-Out dopo la memorizzazione,
        allerta che continua oltre il ritorno; c = allerta che finisce durante il Black-Out; d = velocita' scelta durante
        l'allerta e poi Black-Out (dN = stessa scelta senza Black-Out); e = allerta che inizia durante il Black-Out;
        f = Black-Out mentre l'allerta sta finendo (1 s dopo la fine)
  modello: B = base (al ritorno riparte a Velocita' 1 se non era ferma), R = riparte alla velocita' di prima, - = senza Black-Out
Coppie: P|<A>+<B>|<pat><caso>|<s0>|<vmc>|<modello>|<tasto>"""
import sys, re, itertools
from alerts import A_ON, A_OFF
from gen import base, add_alert, CONFLICT

ALERTS = ['CONG', 'DELTA', 'CO2', 'VOC', 'PDR']
MEMO = {'CONG': 0, 'DELTA': 4, 'CO2': 8, 'VOC': 8, 'PDR': 16}     # attesa di memorizzazione (s)
SPEEDS = [0, 1, 2, 3, 4, 6, 5, 7]
PRESS_D = [0, 1, 4, 6]

def add_bo(sc, t_off, t_on):
    sc['timeline'] += [(t_off, ('online', False)), (t_on, ('online', True))]

def mk(id_, vmc, s0, model, meta):
    sc = base(id_, vmc, s0, [('resume', True)] if model == 'R' else [])
    sc['meta'] = meta
    return sc

def singles():
    out = []
    for a in ALERTS:
        d = MEMO[a]
        for s0 in SPEEDS:
            for vmc in ('F', 'L'):
                # N: riferimento senza Black-Out
                sc = mk(f'B|{a}|N|{s0}|{vmc}|-|-', vmc, s0, '-', dict(case='N', alerts=[(a, 10, 250)], s0=s0, bo=None, press=None))
                add_alert(sc, a, 10, 250)
                sc['checks'] = [(60, 'during'), (240, 'pre_end')]; sc['end'] = 340
                out.append(sc)
                for p in PRESS_D:
                    if p == s0: continue
                    sc = mk(f'B|{a}|dN|{s0}|{vmc}|-|{p}', vmc, s0, '-', dict(case='dN', alerts=[(a, 10, 300)], s0=s0, bo=None, press=(40, p)))
                    add_alert(sc, a, 10, 300); sc['timeline'].append((40, ('press', p)))
                    sc['checks'] = [(30, 'during'), (75, 'after_press'), (260, 'after_ret'), (290, 'pre_end')]; sc['end'] = 400
                    out.append(sc)
                for model in ('B', 'R'):
                    # a: Black-Out prima della memorizzazione (CONG: la VMC va OFF-Line 1 s prima dell'allerta)
                    tbo = 9 if a == 'CONG' else 10 + d - 2
                    sc = mk(f'B|{a}|a|{s0}|{vmc}|{model}|-', vmc, s0, model, dict(case='a', alerts=[(a, 10, 300)], s0=s0, bo=(tbo, tbo + 100), press=None))
                    add_alert(sc, a, 10, 300); add_bo(sc, tbo, tbo + 100)
                    sc['checks'] = [(tbo + 60, 'bo'), (260, 'after_ret'), (290, 'pre_end')]; sc['end'] = 400
                    out.append(sc)
                    # b: Black-Out dopo la memorizzazione, l'allerta continua oltre il ritorno
                    sc = mk(f'B|{a}|b|{s0}|{vmc}|{model}|-', vmc, s0, model, dict(case='b', alerts=[(a, 10, 300)], s0=s0, bo=(60, 160), press=None))
                    add_alert(sc, a, 10, 300); add_bo(sc, 60, 160)
                    sc['checks'] = [(50, 'during'), (140, 'bo'), (260, 'after_ret'), (290, 'pre_end')]; sc['end'] = 400
                    out.append(sc)
                    # c: l'allerta finisce durante il Black-Out
                    sc = mk(f'B|{a}|c|{s0}|{vmc}|{model}|-', vmc, s0, model, dict(case='c', alerts=[(a, 10, 120)], s0=s0, bo=(60, 200), press=None))
                    add_alert(sc, a, 10, 120); add_bo(sc, 60, 200)
                    sc['checks'] = [(50, 'during'), (110, 'bo'), (190, 'bo_end')]; sc['end'] = 330
                    out.append(sc)
                    # e: l'allerta inizia durante il Black-Out (gia' rilevato) e continua oltre il ritorno
                    sc = mk(f'B|{a}|e|{s0}|{vmc}|{model}|-', vmc, s0, model, dict(case='e', alerts=[(a, 60, 300)], s0=s0, bo=(10, 130), press=None))
                    add_alert(sc, a, 60, 300); add_bo(sc, 10, 130)
                    sc['checks'] = [(5, 'before'), (120, 'bo'), (260, 'after_ret'), (290, 'pre_end')]; sc['end'] = 400
                    out.append(sc)
                    # f: Black-Out 1 s dopo la fine dell'allerta (durante l'attesa o il comando di fine allerta)
                    sc = mk(f'B|{a}|f|{s0}|{vmc}|{model}|-', vmc, s0, model, dict(case='f', alerts=[(a, 10, 100)], s0=s0, bo=(101, 201), press=None))
                    add_alert(sc, a, 10, 100); add_bo(sc, 101, 201)
                    sc['checks'] = [(90, 'during'), (180, 'bo')]; sc['end'] = 330
                    out.append(sc)
                    # d: velocita' scelta durante l'allerta (40 s), poi Black-Out 80-180 s, fine allerta 300 s
                    for p in PRESS_D:
                        if p == s0: continue
                        sc = mk(f'B|{a}|d|{s0}|{vmc}|{model}|{p}', vmc, s0, model, dict(case='d', alerts=[(a, 10, 300)], s0=s0, bo=(80, 180), press=(40, p)))
                        add_alert(sc, a, 10, 300); add_bo(sc, 80, 180); sc['timeline'].append((40, ('press', p)))
                        sc['checks'] = [(30, 'during'), (75, 'after_press'), (160, 'bo'), (260, 'after_ret'), (290, 'pre_end')]; sc['end'] = 400
                        out.append(sc)
    return out

def extra():
    """g = Black-Out subito dopo il comando di fine allerta (comando in volo con la VMC lenta);
    h = velocita' scelta 10 s dopo il ritorno della corrente (prima del ripristino), allerta in corso;
    i = velocita' scelta 60 s dopo il ritorno (dopo il ripristino), allerta in corso"""
    out = []
    ENDW = {'CONG': 0, 'DELTA': 4, 'CO2': 8, 'VOC': 8, 'PDR': 16}
    for a in ALERTS:
        for vmc in ('F', 'L'):
            for model in ('B', 'R'):
                for s0 in SPEEDS:
                    tb = 100 + ENDW[a] + 1
                    sc = mk(f'B|{a}|g|{s0}|{vmc}|{model}|-', vmc, s0, model, dict(case='g', alerts=[(a, 10, 100)], s0=s0, bo=(tb, tb + 100), press=None))
                    add_alert(sc, a, 10, 100); add_bo(sc, tb, tb + 100)
                    sc['checks'] = [(90, 'during'), (tb + 60, 'bo')]; sc['end'] = tb + 220
                    out.append(sc)
                for s0 in (0, 2, 6):
                    for p in (0, 4):
                        if p == s0: continue
                        for case, tp in (('h', 170), ('i', 220)):
                            sc = mk(f'B|{a}|{case}|{s0}|{vmc}|{model}|{p}', vmc, s0, model, dict(case=case, alerts=[(a, 10, 330)], s0=s0, bo=(60, 160), press=(tp, p)))
                            add_alert(sc, a, 10, 330); add_bo(sc, 60, 160); sc['timeline'].append((tp, ('press', p)))
                            sc['checks'] = [(50, 'during'), (140, 'bo'), (300, 'after_ret'), (320, 'pre_end')]; sc['end'] = 430
                            out.append(sc)
    return out

def pairs():
    out = []
    for A, B in itertools.permutations(ALERTS, 2):
        if {A, B} in CONFLICT: continue
        if {A, B} == {'CONG', 'DELTA'}: continue
        for pat in ('O', 'N'):          # O: A finisce per prima; N: B finisce per prima
            for s0 in (0, 2, 6):
                for vmc in ('F', 'L'):
                    def tl(case):
                        if case == 'c':  # quella che finisce per prima finisce durante il Black-Out (110-210)
                            return [(A, 10, 150), (B, 60, 360)] if pat == 'O' else [(A, 10, 360), (B, 60, 150)]
                        return [(A, 10, 300), (B, 60, 360)] if pat == 'O' else [(A, 10, 360), (B, 60, 300)]
                    cases = [('-', '-', None)] + [(m, c, None) for m in ('B', 'R') for c in ('b', 'c')] + [(m, 'd', p) for m in ('B', 'R') for p in (0, 4) if p != s0]
                    for model, case, p in cases:
                        cname = 'N' if model == '-' else case
                        al = tl(case if model != '-' else 'b')
                        id_ = f'P|{A}+{B}|{pat}{cname}|{s0}|{vmc}|{model}|' + ('-' if p is None else str(p))
                        sc = mk(id_, vmc, s0, model, dict(case=cname, alerts=al, s0=s0, bo=None if model == '-' else (110, 210), press=None if p is None else (85, p), pair=True))
                        for (n, t1, t2) in al: add_alert(sc, n, t1, t2)
                        if model != '-': add_bo(sc, 110, 210)
                        if p is not None: sc['timeline'].append((85, ('press', p)))
                        sc['checks'] = [(100, 'both'), (200, 'bo'), (280, 'after_ret'), (340, 'one_left')]; sc['end'] = 460
                        out.append(sc)
    return out

def scen():
    return singles() + extra() + pairs()

if __name__ == '__main__':
    import runner
    scs = scen()
    if len(sys.argv) > 3 and sys.argv[3] != '-':
        pat = re.compile(sys.argv[3]); scs = [s for s in scs if pat.search(s['id'])]
    ids = [s['id'] for s in scs]; assert len(ids) == len(set(ids))
    import os
    if os.environ.get('BO_ORDER'):   # prima i casi con Black-Out di tutte le allerte, poi le scelte dell'utente, poi i riferimenti
        pri = {c: i for i, c in enumerate(os.environ['BO_ORDER'].split(','))}
        scs.sort(key=lambda s: pri.get(s['meta']['case'], 99))
    print('scenari', len(scs), flush=True)
    if len(sys.argv) > 2:
        runner.run_all(scs, sys.argv[1], nproc=int(sys.argv[4]) if len(sys.argv) > 4 else 1, cfg=sys.argv[2])
