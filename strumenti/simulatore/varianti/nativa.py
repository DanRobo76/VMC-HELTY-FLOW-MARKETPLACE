"""Variante «nativa»: automazioni e script del package girano nel motore tradotto in Python (fase 3).

- prepara_configurazione toglie dal package tutte le automazioni e tutti gli script YAML
  (pacchetto.togli), copia l'integrazione vmc_master del repository in <cfg>/custom_components/vmc_master
  (solo per importare il motore: non è in configuration.yaml e non si avvia) e aggiunge un'integrazione
  minima, sim_motore_nativo, che nel proprio setup (durante l'avvio di Home Assistant, come l'integrazione
  automation per le automazioni YAML) crea con nativa/motore/ha.py le entità delle automazioni e degli
  script tradotti: stessi entity_id, attributi e servizi, trigger agganciati in un lavoro di avvio;
- il runner chiama script.turn_on come sempre: gli script tradotti sono entità del dominio script.
"""
import os
from pathlib import Path

import pacchetto

DOMINIO = 'sim_motore_nativo'
# il repository con il motore tradotto (non la copia del simulatore, che può essere più vecchia)
RADICE = Path(os.environ.get('VMC_RADICE', '/home/user/vmc-helty-flow-nativa'))
MANIFEST = '''{
  "domain": "sim_motore_nativo",
  "name": "Motore tradotto della VMC (simulatore)",
  "version": "0.0.1",
  "documentation": "https://example.invalid",
  "codeowners": [],
  "requirements": [],
  "dependencies": ["frontend", "http", "lovelace", "repairs"],
  "iot_class": "local_push"
}
'''
INIT = '''"""Motore tradotto della VMC «master» per il simulatore (variante nativa)."""
from homeassistant.core import HomeAssistant

DOMAIN = "sim_motore_nativo"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    from custom_components.vmc_master.nativa.motore.ha import Motore

    motore = Motore(hass)
    await motore.avvia(configurazione=config)
    hass.data[DOMAIN] = motore
    return True
'''


def prepara_configurazione(cfg_dir: str) -> None:
    import shutil

    tolti = pacchetto.togli(cfg_dir, automazioni='tutte', script='tutti')
    if len(tolti['automazioni']) != 14 or len(tolti['script']) != 51:
        raise RuntimeError(f'attese 14 automazioni e 51 script: {tolti}')
    dest = Path(cfg_dir) / 'custom_components' / 'vmc_master'
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        RADICE / 'custom_components' / 'vmc_master', dest,
        ignore=shutil.ignore_patterns('__pycache__'),
    )
    sorgente = Path(cfg_dir) / '.sorgente_motore_nativo'
    sorgente.mkdir(exist_ok=True)
    (sorgente / 'manifest.json').write_text(MANIFEST, encoding='utf-8')
    (sorgente / '__init__.py').write_text(INIT, encoding='utf-8')
    pacchetto.aggiungi_integrazione(cfg_dir, DOMINIO, sorgente, f'{DOMINIO}:\n')


async def avvia(hass) -> None:
    motore = hass.data.get(DOMINIO)
    if motore is None or len(motore.automazioni) != 14 or len(motore.script) != 51:
        raise RuntimeError('motore tradotto non avviato')
