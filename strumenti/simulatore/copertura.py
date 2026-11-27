"""Quali automazioni e script del package hanno girato negli scenari di uno o piu' file di risultati.

Uso:  python copertura.py <risultati.jsonl> [<altri risultati.jsonl> ...] [--trigger]

Dalla traccia (tracce.py): un'automazione ha girato se la sua entita' cambia (attributi last_triggered /
current), uno script se il suo stato diventa 'on'. Automazioni e script che non girano mai negli scenari
scelti non sono provati dal differenziale. La riga '__avvio__' (avvio e riscaldamento) e' contata a parte.
Con piu' file i conteggi si sommano (per esempio un giro dei 17.264 scenari e uno della famiglia M).

--trigger: anche i trigger (id) dell'Automazione VMC Master scattati nella timeline degli scenari (campo
'trig' del runner, registrato dalla preparazione in poi esclusa) e quelli mai scattati. Gli id sono quelli
del file dell'automazione installato (build_config, dal repository di questo simulatore). Ogni ramo della
scelta principale dell'automazione corrisponde a uno o piu' id.
"""
import collections
import json
import sys
from pathlib import Path

import tracce


def id_trigger_principale():
    """Id dei trigger dell'Automazione VMC Master, nell'ordine del file (installatore.genera_file)."""
    import yaml

    import build_config
    repo = Path(__file__).resolve().parents[2]
    inst = build_config.carica_installatore(repo)
    versione = json.loads((repo / 'custom_components/vmc_master/manifest.json').read_text(encoding='utf-8'))['version']
    testo = inst.genera_file(build_config.NOME, build_config.IP_PROVA, versione)[f'vmc_{build_config.NOME}_automazione.yaml']
    auto = yaml.load(testo, Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))['automation'][0]
    return list(dict.fromkeys(str(t.get('id')) for t in auto['triggers']))


def main(argv):
    con_trigger = '--trigger' in argv
    percorsi = [a for a in argv if a != '--trigger']
    tutte = set(); avvio = collections.Counter(); scen = collections.Counter(); trig = collections.Counter(); n = 0
    for percorso in percorsi:
        with open(percorso, encoding='utf-8') as f:
            for riga in f:
                r = json.loads(riga)
                if 'error' in r:
                    continue
                d = tracce.decomprimi(r)
                if r['id'] == '__avvio__':
                    tutte |= {x[0] for x in d.get('iniziale', []) if x[0].split('.')[0] in ('automation', 'script')}
                visti = set()
                for v in d['tr']:
                    if v[0] != 'S':
                        continue
                    dom = v[2].split('.')[0]
                    if dom == 'automation' or (dom == 'script' and v[3] == 'on'):
                        visti.add(v[2])
                if r['id'] == '__avvio__':
                    avvio.update(visti)
                else:
                    n += 1; scen.update(visti); trig.update({s for _, s in r.get('trig', [])})
    print(f"{n} scenari in {', '.join(percorsi)}\n")
    for dom in ('automation', 'script'):
        elenco = sorted(e for e in tutte if e.startswith(dom + '.'))
        mai = [e for e in elenco if not scen[e] and not avvio[e]]
        solo_avvio = [e for e in elenco if not scen[e] and avvio[e]]
        print(f"{dom}: {len(elenco)}, mai eseguiti: {len(mai)}, solo nell'avvio: {len(solo_avvio)}")
        for e in elenco:
            print(f"  {scen[e]:>6} scenari{'  + avvio' if avvio[e] else '         '}  {e}")
        print()
    if con_trigger:
        ids = id_trigger_principale()
        mai = [i for i in ids if not trig[i]]
        print(f"trigger dell'Automazione VMC Master: {len(ids)} id, scattati negli scenari {len(ids) - len(mai)}, "
              f"mai {len(mai)}")
        for i in ids:
            print(f"  {trig[i]:>6} scenari  {i}")
        altri = sorted(set(trig) - set(ids))
        if altri:
            print(f"  id non nel file dell'automazione: {altri}")


if __name__ == '__main__':
    main(sys.argv[1:])
