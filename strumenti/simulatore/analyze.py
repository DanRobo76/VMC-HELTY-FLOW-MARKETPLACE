import json, sys, collections, copy
import oracle
from oracle import State, steady, apply_press, ONSET, SW_GROUP, ENDW

def known_at(seen, t):
    k = None
    for ts, s in seen:
        if ts <= t: k = s
        else: break
    return k

def collisions(res):
    """Collisione: l'automazione invia un comando di velocita' diverso dal suo comando precedente
    senza aver mai riletto dalla VMC l'esito del precedente (nessun comando dell'utente, interruttore o script nel frattempo)."""
    cmds = [(l[0], int(l[2][-1])) for l in res['log'] if l[1]=='cmd' and l[3]=='ha' and l[2].startswith('000000')]
    seen = res['seen']; presses = [e[0] for e in res['events'] if e[1] in ('press','switch','script')]
    offline = [l[0] for l in res['log'] if l[1] in ('power','speed') and l[3] in ('power_off','power_on')]
    out = []
    for (ta, va), (tb, vb) in zip(cmds, cmds[1:]):
        if va == vb: continue
        if any(ta - 2 <= tp <= tb for tp in presses + offline): continue
        if known_at(seen, ta) == va or known_at(seen, tb) == va or any(ta < t <= tb and s == va for t, s in seen): continue
        out.append((ta, va, tb, vb))
    return out

def press_visible(res, tp, p):
    """Il comando manuale conta solo se Home Assistant ha potuto leggerlo (lettura VMGH con la VMC a quella velocita')."""
    log = res['log']
    # istante in cui la VMC e' passata a p per la pressione
    t_set = None
    for l in log:
        if l[1]=='speed' and l[0] >= tp - 1e-6 and l[2]==p and l[3] in ('user','cmd_user'):
            t_set = l[0]; break
    if t_set is None: return False
    t_change = min([l[0] for l in log if l[1]=='speed' and l[0] > t_set and l[2] != p] + [1e9])
    return any(t_set <= t <= t_change and s == p for t, s in res['seen'])

def expected(sc_meta, res, T, skip_press=()):
    m = sc_meta; st = State(m['s0'])
    evs = []
    for al in m['alerts']:
        a, t_on, t_off = al[0], al[1], al[2]
        evs.append((t_on + ONSET[a], 1, 'on', a)); evs.append((t_off, 0, 'off', a))
    for i, (tp, p) in enumerate(m.get('presses', [])):
        if i not in skip_press: evs.append((tp, 2, 'press', (p, i)))
    for (t, a, on) in m.get('switch', []):
        evs.append((t, 2, 'switch', (a, on)))
    if m.get('panic') is not None: evs.append((m['panic'], 2, 'panic', None))
    evs.sort(key=lambda e: (e[0], e[1]))
    active = set(); bo_snap = None; cal_scelta = None
    for t, _, k, x in evs:
        if t > T: break
        if k == 'on':
            active.add(x); oracle.on_alert(st, x, active)
        elif k == 'off':
            active.discard(x); oracle.off_alert(st, x, active)
        elif k == 'press':
            x, i = x
            src = (m.get('press_src') or [None] * (i + 1))[i]   # 'card_u' = scheda/Telecomando di HA (utente nel contesto)
            if x == 1 and oracle.bo_v1_finestra(m, t, res) and not bo_mem_v1(m, res, t):   # b36 578aeff: la Velocita' 1 resta
                if x == cur_speed_at(res, t - 0.01):
                    if src != 'card_u': continue                 # App/Telecomando fisico con la VMC gia' a 1: vince il ripristino
                elif not press_visible(res, t, x): continue
                apply_press(st, active, x); cal_scelta = cal_bo(m, t) or cal_scelta; continue
            if x == cur_speed_at(res, t - 0.01): continue
            if not press_visible(res, t, x): continue
            if oracle.c32_finestra(m, t) and not oracle.c32_press(st, x): continue   # b36 C3-2: vince il ripristino
            if oracle.bo_finestra(m, t):
                if not oracle.bo_press(x):                       # b36 A23 fino alla 22fa38a: la Velocita' 1 non e' una scelta
                    if bo_snap is not None: st = copy.deepcopy(bo_snap)   # e annulla la scelta fatta prima nell'attesa
                    continue
                if bo_snap is None: bo_snap = copy.deepcopy(st)
                cal_scelta = cal_bo(m, t) or cal_scelta          # b36 15c5740: nel Calendario la Fascia non riparte
            apply_press(st, active, x)
        elif k == 'switch':
            a, on = x
            grp = SW_GROUP[a]
            if not on:
                if a in oracle.eff(st, active): st.B = 0
                st.disabled.add(grp)
            else:
                st.disabled.discard(grp)
        elif k == 'panic':
            st.panic = True; st.B = 0
            st.disabled |= {'INQ','PDR','UMID','FREE'}
    cal_speed = None
    cal = m.get('cal')
    if cal:
        for (a1, a2, v) in cal:
            if a1 + 8 <= T < a2: cal_speed = v
            if cal_scelta == (a1, a2, v) and a1 + 8 <= T < a2: cal_speed = st.B   # scelta prima del ritorno della Fascia
        if cal_speed is None and T >= cal[0][0] + 8: st.B = 0   # fuori dalle fasce, dopo la prima, la VMC e' ferma
        if st.panic: cal_speed = None
    res = steady(st, active, cal_speed)
    if not active and st.amb_final: res = res | st.amb_final
    return res

def bo_mem_v1(m, res, t):
    """b36 578aeff: memoria del Black-Out a Velocita' 1 (VMC a 1 quando e' mancata la corrente, Spia velocita_1 accesa):
    la Velocita' 1 premuta dopo il ritorno coincide con il ripristino e non e' una scelta (codice: «spia velocita_1
    spenta»; come C3-2/E7: con gli Inquinanti partiti da ferma la VMC era gia' a 1). Non vale nel Calendario."""
    bos = [al for al in m['alerts'] if al[0] == 'BO' and al[2] <= t]
    if not bos: return False
    al = max(bos, key=lambda a: a[2])
    return not oracle.bo_fascia(m, al) and cur_speed_at(res, al[1] - 0.01) == 1

def cal_bo(m, t):
    """b36 15c5740: Fascia del Calendario nel cui ritorno dopo un Black-Out cade il tasto premuto a t (la scelta resta e la
    Fascia non riparte), o None (nessun Black-Out in una Fascia, oppure codice fino alla 578aeff: la Fascia riparte)."""
    if not (m.get('cal') and oracle.BO_CAL_SCELTA_RESTA): return None
    al = oracle.bo_finestra(m, t)
    return oracle.bo_fascia(m, al) if al else None

def ambiguous_presses(m, res=None):
    """Comandi manuali dati durante l'attesa di conferma della fine di un'allerta (prima che l'automazione ripristini):
    entrambi gli esiti (scelta dell'utente o ripristino) sono accettati."""
    out = []
    for i, (tp, p) in enumerate(m.get('presses', [])):
        for al in m['alerts']:
            a, t_on, t_off = al[0], al[1], al[2]
            if t_off <= tp <= t_off + ENDW[a] + 10:
                if a in oracle.INQ and oracle.c32_finestra(m, tp) is al: continue   # b36 C3-2: la scelta resta (non ambiguo)
                if a == 'BO' and oracle.bo_finestra(m, tp) is al: continue   # b36 A23: scelta prima del ripristino del Black-Out resta
                out.append(i)
        if p == 1 and oracle.bo_v1_finestra(m, tp, res) == 'grigia' and i not in out: out.append(i)   # b36 578aeff: zona grigia
    return tuple(out)

def cur_speed_at(res, t):
    sp = res['seen'][0][1] if res['seen'] else None
    for l in res['log']:
        if l[0] > t: break
        if l[1] == 'speed': sp = l[2]
    return sp

MODEL_DEP = []
def model_dependent(sc):
    return False  # 12-11-2026: utente -> dopo il Black-Out la VMC riparte in funzione del booleano acceso (velocita della fascia)
    # Black-Out dentro una fascia del Calendario con la VMC che al ritorno della corrente riparte a V1:
    # il Foglio dice che il Black-Out "non ha effetto" nel Calendario, quindi l'esito dipende dalla VMC reale.
    m = sc['meta']
    if m.get('cal') and not m.get('resume') and any(al[0]=='BO' for al in m['alerts']): return True
    return False

def check(sc, res):
    errs = []
    if 'error' in res: return ['ERRORE ' + res['error'][-200:]]
    for name, snap in res['snaps'].items():
        T = int(name[1:]) if name.startswith('c') and name[1:].isdigit() else (sc['end'] if name == 'final' else None)
        if name in ('cgap','cf2'): T = [c[0] for c in sc['checks'] if c[1]==name][0]
        exp = expected(sc['meta'], res, T)
        amb = ambiguous_presses(sc['meta'], res)
        if amb: exp = exp | expected(sc['meta'], res, T, skip_press=amb)
        got = 'OFF' if not snap[1] else snap[0]
        if got not in exp: errs.append((name, T, sorted(exp, key=str), got))
    return errs

if __name__ == '__main__':
    import gen
    if '--cfg' in sys.argv:   # interruttori dell'oracolo presi dal package simulato (vedi oracle.configura_da_cfg)
        i = sys.argv.index('--cfg'); print('oracolo configurato da', sys.argv[i + 1], oracle.configura_da_cfg(sys.argv[i + 1])); del sys.argv[i:i + 2]
    fams = gen.all_scenarios(); byid = {s['id']: s for v in fams.values() for s in v}
    tot = 0; ncoll = 0; nwrong = 0; per = collections.Counter(); perw = collections.Counter(); perc = collections.Counter()
    wrong = []; colls = []
    for line in open(sys.argv[1]):
        res = json.loads(line)
        if res['id'].startswith('__'): continue   # '__avvio__': traccia dell'avvio (runner.ID_AVVIO), non e' uno scenario
        sc = byid[res['id']]; tot += 1
        fam = res['id'].split('|')[0]; per[fam] += 1
        c = collisions(res) if 'error' not in res else []
        e = check(sc, res)
        if e and model_dependent(sc): MODEL_DEP.append((res['id'], e)); e = []
        if c: ncoll += 1; perc[fam] += 1; colls.append((res['id'], c))
        if e: nwrong += 1; perw[fam] += 1; wrong.append((res['id'], e))
    print('esiti dipendenti dal modello di VMC (Black-Out nel Calendario, esclusi):', len(MODEL_DEP))
    print('scenari', tot, 'con collisioni', ncoll, 'con esiti sbagliati', nwrong)
    for f in per: print(' ', f, per[f], 'coll', perc[f], 'sbagliati', perw[f])
    json.dump(dict(wrong=wrong, colls=colls), open(sys.argv[1] + '.analysis.json', 'w'), ensure_ascii=False)
    if len(sys.argv) > 2:
        for w in wrong[:int(sys.argv[2])]: print('W', w)
        for c in colls[:int(sys.argv[2])]: print('C', c)
