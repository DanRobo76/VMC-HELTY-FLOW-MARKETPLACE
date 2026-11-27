"""Oracle: comportamento atteso dal Foglio Logiche (Ver. 8.5.0) e dalla descrizione dell'automazione v.8.5.1,
aggiornato alla b36 (Foglio Logiche del 21-11-2026, decisioni del proprietario del 21-11-2026: vedi C32_* e BO_* in fondo)."""
ONSET = {'CONG':0,'DELTA':4,'CO2':8,'VOC':8,'PDR':16,'UMIDA':28,'UMIDS':28,'BO':32,'FREEU':24}
ENDW  = {'CONG':0,'DELTA':4,'CO2':8,'VOC':8,'PDR':16,'UMIDA':28,'UMIDS':28,'BO':32,'FREEU':24}
INQ = ('CO2','VOC'); UMID = ('UMIDA','UMIDS')
SW_GROUP = {'CO2':'INQ','VOC':'INQ','PDR':'PDR','UMIDA':'UMID','UMIDS':'UMID','FREEU':'FREE'}
UMID_SPEED = 2
PRIO = ('BO','CONG','DELTA','CO2','VOC','PDR','FREEU','UMIDA','UMIDS')

class State:
    def __init__(s, s0):
        s.B = s0; s.umid_no_restart = False; s.umid_from0 = False; s.disabled = set(); s.panic = False
        s.inq_keep = False; s.pdr_before_inq = False; s.amb_final = set(); s.umid_amb = False

def eff(st, active):
    e = {a for a in active if SW_GROUP.get(a) not in st.disabled}
    if 'FREEU' in e and st.B != 7: e.discard('FREEU')   # la sospensione Free riguarda solo la VMC in Free Cool./Heat.
    return e

def steady(st, active, cal_speed=None):
    act = eff(st, active)
    if 'BO' in act: return {'OFF'}
    if 'CONG' in act: return {0}
    if 'DELTA' in act: return {1}
    if st.panic: return {0}
    in_cal = cal_speed is not None
    base = cal_speed if in_cal else st.B
    def lower():
        if 'PDR' in act: return {0}
        if 'FREEU' in act and base == 7:
            if any(u in act for u in UMID) and not in_cal: return {1}
            return {0}
        if any(u in act for u in UMID) and not in_cal and not st.umid_no_restart:
            if base == 0: return {UMID_SPEED}
            return {base}
        if any(u in act for u in UMID) and not in_cal and st.umid_amb and base == 0:
            return {0, UMID_SPEED}   # V0 scelta sotto un'allerta superiore: l'Umidita' puo' ripartire da V0 (V2) quando prende il controllo
        return {base}
    if any(i in act for i in INQ):
        if st.inq_keep: return {st.B}
        if 'PDR' in act and base != 0 and not in_cal:
            return {base}       # priorita' 3 (Inquinanti) sopra il Lim. Δ PdR: la VMC va alla velocita' in uso (Foglio, colonna Inquinanti)
        und = lower()
        res = {1 if v == 0 else v for v in und}
        if any(u in act for u in UMID) and base == 0 and not in_cal: res |= {1}
        return res
    return lower()

def top_alert(st, active):
    act = eff(st, active)
    for a in PRIO:
        if a in act: return a
    return None

def on_alert(st, a, active):
    if a in INQ and not any(i in active - {a} for i in INQ):
        st.pdr_before_inq = 'PDR' in eff(st, active)
    if a in UMID:
        st.umid_from0 = (st.B == 0)
        st.umid_no_restart = False; st.umid_amb = False

def off_alert(st, a, active):
    if a in INQ and not any(i in active for i in INQ): st.inq_keep = False

def apply_press(st, active, p):
    a = top_alert(st, active)
    umid_on = any(u in eff(st, active) for u in UMID)
    if a in ('CONG','PDR','FREEU'):
        if p != 0: st.B = p
    elif a == 'DELTA':
        st.B = p
    elif a in INQ:
        st.B = p
        st.inq_keep = (p != 0)
    elif a in UMID:
        if st.umid_from0:
            if p != 0: st.B = p
        else:
            st.B = p
    else:
        st.B = p
    if p == 0 and umid_on and not st.umid_from0:
        st.umid_no_restart = True; st.umid_amb = a not in UMID
    if p != 0: st.umid_amb = False
    if p != 0 and umid_on and st.umid_from0 and a not in UMID:
        st.amb_final.add(0)   # scelta fatta durante un'allerta superiore mentre l'Umidita' (partita da V0) e' in corso

# --- b36, C3-2 (decisione del proprietario 21-11-2026 «la velocita' scelta negli 8 s di attesa resta, come il PdR»;
# Foglio 21-11-2026 A28 NOTA 1: «N.B. UNA VELOCITA' SCELTA DURANTE L'ATTESA DELLA RIPRESA (8 SECONDI) RESTA E LA
# RIPRESA NON AVVIENE»). Fino alla b35 un tasto premuto tra la fine degli Inquinanti e la ripresa era «ambiguo»
# (valeva sia la scelta sia il ripristino); dalla b36 vale solo la scelta, salvo:
#  - Congelamento o Δ Temp. in corso alla fine dell'attesa (codice b36: condizione spie Congelamento/Δ spente);
#  - Velocita' 1 con il ripristino a Velocita' 0 (Inquinanti partiti da ferma): non conta come scelta (codice b36 e
#    Foglio E7/NOTA 1: la VMC era gia' a Velocita' 1 per gli Inquinanti);
#  - un'altra allerta Inquinanti ancora in corso (l'allerta non e' finita).
# Opzione Free esclusa (BRIEF-B36 punto 1, proposta «codice» dell'audit C3-2 approvata dal proprietario: «esclusa
# l'opzione Free, ha la sua logica di ripresa»): con la Free sospesa (allerta FREEU in corso) la scelta segue la
# ripresa Free (Foglio A29), quindi resta «ambigua» come prima.
# C32_ESCLUDE_FREE: il codice b36 (03cff0b, variabile vel_ripristino_inquinanti vuota per ogni memoria Free) esclude
# anche la VMC in Free Cool./Heat. a mese NON programmato (memoria spia_velocita_freecooling_co2_o_voc, Foglio E14),
# che non ha nessuna ripresa Free sua: la scelta negli 8 s viene sovrascritta dal comando Free Cool./Heat. Il Foglio
# (A28, senza eccezioni) e il motivo dell'esclusione («ha la sua ripresa») non valgono per questo caso, quindi
# l'oracolo segue il Foglio (False) e quei casi risultano «sbagliati» (S|CO2/VOC|7|*|E0..E6, 28 scenari).
# Mettere True solo se il proprietario conferma che anche la Free a mese non programmato e' esclusa.
C32_ESCLUDE_FREE = False

def c32_finestra(m, tp):
    """Allerta Inquinanti nella cui attesa di fine (8 s, prima della ripresa) cade il tasto premuto a tp, se la regola
    C3-2 vale (nessun Congelamento/Δ in corso alla fine dell'attesa e nessun'altra allerta Inquinanti in corso); se no None."""
    for al in m['alerts']:
        a, t_on, t_off = al[0], al[1], al[2]
        if a not in INQ or not (t_off <= tp < t_off + ENDW[a]): continue
        t_end = t_off + ENDW[a]
        other = [b for b in m['alerts'] if b is not al]
        if any(b[0] in INQ and b[1] + ONSET[b[0]] <= t_end < b[2] for b in other): continue
        if any(b[0] in ('CONG', 'DELTA') and b[1] + ONSET[b[0]] <= t_end < b[2] + ENDW[b[0]] for b in other): continue
        if any(b[0] == 'FREEU' and b[1] + ONSET[b[0]] <= tp < b[2] + ENDW[b[0]] for b in other): continue   # opzione Free esclusa
        return al
    return None

def c32_press(st, p):
    """True se il tasto nell'attesa di fine Inquinanti conta come scelta che resta (C3-2), False se vince il ripristino."""
    if st.B == 0 and p == 1: return False          # Velocita' 1 degli Inquinanti partiti da ferma: ripresa a Velocita' 0
    if st.B == 7 and C32_ESCLUDE_FREE: return False  # lettura del codice b36 (opzione Free esclusa)
    return True

# --- b36, velocita' scelta prima del ripristino del Black-Out (decisione del proprietario 21-11-2026 12:11Z, «la scelta
# prima del ripristino resta», fix SCELTA-RIPRISTINO; Foglio 21-11-2026 seconda revisione approvata alle 12:12Z, A23:
# «UNA VELOCITA' SCELTA PRIMA DEL RIPRISTINO RESTA E IL RIPRISTINO NON AVVIENE»). Fino alla b35 un tasto premuto tra il
# ritorno della corrente e il ripristino (attesa di 32 s) era «ambiguo» (valeva sia la scelta sia il ripristino, e la
# VMC tornava alla velocita' di prima); ora vale solo la scelta. Un tasto uguale alla velocita' con cui la VMC e'
# ripartita non e' una scelta visibile (analyze.py lo salta gia': la VMC non cambia) e il ripristino resta.
# BO_SCELTA_RESTA = False rimette la regola di prima (ambiguo), per esempio per rileggere la b35 o una b36 senza il fix.
BO_SCELTA_RESTA = True
# BO_V1_NON_SCELTA: la Velocita' 1 scelta in quell'attesa non conta come scelta (la VMC puo' ripartire da sola a
# Velocita' 1 dopo un Black-Out, quindi il codice non la distingue: fix SCELTA-RIPRISTINO nel commit d471a1e (b36,
# unito in deb9bc1), condizione «vel.state not in ['Velocità 1', ...]» in testa agli 8 rami «Black-Out Off», e
# tests/test_b36_scelta.py): il ripristino avviene. Il Foglio A23 non lo dice; mettere False se il codice cambia.
BO_V1_NON_SCELTA = True

def bo_finestra(m, tp):
    """Allerta Black-Out nella cui attesa di ripristino (32 s dal ritorno della corrente) cade il tasto premuto a tp."""
    if not BO_SCELTA_RESTA: return None
    for al in m['alerts']:
        if al[0] == 'BO' and al[2] <= tp < al[2] + ENDW['BO']: return al
    return None

def bo_press(p):
    """True se il tasto nell'attesa del ripristino del Black-Out conta come scelta che resta, False se vince il ripristino.
    (La Velocita' 1 con BO_V1_RESTA acceso la decide bo_v1_finestra in analyze.expected.)"""
    return not (p == 1 and BO_V1_NON_SCELTA and not BO_V1_RESTA)

# --- b36 578aeff, Velocita' 1 scelta prima del ripristino del Black-Out (decisione del proprietario del 21-11-2026 dopo la
# 22fa38a: «anche la Velocita' 1 scelta prima del ripristino resta»; Foglio A23; codice: ramo «Black-Out Scelta Vel. 1»
# con i suoi 2 trigger e tests/test_b36_scelta_v1.py). Nella finestra tra il ritorno ON-Line (visto da HA) e il
# ripristino la Velocita' 1 resta, come le altre velocita' (il ripristino non avviene):
#  - premuta dalla scheda/Telecomando di HA (shell_command con l'utente nel contesto: azione 'card_u' del simulatore),
#    anche con la VMC gia' a Velocita' 1;
#  - premuta da qualsiasi fonte quando la lettura passa a 1 da un'altra velocita' (modello R che riparte alla velocita' di
#    prima, VMC rimasta a 0, oppure scelta 3 e poi 1).
# Non resta (il ripristino avviene) la Velocita' 1 dall'App/Telecomando fisico con la VMC gia' a 1 (modello base):
# analyze.expected la salta gia' (la VMC non cambia). Con BO_V1_RESTA spento (fino alla 22fa38a) la Velocita' 1 nella
# finestra non e' una scelta e annulla anche una scelta fatta prima nella stessa attesa (vince il ripristino).
# Zona grigia (accettati i due esiti): tasto dopo il ritorno della corrente ma prima che HA veda la VMC ON-Line (il codice
# lo perde: entrambi i trigger chiedono la VMC ON-Line; per le altre velocita' vale invece la tolleranza di 20 s prima
# del ritorno ON-Line). Senza la registrazione 'ip' del runner (risultati fatti prima del 21-11-2026 16:00) la zona grigia
# sono i primi 15 s dopo il ritorno della corrente (ping ogni 10 s + 4 s di timeout + lettura ogni 5 s).
BO_V1_RESTA = True
BO_V1_GRIGIA_SENZA_IP = 15
# b36 99e0c68 (BO_V1_LETTURA): la condizione del ramo «Black-Out Scelta Vel. 1» accetta anche la lettura grezza gia' valida
# prima che HA veda la VMC ON-Line («... or states('sensor.vmc_master_status_ventola') not in ['unavailable', 'unknown',
# '']»; come la tolleranza di 20 s degli 8 rami): la finestra della Velocita' 1 comincia alla prima lettura grezza valida
# dopo il Black-Out (campo 'raw' del runner) e la zona grigia resta solo per il tasto con la VMC che non risponde ancora
# (lettura grezza unavailable: la lettura passa da unavailable a 00001 e il codice non la vede). Senza i campi 'raw'/'ip'
# (risultati fatti prima del 21-11-2026 16:00) la zona grigia sono i primi BO_V1_GRIGIA_SENZA_LETTURA s (lettura ogni 5 s).
BO_V1_LETTURA = True
BO_V1_GRIGIA_SENZA_LETTURA = 6

# --- b36 15c5740 (8527150), ritorno della Fascia del Calendario dopo un Black-Out (ramo calendario_ritorno_da_black_out;
# Foglio A23, come il ripristino fuori dalle Fasce): una velocita' scelta dopo il ritorno della corrente e prima del ritorno
# della Fascia resta e la Fascia non riparte; la Velocita' 1 dalla scheda o la lettura che passa a 1 da un'altra velocita'
# spegne la Spia Black-Out del Calendario (ramo «Black-Out Scelta Vel. 1»): la Fascia non riparte. La Velocita' 1 dall'App
# con la VMC gia' a 1 non e' riconoscibile: la Fascia riparte. Fino alla 578aeff la Fascia ripartiva sempre.
# (Non simulato: il ritorno durante il riallineamento al riavvio e la guardia della fase dopo un riavvio di HA.)
BO_CAL_SCELTA_RESTA = True

def bo_fascia(m, al):
    """Fascia del Calendario (a1, a2, v) in cui e' cominciato il Black-Out al, o None."""
    for f in (m.get('cal') or []):
        if f[0] <= al[1] < f[1]: return f
    return None

def bo_v1_finestra(m, tp, res=None):
    """Per la Velocita' 1 premuta a tp con BO_V1_RESTA: 'scelta' (resta), 'grigia' (due esiti) o None (fuori finestra)."""
    if not (BO_V1_RESTA and BO_SCELTA_RESTA): return None
    for al in m['alerts']:
        if al[0] != 'BO' or tp < al[2]: continue
        if bo_fascia(m, al) and not BO_CAL_SCELTA_RESTA: continue   # fino alla 578aeff: nel Calendario la Fascia riparte
        t_ol = None
        if res is not None and res.get('ip') is not None:
            t_ol = next((t for t, s in res['ip'] if t >= al[2] - 1e-6 and s == 'ON-Line'), None)
            if t_ol is None: return 'grigia' if tp < al[2] + ENDW['BO'] else None
        else:
            if tp < al[2] + (BO_V1_GRIGIA_SENZA_LETTURA if BO_V1_LETTURA else BO_V1_GRIGIA_SENZA_IP): return 'grigia'
            if tp < al[2] + ENDW['BO']: return 'scelta'
            continue
        t_ini = t_ol
        if BO_V1_LETTURA and res.get('raw') is not None:   # dalla 99e0c68: basta la lettura grezza valida
            t_rv = next((t for t, s in res['raw'] if t >= al[2] - 1e-6 and s not in ('unavailable', 'unknown', '')), None)
            if t_rv is not None: t_ini = min(t_ini, t_rv)
        if tp < t_ini: return 'grigia'
        if tp < t_ol + ENDW['BO']: return 'scelta'
    return None

def configura_da_cfg(cfg):
    """Imposta gli interruttori dal package simulato (cfg/packages/vmc.yaml): BO_V1_RESTA se c'e' il ramo «Black-Out
    Scelta Vel. 1» (dalla 578aeff), BO_SCELTA_RESTA se c'e' lo stop «Velocita' scelta dall'utente dopo il ritorno della
    corrente mantenuta» (dalla d471a1e), BO_CAL_SCELTA_RESTA se c'e' lo stop «... (la Fascia non riparte)» (dalla 15c5740), BO_V1_LETTURA se la condizione del
    ramo «Black-Out Scelta Vel. 1» accetta la lettura grezza valida (dalla 99e0c68)."""
    global BO_V1_RESTA, BO_SCELTA_RESTA, BO_CAL_SCELTA_RESTA, BO_V1_LETTURA
    import os
    # tutti i file YAML dei package (b36: packages/vmc.yaml; ora packages/vmc_helty_flow/master/*.yaml)
    t = ''
    for radice, _, nomi in sorted(os.walk(os.path.join(cfg, 'packages'))):
        for n in sorted(nomi):
            if n.endswith('.yaml'): t += open(os.path.join(radice, n), encoding='utf-8').read()
    BO_V1_RESTA = 'Black-Out Scelta Vel. 1' in t
    BO_SCELTA_RESTA = "scelta dall'utente dopo il ritorno della corrente mantenuta" in t
    BO_CAL_SCELTA_RESTA = "corrente mantenuta (la Fascia non riparte)" in t        # dalla 15c5740 (8527150)
    BO_V1_LETTURA = "or states('sensor.vmc_master_status_ventola') not in ['unavailable', 'unknown', ''])" in t   # dalla 99e0c68
    return dict(BO_V1_RESTA=BO_V1_RESTA, BO_SCELTA_RESTA=BO_SCELTA_RESTA, BO_CAL_SCELTA_RESTA=BO_CAL_SCELTA_RESTA,
                BO_V1_LETTURA=BO_V1_LETTURA)
