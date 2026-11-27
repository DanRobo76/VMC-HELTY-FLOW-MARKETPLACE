"""Traccia di uno scenario per il confronto A/B (differenziale.py, confronta.py).

La traccia e' un'unica lista di voci nell'ordine in cui accadono (stesso istante virtuale = ordine
di esecuzione nel ciclo). Ogni voce e' una lista [tipo, t, ...]; t e' in secondi virtuali (negli
scenari relativo all'inizio della timeline, negativo durante la preparazione):

  S  t entity_id stato attr ctx   cambio di stato (state_changed) di un'entita' della VMC; stato None
                                  se l'entita' e' stata tolta; attr = impronta degli attributi
                                  (tabella 'attr' della traccia: impronta -> attributi); ctx = forma
                                  del contesto: 'u' utente, 'p' contesto figlio (automazione/script),
                                  'up' entrambi, '' nessuno (gli id dei contesti sono casuali)
  R  t entity_id ctx              scrittura senza cambio (state_reported): stesso stato e attributi,
                                  cambia solo last_reported; ctx = forma del contesto della scrittura
  C  t dominio servizio dati ctx  chiamata di servizio con effetti fuori dalle entita' della VMC
                                  (tutti i domini tranne quelli degli aiutanti, vedi DOMINI_INTERNI)
  E  t dominio servizio dati err  la stessa chiamata non riuscita (servizio inesistente, dati non
                                  validi...): err = classe dell'errore
  V  t tipo valore fonte prima    registro della VMC finta (cmd / speed / power), come runner 'log'
  X  t comando                    comando di shell eseguito (nc dei comandi, ping del sensore IP)
  MS t entity_id stato attr ctx   come S, per un timer o un valore interno dentro il motore (variante
                                  nativa4: confronta.py --mappa le confronta con le S di oggi)

Entita' della VMC: object_id che inizia con «vmc_master_» (tutti i domini) e l'automazione
principale automation.automazione_vmc_master.

Attributi: si registra un'impronta (blake2b dei valori in JSON con chiavi ordinate) di TUTTI gli
attributi. last_changed / last_updated / last_reported e il contesto non sono attributi e non
entrano nell'impronta; nessun attributo delle entita' del package dipende dal tempo reale o da
valori casuali (timer: finishes_at e remaining sono calcolati sull'orologio virtuale; automazioni
e script: last_triggered virtuale), quindi ATTRIBUTI_ESCLUSI e' vuoto: la prova A contro A' lo
conferma (LEGGIMI.md).
"""
import base64
import hashlib
import json
import zlib

DOMINI_INTERNI = frozenset({'input_boolean', 'input_text', 'input_number', 'input_select', 'input_datetime',
                            'input_button', 'counter', 'timer', 'script', 'automation'})
ATTRIBUTI_ESCLUSI = frozenset()
TIPI = {'S': 'cambio di stato', 'R': 'scrittura senza cambio', 'C': 'chiamata di servizio',
        'E': 'chiamata non riuscita', 'V': 'registro della VMC', 'X': 'comando di shell'}


def entita_vmc(entity_id: str) -> bool:
    obj = entity_id.partition('.')[2]
    return obj.startswith('vmc_master_') or obj == 'automazione_vmc_master'


def forma_contesto(ctx) -> str:
    if ctx is None:
        return ''
    return ('u' if ctx.user_id is not None else '') + ('p' if ctx.parent_id is not None else '')


def _json(o):
    return json.dumps(o, sort_keys=True, default=str, ensure_ascii=False, separators=(',', ':'))


class Traccia:
    def __init__(self):
        self.ev = []        # voci con t assoluto (vclock._V)
        self.attr = {}      # impronta -> attributi (JSON)
        self._cache = {}    # id(attributi) -> (attributi, impronta): gli attributi di uno State non cambiano
        self.attiva = False

    def reset(self):
        self.ev.clear(); self.attr.clear(); self._cache.clear()

    def impronta(self, attributi) -> str:
        c = self._cache.get(id(attributi))
        if c is not None and c[0] is attributi:
            return c[1]
        if ATTRIBUTI_ESCLUSI:
            attributi_f = {k: v for k, v in attributi.items() if k not in ATTRIBUTI_ESCLUSI}
        else:
            attributi_f = attributi
        j = _json(dict(attributi_f))
        d = hashlib.blake2b(j.encode('utf-8'), digest_size=8).hexdigest()
        if d not in self.attr:
            self.attr[d] = j
        self._cache[id(attributi)] = (attributi, d)
        return d

    def installa(self, hass):
        """Ascolto diretto del bus (hass.bus.async_listen con event_filter): non aggiunge tracker per
        entita' e quindi non cambia l'ordine dei trigger delle automazioni (vedi runner.install_listeners).
        Le funzioni registrano soltanto: nessun effetto sul ciclo."""
        import vclock
        from homeassistant.core import callback, ServiceRegistry
        from homeassistant.const import EVENT_STATE_CHANGED, EVENT_STATE_REPORTED, EVENT_CALL_SERVICE
        V = vclock._V
        ev = self.ev

        @callback
        def filtro_entita(d):
            return entita_vmc(d['entity_id'])

        @callback
        def cambio(e):
            d = e.data; ns = d['new_state']
            if ns is None:
                ev.append(['S', V[0], d['entity_id'], None, None, forma_contesto(e.context)])
            else:
                ev.append(['S', V[0], d['entity_id'], ns.state, self.impronta(ns.attributes), forma_contesto(ns.context)])

        @callback
        def riportato(e):
            ev.append(['R', V[0], e.data['entity_id'], forma_contesto(e.context)])

        @callback
        def filtro_servizi(d):
            return str(d.get('domain', '')).lower() not in DOMINI_INTERNI

        @callback
        def servizio(e):
            d = e.data
            ev.append(['C', V[0], d.get('domain'), d.get('service'), _json(d.get('service_data') or {}), forma_contesto(e.context)])

        hass.bus.async_listen(EVENT_STATE_CHANGED, cambio, event_filter=filtro_entita)
        hass.bus.async_listen(EVENT_STATE_REPORTED, riportato, event_filter=filtro_entita)
        hass.bus.async_listen(EVENT_CALL_SERVICE, servizio, event_filter=filtro_servizi)

        # chiamate non riuscite (prima dell'evento call_service: servizio inesistente, dati non validi)
        # o finite con un errore: involucro sul metodo, senza passaggi in piu' nel ciclo (await diretto)
        if not getattr(ServiceRegistry.async_call, '_sim', False):
            orig = ServiceRegistry.async_call
            tr = self
            async def async_call(reg, domain, service, service_data=None, *a, **k):
                try:
                    return await orig(reg, domain, service, service_data, *a, **k)
                except Exception as err:   # noqa: BLE001 - si registra e si rilancia
                    if str(domain).lower() not in DOMINI_INTERNI:
                        tr.ev.append(['E', V[0], domain, service, _json(service_data or {}), type(err).__name__])
                    raise
            async_call._sim = True
            ServiceRegistry.async_call = async_call

    def istantanea(self, hass):
        """Stato di tutte le entita' della VMC, in ordine di entity_id: [entity_id, stato, attr]."""
        return [[s.entity_id, s.state, self.impronta(s.attributes)] for s in
                sorted((s for s in hass.states.async_all() if entita_vmc(s.entity_id)), key=lambda s: s.entity_id)]

    def esporta(self, t0: float, ndec: int = 6):
        """Voci con t relativo a t0 (arrotondato a ndec decimali) e tabella degli attributi usati."""
        out = []
        for v in self.ev:
            w = list(v); w[1] = round(v[1] - t0, ndec); out.append(w)
        usati = {v[4] for v in self.ev if v[0] in ('S', 'MS') and v[4] is not None}
        return out, {d: json.loads(self.attr[d]) for d in sorted(usati)}


def comprimi(dati) -> str:
    """Traccia nel file dei risultati: JSON compresso (zlib) in base64, campo 'trz' (circa 12 volte meno spazio)."""
    j = json.dumps(dati, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return base64.b64encode(zlib.compress(j, 6)).decode('ascii')


def decomprimi(res) -> dict:
    """Dati della traccia di un risultato: {'tr': [...], 'attr': {...}} (+ 'iniziale'/'finale' per '__avvio__')."""
    if 'trz' in res:
        return json.loads(zlib.decompress(base64.b64decode(res['trz'])))
    return {k: res[k] for k in ('tr', 'attr', 'iniziale', 'finale') if k in res}


TR = Traccia()
