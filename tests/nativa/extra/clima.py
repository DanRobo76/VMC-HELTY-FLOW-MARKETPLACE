"""Valori in piu' per i modelli di temperatura, umidita', punto di rugiada e umidita' assoluta.

- ``sensori memorizzata``: temperature negative (parte che comincia con 1), umidita' della
  sonda oltre 100 % e a zero, letture troncate (senza la parte della temperatura esterna o
  dell'umidita', un solo carattere con segno negativo), parti non numeriche (con una cifra
  che ``isdigit`` accetta ma ``int`` no: il modello va in errore), stato vuoto (non
  disponibile per tutti tranne il Punto di Rugiada Interno).
- ``sensor.esterno_due`` (sensore scelto dall'utente): numeri scritti in altri modi
  (``21.30``, ``007``, ``1e3``, ``-0``, ``+5``) che Home Assistant riscrive, -100, umidita'
  oltre 100 e quasi zero, temperature dove le formule danno zero, dividono per zero o vanno
  fuori scala (-237.6, -237.7, -237.8, -243.5), valori non numerici.
- scelte delle entita': le sonde della VMC senza Offset per le temperature, che gli script
  di «Aggiorna Elenco Entita'» aggiungono sempre all'elenco.

Home Assistant non cambia lo stato di un sensore modello se il nuovo risultato e' uguale
(==) al precedente (100.0 e 100, -0.0 e 0.0, -100.0 e -100): i modelli in Python lo seguono
ricordando l'ultimo risultato di ogni giro. Dentro un giro pero' Home Assistant rifa' un
modello a ogni ingresso cambiato, e un risultato intermedio puo' restare scritto: qui
mancano quindi i valori che lo rendono frequente (sonda a «-0.0» o a 100 % esatto, -100.0,
la sonda dell'umidita' interna scelta come sensore: Umidita' Int. dipende dalla sonda sia
direttamente sia attraverso Umidita' Int. Selezionata, e Home Assistant la rifa' prima con
la scelta vecchia, cosi' un 100.0 intermedio resta scritto al posto del 100 finale).
"""

from __future__ import annotations

_VUOTE = ",00000" * 11

EXTRA = {
    "sensor.vmc_master_sensori_memorizzata": [
        "VMGI,10055,10100,01005" + _VUOTE,
        "VMGI,00210,00100,00000" + _VUOTE,
        "VMGI,1²,0x10,abc",
        "VMGI,1,1",
        "VMGI,00210",
        "",
    ],
    "sensor.esterno_due": [
        "21.30",
        "007",
        "1e3",
        "-0",
        "+5",
        "-100",
        "100.5",
        "0.04",
        "-237.6",
        "-237.7",
        "-237.8",
        "-243.5",
        "inf",
        "abc",
    ],
    "input_select.vmc_master_selected_temp_external_entity": ["sensor.vmc_master_temp_esterna_status_senza_offset"],
    "input_select.vmc_master_selected_temp_internal_entity": ["sensor.vmc_master_temp_interna_status_senza_offset"],
}
