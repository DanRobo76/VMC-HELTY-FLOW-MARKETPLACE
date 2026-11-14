<p align="center">
  <img src="custom_components/vmc_master/brand/icon@2x.png" alt="VMC Master" width="128">
</p>

# VMC Master: integrazione per il Marketplace di Home Assistant

Integrazione per **VMC Helty Flow Plus/Elite** che installa e aggiorna il package **VMC Master** dal Marketplace di Home Assistant (HACS integrato da Home Assistant 2026.11).

> **Versione beta (9.0.0b1).** La logica di funzionamento è quella della release manuale **8.6.0** del repository [VMC-HELTY-FLOW](https://github.com/DanRobo76/VMC-HELTY-FLOW), senza modifiche: l'integrazione genera gli stessi file che oggi creano a mano gli script Clona e Cambia IP. Chi preferisce l'installazione manuale continua a usare la 8.6.0, che non cambia.

<sub>[English below](#english)</sub>

---

## Cosa fa

- **Una voce per ogni VMC**: si aggiunge da *Impostazioni → Dispositivi e servizi → Aggiungi integrazione → VMC Master* scrivendo nome e IP.
- **Installa il package** in `config/packages/vmc_helty_flow/‹nome›`: `vmc_‹nome›.yaml`, l'automazione principale (ora nel package, non va più incollata) e gli script Cambia IP e Cambia Nome.
- **Scheda «VMC Master» inclusa**: si aggiunge dalla plancia con *Aggiungi scheda → VMC Master* e si sceglie la VMC. È la stessa scheda della 8.6.0, con le stesse schede native di Home Assistant e le stesse immagini; si aggiorna insieme all'integrazione.
- **Aggiornamenti dal Marketplace**: a ogni nuova versione i file del package vengono riscritti e Home Assistant chiede il riavvio con una riparazione (*Impostazioni → Riparazioni*). L'IP impostato resta quello.

### Differenze rispetto all'installazione manuale 8.6.0

| Funzione | Manuale 8.6.0 | Integrazione |
|---|---|---|
| Aggiungere una VMC | Finestra Clona + incollare automazione e scheda | *Aggiungi voce* (nome + IP), nient'altro da incollare |
| Cancellare una VMC | Finestra Clona + cancellare a mano automazione e scheda | Eliminare la voce: la cartella va in `config/vmc_master_backup` |
| Cambiare IP | Campo «Cambia IP VMC» della scheda | Lo stesso campo, oppure *Configura* sulla voce |
| Cambiare nome della VMC | Campo «Cambia Nome VMC» | Invariato |
| Prima Installazione VMC | Nella scheda Master | Invariata, nella scheda Master |
| Automazione principale | Incollata nell'editor (modificabile) | Nel package (`vmc_‹nome›_automazione.yaml`, sola lettura) |
| Nomi delle entità | `vmc_master_…`, `vmc_‹nome›_…` | Identici: la cronologia resta |

La Finestra Clona non c'è più: nella scheda e nel package viene tolto solo il blocco fra i segnaposto «SEZIONE CLONA VMC», lo stesso che la 8.6.0 toglie già alle VMC clonate.

---

## Requisiti

- Home Assistant **2026.11** o successivo (Marketplace integrato).
- Package abilitati nel file `configuration.yaml` (come per la 8.6.0):

```yaml
homeassistant:
  packages: !include_dir_named packages/
```

Se la riga manca, l'integrazione lo segnala in *Impostazioni → Riparazioni*.
- IP statico della VMC impostato nel router; la VMC risponde sulla porta **5001**.

---

## Installazione

### 1. Aggiungere il repository al Marketplace
Finché l'integrazione non è nel catalogo pubblico, si aggiunge come repository personalizzato:

1. **Impostazioni → Marketplace**, menu **⋮** in alto a destra → **Repository personalizzati**;
2. indirizzo: `https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE`, tipo **Integrazione** → **Aggiungi**;
3. cercare **VMC Master** e premere **Scarica**;
4. riavviare Home Assistant se il Marketplace lo chiede.

### 2. Aggiungere la VMC
**Impostazioni → Dispositivi e servizi → Aggiungi integrazione → VMC Master**:
- **Nome VMC**: la prima si chiama `master`; le altre con sole lettere minuscole, da 1 a 10 caratteri;
- **IP VMC su porta 5001**.

Se la VMC non risponde si può aggiungere comunque (per esempio per collegarla al Wi-Fi con la Finestra Prima Installazione VMC) e cambiare l'IP più tardi da *Configura*.

### 3. Riavviare Home Assistant
In *Impostazioni → Riparazioni* compare **«VMC Master: riavviare Home Assistant»**: aprirla e confermare.

### 4. Aggiungere la scheda
Nella plancia: **icona matita → Aggiungi scheda → VMC Master**, scegliere la VMC e salvare. Su una plancia nuova creare prima una plancia da zero (*Impostazioni → Plance → Aggiungi plancia*).

### 5. Profilo Inizializzazione
Come nella 8.6.0: nel pannello **Impostazioni** della scheda premere **Esegui** su **«VMC ‹nome› - Profilo Inizializzazione»** e scegliere le entità dei sensori in **«Opzioni - Sensori da Selezionare»**.

### Altre VMC
Ripetere i punti 2-5 con un nome diverso. Per eliminare una VMC eliminare la sua voce in *Dispositivi e servizi*, togliere la sua scheda e riavviare.

---

## Passare dalla 8.6.0 manuale all'integrazione

1. Installare l'integrazione (punto 1).
2. Aggiungere la VMC con **lo stesso nome** di prima (`master`, poi le clonate): l'integrazione trova la cartella manuale, propone l'IP già impostato e chiede conferma.
3. Confermando, la cartella manuale viene spostata in `config/vmc_master_backup/‹nome›_‹data›` e sostituita da quella dell'integrazione. I nomi delle entità restano uguali, quindi la cronologia si conserva.
4. Riavviare, poi eliminare l'automazione incollata a mano **«Automazione VMC ‹nome›»** (*Impostazioni → Automazioni e scenari*) e la vecchia scheda manuale, e aggiungere la scheda **VMC Master**.

---

## Licenza

**GNU General Public License v3.0** (file [LICENSE](LICENSE)). Copyright © 2023-2026 Ing. Danilo Robotti.

È consentito usare, copiare, modificare e distribuire il software, anche per scopi commerciali; chi lo distribuisce, anche modificato, deve renderne disponibile il codice sorgente con la stessa licenza e mantenere la nota di copyright. Il software è fornito senza alcuna garanzia.

La release manuale 8.6.0 del repository [VMC-HELTY-FLOW](https://github.com/DanRobo76/VMC-HELTY-FLOW) resta sotto PolyForm Noncommercial License 1.0.0.

**Impiego dell'Intelligenza Artificiale:** nello sviluppo del software l'autore si è avvalso anche di strumenti di intelligenza artificiale.

---

<a id="english"></a>
## English

Integration for **Helty Flow Plus/Elite** ventilation units that installs and updates the **VMC Master** package from the Home Assistant Marketplace (HACS built in since Home Assistant 2026.11).

- The logic is the unchanged manual release **8.6.0** of [VMC-HELTY-FLOW](https://github.com/DanRobo76/VMC-HELTY-FLOW): the integration writes the same files the Clone and Change IP scripts create by hand.
- **One entry per unit** (name + IP) from *Settings → Devices & services → Add integration → VMC Master*. The package goes to `config/packages/vmc_helty_flow/‹name›`, including the main automation (no more pasting).
- **«VMC Master» card included**: *Add card → VMC Master*, then pick the unit. Same card as 8.6.0, updated with the integration.
- Requirements: Home Assistant 2026.11+, `packages: !include_dir_named packages/` in `configuration.yaml`, static IP for the unit (port 5001).
- Install as a custom repository: *Settings → Marketplace → ⋮ → Custom repositories*, URL `https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE`, type **Integration**.
- Moving from manual 8.6.0: add the unit with the same name; the manual folder is moved to `config/vmc_master_backup` and entity names (and history) stay the same. Then delete the hand-pasted automation and old card.

Licence: **GPL-3.0**. Copyright © 2023-2026 Ing. Danilo Robotti.
