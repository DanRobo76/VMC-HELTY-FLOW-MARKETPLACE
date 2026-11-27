# VMC Master: nomi cambiati / Changed names

<!-- File generato da tests/nativa/genera_elenco_nomi.py: non modificarlo a mano. -->

🇮🇹 Nomi che cambiano nella versione nativa, uguali per ogni VMC. ‹nome› è il nome della VMC (per la prima VMC: `master`). Cambia solo la parte prima del punto.

🇺🇸 Names that change in the native version, the same for every unit. ‹nome› is the unit's name (for the first unit: `master`). Only the part before the dot changes.

| Gruppo / Group | Voci / Items |
|---|---|
| Impostazioni che cambiano dominio / Settings that change domain | 173 |
| Timer che diventano sensori con l'ora di fine / Timers that become end-time sensors | 34 |
| Script e comandi che diventano pulsanti / Scripts and commands that become buttons | 25 |
| Voci che diventano interne all'integrazione (non più entità) / Items that become internal to the integration (no longer entities) | 110 |

## 1. Impostazioni che cambiano dominio / Settings that change domain (173)

### `input_boolean` → `binary_sensor` (77)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_boolean.vmc_‹nome›_attese_inizializzate` | `binary_sensor.vmc_‹nome›_attese_inizializzate` | Tempi di Attesa Inizializzati |
| `input_boolean.vmc_‹nome›_avvio_home_assistant_in_corso_per_audio` | `binary_sensor.vmc_‹nome›_avvio_home_assistant_in_corso_per_audio` | Spia Audio all'Avvio di Home Assistant |
| `input_boolean.vmc_‹nome›_congelamento_verifica_soglia_valore_spia` | `binary_sensor.vmc_‹nome›_congelamento_verifica_soglia_valore_spia` | Spia VMC Congelamento ≤ -18 [°C] Temp. Esterna ? |
| `input_boolean.vmc_‹nome›_delta_temp_verifica_soglia_valore_spia` | `binary_sensor.vmc_‹nome›_delta_temp_verifica_soglia_valore_spia` | Spia VMC Sensori Int. Δ Temp. > 23 [°C] ? |
| `input_boolean.vmc_‹nome›_opzione_finestra_tempi_attesa` | `binary_sensor.vmc_‹nome›_opzione_finestra_tempi_attesa` | Finestra Tempi di Attesa |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_avvisi_spia` | `binary_sensor.vmc_‹nome›_opzioni_accendi_spegni_avvisi_spia` | Spia Avvisi |
| `input_boolean.vmc_‹nome›_popup_versione_corrente_vs_repository` | `binary_sensor.vmc_‹nome›_popup_versione_corrente_vs_repository` | PopUp Notifica Aggiornamento |
| `input_boolean.vmc_‹nome›_spia_calendario_black_out` | `binary_sensor.vmc_‹nome›_spia_calendario_black_out` | Spia Black-Out all'interno del Calendario |
| `input_boolean.vmc_‹nome›_spia_calendario_comando_non_eseguito` | `binary_sensor.vmc_‹nome›_spia_calendario_comando_non_eseguito` | Spia Comando non eseguito all'interno del Calendario |
| `input_boolean.vmc_‹nome›_spia_calendario_domenica_1` | `binary_sensor.vmc_‹nome›_spia_calendario_domenica_1` | Spia all'interno del Calendario Domenica 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_domenica_2` | `binary_sensor.vmc_‹nome›_spia_calendario_domenica_2` | Spia all'interno del Calendario Domenica 2° |
| `input_boolean.vmc_‹nome›_spia_calendario_giovedi_1` | `binary_sensor.vmc_‹nome›_spia_calendario_giovedi_1` | Spia all'interno del Calendario Giovedì 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_giovedi_2` | `binary_sensor.vmc_‹nome›_spia_calendario_giovedi_2` | Spia all'interno del Calendario Giovedì 2° |
| `input_boolean.vmc_‹nome›_spia_calendario_lunedi_1` | `binary_sensor.vmc_‹nome›_spia_calendario_lunedi_1` | Spia all'interno del Calendario Lunedì 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_lunedi_2` | `binary_sensor.vmc_‹nome›_spia_calendario_lunedi_2` | Spia all'interno del Calendario Lunedì 2° |
| `input_boolean.vmc_‹nome›_spia_calendario_martedi_1` | `binary_sensor.vmc_‹nome›_spia_calendario_martedi_1` | Spia all'interno del Calendario Martedì 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_martedi_2` | `binary_sensor.vmc_‹nome›_spia_calendario_martedi_2` | Spia all'interno del Calendario Martedì 2° |
| `input_boolean.vmc_‹nome›_spia_calendario_mercoledi_1` | `binary_sensor.vmc_‹nome›_spia_calendario_mercoledi_1` | Spia all'interno del Calendario Mercoledì 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_mercoledi_2` | `binary_sensor.vmc_‹nome›_spia_calendario_mercoledi_2` | Spia all'interno del Calendario Mercoledì 2° |
| `input_boolean.vmc_‹nome›_spia_calendario_sabato_1` | `binary_sensor.vmc_‹nome›_spia_calendario_sabato_1` | Spia all'interno del Calendario Sabato 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_sabato_2` | `binary_sensor.vmc_‹nome›_spia_calendario_sabato_2` | Spia all'interno del Calendario Sabato 2° |
| `input_boolean.vmc_‹nome›_spia_calendario_venerdi_1` | `binary_sensor.vmc_‹nome›_spia_calendario_venerdi_1` | Spia all'interno del Calendario Venerdì 1° |
| `input_boolean.vmc_‹nome›_spia_calendario_venerdi_2` | `binary_sensor.vmc_‹nome›_spia_calendario_venerdi_2` | Spia all'interno del Calendario Venerdì 2° |
| `input_boolean.vmc_‹nome›_spia_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_co2_o_voc` | Spia Inquinanti CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_co2_o_voc_partenza_ritorno_velocita_0` | `binary_sensor.vmc_‹nome›_spia_co2_o_voc_partenza_ritorno_velocita_0` | Spia di Richiamo Vel. 0 CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_0` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_0` | Spia Umidità Velocità 0 |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_1` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_1` | Spia Umidità Velocità 1 |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_2` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_2` | Spia Umidità Velocità 2 |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_3` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_3` | Spia Umidità Velocità 3 |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_4` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_4` | Spia Umidità Velocità 4 |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_freecooling` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_freecooling` | Spia Umidità Velocità Free Cool./Heat. |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_iperventilazione` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_iperventilazione` | Spia Umidità Velocità Iperventilazione |
| `input_boolean.vmc_‹nome›_spia_umidita_velocita_notturna` | `binary_sensor.vmc_‹nome›_spia_umidita_velocita_notturna` | Spia Umidità Velocità Notturna |
| `input_boolean.vmc_‹nome›_spia_velocita_0` | `binary_sensor.vmc_‹nome›_spia_velocita_0` | Spia Velocità 0 |
| `input_boolean.vmc_‹nome›_spia_velocita_0_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_0_co2_o_voc` | Spia Velocità 0 CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_0_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_0_congelamento` | Spia Velocità 0 Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_0_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_0_delta_temp_verifica_soglia_valore` | Spia Velocità 0 Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_0_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_0_un_solo_avvio` | Spia Velocità 0 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_1` | `binary_sensor.vmc_‹nome›_spia_velocita_1` | Spia Velocità 1 |
| `input_boolean.vmc_‹nome›_spia_velocita_1_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_1_co2_o_voc` | Spia Velocità 1 CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_1_co2_o_voc_pdr` | `binary_sensor.vmc_‹nome›_spia_velocita_1_co2_o_voc_pdr` | Spia Velocità 1 CO₂ e/o VOC Vs PdR |
| `input_boolean.vmc_‹nome›_spia_velocita_1_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_1_congelamento` | Spia Velocità 1 Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_1_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_1_delta_temp_verifica_soglia_valore` | Spia Velocità 1 Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_1_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_1_un_solo_avvio` | Spia Velocità 1 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_2` | `binary_sensor.vmc_‹nome›_spia_velocita_2` | Spia Velocità 2 |
| `input_boolean.vmc_‹nome›_spia_velocita_2_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_2_co2_o_voc` | Spia Velocità 2 CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_2_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_2_congelamento` | Spia Velocità 2 Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_2_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_2_delta_temp_verifica_soglia_valore` | Spia Velocità 2 Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_2_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_2_un_solo_avvio` | Spia Velocità 2 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_3` | `binary_sensor.vmc_‹nome›_spia_velocita_3` | Spia Velocità 3 |
| `input_boolean.vmc_‹nome›_spia_velocita_3_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_3_co2_o_voc` | Spia Velocità 3 CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_3_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_3_congelamento` | Spia Velocità 3 Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_3_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_3_delta_temp_verifica_soglia_valore` | Spia Velocità 3 Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_3_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_3_un_solo_avvio` | Spia Velocità 3 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_4` | `binary_sensor.vmc_‹nome›_spia_velocita_4` | Spia Velocità 4 |
| `input_boolean.vmc_‹nome›_spia_velocita_4_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_4_co2_o_voc` | Spia Velocità 4 CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_4_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_4_congelamento` | Spia Velocità 4 Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_4_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_4_delta_temp_verifica_soglia_valore` | Spia Velocità 4 Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_4_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_4_un_solo_avvio` | Spia Velocità 4 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling` | Spia Velocità Free Cool./Heat. |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling_co2_o_voc` | Spia Velocità Free Cool./Heat. CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling_congelamento` | Spia Velocità Free Cool./Heat. Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling_delta_temp_verifica_soglia_valore` | Spia Velocità Free Cool./Heat. Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling_un_solo_avvio` | Spia Velocità freecooling 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling` | Spia su Programmazione Velocità Free Cooling 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating` | `binary_sensor.vmc_‹nome›_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating` | Spia su Programmazione Velocità Free Heating 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_iperventilazione` | `binary_sensor.vmc_‹nome›_spia_velocita_iperventilazione` | Spia Velocità Iperventilazione |
| `input_boolean.vmc_‹nome›_spia_velocita_iperventilazione_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_iperventilazione_co2_o_voc` | Spia Velocità Iperventilazione CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_iperventilazione_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_iperventilazione_congelamento` | Spia Velocità Iperventilazione Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_iperventilazione_delta_temp_verifica_soglia_valore` | Spia Velocità Iperventilazione Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_iperventilazione_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_iperventilazione_un_solo_avvio` | Spia Velocità Iperventilazione 1° Avvio |
| `input_boolean.vmc_‹nome›_spia_velocita_notturna` | `binary_sensor.vmc_‹nome›_spia_velocita_notturna` | Spia Velocità Notturna |
| `input_boolean.vmc_‹nome›_spia_velocita_notturna_co2_o_voc` | `binary_sensor.vmc_‹nome›_spia_velocita_notturna_co2_o_voc` | Spia Velocità Notturna CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_spia_velocita_notturna_congelamento` | `binary_sensor.vmc_‹nome›_spia_velocita_notturna_congelamento` | Spia Velocità Notturna Congelamento |
| `input_boolean.vmc_‹nome›_spia_velocita_notturna_delta_temp_verifica_soglia_valore` | `binary_sensor.vmc_‹nome›_spia_velocita_notturna_delta_temp_verifica_soglia_valore` | Spia Velocità Notturna Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_spia_velocita_notturna_un_solo_avvio` | `binary_sensor.vmc_‹nome›_spia_velocita_notturna_un_solo_avvio` | Spia Velocità notturna 1° Avvio |
| `input_boolean.vmc_‹nome›_umidita_verifica_soglia_valore_spia` | `binary_sensor.vmc_‹nome›_umidita_verifica_soglia_valore_spia` | Spia VMC Umidità |

### `input_boolean` → `switch` (37)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_boolean.vmc_‹nome›_conferma_pulizia_cronologia` | `switch.vmc_‹nome›_conferma_pulizia_cronologia` | Conferma Pulizia Cronologia Entità |
| `input_boolean.vmc_‹nome›_notifica_allerta_black_out` | `switch.vmc_‹nome›_notifica_allerta_black_out` | Notifica ON/OFF Allerta Black-Out |
| `input_boolean.vmc_‹nome›_notifica_allerta_congelamento` | `switch.vmc_‹nome›_notifica_allerta_congelamento` | Notifica ON/OFF Allerta Congelamento |
| `input_boolean.vmc_‹nome›_notifica_allerta_differenza_temp_int_est` | `switch.vmc_‹nome›_notifica_allerta_differenza_temp_int_est` | Notifica ON/OFF Allerta Diff. Temp. Int-Est > 23 [°C] |
| `input_boolean.vmc_‹nome›_notifica_allerta_freecooling_heating` | `switch.vmc_‹nome›_notifica_allerta_freecooling_heating` | Notifica ON/OFF Allerta Free Cool./Heat. |
| `input_boolean.vmc_‹nome›_notifica_allerta_inquinanti` | `switch.vmc_‹nome›_notifica_allerta_inquinanti` | Notifica ON/OFF Allerta Inquinanti |
| `input_boolean.vmc_‹nome›_notifica_allerta_pdr` | `switch.vmc_‹nome›_notifica_allerta_pdr` | Notifica ON/OFF Allerta Lim. Δ P. di Rugiada |
| `input_boolean.vmc_‹nome›_notifica_allerta_riepilogo` | `switch.vmc_‹nome›_notifica_allerta_riepilogo` | Notifica ON/OFF Riepilogo Allerte |
| `input_boolean.vmc_‹nome›_notifica_allerta_status_velocita` | `switch.vmc_‹nome›_notifica_allerta_status_velocita` | Notifica ON/OFF Status Velocità |
| `input_boolean.vmc_‹nome›_notifica_allerta_umidita` | `switch.vmc_‹nome›_notifica_allerta_umidita` | Notifica ON/OFF Allerta Umidità |
| `input_boolean.vmc_‹nome›_notifica_audio` | `switch.vmc_‹nome›_notifica_audio` | Invio Notifica Audio |
| `input_boolean.vmc_‹nome›_notifica_status_vmc` | `switch.vmc_‹nome›_notifica_status_vmc` | Invio Notifica |
| `input_boolean.vmc_‹nome›_opzione_finestra_audio` | `switch.vmc_‹nome›_opzione_finestra_audio` | Finestra Audio |
| `input_boolean.vmc_‹nome›_opzione_finestra_prossime_letture` | `switch.vmc_‹nome›_opzione_finestra_prossime_letture` | Timer Lettura Dati VMC |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_avvisi` | `switch.vmc_‹nome›_opzioni_accendi_spegni_avvisi` | Mostra o Nascondi gli Avvisi |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_calendario` | `switch.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_calendario` | VMC ON/OFF, in Funzione del Calendario |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_co2_e_voc` | `switch.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_co2_e_voc` | VMC ON/OFF, in Funzione del Lim. CO₂ e/o VOC |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_freecooling` | `switch.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_freecooling` | VMC ON/OFF, in Funzione della Vel. Free Cooling |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_freeheating` | `switch.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_freeheating` | VMC ON/OFF, in Funzione della Vel. Free Heating |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_pdr` | `switch.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_pdr` | VMC ON/OFF, in Funzione del Lim. Δ P. di Rugiada |
| `input_boolean.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_umidita` | `switch.vmc_‹nome›_opzioni_accendi_spegni_vmc_vs_umidita` | VMC ON/OFF, in Funzione dell'Umidità Interna |
| `input_boolean.vmc_‹nome›_opzioni_avvisi` | `switch.vmc_‹nome›_opzioni_avvisi` | Avvisi |
| `input_boolean.vmc_‹nome›_opzioni_avvisi_grafici` | `switch.vmc_‹nome›_opzioni_avvisi_grafici` | Grafici |
| `input_boolean.vmc_‹nome›_opzioni_calendario` | `switch.vmc_‹nome›_opzioni_calendario` | Programmazione Calendario |
| `input_boolean.vmc_‹nome›_opzioni_calendario_main` | `switch.vmc_‹nome›_opzioni_calendario_main` | Calendario |
| `input_boolean.vmc_‹nome›_opzioni_elementi_chimici` | `switch.vmc_‹nome›_opzioni_elementi_chimici` | Elementi Chimici |
| `input_boolean.vmc_‹nome›_opzioni_free_heating_o_free_cooling` | `switch.vmc_‹nome›_opzioni_free_heating_o_free_cooling` | Calendario Free Heating / Free Cooling |
| `input_boolean.vmc_‹nome›_opzioni_interruttore_calendario` | `switch.vmc_‹nome›_opzioni_interruttore_calendario` | Status Programmazione Giornaliera |
| `input_boolean.vmc_‹nome›_opzioni_interruttore_monitoraggio_sensori_extra` | `switch.vmc_‹nome›_opzioni_interruttore_monitoraggio_sensori_extra` | Sensori - Extra |
| `input_boolean.vmc_‹nome›_opzioni_interruttore_offset_sensori` | `switch.vmc_‹nome›_opzioni_interruttore_offset_sensori` | Sensori Selezionati - Offset |
| `input_boolean.vmc_‹nome›_opzioni_interruttore_sensori_vmc_interni` | `switch.vmc_‹nome›_opzioni_interruttore_sensori_vmc_interni` | Sensori - VMC Interni |
| `input_boolean.vmc_‹nome›_opzioni_lettura_sensori` | `switch.vmc_‹nome›_opzioni_lettura_sensori` | Informazioni |
| `input_boolean.vmc_‹nome›_opzioni_monitoraggio_sensori` | `switch.vmc_‹nome›_opzioni_monitoraggio_sensori` | Sensori |
| `input_boolean.vmc_‹nome›_opzioni_offset_sensori` | `switch.vmc_‹nome›_opzioni_offset_sensori` | Opzioni |
| `input_boolean.vmc_‹nome›_opzioni_punto_di_rugiada` | `switch.vmc_‹nome›_opzioni_punto_di_rugiada` | Lim. Δ P. di Rugiada |
| `input_boolean.vmc_‹nome›_opzioni_scelta_sensori` | `switch.vmc_‹nome›_opzioni_scelta_sensori` | Sensori Opzionati |
| `input_boolean.vmc_‹nome›_opzioni_vmc` | `switch.vmc_‹nome›_opzioni_vmc` | Telecomando |

### `input_datetime` → `time` (30)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_datetime.vmc_‹nome›_accensione_domenica` | `time.vmc_‹nome›_accensione_domenica` | Dom. 1° |
| `input_datetime.vmc_‹nome›_accensione_domenica_2` | `time.vmc_‹nome›_accensione_domenica_2` | Dom. 2° |
| `input_datetime.vmc_‹nome›_accensione_giovedi` | `time.vmc_‹nome›_accensione_giovedi` | Gio. 1° |
| `input_datetime.vmc_‹nome›_accensione_giovedi_2` | `time.vmc_‹nome›_accensione_giovedi_2` | Gio. 2° |
| `input_datetime.vmc_‹nome›_accensione_lunedi` | `time.vmc_‹nome›_accensione_lunedi` | Lun. 1° |
| `input_datetime.vmc_‹nome›_accensione_lunedi_2` | `time.vmc_‹nome›_accensione_lunedi_2` | Lun. 2° |
| `input_datetime.vmc_‹nome›_accensione_martedi` | `time.vmc_‹nome›_accensione_martedi` | Mar. 1° |
| `input_datetime.vmc_‹nome›_accensione_martedi_2` | `time.vmc_‹nome›_accensione_martedi_2` | Mar. 2° |
| `input_datetime.vmc_‹nome›_accensione_mercoledi` | `time.vmc_‹nome›_accensione_mercoledi` | Mer. 1° |
| `input_datetime.vmc_‹nome›_accensione_mercoledi_2` | `time.vmc_‹nome›_accensione_mercoledi_2` | Mer. 2° |
| `input_datetime.vmc_‹nome›_accensione_sabato` | `time.vmc_‹nome›_accensione_sabato` | Sab. 1° |
| `input_datetime.vmc_‹nome›_accensione_sabato_2` | `time.vmc_‹nome›_accensione_sabato_2` | Sab. 2° |
| `input_datetime.vmc_‹nome›_accensione_venerdi` | `time.vmc_‹nome›_accensione_venerdi` | Ven. 1° |
| `input_datetime.vmc_‹nome›_accensione_venerdi_2` | `time.vmc_‹nome›_accensione_venerdi_2` | Ven. 2° |
| `input_datetime.vmc_‹nome›_audio_end_time` | `time.vmc_‹nome›_audio_end_time` | Notifica Audio - Ora Fine |
| `input_datetime.vmc_‹nome›_audio_start_time` | `time.vmc_‹nome›_audio_start_time` | Notifica Audio - Ora Inizio |
| `input_datetime.vmc_‹nome›_spegnimento_domenica` | `time.vmc_‹nome›_spegnimento_domenica` | Dom. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_domenica_2` | `time.vmc_‹nome›_spegnimento_domenica_2` | Dom. 2° |
| `input_datetime.vmc_‹nome›_spegnimento_giovedi` | `time.vmc_‹nome›_spegnimento_giovedi` | Gio. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_giovedi_2` | `time.vmc_‹nome›_spegnimento_giovedi_2` | Gio. 2° |
| `input_datetime.vmc_‹nome›_spegnimento_lunedi` | `time.vmc_‹nome›_spegnimento_lunedi` | Lun. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_lunedi_2` | `time.vmc_‹nome›_spegnimento_lunedi_2` | Lun. 2° |
| `input_datetime.vmc_‹nome›_spegnimento_martedi` | `time.vmc_‹nome›_spegnimento_martedi` | Mar. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_martedi_2` | `time.vmc_‹nome›_spegnimento_martedi_2` | Mar. 2° |
| `input_datetime.vmc_‹nome›_spegnimento_mercoledi` | `time.vmc_‹nome›_spegnimento_mercoledi` | Mer. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_mercoledi_2` | `time.vmc_‹nome›_spegnimento_mercoledi_2` | Mer. 2° |
| `input_datetime.vmc_‹nome›_spegnimento_sabato` | `time.vmc_‹nome›_spegnimento_sabato` | Sab. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_sabato_2` | `time.vmc_‹nome›_spegnimento_sabato_2` | Sab. 2° |
| `input_datetime.vmc_‹nome›_spegnimento_venerdi` | `time.vmc_‹nome›_spegnimento_venerdi` | Ven. 1° |
| `input_datetime.vmc_‹nome›_spegnimento_venerdi_2` | `time.vmc_‹nome›_spegnimento_venerdi_2` | Ven. 2° |

### `input_number` → `number` (10)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_number.vmc_‹nome›_audio_volume` | `number.vmc_‹nome›_audio_volume` | Volume Media Player |
| `input_number.vmc_‹nome›_offset_co2` | `number.vmc_‹nome›_offset_co2` | Offset CO₂ Int. |
| `input_number.vmc_‹nome›_offset_temp_esterna` | `number.vmc_‹nome›_offset_temp_esterna` | Offset Temperatura Ext. |
| `input_number.vmc_‹nome›_offset_temp_interna` | `number.vmc_‹nome›_offset_temp_interna` | Offset Temperatura |
| `input_number.vmc_‹nome›_offset_umidita_esterna` | `number.vmc_‹nome›_offset_umidita_esterna` | Offset Umidità Ext. |
| `input_number.vmc_‹nome›_offset_umidita_interna` | `number.vmc_‹nome›_offset_umidita_interna` | Offset Umidità Int. |
| `input_number.vmc_‹nome›_offset_verifica_impiego_vmc` | `number.vmc_‹nome›_offset_verifica_impiego_vmc` | Set Lim. Δ Punto di Rugiada |
| `input_number.vmc_‹nome›_offset_voc` | `number.vmc_‹nome›_offset_voc` | Offset VOC Int. |
| `input_number.vmc_‹nome›_umidita_avvio` | `number.vmc_‹nome›_umidita_avvio` | Avvio VMC per Umidità ≥ |
| `input_number.vmc_‹nome›_volume_da_inserire` | `number.vmc_‹nome›_volume_da_inserire` | Volume ambiente Int. |

### `input_number` → `sensor` (1)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_number.vmc_‹nome›_fase_riallineamento_al_riavvio` | `sensor.vmc_‹nome›_fase_riallineamento_al_riavvio` | Fase Riallineamento Allerte al Riavvio |

### `input_select` → `select` (14)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_select.vmc_‹nome›_mese_1_fascia_freecooling` | `select.vmc_‹nome›_mese_1_fascia_freecooling` | Set Inizio Mese Free Cooling |
| `input_select.vmc_‹nome›_mese_1_fascia_freeheating` | `select.vmc_‹nome›_mese_1_fascia_freeheating` | Set Inizio Mese Free Heating |
| `input_select.vmc_‹nome›_mese_2_fascia_freecooling` | `select.vmc_‹nome›_mese_2_fascia_freecooling` | Set Fine Mese Free Cooling |
| `input_select.vmc_‹nome›_mese_2_fascia_freeheating` | `select.vmc_‹nome›_mese_2_fascia_freeheating` | Set Fine Mese Free Heating |
| `input_select.vmc_‹nome›_selected_co2_internal_entity` | `select.vmc_‹nome›_selected_co2_internal_entity` | Seleziona Entità CO₂ Interna |
| `input_select.vmc_‹nome›_selected_humidity_external_entity` | `select.vmc_‹nome›_selected_humidity_external_entity` | Seleziona Entità Umidità Esterna |
| `input_select.vmc_‹nome›_selected_humidity_internal_entity` | `select.vmc_‹nome›_selected_humidity_internal_entity` | Seleziona Entità Umidità Interna |
| `input_select.vmc_‹nome›_selected_media_player_entity` | `select.vmc_‹nome›_selected_media_player_entity` | Seleziona Media Player |
| `input_select.vmc_‹nome›_selected_notification_device` | `select.vmc_‹nome›_selected_notification_device` | Seleziona Dispositivo per Invio Notifica |
| `input_select.vmc_‹nome›_selected_temp_external_entity` | `select.vmc_‹nome›_selected_temp_external_entity` | Seleziona Entità Temperatura Esterna |
| `input_select.vmc_‹nome›_selected_temp_internal_entity` | `select.vmc_‹nome›_selected_temp_internal_entity` | Seleziona Entità Temperatura Interna |
| `input_select.vmc_‹nome›_speed_1_fascia_calendario` | `select.vmc_‹nome›_speed_1_fascia_calendario` | Set Velocità 1° Fascia Calendario |
| `input_select.vmc_‹nome›_speed_2_fascia_calendario` | `select.vmc_‹nome›_speed_2_fascia_calendario` | Set Velocità 2° Fascia Calendario |
| `input_select.vmc_‹nome›_speed_umidita` | `select.vmc_‹nome›_speed_umidita` | Set Velocità Umidità di Avvio |

### `input_select` → `sensor` (1)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_select.vmc_‹nome›_entita_escluse_recorder` | `sensor.vmc_‹nome›_entita_escluse_recorder` | Entità escluse dal Recorder |

### `input_text` → `sensor` (1)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_text.vmc_‹nome›_comando_non_eseguito` | `sensor.vmc_‹nome›_comando_non_eseguito` | Comando non Eseguito durante una Fascia |

### `input_text` → `text` (2)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `input_text.vmc_‹nome›_ip_insert` | `text.vmc_‹nome›_ip_insert` | Cambia IP VMC (Riavvio di H.A.) |
| `input_text.vmc_‹nome›_nome_da_inserire` | `text.vmc_‹nome›_nome_da_inserire` | Cambia Nome VMC |

## 2. Timer che diventano sensori con l'ora di fine / Timers that become end-time sensors (34)

### `timer` → `sensor` (34)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `timer.vmc_‹nome›_countdown_avvio_home_assistant` | `sensor.vmc_‹nome›_countdown_avvio_home_assistant` | Avvio di Home Assistant |
| `timer.vmc_‹nome›_countdown_avvisi` | `sensor.vmc_‹nome›_countdown_avvisi` | Aggiornamento Avvisi |
| `timer.vmc_‹nome›_countdown_blackout_rilevazione` | `sensor.vmc_‹nome›_countdown_blackout_rilevazione` | Rilevazione Black-Out |
| `timer.vmc_‹nome›_countdown_blackout_ripristino` | `sensor.vmc_‹nome›_countdown_blackout_ripristino` | Ripristino dopo Black-Out |
| `timer.vmc_‹nome›_countdown_calendario_fine` | `sensor.vmc_‹nome›_countdown_calendario_fine` | Fine Fascia |
| `timer.vmc_‹nome›_countdown_calendario_inizio` | `sensor.vmc_‹nome›_countdown_calendario_inizio` | Inizio Fascia |
| `timer.vmc_‹nome›_countdown_delta_avvio` | `sensor.vmc_‹nome›_countdown_delta_avvio` | Avvio Allerta Δ Temp. |
| `timer.vmc_‹nome›_countdown_delta_fine` | `sensor.vmc_‹nome›_countdown_delta_fine` | Fine Allerta Δ Temp. |
| `timer.vmc_‹nome›_countdown_delta_memoria` | `sensor.vmc_‹nome›_countdown_delta_memoria` | Memorizzazione Velocità (Δ Temp.) |
| `timer.vmc_‹nome›_countdown_fase_allerte` | `sensor.vmc_‹nome›_countdown_fase_allerte` | Riattivazione Gruppo di Allerte |
| `timer.vmc_‹nome›_countdown_free_cooling_annullamento` | `sensor.vmc_‹nome›_countdown_free_cooling_annullamento` | Annullamento Memoria Free Cooling |
| `timer.vmc_‹nome›_countdown_free_cooling_ripristino` | `sensor.vmc_‹nome›_countdown_free_cooling_ripristino` | Ripristino Free Cooling |
| `timer.vmc_‹nome›_countdown_free_cooling_sospensione` | `sensor.vmc_‹nome›_countdown_free_cooling_sospensione` | Sospensione Free Cooling |
| `timer.vmc_‹nome›_countdown_free_heating_annullamento` | `sensor.vmc_‹nome›_countdown_free_heating_annullamento` | Annullamento Memoria Free Heating |
| `timer.vmc_‹nome›_countdown_free_heating_ripristino` | `sensor.vmc_‹nome›_countdown_free_heating_ripristino` | Ripristino Free Heating |
| `timer.vmc_‹nome›_countdown_free_heating_sospensione` | `sensor.vmc_‹nome›_countdown_free_heating_sospensione` | Sospensione Free Heating |
| `timer.vmc_‹nome›_countdown_inquinanti_avvio` | `sensor.vmc_‹nome›_countdown_inquinanti_avvio` | Avvio Allerta Inquinanti |
| `timer.vmc_‹nome›_countdown_inquinanti_fine` | `sensor.vmc_‹nome›_countdown_inquinanti_fine` | Fine Allerta Inquinanti |
| `timer.vmc_‹nome›_countdown_inquinanti_memoria` | `sensor.vmc_‹nome›_countdown_inquinanti_memoria` | Memorizzazione Velocità (Inquinanti) |
| `timer.vmc_‹nome›_countdown_pdr_cambio` | `sensor.vmc_‹nome›_countdown_pdr_cambio` | Cambio Velocità per Lim. Δ PdR |
| `timer.vmc_‹nome›_countdown_pdr_ripristino` | `sensor.vmc_‹nome›_countdown_pdr_ripristino` | Ripristino dopo Lim. Δ PdR |
| `timer.vmc_‹nome›_countdown_riattivazione_allerte` | `sensor.vmc_‹nome›_countdown_riattivazione_allerte` | Riattivazione Allerte |
| `timer.vmc_‹nome›_countdown_script_agg_sensori` | `sensor.vmc_‹nome›_countdown_script_agg_sensori` | Agg. Sensori in corso |
| `timer.vmc_‹nome›_countdown_script_inizializzazione` | `sensor.vmc_‹nome›_countdown_script_inizializzazione` | Profilo Inizializzazione in corso |
| `timer.vmc_‹nome›_countdown_script_panic_button` | `sensor.vmc_‹nome›_countdown_script_panic_button` | Panic Button in corso |
| `timer.vmc_‹nome›_countdown_script_reset_filtro` | `sensor.vmc_‹nome›_countdown_script_reset_filtro` | Reset Filtro in corso |
| `timer.vmc_‹nome›_countdown_umidita_avvio` | `sensor.vmc_‹nome›_countdown_umidita_avvio` | Avvio Allerta Umidità |
| `timer.vmc_‹nome›_countdown_umidita_fine` | `sensor.vmc_‹nome›_countdown_umidita_fine` | Fine Allerta Umidità |
| `timer.vmc_‹nome›_countdown_umidita_memoria` | `sensor.vmc_‹nome›_countdown_umidita_memoria` | Memorizzazione Velocità (Umidità) |
| `timer.vmc_‹nome›_lettura_ambientali` | `sensor.vmc_‹nome›_lettura_ambientali` | Prossima Lettura Sensori Ambientali |
| `timer.vmc_‹nome›_lettura_lan` | `sensor.vmc_‹nome›_lettura_lan` | Prossima Lettura Sensori Lan |
| `timer.vmc_‹nome›_lettura_nome` | `sensor.vmc_‹nome›_lettura_nome` | Prossima Lettura Sensore Nome |
| `timer.vmc_‹nome›_lettura_ping` | `sensor.vmc_‹nome›_lettura_ping` | Prossima Lettura Verifica On-Line (Ping) |
| `timer.vmc_‹nome›_lettura_ventilazione` | `sensor.vmc_‹nome›_lettura_ventilazione` | Prossima Lettura Sensori Ventilazione |

## 3. Script e comandi che diventano pulsanti / Scripts and commands that become buttons (25)

### `script` → `button` (13)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `script.vmc_‹nome›_audio_profilo` | `button.vmc_‹nome›_audio_profilo` | VMC ‹nome› - Profilo Audio |
| `script.vmc_‹nome›_azzera_aria_scambiata` | `button.vmc_‹nome›_azzera_aria_scambiata` | VMC ‹nome› - Azzera Totale Aria Scambiata |
| `script.vmc_‹nome›_azzera_offset_sensors` | `button.vmc_‹nome›_azzera_offset_sensors` | VMC ‹nome› - Azzera gli Offset dei Sensori |
| `script.vmc_‹nome›_bottone_panico` | `button.vmc_‹nome›_bottone_panico` | VMC ‹nome› - Panic Button |
| `script.vmc_‹nome›_profilo_calendario` | `button.vmc_‹nome›_profilo_calendario` | VMC ‹nome› - Profilo Calendario |
| `script.vmc_‹nome›_profilo_free_heating_cooling` | `button.vmc_‹nome›_profilo_free_heating_cooling` | VMC ‹nome› - Profilo Free Heating/Cooling |
| `script.vmc_‹nome›_profilo_inizializzazione` | `button.vmc_‹nome›_profilo_inizializzazione` | VMC ‹nome› - Profilo Inizializzazione |
| `script.vmc_‹nome›_profilo_pdr` | `button.vmc_‹nome›_profilo_pdr` | VMC ‹nome› - Profilo Lim. Δ P. di Rugiada |
| `script.vmc_‹nome›_profilo_umidita` | `button.vmc_‹nome›_profilo_umidita` | VMC ‹nome› - Profilo Umidità Interna di Avvio |
| `script.vmc_‹nome›_pulisci_cronologia_audio` | `button.vmc_‹nome›_pulisci_cronologia_audio` | VMC ‹nome› - Pulisci cronologia Audio |
| `script.vmc_‹nome›_pulisci_cronologia_entita` | `button.vmc_‹nome›_pulisci_cronologia_entita` | VMC ‹nome› - Pulisci cronologia Entità |
| `script.vmc_‹nome›_reset_filtro_vmc` | `button.vmc_‹nome›_reset_filtro_vmc` | VMC ‹nome› - Reset Filtro |
| `script.vmc_‹nome›_upgrade_sensors` | `button.vmc_‹nome›_upgrade_sensors` | VMC ‹nome› - Agg. Sensori |

### `shell_command` → `button` (12)

| Oggi / Today | Versione nativa / Native | Nome / Name |
|---|---|---|
| `shell_command.vmc_‹nome›_freecooling` | `button.vmc_‹nome›_freecooling` | VMC ‹nome› - Free Cool./Heat. |
| `shell_command.vmc_‹nome›_iperventilazione` | `button.vmc_‹nome›_iperventilazione` | VMC ‹nome› - Iperventilazione |
| `shell_command.vmc_‹nome›_notturna` | `button.vmc_‹nome›_notturna` | VMC ‹nome› - Notturna |
| `shell_command.vmc_‹nome›_pannello_led_off` | `button.vmc_‹nome›_pannello_led_off` | VMC ‹nome› - Led Pannello Off |
| `shell_command.vmc_‹nome›_pannello_led_on` | `button.vmc_‹nome›_pannello_led_on` | VMC ‹nome› - Led Pannello On |
| `shell_command.vmc_‹nome›_sensori_off` | `button.vmc_‹nome›_sensori_off` | VMC ‹nome› - Sensori Off |
| `shell_command.vmc_‹nome›_sensori_on` | `button.vmc_‹nome›_sensori_on` | VMC ‹nome› - Sensori On |
| `shell_command.vmc_‹nome›_velocita_0` | `button.vmc_‹nome›_velocita_0` | VMC ‹nome› - Velocità 0 |
| `shell_command.vmc_‹nome›_velocita_1` | `button.vmc_‹nome›_velocita_1` | VMC ‹nome› - Velocità 1 |
| `shell_command.vmc_‹nome›_velocita_2` | `button.vmc_‹nome›_velocita_2` | VMC ‹nome› - Velocità 2 |
| `shell_command.vmc_‹nome›_velocita_3` | `button.vmc_‹nome›_velocita_3` | VMC ‹nome› - Velocità 3 |
| `shell_command.vmc_‹nome›_velocita_4` | `button.vmc_‹nome›_velocita_4` | VMC ‹nome› - Velocità 4 |

## 4. Voci che diventano interne all'integrazione (non più entità) / Items that become internal to the integration (no longer entities) (110)

### `input_boolean` → – (1)

| Oggi / Today | Nome / Name |
|---|---|
| `input_boolean.vmc_‹nome›_spia_umidita_mantenuta_velocita_0` | Spia Umidità Velocità 0 Mantenuta |

### `input_number` → – (32)

| Oggi / Today | Nome / Name |
|---|---|
| `input_number.vmc_‹nome›_aria_scambiata_freecooling` | Aria Scambiata a Vel. Free Heating/Cooling |
| `input_number.vmc_‹nome›_aria_scambiata_iperventilazione` | Aria Scambiata a Vel. Iperventilazione |
| `input_number.vmc_‹nome›_aria_scambiata_notte` | Aria Scambiata a Vel. Notturna |
| `input_number.vmc_‹nome›_aria_scambiata_ricomincio` | Aria Scambiata Ricomincio |
| `input_number.vmc_‹nome›_aria_scambiata_v1` | Aria Scambiata a Velocità 1 |
| `input_number.vmc_‹nome›_aria_scambiata_v2` | Aria Scambiata a Velocità 2 |
| `input_number.vmc_‹nome›_aria_scambiata_v3` | Aria Scambiata a Velocità 3 |
| `input_number.vmc_‹nome›_aria_scambiata_v4` | Aria Scambiata a Velocità 4 |
| `input_number.vmc_‹nome›_attesa_avvisi` | Attesa Aggiornamento Avvisi |
| `input_number.vmc_‹nome›_attesa_blackout_rilevazione` | Attesa Rilevazione Black-Out |
| `input_number.vmc_‹nome›_attesa_blackout_ripristino` | Attesa Ripristino dopo Black-Out |
| `input_number.vmc_‹nome›_attesa_calendario_fine` | Attesa Fine Fascia |
| `input_number.vmc_‹nome›_attesa_calendario_inizio` | Attesa Inizio Fascia |
| `input_number.vmc_‹nome›_attesa_delta_avvio` | Attesa Avvio Allerta Δ Temp. |
| `input_number.vmc_‹nome›_attesa_delta_fine` | Attesa Fine Allerta Δ Temp. |
| `input_number.vmc_‹nome›_attesa_delta_memoria` | Attesa Memorizzazione Velocità (Δ Temp.) |
| `input_number.vmc_‹nome›_attesa_free_annullamento` | Attesa Annullamento Memoria Free Heating/Cooling |
| `input_number.vmc_‹nome›_attesa_free_ripristino` | Attesa Ripristino Free Heating/Cooling |
| `input_number.vmc_‹nome›_attesa_free_ripristino_inquinanti` | Attesa Ripristino Free Heating/Cooling (con Inquinanti) |
| `input_number.vmc_‹nome›_attesa_free_sospensione` | Attesa Sospensione Free Heating/Cooling |
| `input_number.vmc_‹nome›_attesa_free_sospensione_inquinanti` | Attesa Sospensione Free Heating/Cooling (con Inquinanti) |
| `input_number.vmc_‹nome›_attesa_inquinanti_avvio` | Attesa Avvio Allerta Inquinanti |
| `input_number.vmc_‹nome›_attesa_inquinanti_avvio_spia_pdr` | Attesa Avvio Allerta Inquinanti (con Spia PdR) |
| `input_number.vmc_‹nome›_attesa_inquinanti_fine` | Attesa Fine Allerta Inquinanti |
| `input_number.vmc_‹nome›_attesa_inquinanti_memoria` | Attesa Memorizzazione Velocità (Inquinanti) |
| `input_number.vmc_‹nome›_attesa_pdr_cambio` | Attesa Cambio Velocità per Lim. Δ PdR |
| `input_number.vmc_‹nome›_attesa_pdr_cambio_inquinanti` | Attesa Cambio Velocità per Lim. Δ PdR (con Inquinanti) |
| `input_number.vmc_‹nome›_attesa_pdr_ripristino` | Attesa Ripristino dopo Lim. Δ PdR |
| `input_number.vmc_‹nome›_attesa_pdr_ripristino_inquinanti` | Attesa Ripristino dopo Lim. Δ PdR (con Inquinanti) |
| `input_number.vmc_‹nome›_attesa_umidita_avvio` | Attesa Avvio Allerta Umidità |
| `input_number.vmc_‹nome›_attesa_umidita_fine` | Attesa Fine Allerta Umidità |
| `input_number.vmc_‹nome›_attesa_umidita_memoria` | Attesa Memorizzazione Velocità (Umidità) |

### `input_text` → – (35)

| Oggi / Today | Nome / Name |
|---|---|
| `input_text.vmc_‹nome›_countdown_avvisi` | Aggiornamento Avvisi - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_blackout_rilevazione` | Rilevazione Black-Out - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_blackout_ripristino` | Ripristino dopo Black-Out - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_calendario_fine` | Fine Fascia - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_calendario_inizio` | Inizio Fascia - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_delta_avvio` | Avvio Allerta Δ Temp. - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_delta_fine` | Fine Allerta Δ Temp. - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_delta_memoria` | Memorizzazione Velocità (Δ Temp.) - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_free_cooling_annullamento` | Annullamento Memoria Free Cooling - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_free_cooling_ripristino` | Ripristino Free Cooling - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_free_cooling_sospensione` | Sospensione Free Cooling - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_free_heating_annullamento` | Annullamento Memoria Free Heating - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_free_heating_ripristino` | Ripristino Free Heating - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_free_heating_sospensione` | Sospensione Free Heating - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_inquinanti_avvio` | Avvio Allerta Inquinanti - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_inquinanti_fine` | Fine Allerta Inquinanti - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_inquinanti_memoria` | Memorizzazione Velocità (Inquinanti) - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_pdr_cambio` | Cambio Velocità per Lim. Δ PdR - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_pdr_ripristino` | Ripristino dopo Lim. Δ PdR - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_umidita_avvio` | Avvio Allerta Umidità - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_umidita_fine` | Fine Allerta Umidità - Trigger in Attesa |
| `input_text.vmc_‹nome›_countdown_umidita_memoria` | Memorizzazione Velocità (Umidità) - Trigger in Attesa |
| `input_text.vmc_‹nome›_ip_insert_esito` | Esito Verifica VMC al Nuovo IP |
| `input_text.vmc_‹nome›_last_co2_internal_entity` | Ultima Entità CO₂ interna Selezionata |
| `input_text.vmc_‹nome›_last_humidity_external_entity` | Ultima Entità Umidità esterna Selezionata |
| `input_text.vmc_‹nome›_last_humidity_internal_entity` | Ultima Entità Umidità interna Selezionata |
| `input_text.vmc_‹nome›_last_media_player_entity` | Ultima Entità Media Player Selezionato |
| `input_text.vmc_‹nome›_last_notification_device` | Ultimo Dispositivo per Invio Notifica Selezionato |
| `input_text.vmc_‹nome›_last_temp_external_entity` | Ultima Entità Temperatura esterna Selezionata |
| `input_text.vmc_‹nome›_last_temp_internal_entity` | Ultima Entità Temperatura interna Selezionata |
| `input_text.vmc_‹nome›_tempo_mancante_reset` | Reset Countdown Ricambio |
| `input_text.vmc_‹nome›_ultima_scelta_utente` | Ultima Scelta di Velocità dell'Utente |
| `input_text.vmc_‹nome›_ultime_letture_velocita` | Ultime Letture di Velocità della VMC |
| `input_text.vmc_‹nome›_ultimi_comandi_automazione` | Ultimi Comandi di Velocità dell'Automazione |
| `input_text.vmc_‹nome›_velocita_precedente` | Velocità precedente VMC |

### `script` → – (38)

| Oggi / Today | Nome / Name |
|---|---|
| `script.vmc_‹nome›_aggiorna_elenco_entita_co2_interna` | VMC ‹nome› - Aggiorna Elenco Entità Anidride Carbonica Interna |
| `script.vmc_‹nome›_aggiorna_elenco_entita_media_player` | VMC ‹nome› - Aggiorna Elenco Entità Media Player |
| `script.vmc_‹nome›_aggiorna_elenco_entita_notifica_dispositivo` | VMC ‹nome› - Aggiorna Elenco Entità Notifica Dispositivo |
| `script.vmc_‹nome›_aggiorna_elenco_entita_temperatura_esterna` | VMC ‹nome› - Aggiorna Elenco Entità Temperatura Esterna |
| `script.vmc_‹nome›_aggiorna_elenco_entita_temperatura_interna` | VMC ‹nome› - Aggiorna Elenco Entità Temperatura Interna |
| `script.vmc_‹nome›_aggiorna_elenco_entita_umidita_esterna` | VMC ‹nome› - Aggiorna Elenco Entità Umidità Esterna |
| `script.vmc_‹nome›_aggiorna_elenco_entita_umidita_interna` | VMC ‹nome› - Aggiorna Elenco Entità Umidità Interna |
| `script.vmc_‹nome›_audio_allerta_black_out` | VMC ‹nome› - Audio Black-Out |
| `script.vmc_‹nome›_audio_allerta_co2` | VMC ‹nome› - Audio CO₂ |
| `script.vmc_‹nome›_audio_allerta_congelamento` | VMC ‹nome› - Audio Congelamento |
| `script.vmc_‹nome›_audio_allerta_diff_temp` | VMC ‹nome› - Audio Diff. Temp. Int-Est > 23 [°C] |
| `script.vmc_‹nome›_audio_allerta_pdr` | VMC ‹nome› - Audio Punto di Rugiada |
| `script.vmc_‹nome›_audio_allerta_umidita_interna` | VMC ‹nome› - Audio Umidità Interna |
| `script.vmc_‹nome›_audio_allerta_voc` | VMC ‹nome› - Audio VOC |
| `script.vmc_‹nome›_audio_free_heating_o_free_cooling` | VMC ‹nome› - Audio Free Heating/Cooling |
| `script.vmc_‹nome›_audio_nessuna_allerta_black_out` | VMC ‹nome› - Audio Assenza Black-Out |
| `script.vmc_‹nome›_audio_nessuna_allerta_co2` | VMC ‹nome› - Audio Assenza CO₂ |
| `script.vmc_‹nome›_audio_nessuna_allerta_congelamento` | VMC ‹nome› - Audio Assenza Congelamento |
| `script.vmc_‹nome›_audio_nessuna_allerta_diff_temp` | VMC ‹nome› - Audio Assenza Diff. Temp. Int-Est > 23 [°C] |
| `script.vmc_‹nome›_audio_nessuna_allerta_pdr` | VMC ‹nome› - Audio Assenza Punto di Rugiada |
| `script.vmc_‹nome›_audio_nessuna_allerta_umidita_interna` | VMC ‹nome› - Audio Assenza Umidità Interna |
| `script.vmc_‹nome›_audio_nessuna_allerta_voc` | VMC ‹nome› - Audio Assenza VOC |
| `script.vmc_‹nome›_audio_status_velocita` | VMC ‹nome› - Audio Status Velocità |
| `script.vmc_‹nome›_azzera_aria_scambiata_puntuale` | VMC ‹nome› - Azzera Totale Aria Scambiata Puntuale |
| `script.vmc_‹nome›_azzera_booleans` | VMC ‹nome› - Booleans Off |
| `script.vmc_‹nome›_calendario_fascia_1_o_2_off` | VMC ‹nome› - Calendario Fascia 1 o 2 Off |
| `script.vmc_‹nome›_calendario_fascia_1_on` | VMC ‹nome› - Calendario Fascia 1 On |
| `script.vmc_‹nome›_calendario_fascia_2_on` | VMC ‹nome› - Calendario Fascia 2 On |
| `script.vmc_‹nome›_notifica_cambio_filtro` | VMC ‹nome› - Invia notifica Cambio Filtro |
| `script.vmc_‹nome›_notifica_errore_co2_interna` | VMC ‹nome› - Invia notifica Errore CO₂ Interna |
| `script.vmc_‹nome›_notifica_errore_media_player` | VMC ‹nome› - Invia notifica Errore Media Player |
| `script.vmc_‹nome›_notifica_errore_temp_esterna` | VMC ‹nome› - Invia notifica Errore Temp. Esterna |
| `script.vmc_‹nome›_notifica_errore_temp_interna` | VMC ‹nome› - Invia notifica Errore Temp. Interna |
| `script.vmc_‹nome›_notifica_errore_umidita_esterna` | VMC ‹nome› - Invia notifica Errore Umidità Esterna |
| `script.vmc_‹nome›_notifica_errore_umidita_interna` | VMC ‹nome› - Invia notifica Errore Umidità Interna |
| `script.vmc_‹nome›_notifica_velocita_0` | VMC ‹nome› - Invia notifica Velocità 0 |
| `script.vmc_‹nome›_notifica_velocita_diversa_da_0` | VMC ‹nome› - Invia notifica VMC in Funzione |
| `script.vmc_‹nome›_ripristina_tempi_attesa` | VMC ‹nome› - Ripristina Tempi di Attesa Originali |

### `shell_command` → – (4)

| Oggi / Today | Nome / Name |
|---|---|
| `shell_command.vmc_‹nome›_aggiorna_indirizzo_ip` | – |
| `shell_command.vmc_‹nome›_cambia_nome` | – |
| `shell_command.vmc_‹nome›_reset_filtro` | – |
| `shell_command.vmc_‹nome›_rimuovi_caratteri_di_ritorno` | – |
