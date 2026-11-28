# Portare il motore logico in Python (fase 3)

Il motore logico della b41 sono 14 automazioni (l'Automazione VMC Master e 13 altre) e 51
script del package, dopo aver tolto le sezioni Clona e Installa VMC
(`trasforma.rimuovi_sezioni_solo_master`). In tutto 3.257 modelli Jinja, 1.984 condizioni
modello, 433 trigger modello, 1.213 pause, 619 cicli «ripeti fino a».

## Come si porta

Il codice Python del motore **si genera una volta** dal package con un traduttore
(`tests/nativa/motore/traduci.py`) e poi resta il codice dell'integrazione. Il traduttore
riproduce 1:1 la semantica di Home Assistant:

- ogni modello Jinja diventa un'espressione Python che usa le funzioni di `jinja.py`
  (filtri, test, valore indefinito, conversione in testo) e del contesto (`states`,
  `is_state`, `state_attr`, `now`), con le stesse letture nello stesso ordine;
- ogni azione (`if`, `choose`, `repeat`, `delay`, `wait_template`, `variables`, `stop`,
  `condition`, chiamate di servizio) diventa codice Python con le regole di
  `homeassistant/helpers/script.py` (per esempio: una condizione fallita in una sequenza
  annidata ferma solo quella sequenza);
- ogni trigger diventa una dichiarazione Python con le regole dei trigger di Home
  Assistant (`state` con `from`/`to`/`for`, `template` armato solo dopo un risultato falso,
  `time`, `time_pattern`, `event`, `homeassistant`);
- ogni automazione e script ha la stessa modalità (`queued` con lo stesso massimo,
  `restart`, `single`, `parallel`).

I nomi «master/Master/MASTER» nelle stringhe si adattano a ogni VMC come fa
`trasforma.rinomina`.

## Moduli

- `jinja.py`: semantica di Jinja e dei filtri di Home Assistant usati dal package.
- `esecuzione.py`: variabili con gli stessi ambiti di Home Assistant, modalità delle
  esecuzioni, pause, attese.
- `trigger.py`: i trigger.
- `ha.py`: il motore che lavora sulle entità di oggi (aiutanti e sensori del package),
  per il confronto con il simulatore; nella fase 4 si aggiunge quello sulle entità native.
- `tests/nativa/motore/generato/`: il codice generato della fase 3 (non si modifica a
  mano finché il traduttore è in uso). Lo usano solo le prove e gli strumenti: è fuori
  dall'integrazione e non si installa.
- `generato_fase4/`: il codice della fase 4, sulle entità native. Dalla b46 ha 13
  automazioni: il traduttore toglie «Cambio IP VMC (Riavvio di H.A.)»
  (`tests/nativa/motore/traduci_fase4.py`, `escluse`).

## Come si controlla

1. `tests/nativa/motore/test_jinja.py`: ogni funzione di `jinja.py` contro il vero motore
   dei modelli di Home Assistant, su molti valori.
2. `tests/nativa/motore/test_modelli_motore.py`: ogni modello tradotto contro lo stesso
   modello reso da Home Assistant, con stati e variabili casuali o realistici (letti dal
   package: `valori_package.py`) e un giro mirato su ogni valore di ogni confronto: stesso
   testo, stesso risultato interpretato (tipo e valore), stessa `RenderInfo` (quello che
   ascoltano trigger e attese) e stesso esito come condizione `template`, errori compresi.
3. `strumenti/simulatore/`: ogni scenario del simulatore gira con l'automazione di oggi e
   con il motore in Python; comandi alla VMC, cambi di stato e notifiche devono essere
   identici, allo stesso istante. Si accetta zero differenze.

## Esito

26-11-2026: giro completo del simulatore, tutte le famiglie (17.395 scenari più l'avvio):
**17.396 / 17.396 identici**, zero differenze (dettagli in `strumenti/simulatore/LEGGIMI.md`).
