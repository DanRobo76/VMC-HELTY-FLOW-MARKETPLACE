// Fotografie della scheda «VMC Master» di oggi e di quella tradotta (vedi banco.py).
//
// node scatta.js <indirizzo> <cartella> <utente> <parola> <immagini>
// Comandi su stdin, una riga ciascuno (risposte su stdout):
//   SCENA <nome> <ora in ms> <apri|-> [<testi.json>]
//                                      ferma l'orologio delle due pagine all'ora data, apre i
//                                      riquadri <details> se richiesto e fotografa le due
//                                      schede intere, a pezzi: <nome>_oggi.png.<i>.png,
//                                      <nome>_nativa.png.<i>.png -> FATTO <pezzi> <pezzi>;
//                                      con <testi.json> ({"oggi": [...], "nativa": [...]},
//                                      espressioni regolari) scrive in <nome>_testi.json dove
//                                      ogni testo si vede in ogni pagina
//   CLICCA <oggi|nativa> chip <entità> tocca il pulsante del piè di pagina di quell'entità
//   CLICCA <oggi|nativa> nome <nome>   tocca la scheda pulsante con quel nome -> CLICCATO <n>
//   FINE                               chiude il browser
// Le immagini del repository (raw.githubusercontent.com/<IMMAGINI_REPOSITORY>/<percorso>)
// arrivano dalla cartella <immagini>, dove banco.py le estrae dal repository locale; le altre
// richieste verso fuori (icone dei marchi) sono bloccate: le due pagine le mostrano mancanti
// allo stesso modo.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const [base, cartella, utente, parola, immagini] = process.argv.slice(2);
const IMMAGINI_REPOSITORY = '/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/main/';
const LARGHEZZA = 480;
const FETTA = 3000;
const PAGINE = { oggi: '/scheda-oggi/vmc', nativa: '/scheda-nativa/vmc' };

// Tutti gli elementi (anche dentro le shadow root) che soddisfano il selettore
const PROFONDO = `(selettore) => {
  const trovati = [];
  const visita = (radice) => {
    for (const el of radice.querySelectorAll('*')) {
      if (el.matches(selettore)) trovati.push(el);
      if (el.shadowRoot) visita(el.shadowRoot);
    }
  };
  visita(document);
  return trovati;
}`;

async function quanti(pagina) {
  return pagina.evaluate(`(${PROFONDO})('*').length`);
}

// Aspetta che il numero di elementi resti fermo per tre controlli di fila
async function attendi(pagina, minimo = 2000) {
  await pagina.waitForTimeout(minimo);
  let prima = -1;
  let fermi = 0;
  for (let i = 0; i < 60 && fermi < 3; i += 1) {
    const ora = await quanti(pagina);
    fermi = ora === prima ? fermi + 1 : 0;
    prima = ora;
    await pagina.waitForTimeout(400);
  }
}

async function accedi(contesto, percorso) {
  const pagina = await contesto.newPage();
  pagina.on('console', async (m) => {
    if (!['error', 'warning'].includes(m.type())) return;
    const parti = await Promise.all(
      m.args().map((a) => a.jsonValue().then((v) => JSON.stringify(v)).catch(() => String(a))),
    );
    process.stderr.write(`[${percorso}] ${m.text()} ${parti.join(' ').slice(0, 600)}\n`);
  });
  pagina.on('requestfailed', (r) => process.stderr.write(`[${percorso}] fallita ${r.url().slice(0, 120)}\n`));
  pagina.on('response', (r) => {
    if (r.status() >= 400) process.stderr.write(`[${percorso}] ${r.status()} ${r.url().slice(0, 120)}\n`);
  });
  pagina.on('pageerror', (e) => process.stderr.write(`[${percorso}] ${e}\n`));
  await pagina.goto(`${base}/`, { waitUntil: 'networkidle' });
  if (new URL(pagina.url()).pathname.startsWith('/auth')) {
    // la seconda pagina trova già i gettoni salvati dalla prima
    await pagina.fill('input[name="username"]', utente);
    await pagina.fill('input[name="password"]', parola);
    await pagina.keyboard.press('Enter');
    await pagina.waitForFunction(() => !location.pathname.startsWith('/auth'), null, { timeout: 60000 });
    await pagina.waitForTimeout(1500);
  }
  await pagina.goto(`${base}${percorso}`, { waitUntil: 'networkidle' });
  await attendi(pagina, 4000);
  return pagina;
}

// Altezza della pagina: il fondo dell'ultima scheda della vista
async function altezza(pagina) {
  return pagina.evaluate(`(() => {
    const viste = (${PROFONDO})('hui-view, hui-masonry-view');
    let fondo = document.documentElement.scrollHeight;
    for (const v of viste) {
      const r = v.getBoundingClientRect();
      fondo = Math.max(fondo, r.top + window.scrollY + v.scrollHeight);
    }
    for (const c of (${PROFONDO})('ha-card')) {
      const r = c.getBoundingClientRect();
      if (r.height > 0) fondo = Math.max(fondo, r.bottom + window.scrollY);
    }
    return Math.ceil(fondo + 16);
  })()`);
}

// Dove si vedono i testi (espressioni regolari) nella pagina: per ogni testo i rettangoli
// [sopra, sotto, sinistra, destra] in px CSS. Il testo di ogni radice (documento e shadow
// root) è letto di fila, con gli spazi ridotti a uno come li mostra il browser.
const TROVA = `(sorgenti) => {
  const radici = [document];
  const visita = (radice) => {
    for (const el of radice.querySelectorAll('*')) {
      if (el.shadowRoot) {
        radici.push(el.shadowRoot);
        visita(el.shadowRoot);
      }
    }
  };
  visita(document);
  const esiti = sorgenti.map(() => []);
  for (const radice of radici) {
    const camminatore = document.createTreeWalker(radice, NodeFilter.SHOW_TEXT);
    let testo = '';
    const posti = [];
    let spazio = true;
    for (let nodo = camminatore.nextNode(); nodo; nodo = camminatore.nextNode()) {
      if (nodo.parentElement && nodo.parentElement.closest('script, style')) continue;
      for (let k = 0; k < nodo.data.length; k += 1) {
        const c = /\\s/.test(nodo.data[k]) ? ' ' : nodo.data[k];
        if (c === ' ' && spazio) continue;
        spazio = c === ' ';
        testo += c;
        posti.push([nodo, k]);
      }
    }
    sorgenti.forEach((sorgente, i) => {
      for (const trovato of testo.matchAll(new RegExp(sorgente, 'g'))) {
        if (!trovato[0].length) continue;
        const [n1, o1] = posti[trovato.index];
        const [n2, o2] = posti[trovato.index + trovato[0].length - 1];
        const intervallo = document.createRange();
        intervallo.setStart(n1, o1);
        intervallo.setEnd(n2, o2 + 1);
        const r = intervallo.getBoundingClientRect();
        if (r.height > 0 && r.width > 0) {
          esiti[i].push([r.top + window.scrollY, r.bottom + window.scrollY, r.left, r.right]);
        }
      }
    });
  }
  return esiti;
}`;

// Aspetta che ogni immagine visibile sia caricata (o fallita): l'altezza dipende da loro
async function immaginiPronte(pagina) {
  for (let i = 0; i < 50; i += 1) {
    const inAttesa = await pagina.evaluate(
      `(${PROFONDO})('img').filter((el) => !el.complete).length`,
    );
    if (inAttesa === 0) return;
    await pagina.waitForTimeout(200);
  }
  process.stderr.write('immagini non caricate entro 10 s\n');
}

async function fotografa(pagina, file, sorgenti) {
  let h = 0;
  for (let i = 0; i < 6; i += 1) {
    await immaginiPronte(pagina);
    const nuova = await altezza(pagina);
    if (nuova === h) break;
    h = nuova;
    await pagina.setViewportSize({ width: LARGHEZZA, height: h });
    await pagina.waitForTimeout(700);
  }
  await immaginiPronte(pagina);
  await pagina.evaluate(() => window.scrollTo(0, 0));
  // i testi si cercano con la pagina grande come nella fotografia
  const testi = sorgenti ? await pagina.evaluate(`(${TROVA})(${JSON.stringify(sorgenti)})`) : null;
  // a pezzi di FETTA px: le fotografie molto alte in un colpo solo restano in parte bianche
  let pezzi = 0;
  for (let y = 0; y < h; y += FETTA) {
    await pagina.screenshot({
      path: `${file}.${pezzi}.png`,
      clip: { x: 0, y, width: LARGHEZZA, height: Math.min(FETTA, h - y) },
      animations: 'disabled',
      caret: 'hide',
    });
    pezzi += 1;
  }
  await pagina.setViewportSize({ width: LARGHEZZA, height: 900 });
  return { pezzi, testi };
}

async function apriDettagli(pagina) {
  return pagina.evaluate(`(() => {
    const tutti = (${PROFONDO})('details');
    for (const d of tutti) d.open = true;
    return tutti.length;
  })()`);
}

async function clicca(pagina, tipo, valore) {
  const maniglia = await pagina.evaluateHandle(
    ([profondo, t, v]) => {
      const trova = eval(profondo);
      const visibile = (el) => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      };
      if (t === 'chip') {
        return trova('ha-assist-chip').filter((el) => el.config && el.config.entity === v && visibile(el));
      }
      return trova('hui-button-card')
        .filter((el) => el._config && el._config.name === v && visibile(el))
        .map((el) => el.shadowRoot.querySelector('ha-card'));
    },
    [PROFONDO, tipo, valore],
  );
  const n = await maniglia.evaluate((elenco) => elenco.length);
  if (n > 0) {
    const primo = await maniglia.evaluateHandle((elenco) => elenco[0]);
    await primo.asElement().click();
  }
  return n;
}

(async () => {
  // le intestazioni sono WebP animate: il fotogramma visibile dipenderebbe dall'istante dello
  // scatto, così ogni immagine animata resta ferma sul primo fotogramma in tutte e due le pagine
  const browser = await chromium.launch({ args: ['--blink-settings=imageAnimationPolicy=2'] });
  const contesto = await browser.newContext({
    viewport: { width: LARGHEZZA, height: 900 },
    deviceScaleFactor: 2,
    locale: 'it-IT',
    timezoneId: 'Europe/Rome',
  });
  await contesto.addInitScript(() => {
    try {
      localStorage.setItem('selectedLanguage', '"it"');
      localStorage.setItem('dockedSidebar', '"always_hidden"');
      localStorage.setItem('selectedTheme', '{"theme":"default","dark":false}');
    } catch (e) {
      // pagina senza localStorage
    }
  });
  await contesto.route('**/*', (richiesta) => {
    const indirizzo = new URL(richiesta.request().url());
    if (['127.0.0.1', 'localhost'].includes(indirizzo.hostname) || indirizzo.protocol === 'data:') {
      return richiesta.continue();
    }
    if (indirizzo.hostname === 'raw.githubusercontent.com' && indirizzo.pathname.startsWith(IMMAGINI_REPOSITORY)) {
      const relativo = decodeURIComponent(indirizzo.pathname.slice(IMMAGINI_REPOSITORY.length));
      const file = path.join(immagini, relativo);
      if (file.startsWith(immagini + path.sep) && fs.existsSync(file)) {
        return richiesta.fulfill({ path: file });
      }
      process.stderr.write(`immagine assente in ${immagini}: ${relativo}\n`);
    }
    return richiesta.abort();
  });
  const pagine = {};
  for (const [nome, percorso] of Object.entries(PAGINE)) {
    pagine[nome] = await accedi(contesto, percorso);
    await pagine[nome].screenshot({ path: `${cartella}/_accesso_${nome}.png` });
  }
  console.log('PRONTO');
  const righe = readline.createInterface({ input: process.stdin });
  for await (const riga of righe) {
    const [comando, ...resto] = riga.trim().split(' ');
    if (comando === 'FINE') break;
    if (comando === 'SCENA') {
      const [nome, ora, apri, cerca] = resto;
      const sorgenti = cerca ? JSON.parse(fs.readFileSync(cerca, 'utf-8')) : {};
      const pezzi = {};
      const testi = {};
      for (const pagina of Object.values(pagine)) {
        await pagina.clock.setFixedTime(new Date(Number(ora)));
      }
      await Promise.all(Object.values(pagine).map((pagina) => attendi(pagina, 2500)));
      for (const [quale, pagina] of Object.entries(pagine)) {
        if (apri === 'apri') {
          await apriDettagli(pagina);
          await pagina.waitForTimeout(800);
        }
        const esito = await fotografa(pagina, `${cartella}/${nome}_${quale}.png`, sorgenti[quale]);
        pezzi[quale] = esito.pezzi;
        testi[quale] = esito.testi;
      }
      if (cerca) fs.writeFileSync(`${cartella}/${nome}_testi.json`, JSON.stringify(testi));
      console.log(`FATTO ${nome} ${pezzi.oggi} ${pezzi.nativa}`);
    } else if (comando === 'CLICCA') {
      const [quale, tipo, ...valore] = resto;
      const n = await clicca(pagine[quale], tipo, valore.join(' '));
      console.log(`CLICCATO ${n}`);
    } else {
      console.log(`SCONOSCIUTO ${riga}`);
    }
  }
  await browser.close();
  process.exit(0);
})().catch((errore) => {
  console.error(errore);
  process.exit(1);
});
