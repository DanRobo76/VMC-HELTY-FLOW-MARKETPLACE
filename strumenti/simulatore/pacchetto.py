"""Aiuti per le varianti: leggere e modificare i file del package nella configurazione del simulatore.

Esempio (variante del motore nativo, in prepara_configurazione):
    import pacchetto
    pacchetto.togli(cfg_dir, automazioni='tutte', script='tutti')

I file modificati si riscrivono dal YAML letto (commenti e formattazione si perdono, gli alias come
«*vmc_master_entita_escluse_recorder» diventano copie del valore): dopo la scrittura il file si rilegge
e deve dare gli stessi dati, tolte le parti richieste. La variante «riscritta» (varianti/riscritta.py)
riscrive i file senza togliere niente: il differenziale contro «identica» prova che la riscrittura
non cambia il comportamento.
"""
import os
from pathlib import Path

import yaml

_LOADER = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)


class _Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def _rappresenta_testo(d, s):
    # testi su piu' righe (modelli Jinja) in stile letterale «|», come build_config della b36; PyYAML passa da
    # solo alle virgolette se lo stile letterale non puo' rappresentare il testo
    return d.represent_scalar('tag:yaml.org,2002:str', s, style='|' if '\n' in s else None)


_Dumper.add_representer(str, _rappresenta_testo)


def cartella_vmc(cfg_dir, nome='master') -> Path:
    return Path(cfg_dir) / 'packages' / 'vmc_helty_flow' / nome


def file_package(cfg_dir, nome='master'):
    """File YAML del package della VMC (vmc_master.yaml, vmc_master_automazione.yaml)."""
    return sorted(cartella_vmc(cfg_dir, nome).glob('*.yaml'))


def leggi(percorso):
    with open(percorso, encoding='utf-8') as f:
        return yaml.load(f, Loader=_LOADER)


def scrivi(percorso, dati, atteso=None):
    """Scrive dati come YAML; poi lo rilegge e controlla che sia uguale ad atteso (di base: dati)."""
    testo = yaml.dump(dati, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=10 ** 9)
    with open(percorso, 'w', encoding='utf-8') as f:
        f.write(testo)
    if leggi(percorso) != (dati if atteso is None else atteso):
        raise RuntimeError(f'{percorso}: il YAML riscritto non rilegge gli stessi dati')


def togli(cfg_dir, automazioni=(), script=(), nome='master'):
    """Toglie dal package le automazioni (per id o alias) e gli script (per nome) indicati.
    automazioni='tutte' / script='tutti': tutte le automazioni / tutti gli script del package.
    Restituisce {'automazioni': [id tolti], 'script': [nomi tolti]}; errore se un nome chiesto non c'e'."""
    tolte, tolti = [], []
    for p in file_package(cfg_dir, nome):
        d = leggi(p); cambiato = False
        if isinstance(d, dict) and d.get('automation'):
            resta = []
            for a in d['automation']:
                if automazioni == 'tutte' or a.get('id') in automazioni or a.get('alias') in automazioni:
                    tolte.append(a.get('id') or a.get('alias')); cambiato = True
                else:
                    resta.append(a)
            d['automation'] = resta
        if isinstance(d, dict) and d.get('script'):
            for k in list(d['script']):
                if script == 'tutti' or k in script:
                    del d['script'][k]; tolti.append(k); cambiato = True
        if cambiato:
            scrivi(p, d)
    mancano = ([] if automazioni == 'tutte' else [a for a in automazioni if a not in tolte]) + \
              ([] if script == 'tutti' else [s for s in script if s not in tolti])
    if mancano:
        raise KeyError(f'non trovati nel package: {mancano}')
    return dict(automazioni=tolte, script=tolti)


def riscrivi(cfg_dir, nome='master'):
    """Riscrive ogni file del package dal YAML letto, senza cambiare i dati."""
    for p in file_package(cfg_dir, nome):
        scrivi(p, leggi(p))


def aggiungi_integrazione(cfg_dir, dominio, sorgente, config_yaml=None):
    """Copia un'integrazione (cartella con manifest.json) in <cfg>/custom_components/<dominio> e, se config_yaml
    e' dato (testo YAML, es. «dominio:\\n  opzione: 1\\n»), lo aggiunge in fondo a configuration.yaml
    (senza configurazione si puo' caricare anche solo con «dominio:»)."""
    import shutil
    dest = Path(cfg_dir) / 'custom_components' / dominio
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(sorgente, dest, ignore=shutil.ignore_patterns('__pycache__'))
    if config_yaml is not None:
        conf = Path(cfg_dir) / 'configuration.yaml'
        testo = conf.read_text(encoding='utf-8')
        conf.write_text(testo + ('' if testo.endswith('\n') else '\n') + config_yaml, encoding='utf-8')
    return dest
