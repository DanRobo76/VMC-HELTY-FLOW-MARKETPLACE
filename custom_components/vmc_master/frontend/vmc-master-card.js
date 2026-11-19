/*
 * Scheda «VMC Master» dell'integrazione VMC Master.
 *
 * Non disegna nulla da sola: chiede all'integrazione la configurazione della scheda
 * della VMC scelta (la stessa scheda manuale della release 8.6.0, con le schede native
 * di Home Assistant) e la costruisce con gli strumenti standard della plancia.
 *
 * Copyright (C) 2023-2026 Ing. Danilo Robotti - Licenza GPL-3.0
 */

const TIPO = "vmc-master-card";
const DOMINIO = "vmc_master";
// Dopo un errore la scheda si richiede di nuovo solo dopo questo tempo (o se cambia la VMC)
const ATTESA_DOPO_ERRORE_MS = 30 * 1000;
// Dopo un errore temporaneo (Home Assistant in avvio, integrazione non ancora partita, rete
// assente) si riprova da soli dopo pochi secondi, anche senza cambi di stato
const ATTESA_RIPROVA_MS = 3 * 1000;
// Controllo aggiornamenti all'apertura del Pannello Informazioni: al massimo una volta
// al minuto (GitHub accetta 60 richieste all'ora senza autenticazione e tiene in cache
// la risposta di releases/latest per 60 s: un limite piu' lungo nasconde la release
// appena pubblicata anche riaprendo il pannello)
const ATTESA_CONTROLLO_MS = 60 * 1000;
// Versione di questo file JavaScript (?v=... messo dall'integrazione nell'indirizzo)
const VERSIONE_JS = new URL(import.meta.url).searchParams.get("v") || "";
const RE_SENSORE_REPOSITORY = /sensor\.vmc_[a-z]+_versione_repository/;
const TITOLO_INFORMAZIONI = "Informazioni";
// Ora dell'ultimo controllo aggiornamenti (di tutte le VMC), salvata nella pagina e non
// nella singola scheda: cambiando vista la scheda si ricrea ma il limite resta
const ULTIMI_CONTROLLI = (window.__vmcMasterUltimiControlli = window.__vmcMasterUltimiControlli || {});

// Solo la risposta JSON «VMC non trovata» dell'integrazione dice che la VMC scelta non
// esiste piu'. Un 404 senza quel testo arriva per esempio subito dopo il riavvio di
// Home Assistant, quando l'integrazione non e' ancora partita.
function vmcNonTrovata(errore) {
  return Boolean(
    errore &&
      errore.status_code === 404 &&
      errore.body &&
      typeof errore.body === "object" &&
      errore.body.message === "VMC non trovata"
  );
}

// Errore che passa da solo: rete assente, Home Assistant in avvio, 404 di una vista non
// ancora registrata (integrazione non ancora partita), 502/503/504
function erroreTemporaneo(errore) {
  if (vmcNonTrovata(errore)) {
    return false;
  }
  const stato = errore && errore.status_code;
  return stato === undefined || stato === null || stato === 404 || stato === 502 || stato === 503 || stato === 504;
}

// Consiglio per gli errori diversi da «VMC non trovata»: l'integrazione risponde solo con
// la scheda o con quel messaggio, quindi gli altri errori (rete assente, Home Assistant in
// avvio, 404 di una vista non ancora registrata, 5xx) non dipendono dalla configurazione.
function consiglioErrore(errore) {
  if (vmcNonTrovata(errore)) {
    return "Scegliere di nuovo la VMC nelle opzioni della scheda.";
  }
  if (erroreTemporaneo(errore)) {
    return "Home Assistant non raggiungibile o in avvio: la scheda riprova da sola.";
  }
  return "La scheda riprova da sola; se il messaggio resta, controllare i log di Home Assistant.";
}

// Errore di hass.callApi: un oggetto { error, status_code, body } e non un Error
function dettaglioErrore(errore) {
  if (!errore) {
    return "";
  }
  const corpo = errore.body;
  return (
    (corpo && typeof corpo === "object" && corpo.message) ||
    errore.error ||
    errore.message ||
    ""
  );
}

function titoloInformazioni(elemento) {
  return (
    elemento &&
    elemento.tagName === "SUMMARY" &&
    (elemento.textContent || "").trim() === TITOLO_INFORMAZIONI
  );
}

function testoTitolo(titolo) {
  return (titolo.textContent || "").replace(/\s+/g, " ").trim();
}

// Chiave di un <summary> nel contenitore: il testo e, se lo stesso testo si ripete, il
// numero d'ordine (il ridisegno del markdown crea elementi nuovi con lo stesso testo)
function chiaviTitoli(contenitore) {
  const conteggi = new Map();
  return Array.from(contenitore.querySelectorAll("details > summary")).map((titolo) => {
    const testo = testoTitolo(titolo);
    const numero = conteggi.get(testo) || 0;
    conteggi.set(testo, numero + 1);
    return { titolo, chiave: `${testo}#${numero}` };
  });
}

// Ricollegamenti di ogni collegamento a Home Assistant, contati da un solo ascoltatore per
// collegamento che vive quanto la pagina: una scheda staccata dal DOM (vista non visibile)
// non ascolta, ma al rientro sa se nel frattempo Home Assistant si e' ricollegato.
const RICOLLEGAMENTI = new WeakMap();

function contaRicollegamenti(connessione) {
  if (!connessione || typeof connessione.addEventListener !== "function") {
    return 0;
  }
  if (!RICOLLEGAMENTI.has(connessione)) {
    RICOLLEGAMENTI.set(connessione, 0);
    connessione.addEventListener("ready", () => {
      RICOLLEGAMENTI.set(connessione, RICOLLEGAMENTI.get(connessione) + 1);
    });
  }
  return RICOLLEGAMENTI.get(connessione);
}

class VmcMasterCard extends HTMLElement {
  constructor() {
    super();
    this._config = undefined;
    this._hass = undefined;
    this._scheda = undefined;
    this._testoConfigurazione = undefined; // configurazione della scheda costruita (JSON)
    this._caricata = undefined; // VMC (entry_id) della scheda costruita o in costruzione
    this._connessione = undefined; // collegamento a Home Assistant che stiamo ascoltando
    this._errore = undefined; // { vmc, alle, temporaneo }: ultima richiesta della scheda non riuscita
    this._sensoreRepository = undefined; // sensore «Versione Repository» della scheda
    this._riprova = undefined; // nuovo tentativo dopo un ricollegamento non riuscito
    this._daAggiornare = false; // ricollegamento senza risposta: si riprova
    this._richiesta = 0; // numero dell'ultima richiesta: le risposte delle precedenti si ignorano
    this._ricollegamentiVisti = undefined; // ricollegamenti contati all'ultima richiesta riuscita
    this._testoMessaggio = undefined; // testo del messaggio mostrato al posto della scheda
    // pannelli <details> aperti o chiusi dall'utente, per ogni scheda markdown (contenitore):
    // { stati: Map(chiave del titolo -> aperto), osservatore }
    this._pannelli = new Map();
    // Dopo un riavvio di Home Assistant il browser si ricollega senza ricaricare la pagina
    // (succede anche sbloccando il telefono o dopo un calo di rete): si chiede di nuovo la
    // configurazione e la scheda si ricostruisce solo se e' cambiata, per esempio dopo un
    // aggiornamento. Vale per la configurazione della scheda; questo file JavaScript resta
    // quello gia' caricato fino al ricaricamento della pagina.
    this._alRicollegamento = () => {
      this._avvisaVersioneVecchia();
      if (this._scheda) {
        this._aggiorna();
        return;
      }
      this._caricata = undefined;
      this._errore = undefined;
      this._carica();
    };
    // Clic sui titoli dei pannelli <details> (stato da ricordare) e apertura del Pannello
    // Informazioni: si controlla subito se c'e' una nuova release, come fa «Agg. Sensori»
    // per la versione installata.
    this._alClic = (evento) => this._clicInformazioni(evento);
    this.addEventListener("click", this._alClic);
  }

  // Dopo un aggiornamento dell'integrazione il browser si ricollega senza ricaricare la
  // pagina e questo file resta quello vecchio (per esempio una versione senza il controllo
  // all'apertura del Pannello Informazioni): lo si dice una volta, nella console e con un
  // avviso di Home Assistant, finche' la pagina non viene ricaricata.
  _avvisaVersioneVecchia() {
    const stati = (this._hass && this._hass.states) || {};
    const id = Object.keys(stati).find((x) => /^sensor\.vmc_[a-z]+_versione_corrente$/.test(x));
    const stato = id && stati[id];
    const installata = stato ? String(stato.state).replace(/^[^0-9]*/, "").trim() : "";
    if (!VERSIONE_JS || !/^[0-9]/.test(installata) || installata === VERSIONE_JS) {
      return;
    }
    if (window.__vmcMasterAvvisoVersione === installata) {
      return;
    }
    window.__vmcMasterAvvisoVersione = installata;
    console.warn(`VMC Master: scheda ${VERSIONE_JS} caricata, integrazione ${installata}: ricaricare la pagina`);
    this.dispatchEvent(
      new CustomEvent("hass-notification", {
        detail: { message: `VMC Master aggiornata a ${installata}: ricaricare la pagina`, duration: 10000 },
        bubbles: true,
        composed: true,
      })
    );
  }

  // Clic su un titolo <summary> dentro la scheda: si ricorda se il pannello resta aperto o
  // chiuso. Il clic attraversa le schede interne (shadow DOM): composedPath() da' anche gli
  // elementi al loro interno. Se e' il Pannello Informazioni che si apre, si controlla
  // subito se c'e' una nuova release.
  _clicInformazioni(evento) {
    const percorso = typeof evento.composedPath === "function" ? evento.composedPath() : [];
    const titolo = percorso.find((elemento) => elemento && elemento.tagName === "SUMMARY");
    if (!titolo) {
      return;
    }
    const pannello = titolo.parentElement;
    if (!pannello || pannello.tagName !== "DETAILS") {
      return;
    }
    // il clic arriva prima che il pannello cambi stato: aperto ora = si sta chiudendo
    const apertura = !pannello.open;
    this._ricordaPannello(titolo, apertura);
    if (apertura && titoloInformazioni(titolo)) {
      this._controllaAggiornamenti();
    }
  }

  _contenitore(elemento) {
    const radice = elemento.getRootNode();
    const contenitore = radice === document ? elemento.parentNode : radice;
    return contenitore && typeof contenitore.querySelectorAll === "function"
      ? contenitore
      : undefined;
  }

  _ricordaPannello(titolo, aperto) {
    const contenitore = this._contenitore(titolo);
    if (!contenitore) {
      return;
    }
    const voce = chiaviTitoli(contenitore).find((x) => x.titolo === titolo);
    if (!voce) {
      return;
    }
    let pannelli = this._pannelli.get(contenitore);
    if (!pannelli) {
      pannelli = { stati: new Map(), osservatore: undefined };
      this._pannelli.set(contenitore, pannelli);
    }
    pannelli.stati.set(voce.chiave, aperto);
    this._osserva(contenitore, pannelli);
  }

  // La scheda markdown che contiene i pannelli si ridisegna quando cambia un suo valore
  // (per esempio la riga della versione dopo il controllo aggiornamenti) e ricrea tutti i
  // <details> come sono scritti: il Pannello Informazioni e le voci aperte si
  // richiuderebbero. Si rimette subito ogni pannello come l'ha lasciato l'utente.
  _osserva(contenitore, pannelli) {
    if (pannelli.osservatore || typeof MutationObserver !== "function") {
      return;
    }
    pannelli.osservatore = new MutationObserver(() => this._ripristina(contenitore, pannelli));
    pannelli.osservatore.observe(contenitore, { childList: true, subtree: true });
  }

  _ripristina(contenitore, pannelli) {
    for (const { titolo, chiave } of chiaviTitoli(contenitore)) {
      if (!pannelli.stati.has(chiave)) {
        continue;
      }
      const aperto = pannelli.stati.get(chiave);
      if (titolo.parentElement.open !== aperto) {
        titolo.parentElement.open = aperto;
      }
    }
  }

  // Scheda staccata dal DOM (vista non visibile): si smette di osservare ma si ricorda lo
  // stato dei pannelli; al rientro si riprende (oblio=true: scheda nuova, si dimentica tutto)
  _fermaOsservatore(oblio = false) {
    for (const pannelli of this._pannelli.values()) {
      if (pannelli.osservatore) {
        pannelli.osservatore.disconnect();
        pannelli.osservatore = undefined;
      }
    }
    if (oblio) {
      this._pannelli.clear();
    }
  }

  _riprendiOsservatore() {
    for (const [contenitore, pannelli] of Array.from(this._pannelli.entries())) {
      if (!contenitore.isConnected) {
        this._pannelli.delete(contenitore);
        continue;
      }
      this._ripristina(contenitore, pannelli);
      this._osserva(contenitore, pannelli);
    }
  }

  _controllaAggiornamenti() {
    // L'integrazione e' una sola per tutte le VMC: si aggiornano i sensori «Versione
    // Repository» di tutte, cosi' ogni scheda mostra subito lo stesso avviso
    const sensori = this._sensoriRepository();
    const adesso = Date.now();
    if (!sensori.length || !this._hass) {
      console.info("VMC Master: controllo aggiornamenti non possibile (sensore non trovato)");
      return;
    }
    if (adesso - (ULTIMI_CONTROLLI.tutte || 0) < ATTESA_CONTROLLO_MS) {
      console.info("VMC Master: controllo aggiornamenti gia' fatto da meno di un minuto");
      return;
    }
    ULTIMI_CONTROLLI.tutte = adesso;
    Promise.resolve()
      .then(() =>
        this._hass.callService("homeassistant", "update_entity", { entity_id: sensori })
      )
      .catch((errore) => {
        // controllo non riuscito: si potra' riprovare subito riaprendo il pannello
        ULTIMI_CONTROLLI.tutte = 0;
        console.warn("VMC Master: controllo aggiornamenti non riuscito", errore);
      });
  }

  _sensoriRepository() {
    const tutti = Object.keys((this._hass && this._hass.states) || {}).filter((id) =>
      new RegExp(`^${RE_SENSORE_REPOSITORY.source}$`).test(id)
    );
    const sensore = this._trovaSensoreRepository();
    if (sensore && !tutti.includes(sensore)) {
      tutti.push(sensore);
    }
    return tutti;
  }

  _trovaSensoreRepository() {
    if (this._sensoreRepository) {
      return this._sensoreRepository;
    }
    // senza la configurazione si usa il sensore solo se ce n'e' uno (una sola VMC)
    const sensori = Object.keys((this._hass && this._hass.states) || {}).filter((id) =>
      new RegExp(`^${RE_SENSORE_REPOSITORY.source}$`).test(id)
    );
    return sensori.length === 1 ? sensori[0] : undefined;
  }

  disconnectedCallback() {
    this._ascolta(undefined);
    this._fermaRiprova();
    this._fermaOsservatore();
  }

  connectedCallback() {
    if (this._hass) {
      this._ascolta(this._hass.connection);
    }
    this._riprendiOsservatore();
    // Ricollegamento avvenuto mentre la scheda era staccata dal DOM (per esempio riavvio di
    // Home Assistant con la scheda in una vista non visibile): si chiede di nuovo la
    // configurazione, come farebbe l'ascoltatore del ricollegamento
    const ricollegata =
      this._scheda &&
      this._hass &&
      this._ricollegamentiVisti !== undefined &&
      contaRicollegamenti(this._hass.connection) !== this._ricollegamentiVisti;
    if (this._daAggiornare || ricollegata) {
      this._aggiorna();
    }
  }

  _ascolta(connessione) {
    if (this._connessione === connessione) {
      return;
    }
    // prima l'ascoltatore del modulo, cosi' il conteggio e' gia' aggiornato quando la
    // scheda reagisce al ricollegamento
    contaRicollegamenti(connessione);
    if (this._connessione) {
      this._connessione.removeEventListener("ready", this._alRicollegamento);
    }
    this._connessione = connessione;
    if (connessione) {
      connessione.addEventListener("ready", this._alRicollegamento);
    }
  }

  _fermaRiprova() {
    if (this._riprova !== undefined) {
      clearTimeout(this._riprova);
      this._riprova = undefined;
    }
  }

  static getConfigForm() {
    return {
      schema: [
        {
          name: "vmc",
          required: true,
          selector: { config_entry: { integration: DOMINIO } },
        },
      ],
      computeLabel: (campo) => (campo.name === "vmc" ? "VMC" : undefined),
    };
  }

  static async getStubConfig(hass) {
    try {
      const voci = await hass.callWS({ type: "config_entries/get", domain: DOMINIO });
      if (voci && voci.length) {
        return { vmc: voci[0].entry_id };
      }
    } catch (_errore) {
      // nessuna VMC configurata: la scelta resta vuota
    }
    return { vmc: "" };
  }

  setConfig(config) {
    if (!config) {
      throw new Error("Configurazione non valida");
    }
    const cambiata = !this._config || this._config.vmc !== config.vmc;
    this._config = config;
    if (cambiata) {
      this._caricata = undefined;
      this._errore = undefined;
      this._sensoreRepository = undefined;
      this._daAggiornare = false;
      this._richiesta += 1; // le risposte per la VMC di prima non contano piu'
      this._fermaRiprova();
      this._carica();
    }
  }

  set hass(hass) {
    this._hass = hass;
    this._avvisaVersioneVecchia();
    if (this.isConnected) {
      this._ascolta(hass.connection);
    }
    if (this._scheda) {
      this._scheda.hass = hass;
    } else {
      this._carica();
    }
  }

  get hass() {
    return this._hass;
  }

  getCardSize() {
    return this._scheda && typeof this._scheda.getCardSize === "function"
      ? this._scheda.getCardSize()
      : 12;
  }

  // ruolo "alert" per gli errori (letto subito dai lettori di schermo), "status" per le
  // indicazioni
  _messaggio(testo, ruolo = "status") {
    this._fermaOsservatore(true);
    this._scheda = undefined;
    this._testoConfigurazione = undefined;
    this._testoMessaggio = testo;
    this.replaceChildren();
    const card = document.createElement("ha-card");
    const corpo = document.createElement("div");
    corpo.style.padding = "16px";
    corpo.setAttribute("role", ruolo);
    corpo.setAttribute("aria-live", ruolo === "alert" ? "assertive" : "polite");
    corpo.textContent = testo;
    card.appendChild(corpo);
    this.appendChild(card);
  }

  _costruisci(configurazione, testo, aiuti) {
    this._fermaOsservatore(true);
    this._errore = undefined;
    this._testoMessaggio = undefined;
    const trovato = testo.match(RE_SENSORE_REPOSITORY);
    this._sensoreRepository = trovato ? trovato[0] : undefined;
    const scheda = aiuti.createCardElement(configurazione);
    scheda.hass = this._hass;
    this._scheda = scheda;
    this._testoConfigurazione = testo;
    this.replaceChildren(scheda);
  }

  _mostraErrore(vmc, errore) {
    this._caricata = undefined;
    const temporaneo = erroreTemporaneo(errore);
    this._errore = { vmc, alle: Date.now(), temporaneo };
    const dettaglio = dettaglioErrore(errore);
    this._messaggio(
      `Scheda VMC Master non disponibile${dettaglio ? `: ${dettaglio}` : ""}. ${consiglioErrore(errore)}`,
      "alert"
    );
    // Errore temporaneo, per esempio il 404 subito dopo il riavvio di Home Assistant, quando
    // la plancia si ricollega prima che l'integrazione sia partita: nuovo tentativo dopo
    // pochi secondi, senza aspettare un cambio di stato
    this._fermaRiprova();
    if (temporaneo && this.isConnected) {
      this._riprova = setTimeout(() => {
        this._riprova = undefined;
        this._errore = undefined;
        this._carica();
      }, ATTESA_RIPROVA_MS);
    }
  }

  // Dopo un ricollegamento, con la scheda gia' costruita: la si ricostruisce solo se la
  // configurazione e' cambiata (cosi' il Pannello Informazioni aperto e lo scorrimento
  // restano). Se la richiesta non riesce si tiene la scheda e si riprova.
  async _aggiorna() {
    this._fermaRiprova();
    this._daAggiornare = false;
    const vmc = this._config && this._config.vmc;
    if (!this._hass || !vmc || this._caricata !== vmc || !this._scheda) {
      return;
    }
    const numero = ++this._richiesta;
    const ricollegamenti = contaRicollegamenti(this._hass.connection);
    // vale solo la risposta dell'ultima richiesta, per la scheda ancora costruita
    const valida = () => numero === this._richiesta && this._caricata === vmc && this._scheda;
    let configurazione;
    try {
      configurazione = await this._hass.callApi("GET", `${DOMINIO}/scheda/${vmc}`);
    } catch (errore) {
      if (!valida()) {
        return; // richiesta superata da una piu' recente o da un'altra VMC
      }
      if (vmcNonTrovata(errore)) {
        this._mostraErrore(vmc, errore);
        return;
      }
      this._daAggiornare = true;
      if (this.isConnected) {
        this._fermaRiprova();
        this._riprova = setTimeout(() => this._aggiorna(), ATTESA_DOPO_ERRORE_MS);
      }
      return;
    }
    if (!valida()) {
      return;
    }
    this._ricollegamentiVisti = ricollegamenti;
    const testo = JSON.stringify(configurazione);
    if (testo === this._testoConfigurazione) {
      return; // configurazione invariata: la scheda resta com'e'
    }
    try {
      const aiuti = await window.loadCardHelpers();
      if (valida()) {
        this._costruisci(configurazione, testo, aiuti);
      }
    } catch (_errore) {
      // scheda nuova non costruita: resta quella di prima
    }
  }

  async _carica() {
    if (!this._hass || !this._config) {
      return;
    }
    const vmc = this._config.vmc;
    if (!vmc) {
      // il messaggio si disegna una volta sola, non a ogni cambio di stato
      const testo = "Scegliere la VMC nelle opzioni della scheda.";
      if (this._testoMessaggio !== testo || this._scheda) {
        this._messaggio(testo);
      }
      return;
    }
    if (this._caricata === vmc) {
      return;
    }
    if (
      this._errore &&
      this._errore.vmc === vmc &&
      Date.now() - this._errore.alle < (this._errore.temporaneo ? ATTESA_RIPROVA_MS : ATTESA_DOPO_ERRORE_MS)
    ) {
      return; // errore recente: non si riprova a ogni cambio di stato
    }
    this._caricata = vmc;
    const numero = ++this._richiesta;
    const ricollegamenti = contaRicollegamenti(this._hass.connection);
    try {
      const [configurazione, aiuti] = await Promise.all([
        this._hass.callApi("GET", `${DOMINIO}/scheda/${vmc}`),
        window.loadCardHelpers(),
      ]);
      if (numero !== this._richiesta || this._caricata !== vmc) {
        return; // nel frattempo e' partita un'altra richiesta o e' stata scelta un'altra VMC
      }
      this._ricollegamentiVisti = ricollegamenti;
      this._costruisci(configurazione, JSON.stringify(configurazione), aiuti);
    } catch (errore) {
      if (numero !== this._richiesta || this._caricata !== vmc) {
        return; // errore di una richiesta vecchia: non tocca la risposta della nuova
      }
      this._mostraErrore(vmc, errore);
    }
  }
}

if (!customElements.get(TIPO)) {
  customElements.define(TIPO, VmcMasterCard);
}

window.customCards = window.customCards || [];
if (!window.customCards.some((scheda) => scheda.type === TIPO)) {
  window.customCards.push({
    type: TIPO,
    name: "VMC Master",
    description: "Scheda completa della VMC Helty Flow Plus/Elite gestita dall'integrazione VMC Master.",
    preview: false,
    documentationURL: "https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE",
  });
}
