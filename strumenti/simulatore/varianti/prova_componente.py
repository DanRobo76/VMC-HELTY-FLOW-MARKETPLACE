"""Variante di prova del meccanismo delle varianti (non e' un motore).

- prepara_configurazione scrive un'integrazione personalizzata minima in <cfg>/custom_components/sim_prova_componente
  e la aggiunge a configuration.yaml, come fara' la variante del motore nativo;
- il manifest dichiara le stesse dipendenze di vmc_master (frontend, http, lovelace, repairs): il simulatore
  non deve caricare frontend e lovelace (simlib.DIPENDENZE_TOLTE; http e repairs ci sono gia', per notify),
  avvia(hass) lo controlla;
- l'integrazione registra un lavoro di avvio (hass.async_add_startup_job, come le automazioni YAML) che si segna
  in hass.data; avvia(hass) controlla che l'integrazione sia stata caricata e che il lavoro di avvio sia girato;
- script(hass, entity_id, dati, contesto) esegue lo script YAML con la stessa chiamata del runner e restituisce
  True (il runner non lo richiama).
Non scrive stati ne' chiama servizi: il differenziale contro «identica» deve dare zero differenze. Se ne da',
la sola presenza di un'integrazione personalizzata cambia l'ordine degli eventi all'avvio.
"""
from pathlib import Path

DOMINIO = 'sim_prova_componente'
MANIFEST = '''{
  "domain": "sim_prova_componente",
  "name": "Prova componente del simulatore",
  "version": "0.0.1",
  "documentation": "https://example.invalid",
  "codeowners": [],
  "requirements": [],
  "dependencies": ["frontend", "http", "lovelace", "repairs"],
  "iot_class": "local_push"
}
'''
INIT = '''"""Integrazione di prova del simulatore: solo un lavoro di avvio che si segna in hass.data."""
from homeassistant.core import HassJob, HomeAssistant

DOMAIN = "sim_prova_componente"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data[DOMAIN] = {"setup": True, "avvio": False}

    async def _avvio() -> None:
        hass.data[DOMAIN]["avvio"] = True

    hass.async_add_startup_job(HassJob(_avvio))
    return True
'''


def prepara_configurazione(cfg_dir: str) -> None:
    import pacchetto
    sorgente = Path(cfg_dir) / '.sorgente_prova_componente'
    sorgente.mkdir(exist_ok=True)
    (sorgente / 'manifest.json').write_text(MANIFEST, encoding='utf-8')
    (sorgente / '__init__.py').write_text(INIT, encoding='utf-8')
    pacchetto.aggiungi_integrazione(cfg_dir, DOMINIO, sorgente, f'{DOMINIO}:\n')


async def avvia(hass) -> None:
    stato = hass.data.get(DOMINIO)
    if not stato or not stato.get('setup') or not stato.get('avvio'):
        raise RuntimeError(f'integrazione {DOMINIO} non caricata o lavoro di avvio non eseguito: {stato}')
    caricate = {'frontend', 'lovelace', 'onboarding'} & set(hass.config.components)
    if caricate:
        raise RuntimeError(f'dipendenze che il simulatore non deve caricare: {sorted(caricate)}')


async def script(hass, entity_id: str, dati: dict, contesto) -> bool:
    await hass.services.async_call('script', 'turn_on', {'entity_id': entity_id, **dati}, blocking=False, context=contesto)
    return True
