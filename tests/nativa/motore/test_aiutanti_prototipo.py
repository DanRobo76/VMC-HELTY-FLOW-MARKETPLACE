"""Prototipo della fase 4, solo per gli ``input_boolean``: il motore tradotto con la
mappa dei nomi gira contro entità native e fa quello che fa Home Assistant con gli
aiutanti.

Da una parte Home Assistant con lo YAML (aiutanti ``input_boolean``, automazioni,
script); dall'altra il motore tradotto CON la mappa (``rinomina.py``) contro gli
``switch`` e i ``binary_sensor`` minimi di ``aiutanti_nativi.py``. Stesso orologio,
stessi passi; i due registri, riportati i nomi di domani a quelli di oggi, devono dire
gli stessi cambi di stato, agli stessi istanti e con gli stessi contesti.

Nulla di questo è collegato alle piattaforme vere dell'integrazione.
"""

from __future__ import annotations

import difflib
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import Context, Event, HomeAssistant, ServiceCall, callback
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockUser,
    async_test_home_assistant,
)

from custom_components.vmc_master.nativa.motore import generato
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche

from .aiutanti_nativi import (
    DOMINIO_SCRITTURA,
    InterruttoreNativo,
    ScritturaNativa,
    SpiaNativa,
    aggiungi,
)
from .fase3 import MotoreFase3
from .rinomina import NomeAmbiguo, Rinomina, da_fase_1
from .test_semantica import (
    EVENTI,
    T0,
    _avanza,
    _carica,
    _gira,
    _norma,
    moduli,  # noqa: F401
)
from .traduci import leggi_package, traduci_configurazione, traduzione

SERVIZI = {
    f"input_boolean.{nome}": f"{DOMINIO_SCRITTURA}.{nome}"
    for nome in ("turn_on", "turn_off", "toggle")
}


def _mappa() -> Rinomina:
    """La mappa degli ``input_boolean`` del package: 37 ``switch``, 77
    ``binary_sensor`` e, nel prototipo, anche l'unico «interno» come ``binary_sensor``
    (un'entità nascosta: resta nella macchina degli stati)."""
    return da_fase_1(["input_boolean"], SERVIZI, interna="binary_sensor")


# --- la mappa e il traduttore -----------------------------------------------------------------


def test_mappa_degli_input_boolean() -> None:
    mappa = _mappa()
    domini = [nuova.split(".")[0] for nuova in mappa.entita.values()]
    assert len(mappa.entita) == 115
    assert (domini.count("switch"), domini.count("binary_sensor")) == (37, 78)
    assert all(
        vecchia.split(".", 1)[1] == nuova.split(".", 1)[1]
        for vecchia, nuova in mappa.entita.items()
    )
    assert len(set(mappa.entita.values())) == 115
    assert da_fase_1(["input_boolean"], SERVIZI).entita.keys() == (
        mappa.entita.keys()
        - {"input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0"}
    )


def test_testi_con_la_mappa() -> None:
    """Un'entità prende il nome di domani; l'inizio di un nome composto cambia dominio
    solo se tutte le entità che cominciano così vanno nello stesso; il resto non
    cambia."""
    mappa = _mappa()
    avvisi = "vmc_master_opzioni_accendi_spegni_avvisi"
    casi = {
        f"input_boolean.{avvisi}": f"switch.{avvisi}",
        f"input_boolean.{avvisi}_spia": f"binary_sensor.{avvisi}_spia",
        "input_boolean.vmc_master_spia_": "binary_sensor.vmc_master_spia_",
        "input_boolean.vmc_master_spia_velocita_0,input_boolean.vmc_master_notifica_audio": (
            "binary_sensor.vmc_master_spia_velocita_0,switch.vmc_master_notifica_audio"
        ),
        "state of input_boolean.vmc_master_notifica_audio": (
            "state of switch.vmc_master_notifica_audio"
        ),
        "input_boolean.turn_on": "input_boolean.turn_on",
        "input_boolean.altro": "input_boolean.altro",
        "sensor.vmc_master_status_ventola": "sensor.vmc_master_status_ventola",
        "states.input_boolean.vmc_master_notifica_audio": (
            "states.input_boolean.vmc_master_notifica_audio"
        ),
        "nessun nome qui": "nessun nome qui",
    }
    for vecchio, nuovo in casi.items():
        assert mappa.testo(vecchio) == nuovo
        assert mappa.indietro(nuovo) == vecchio
    assert mappa.frammenti == {
        "input_boolean.vmc_master_spia_": "binary_sensor.vmc_master_spia_"
    }
    assert mappa.servizio("input_boolean.turn_off") == "nativa_prova.turn_off"
    assert mappa.servizio("script.turn_on") == "script.turn_on"
    # un pezzo che comincia sia interruttori sia spie non si può tradurre a priori
    for pezzo in (
        "input_boolean.",
        "input_boolean.vmc_master_",
        f"input_boolean.{avvisi[:-1]}",
    ):
        with pytest.raises(NomeAmbiguo, match="binary_sensor.*switch"):
            mappa.testo(pezzo)
    # e nemmeno uno le cui entità domani cambiano anche l'oggetto
    cambia = Rinomina({"input_boolean.spia_a": "binary_sensor.luce_a"})
    assert cambia.testo("input_boolean.spia_a") == "binary_sensor.luce_a"
    with pytest.raises(NomeAmbiguo, match="cambia oggetto"):
        cambia.testo("input_boolean.spia_")


async def test_tutto_il_package_con_la_mappa(hass: HomeAssistant) -> None:
    """Tutto il package si traduce con la mappa: nel codice non resta nessun
    ``input_boolean`` (fuori dal testo dei modelli, tenuto per i messaggi d'errore) e,
    rimessi i nomi di oggi, il codice è byte per byte quello tradotto senza mappa: la
    mappa cambia i nomi e nient'altro."""
    automazioni, script = leggi_package()
    _, _, modelli_oggi, motore_oggi = await traduzione(hass, automazioni, script)
    automazioni, script = leggi_package()
    mappa = _mappa()
    _, _, modelli, motore = await traduzione(hass, automazioni, script, rinomina=mappa)
    assert mappa.frammenti == {
        "input_boolean.vmc_master_spia_": "binary_sensor.vmc_master_spia_",
        "input_boolean.vmc_master_spia_calendario_": (
            "binary_sensor.vmc_master_spia_calendario_"
        ),
    }
    for nome, testo, oggi in (
        ("modelli.py", modelli, modelli_oggi),
        ("motore.py", motore, motore_oggi),
    ):
        assert "input_boolean." not in _senza_sorgente(testo), nome
        assert "input_boolean." in _senza_sorgente(oggi), nome
        compile(testo, nome, "exec")
        assert testo != oggi, nome
        assert mappa.indietro(testo) == oggi, nome
    # le chiamate del package: 575 turn_on e 584 turn_off (come nell'inventario)
    for servizio, quante in (("turn_on", 575), ("turn_off", 584), ("toggle", 0)):
        assert motore_oggi.count(f"'input_boolean.{servizio}'") == quante
        assert motore.count(f"'nativa_prova.{servizio}'") == quante


# --- una prova fatta come il package, a confronto ---------------------------------------------

SPIE = [
    "vmc_master_spia_velocita_0",
    "vmc_master_spia_velocita_1",
    "vmc_master_spia_velocita_2",
    "vmc_master_spia_velocita_0_co2_o_voc",
    "vmc_master_spia_co2_o_voc",
    "vmc_master_spia_umidita_mantenuta_velocita_0",
]
CONFIGURAZIONE = (
    """
input_number:
  n: {min: 0, max: 100, step: 1}
input_boolean:
  vmc_master_opzioni_vmc: {name: Opzioni VMC, icon: "mdi:fan"}
  vmc_master_notifica_audio: {name: Notifica Audio, icon: "mdi:volume-high"}
  vmc_master_opzioni_accendi_spegni_avvisi: {name: Avvisi, icon: "mdi:bell"}
  vmc_master_opzioni_accendi_spegni_avvisi_spia: {name: Spia Avvisi}
  vmc_master_spia_velocita_0: {name: Spia Velocità 0, initial: true}
  vmc_master_spia_velocita_1: {name: Spia Velocità 1}
  vmc_master_spia_velocita_2: {name: Spia Velocità 2}
  vmc_master_spia_velocita_0_co2_o_voc: {name: Spia Velocità 0 CO2, initial: true}
  vmc_master_spia_co2_o_voc: {name: Spia CO2}
  vmc_master_spia_umidita_mantenuta_velocita_0: {name: Spia Umidità Mantenuta}
automation:
  - alias: Prova Velocità
    id: prova_velocita
    mode: queued
    triggers:
      - trigger: state
        entity_id: input_number.n
    variables:
      nomi: {0: velocita_0, 1: velocita_1, 2: velocita_2}
      scelta: "{{ states('input_number.n') | int }}"
    actions:
      - action: input_boolean.turn_off
        target:
          entity_id: >-
            {{ ['input_boolean.vmc_master_spia_velocita_0',
                'input_boolean.vmc_master_spia_velocita_1',
                'input_boolean.vmc_master_spia_velocita_2']
               | reject('eq', 'input_boolean.vmc_master_spia_' ~ nomi[scelta])
               | join(',') }}
      - action: input_boolean.turn_on
        target:
          entity_id: "input_boolean.vmc_master_spia_{{ nomi[scelta] }}"
      - action: prova.registra
        data:
          spie: >-
            {{ states('input_boolean.vmc_master_spia_velocita_0') }}
            {{ is_state('input_boolean.vmc_master_spia_velocita_1', 'on') }}
            {{ states.input_boolean.vmc_master_spia_velocita_2.state }}
            {{ states.input_boolean.vmc_master_spia_velocita_2.entity_id }}
          da: >-
            {{ (now() - states.input_boolean.vmc_master_spia_velocita_0.last_changed)
               .total_seconds() | round(1) }}
  - alias: Prova Spie
    id: prova_spie
    mode: restart
    triggers:
      - trigger: template
        value_template: >-
          {{ is_state('input_boolean.vmc_master_spia_velocita_2', 'on')
             and is_state('input_boolean.vmc_master_opzioni_vmc', 'on') }}
        for: {seconds: 2}
        id: mantenuta
      - trigger: state
        entity_id: input_boolean.vmc_master_spia_velocita_1
        to: "on"
        for: {seconds: 1}
        id: uno
    conditions:
      - condition: state
        entity_id: input_boolean.vmc_master_opzioni_accendi_spegni_avvisi
        state: "off"
    actions:
      - action: input_boolean.turn_on
        target:
          entity_id:
            - input_boolean.vmc_master_spia_co2_o_voc
            - input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0
            - input_boolean.vmc_master_opzioni_accendi_spegni_avvisi_spia
      - action: prova.registra
        data:
          quale: "{{ trigger.id }} {{ trigger.entity_id }} {{ trigger.to_state.state }}"
      - wait_template: "{{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'off') }}"
        timeout: {seconds: 3}
      - action: script.prova_fine
        data: {motivo: "{{ wait.completed }}"}
  - alias: Prova Interruttori
    id: prova_interruttori
    mode: parallel
    triggers:
      - trigger: state
        entity_id:
          - input_boolean.vmc_master_opzioni_vmc
          - input_boolean.vmc_master_notifica_audio
        from: "off"
        to: "on"
        id: acceso
      - trigger: state
        entity_id: input_boolean.vmc_master_notifica_audio
        from: "on"
        to: "off"
        id: spento
    actions:
      - choose:
          - conditions:
              - condition: template
                value_template: >-
                  {{ trigger.entity_id == 'input_boolean.vmc_master_notifica_audio'
                     and trigger.id == 'acceso' }}
            sequence:
              - action: input_boolean.turn_off
                target:
                  entity_id:
"""
    + "".join(f"                    - input_boolean.{spia}\n" for spia in SPIE)
    + """
              - action: input_boolean.toggle
                target:
                  entity_id: input_boolean.vmc_master_opzioni_accendi_spegni_avvisi
        default:
          - action: prova.registra
            data:
              chi: >-
                {{ trigger.entity_id }} {{ trigger.from_state.state }}
                {{ trigger.to_state.state }}
              utente: "{{ trigger.to_state.context.user_id is not none }}"
script:
  prova_fine:
    alias: Prova Fine
    mode: queued
    fields: {motivo: {description: Motivo}}
    sequence:
      - action: input_boolean.turn_off
        target:
          entity_id: input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0
      - delay: {seconds: 1}
      - action: prova.registra
        data:
          motivo: "{{ motivo }}"
          stato: "{{ states('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0') }}"
"""
)


def _servizio(
    nome: str, entita: str, utente: bool = False, **dati: Any
) -> tuple[Any, ...]:
    return ("servizio", nome, {"entity_id": entita, **dati}, utente)


def _numero(valore: int) -> tuple[Any, ...]:
    return _servizio("input_number.set_value", "input_number.n", value=valore)


PASSI: list[tuple[Any, ...]] = [
    # velocità 1: si spegne la spia 0, si accende la 1; dopo 1 s parte «Prova Spie»
    _numero(1),
    ("attendi", 1.5),
    # una spia cambiata da fuori: l'attesa di «Prova Spie» finisce, parte lo script
    _servizio("input_boolean.turn_off", "input_boolean.vmc_master_spia_co2_o_voc"),
    ("attendi", 2),
    # un utente accende un interruttore
    _servizio("input_boolean.turn_on", "input_boolean.vmc_master_opzioni_vmc", True),
    # velocità 2: il modello di «Prova Spie» diventa vero e lo resta 2 s
    _numero(2),
    ("attendi", 2.5),
    # un interruttore spegne tutte le spie in una chiamata e ne inverte un altro
    _servizio("input_boolean.turn_on", "input_boolean.vmc_master_notifica_audio"),
    ("attendi", 2),
    # la spia 1 si riaccende, ma ora la condizione di «Prova Spie» è falsa
    _numero(1),
    ("attendi", 1.5),
    _servizio(
        "input_boolean.turn_off", "input_boolean.vmc_master_notifica_audio", True
    ),
    _servizio("input_boolean.toggle", "input_boolean.vmc_master_opzioni_vmc"),
    ("attendi", 1),
]


class _Registro:
    """Il registro di una corsa: ogni evento con l'istante, i dati e il contesto.

    Un contesto è scritto come (numero in ordine di comparsa, numero del contesto
    genitore, c'è un utente): gli identificativi cambiano a ogni corsa, i legami no.
    Con la mappa, i nomi di domani tornano quelli di oggi.
    """

    def __init__(self, mappa: Rinomina | None) -> None:
        self.mappa = mappa
        self.voci: list[tuple[Any, ...]] = []
        self._contesti: dict[str, int] = {}

    def _contesto(self, contesto: Context) -> tuple[int, int | None, bool]:
        numero = self._contesti.setdefault(contesto.id, len(self._contesti))
        genitore = None
        if contesto.parent_id is not None:
            genitore = self._contesti.get(contesto.parent_id, -1)
        return (numero, genitore, contesto.user_id is not None)

    def _nomi(self, valore: Any) -> Any:
        if self.mappa is None:
            return valore
        if isinstance(valore, str):
            return self.mappa.indietro(valore)
        if isinstance(valore, dict):
            return {k: self._nomi(v) for k, v in valore.items()}
        if isinstance(valore, (list, tuple)):
            return type(valore)(self._nomi(v) for v in valore)
        return valore

    @callback
    def annota(self, evento: Event) -> None:
        if evento.event_type not in EVENTI:
            return
        dati = dict(evento.data)
        if evento.event_type == EVENT_STATE_CHANGED:
            dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
        dati = self._nomi(_norma(dati))
        if evento.event_type == EVENT_STATE_CHANGED:
            # ``editable`` c'è solo negli aiutanti
            dati["new_state"][2].pop("editable", None)
        elif evento.event_type == EVENT_CALL_SERVICE and self.mappa is not None:
            dati = _servizio_di_oggi(dati)
        self.voci.append(
            (
                _norma(evento.time_fired),
                evento.event_type,
                dati,
                self._contesto(evento.context),
            )
        )


def _servizio_di_oggi(dati: dict[str, Any]) -> dict[str, Any]:
    """Una chiamata a ``switch`` o a ``nativa_prova`` per un ``input_boolean`` di oggi è
    scritta come la chiamata a ``input_boolean`` (le chiamate cambiano per forza: qui si
    guarda se, nome a parte, sono le stesse)."""
    bersagli = dati["service_data"].get("entity_id", "")
    if isinstance(bersagli, list):
        bersagli = ",".join(bersagli)
    if dati["domain"] in ("switch", DOMINIO_SCRITTURA) and all(
        nome.startswith("input_boolean.") for nome in bersagli.split(",")
    ):
        return dict(dati, domain="input_boolean")
    return dati


def _raggruppa(voci: list[tuple[Any, ...]]) -> list[Any]:
    """I cambi di stato di una stessa chiamata (di fila, stesso istante e stesso
    contesto) in ordine di nome: Home Assistant li scrive nell'ordine di un insieme,
    che cambia a ogni avvio."""
    uscita: list[Any] = []
    gruppo: list[tuple[Any, ...]] = []
    for voce in [*voci, None]:
        if (
            voce is not None
            and voce[1] == EVENT_STATE_CHANGED
            and (not gruppo or (voce[0], voce[3]) == (gruppo[0][0], gruppo[0][3]))
        ):
            gruppo.append(voce)
            continue
        uscita.extend(sorted(gruppo, key=lambda v: v[2]["entity_id"]))
        gruppo = []
        if voce is not None and voce[1] == EVENT_STATE_CHANGED:
            gruppo = [voce]
        elif voce is not None:
            uscita.append(voce)
    return uscita


async def _corsa(
    freezer: FrozenDateTimeFactory,
    modo: str,
    moduli: list[str],  # noqa: F811
) -> list[Any]:
    """Una corsa della prova: ``ha`` (Home Assistant e gli aiutanti), ``motore`` (il
    motore tradotto senza mappa e gli aiutanti, come nella fase 3) o ``nativo`` (il
    motore tradotto con la mappa e le entità native)."""
    configurazione = yaml.safe_load(CONFIGURAZIONE)
    mappa = _mappa() if modo.startswith("nativo") else None
    registro = _Registro(mappa)
    freezer.move_to(T0)
    async with async_test_home_assistant() as hass:
        assert await async_setup_component(hass, "homeassistant", {})
        utente = MockUser(is_owner=True).add_to_hass(hass)
        numeri = {"input_number": configurazione["input_number"]}
        assert await async_setup_component(hass, "input_number", numeri)
        aiutanti = configurazione["input_boolean"]
        scrittura = None
        if mappa is None:
            assert await async_setup_component(
                hass, "input_boolean", {"input_boolean": aiutanti}
            )
        else:
            native = []
            for oggetto, config in aiutanti.items():
                nuova = mappa.entita[f"input_boolean.{oggetto}"]
                classe = (
                    InterruttoreNativo if nuova.startswith("switch.") else SpiaNativa
                )
                native.append(classe(nuova, config))
            await aggiungi(hass, native)
            scrittura = ScritturaNativa(hass, native, subito=modo == "nativo_subito")

        async def registra(chiamata: ServiceCall) -> None:
            """Il servizio che le prove chiamano per lasciare un segno nel registro."""

        hass.services.async_register("prova", "registra", registra)
        automazioni = configurazione["automation"]
        script = configurazione["script"]
        if modo == "ha":
            assert await async_setup_component(hass, "script", {"script": script})
            assert await async_setup_component(
                hass, "automation", {"automation": automazioni}
            )
        else:
            nome = f"prototipo_{modo}"
            testo_modelli, testo_motore = await traduci_configurazione(
                hass,
                automazioni,
                script,
                nome_modelli=f"{nome}_modelli",
                rinomina=mappa,
            )
            assert ("input_boolean." in _senza_sorgente(testo_motore)) is (
                mappa is None
            )
            moduli.append(f"{generato.__name__}.{nome}_modelli")
            moduli.append(f"{generato.__name__}.{nome}_motore")
            _carica(f"{nome}_modelli", testo_modelli)
            codice = _carica(f"{nome}_motore", testo_motore)
            m = MotoreFase3(hass)
            await m.avvia(crea=codice.crea)
        await _gira(hass)

        togli = hass.bus.async_listen(MATCH_ALL, registro.annota)
        if modo != "ha":
            # gli stati delle logiche (le automazioni del motore) non sono nella macchina
            # degli stati: entrano nel registro nel punto del bus di state_changed
            smetti = stati_logiche(hass).osserva(
                callback(
                    lambda e: registro.annota(e)
                    if e.event_type == EVENT_STATE_CHANGED
                    else None
                )
            )
        for passo in PASSI:
            if passo[0] == "attendi":
                await _avanza(hass, freezer, passo[1])
                continue
            servizio, dati = passo[1], passo[2]
            if mappa is not None and servizio.startswith("input_boolean."):
                # l'utente comanda uno switch; una spia la scrive solo chi la possiede
                nuova = mappa.entita[dati["entity_id"]]
                dati = dict(dati, entity_id=nuova)
                if nuova.startswith("switch."):
                    servizio = servizio.replace("input_boolean.", "switch.")
                else:
                    servizio = mappa.servizio(servizio)
            dominio, nome_servizio = servizio.split(".")
            contesto = Context(user_id=utente.id if passo[3] else None)
            await hass.services.async_call(
                dominio, nome_servizio, dati, blocking=True, context=contesto
            )
            await _gira(hass)
        togli()
        if scrittura is not None:
            assert scrittura.mancanti == []
        domini = ("automation", "script")
        if modo != "ha":
            smetti()
            # le logiche si fermano (non hanno automation.turn_off)
            await m.ferma()
            domini = ("script",)
        for dominio in domini:
            await hass.services.async_call(
                dominio, "turn_off", {"entity_id": "all"}, blocking=True
            )
        await _gira(hass)
        await hass.async_stop(force=True)
    return _raggruppa(registro.voci)


def _senza_sorgente(testo: str) -> str:
    """Il codice senza il testo dei modelli (``mNNNN.sorgente``) e senza i commenti."""
    return "\n".join(
        riga
        for riga in testo.splitlines()
        if ".sorgente = " not in riga and not riga.lstrip().startswith("#")
    )


def _diversi(atteso: list[Any], ottenuto: list[Any], nome: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            [repr(voce) for voce in atteso],
            [repr(voce) for voce in ottenuto],
            "home_assistant",
            nome,
            lineterm="",
            n=2,
        )
    )


def _senza_chiamate_agli_aiutanti(voci: list[Any]) -> list[Any]:
    """Il registro senza le chiamate ai servizi degli aiutanti (cambiano per forza)."""
    return [
        voce
        for voce in voci
        if not (
            voce[1] == EVENT_CALL_SERVICE
            and voce[2]["domain"] in ("input_boolean", "switch", DOMINIO_SCRITTURA)
        )
    ]


async def test_motore_con_le_entita_native_come_home_assistant(
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
) -> None:
    """Home Assistant con gli aiutanti, il motore di oggi con gli aiutanti e il motore
    con la mappa contro le entità native: stessi cambi di stato, agli stessi istanti,
    con gli stessi contesti (chi ha cambiato cosa, per conto di chi)."""
    atteso = await _corsa(freezer, "ha", moduli)
    motore = await _corsa(freezer, "motore", moduli)
    nativo = await _corsa(freezer, "nativo", moduli)

    # la prova tocca davvero quello che deve: interruttori, spie, chiamate con più
    # entità, automazioni e script partiti, un utente, i contesti figli
    tipi = [voce[1] for voce in atteso]
    assert len(atteso) == 79
    assert tipi.count(EVENT_STATE_CHANGED) == 46
    assert tipi.count(EVENT_CALL_SERVICE) == 31
    assert tipi.count("script_started") == 2
    # le automazioni partite: ogni avvio fa salire ``current`` (le logiche del motore
    # non hanno l'evento automation_triggered)
    correnti: dict[str, int] = {}
    avvii = 0
    for voce in atteso:
        if voce[1] == EVENT_STATE_CHANGED and voce[2]["entity_id"].startswith(
            "automation."
        ):
            corrente = voce[2]["new_state"][2]["current"]
            avvii += corrente > correnti.get(voce[2]["entity_id"], 0)
            correnti[voce[2]["entity_id"]] = corrente
    assert avvii == 8
    cambi = [
        voce
        for voce in atteso
        if voce[1] == EVENT_STATE_CHANGED
        and voce[2]["entity_id"].startswith("input_boolean.")
    ]
    assert len(cambi) == 21
    toccate = {voce[2]["entity_id"] for voce in cambi}
    assert {f"input_boolean.{spia}" for spia in SPIE} - toccate == set()
    assert "input_boolean.vmc_master_opzioni_accendi_spegni_avvisi" in toccate
    assert sum(voce[3][2] for voce in cambi) == 2  # cambi con l'utente
    assert sum(voce[3][1] is not None for voce in cambi) == 16  # con un genitore
    assert _senza_chiamate_agli_aiutanti(atteso) != atteso

    assert motore == atteso, _diversi(atteso, motore, "motore")
    # con le entità native, a parte i nomi, è uguale TUTTO il registro: anche le
    # chiamate ai servizi, riportate al dominio di oggi
    assert nativo == atteso, _diversi(atteso, nativo, "nativo")


async def test_piu_entita_scritte_subito_cambiano_l_ordine(
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
) -> None:
    """La differenza trovata dal prototipo. Se il motore scrive le entità di una
    chiamata con più bersagli una dopo l'altra, dentro la chiamata (la via più
    semplice), gli eventi sono gli stessi ma in un altro ordine: l'automazione che ha
    fatto la chiamata va avanti prima di quella che una delle scritture ha svegliato.
    Home Assistant scrive ogni entità in un suo compito (un giro dopo), e chi è stato
    svegliato passa prima. ``ScritturaNativa`` senza ``subito`` fa come Home Assistant
    (prova qui sopra)."""
    atteso = await _corsa(freezer, "ha", moduli)
    subito = await _corsa(freezer, "nativo_subito", moduli)
    assert sorted(map(repr, subito)) == sorted(map(repr, atteso))
    assert subito != atteso
    diversi = [
        numero
        for numero, (una, altra) in enumerate(zip(atteso, subito, strict=True))
        if una != altra
    ]
    # otto eventi di fila, tutti allo stesso istante: in Home Assistant prima lo script
    # dell'automazione svegliata, poi il resto dell'automazione che ha scritto
    assert diversi == list(range(diversi[0], diversi[0] + 8))
    assert {atteso[numero][0] for numero in diversi} == {6.0}
    assert atteso[diversi[0]][1:3] == (
        EVENT_CALL_SERVICE,
        {"domain": "script", "service": "prova_fine", "service_data": {"motivo": True}},
    )
    assert subito[diversi[0]][2]["service"] == "toggle"
