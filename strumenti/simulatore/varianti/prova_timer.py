"""Variante di prova dell'orologio virtuale (non e' un motore): registra timer che non fanno niente.

Un timer ogni 0,37 s virtuali (che ogni volta ne registra e ne annulla altri due) non cambia nessuno
stato: il differenziale contro «identica» deve dare zero differenze. Imita un motore che usa timer suoi,
diversi da quelli degli script YAML. Con l'orologio della b36 (SIM_TIMER=b36) l'ordine di due timer allo
stesso istante e i microsecondi degli istanti dipendevano anche da questi timer estranei.
"""


def prepara_configurazione(cfg_dir: str) -> None:
    """Nessuna modifica alla configurazione."""


async def avvia(hass) -> None:
    loop = hass.loop

    def niente():
        pass

    def battito():
        for ritardo in (0.5, 1.3):
            loop.call_later(ritardo, niente).cancel()
        loop.call_later(0.37, battito)

    loop.call_later(0.37, battito)
