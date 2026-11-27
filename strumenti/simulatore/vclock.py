"""Orologio virtuale: va importato PRIMA di qualsiasi modulo di homeassistant.

time.time / time.monotonic (e le versioni _ns), dt_util.utcnow / dt_util.now e loop.time() leggono il
tempo virtuale _V; il ciclo (VLoop) salta in avanti fino al prossimo timer quando non ha niente da fare.

Rispetto alla b36, per avere giri ripetibili e confrontabili (differenziale.py):
- il salto porta _V esattamente all'istante del timer (_V = when), non a _V + (when - _V): con la somma
  l'errore di arrotondamento dipendeva da quali istanti intermedi il ciclo aveva visitato, e una variante
  con un timer in piu' (per esempio un motore che si sveglia a un istante in piu') spostava di qualche
  1e-16 tutti gli istanti seguenti, quindi i microsecondi di utcnow() e l'ordine dei timer quasi uguali;
- istanti dei timer sulla griglia del microsecondo (al microsecondo successivo) e ordine dei timer per
  istante e, a parita', in ordine di registrazione (TimerOrdinato). Con il confronto di asyncio (solo l'istante, heap non stabile) due timer allo stesso
  istante virtuale (frequente: l'orologio virtuale non ha il rumore di quello reale) uscivano in un ordine
  che dipendeva dalla storia dello heap, cioe' da tutti gli altri timer registrati e annullati: bastava un
  timer in piu' in una variante per cambiare l'ordine di due eventi che non lo riguardano.
"""
import os, math, time, datetime as _dt, asyncio, selectors, heapq, itertools
TIMER_B36 = os.environ.get('SIM_TIMER') == 'b36'   # solo per provare che i timer della b36 danno giri non confrontabili
START_EPOCH = [_dt.datetime(2026, 1, 15, 9, 0, 0, tzinfo=_dt.timezone.utc).timestamp()]
_V = [0.0]          # virtual monotonic seconds
_real_time = time.time; _real_mono = time.monotonic
def vtime(): return START_EPOCH[0] + _V[0]
def vmono(): return _V[0]
def vtime_ns(): return int(vtime()*1e9)
def vmono_ns(): return int(_V[0]*1e9)
time.time = vtime; time.monotonic = vmono; time.time_ns = vtime_ns; time.monotonic_ns = vmono_ns
import homeassistant.util.dt as dt_util
UTC = _dt.timezone.utc
def utcnow(): return _dt.datetime.fromtimestamp(vtime(), UTC)
def now(time_zone=None): return _dt.datetime.fromtimestamp(vtime(), time_zone or dt_util.DEFAULT_TIME_ZONE)
dt_util.utcnow = utcnow; dt_util.now = now

_SEQ = itertools.count()


def quantizza(when):
    """Istante portato al microsecondo successivo (mai prima di when: un timer che scatta anche di poco
    prima del previsto viene riarmato da Home Assistant, _TrackPointUTCTime)."""
    n = math.ceil(when * 1e6)
    q = n / 1e6
    if q < when:
        q = (n + 1) / 1e6
    return q


class TimerOrdinato(asyncio.TimerHandle):
    """TimerHandle con istante sulla griglia del microsecondo e ordine totale (istante, numero di registrazione).
    L'istante stesso e' quantizzato (non solo la chiave di ordinamento): asyncio._run_once toglie dallo heap i
    timer scaduti finche' trova un istante >= ora, e con istanti diversi entro lo stesso microsecondo un timer
    estraneo (anche annullato) registrato prima poteva fermare l'estrazione e rimandare al giro dopo un timer
    dello stesso istante (osservato con varianti/prova_timer.py)."""
    __slots__ = ('_chiave',)

    def __init__(self, when, callback, args, loop, context=None):
        when = quantizza(when)
        super().__init__(when, callback, args, loop, context)
        self._chiave = (when, next(_SEQ))

    def __lt__(self, other):
        if isinstance(other, TimerOrdinato):
            return self._chiave < other._chiave
        return super().__lt__(other)

    def __gt__(self, other):
        if isinstance(other, TimerOrdinato):
            return self._chiave > other._chiave
        return super().__gt__(other)

    __hash__ = asyncio.TimerHandle.__hash__


class VSelector:
    def __init__(self, loop, sel):
        self.loop = loop; self.sel = sel
    def __getattr__(self, k): return getattr(self.sel, k)
    def register(self, *a, **k): return self.sel.register(*a, **k)
    def unregister(self, *a, **k): return self.sel.unregister(*a, **k)
    def modify(self, *a, **k): return self.sel.modify(*a, **k)
    def select(self, timeout=None):
        if self.loop.pending_exec > 0 or self.loop.realtime:
            t = 0.02 if timeout is None else min(timeout, 0.02)
            ev = self.sel.select(t)
            if not ev and self.loop.pending_exec == 0 and not self.loop.realtime and timeout:
                pass
            return ev
        ev = self.sel.select(0)
        if ev: return ev
        if timeout is None:
            return self.sel.select(0.01)
        if timeout > 0 and TIMER_B36:
            _V[0] += timeout; self.loop.jumps += 1
        elif timeout > 0:
            # timeout = when del primo timer - _V (asyncio._run_once): si salta esattamente a when
            sched = self.loop._scheduled
            dest = sched[0]._when if sched else _V[0] + timeout
            if not (dest > _V[0]) or dest - _V[0] > timeout + 1e-6:   # limite di asyncio (24 h) o caso strano
                dest = _V[0] + timeout
            _V[0] = dest
            self.loop.jumps += 1
        return []

class VLoop(asyncio.SelectorEventLoop):
    def __init__(self):
        super().__init__()
        self.pending_exec = 0; self.realtime = False; self.jumps = 0
        self._selector = VSelector(self, self._selector)
    def time(self): return _V[0]
    def call_at(self, when, callback, *args, context=None):
        # come asyncio.BaseEventLoop.call_at, con TimerOrdinato
        if when is None:
            raise TypeError("when cannot be None")
        self._check_closed()
        if self._debug:
            self._check_thread()
            self._check_callback(callback, 'call_at')
        timer = (asyncio.TimerHandle if TIMER_B36 else TimerOrdinato)(when, callback, args, self, context)
        if timer._source_traceback:
            del timer._source_traceback[-1]
        heapq.heappush(self._scheduled, timer)
        timer._scheduled = True
        return timer
    def run_in_executor(self, executor, func, *args):
        fut = super().run_in_executor(executor, func, *args)
        self.pending_exec += 1
        def done(_f): self.pending_exec -= 1
        fut.add_done_callback(done)
        return fut
