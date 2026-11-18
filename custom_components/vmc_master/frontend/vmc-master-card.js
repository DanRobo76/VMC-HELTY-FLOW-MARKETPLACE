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

class VmcMasterCard extends HTMLElement {
  constructor() {
    super();
    this._config = undefined;
    this._hass = undefined;
    this._scheda = undefined;
    this._caricata = undefined; // VMC (entry_id) della scheda costruita o in costruzione
    this._connessione = undefined; // collegamento a Home Assistant che stiamo ascoltando
    this._errore = undefined; // { vmc, alle }: ultima richiesta della scheda non riuscita
    this._sensoreRepository = undefined; // sensore «Versione Repository» della scheda
    this._ultimoControllo = 0; // ora dell'ultimo controllo aggiornamenti dalla scheda
    // Dopo un riavvio di Home Assistant (per esempio dopo un aggiornamento) il browser
    // si ricollega senza ricaricare la pagina: si chiede di nuovo la configurazione,
    // cosi' la scheda e' sempre quella della versione installata, senza Ctrl+F5.
    this._alRicollegamento = () => {
      this._caricata = undefined;
      this._errore = undefined;
      this._carica();
    };
    // Apertura del Pannello Informazioni: si controlla subito se c'e' una nuova release,
    // come fa «Agg. Sensori» per la versione installata. Il clic attraversa le schede
    // interne (shadow DOM): composedPath() da' anche gli elementi al loro interno.
    this._alClic = (evento) => this._controllaAggiornamenti(evento);
    this.addEventListener("click", this._alClic);
  }

  _controllaAggiornamenti(evento) {
    const percorso = typeof evento.composedPath === "function" ? evento.composedPath() : [];
    const titolo = percorso.find((elemento) => elemento && elemento.tagName === "SUMMARY");
    if (!titolo || (titolo.textContent || "").trim() !== "Informazioni") {
      return;
    }
    const pannello = titolo.parentElement;
    // il clic arriva prima che il pannello cambi stato: aperto ora = si sta chiudendo
    if (!pannello || pannello.tagName !== "DETAILS" || pannello.open) {
      return;
    }
    const sensore = this._trovaSensoreRepository();
    const adesso = Date.now();
    if (!sensore || !this._hass || adesso - this._ultimoControllo < ATTESA_CONTROLLO_MS) {
      return;
    }
    this._ultimoControllo = adesso;
    Promise.resolve()
      .then(() =>
        this._hass.callService("homeassistant", "update_entity", { entity_id: sensore })
      )
      .catch(() => {
        // controllo non riuscito: la scheda mostra lo stato del sensore
      });
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
  }

  connectedCallback() {
    if (this._hass) {
      this._ascolta(this._hass.connection);
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
    this._scheda = undefined;
    this.replaceChildren();
    const card = document.createElement("ha-card");
    const corpo = document.createElement("div");
    corpo.style.padding = "16px";
    corpo.textContent = testo;
    card.appendChild(corpo);
    this.appendChild(card);
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
      this._errore = undefined;
      const trovato = JSON.stringify(configurazione).match(RE_SENSORE_REPOSITORY);
      this._sensoreRepository = trovato ? trovato[0] : undefined;
      const scheda = aiuti.createCardElement(configurazione);
      scheda.hass = this._hass;
      this._scheda = scheda;
      this.replaceChildren(scheda);
    } catch (errore) {
      if (this._caricata !== vmc) {
        return; // errore di una richiesta vecchia: nel frattempo e' stata scelta un'altra VMC
      }
      this._caricata = undefined;
      this._errore = { vmc, alle: Date.now() };
      const dettaglio = errore && (errore.body?.message || errore.message);
      const consiglio =
        errore && errore.status_code === 404
          ? "Scegliere di nuovo la VMC nelle opzioni della scheda."
          : "Verificare che la VMC sia configurata in Impostazioni → Dispositivi e servizi → VMC Master.";
      this._messaggio(
        `Scheda VMC Master non disponibile${dettaglio ? `: ${dettaglio}` : ""}. ${consiglio}`
      );
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
