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
// Controllo aggiornamenti all'apertura del Pannello Informazioni: al massimo una volta
// ogni 5 minuti (GitHub accetta 60 richieste all'ora senza autenticazione)
const ATTESA_CONTROLLO_MS = 5 * 60 * 1000;
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

function titoloInformazioni(elemento) {
  return (
    elemento &&
    elemento.tagName === "SUMMARY" &&
    (elemento.textContent || "").trim() === TITOLO_INFORMAZIONI
  );
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
    this._errore = undefined; // { vmc, alle }: ultima richiesta della scheda non riuscita
    this._sensoreRepository = undefined; // sensore «Versione Repository» della scheda
    this._riprova = undefined; // nuovo tentativo dopo un ricollegamento non riuscito
    this._daAggiornare = false; // ricollegamento senza risposta: si riprova
    this._osservatore = undefined; // tiene aperto il Pannello Informazioni
    // Dopo un riavvio di Home Assistant il browser si ricollega senza ricaricare la pagina
    // (succede anche sbloccando il telefono o dopo un calo di rete): si chiede di nuovo la
    // configurazione e la scheda si ricostruisce solo se e' cambiata, per esempio dopo un
    // aggiornamento. Vale per la configurazione della scheda; questo file JavaScript resta
    // quello gia' caricato fino al ricaricamento della pagina.
    this._alRicollegamento = () => {
      if (this._scheda) {
        this._aggiorna();
        return;
      }
      this._caricata = undefined;
      this._errore = undefined;
      this._carica();
    };
    // Apertura del Pannello Informazioni: si controlla subito se c'e' una nuova release,
    // come fa «Agg. Sensori» per la versione installata. Il clic attraversa le schede
    // interne (shadow DOM): composedPath() da' anche gli elementi al loro interno.
    this._alClic = (evento) => this._clicInformazioni(evento);
    this.addEventListener("click", this._alClic);
  }

  _clicInformazioni(evento) {
    const percorso = typeof evento.composedPath === "function" ? evento.composedPath() : [];
    const titolo = percorso.find(titoloInformazioni);
    if (!titolo) {
      return;
    }
    const pannello = titolo.parentElement;
    if (!pannello || pannello.tagName !== "DETAILS") {
      return;
    }
    // il clic arriva prima che il pannello cambi stato: aperto ora = si sta chiudendo
    if (pannello.open) {
      this._fermaOsservatore();
      return;
    }
    this._tieniAperto(pannello);
    this._controllaAggiornamenti();
  }

  // La scheda markdown che contiene il pannello si ridisegna quando cambia un suo valore
  // (per esempio la riga della versione dopo il controllo aggiornamenti) e il pannello
  // si richiuderebbe: finche' l'utente non lo chiude, lo si riapre subito.
  _tieniAperto(pannello) {
    this._fermaOsservatore();
    if (typeof MutationObserver !== "function") {
      return;
    }
    const radice = pannello.getRootNode();
    const contenitore = radice === document ? pannello.parentNode : radice;
    if (!contenitore || typeof contenitore.querySelectorAll !== "function") {
      return;
    }
    this._osservatore = new MutationObserver(() => {
      const titolo = Array.from(contenitore.querySelectorAll("details > summary")).find(
        titoloInformazioni
      );
      if (titolo && !titolo.parentElement.open) {
        titolo.parentElement.open = true;
      }
    });
    this._osservatore.observe(contenitore, { childList: true, subtree: true });
  }

  _fermaOsservatore() {
    if (this._osservatore) {
      this._osservatore.disconnect();
      this._osservatore = undefined;
    }
  }

  _controllaAggiornamenti() {
    // L'integrazione e' una sola per tutte le VMC: si aggiornano i sensori «Versione
    // Repository» di tutte, cosi' ogni scheda mostra subito lo stesso avviso
    const sensori = this._sensoriRepository();
    const adesso = Date.now();
    if (
      !sensori.length ||
      !this._hass ||
      adesso - (ULTIMI_CONTROLLI.tutte || 0) < ATTESA_CONTROLLO_MS
    ) {
      return;
    }
    ULTIMI_CONTROLLI.tutte = adesso;
    Promise.resolve()
      .then(() =>
        this._hass.callService("homeassistant", "update_entity", { entity_id: sensori })
      )
      .catch(() => {
        // controllo non riuscito: la scheda mostra lo stato del sensore
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
    if (this._daAggiornare) {
      this._aggiorna();
    }
  }

  _ascolta(connessione) {
    if (this._connessione === connessione) {
      return;
    }
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
      this._fermaRiprova();
      this._carica();
    }
  }

  set hass(hass) {
    this._hass = hass;
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

  _messaggio(testo) {
    this._fermaOsservatore();
    this._scheda = undefined;
    this._testoConfigurazione = undefined;
    this.replaceChildren();
    const card = document.createElement("ha-card");
    const corpo = document.createElement("div");
    corpo.style.padding = "16px";
    corpo.textContent = testo;
    card.appendChild(corpo);
    this.appendChild(card);
  }

  _costruisci(configurazione, testo, aiuti) {
    this._fermaOsservatore();
    this._errore = undefined;
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
    this._errore = { vmc, alle: Date.now() };
    const dettaglio = errore && (errore.body?.message || errore.message);
    const consiglio = vmcNonTrovata(errore)
      ? "Scegliere di nuovo la VMC nelle opzioni della scheda."
      : "Verificare che la VMC sia configurata in Impostazioni → Dispositivi e servizi → VMC Master.";
    this._messaggio(
      `Scheda VMC Master non disponibile${dettaglio ? `: ${dettaglio}` : ""}. ${consiglio}`
    );
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
    let configurazione;
    try {
      configurazione = await this._hass.callApi("GET", `${DOMINIO}/scheda/${vmc}`);
    } catch (errore) {
      if (this._caricata !== vmc || !this._scheda) {
        return; // nel frattempo e' stata scelta un'altra VMC
      }
      if (vmcNonTrovata(errore)) {
        this._mostraErrore(vmc, errore);
        return;
      }
      this._daAggiornare = true;
      if (this.isConnected) {
        this._riprova = setTimeout(() => this._aggiorna(), ATTESA_DOPO_ERRORE_MS);
      }
      return;
    }
    if (this._caricata !== vmc || !this._scheda) {
      return;
    }
    const testo = JSON.stringify(configurazione);
    if (testo === this._testoConfigurazione) {
      return; // configurazione invariata: la scheda resta com'e'
    }
    try {
      const aiuti = await window.loadCardHelpers();
      if (this._caricata === vmc) {
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
      this._messaggio("Scegliere la VMC nelle opzioni della scheda.");
      return;
    }
    if (this._caricata === vmc) {
      return;
    }
    if (
      this._errore &&
      this._errore.vmc === vmc &&
      Date.now() - this._errore.alle < ATTESA_DOPO_ERRORE_MS
    ) {
      return; // errore recente: non si riprova a ogni cambio di stato
    }
    this._caricata = vmc;
    try {
      const [configurazione, aiuti] = await Promise.all([
        this._hass.callApi("GET", `${DOMINIO}/scheda/${vmc}`),
        window.loadCardHelpers(),
      ]);
      if (this._caricata !== vmc) {
        return; // nel frattempo e' stata scelta un'altra VMC
      }
      this._costruisci(configurazione, JSON.stringify(configurazione), aiuti);
    } catch (errore) {
      if (this._caricata !== vmc) {
        return; // errore di una richiesta vecchia: nel frattempo e' stata scelta un'altra VMC
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
