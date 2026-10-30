/* Desktop ↔ phone parity check.
   Every beat is opened on a desktop (1920×1080, mouse) and on a phone (iPhone 13 landscape, touch → LITE, low tier),
   and the user-visible features are compared: subtitles, the now-playing card, the ∞ switch, MV switches and the
   MV question, overlays and particles, 3D entrances, tappable pieces, running animations, photo slots.
   A phone may draw things cheaper (fewer particles, smaller canvases); it may not lose any of them.

   usage:  node tests/parity.js [http://localhost:8000/index.html] [from] [to]
   exit code 1 when a feature exists on the desktop and not on the phone. */
const { chromium, devices } = require('playwright');
const URL = process.argv[2] || 'http://localhost:8000/index.html';
const FROM = +(process.argv[3] || 0), TO = +(process.argv[4] || 999);

const snap = () => {
  const st = document.querySelector('#stage'), sc = document.querySelector('.scene.active');
  const vis = (e) => { if (!e) return false; const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false; for (let x = e; x && x !== document.body; x = x.parentElement) { const cs = getComputedStyle(x); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < .05) return false; } return true; };
  const shown = (sel) => [...document.querySelectorAll(sel)].filter(vis).length;
  const f = {};
  f.subtitles = vis(document.querySelector('#capt.on'));
  f.nowPlaying = vis(document.querySelector('.np.on'));
  f.autoSwitch = vis(document.querySelector('#autobtn'));
  f.mvSwitches = sc ? [...sc.querySelectorAll('.mvs')].filter(vis).map(b => b.dataset.work).sort().join(',') : '';
  f.mvQuestion = vis(document.querySelector('#mvask.on'));
  f.particles = (() => { const c = document.querySelector('#fx'); return !!c && getComputedStyle(c).display !== 'none'; })();
  f.grain = (() => { const g = document.querySelector('#grain'); return !!g && getComputedStyle(g).display !== 'none'; })();
  f.overlays = [...document.querySelectorAll('#overlays .ov')].filter(o => getComputedStyle(o).display !== 'none' && +getComputedStyle(o).opacity > .01).map(o => o.id).sort().join(',');
  f.grade = (() => { const g = document.querySelector('#grade'); return !!g && getComputedStyle(g).display !== 'none'; })();
  f.card3d = (() => { const c = document.querySelector('.rv.card3d:not(.on)'); return c ? getComputedStyle(c).transform !== 'none' : null; })();
  f.flip3d = (() => { const c = document.querySelector('.rv.flip3d:not(.on)'); return c ? getComputedStyle(c).transform !== 'none' : null; })();
  f.tappable = sc ? [...sc.querySelectorAll('.int, .drag, .mvs')].filter(e => vis(e) && getComputedStyle(e).pointerEvents !== 'none').length : 0;
  f.photos = shown('.scene.active .photo-w:not(.nophoto), .scene.active .hero:not(.nophoto)');
  f.photoToned = (() => { const i = document.querySelector('.scene.active .hero img'); return i ? getComputedStyle(i).filter !== 'none' : null; })();
  f.figures = shown('.scene.active .fig');
  f.texts = sc ? [...sc.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !e.closest('svg') && vis(e)).length : 0;
  f.cssAnimations = document.getAnimations().filter(a => a.playState === 'running' && a.animationName && sc && a.effect && a.effect.target && sc.contains(a.effect.target)).map(a => a.animationName).filter((v, i, s) => s.indexOf(v) === i).sort().join(',');
  return f;
};

(async () => {
  const browser = await chromium.launch(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } } : {});
  const open = async (ctxOpt, qs = '') => {
    const ctx = await browser.newContext(ctxOpt); const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    await page.goto(URL + qs); await page.evaluate(() => { localStorage.clear(); localStorage.setItem('bts.settings', JSON.stringify({ rate: 7, lang: 'ko' })); });
    await page.reload(); await page.waitForTimeout(2500); return { page, errs };
  };
  /* the desktop at its best (a slow test machine would otherwise lower its own tier); the phone as it decides for itself */
  const D = await open({ viewport: { width: 1920, height: 1080 } }, (URL.includes('?') ? '&' : '?') + 'q=high');
  const P = await open({ ...devices['iPhone 13 landscape'] });
  const n = Math.min(TO, await D.page.evaluate(() => BTS.BEATS.length));
  const fails = [];
  for (let b = FROM; b < n; b++) {
    const go = (p) => p.evaluate((b) => BTS.Director.go(b, 'jump'), b);
    await Promise.all([go(D.page), go(P.page)]);
    await Promise.all([D.page.waitForTimeout(4200), P.page.waitForTimeout(4200)]);
    const [d, p] = await Promise.all([D.page.evaluate(snap), P.page.evaluate(snap)]);
    const key = await D.page.evaluate(() => { const x = BTS.BEATS[BTS.Director.beat]; return BTS.SCENES[x.scene].key + '-' + x.local; });
    const diff = [];
    for (const k of Object.keys(d)) {
      const a = d[k], c = p[k];
      if (a === c || a === null || c === null) continue;
      if (typeof a === 'boolean') { if (a && !c) diff.push(`${k}: desktop yes, phone NO`); continue; }
      if (typeof a === 'number') { if (c < a) diff.push(`${k}: desktop ${a}, phone ${c}`); continue; }
      const A = a ? a.split(',') : [], C = c ? c.split(',') : [];
      const miss = A.filter(x => !C.includes(x));
      if (miss.length) diff.push(`${k}: phone lacks ${miss.join(' ')}`);
    }
    if (diff.length) { fails.push([b, key, diff]); console.log(`#${b} ${key}\n   ` + diff.join('\n   ')); }
  }
  const errs = [...D.errs.map(e => 'desktop: ' + e), ...P.errs.map(e => 'phone: ' + e)];
  if (errs.length) console.log('page errors:', errs.slice(0, 6));
  console.log(fails.length ? `\n✗ ${fails.length} beat(s) differ` : '\n✓ desktop and phone show the same features on every beat');
  await browser.close();
  process.exit(fails.length || errs.length ? 1 : 0);
})();
