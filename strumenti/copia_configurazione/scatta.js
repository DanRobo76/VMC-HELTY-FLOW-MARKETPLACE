// Fotografie delle viste della plancia «Panoramica» della casa di prova (vedi banco.py).
//
// node scatta.js <indirizzo> <utente> <parola> <cartella> <vista> [<vista> ...]
//
// Per ogni vista (percorso della plancia, es. «vmc-master») accede come l'utente, apre
// /lovelace/<vista>, aspetta che la pagina smetta di cambiare, conta gli avvisi della
// plancia (hui-warning: «Entità non disponibile: …», «L'entità non è attualmente
// disponibile: …»), le schede in errore (hui-error-card) e il messaggio della scheda VMC
// Master «Scheda VMC Master non disponibile», poi fotografa la vista intera a pezzi
// (<cartella>/<vista>.<i>.png, deviceScaleFactor 1). Stampa su stdout una riga JSON per
// vista. Le richieste verso fuori (immagini della scheda su GitHub) sono bloccate: nello
// spazio di rete del banco non c'è internet.
const { chromium } = require('playwright');

const [base, utente, parola, cartella, ...viste] = process.argv.slice(2);
const LARGHEZZA = 480;
const FETTA = 3000;

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

// Testi visibili di tutte le radici (documento e shadow root), per cercare i messaggi
const TESTI = `(() => {
  const radici = [document];
  const visita = (radice) => {
    for (const el of radice.querySelectorAll('*')) {
      if (el.shadowRoot) { radici.push(el.shadowRoot); visita(el.shadowRoot); }
    }
  };
  visita(document);
  const testi = [];
  for (const radice of radici) {
    const camminatore = document.createTreeWalker(radice, NodeFilter.SHOW_TEXT);
    for (let n = camminatore.nextNode(); n; n = camminatore.nextNode()) {
      if (n.parentElement && n.parentElement.closest('script, style')) continue;
      const t = n.data.replace(/\\s+/g, ' ').trim();
      if (t) testi.push(t);
    }
  }
  return testi;
})()`;

async function quanti(pagina) {
  return pagina.evaluate(`(${PROFONDO})('*').length`);
}

async function attendi(pagina, minimo) {
  await pagina.waitForTimeout(minimo);
  let prima = -1;
  let fermi = 0;
  for (let i = 0; i < 60 && fermi < 3; i += 1) {
    const ora = await quanti(pagina);
    fermi = ora === prima ? fermi + 1 : 0;
    prima = ora;
    await pagina.waitForTimeout(500);
  }
}

async function altezza(pagina) {
  return pagina.evaluate(`(() => {
    let fondo = document.documentElement.scrollHeight;
    for (const c of (${PROFONDO})('ha-card, hui-view, hui-masonry-view')) {
      const r = c.getBoundingClientRect();
      if (r.height > 0) fondo = Math.max(fondo, r.bottom + window.scrollY);
    }
    return Math.ceil(fondo + 16);
  })()`);
}

async function esamina(pagina) {
  return pagina.evaluate(`(() => {
    const trova = ${PROFONDO};
    const avvisi = trova('hui-warning').map((el) => (el.textContent || '').replace(/\\s+/g, ' ').trim());
    const errori = trova('hui-error-card').map((el) => {
      const c = el._config || el.config || {};
      return JSON.stringify(c.error || c).slice(0, 300);
    });
    return { avvisi, errori, schede_vmc: trova('vmc-master-card').length, ha_card: trova('ha-card').length };
  })()`);
}

(async () => {
  const browser = await chromium.launch({ args: ['--blink-settings=imageAnimationPolicy=2'] });
  const contesto = await browser.newContext({
    viewport: { width: LARGHEZZA, height: 900 },
    deviceScaleFactor: 1,
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
  // Niente rete fuori dalla casa di prova: gli indirizzi esterni (immagini, caratteri)
  // falliscono e si annotano per vista
  const bloccati = new Set();
  await contesto.route('**/*', (richiesta) => {
    const indirizzo = new URL(richiesta.request().url());
    if (['127.0.0.1', 'localhost'].includes(indirizzo.hostname) || indirizzo.protocol === 'data:') {
      return richiesta.continue();
    }
    bloccati.add(`${indirizzo.origin}${indirizzo.pathname}`.slice(0, 200));
    return richiesta.abort();
  });
  const pagina = await contesto.newPage();
  const console_ = [];
  pagina.on('console', (m) => {
    if (['error', 'warning'].includes(m.type())) console_.push(`${m.type()}: ${m.text().slice(0, 300)}`);
  });
  pagina.on('pageerror', (e) => console_.push(`pageerror: ${String(e).slice(0, 300)}`));
  await pagina.goto(`${base}/`, { waitUntil: 'networkidle' });
  if (new URL(pagina.url()).pathname.startsWith('/auth')) {
    await pagina.fill('input[name="username"]', utente);
    await pagina.fill('input[name="password"]', parola);
    await pagina.keyboard.press('Enter');
    await pagina.waitForFunction(() => !location.pathname.startsWith('/auth'), null, { timeout: 60000 });
    await pagina.waitForTimeout(1500);
  }
  for (const vista of viste) {
    console_.length = 0;
    bloccati.clear();
    await pagina.setViewportSize({ width: LARGHEZZA, height: 900 });
    await pagina.goto(`${base}/lovelace/${vista}`, { waitUntil: 'networkidle' });
    await attendi(pagina, 4000);
    let h = 0;
    for (let i = 0; i < 6; i += 1) {
      const nuova = await altezza(pagina);
      if (nuova === h) break;
      h = nuova;
      await pagina.setViewportSize({ width: LARGHEZZA, height: Math.min(h, 30000) });
      await pagina.waitForTimeout(800);
    }
    await attendi(pagina, 1500);
    const esito = await esamina(pagina);
    const testi = await pagina.evaluate(TESTI);
    esito.messaggi_scheda = testi.filter((t) => /Scheda VMC Master non disponibile|non disponibile:|non è attualmente disponibile/.test(t));
    await pagina.evaluate(() => window.scrollTo(0, 0));
    let pezzi = 0;
    for (let y = 0; y < h; y += FETTA) {
      await pagina.screenshot({
        path: `${cartella}/${vista}.${pezzi}.png`,
        clip: { x: 0, y, width: LARGHEZZA, height: Math.min(FETTA, h - y) },
        animations: 'disabled',
        caret: 'hide',
      });
      pezzi += 1;
    }
    esito.vista = vista;
    esito.pezzi = pezzi;
    esito.altezza = h;
    esito.console = console_.slice(0, 40);
    esito.bloccati = [...bloccati].slice(0, 40);
    console.log(JSON.stringify(esito));
  }
  await browser.close();
  process.exit(0);
})().catch((errore) => {
  console.error(errore);
  process.exit(1);
});
