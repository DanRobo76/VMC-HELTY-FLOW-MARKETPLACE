"""Scenari scelti con un'espressione regolare sull'id (o un file di id) e lanciati con il runner.

Uso:  python targeted.py <out.jsonl> <cfg> <regex|@file_id> [n_campione] [nproc] [--variante <modulo>] [--coda <s>]
  regex: cercata nell'id (re.search); attenzione, «|» va scritto «\\|» per cercarlo alla lettera
  @file_id: file con un id per riga (o separati da spazi); cerca anche tra i 4.842 scenari Black-Out
  blackout: i 4.842 scenari Black-Out della b36 (famiglie_blackout.py); una regex non li prende mai
  n_campione: 0 = tutti, altrimenti un campione casuale (seme 1) di n scenari
  --variante: modulo della variante (vedi runner.carica_variante); senza: nessuna variante (come la b36)
  --coda: secondi virtuali registrati nella traccia dopo la fine di ogni scenario (di base 0)
"""
import sys
import runner
runner.assicura_determinismo()
import famiglie_blackout, gen, gen_mancanti, re, random


def scegli(sel, n=0):
    """Scenari di gen.py (i 17.264 fissi) e della famiglia M (gen_mancanti.py) scelti con la stessa sintassi di
    targeted.py (regex o @file), campione di n (seme 1). «blackout» sceglie i 4.842 scenari Black-Out, che un
    file di id trova anche mischiati agli altri; una regex resta sui 17.264 e sulla famiglia M (come prima)."""
    f = gen.all_scenarios()
    f['M'] = gen_mancanti.famiglia()
    random.seed(1)
    if sel == "blackout":
        f = {'BO': famiglie_blackout.famiglia()}; ok = lambda i: True
    elif sel.startswith("@"):
        f['BO'] = famiglie_blackout.famiglia()
        want = set(open(sel[1:]).read().split()); ok = lambda i: i in want
    else:
        pat = re.compile(sel); ok = lambda i: bool(pat.search(i))
    scs = [s for v in f.values() for s in v if ok(s["id"])]
    if n and len(scs) > n: scs = random.sample(scs, n)
    return scs


if __name__ == '__main__':
    argv = list(sys.argv[1:]); variante = None; coda = 0
    if '--variante' in argv:
        i = argv.index('--variante'); variante = argv[i + 1]; del argv[i:i + 2]
    if '--coda' in argv:
        i = argv.index('--coda'); coda = float(argv[i + 1]); del argv[i:i + 2]
    scs = scegli(argv[2], int(argv[3]) if len(argv) > 3 else 0)
    print('scenari', len(scs), flush=True)
    runner.run_all(scs, argv[0], nproc=int(argv[4]) if len(argv) > 4 else 4, cfg=argv[1], variante=variante, coda=coda)
