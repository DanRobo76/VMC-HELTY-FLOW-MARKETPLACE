"""Scenario generator. Each scenario: runner fields + 'meta' for the oracle."""
import alerts, itertools, json
from alerts import A_ON, A_OFF, SW
SPEEDS = [0,1,2,3,4,6,5,7]           # 6=Notturna 5=Iperventilazione 7=Free
VMCS = {'F':0.5, 'L':6.0}             # VMC veloce / lenta (latenza di esecuzione del comando)
PANIC = 'script.vmc_master_bottone_panico'
CAL_SW = 'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario'
SPEED_OPT = {0:'Velocità 0',1:'Velocità 1',2:'Velocità 2',3:'Velocità 3',4:'Velocità 4',6:'Notturna',5:'Iperventilazione',7:'Free Cool./Heat.'}
CONFLICT = [{'CONG','DELTA'},{'CONG','PDR'},{'DELTA','PDR'},{'UMIDA','UMIDS'},{'PDR','UMIDS'}]

def base(id_, vmc, s0, extra_setup=()):
    return dict(id=id_, setup=[('latency', VMCS[vmc])] + list(extra_setup) + [('press', s0)], timeline=[], checks=[])

def add_alert(sc, a, t_on, t_off):
    sc['timeline'] += [(t_on, x) for x in A_ON[a]] + ([(t_off, x) for x in A_OFF[a]] if t_off is not None else [])

def fam_single():
    out = []
    for a in A_ON:
        for s0 in SPEEDS:
            for vmc in VMCS:
                presses = [None] + [(ph, p) for ph in ('W','A','E') for p in SPEEDS]
                if a == 'BO': presses = [None] + [('E', p) for p in SPEEDS]
                else: presses += [('Q', p) for p in SPEEDS]      # Q = tasto della scheda durante l'allerta
                for pr in presses:
                    id_ = f'S|{a}|{s0}|{vmc}|' + ('-' if pr is None else f'{pr[0]}{pr[1]}')
                    sc = base(id_, vmc, s0)
                    add_alert(sc, a, 10, 250)
                    meta = dict(fam='S', s0=s0, vmc=vmc, alerts=[(a, 10, 250)], presses=[])
                    if pr:
                        t = {'W':12,'A':60,'E':252,'Q':60}[pr[0]]
                        sc['timeline'].append((t, ('card' if pr[0]=='Q' else 'press', pr[1]))); meta['presses'].append((t, pr[1]))
                    sc['checks'] = [(150,'c150'),(240,'c240')]; sc['end'] = 460
                    sc['meta'] = meta; out.append(sc)
    return out

def fam_pairs():
    out = []
    names = list(A_ON)
    for A, B in itertools.permutations(names, 2):
        if {A,B} in CONFLICT: continue
        for pat in ('O','N'):
            tl = [(A,10,210),(B,110,310)] if pat=='O' else [(A,10,310),(B,110,210)]
            for s0 in SPEEDS:
                for vmc in VMCS:
                    presses = [None] + ([] if 'BO' in (A,B) else SPEEDS)
                    for p in presses:
                        id_ = f'P|{A}+{B}|{pat}|{s0}|{vmc}|' + ('-' if p is None else f'A{p}')
                        sc = base(id_, vmc, s0)
                        for (n, a1, a2) in tl: add_alert(sc, n, a1, a2)
                        meta = dict(fam='P', s0=s0, vmc=vmc, alerts=tl, presses=[])
                        if p is not None:
                            sc['timeline'].append((150, ('press', p))); meta['presses'].append((150, p))
                        sc['checks'] = [(100,'c100'),(200,'c200'),(300,'c300')]; sc['end'] = 460
                        sc['meta'] = meta; out.append(sc)
    return out

def fam_free():
    out = []
    for mode in 'HC':
        for s0 in SPEEDS:
            for inq in (False, True):
                for vmc in VMCS:
                    presses = [None] + [(ph, p) for ph in ('W','A','E') for p in SPEEDS]
                    for pr in presses:
                        id_ = f'F|{mode}|{s0}|{"I" if inq else "-"}|{vmc}|' + ('-' if pr is None else f'{pr[0]}{pr[1]}')
                        sc = base(id_, vmc, s0, alerts.free_setup(mode))
                        sc['timeline'] += [(10, x) for x in alerts.FREE_UNFAV[mode]] + [(210, x) for x in alerts.FREE_FAV[mode]]
                        al = [('FREEU', 10, 210)]
                        if inq:
                            sc['timeline'] += [(110, x) for x in A_ON['CO2']] + [(170, x) for x in A_OFF['CO2']]
                            al.append(('CO2', 110, 170))
                        meta = dict(fam='F', s0=s0, vmc=vmc, alerts=al, presses=[], free=mode)
                        if pr:
                            t = {'W':12,'A':60,'E':212}[pr[0]]
                            sc['timeline'].append((t, ('press', pr[1]))); meta['presses'].append((t, pr[1]))
                        sc['checks'] = [(105,'c105'),(160,'c160'),(200,'c200')]; sc['end'] = 420
                        sc['meta'] = meta; out.append(sc)
    return out

def cal_setup(v1, v2, gap):
    # fascia 1: minuti 1-5 (60-300 s); fascia 2: minuti 6-10 (360-600 s, intervallo minimo di 1 minuto) oppure 8-12 (480-720 s)
    k2a, k2b = (6, 10) if not gap else (8, 12)
    t0 = [('datetime_min','input_datetime.vmc_master_accensione_giovedi', 1), ('datetime_min','input_datetime.vmc_master_spegnimento_giovedi', 5),
          ('datetime_min','input_datetime.vmc_master_accensione_giovedi_2', k2a), ('datetime_min','input_datetime.vmc_master_spegnimento_giovedi_2', k2b)]
    setup = [('select','input_select.vmc_master_speed_1_fascia_calendario', SPEED_OPT[v1]), ('select','input_select.vmc_master_speed_2_fascia_calendario', SPEED_OPT[v2])]
    return setup, t0, (60*k2a, 60*k2b)

def fam_calendar():
    out = []
    for v1 in SPEEDS:
        for v2 in SPEEDS:
            for gap in (False, True):
                for s0 in (0, 2):
                    for vmc in VMCS:
                        id_ = f'C|{v1}|{v2}|{"G" if gap else "A"}|{s0}|{vmc}|-'
                        setup, t0a, (s2a, s2b) = cal_setup(v1, v2, gap)
                        sc = base(id_, vmc, s0, setup)
                        sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]
                        sc['align_minute'] = True
                        meta = dict(fam='C', s0=s0, vmc=vmc, alerts=[], presses=[], cal=[(60,300,v1),(s2a,s2b,v2)])
                        sc['checks'] = [(200,'c200'),(420 if gap else 330,'cgap'),(600 if gap else 500,'cf2')]; sc['end'] = 840
                        sc['meta'] = meta; out.append(sc)
    # allerta durante la fascia 1 / a cavallo delle 2 fasce
    for a in A_ON:
        for v1 in SPEEDS:
            for span in ('in','cross'):
                for vmc in VMCS:
                    v2 = 3
                    id_ = f'C|{v1}|{v2}|A|0|{vmc}|{a}-{span}'
                    setup, t0a, (s2a, s2b) = cal_setup(v1, v2, False)
                    sc = base(id_, vmc, 0, setup)
                    sc['setup_t0'] = t0a + [('switch', CAL_SW, True)]; sc['align_minute'] = True
                    ta = (100, 230) if span == 'in' else (200, 470)
                    add_alert(sc, a, *ta)
                    meta = dict(fam='C', s0=0, vmc=vmc, alerts=[(a,)+ta], presses=[], cal=[(60,300,v1),(s2a,s2b,v2)])
                    chk = [(190,'c190'),(290,'c290'),(340,'c340'),(450,'c450'),(570,'c570')]
                    sc['checks'] = chk; sc['end'] = 840
                    sc['meta'] = meta; out.append(sc)
    return out

def fam_switch_panic():
    out = []
    for a in ['CO2','VOC','PDR','UMIDA','UMIDS']:
        for s0 in SPEEDS:
            for vmc in VMCS:
                for ph in ('W','A'):
                    for reon in (False, True):
                        id_ = f'W|{a}|{s0}|{vmc}|{ph}|{"R" if reon else "-"}'
                        sc = base(id_, vmc, s0); add_alert(sc, a, 10, 210)
                        t = 12 if ph == 'W' else 80
                        sc['timeline'].append((t, ('switch', SW[a], False)))
                        meta = dict(fam='W', s0=s0, vmc=vmc, alerts=[(a,10,210)], presses=[], switch=[(t, a, False)])
                        if reon:
                            sc['timeline'].append((300, ('switch', SW[a], True))); meta['switch'].append((300, a, True))
                        sc['checks'] = [(100,'c100'),(200,'c200'),(290,'c290')]; sc['end'] = 420
                        sc['meta'] = meta; out.append(sc)
    # interruttore Free durante la sospensione Free
    for mode in 'HC':
        sw = 'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_' + ('freeheating' if mode=='H' else 'freecooling')
        for s0 in SPEEDS:
            for vmc in VMCS:
                for ph in ('W','A'):
                    for inq in (False, True):
                        id_ = f'W|FREE{mode}|{s0}|{vmc}|{ph}|{"I" if inq else "-"}'
                        sc = base(id_, vmc, s0, alerts.free_setup(mode))
                        sc['timeline'] += [(10, x) for x in alerts.FREE_UNFAV[mode]] + [(210, x) for x in alerts.FREE_FAV[mode]]
                        al = [('FREEU', 10, 210)]
                        if inq:
                            sc['timeline'] += [(60, x) for x in A_ON['CO2']] + [(170, x) for x in A_OFF['CO2']]; al.append(('CO2', 60, 170))
                        t = 12 if ph == 'W' else 80
                        sc['timeline'].append((t, ('switch', sw, False)))
                        meta = dict(fam='W', s0=s0, vmc=vmc, alerts=al, presses=[], switch=[(t, 'FREEU', False)], free=mode)
                        sc['checks'] = [(100,'c100'),(160,'c160'),(200,'c200')]; sc['end'] = 420
                        sc['meta'] = meta; out.append(sc)
    # Bottone Panico durante ogni allerta (e senza allerta)
    for a in list(A_ON) + ['NONE']:
        for s0 in SPEEDS:
            for vmc in VMCS:
                for ph in ('W','A'):
                    id_ = f'K|{a}|{s0}|{vmc}|{ph}'
                    sc = base(id_, vmc, s0)
                    al = []
                    if a != 'NONE': add_alert(sc, a, 10, 210); al = [(a,10,210)]
                    t = 12 if ph == 'W' else 80
                    sc['timeline'].append((t, ('script', PANIC)))
                    meta = dict(fam='K', s0=s0, vmc=vmc, alerts=al, presses=[], panic=t)
                    sc['checks'] = [(100,'c100'),(200,'c200')]; sc['end'] = 420
                    sc['meta'] = meta; out.append(sc)
    return out

def fam_resume(fams):
    # stessi scenari con Black-Out, ma con la VMC che al ritorno della corrente riparte da sola alla velocita' di prima
    import copy
    out = []
    for v in fams.values():
        for sc in v:
            if any(al[0] == 'BO' for al in sc['meta']['alerts']):
                s2 = copy.deepcopy(sc); s2['id'] = 'R|' + sc['id']
                s2['setup'] = [('resume', True)] + s2['setup']; s2['meta']['resume'] = True
                out.append(s2)
    return out

def all_scenarios():
    fams = dict(S=fam_single(), P=fam_pairs(), F=fam_free(), C=fam_calendar(), W=fam_switch_panic())
    fams['R'] = fam_resume(fams)
    return fams

if __name__ == '__main__':
    f = all_scenarios()
    tot = 0
    for k, v in f.items(): print(k, len(v)); tot += len(v)
    print('tot', tot)
    ids = [s['id'] for v in f.values() for s in v]; assert len(ids) == len(set(ids))
