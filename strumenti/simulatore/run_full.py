"""Tutti gli scenari di gen.py.  Uso: python run_full.py <out.jsonl> <cfg> [nproc] [--variante <modulo>] [--coda <s>]"""
import sys
import runner
runner.assicura_determinismo()
import gen
argv = list(sys.argv[1:]); variante = None; coda = 0
if '--variante' in argv:
    i = argv.index('--variante'); variante = argv[i + 1]; del argv[i:i + 2]
if '--coda' in argv:
    i = argv.index('--coda'); coda = float(argv[i + 1]); del argv[i:i + 2]
f = gen.all_scenarios()
scs = [s for v in f.values() for s in v]
print('scenari', len(scs), flush=True)
runner.run_all(scs, argv[0], nproc=int(argv[2]) if len(argv) > 2 else 4, cfg=argv[1], variante=variante, coda=coda)
