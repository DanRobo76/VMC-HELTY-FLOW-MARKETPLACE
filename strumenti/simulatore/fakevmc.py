"""VMC finta: velocita', corrente, comandi (shell_command con nc), letture TCP e ping.

Ogni voce del registro della VMC (self.log) e ogni comando di shell eseguito vanno anche nella
traccia dello scenario (EVENTI, una lista impostata dal runner con tracce.TR.ev), nello stesso
ordine in cui accadono rispetto ai cambi di stato e alle chiamate di servizio.
"""
import asyncio, re, time
import vclock
CMD_RE = re.compile(r"VMWH(\d{7})")
EVENTI = None   # lista della traccia (tracce.Traccia.ev) o None

def _registra(voce, tipo='V'):
    if EVENTI is not None: EVENTI.append([tipo, voce[0]] + list(voce[1:]))
class FakeVMC:
    def __init__(self):
        self.speed = 1; self.online = True; self.latency = 0.5
        self.log = []   # (t, kind, value, source)
        self.sens = dict(t_int=210, t_ext=100, rh=500, co2=600, voc=50)  # VMGI raw (tenths)
        self.leds = '00000'; self.pending = []
        self.loop = None; self.user_cmd = False; self.resume = False; self.voc_dirty = False; self.on_voc_dirty = None; self.mute = False
    def status_str(self):
        return f"VMGO,{self.speed:05d},00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000"
    def sensori_str(self):
        s = self.sens
        return f"VMGI,{s['t_int']:05d},{s['t_ext']:05d},{s['rh']:05d},{s['co2']:05d},00000,00000,00000,00000,00000,00000,{s['voc']:05d},00000,00000,00000"
    def _log(self, voce):
        self.log.append(voce); _registra(voce)
    def set_speed(self, v, source):
        if not self.online: return
        old = self.speed; self.speed = v
        self._log((vclock._V[0], 'speed', v, source, old))
    def power(self, on):
        t = vclock._V[0]
        if on and not self.online:
            self.online = True
            old = self.speed
            if self.speed != 0 and not self.resume: self.speed = 1   # modello base: dopo un Black-Out la VMC riparte a Velocita' 1 (se non era ferma); modello R: riparte alla velocita' di prima
            self._log((t, 'speed', self.speed, 'power_on', old))
            if self.voc_dirty and self.loop: self.loop.call_soon(self.on_voc_dirty)
        elif not on and self.online:
            self.online = False
            self._log((t, 'power', 'off', 'power_off', self.speed))
    def command(self, code):
        t = vclock._V[0]
        src = 'user' if self.user_cmd else 'ha'; self.user_cmd = False
        self._log((t, 'cmd', code, src, self.speed))
        if not self.online or self.mute: return False
        grp = code[:3]; val = int(code[3:])
        if grp == '000':
            self.loop.call_later(self.latency, self.set_speed, val, 'cmd_'+src)
        return True
    def _apply(self, val):
        self.set_speed(val, 'cmd')
VMC = FakeVMC()

class FakeProc:
    def __init__(self, out=b'', rc=0, delay=0.05):
        self._out = out; self.returncode = None; self._rc = rc; self._delay = delay; self.pid = 1
    async def communicate(self, input=None):
        await asyncio.sleep(self._delay)
        self.returncode = self._rc
        return self._out, b''
    async def wait(self):
        await asyncio.sleep(self._delay); self.returncode = self._rc; return self._rc
    def kill(self): pass
    def terminate(self): pass

async def fake_shell(cmd, *a, **k):
    return _handle(cmd if isinstance(cmd, str) else ' '.join(cmd))
async def fake_exec(*args, **k):
    return _handle(' '.join(str(x) for x in args))
SHELL_LOG = []
def _handle(cmd):
    SHELL_LOG.append((vclock._V[0], cmd)); _registra((vclock._V[0], cmd), 'X')
    if 'ping' in cmd:
        return FakeProc(b'ON-Line\n' if VMC.online else b'OFF-Line\n', 0, 0.05 if VMC.online else 4.0)
    m = CMD_RE.search(cmd)
    if m:
        ok = VMC.command(m.group(1))
        return FakeProc(b'', 0 if ok else 1, 0.05 if ok else 3.0)
    return FakeProc(b'', 0, 0.01)

def tcp_update(self):
    p = self._config['payload']
    if not VMC.online or VMC.mute:
        self._attr_available = False; return
    self._attr_available = True
    if p.startswith('VMGH'): v = VMC.status_str()
    elif p.startswith('VMGI'): v = VMC.sensori_str()
    elif p.startswith('VMNM'): v = 'VMNM Master'
    elif p.startswith('VMSL'): v = 'VMSL,192,168,1,160'
    else: v = ''
    self._state = v

def install():
    asyncio.create_subprocess_shell = fake_shell
    asyncio.create_subprocess_exec = fake_exec
    from homeassistant.components.tcp import entity as tcpe
    tcpe.TcpEntity.update = tcp_update
