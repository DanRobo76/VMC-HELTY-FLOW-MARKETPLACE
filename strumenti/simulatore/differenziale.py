"""Prova differenziale: gli stessi scenari con la variante A (di base «identica», cioe' automazioni e script
YAML di oggi) e con la variante B, poi il confronto delle tracce scenario per scenario (confronta.py).

Uso:
  python differenziale.py <cartella_uscita> <regex|@file_id> [n_campione] [nproc] --variante <modulo B>
                          [--variante-a <modulo A>] [--cfg <cfg di base>] [--coda <s>] [opzioni di confronta.py]

  regex / @file_id / n_campione: come targeted.py (regex cercata nell'id, «|» da scrivere «\\|»;
      n_campione 0 = tutti, altrimenti campione casuale con seme 1); nproc di base 4
  --variante: modulo della variante B (nome importabile come varianti.identica, o file .py)
  --cfg: configurazione di base gia' fatta con build_config.py; senza, la crea dal repository in
      <cartella_uscita>/cfg_base
  --coda: secondi virtuali registrati nella traccia dopo la fine di ogni scenario (di base 0; per esempio
      120 per vedere anche comandi o cambi di stato che arrivano dopo 'end')
Nella cartella di uscita: scenari.ids (gli id lanciati, uguali per A e B), cfg_A e cfg_B (copie della
configurazione di base passate a prepara_configurazione di ogni variante), A.jsonl / B.jsonl (risultati),
A.log / B.log, rapporto.txt (+ .json, .diversi.ids). Rilanciato con gli stessi argomenti riprende i giri
interrotti (il runner salta gli id gia' scritti) e rifa' il confronto.
Codice di uscita: 0 se nessuna differenza, 1 se ci sono differenze, 2 se un giro non e' finito.
"""
import os
import shutil
import subprocess
import sys
import time

_ora = time.time   # tempo reale (runner e tracce importano vclock, che sostituisce time.time con l'orologio virtuale)

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)


def copia_cfg(base, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(base, dest, ignore=shutil.ignore_patterns('.storage', 'home-assistant.log*', '__pycache__', 'deps'))


def giro(nome, uscita, cfg, ids, nproc, variante, coda='0'):
    out = os.path.join(uscita, f'{nome}.jsonl'); log = os.path.join(uscita, f'{nome}.log')
    cmd = [sys.executable, os.path.join(QUI, 'targeted.py'), out, cfg, '@' + ids, '0', str(nproc), '--variante', variante, '--coda', str(coda)]
    env = dict(os.environ, PYTHONHASHSEED='0')
    t = _ora()
    with open(log, 'a') as f:
        f.write(f"=== {time.strftime('%Y-%m-%d %H:%M:%S')} {' '.join(cmd)}\n"); f.flush()
        rc = subprocess.call(cmd, cwd=QUI, env=env, stdout=f, stderr=subprocess.STDOUT)
    return out, rc, _ora() - t


def main(argv):
    import confronta
    argv = list(argv)
    def opzione(nome, default=None):
        if nome in argv:
            i = argv.index(nome); v = argv[i + 1]; del argv[i:i + 2]; return v
        return default
    var_b = opzione('--variante'); var_a = opzione('--variante-a', 'varianti.identica'); cfg = opzione('--cfg')
    coda = opzione('--coda', '0')
    # le opzioni rimaste («--nome valore») sono di confronta.py
    pos = []; resto = []
    it = iter(argv)
    for x in it:
        if x.startswith('--'):
            resto += [x, next(it)]
        else:
            pos.append(x)
    if var_b is None or len(pos) < 2:
        print(__doc__); return 2
    uscita = os.path.abspath(pos[0]); sel = pos[1]
    n = int(pos[2]) if len(pos) > 2 else 0; nproc = int(pos[3]) if len(pos) > 3 else 4
    os.makedirs(uscita, exist_ok=True)
    opz = confronta.opzioni(con_file=False).parse_args(resto)
    if not opz.rapporto:
        opz.rapporto = os.path.join(uscita, 'rapporto.txt')
    if cfg is None:
        import build_config
        from pathlib import Path
        cfg = os.path.join(uscita, 'cfg_base')
        if not os.path.exists(os.path.join(cfg, 'SORGENTE.json')):
            info = build_config.costruisci(Path(cfg), Path(QUI).parents[1])
            print(f"configurazione di base: {cfg} (commit {info['commit']})", flush=True)
    cfg = os.path.abspath(cfg)
    ids = os.path.join(uscita, 'scenari.ids')
    if not os.path.exists(ids):
        os.environ.setdefault('PYTHONHASHSEED', '0')
        import targeted   # solo la scelta degli scenari (targeted.scegli), stessa sintassi
        scs = targeted.scegli(sel, n)
        with open(ids, 'w') as f:
            f.write(''.join(s['id'] + '\n' for s in scs))
    nsc = sum(1 for _ in open(ids))
    print(f"scenari: {nsc} (in {ids}); A = {var_a}, B = {var_b}; {nproc} processi", flush=True)
    import runner
    risultati = {}
    for nome, var in (('A', var_a), ('B', var_b)):
        c = os.path.join(uscita, f'cfg_{nome}')
        if not os.path.exists(os.path.join(c, '.preparata')):
            copia_cfg(cfg, c)
            mod = runner.carica_variante(var)
            if hasattr(mod, 'prepara_configurazione'):
                mod.prepara_configurazione(c)
            open(os.path.join(c, '.preparata'), 'w').write(var + '\n')
        out, rc, dt = giro(nome, uscita, c, ids, nproc, var, coda)
        fatti = len(confronta.indicizza(out)) - 1 if os.path.exists(out) else 0
        print(f"giro {nome}: {fatti}/{nsc} scenari in {dt:.0f} s ({fatti / dt if dt else 0:.2f} scenari/s), codice {rc}", flush=True)
        risultati[nome] = (out, rc, fatti)
    if any(rc != 0 or fatti < nsc for _, rc, fatti in risultati.values()):
        print("un giro non e' finito: rilanciare con gli stessi argomenti per riprendere", flush=True)
        return 2
    riep = confronta.scrivi_rapporto(risultati['A'][0], risultati['B'][0], opz)
    print(f"confronto: {riep['comuni']} in comune, identici {riep['identici']}, diversi {riep['diversi']}; "
          f"rapporto in {opz.rapporto}", flush=True)
    return 0 if riep['diversi'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
