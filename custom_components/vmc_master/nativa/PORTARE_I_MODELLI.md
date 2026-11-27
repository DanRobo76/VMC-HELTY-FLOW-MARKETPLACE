# Portare i modelli del package in Python

Regole per i sensori calcolati (fase 2 della riscrittura nativa). Valgono per ogni modulo
di `nativa/modelli/`.

## Cosa si porta

Ogni sensore modello del package (`template:` in `package/vmc_master.yaml`) diventa una
funzione registrata con `@modello("dominio.oggetto")`. La chiave è l'entity_id del package
senza `vmc_master_`: `sensor.vmc_master_co2_status` → `"sensor.co2_status"`.

- `stato`: la funzione stessa. Restituisce lo **stato finale** come lo mostra Home
  Assistant: testo già senza spazi all'inizio e alla fine; `on`/`off` per i sensori binari.
- `icona=`: funzione per un'icona scritta con un modello (un'icona fissa non si porta).
- `disponibile=`: funzione per `availability` (False → stato `unavailable`).
- `ritardo_on=`: funzione per `delay_on` (secondi); la funzione `stato` restituisce allora
  la condizione prima del ritardo.

## Come si legge

- `L.v("input_boolean.spia_velocita_1")` = `states('input_boolean.vmc_master_spia_velocita_1')`.
- `L.is_v(chiave, valore_o_lista)` = `is_state(...)`.
- `L.s(entity_id)` = `states(x)` con un entity_id completo (sensore scelto dall'utente);
  accetta anche valori non testo (danno `unknown`).
- `L.attr_v(chiave, nome)` / `L.attr(entity_id, nome)` = `state_attr(...)`.
- `L.now()` = `now()` (fuso orario di Home Assistant).
- Gli altri sensori modello si leggono con `L.v` come gli ingressi: il calcolo li fa al
  bisogno, nell'ordine giusto.

## Uguali al package, anche nei casi limite

- `| float(d)` → `fl(x, d)`; `| int(d)` → `it(x, d)`; `| round(n)` → `rnd(x, n)`;
  `is_number(x)` → `is_number(x)`; `{{ x }}` di un numero → `testo(x)` (`str`).
- Attenzione a `float` stampati (`21.0`, non `21`), a `round(0)` che dà un intero, ai
  confronti tra testo e numero, a `in [...]`, a `| trim`, `| lower`, `| capitalize`.
- Si porta la logica, non il testo: niente copie per giorno o per Fascia, ma funzioni
  comuni con parametri, purché il risultato sia identico in ogni caso.
- Commenti e docstring in italiano, come il resto dell'integrazione.

## Come si controlla

`tests/nativa/test_modelli_confronto.py` fa girare i modelli del package nel vero Home
Assistant e confronta, giro per giro, stato, icona, disponibilità (e condizione e ritardo
per `delay_on`) di ogni modello portato:

    cd <repository> && /home/user/hat/bin/python -m pytest -q tests/nativa/test_modelli_confronto.py -p no:cacheprovider -W ignore

`VMC_GIRI` (predefinito 400) e `VMC_SEME` cambiano numero di giri e semi. Un modello è
portato quando passa con almeno 3 semi diversi a 2000 giri e dà più di un risultato.
Valori in più per gli ingressi, ingressi che il banco non trova e modelli con un solo
risultato possibile vanno in `tests/nativa/extra/<gruppo>.py` (vedi `extra/__init__.py`).
