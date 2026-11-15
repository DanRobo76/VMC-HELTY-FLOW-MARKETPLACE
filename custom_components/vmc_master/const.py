"""Costanti dell'integrazione VMC Master."""

from __future__ import annotations

import re
from typing import Final

DOMAIN: Final = "vmc_master"

# Dati salvati in ogni voce di configurazione (una per VMC)
CONF_NOME: Final = "nome"
CONF_HOST: Final = "host"

# Nome della prima VMC: e' l'unica che contiene la Finestra Prima Installazione VMC
NOME_MASTER: Final = "master"

# Stesse regole della Finestra Clona: solo lettere minuscole, da 1 a 10 caratteri
NOME_RE: Final = re.compile(r"[a-z]{1,10}")

# Stessa regola degli script Clona e Cambia IP
IP_RE: Final = re.compile(r"[0-9]{1,3}(\.[0-9]{1,3}){3}")

# Porta TCP della VMC (impostazione di fabbrica)
PORTA_VMC: Final = 5001
TIMEOUT_VMC: Final = 3

# Percorsi web serviti dall'integrazione
URL_FRONTEND: Final = "/vmc_master_frontend"
FILE_SCHEDA_JS: Final = "vmc-master-card.js"

# Sorgente della scheda (identica alla scheda manuale della release 8.6.0)
FILE_SCHEDA: Final = "vmc_master_scheda_manuale_interfaccia.txt"

URL_REPOSITORY: Final = "https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE"

# Entita' della Finestra Clona della VMC Master 8.6.0 (18): l'integrazione toglie la Finestra
# Clona, quindi dopo la migrazione restano «non piu' fornite» e vengono tolte dal registro
ENTITA_FINESTRA_CLONA: Final = (
    "automation.vmc_master_clona_annulla_conferma_cancellazione",
    "automation.vmc_master_clona_rimuovi_file_obsoleti",
    "button.vmc_master_clona_pulsante_cancella",
    "button.vmc_master_clona_pulsante_clona",
    "button.vmc_master_clona_pulsante_conferma_cancella",
    "input_boolean.vmc_master_clona_conferma_cancellazione",
    "input_boolean.vmc_master_clona_eseguita",
    "input_boolean.vmc_master_opzione_finestra_clona",
    "input_text.vmc_master_clona_ip",
    "input_text.vmc_master_clona_nome",
    "input_text.vmc_master_clona_vmc_cancellate",
    "input_text.vmc_master_clona_vmc_clonate",
    "script.vmc_master_clona_cancella_vmc",
    "script.vmc_master_clona_nuova_clonazione",
    "script.vmc_master_clona_riavvio_ha",
    "script.vmc_master_clona_vmc",
    "sensor.vmc_master_clona_verifica_ip",
    "sensor.vmc_master_clona_verifica_nome",
)
