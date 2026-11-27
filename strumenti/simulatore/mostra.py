import json, sys
N = {0: 'V0', 1: 'V1', 2: 'V2', 3: 'V3', 4: 'V4', 5: 'Iper', 6: 'Nott', 7: 'Free'}
pat = sys.argv[2] if len(sys.argv) > 2 else ''
for line in open(sys.argv[1]):
    r = json.loads(line)
    if pat not in r['id'] or r['id'].startswith('__'): continue
    if 'error' in r:
        print(r['id'], 'ERRORE', r['error'][-300:]); continue
    ch = [f"{l[0]}:{N.get(l[2], l[2])}({l[3]})" for l in r['log'] if l[1] == 'speed']
    pw = [f"{l[0]}:{l[2]}" for l in r['log'] if l[1] == 'power']
    print(f"{r['id']:<22} finale={N[r['snaps']['final'][0]]:<5} velocità: {' '.join(ch)}" + (f"  power_off {pw}" if pw else ''))
