# Simulatore VMC Master e prova differenziale

È il simulatore della b36 (`/home/user/sim36/simulatore-b36`) portato nel repository, con in più la
**traccia completa** di ogni scenario e la **prova differenziale**: gli stessi scenari girano con le
automazioni e gli script YAML di oggi (variante A, `identica`) e con un'altra variante B (per esempio il
motore in Python, vedi `custom_components/vmc_master/nativa/motore/PORTARE_IL_MOTORE.md`) e le tracce
devono essere identiche: stessi comandi alla VMC agli stessi istanti virtuali, stessi cambi di stato di
tutte le entità della VMC, stesse chiamate di servizio con effetti esterni. Zero differenze accettate.

Avvia un vero Home Assistant 2026.11.1 con un orologio virtuale (`vclock.py`) e una VMC finta
(`fakevmc.py`), carica il package della VMC «master», fa l'avvio e il riscaldamento una volta e poi un
processo figlio (fork) per scenario. `gen.py` genera i 17.264 scenari (famiglie S, P, F, C, W, K, R);
`gen_mancanti.py` la famiglia M (131 scenari per le automazioni, gli script e i rami che i 17.264 non
eseguono mai, sez. 3bis); `oracle.py` e `analyze.py` sono l'oracolo della b36 (funzionano come prima sui
file dei risultati, non sulla famiglia M).

## Requisiti

Linux (usa `os.fork`) e il Python di Home Assistant 2026.11.1 con le sue dipendenze (qui
`/home/user/hav/bin/python`). Tutti i comandi si lanciano da questa cartella.

## 1. Configurazione di Home Assistant

    python build_config.py /home/user/sim-diff/cfg

Scrive in `<cfg>/packages/vmc_helty_flow/master/` i file che l'integrazione installa per la VMC
«master» (`installatore.genera_file`: `trasforma.package_per_vmc` con `rimuovi_sezioni_solo_master`,
IP di prova `192.168.1.160`, `adatta_versione`, `adatta_link_repository`, automazione come package),
**identici byte per byte** (md5 in `<cfg>/SORGENTE.json`, con il commit), e `configuration.yaml` con
`packages: !include_dir_named packages/`. Le due parti del package che il simulatore non può usare
restano nel file e si spengono all'avvio (`simlib.boot`): la chiave `recorder:` non avvia il registro
e il sensore `platform: rest` (versione del repository, andrebbe in rete) non viene creato. Servizi
finti (non fanno niente, ma le chiamate restano nella traccia): `tts.*`, `media_player.*`,
`notify.notify`, `recorder.purge_entities`, `recorder.get_statistics`, `vmc_master.verifica_ip` e
`homeassistant.restart` (un riavvio vero fermerebbe il simulatore). `vmc_master.verifica_ip` risponde come
il servizio dell'integrazione (solo risposta: `risponde`, `nome`, `esito`) senza leggere la rete: esito e
ritardo li sceglie lo scenario (azione `verifica_ip`, di base `non_risponde`). All'avvio `simlib` crea un
utente amministratore con id `utente_simulatore`: le azioni di un utente degli scenari (`card_u`, `ui`,
tasti degli script) hanno un `Context` con il suo `user_id`, come quelle del frontend (con un utente che
non esiste i servizi delle entità rifiutano la chiamata, `UnknownUser`).

Altre parti di Home Assistant spente da `simlib` (come nella b36: niente frontend, niente rete):
il server web non apre la porta (`http` viene caricato lo stesso perché `notify` dipende da `repairs`
che dipende da `http`; `SIM_HTTP=vero` lo riaccende, solo per prove); delle integrazioni
personalizzate si ignorano le dipendenze da `frontend`, `http`, `lovelace`, `repairs`, `onboarding`,
`websocket_api`, `api`, `config`, `cloud`, `auth`, `person` e dalle scoperte di rete
(`simlib.DIPENDENZE_TOLTE`), così una variante con un componente personalizzato non riporta dentro il
frontend; le cartelle `custom_components` e i lavori di avvio restano.

## 2. Giro semplice e oracolo

    python targeted.py out.jsonl <cfg> '<regex>' [n_campione] [nproc] [--variante <modulo>] [--coda <s>]
    python targeted.py out.jsonl <cfg> '^M\|' 0 3 --coda 60      # la famiglia M (sez. 3bis)
    python run_full.py out.jsonl <cfg> [nproc]                   # tutti i 17.264 (senza la famiglia M)
    python analyze.py out.jsonl 40 --cfg <cfg>                    # oracolo della b36
    python mostra.py out.jsonl 'S|CO2'                            # velocità scenario per scenario

La regex è cercata nell'id: `|` va scritto `\|` (es. `'^S\|CO2\|'`); `@file` legge gli id da un file.
`targeted.scegli` cerca tra i 17.264 scenari di `gen.py` e quelli della famiglia M (una regex come `.`
prende anche questi). La parola `blackout` al posto della regex sceglie i 4.842 scenari Black-Out della
simulazione completa di ogni versione (`famiglie_blackout.py`: `bo_a.py` 3.480, `b36bo.py` 982,
`b36bo_extra.py` 380, copiati senza modifiche dal simulatore della b36); un file `@` li trova anche
mischiati agli altri, una regex mai (gli id dei Black-Out non coincidono con gli altri).
La prima riga del file dei risultati ha id `__avvio__` (traccia dell'avvio, vedi sotto).

## 3. Prova differenziale

    python differenziale.py <uscita> '<regex>|@file' [n_campione] [nproc] --variante <modulo B> \
        [--variante-a varianti.identica] [--cfg <cfg>] [--coda <s>] [--mappa <csv>]
    python confronta.py A.jsonl B.jsonl --rapporto rapporto.txt  # confronto di due giri già fatti

`differenziale.py` sceglie gli scenari una volta (`<uscita>/scenari.ids`), copia la configurazione
(senza `--cfg` la crea dal repository) in `cfg_A` e `cfg_B`, passa ogni copia a
`prepara_configurazione` della sua variante, lancia A e poi B con `nproc` processi (`A.jsonl`,
`B.jsonl`, `A.log`, `B.log`) e scrive `rapporto.txt`, `rapporto.txt.json` e
`rapporto.txt.diversi.ids` (da rilanciare con `targeted.py ... @rapporto.txt.diversi.ids`).
Rilanciato con gli stessi argomenti riprende i giri interrotti. Se si cambia il codice di una variante
(o, con `nativa4`, dell'integrazione: `cfg_B` ne tiene una copia), cancellare `<uscita>/cfg_B` (la copia
preparata resta, segnata da `.preparata`), `B.jsonl`, `B.log` e `rapporto.txt*`.
Per provare un'altra B sugli stessi scenari senza rifare A: copiare in una nuova `<uscita>` i file
`scenari.ids`, `A.jsonl` e la cartella `cfg_A` di un giro finito (il giro A trova tutto fatto).
`--coda 60` registra nella traccia anche 60 s virtuali dopo la fine di ogni scenario (comandi o cambi
di stato in ritardo); i campi dell'oracolo restano quelli fino alla fine.

`--mappa tests/nativa/motore/aiutanti_fase1.csv` (opzione di `confronta.py`, passata da
`differenziale.py`) serve con B = `nativa4`, l'integrazione nativa della fase 4, dove le entità della VMC
non sono più quelle del package: prima del confronto le voci dei due lati passano dalla mappa dei nomi
(`mappa.py`, dalla colonna «Domani» della fase 1): entity_id di oggi → di domani, attributi che solo
l'aiutante ha, timer e valori interni come voci `MS`/`MR` («nel motore»), comandi di shell nelle forme
`tcp: <comando>`, `ping <ip>`, `tcp: VMNM <nome>`. Le voci che la mappa toglie (o
cambia) si contano per tipo, lato e motivo e il rapporto le elenca con i numeri esatti in cima; nessuna
tolleranza oltre a quelle scritte in `mappa.py`. Dalla b46 il campo «Cambia IP VMC» non c'è più nella
versione nativa: la mappa toglie dal lato A le sue voci (motivo `tolta`) e gli scenari `IP` della
famiglia M provano solo il lato A. Esempio (giro completo, A riusato da un giro finito):

    VMC_RADICE=<repository> python differenziale.py <uscita> '@<uscita>/scenari.ids' 0 3 \
        --variante varianti.nativa4 --cfg <cfg_base> --coda 60 \
        --mappa <repository>/tests/nativa/motore/aiutanti_fase1.csv

### Varianti

Una variante è un modulo Python (nome importabile da questa cartella, es. `varianti.identica`, o un
file `.py`) con:

- `prepara_configurazione(cfg_dir) -> None`: modifica la configurazione generata (la chiama
  `differenziale.py`). Aiuti in `pacchetto.py`: `pacchetto.togli(cfg, automazioni='tutte',
  script='tutti')` toglie automazioni e script YAML (riscrive i file e controlla che il YAML riletto
  sia quello atteso); `pacchetto.aggiungi_integrazione(cfg, dominio, cartella, 'dominio:\n')` copia
  un'integrazione personalizzata in `<cfg>/custom_components/<dominio>` e la aggiunge a
  `configuration.yaml` (il `manifest.json` deve avere `version`). Home Assistant la carica con le altre
  e fa girare i suoi lavori di avvio (`hass.async_add_startup_job`) prima di `homeassistant_started`,
  come per le automazioni YAML;
- `async avvia(hass) -> None`: chiamata subito dopo l'avvio di Home Assistant, prima del riscaldamento;
- facoltativa `async prima_dell_avvio(hass) -> None`: dopo il setup delle integrazioni e prima di
  `hass.async_run` (prima dell'evento `homeassistant_start`);
- facoltativa `async script(hass, entity_id, dati, contesto) -> bool`: per l'azione `script` degli
  scenari (Bottone Panico) il runner la chiama per prima, con il `Context` che userebbe; se restituisce
  True la chiamata `script.turn_on` non si fa (gli script YAML tolti dalla variante nativa);
- facoltativa `async servizio(hass, dominio, servizio, dati, blocking, contesto) -> bool`: per ogni
  azione di servizio degli scenari (`simlib.svc`) la chiama per prima; se restituisce True la chiamata
  di oggi non si fa (in `nativa4`: le stesse azioni sulle entità di domani, il pulsante al posto dello
  shell_command o dello script, la scrittura del motore per un valore interno).

Varianti fornite:

- `identica`: niente (lato A e prova di determinismo);
- `nativa4`: l'integrazione nativa della fase 4 (`nativa/assemblaggio.py`, `VMCAssemblata`) al posto
  di tutto il package, da confrontare con `--mappa`. La VMC finta resta quella del lato A: letture e
  comandi come il sensore tcp e i comandi di shell finti (0,05 s / 3 s; il ping 0,05 s / 4 s; il cambio
  del nome e dell'indirizzo e i comandi senza effetto fuori da Home Assistant, oggi il «find ... sed»,
  0,01 s come il file .sh finto). Le voci del motore entrano nella traccia nel punto del bus in cui Home
  Assistant consegnerebbe le loro: i comandi (`C`) e i cambi dei timer (`MS`) con un evento
  `state_reported` con un marchio, i valori interni dalla memoria interna; `prima_dell_avvio` rimette
  gli ascoltatori della traccia davanti ai distributori dei tracker (solo il punto in cui la traccia
  annota, nessun effetto sul comportamento);
- `riscritta`: riscrive i file del package con `pacchetto`; deve dare zero differenze;
- `prova_ritardo`: ritarda di 10 ms ogni `shell_command.vmc_master_velocita_0`; deve dare differenze
  esattamente negli scenari con quel comando (prova che il confronto vede una differenza piccola);
- `prova_componente`: integrazione personalizzata minima (`manifest.json` con dipendenze `frontend`,
  `http`, `lovelace`, `repairs`), un lavoro di avvio e l'aggancio `script`; deve dare zero differenze
  (prova che il simulatore carica un componente personalizzato e fa girare il lavoro di avvio);
- `prova_timer`: un timer che non fa niente ogni 0,37 s (più due timer registrati e annullati); deve
  dare zero differenze (prova che i timer di un motore non cambiano l'ordine degli altri, sez. 6);
- `prova_casuale`: consuma numeri casuali e crea ascoltatori di orari che non fanno niente, prima
  dell'avvio e ogni 7 s; deve dare zero differenze (sez. 6);
- `prova_audio`: ritarda di 10 ms ogni `tts.google_translate_say` (avvisi audio, mai eseguiti dai
  17.264); sulla famiglia M deve dare differenze esattamente negli scenari con un avviso audio;
- `nativa`: il motore in Python del repository principale (`$VMC_RADICE`, di default
  `/home/user/vmc-helty-flow-nativa`): toglie le 14 automazioni e i 51 script YAML, copia
  `custom_components/vmc_master` e aggiunge l'integrazione `sim_motore_nativo` che avvia `Motore`.

**Giro completo `identica` contro `nativa`** (26-11-2026, motore a e45db0c, uguale a c62e005 in
`custom_components`; `'.'` = tutte le famiglie, 4 processi, `--coda 60`): **17.396 / 17.396 identici**,
0 diversi, 0 mancanti, 0 errori. Per famiglia (diversi / scenari): C 0 / 768, F 0 / 1600, K 0 / 288,
M 0 / 131, P 0 / 9664, R 0 / 656, S 0 / 3840, W 0 / 448, `__avvio__` 0 / 1.

**Giro completo `identica` contro `nativa4`** (26-11-2026, integrazione a c0ec1b0, A riusato dal giro
sopra; `'.'` = tutte le famiglie, 3 processi, `--coda 60`, `--mappa
tests/nativa/motore/aiutanti_fase1.csv`): **17.396 / 17.396 identici**, 0 diversi, 0 mancanti, 0 errori,
con le stesse famiglie e gli stessi numeri del giro sopra. Voci tolte o cambiate dalla mappa (tutti gli
scenari, numero tipo lato): 16.353 C B (chiamate dell'utente alle entità native), 4 X A (comando di
shell «find ... sed»), 68+68 I/F A (valori interni), 34+34 I/F A (timer), 51+51 I/F A, 5.677 R A e
179.278 S A (entità degli script), 25+25 I/F B e 1.283 S B (pulsanti), 34+34 I/F B e 177.846 S B
(sensori di fine dei timer); 9.536 C A cambiate (update_entity senza i valori interni). Nessun'altra
tolleranza.

`copertura.py <risultati.jsonl> [altri.jsonl ...] [--trigger]` dice quali automazioni e script hanno
girato negli scenari (e nell'avvio), sommando più file; con `--trigger` anche quali trigger (id)
dell'Automazione VMC Master sono scattati nella timeline degli scenari (campo `trig`) e quali mai. Le parti
mai eseguite non sono provate dal differenziale (sez. 8).

## 3bis. Famiglia M (parti del package che i 17.264 scenari non eseguono)

`gen_mancanti.py`, 131 scenari con id `M|<gruppo>|...`, tutti con la VMC veloce (latenza 0,5 s). Ogni
scenario fa quello che fa l'utente dalla scheda o dall'interfaccia di Home Assistant, o quello che succede
in casa:

| gruppo | scenari | cosa prova |
|---|---|---|
| `AUD` | 27 | `audio_allerte_e_stato` e gli script `audio_*`: media player in casa, elenco aggiornato e scelto nella scheda, Profilo Audio, poi ogni allerta (inizio e fine, anche Congelamento e Δ Temp. «[No ma Prossimo]», Black-Out, Free H./C.) o cambi di velocità; rami: audio spento, nessun media player, fuori fascia, fascia oltre la mezzanotte (dentro e fuori), categoria spenta, volume |
| `RIE` | 16 | `riepilogo_audio_avvio`: «Esegui azioni» dall'interfaccia (`automation.trigger` con le condizioni) con ogni allerta in corso, a VMC OFF-Line, un'allerta che inizia durante il riepilogo, audio o riepilogo spenti, senza condizioni e senza media player, spia dell'avvio rimasta accesa 10 minuti (secondo trigger) |
| `RIA` | 9 | `riallineamento_allerte_al_riavvio` (`automation.trigger`, le 4 fasi in 200 s) con un'allerta che inizia nella fase 1 |
| `INI` | 3 | `inizializza_tempi_di_attesa` e `ripristina_tempi_attesa`: `automation.trigger` con e senza condizioni, `attese_inizializzate` spento |
| `IP` | 13 | `cambio_ip_vmc_riavvio_di_h_a`: IP non valido (4 casi), testo, uguale, di un'altra VMC (`sensor.vmc_soggiorno_ip`), valido con esito `ok` (comandi di shell e riavvio), `non_risponde`, `altro_dispositivo`, `nome_diverso`, IP cambiato durante la verifica, VMC OFF-Line |
| `UI`, `FIN` | 18 + 2 | finestre e pannelli della scheda aperti e chiusi (rami «Opzioni ...» dell'automazione principale) e `esclusivita_finestre_opzioni` (tutti i suoi trigger) |
| `NOT` | 15 | script `notifica_*`: cellulare dell'app scelto o no, cambi di velocità, ogni sensore scelto non disponibile, cellulare tolto, servizio di notifica mancante (chiamata non riuscita, voce `E`), notifica spenta; `notifica_cambio_filtro` e `notifica_errore_media_player` dallo script |
| `PUL` | 3 | pulizia della cronologia (conferma Sì / No) e della cache audio |
| `PRO` | 11 | Profilo Inizializzazione (da Velocità 2 e 0), Calendario, Free, PdR, Umidità, Audio, Azzera Offset, Azzera Aria Scambiata, Reset Filtro, Agg. Sensori |
| `VAR` | 4 | Rinomina VMC (valido e no), nuova versione nel repository, scelta di sensori, media player e cellulare |
| `RIP` | 10 | `ripartenza_della_vmc`: taglio della corrente di 10 s (più breve del Black-Out) da ogni velocità, la VMC riparte a Velocità 1; da Velocità 1, VMC che riprende la velocità, comando durante il taglio, durante una Fascia del Calendario |

Azioni del runner aggiunte per la famiglia M (le altre famiglie non le usano):

- `('ui', dominio, servizio, dati)`: servizio chiamato da un utente (scheda o interfaccia di HA),
  non bloccante, `Context` con `user_id`;
- `('script', entity_id, dati, True)`: tasto della scheda che lancia uno script (`script.turn_on` con le
  variabili e il contesto dell'utente; senza i due argomenti in più resta l'azione del Bottone Panico);
- `('stato', entity_id, stato, attributi)`: entità fuori dal package (media player, sensore IP di
  un'altra VMC, versione del repository, sensore scelto non disponibile, cellulare tolto);
- `('telefono', nome[, con_servizio])`: cellulare con l'app Home Assistant come lo crea l'integrazione
  Mobile App, senza avviarla (`simlib.aggiungi_telefono`: voce di configurazione, dispositivo, device_tracker
  della piattaforma `mobile_app`, letto da `integration_entities('mobile_app')`, e il servizio finto
  `notify.mobile_app_<nome>`; senza servizio la notifica non riesce);
- `('verifica_ip', esito[, ritardo])`: risposta del servizio finto `vmc_master.verifica_ip`;
- `('attendi', s)`: pausa nella preparazione dello scenario.

Limiti della famiglia M: il riavvio di Home Assistant non si può fare in un processo figlio (il trigger
`homeassistant: start` scatta solo durante l'avvio vero): le automazioni dell'avvio si lanciano con
`automation.trigger`, come «Esegui azioni» dell'interfaccia (`trigger.platform` è `None`, non
`homeassistant`). Il Cambio Filtro delle 08:00 e i giorni del Calendario diversi dal giovedì non sono
raggiungibili (gli scenari partono tutti giovedì 15-01-2026 verso le 10:07, ora locale, e la VMC finta non
segnala «Verificare Filtro»).

Risultati (3 processi, `--coda 60`): `identica` contro `identica` 132 / 132 identici (sez. 6);
`identica` contro `nativa` 132 / 132 identici con il motore del ramo di lavoro a 82f8633 e a 43015bb.

## 4. Cosa contiene la traccia

Campo `trz` di ogni risultato (JSON compresso, `tracce.decomprimi`), un'unica lista nell'ordine in cui
le cose accadono; ogni voce è `[tipo, t, ...]` con `t` in secondi virtuali dall'inizio della timeline
(negativo durante la preparazione dello scenario, che è registrata):

| tipo | contenuto |
|---|---|
| `S` | cambio di stato (`state_changed`) di un'entità della VMC: entity_id, stato, impronta degli attributi, forma del contesto |
| `R` | scrittura senza cambio (`state_reported`): entity_id, forma del contesto |
| `C` | chiamata di servizio con effetti esterni: dominio, servizio, dati (JSON con chiavi ordinate), forma del contesto |
| `E` | la stessa chiamata non riuscita (servizio inesistente, dati non validi): classe dell'errore |
| `V` | registro della VMC finta: comando (`cmd`), cambio di velocità (`speed`), corrente (`power`) |
| `X` | comando di shell eseguito (`nc` dei comandi, `ping` del sensore IP) |
| `MS` | (solo con `--mappa`) cambio di stato nel motore: timer o valore interno (oggi una `S` dell'aiutante) |
| `MR` | (solo con `--mappa`) scrittura senza cambio nel motore: timer o valore interno (oggi una `R`) |

- **Entità della VMC**: object_id che inizia con `vmc_master_` (tutti i domini: input_*, timer,
  sensor, binary_sensor, automation, script...) e `automation.automazione_vmc_master`; 476 entità.
- **Attributi**: impronta (blake2b, 64 bit) del JSON di tutti gli attributi con chiavi ordinate; la
  tabella impronta → attributi è nella traccia e il rapporto mostra gli attributi diversi.
  `last_changed`, `last_updated`, `last_reported` e il contesto non sono attributi; nessun attributo
  del package dipende dal tempo reale o dal caso (timer `finishes_at`/`remaining`, `last_triggered` di
  automazioni e script sono sull'orologio virtuale): nessun attributo è escluso
  (`tracce.ATTRIBUTI_ESCLUSI` vuoto) e la prova A contro A' lo conferma.
- **Contesto**: gli id sono casuali, si registra la forma: `u` (utente), `p` (contesto figlio, cioè
  azione di un'automazione o di uno script), `up`, vuoto. Il package legge `context.user_id`.
- **Servizi**: tutti i domini tranne quelli degli aiutanti (`input_*`, `timer`, `counter`, `script`,
  `automation`), i cui effetti sono già nelle voci `S`/`R`: quindi `shell_command.*`,
  `homeassistant.*` (anche `update_entity`, che legge la VMC), `persistent_notification.*`,
  `notify.*`, `tts.*`, `media_player.*`, `recorder.*`, `vmc_master.*` e qualsiasi altro dominio.
- Riga `__avvio__`: traccia dal setup delle integrazioni al fork (avvio, `homeassistant_start`,
  `avvia` della variante, preparazione di base, 300 s di riscaldamento) e lo stato di tutte le entità
  della VMC dopo il setup (voci `I`) e al fork (voci `F`).
- Ascolto: `hass.bus.async_listen` con `event_filter` (nessun tracker per entità: non cambia l'ordine
  dei trigger delle automazioni) e un involucro su `ServiceRegistry.async_call` per le chiamate non
  riuscite. Le funzioni registrano soltanto.

Il confronto (`confronta.py`) guarda la traccia voce per voce nello stesso ordine (istanti uguali entro
1e-6 s, l'unità dell'arrotondamento), `t0` e i campi del runner della b36 (`snaps`, `log`, `seen`,
`events`, `raw`, `ip`). Non confronta `trig` (trigger dell'automazione YAML, che con il motore nativo
non c'è) e `real_s`.

## 5. Leggere il rapporto

In cima: file e varianti, opzioni, scenari identici / diversi / mancanti / con errori, **ESITO**,
tipi di differenza (quanti scenari per tipo di voce: `S`, `R`, `C`, ...; `ordine` = stesse voci in
ordine diverso; `campo log` ecc. = campi del runner; `t0`; `errore`), famiglie. Poi, per ogni scenario
diverso: numero di voci dei due lati, posizione e istante della prima differenza, quante voci di ogni
tipo non hanno corrispondente, 10 voci intorno alla prima differenza per A e per B (`>>` segna la
voce diversa) e, se cambiano solo gli attributi, quali. Esempio (variante `prova_ritardo`):

    === S|CO2|1|F|A0   [C, R, S, V, X, campo log]
      traccia: 4527 voci in A, 4527 in B; prima differenza alla voce 3532 (t=258.0)
      --- A
      >>   258.000000 C shell_command.vmc_master_velocita_0 {}  [contesto p]
           258.000000 X shell: printf 'VMWH0000000\n' | timeout 5 nc -w 3 192.168.1.160 5001
      --- B
      >>   258.010000 C shell_command.vmc_master_velocita_0 {}  [contesto p]

`--ignora-tipi R` e `--ignora-entita '<regex>'` servono solo a capire una differenza (per esempio se
resta togliendo le entità `automation.*`/`script.*`), non ad accettarla.

## 6. Determinismo

Una prova differenziale vale solo se A contro A' (stessa variante, due processi diversi) dà zero
differenze. Correzioni rispetto alla b36 (tutte nel simulatore, nessuna nel package), ognuna con la
prova che senza di essa il confronto non regge:

- **Nessun thread** (`simlib.EsecutoreSincrono`): con i thread della b36 l'istante reale in cui finiva
  un lavoro dell'executor (lettura TCP dei sensori per `update_entity` e per l'aggiornamento periodico,
  caricamento del YAML, import delle integrazioni) decideva in che punto della coda del ciclo entrava
  il risultato. Allo stesso istante virtuale l'ordine degli eventi cambiava da un giro all'altro e a
  volte anche il comportamento (un'automazione leggeva il sensore prima o dopo la lettura). Prova con i
  thread (`SIM_ESECUTORE=thread`, 120 scenari di tutte le famiglie): 121 su 121 diversi (120 solo
  nell'ordine, 1 con cambi di stato diversi). Ora ogni lavoro gira subito nel thread del ciclo e il
  risultato arriva come un callback, nell'ordine in cui i lavori sono chiesti.
  `block_async_io` è spento (i lavori «da executor» girano nel ciclo).
- **Nessuna porta aperta**: nella b36 il server web apriva davvero la porta 8123; se era occupata (un
  altro giro in parallelo, A e B lanciati insieme, un altro Home Assistant) l'avvio prendeva un'altra
  strada e cambiava la storia dei timer di tutti gli scenari. Prova (porta libera contro occupata, 120
  scenari): 121 su 121 diversi. Ora il server non apre niente (sez. 1).
- **Timer** (`vclock.py`). Tre correzioni, perché un motore nativo registra timer diversi da quelli
  delle automazioni YAML e questo non deve spostare nient'altro:
  1. il salto dell'orologio porta il tempo virtuale esattamente all'istante del primo timer
     (`_V = when`) invece di sommare il timeout: con la somma l'arrotondamento dipendeva dagli istanti
     intermedi visitati, e un timer in più spostava di 1e-16 s gli istanti seguenti (i microsecondi di
     `utcnow()` e l'ordine dei timer quasi uguali);
  2. ordine totale dei timer (`TimerOrdinato`: istante e, a parità, ordine di registrazione): asyncio
     confronta solo l'istante e lo heap non è stabile, quindi due timer allo stesso istante virtuale
     (frequente: non c'è il rumore dell'orologio reale) uscivano in un ordine che dipendeva da tutti gli
     altri timer registrati e annullati;
  3. istante di ogni timer portato al microsecondo successivo (mai prima: Home Assistant riarma un
     timer che scatta in anticipo). Con istanti diversi entro lo stesso microsecondo un timer estraneo,
     anche annullato, poteva fermare l'estrazione dei timer scaduti di asyncio e rimandare al giro dopo
     un timer dello stesso istante.

  Prova (`prova_timer` contro `identica`, 60 scenari K e R più l'avvio): con i timer della b36
  (`SIM_TIMER=b36`) 61 su 61 diversi; con le correzioni 1 e 2 ne restava 1 (due voci scambiate
  allo stesso istante); con tutte e tre 0 su 61.
- **Scarti degli orari** (`simlib._scarto_stabile`): Home Assistant sposta ogni ascoltatore di un orario
  (trigger `time_pattern` e `time`, modelli con `now()` rinfrescati al secondo 0) di 50-500 ms presi da
  `random.randint`, nell'ordine in cui gli ascoltatori nascono. Con il seme fisso A contro A' coincide,
  ma il motore nativo crea gli ascoltatori in un altro ordine: gli stessi scarti finivano ad ascoltatori
  diversi (nei primi giri della variante `nativa` il conto alla rovescia del calendario partiva a 59,06 s
  in A e a 59,45 s in B, e lo scarto di A ricompariva in B su un altro ascoltatore). Ora lo scarto dipende
  solo dall'orario richiesto (ora, minuto, secondo); due ascoltatori dello stesso orario scattano allo
  stesso istante, in ordine di registrazione. Prova (`prova_casuale` contro `identica`, 60 scenari):
  con gli scarti di Home Assistant (`SIM_SCARTI=casuali`) 61 su 61 diversi, 24 anche nei comandi alla
  VMC; con gli scarti stabili 0 su 61.
- **PYTHONHASHSEED=0** (`runner.assicura_determinismo`, il processo si rilancia da solo): ordine di
  set di stringhe (entity_id nei modelli, nei tracker).
- **Seme di random** fisso nel padre e in ogni figlio (dall'id dello scenario).

`SIM_ESECUTORE=thread`, `SIM_HTTP=vero`, `SIM_TIMER=b36` e `SIM_SCARTI=casuali` rimettono il
comportamento della b36 e servono solo a rifare queste prove.

Risultati (variante `identica` contro se stessa, 4 processi, codice definitivo):

| prova | scenari | `--coda` | identici / confrontati |
|---|---|---|---|
| tutta la famiglia C (768) e 100 per ognuna delle altre sei famiglie, più `__avvio__` | 1368 | 60 s | **1369 / 1369** |
| famiglia M (`'^M\|'`), più `__avvio__` (3 processi) | 131 | 60 s | **132 / 132** |

Il lato A del giro grande è girato con il calcolatore molto carico (altri processi, carico medio 7-8
su 4 CPU, 0,77 scenari/s), il lato B con poco carico (1,83 scenari/s): tempi reali diversi, tracce
identiche. Prove delle varianti con il codice definitivo: `riscritta` 121 / 121 identici;
`prova_ritardo` 53 diversi su 121, esattamente gli scenari con `shell_command.vmc_master_velocita_0`
nella traccia; `prova_componente` 121 / 121 identici; `prova_timer` 61 / 61 identici;
`prova_casuale` 61 / 61 identici; `prova_audio` sulla famiglia M 30 diversi su 132, esattamente i 30
scenari con `tts.google_translate_say` nella traccia di A. Con le modifiche al simulatore per la famiglia M
(utente, `verifica_ip`, azioni nuove) 42 scenari delle altre famiglie più `__avvio__` danno le stesse
tracce di prima (43 / 43 identici a un giro A fatto senza).

## 7. Tempi

Con 4 processi su un calcolatore di 4 CPU: avvio e riscaldamento 8-10 s (una volta per giro);
1,8-2,3 scenari/s senza coda (120 scenari misti); con `--coda 60` sui 1368 scenari della prova di
determinismo 1,83 scenari/s con il calcolatore libero (12 minuti per lato) e 0,77 scenari/s con altri
lavori pesanti in corso (30 minuti). La traccia pesa circa 100 KB per scenario (130 KB con
`--coda 60`; la riga `__avvio__` circa 110 KB): 1368 scenari sono circa 180 MB per lato. Tutti i
17.264 scenari: circa 2,5 ore per lato senza coda e 2,5-3 ore con `--coda 60` a calcolatore libero.
Giro completo del 26-11-2026 (17.395 scenari, `--coda 60`): lato A (YAML) 2,71 scenari/s nell'ultima
ripresa, lato B (motore in Python) 3,80 scenari/s, 4.578 s. Ogni lato pesa circa 1,8 GB.
Un differenziale fa i due lati uno dopo l'altro.

## 8. Limiti (cose che possono nascondere differenze tra A e B)

- La traccia di uno scenario finisce a `end` (più `--coda`): un comando o un cambio di stato più
  tardo non si confronta. Gli scenari partono tutti dallo stesso stato (il fork dopo il
  riscaldamento): l'avvio si confronta solo nella riga `__avvio__`, dove l'ordine di creazione delle
  entità durante il setup non c'è (solo lo stato dopo il setup, voci `I`).
- Si confrontano solo le entità `vmc_master_*`, le chiamate ai domini non aiutanti e la VMC finta:
  non i log (Home Assistant ha i log spenti: errori dei modelli o delle azioni si vedono solo dai loro
  effetti), non le tracce delle automazioni, non gli eventi diversi da `state_changed`,
  `state_reported` e `call_service`. Una chiamata non riuscita a un servizio degli aiutanti (per
  esempio un valore fuori intervallo) non è registrata: si vede solo da quello che non cambia dopo.
- Del contesto si confronta la forma (utente / figlio), non a quale contesto padre appartiene.
- La VMC finta risponde subito alle letture TCP e ha latenze fisse; con l'executor sincrono il
  risultato di un lavoro arriva sempre al primo giro del ciclo e i timer dello stesso microsecondo
  escono in ordine di registrazione. Il simulatore esplora una sola delle sequenze possibili: A e B
  possono coincidere qui e non con i tempi reali di una VMC vera (e viceversa una differenza di solo
  ordine allo stesso istante può non avere effetti nella realtà, ma va capita comunque).
- Scarti degli orari stabili (sez. 6): in Home Assistant gli ascoltatori dello stesso orario scattano a
  frazioni di secondo casuali e diverse, qui tutti allo stesso istante in ordine di registrazione. Una
  variante che registra nello stesso orario in un altro ordine dà differenze di `ordine` che nella
  realtà possono non contare (vanno capite comunque).
- Coincidenze dell'orologio virtuale: i passi degli scenari cadono su secondi interi e i timer di
  Home Assistant (`timer.start`) troncano l'inizio al secondo, quindi la fine di un timer entità
  coincide spesso con la fine di un'attesa `for:` partita dallo stesso cambio di stato; con un orologio
  vero il timer finirebbe fino a 1 s prima. A parità di istante l'ordine è quello di creazione dei due
  timer (sez. 6): una differenza di `ordine` lì è vera nel simulatore ma nella realtà può non esserci.
- Posizione delle voci `S`/`R`: l'ascolto della traccia viene dopo il distributore degli
  `state_changed` dei tracker di Home Assistant (entità template, trigger delle automazioni). Un'azione
  eseguita dentro il callback del trigger, senza tornare al ciclo, compare prima del cambio di stato
  che l'ha fatta partire: è una differenza vera (gli altri ascoltatori di quel cambio la vedono dopo),
  ma l'istante è lo stesso.
- **Copertura**: gli scenari di `gen.py` non usano tutte le parti del package. Su 1368 scenari (tutta
  la famiglia C e 100 per ognuna delle altre) `copertura.py` dà: automazioni mai eseguite negli
  scenari 7 su 14 (`audio_allerte_e_stato`, `cambio_ip_vmc_riavvio_di_h_a`,
  `esclusivita_finestre_opzioni`, `riepilogo_audio_avvio`, `ripartenza_della_vmc`; e
  `inizializza_tempi_di_attesa` e `riallineamento_allerte_al_riavvio` solo nell'avvio); script mai
  eseguiti 37 su 51 (tutti gli `audio_*`, `notifica_*`, `profilo_*`, `pulisci_cronologia_*`,
  `azzera_aria_scambiata`, `azzera_offset_sensors`, `reset_filtro_vmc`, `upgrade_sensors`;
  `ripristina_tempi_attesa` solo nell'avvio). Le parti mai eseguite non sono provate dal differenziale:
  per questo c'è la famiglia M (sez. 3bis). Con la famiglia M (131 scenari) le automazioni eseguite
  negli scenari sono 14 su 14 e gli script 50 su 51 (manca solo `bottone_panico`, che è della famiglia K);
  sommando i 1368 scenari sopra, 14 su 14 e 51 su 51. Trigger (id) dell'Automazione VMC Master scattati
  negli scenari (`copertura.py --trigger`): 106 su 217 nei 1368, 94 nella famiglia M, 163 su 217 insieme.
  I 54 mai scattati: 24 dei giorni del Calendario diversi dal giovedì e i 2 del Cambio Filtro delle 08:00
  (non raggiungibili: data e ora virtuali fisse), 1 dell'avvio di Home Assistant (scatta solo nella riga
  `__avvio__`), 27 combinazioni di allerte (PdR / Free / Inquinanti / Calendario spento tra le Fasce /
  Black-Out a Velocità 1 / Comando non eseguito / pannello avvisi / Umidità finita con Inquinanti), che
  sono degli scenari di `gen.py` e potrebbero scattare negli scenari fuori dal campione di 1368.
- Le dipendenze di un componente personalizzato da `frontend`, `http`, `lovelace` e simili sono
  ignorate e il server web non è in ascolto (sez. 1): una variante che registra pannelli, viste o API
  web non le vede funzionare qui.
- Con la variante nativa le entità `automation.*` e `script.*` del package spariscono (o diventano
  altro): le loro voci `S`/`R` (stato `on`/`off` degli script, attributi `current` e `last_triggered`)
  risultano differenze finché il motore non le riproduce o si decide di non confrontarle
  (`--ignora-entita '^(automation|script)\.'` per vedere il resto). Con `nativa4` le automazioni restano
  entità `automation` e le voci degli script le toglie la mappa (`--mappa`, contate nel rapporto).
- I servizi finti (tts, media_player, notify.notify, recorder, homeassistant.restart,
  vmc_master.verifica_ip) non fanno niente: si confrontano le chiamate, non i loro effetti.
