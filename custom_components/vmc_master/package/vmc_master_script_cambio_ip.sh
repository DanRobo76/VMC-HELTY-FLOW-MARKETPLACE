###########################################################################################################################################################################################################################
#                                                                                                                                                                                                                         #
#                                                          SCRIPT CAMBIO IP VMC HELTY FLOW PLUS RELEASE [VER. 1.0]                                                                                                        #
#                                                                                                                                                                                                                         #
# SVILUPPATO DA ING. DANILO ROBOTTI, ALLE PRIME ARMI CON HOME ASSISTANT :)                                                                                                                                                #
#                                                                                                                                                                                                                         #
# COPYRIGHT © 2023-2026 ING. DANILO ROBOTTI                                                                                                                                                                               #
#                                                                                                                                                                                                                         #
# LICENZA: GNU GENERAL PUBLIC LICENSE VERSIONE 3 (GPL-3.0), PER LA VERSIONE DISTRIBUITA CON L'INTEGRAZIONE VMC MASTER (MARKETPLACE)                                                                                       #
# TESTO UFFICIALE DELLA LICENZA (IN INGLESE, L'UNICO CHE FA FEDE): https://www.gnu.org/licenses/gpl-3.0.html                                                                                                              #
# Copyright © 2023-2026 Ing. Danilo Robotti (https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE)                                                                                                                     #
#                                                                                                                                                                                                                         #
# LA LICENZA GPL-3.0 SI APPLICA AI SEGUENTI FILES DISTRIBUITI CON L'INTEGRAZIONE VMC MASTER:                                                                                                                              #
#   - VMC_MASTER.YAML                                                                                                                                                                                                     #
#   - VMC_MASTER_AUTOMAZIONE.TXT                                                                                                                                                                                          #
#   - VMC_MASTER_SCHEDA_MANUALE_INTERFACCIA.TXT                                                                                                                                                                           #
#   - VMC_MASTER_SCRIPT_CAMBIO_IP.SH                                                                                                                                                                                      #
#   - VMC_MASTER_SCRIPT_CAMBIO_NOME.SH                                                                                                                                                                                    #
#   LA RELEASE MANUALE 8.6.0 DEL REPOSITORY VMC-HELTY-FLOW RESTA SOTTO POLYFORM NONCOMMERCIAL LICENSE 1.0.0.                                                                                                              #
#                                                                                                                                                                                                                         #
# IN SINTESI:                                                                                                                                                                                                             #
#  - È CONSENTITO USARE, COPIARE, MODIFICARE E DISTRIBUIRE IL SOFTWARE, ANCHE PER SCOPI COMMERCIALI;                                                                                                                      #
#  - CHI DISTRIBUISCE IL SOFTWARE, ANCHE MODIFICATO, DEVE RENDERNE DISPONIBILE IL CODICE SORGENTE CON LA STESSA LICENZA GPL-3.0,                                                                                          #
#    MANTENERE QUESTA NOTA DI COPYRIGHT E INDICARE LE MODIFICHE APPORTATE;                                                                                                                                                #
#  - IL SOFTWARE È FORNITO SENZA ALCUNA GARANZIA (SEZIONI 15 E 16 DELLA LICENZA);                                                                                                                                         #
#  - IN CASO DI VIOLAZIONE LA LICENZA DECADE, SALVO REGOLARIZZAZIONE ENTRO 30 GIORNI DALLA SEGNALAZIONE (SEZIONE 8 DELLA LICENZA).                                                                                        #
#                                                                                                                                                                                                                         #
# PER INFORMAZIONI CONTATTARE L'AUTORE: danilo.robotti@gmail.com                                                                                                                                                          #
#                                                                                                                                                                                                                         #
# DATA: 11 NOVEMBRE 2026                                                                                                                                                                                                  #
#                                                                                                                                                                                                                         #
# Impiego dell'Intelligenza Artificiale                                                                                                                                                                                   #
# Nello sviluppo del presente software l'autore si è avvalso anche di strumenti di intelligenza artificiale.                                                                                                              #
#                                                                                                                                                                                                                         #
# Esonero di Responsabilità                                                                                                                                                                                               #
# Il software è fornito «così com'è», senza garanzie di alcun tipo. In nessun caso lo sviluppatore sarà responsabile di danneggiamenti diretti, indiretti o conseguenti, correlati a difetti del presente software.       #
# L'usufruitore ha l'onere e la responsabilità della scelta, dell'installazione, dell'uso e della gestione del software al fine del raggiungimento del risultato prefissatosi.                                            #
#                                                                                                                                                                                                                         #
###########################################################################################################################################################################################################################
#!/bin/bash

export LC_ALL=C  # Confronti e intervalli di caratteri indipendenti dalla lingua del sistema
IP="$1"  # Imposta l'indirizzo IP specificato come argomento

# Interrompe senza modificare nulla se l'argomento non è un indirizzo IP valido (altrimenti gli indirizzi nei file verrebbero cancellati).
# Si controlla l'intero testo, non riga per riga: un solo argomento, una sola riga, 4 numeri da 0 a 255 senza zeri iniziali
# (stessa regola del controllo dell'Automazione Cambio IP), così nei comandi sed qui sotto non può entrare altro testo.
OTTETTO='(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'
[[ $# -eq 1 && $IP =~ ^($OTTETTO\.){3}$OTTETTO$ ]] || { echo "Indirizzo IP non valido: '$IP'"; exit 1; }

# Esegui la sostituzione dell'indirizzo IP nel file YAML
sed -i "s/[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+/$IP/g" "/config/packages/vmc_helty_flow/master/vmc_master.yaml"
sed -i 's/nc -w 3 [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+ 5001/nc -w 3 '"$IP"' 5001/' "/config/packages/vmc_helty_flow/master/vmc_master_script_cambio_nome.sh"