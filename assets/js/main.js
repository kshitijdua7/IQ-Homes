/* ==========================================================================
   IQ Homes — site behaviour
   Plain ES module, no dependencies.
   ========================================================================== */

/* ---------- Mobile nav --------------------------------------------------- */
function initNav() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (!toggle || !nav) return;

  const close = () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.style.removeProperty('overflow');
  };

  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    if (open) return close();
    nav.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    if (window.matchMedia('(max-width: 960px)').matches) {
      document.body.style.overflow = 'hidden';
    }
  });

  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 960) close();
  });
}

/* ---------- Sticky header state ------------------------------------------ */
function initHeader() {
  const header = document.querySelector('[data-header]');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-stuck', window.scrollY > 12);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ---------- Reveal on scroll --------------------------------------------- */
function initReveal() {
  const items = document.querySelectorAll('.reveal');
  if (!items.length) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
      !('IntersectionObserver' in window)) {
    items.forEach(el => el.classList.add('is-in'));
    return;
  }

  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      obs.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  items.forEach(el => io.observe(el));
}

/* ---------- FAQ accordion ------------------------------------------------ */
function initFaq() {
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      item.classList.toggle('is-open', !open);
    });
  });
}

/* ---------- Before / after slider ---------------------------------------- */
function initBeforeAfter() {
  document.querySelectorAll('.ba').forEach(ba => {
    const range = ba.querySelector('.ba-range');
    if (!range) return;
    const apply = () => ba.style.setProperty('--pos', range.value + '%');
    range.addEventListener('input', apply);
    apply();
  });
}

/* ---------- Service-area checker ----------------------------------------- */
/* The whole GTA: the City of Toronto plus Peel, York, Durham and Halton.
   Neighbourhood names are included because that's how people actually
   describe where they live — nobody types "City of Toronto". */
const COVERED = [
  // City of Toronto + its neighbourhoods
  'toronto', 'north york', 'scarborough', 'etobicoke', 'east york', 'york',
  'downtown', 'midtown', 'the beaches', 'beaches', 'leaside', 'don mills',
  'willowdale', 'agincourt', 'rexdale', 'weston', 'forest hill', 'rosedale',
  'liberty village', 'the annex', 'annex', 'high park', 'roncesvalles',
  // Peel
  'mississauga', 'port credit', 'streetsville', 'meadowvale', 'erin mills',
  'churchill meadows', 'clarkson', 'lorne park', 'malton', 'cooksville',
  'brampton', 'bramalea', 'heart lake', 'springdale', 'castlemore',
  'mount pleasant', 'caledon', 'bolton', 'caledon east',
  // York
  'vaughan', 'woodbridge', 'maple', 'thornhill', 'concord', 'kleinburg',
  'markham', 'unionville', 'cornell', 'milliken', 'berczy', 'angus glen',
  'richmond hill', 'oak ridges', 'newmarket', 'aurora', 'king city', 'king',
  'whitchurch-stouffville', 'stouffville', 'east gwillimbury', 'holland landing',
  'sharon', 'mount albert', 'georgina', 'keswick', 'sutton', 'jacksons point',
  // Durham
  'pickering', 'ajax', 'whitby', 'brooklin', 'oshawa', 'clarington',
  'bowmanville', 'courtice', 'newcastle', 'uxbridge', 'scugog', 'port perry',
  'brock', 'beaverton', 'cannington', 'sunderland',
  // Halton
  'oakville', 'bronte', 'glen abbey', 'burlington', 'aldershot', 'milton',
  'halton hills', 'georgetown', 'acton'
];

/* Genuinely outside the GTA — we'll travel for these case by case. */
const NEARBY = [
  'hamilton', 'stoney creek', 'dundas', 'ancaster', 'waterdown',
  'barrie', 'innisfil', 'bradford', 'alliston', 'orillia',
  'guelph', 'kitchener', 'waterloo', 'cambridge', 'orangeville', 'shelburne',
  'st. catharines', 'st catharines', 'niagara falls', 'welland', 'grimsby',
  'peterborough', 'cobourg', 'port hope', 'lindsay', 'brantford'
];

function initChecker() {
  const form = document.querySelector('[data-checker]');
  if (!form) return;
  const input = form.querySelector('input');
  const out = document.querySelector('[data-checker-result]');
  if (!input || !out) return;

  /* Normalise a typed address to just its words. Postal codes and street
     numbers fall away; punctuation in names like "St. Catharines" survives. */
  const normalise = s => s.toLowerCase()
    .replace(/[^a-z\s.'-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  /* Whole-word matching in both directions. Substring matching would be wrong
     here: "Hamilton" contains "Milton", and Hamilton is not in the GTA. */
  const matchesAny = (query, list) => list.some(city => {
    if (query === city) return true;
    if (new RegExp(`(^|\\s)${escapeRe(city)}($|\\s)`).test(query)) return true;
    if (query.length > 3 &&
        new RegExp(`(^|\\s)${escapeRe(query)}($|\\s)`).test(city)) return true;
    return false;
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!input.value.trim()) return;
    const q = normalise(input.value);
    if (!q) return;

    const covered = matchesAny(q, COVERED);
    const nearby = !covered && matchesAny(q, NEARBY);

    out.classList.remove('checker-result--yes', 'checker-result--maybe');
    out.classList.add('is-shown');

    if (covered) {
      out.classList.add('checker-result--yes');
      out.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
        <span><strong>Yes — that's in our service area.</strong> We cover the whole GTA with no travel charge. Book your free consultation and we'll come out, walk the home with you, and design a system around it.</span>`;
    } else if (nearby) {
      out.classList.add('checker-result--maybe');
      out.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16.5v.01"/></svg>
        <span><strong>That's just outside the GTA — but get in touch anyway.</strong> We travel beyond it regularly, depending on the job. Call <a href="tel:+16479362469">647-936-2469</a> and we'll tell you straight away.</span>`;
    } else {
      out.classList.add('checker-result--maybe');
      out.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16.5v.01"/></svg>
        <span><strong>We couldn't match that one.</strong> We cover the entire Greater Toronto Area — try your city or neighbourhood name, or just call <a href="tel:+16479362469">647-936-2469</a> and we'll confirm in seconds.</span>`;
    }
  });
}

/* ---------- Consultation form -------------------------------------------- */
function initForm() {
  const form = document.querySelector('[data-consult-form]');
  if (!form) return;
  const success = document.querySelector('[data-form-success]');

  const setError = (field, on) => field && field.classList.toggle('has-error', on);

  form.addEventListener('submit', e => {
    let ok = true;

    form.querySelectorAll('[required]').forEach(el => {
      const field = el.closest('.field');
      let valid = el.value.trim() !== '';
      if (valid && el.type === 'email') {
        valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
      }
      if (valid && el.type === 'tel') {
        valid = el.value.replace(/\D/g, '').length >= 10;
      }
      setError(field, !valid);
      if (!valid && ok) { el.focus(); }
      ok = ok && valid;
    });

    if (!ok) { e.preventDefault(); return; }

    // No backend wired up yet — show the confirmation state instead of posting.
    // Once you connect a form service, delete this block and let it submit.
    if (!form.getAttribute('action')) {
      e.preventDefault();
      form.style.display = 'none';
      if (success) {
        success.classList.add('is-shown');
        success.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  });

  // Clear the error state as soon as the visitor starts fixing it
  form.querySelectorAll('input, select, textarea').forEach(el => {
    el.addEventListener('input', () => setError(el.closest('.field'), false));
  });
}

/* ---------- Prefill the form from a "book this service" link -------------- */
function initServicePrefill() {
  const params = new URLSearchParams(window.location.search);
  const svc = params.get('service');
  if (!svc) return;
  const box = document.querySelector(`input[type="checkbox"][value="${CSS.escape(svc)}"]`);
  if (box) {
    box.checked = true;
    box.closest('.check')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

/* ---------- Footer year --------------------------------------------------- */
function initYear() {
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });
}

/* ---------- Hero headline: word-by-word glitch reveal --------------------
   Each word gets a small randomised delay on top of its sequence position,
   so the line lands unevenly rather than metronomically. The subtitle and
   scroll cue follow once the headline has finished.                        */
function initHeroTitle() {
  const words = document.querySelectorAll('.hero h1 .hw');
  if (!words.length) return;

  const sub = document.querySelector('[data-hero-sub]');
  const cue = document.querySelector('.explore-btn');

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    words.forEach(w => { w.style.opacity = '1'; w.style.animation = 'none'; });
    if (sub) { sub.style.opacity = '1'; sub.style.animation = 'none'; }
    if (cue) { cue.style.opacity = '1'; cue.style.animation = 'none'; }
    return;
  }

  let last = 0;
  words.forEach((w, i) => {
    const delay = i * 0.135 + Math.random() * 0.07;
    last = delay;
    w.style.animationDelay = delay + 's';
    w.classList.add('is-in');
  });

  if (sub) {
    sub.style.animationDelay = (last + 0.28 + Math.random() * 0.1) + 's';
    sub.classList.add('is-in');
  }
  if (cue) cue.style.animationDelay = (last + 0.9) + 's';
}

/* ---------- 3D house (lazy) ---------------------------------------------- */
async function initStage() {
  const stage = document.querySelector('[data-stage]');
  if (!stage) return;
  try {
    const { initHouse } = await import('./house3d.js');
    initHouse(stage);
  } catch (err) {
    console.warn('[IQ Homes] 3D scene unavailable:', err);
    stage.classList.add('no-webgl');
  }
}

/* ---------- Service cards can drive the 3D scene ------------------------- */
function initDeviceLinks() {
  document.querySelectorAll('[data-focus-device]').forEach(el => {
    el.addEventListener('click', e => {
      const stage = document.querySelector('[data-stage]');
      if (!stage || !stage.focusDevice) return;
      e.preventDefault();
      stage.focusDevice(el.getAttribute('data-focus-device'));
      stage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
}

/* ---------- Boot ---------------------------------------------------------- */
function boot() {
  initNav();
  initHeader();
  initReveal();
  initFaq();
  initBeforeAfter();
  initChecker();
  initForm();
  initServicePrefill();
  initYear();
  initDeviceLinks();
  initHeroTitle();
  initStage();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
