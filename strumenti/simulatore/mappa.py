"""Mappa dei nomi per confronta.py --mappa: il package di oggi (A) contro l'integrazione nativa (B).

Con la variante nativa4 (fase 4) le entita' della VMC non sono piu' quelle del package: i 172
aiutanti visibili diventano entita' native con un altro dominio (stesso object_id), i valori
interni, i timer e gli script vanno dentro il motore, arrivano 25 pulsanti e 34 sensori con
l'istante di fine dei timer. La mappa viene dalla colonna «Domani» della fase 1
(tests/nativa/motore/aiutanti_fase1.csv) e trasforma le voci dei due lati prima del confronto;
nessuna tolleranza oltre a quella scritta qui. Ogni voce tolta si conta per lato e motivo e il
rapporto ne da' l'elenco con i numeri esatti.

Voci di A (oggi):
- S/R/I/F di un aiutante visibile: l'entity_id di domani; dagli attributi si tolgono quelli che
  l'entita' nativa non ha (ATTRIBUTI_SOLO_AIUTANTE, gli stessi di
  tests/nativa/test_comandi_confronto.py, dove la prova con Home Assistant li conferma);
- S/R di un timer o di un valore interno: voci MS/MR («nel motore»), confrontate con le voci MS/MR
  che il lato B scrive dal motore (timer del motore; memoria interna) o, finche' i valori interni
  restano aiutanti del package anche in B, con le sue S/R degli stessi aiutanti; le loro voci I/F
  (stato all'avvio e al fork) si tolgono: nel motore non sono stati di Home Assistant;
- S/R/I/F degli script: tolte (domani gli script sono nel motore, senza entita');
- S/R/I/F, C/E e «cambio ip» delle voci tolte (colonna «Domani» = «tolta», piu' il sensore e
  l'automazione del campo «Cambia IP VMC»): tolte (dalla b46 domani non ci sono; gli scenari
  IP di gen_mancanti restano solo per il lato A);
- C/E: gli entity_id dei dati con i nomi di domani; in homeassistant.update_entity si tolgono
  i valori interni dalle entita' (domani non sono entita': il motore li toglie dalla chiamata
  e li riscrive lui nel loro turno, con la stessa voce MR di oggi);
- X: i comandi alla VMC (printf ... | nc) come «tcp: <comando>», il ping come «ping <ip>», il
  cambio del nome come «tcp: VMNM <nome>» (le stesse forme che scrive nativa4); il «find ... sed»
  dei file .sh e il cambio dell'indirizzo (b46), che domani non ci sono, si tolgono.

Voci di B (domani):
- S/R/I/F dei 25 pulsanti e dei 34 sensori dei timer: tolte (entita' nuove, senza una di oggi);
- C/E di un servizio di un dominio nativo su sole entita' della VMC (l'utente degli scenari che
  preme un pulsante o cambia un'impostazione): tolte, perche' oggi la stessa azione e' una
  chiamata a un aiutante, che la traccia non registra (tracce.DOMINI_INTERNI).
"""
import collections
import csv
import hashlib
import json
import re

import tracce

ATTRIBUTI_SOLO_AIUTANTE = {
    ('input_boolean', 'switch'): {'editable'},
    ('input_boolean', 'binary_sensor'): {'editable'},
    ('input_number', 'number'): {'editable', 'initial'},
    ('input_number', 'sensor'): {'editable', 'initial', 'min', 'max', 'step', 'mode'},
    ('input_select', 'select'): {'editable'},
    ('input_select', 'sensor'): {'editable'},
    ('input_text', 'text'): {'editable'},
    ('input_text', 'sensor'): {'editable', 'min', 'max', 'pattern', 'mode'},
    ('input_datetime', 'time'): {'editable', 'has_date', 'has_time', 'hour', 'minute', 'second', 'timestamp'},
}
AIUTANTI = ('input_boolean', 'input_number', 'input_select', 'input_text', 'input_datetime')
DOMINI_NATIVI = frozenset({'switch', 'binary_sensor', 'number', 'select', 'text', 'time', 'sensor', 'button'})

MOTIVI = {
    'script': "entita' di uno script: domani lo script e' nel motore, senza entita'",
    'interno_avvio': "valore interno nello stato all'avvio o al fork (I/F): domani e' nella memoria del motore",
    'timer_avvio': "timer nello stato all'avvio o al fork (I/F): domani e' un timer del motore",
    'pulsante': "pulsante: entita' nuova, oggi non c'e'",
    'sensore_timer': ("sensore con l'istante di fine di un timer: entita' nuova, oggi non c'e' (i 5 lettura_* scrivono "
                      "solo con la finestra «Prossime letture» accesa: sensori_timer.SOLO_CON_LA_FINESTRA)"),
    'chiamata_nativa': "chiamata dell'utente a un'entita' nativa: oggi va a un aiutante e la traccia non la registra",
    'find': "comando di shell «find ... sed» sui file .sh: domani non c'e'",
    'tolta': "voce tolta (b46: campo «Cambia IP VMC» della scheda e chi lo serve): domani non c'e'",
}
# Le voci tolte che non sono nella fase 1 (tabelle.TOLTE): il sensore e l'automazione del campo.
TOLTE_FUORI_DALLA_FASE_1 = frozenset({'sensor.vmc_master_verifica_ip_inserito',
                                      'automation.vmc_master_cambio_ip_vmc_riavvio_di_h_a'})
# Voci cambiate (non tolte) dalla mappa, contate come le voci tolte.
MOTIVI_CAMBIATE = {
    'update_interni': ("homeassistant.update_entity con valori interni tra le entita': tolti dai dati "
                       "(domani il motore li toglie dalla chiamata e li riscrive lui: voce MR uguale)"),
}
TIPI_MOTORE = {'MS': "cambio di stato nel motore (timer, valore interno)",
               'MR': "scrittura senza cambio nel motore (timer, valore interno)"}

_PRINTF = re.compile(r"^printf '([^'\\]*)\\n' \| timeout \d+ nc ")
_PING = re.compile(r"^ping .* (\d+\.\d+\.\d+\.\d+) ")
_NOME = re.compile(r'^bash \S*vmc_\w+_script_cambio_nome\.sh\s+"?(.*?)"?\s*$')
_IP = re.compile(r"^bash \S*vmc_\w+_script_cambio_ip\.sh\s+(\S*)\s*$")


def _impronta(attributi):
    return hashlib.blake2b(tracce._json(attributi).encode('utf-8'), digest_size=8).hexdigest()


class Mappa:
    """La mappa dei nomi della fase 1 e il conto delle voci tolte (lato, motivo, tipo)."""

    def __init__(self, percorso):
        self.percorso = percorso
        with open(percorso, encoding='utf-8-sig', newline='') as f:
            righe = [(r['Entità oggi'], r['Domani']) for r in csv.DictReader(f, delimiter=';')]
        self.visibili = {}
        self.interni = set()
        self.timer = {}
        self.script = set()
        self.pulsanti = set()
        self.voci_tolte = set(TOLTE_FUORI_DALLA_FASE_1)
        for oggi, domani in righe:
            tipo = oggi.split('.')[0]
            if domani.startswith('button.'):
                self.pulsanti.add(domani)
            if domani == 'tolta':
                self.voci_tolte.add(oggi)
            elif tipo in AIUTANTI:
                if domani.startswith('interna'):
                    self.interni.add(oggi)
                else:
                    self.visibili[oggi] = domani
            elif tipo == 'timer':
                self.timer[oggi] = domani
            elif tipo == 'script':
                self.script.add(oggi)
        self.sensori_timer = set(self.timer.values())
        self.tolte = collections.Counter()
        self.cambiate = collections.Counter()

    def descrizione(self):
        return (f"{self.percorso}: {len(self.visibili)} aiutanti visibili, {len(self.interni)} valori interni, "
                f"{len(self.timer)} timer, {len(self.script)} script, {len(self.pulsanti)} pulsanti")

    # --- trasformazione --------------------------------------------------------------------

    def _togli(self, lato, motivo, tipo):
        """Conta la voce tolta; la voce trasformata è None (tolta)."""
        self.tolte[(lato, motivo, tipo)] += 1

    def _attributi(self, voce, attr, nuovi, togli=()):
        """La voce con l'impronta degli attributi ricalcolata (senza gli attributi ``togli``)."""
        if voce[4] is None:
            return voce
        a = {k: v for k, v in attr.get(voce[4], {}).items() if k not in togli}
        d = _impronta(a)
        nuovi[d] = a
        return voce[:4] + [d] + voce[5:]

    def _dati(self, testo, servizio=None, lato='A', tipo='C'):
        dati = json.loads(testo)
        e = dati.get('entity_id')
        if servizio == ('homeassistant', 'update_entity'):
            elenco = [e] if isinstance(e, str) else e
            if isinstance(elenco, list) and any(x in self.interni for x in elenco):
                self.cambiate[(lato, 'update_interni', tipo)] += 1
                e = [x for x in elenco if x not in self.interni]
        if isinstance(e, str):
            dati['entity_id'] = self.visibili.get(e, e)
        elif isinstance(e, list):
            dati['entity_id'] = [self.visibili.get(x, x) for x in e]
        return tracce._json(dati)

    def _shell(self, comando):
        for regola, forma in ((_PRINTF, 'tcp: {}'), (_PING, 'ping {}'), (_NOME, 'tcp: VMNM {}')):
            m = regola.search(comando)
            if m:
                return forma.format(m.group(1))
        return comando

    def voce(self, v, lato, attr, nuovi):
        """La voce ``v`` del lato ``lato`` ('A' o 'B') con i nomi di domani, o None se si toglie."""
        k = v[0]
        if k in 'SRIF':
            e = v[2]
            if e in self.voci_tolte:
                return self._togli(lato, 'tolta', k)
            if e in self.script:
                return self._togli(lato, 'script', k)
            if lato == 'B' and e in self.pulsanti:
                return self._togli(lato, 'pulsante', k)
            if lato == 'B' and e in self.sensori_timer:
                return self._togli(lato, 'sensore_timer', k)
            if e in self.interni or e in self.timer:
                if k in 'IF':
                    return self._togli(lato, 'interno_avvio' if e in self.interni else 'timer_avvio', k)
                v = ['M' + k] + v[1:]
                return self._attributi(v, attr, nuovi) if k == 'S' else v
            if lato == 'A' and e in self.visibili:
                nuovo = self.visibili[e]
                v = v[:2] + [nuovo] + v[3:]
                if k == 'R':
                    return v
                return self._attributi(v, attr, nuovi, ATTRIBUTI_SOLO_AIUTANTE[(e.split('.')[0], nuovo.split('.')[0])])
            return v if k == 'R' else self._attributi(v, attr, nuovi)
        if k == 'MS':
            return self._attributi(v, attr, nuovi)
        if k in 'CE':
            bersagli = json.loads(v[4]).get('entity_id')
            bersagli = [bersagli] if isinstance(bersagli, str) else (bersagli or [])
            if bersagli and all(b in self.voci_tolte for b in bersagli):
                return self._togli(lato, 'tolta', k)
            if lato == 'A':
                return v[:4] + [self._dati(v[4], (v[2], v[3]), lato, k)] + v[5:]
            if v[2] in DOMINI_NATIVI:
                bersagli = json.loads(v[4]).get('entity_id')
                bersagli = [bersagli] if isinstance(bersagli, str) else (bersagli or [])
                if bersagli and all(tracce.entita_vmc(b) for b in bersagli):
                    return self._togli(lato, 'chiamata_nativa', k)
            return v
        if k == 'X' and lato == 'A':
            if v[2].startswith('find '):
                return self._togli(lato, 'find', k)
            if _IP.search(v[2]):
                return self._togli(lato, 'tolta', k)
            return v[:2] + [self._shell(v[2])]
        return v

    def applica(self, voci, attr, lato):
        """Le voci di un lato con la mappa e la nuova tabella degli attributi (impronta -> attributi)."""
        nuovi = {}
        uscita = []
        for v in voci:
            w = self.voce(list(v), lato, attr, nuovi)
            if w is not None:
                uscita.append(w)
        # le istantanee (I all'inizio, F alla fine) sono in ordine di entity_id: con i nuovi nomi si
        # rimettono in ordine
        iniziali = sorted((w for w in uscita if w[0] == 'I'), key=lambda w: w[2])
        finali = sorted((w for w in uscita if w[0] == 'F'), key=lambda w: w[2])
        altre = [w for w in uscita if w[0] not in 'IF']
        return iniziali + altre + finali, nuovi

    def elenco(self):
        """Righe del rapporto: le voci tolte per motivo, tipo e lato, con i numeri esatti."""
        righe = []
        for (lato, motivo, tipo), n in sorted(self.tolte.items(), key=lambda x: (x[0][1], x[0][2], x[0][0])):
            righe.append(f"  {n:>9}  {tipo:<2} {lato}  {MOTIVI[motivo]}")
        for (lato, motivo, tipo), n in sorted(self.cambiate.items()):
            righe.append(f"  {n:>9}  {tipo:<2} {lato}  (cambiata, non tolta) {MOTIVI_CAMBIATE[motivo]}")
        return righe
