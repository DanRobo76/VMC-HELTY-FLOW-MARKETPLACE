"""Variante «nativa4»: la VMC nativa della fase 4 al posto di quasi tutto il package.

- prepara_configurazione toglie dal package tutto quello che la fase 4 (con le fasi 2 e 3)
  sostituisce: le 14 automazioni, i 51 script, i 16 comandi di shell, i 34 timer, tutti gli
  aiutanti input_* (172 entità native, 67 valori interni nella memoria del motore, 2 voci
  tolte dalla b46 con il campo «Cambia IP VMC»), i sensori template, tcp, rest e
  command_line.
  Restano «homeassistant: customize» (le icone delle automazioni, che restano entità) e
  «recorder:» (spento dal simulatore). Copia l'integrazione vmc_master del repository
  ($VMC_RADICE) in <cfg>/custom_components/vmc_master (solo per importarla: non è in
  configuration.yaml) e aggiunge un'integrazione minima, sim_vmc_nativa4, che nel suo setup
  (durante l'avvio di Home Assistant) crea la VMC con nativa/assemblaggio.py
  (``VMCAssemblata``): StatoVMC e letture, 136 sensori, 172 impostazioni, memoria interna,
  motore con il codice di generato_fase4 (13 automazioni), 34 sensori dei timer, 25
  pulsanti;
- la VMC finta (fakevmc) parla con il motore attraverso ``ClientFinto`` (al posto del
  client TCP) e ``ping_finto`` (al posto del ping), con gli stessi tempi dei comandi di
  shell finti del lato A (fakevmc.FakeProc: 0,05 s se la VMC riceve, 3 s se no; il ping
  0,05 s o 4 s; i file .sh 0,01 s);
- le azioni degli scenari sono quelle dell'utente di domani (aggancio ``servizio``):
  input_boolean -> switch.turn_on/turn_off, input_select -> select.select_option,
  input_number -> number.set_value, input_text -> text.set_value, input_datetime ->
  time.set_value, shell_command -> button.press (o il comando del motore se non ha un
  pulsante), script -> button.press (o lo script del motore se non ha un pulsante). Quello
  che domani nessun utente può fare (scrivere una spia, cioè un binary_sensor, o cambiare
  le opzioni di una scelta come fa la preparazione degli scenari, scrivere un valore
  interno) passa dalle scritture del motore (``ScritturaComandi``), con lo stesso contesto;
- nella traccia, come nel lato A: ``C shell_command.*`` per ogni comando del motore (dal
  suo aggancio, nello stesso punto dell'evento call_service di oggi); ``X tcp: <comando>``
  per i comandi alla VMC e ``X ping <ip>`` per il ping (al posto delle righe di shell di
  oggi); voci ``MS`` per i cambi dei timer del motore (stato, attributi e contesto come li
  scriverebbe Home Assistant) che confronta.py --mappa mette a confronto con le voci ``S``
  dei timer del lato A; voci ``S``/``R`` dei valori interni dalla memoria (con l'entity_id
  di oggi), che confronta.py --mappa fa diventare ``MS``/``MR`` sui due lati. Le voci C e MS
  entrano nella traccia nel punto del bus in cui Home Assistant consegnerebbe l'evento.
"""

import asyncio
import csv
import os
import re
from pathlib import Path

import fakevmc
import pacchetto
import tracce
import vclock

DOMINIO = 'sim_vmc_nativa4'
NOME = 'master'
IP = '192.168.1.160'
RADICE = Path(os.environ.get('VMC_RADICE', '/home/user/vmc-helty-flow-nativa'))
FASE_1 = RADICE / 'tests' / 'nativa' / 'motore' / 'aiutanti_fase1.csv'


MANIFEST = '''{
  "domain": "sim_vmc_nativa4",
  "name": "VMC nativa della fase 4 (simulatore)",
  "version": "0.0.1",
  "documentation": "https://example.invalid",
  "codeowners": [],
  "requirements": [],
  "dependencies": [],
  "iot_class": "local_push"
}
'''
INIT = '''"""VMC nativa della fase 4 per il simulatore (variante nativa4)."""
from homeassistant.core import HomeAssistant

DOMAIN = "sim_vmc_nativa4"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    from varianti import nativa4

    await nativa4.avvia_assemblaggio(hass, config)
    return True
'''

AIUTANTI = ('input_boolean', 'input_number', 'input_select', 'input_text', 'input_datetime')
TOLTE = ('automation', 'script', 'shell_command', 'timer', 'template', 'sensor', 'command_line')


def domani():
    """Colonna «Domani» della fase 1: entità di oggi -> entità di domani (o «interna ...»)."""
    with FASE_1.open(encoding='utf-8-sig', newline='') as f:
        return {r['Entità oggi']: r['Domani'] for r in csv.DictReader(f, delimiter=';')}


def interni():
    """I valori interni con stato (aiutanti input_* che domani sono dentro il motore)."""
    return {e for e, d in domani().items() if d.startswith('interna') and e.split('.')[0] in AIUTANTI}


def prepara_configurazione(cfg_dir: str) -> None:
    import shutil

    tolto = {}
    for p in pacchetto.file_package(cfg_dir, NOME):
        d = pacchetto.leggi(p)
        if not isinstance(d, dict):
            continue
        for chiave in TOLTE:
            if chiave in d:
                tolto[chiave] = tolto.get(chiave, 0) + len(d[chiave] or [])
                del d[chiave]
        for dominio in AIUTANTI:
            if dominio not in d:
                continue
            tolto[dominio] = tolto.get(dominio, 0) + len(d[dominio] or {})
            del d[dominio]
        pacchetto.scrivi(p, d)
    attesi = {'automation': 14, 'script': 51, 'shell_command': 16, 'timer': 34, 'sensor': 5, 'command_line': 1,
              'input_boolean': 115, 'input_number': 43, 'input_select': 15, 'input_text': 38, 'input_datetime': 30}
    tolto_senza_template = {k: v for k, v in tolto.items() if k != 'template'}
    if tolto_senza_template != attesi:
        raise RuntimeError(f'parti tolte dal package diverse dalle attese: {tolto} invece di {attesi}')
    dest = Path(cfg_dir) / 'custom_components' / 'vmc_master'
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(RADICE / 'custom_components' / 'vmc_master', dest, ignore=shutil.ignore_patterns('__pycache__'))
    sorgente = Path(cfg_dir) / '.sorgente_vmc_nativa4'
    sorgente.mkdir(exist_ok=True)
    (sorgente / 'manifest.json').write_text(MANIFEST, encoding='utf-8')
    (sorgente / '__init__.py').write_text(INIT, encoding='utf-8')
    pacchetto.aggiungi_integrazione(cfg_dir, DOMINIO, sorgente, f'{DOMINIO}:\n')


# --- la VMC finta per il client e il ping del motore ----------------------------------------------

CMD_RE = re.compile(r'VMWH(\d{7})')


class ClientFinto:
    """Al posto di ``ClientVMC``: legge e comanda la VMC finta (fakevmc.VMC).

    Le letture come il sensore tcp finto del lato A (fakevmc.tcp_update), in un lavoro
    dell'executor (l'esecutore sincrono del simulatore, come l'update del sensore tcp); i
    comandi come i comandi di shell finti del lato A (fakevmc._handle e FakeProc)."""

    def __init__(self, hass, host):
        self.hass = hass
        self.host = host

    def _leggi(self, richiesta):
        from custom_components.vmc_master.nativa.client import ErroreVMC
        VMC = fakevmc.VMC
        if not VMC.online or VMC.mute:
            raise ErroreVMC('VMC finta spenta o muta')
        if richiesta.startswith('VMGH'):
            return VMC.status_str()
        if richiesta.startswith('VMGI'):
            return VMC.sensori_str()
        if richiesta.startswith('VMNM'):
            return 'VMNM Master'
        if richiesta.startswith('VMSL'):
            return 'VMSL,192,168,1,160'
        return ''

    async def interroga(self, richiesta):
        return await self.hass.async_add_executor_job(self._leggi, richiesta)

    async def comanda(self, comando):
        from custom_components.vmc_master.nativa.client import ErroreVMC
        trovato = CMD_RE.search(comando)
        if trovato is None:
            # il cambio del nome: oggi il file .sh (FakeProc da 0,01 s, nessun comando alla VMC
            # finta); la voce X come quella del lato A tradotta da confronta.py --mappa
            fakevmc._registra((vclock._V[0], f'tcp: {comando}'), 'X')
            await asyncio.sleep(0.01)
            return ''
        fakevmc._registra((vclock._V[0], f'tcp: {comando}'), 'X')
        ricevuto = fakevmc.VMC.command(trovato.group(1))
        await asyncio.sleep(0.05 if ricevuto else 3.0)
        if not ricevuto:
            raise ErroreVMC('VMC finta spenta o muta')
        return ''


async def ping_finto(host):
    """Al posto del ping: come il comando ping finto del lato A (fakevmc._handle)."""
    fakevmc._registra((vclock._V[0], f'ping {host}'), 'X')
    acceso = fakevmc.VMC.online
    await asyncio.sleep(0.05 if acceso else 4.0)
    return acceso


def comandi_come_oggi(comandi):
    """I comandi senza effetto fuori da Home Assistant (oggi lo shell_command
    rimuovi_caratteri_di_ritorno, find e sed sui file del package; domani nessun comando: tipo
    COMANDO_NESSUNO) durano 0,01 s come il comando di shell finto del lato A (FakeProc), così le
    azioni dopo di loro partono nello stesso istante. Solo il simulatore: l'integrazione non
    aspetta nulla."""
    from custom_components.vmc_master.nativa.motore.definizioni import COMANDO_NESSUNO
    originale = comandi.esegui

    async def esegui(nome, dati, bersaglio, contesto, **argomenti):
        risultato = await originale(nome, dati, bersaglio, contesto, **argomenti)
        if comandi.comandi[nome].tipo == COMANDO_NESSUNO:
            await asyncio.sleep(0.01)
        return risultato

    comandi.esegui = esegui


# --- avvio ---------------------------------------------------------------------------------------

STATO = {}


async def avvia_assemblaggio(hass, config):
    """Il setup dell'integrazione sim_vmc_nativa4: la VMC nativa della fase 4."""
    from custom_components.vmc_master.nativa.assemblaggio import (
        VMCAssemblata,
        aggiungi_con_piattaforme,
    )
    from homeassistant.core import callback
    vmc = VMCAssemblata(hass, NOME, IP, client=ClientFinto(hass, IP), prova_ping=ping_finto, versione=False)
    await vmc.avvia(await aggiungi_con_piattaforme(hass), config)
    comandi_come_oggi(vmc.c.comandi)
    _ascolta_voci(hass)
    vmc.c.comandi.ascolta(callback(_traccia_comando))
    vmc.annunci_timer.osserva(_traccia_timer)
    vmc.memoria.ascolta_cambi(_traccia_interno)
    STATO['vmc'] = vmc
    STATO['domani'] = domani()


# Le voci C dei comandi entrano nella traccia nel punto in cui Home Assistant consegnerebbe
# l'evento call_service del comando (le MS dei timer arrivano con AnnunciDeiTimer): un evento
# lanciato mentre il bus ne consegna un altro aspetta la fine di quella consegna
# (EventBus.async_fire_internal). Per avere lo stesso punto la voce viaggia su un evento
# state_reported con un marchio (escluso dagli ascoltatori di tutti gli eventi, entity_id vuoto:
# nessuno lo prende per il rapporto di un'entità), come fa la memoria interna per i suoi annunci.
_MARCHIO = 'sim_nativa4_voce'


def _in_traccia(hass, voce, contesto):
    from homeassistant.const import EVENT_STATE_REPORTED
    hass.bus.async_fire_internal(EVENT_STATE_REPORTED, {'entity_id': '', _MARCHIO: voce}, context=contesto)


def _ascolta_voci(hass):
    from homeassistant.const import EVENT_STATE_REPORTED
    from homeassistant.core import callback

    @callback
    def consegna(evento):
        tracce.TR.ev.append(evento.data[_MARCHIO])

    hass.bus.async_listen(EVENT_STATE_REPORTED, consegna, event_filter=callback(lambda d: _MARCHIO in d))


def _traccia_comando(evento):
    """Il comando del motore nella traccia come la chiamata call_service di oggi (voce C)."""
    d = evento.data
    voce = ['C', vclock._V[0], d['domain'], d['service'], tracce._json(d['service_data'] or {}),
            tracce.forma_contesto(evento.context)]
    _in_traccia(STATO['vmc'].hass, voce, evento.context)


def _traccia_interno(evento):
    """Il cambio di un valore interno (voce S con l'entity_id di oggi, come l'aiutante di oggi:
    la memoria lo consegna nel punto del bus di state_changed; confronta.py --mappa ne fa una MS).
    Le scritture senza cambio arrivano già come R: la memoria le annuncia con lo state_reported
    dell'aiutante (entity_id di oggi)."""
    s = evento.data['new_state']
    tracce.TR.ev.append(['S', vclock._V[0], s.entity_id, s.state, tracce.TR.impronta(s.attributes),
                         tracce.forma_contesto(s.context)])


def _traccia_timer(evento):
    """Il cambio di un timer del motore (voce MS: come la S del timer di oggi), nel punto
    del bus in cui oggi arriva il suo state_changed, prima di chi segue il timer
    (sensori_template.AnnunciDeiTimer: come la traccia ascolta il bus prima dei tracker)."""
    s = evento.data['new_state']
    tracce.TR.ev.append(['MS', vclock._V[0], s.entity_id, s.state, tracce.TR.impronta(dict(s.attributes)),
                         tracce.forma_contesto(s.context)])


async def prima_dell_avvio(hass) -> None:
    """La traccia ascolta il bus prima di chi segue le entità, come nel lato A.

    Il runner registra gli ascoltatori della traccia (tracce.installa) dopo il setup delle
    integrazioni. Oggi a quel punto nessuno segue ancora un'entità (sensori template e
    automazioni cominciano all'avvio), così la traccia annota un cambio prima che i trigger
    e i sensori che lo seguono facciano qualcosa (per esempio un comando alla VMC). La VMC
    nativa segue già le sue letture durante il setup: il distributore degli eventi di
    ``async_track_state_change_event`` è registrato prima della traccia, che annoterebbe il
    comando prima del cambio che l'ha causato. Qui gli ascoltatori della traccia (che
    annotano soltanto) tornano davanti ai distributori di homeassistant.helpers.event:
    nessun effetto sul comportamento, solo il punto in cui la traccia annota."""
    from homeassistant.const import (
        EVENT_CALL_SERVICE,
        EVENT_STATE_CHANGED,
        EVENT_STATE_REPORTED,
    )
    for tipo in (EVENT_STATE_CHANGED, EVENT_STATE_REPORTED, EVENT_CALL_SERVICE):
        ascoltatori = hass.bus._listeners.get(tipo, [])
        traccia = [a for a in ascoltatori if getattr(a[0].target, '__module__', '') == 'tracce']
        altri = [a for a in ascoltatori if a not in traccia]
        primo = next((i for i, a in enumerate(altri) if _distributore(a[0].target)), None)
        if traccia and primo is not None:
            ascoltatori[:] = altri[:primo] + traccia + altri[primo:]


def _distributore(funzione):
    """Il distributore di un tracker di homeassistant.helpers.event (functools.partial)."""
    return getattr(getattr(funzione, 'func', None), '__module__', '') == 'homeassistant.helpers.event'


async def avvia(hass) -> None:
    vmc = STATO.get('vmc')
    if vmc is None or len(vmc.motore.automazioni) != 13 or len(vmc.c.interni.script) != 51:
        raise RuntimeError('VMC nativa della fase 4 non avviata')


# --- le azioni degli scenari con le entità di domani -----------------------------------------------

SERVIZI_DOMANI = {
    ('input_boolean', 'turn_on', 'switch'): ('switch', 'turn_on'),
    ('input_boolean', 'turn_off', 'switch'): ('switch', 'turn_off'),
    ('input_select', 'select_option', 'select'): ('select', 'select_option'),
    ('input_number', 'set_value', 'number'): ('number', 'set_value'),
    ('input_text', 'set_value', 'text'): ('text', 'set_value'),
    ('input_datetime', 'set_datetime', 'time'): ('time', 'set_value'),
}


def _entita_domani(entity_id):
    return STATO['domani'].get(entity_id)


async def _come_task(coro, blocking):
    """blocking=False come ServiceRegistry.async_call: un task che parte subito (eager)."""
    import simlib
    if blocking:
        await coro
    else:
        simlib.HASS.async_create_task(coro, eager_start=True)


async def servizio(hass, dominio, nome, dati, blocking, contesto):
    """Aggancio di simlib.svc: le chiamate degli scenari sulle entità di domani."""
    from homeassistant.core import Context
    vmc = STATO['vmc']
    contesto = contesto or Context()
    if dominio == 'shell_command':
        oggi = f'shell_command.{nome}'
        dest = _entita_domani(oggi)
        if dest and dest.startswith('button.'):
            await hass.services.async_call('button', 'press', {'entity_id': dest}, blocking=blocking, context=contesto)
        else:
            await _come_task(vmc.c.comandi.esegui(nome, dati, {}, contesto), blocking)
        return True
    if dominio not in AIUTANTI:
        return False
    entita = dati.get('entity_id')
    if not isinstance(entita, str):
        raise TypeError(f'azione dello scenario non prevista: {dominio}.{nome} {dati}')
    dest = _entita_domani(entita)
    if dest is None:
        raise RuntimeError(f'entità senza voce nella colonna Domani: {entita}')
    if dest == 'tolta':
        # b46: il campo «Cambia IP VMC» non c'è più: domani l'azione non ha un'entità
        return True
    if dest.startswith('interna'):
        # domani nessun utente scrive un valore interno: la scrittura del motore (memoria)
        await _come_task(vmc.scrittura.chiama(f'{dominio}.{nome}', dati, contesto), blocking)
        return True
    dominio_domani = dest.split('.')[0]
    voce = SERVIZI_DOMANI.get((dominio, nome, dominio_domani))
    if voce is None:
        # domani nessun utente lo può fare (una spia, le opzioni di una scelta): la scrittura del motore
        await _come_task(vmc.scrittura.chiama(f'{dominio}.{nome}', dati, contesto), blocking)
        return True
    nuovi = {**dati, 'entity_id': dest}
    await hass.services.async_call(voce[0], voce[1], nuovi, blocking=blocking, context=contesto)
    return True


async def script(hass, entity_id, dati, contesto):
    """Aggancio dell'azione «script» degli scenari: il pulsante di domani o lo script del motore."""
    vmc = STATO['vmc']
    dest = _entita_domani(entity_id)
    if dest and dest.startswith('button.') and not dati:
        await hass.services.async_call('button', 'press', {'entity_id': dest}, blocking=False, context=contesto)
        return True
    bersaglio = {'entity_id': [entity_id]}
    variabili = {'variables': dati} if dati else {}
    hass.async_create_task(vmc.c.interni.chiama('turn_on', variabili, bersaglio, contesto), eager_start=True)
    return True
