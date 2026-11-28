"""Confronto di due giri del simulatore (A e B), scenario per scenario.

Uso:  python confronta.py <a.jsonl> <b.jsonl> [--rapporto <file>] [--max-dettagli N] [--contesto N]
                          [--tolleranza S] [--ignora-tipi TIPI] [--ignora-entita REGEX] [--mappa CSV]

Per ogni scenario (id) presente in A o in B si confrontano:
- la traccia (tracce.py) voce per voce, nello stesso ordine: tipo, istante virtuale (uguale entro
  --tolleranza, di base 1e-6 s: l'unita' dell'arrotondamento), entita', stato, impronta degli
  attributi, forma del contesto, chiamate di servizio con i dati, registro della VMC, comandi di shell;
  per '__avvio__' anche lo stato di tutte le entita' della VMC dopo il setup (voci I) e al fork (voci F);
- l'istante virtuale dell'inizio della timeline (t0);
- i campi del runner della b36 (snaps, log, seen, events, raw, ip); non si confrontano 'trig' (trigger
  dell'automazione YAML: con il motore nativo non esiste) e 'real_s' (tempo reale).
Nessuna differenza e' tollerata: --ignora-tipi (es. R) e --ignora-entita servono solo per capire
una differenza, non per accettarla.

Con --mappa <csv della fase 1> (tests/nativa/motore/aiutanti_fase1.csv) il lato B e' l'integrazione
nativa (variante nativa4): prima del confronto le voci dei due lati passano dalla mappa dei nomi
(mappa.py: entity_id di oggi -> di domani dalla colonna «Domani», timer e valori interni nelle voci MS/MR
del motore, entita' senza corrispondente tolte); il rapporto elenca le voci tolte con i numeri esatti.

Il rapporto (in italiano) ha i conteggi (identici, diversi, mancanti, con errori; tipi di differenza;
famiglie) e, per ogni scenario diverso, la prima differenza con le voci intorno dei due lati.
Accanto al rapporto: <rapporto>.json (riepilogo) e <rapporto>.diversi.ids (id da rilanciare con
targeted.py @file). Codice di uscita: 0 se tutto identico, 1 se no.
"""
import argparse
import collections
import json
import re
import sys

import mappa as mappa_nomi
import tracce

CAMPI_SIM = ('snaps', 'log', 'seen', 'events', 'raw', 'ip')
NOMI_TIPI = dict(tracce.TIPI, I="stato dopo il setup (avvio)", F="stato al fork (avvio)",
                 ordine="stesse voci in ordine diverso", mancante="scenario presente in un solo giro",
                 errore="scenario finito con un errore", t0="inizio della timeline", coda="--coda diverso",
                 **mappa_nomi.TIPI_MOTORE)


def indicizza(percorso):
    """id -> posizione della riga nel file (se un id compare piu' volte vale l'ultima) e intestazione."""
    indice = {}
    with open(percorso, 'rb') as f:
        while True:
            pos = f.tell(); riga = f.readline()
            if not riga:
                break
            if not riga.strip():
                continue
            try:
                i = riga.index(b'"id": "') + 7
                indice[riga[i:riga.index(b'"', i)].decode('utf-8')] = pos
            except ValueError:
                try:
                    indice[json.loads(riga)['id']] = pos
                except Exception:   # riga troncata (giro interrotto): si ignora
                    pass
    return indice


def leggi(f, pos):
    f.seek(pos)
    return json.loads(f.readline())


def voci(res, opz, lato='A'):
    """Voci confrontabili di un risultato: traccia filtrata (+ istantanee per l'avvio) e tabella attributi."""
    d = tracce.decomprimi(res)
    v = [['I', 0.0] + x for x in d.get('iniziale', [])] + list(d.get('tr', []))
    if 'finale' in d:
        tf = res.get('t0', 0.0)
        v += [['F', tf] + x for x in d['finale']]
    attr = d.get('attr', {})
    if getattr(opz, 'mappa_nomi', None) is not None:
        v, attr = opz.mappa_nomi.applica(v, attr, lato)
    if opz.ignora_tipi:
        v = [x for x in v if x[0] not in opz.ignora_tipi]
    if opz.ignora_entita:
        r = re.compile(opz.ignora_entita)
        v = [x for x in v if not (x[0] in ('S', 'R', 'I', 'F', 'MS', 'MR') and r.search(x[2]))]
    if getattr(opz, 'ordine_esterno', False):
        v = ordine_esterno(v)
    return v, attr


def interna(x):
    """Una voce del motore che fuori dal motore non si vede: valori interni e timer (MS, MR) e
    stati delle logiche (S, R di automation.*)."""
    return x[0] in ('MS', 'MR') or (x[0] in ('S', 'R') and str(x[2]).startswith('automation.'))


def ordine_esterno(v):
    """--ordine-esterno: prima tutte le voci che si vedono fuori dal motore, nel loro ordine,
    poi le voci interne raggruppate per entita', ognuna nel suo ordine. Il confronto resta
    voce per voce: stesso ordine di tutto cio' che si vede (comandi, entita', servizi) e stessa
    sequenza (istanti, stati, contesti) di ogni valore interno; cambia solo il posto delle voci
    interne tra le altre allo stesso istante."""
    return [x for _, x in sorted(enumerate(v), key=lambda p: (1, str(p[1][2]), p[0]) if interna(p[1])
                                 else (0, '', p[0]))]


def uguale(a, b, tol):
    if len(a) != len(b) or a[0] != b[0]:
        return False
    if abs(a[1] - b[1]) > tol + 1e-12:
        return False
    return a[2:] == b[2:]


def descrivi(v):
    t = f"{v[1]:>12.6f}"
    k = v[0]
    if k in ('S', 'I', 'F', 'MS'):
        ctx = f", contesto {v[5]}" if k == 'S' and len(v) > 5 and v[5] else ''
        return f"{t} {k} {v[2]} = {v[3]!r}  [attr {v[4]}{ctx}]"
    if k in ('R', 'MR'):
        return f"{t} {k} {v[2]} (scrittura senza cambio" + (f", contesto {v[3]})" if len(v) > 3 and v[3] else ")")
    if k == 'C':
        return f"{t} C {v[2]}.{v[3]} {v[4]}" + (f"  [contesto {v[5]}]" if len(v) > 5 and v[5] else '')
    if k == 'E':
        return f"{t} E {v[2]}.{v[3]} {v[4]} -> {v[5]}"
    if k == 'V':
        return f"{t} V VMC {v[2]} {v[3]} (fonte {v[4]}, prima {v[5]})"
    if k == 'X':
        return f"{t} X shell: {v[2]}"
    return f"{t} {v}"


def differenze_attributi(da, db):
    chiavi = sorted(set(da) | set(db))
    out = []
    for c in chiavi:
        if da.get(c, '<assente>') != db.get(c, '<assente>'):
            out.append(f"      attributo {c!r}: A={json.dumps(da.get(c, '<assente>'), ensure_ascii=False)[:200]}"
                       f"  B={json.dumps(db.get(c, '<assente>'), ensure_ascii=False)[:200]}")
    return out


def chiave_ordine(x):
    return (round(x[1], 6), json.dumps(x, ensure_ascii=False))


def confronta_scenario(ra, rb, opz):
    """(tipi di differenza: set, righe di dettaglio: list) - set vuoto = identici."""
    tipi, det = set(), []
    if 'error' in ra or 'error' in rb:
        tipi.add('errore')
        for lato, r in (('A', ra), ('B', rb)):
            if 'error' in r:
                det.append(f"  errore in {lato}: " + r['error'].strip().splitlines()[-1][:300])
        return tipi, det
    if ra.get('coda', 0) != rb.get('coda', 0):
        tipi.add('coda'); det.append(f"  giri fatti con --coda diverso: A {ra.get('coda', 0)} s, B {rb.get('coda', 0)} s")
    if abs(ra.get('t0', 0) - rb.get('t0', 0)) > opz.tolleranza + 1e-12:
        tipi.add('t0'); det.append(f"  inizio della timeline diverso: A t0={ra.get('t0')}  B t0={rb.get('t0')}")
    va, aa = voci(ra, opz, 'A'); vb, ab = voci(rb, opz, 'B')
    n = min(len(va), len(vb)); i = 0
    while i < n and uguale(va[i], vb[i], opz.tolleranza):
        i += 1
    if i < n or len(va) != len(vb):
        ca = collections.Counter(json.dumps(x[:1] + [round(x[1], 6)] + x[2:], ensure_ascii=False) for x in va)
        cb = collections.Counter(json.dumps(x[:1] + [round(x[1], 6)] + x[2:], ensure_ascii=False) for x in vb)
        solo_a = ca - cb; solo_b = cb - ca
        for x in list(solo_a) + list(solo_b):
            tipi.add(json.loads(x)[0])
        if not solo_a and not solo_b:
            tipi.add('ordine')
        det.append(f"  traccia: {len(va)} voci in A, {len(vb)} in B; prima differenza alla voce {i + 1}"
                   + (f" (t={va[i][1] if i < len(va) else vb[i][1]})" if i < max(len(va), len(vb)) else ''))
        if not solo_a and not solo_b:
            det.append("  le voci sono le stesse: cambia solo l'ordine (allo stesso istante o tra istanti vicini)")
        else:
            per = collections.Counter()
            for x, c in solo_a.items(): per[(json.loads(x)[0], 'A')] += c
            for x, c in solo_b.items(): per[(json.loads(x)[0], 'B')] += c
            det.append("  voci senza corrispondente: " + ', '.join(
                f"{NOMI_TIPI.get(k, k)} solo in {lato}: {c}" for (k, lato), c in sorted(per.items())))
        lo = max(0, i - opz.contesto // 2); hi = i + opz.contesto // 2 + 1
        for lato, v in (('A', va), ('B', vb)):
            det.append(f"  --- {lato} (voci {lo + 1}-{min(hi, len(v))} di {len(v)})")
            for j in range(lo, min(hi, len(v))):
                det.append(("  >> " if j == i else "     ") + descrivi(v[j]))
            if i >= len(v):
                det.append("  >> (fine della traccia)")
        if i < n and va[i][0] in ('S', 'I', 'F', 'MS') and vb[i][0] == va[i][0] and va[i][2:4] == vb[i][2:4] and va[i][4] != vb[i][4]:
            det.append("  stessi entita' e stato, attributi diversi:")
            det += differenze_attributi(aa.get(va[i][4], {}), ab.get(vb[i][4], {}))
    for k in CAMPI_SIM:
        if json.dumps(ra.get(k), sort_keys=True) != json.dumps(rb.get(k), sort_keys=True):
            tipi.add('campo ' + k)
            det.append(f"  campo del runner {k!r} diverso:")
            det.append(f"     A: {json.dumps(ra.get(k), ensure_ascii=False)[:400]}")
            det.append(f"     B: {json.dumps(rb.get(k), ensure_ascii=False)[:400]}")
    return tipi, det


def intestazione(f, indice):
    if '__avvio__' in indice:
        r = leggi(f, indice['__avvio__'])
        return f"variante {r.get('variante')}, cfg {r.get('cfg')}"
    return 'senza riga __avvio__ (giro fatto senza tracce?)'


def confronta(path_a, path_b, opz, out=sys.stdout):
    opz.mappa_nomi = mappa_nomi.Mappa(opz.mappa) if getattr(opz, 'mappa', None) else None
    ia, ib = indicizza(path_a), indicizza(path_b)
    ids = sorted(set(ia) | set(ib), key=lambda i: (not i.startswith('__'), i))
    conti = collections.Counter(); per_tipo = collections.Counter(); fam = collections.defaultdict(lambda: [0, 0])
    diversi = []; dettagli = []
    with open(path_a, 'rb') as fa, open(path_b, 'rb') as fb:
        ha, hb = intestazione(fa, ia), intestazione(fb, ib)
        for sid in ids:
            f_ = sid.split('|')[0] if not sid.startswith('__') else sid
            if sid not in ia or sid not in ib:
                conti['solo_B' if sid not in ia else 'solo_A'] += 1
                diversi.append(sid); fam[f_][0] += 1; fam[f_][1] += 1; per_tipo['mancante'] += 1
                dettagli.append((sid, {'mancante'}, [f"  presente solo in {'B' if sid not in ia else 'A'}"]))
                continue
            tipi, det = confronta_scenario(leggi(fa, ia[sid]), leggi(fb, ib[sid]), opz)
            fam[f_][1] += 1
            if tipi:
                conti['diversi'] += 1; fam[f_][0] += 1; diversi.append(sid)
                for t in tipi: per_tipo[t] += 1
                if 'errore' in tipi: conti['errori'] += 1
                dettagli.append((sid, tipi, det))
            else:
                conti['identici'] += 1
    comuni = len(set(ia) & set(ib))
    w = out.write
    w("CONFRONTO DIFFERENZIALE DEL SIMULATORE VMC MASTER\n\n")
    w(f"A: {path_a}\n   {ha}\n   {len(ia)} risultati\n")
    w(f"B: {path_b}\n   {hb}\n   {len(ib)} risultati\n")
    w(f"Opzioni: tolleranza sugli istanti {opz.tolleranza} s; tipi ignorati: {opz.ignora_tipi or 'nessuno'}; "
      f"entita' ignorate: {opz.ignora_entita or 'nessuna'}\n")
    if opz.mappa_nomi is not None:
        w(f"Mappa dei nomi: {opz.mappa_nomi.descrizione()}\n")
        w("Voci tolte (o cambiate) dalla mappa in tutti gli scenari confrontati (numero, tipo, lato, motivo):\n")
        w('\n'.join(opz.mappa_nomi.elenco() or ['  nessuna']) + '\n')
    w("\n")
    w(f"Scenari in comune: {comuni} (compresa la riga __avvio__ se c'e')\n")
    w(f"  identici: {conti['identici']}\n  diversi:  {conti['diversi']}" +
      (f" (di cui con errori: {conti['errori']})" if conti['errori'] else '') + "\n")
    if conti['solo_A'] or conti['solo_B']:
        w(f"  solo in A: {conti['solo_A']}   solo in B: {conti['solo_B']}\n")
    esito = 'NESSUNA DIFFERENZA' if not diversi else f"{len(diversi)} SCENARI CON DIFFERENZE"
    w(f"\nESITO: {esito}\n")
    if per_tipo:
        w("\nTipi di differenza (numero di scenari):\n")
        for t, c in per_tipo.most_common():
            w(f"  {NOMI_TIPI.get(t, t)} [{t}]: {c}\n")
    w("\nFamiglie (con differenze / totale, mancanti compresi):\n")
    for f_ in sorted(fam):
        w(f"  {f_}: {fam[f_][0]} / {fam[f_][1]}\n")
    if dettagli:
        w(f"\nDETTAGLIO (prima differenza di ogni scenario, {opz.contesto} voci di contesto per lato)\n")
        w("Formato delle voci: istante, tipo (S cambio di stato, R scrittura senza cambio, C chiamata di servizio,\n"
          "E chiamata non riuscita, V registro della VMC, X comando di shell, I/F stato all'avvio/al fork), dati.\n")
        for sid, tipi, det in dettagli[:opz.max_dettagli]:
            w(f"\n=== {sid}   [{', '.join(sorted(tipi))}]\n")
            w('\n'.join(det) + '\n')
        if len(dettagli) > opz.max_dettagli:
            w(f"\n... altri {len(dettagli) - opz.max_dettagli} scenari diversi (elenco completo nel file .diversi.ids)\n")
    riep = dict(a=path_a, b=path_b, comuni=comuni, identici=conti['identici'], diversi=len(diversi),
                solo_a=conti['solo_A'], solo_b=conti['solo_B'], errori=conti['errori'],
                tipi=dict(per_tipo), famiglie={k: v for k, v in fam.items()}, ids_diversi=diversi)
    if opz.mappa_nomi is not None:
        riep['tolte_dalla_mappa'] = [{'lato': lato, 'motivo': motivo, 'tipo': tipo, 'voci': n}
                                     for (lato, motivo, tipo), n in sorted(opz.mappa_nomi.tolte.items())]
        riep['cambiate_dalla_mappa'] = [{'lato': lato, 'motivo': motivo, 'tipo': tipo, 'voci': n}
                                        for (lato, motivo, tipo), n in sorted(opz.mappa_nomi.cambiate.items())]
    return riep


def opzioni(argv=None, con_file=True):
    ap = argparse.ArgumentParser(description='Confronto di due giri del simulatore (A e B)')
    if con_file:
        ap.add_argument('a'); ap.add_argument('b')
    ap.add_argument('--rapporto', default=None, help="file del rapporto (senza: a schermo)")
    ap.add_argument('--max-dettagli', type=int, default=300)
    ap.add_argument('--contesto', type=int, default=10, help='voci di contesto per lato (di base 10)')
    ap.add_argument('--tolleranza', type=float, default=1e-6)
    ap.add_argument('--ignora-tipi', default='', help='tipi di voce da non confrontare, es. R (solo per indagare)')
    ap.add_argument('--ignora-entita', default='', help='regex di entity_id da non confrontare (solo per indagare)')
    ap.add_argument('--ordine-esterno', action='store_true',
                    help="voci interne del motore (MS, MR, stati delle logiche) confrontate per entita' "
                         "(il resto nello stesso ordine)")
    ap.add_argument('--mappa', default=None,
                    help="csv della fase 1 (colonna «Domani»): B e' l'integrazione nativa (variante nativa4)")
    return ap


def scrivi_rapporto(path_a, path_b, opz):
    if opz.rapporto:
        with open(opz.rapporto, 'w', encoding='utf-8') as out:
            riep = confronta(path_a, path_b, opz, out)
        with open(opz.rapporto + '.json', 'w', encoding='utf-8') as f:
            json.dump(riep, f, ensure_ascii=False, indent=1)
        with open(opz.rapporto + '.diversi.ids', 'w', encoding='utf-8') as f:
            f.write(''.join(i + '\n' for i in riep['ids_diversi'] if not i.startswith('__')))
    else:
        riep = confronta(path_a, path_b, opz, sys.stdout)
    return riep


if __name__ == '__main__':
    o = opzioni().parse_args()
    r = scrivi_rapporto(o.a, o.b, o)
    print(f"in comune {r['comuni']}: identici {r['identici']}; con differenze (mancanti compresi) {r['diversi']}"
          + (f" (rapporto in {o.rapporto})" if o.rapporto else ''), file=sys.stderr)
    sys.exit(0 if r['diversi'] == 0 else 1)
