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

class VmcMasterCard extends HTMLElement {
  constructor() {
    super();
    this._config = undefined;
    this._hass = undefined;
    this._scheda = undefined;
    this._caricata = undefined; // VMC (entry_id) della scheda costruita o in costruzione
    this._connessione = undefined; // collegamento a Home Assistant che stiamo ascoltando
    // Dopo un riavvio di Home Assistant (per esempio dopo un aggiornamento) il browser
    // si ricollega senza ricaricare la pagina: si chiede di nuovo la configurazione,
    // cosi' la scheda e' sempre quella della versione installata, senza Ctrl+F5.
    this._alRicollegamento = () => {
      this._caricata = undefined;
      this._carica();
    };
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
    this._caricata = vmc;
    try {
      const [configurazione, aiuti] = await Promise.all([
        this._hass.callApi("GET", `${DOMINIO}/scheda/${vmc}`),
        window.loadCardHelpers(),
      ]);
      if (this._caricata !== vmc) {
        return; // nel frattempo e' stata scelta un'altra VMC
      }
      const scheda = aiuti.createCardElement(configurazione);
      scheda.hass = this._hass;
      this._scheda = scheda;
      this.replaceChildren(scheda);
    } catch (errore) {
      this._caricata = undefined;
      const dettaglio = errore && (errore.body?.message || errore.message);
      this._messaggio(
        `Scheda VMC Master non disponibile${dettaglio ? `: ${dettaglio}` : ""}. ` +
          "Verificare che la VMC sia configurata in Impostazioni → Dispositivi e servizi → VMC Master."
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
