"""Crea la configurazione di Home Assistant per il simulatore dai file del package del repository.

I file sono quelli che l'integrazione installa per la VMC «master» (installatore.genera_file:
trasforma.package_per_vmc con rimuovi_sezioni_solo_master e l'IP, adatta_versione,
adatta_link_repository, automazione_come_package), scritti in
<cfg>/packages/vmc_helty_flow/master/ come fa l'integrazione, con configuration.yaml che carica
i package con «packages: !include_dir_named packages/» (come chiede il README).

I file sono identici byte per byte a quelli installati (md5 in <cfg>/SORGENTE.json). Le due parti
che il simulatore non puo' usare restano nel file e si spengono all'avvio (simlib.boot):
- la chiave «recorder:» non avvia il registro (vorrebbe un database e dei thread; i servizi
  recorder.* chiamati dal package sono finti);
- il sensore «platform: rest» della versione del repository non viene creato (andrebbe in rete),
  come nel simulatore della b36 che lo toglieva dal file.

Uso:  python build_config.py <cartella_cfg> [--repo <radice del repository>] [--ip 192.168.1.160]
      (senza --repo usa il repository che contiene questo file)
"""
import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
import types
from pathlib import Path

import yaml

QUI = Path(__file__).resolve().parent
IP_PROVA = '192.168.1.160'   # coerente con la risposta VMSL della VMC finta (fakevmc.tcp_update)
NOME = 'master'
_LOADER = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)


def carica_installatore(repo: Path):
    """Importa custom_components.vmc_master.installatore senza eseguire __init__.py dell'integrazione
    (che importerebbe mezzo Home Assistant): pacchetti sintetici con il solo __path__."""
    base = repo / 'custom_components'
    for nome, cartella in (('custom_components', base), ('custom_components.vmc_master', base / 'vmc_master')):
        mod = sys.modules.get(nome)
        if mod is None or list(getattr(mod, '__path__', [])) != [str(cartella)]:
            mod = types.ModuleType(nome); mod.__path__ = [str(cartella)]
            sys.modules[nome] = mod
    for nome in ('custom_components.vmc_master.const', 'custom_components.vmc_master.trasforma',
                 'custom_components.vmc_master.installatore'):
        sys.modules.pop(nome, None)
    return importlib.import_module('custom_components.vmc_master.installatore')


def configurazione_ha() -> str:
    return ("homeassistant:\n  name: sim\n  latitude: 44.2\n  longitude: 9.4\n  elevation: 0\n  unit_system: metric\n"
            "  time_zone: Europe/Rome\n  country: IT\n  packages: !include_dir_named packages/\n"
            "logger:\n  default: warning\n")


def costruisci(cfg: Path, repo: Path, ip: str = IP_PROVA) -> dict:
    inst = carica_installatore(repo)
    versione = json.loads((repo / 'custom_components/vmc_master/manifest.json').read_text(encoding='utf-8'))['version']
    file = inst.genera_file(NOME, ip, versione)
    cartella = cfg / 'packages' / 'vmc_helty_flow' / NOME
    if cfg.exists():
        import shutil
        shutil.rmtree(cfg)
    cartella.mkdir(parents=True)
    for nome_file, testo in file.items():
        with open(cartella / nome_file, 'w', encoding='utf-8', newline='') as f:
            f.write(testo)
    (cfg / 'configuration.yaml').write_text(configurazione_ha(), encoding='utf-8')
    try:
        commit = subprocess.run(['git', '-C', str(repo), 'rev-parse', '--short', 'HEAD'], capture_output=True,
                                text=True).stdout.strip()
        sporco = bool(subprocess.run(['git', '-C', str(repo), 'status', '--porcelain', '--',
                                      'custom_components/vmc_master'], capture_output=True, text=True).stdout.strip())
    except OSError:
        commit, sporco = '', None
    sorg = repo / 'custom_components/vmc_master/package'
    info = dict(repo=str(repo), commit=commit, modifiche_non_salvate=sporco, versione=versione, nome=NOME, ip=ip,
                md5_sorgenti={p.name: hashlib.md5(p.read_bytes()).hexdigest() for p in sorted(sorg.iterdir()) if p.is_file()},
                md5_installati={n: hashlib.md5(t.encode('utf-8')).hexdigest() for n, t in file.items()})
    (cfg / 'SORGENTE.json').write_text(json.dumps(info, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    d = yaml.load(file[f'vmc_{NOME}.yaml'], Loader=_LOADER); auto = yaml.load(file[f'vmc_{NOME}_automazione.yaml'], Loader=_LOADER)
    info['automazioni'] = len(d.get('automation', [])) + len(auto.get('automation', []))
    info['script'] = len(d.get('script', {}))
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('cfg')
    ap.add_argument('--repo', default=str(QUI.parents[1]))
    ap.add_argument('--ip', default=IP_PROVA)
    a = ap.parse_args()
    info = costruisci(Path(a.cfg).resolve(), Path(a.repo).resolve(), a.ip)
    print(f"ok: {a.cfg} dal commit {info['commit']}{' (con modifiche non salvate)' if info['modifiche_non_salvate'] else ''}, "
          f"versione {info['versione']}, IP {info['ip']}: {info['automazioni']} automazioni, {info['script']} script")


if __name__ == '__main__':
    main()
