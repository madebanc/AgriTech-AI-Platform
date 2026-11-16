/**
 * app.js — AgriTech AI Platform
 * Author : Daniel Oyanogbezina
 * Complete file: health status, rainfall auto-fill, unit and soil helpers,
 * farm review, results, what to do now, market timing, estimate notice,
 * saved farms, sharing, monthly checklist, and language switching.
 */

const API = 'https://agritech-ai-platform.onrender.com';

/* ── Reference data ─────────────────────────────────────── */
const STATE_RAINFALL = {
  "Abia":650,"Adamawa":900,"Akwa Ibom":2000,
  "Anambra":1500,"Bauchi":850,"Bayelsa":2200,
  "Benue":1100,"Borno":700,"Cross River":1800,
  "Delta":1800,"Ebonyi":1500,"Edo":1600,
  "Ekiti":1300,"Enugu":1400,"FCT Abuja":1100,
  "Gombe":800,"Imo":1600,"Jigawa":600,
  "Kaduna":900,"Kano":650,"Katsina":600,
  "Kebbi":550,"Kogi":1100,"Kwara":1000,
  "Lagos":1450,"Nasarawa":1100,"Niger":1100,
  "Ogun":1200,"Ondo":1400,"Osun":1200,
  "Oyo":1200,"Plateau":1300,"Rivers":2000,
  "Sokoto":500,"Taraba":1000,"Yobe":600,
  "Zamfara":600
};

const SOIL_DEFAULTS = { sandy: 5.8, loamy: 6.2, clay: 5.5, unknown: 6.0, "": 6.0 };

const FALLBACK_PRICES = {
  Cassava: [40000, 80000], Yam: [200000, 400000], Maize: [150000, 250000],
  Rice: [180000, 320000], Groundnut: [120000, 220000], Cocoa: [800000, 1500000]
};

const PROFILE_KEY = 'agritech_farm_profiles';
const CHECK_PREFIX = 'agritech_checks_';

const BTN_PRIMARY = 'padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#1a6b3c;color:#fff;border:none;border-radius:24px;cursor:pointer;';
const BTN_OUTLINE = 'padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#fff;color:#1a6b3c;border:2px solid #1a6b3c;border-radius:24px;cursor:pointer;';
const BTN_DANGER  = 'padding:.45rem 1rem;font-size:.85rem;font-weight:800;background:#fff;color:#b91c1c;border:2px solid #b91c1c;border-radius:24px;cursor:pointer;';

/* ── Helpers ────────────────────────────────────────────── */
const $ = id => document.getElementById(id);
const naira = n => '\u20a6' + Math.round(Number(n) || 0).toLocaleString('en-NG');
const bagsFromTons = tons => Math.round((parseFloat(tons) || 0) * 20);

function t(key, fallback) {
  try {
    const v = LANG.t(key);
    if (v && v !== key) return v;
  } catch (e) { /* fall through */ }
  return fallback !== undefined ? fallback : key;
}

function fill(template, vars) {
  let out = template;
  Object.keys(vars).forEach(k => {
    out = out.split('{' + k + '}').join(String(vars[k]));
  });
  return out;
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, m => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]
  ));
}

function show(id) { const el = $(id); if (el) el.classList.remove('hidden'); }
function hide(id) { const el = $(id); if (el) el.classList.add('hidden'); }
function setText(id, value) { const el = $(id); if (el) el.textContent = value; }
function setVal(id, value) {
  const el = $(id);
  if (el && value !== undefined && value !== null) el.value = value;
}
function removeEl(id) {
  const el = $(id);
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function checkedValue(name) {
  const el = document.querySelector('input[name="' + name + '"]:checked');
  return el ? el.value : '';
}
function cleanTip(tip) {
  return String(tip || '-')
    .replace(/^Best selling months:\s*/i, '')
    .replace(/^Best time to sell:\s*/i, '');
}

/* ── Server status ──────────────────────────────────────── */
let serverState = 'connecting';

function paintStatus() {
  const dot = $('statusDot'), text = $('statusText');
  if (!dot || !text) return;
  const map = {
    connecting: { cls: '',        key: 'status_connecting', fb: 'Connecting...' },
    online:     { cls: 'online',  key: 'status_online',     fb: 'AI Online' },
    offline:    { cls: 'offline', key: 'status_offline',    fb: 'Server offline' }
  };
  const s = map[serverState];
  dot.className = s.cls ? 'status-dot ' + s.cls : 'status-dot';
  text.textContent = t(s.key, s.fb);
}

async function checkServerStatus() {
  serverState = 'connecting';
  paintStatus();
  try {
    const res = await fetch(API + '/health', { signal: AbortSignal.timeout(20000) });
    const data = await res.json();
    serverState = (data.success && data.model_loaded) ? 'online' : 'offline';
  } catch (e) {
    serverState = 'offline';
  }
  paintStatus();
}

/* ── Rainfall auto-fill ─────────────────────────────────── */
async function onStateChange(state) {
  const rain  = $('rainfall');
  const hint  = $('rainfallHint');
  const badge = $('autoFillBadge');
  if (!rain) return;

  if (!state) {
    rain.value = '';
    rain.placeholder = t('ph_rainfall', 'Select state above to auto-fill');
    if (hint) hint.textContent = t('hint_rainfall', '');
    if (badge) badge.style.display = 'none';
    return;
  }

  const local = STATE_RAINFALL[state];
  if (local) {
    rain.value = local;
    if (hint) hint.textContent = state + ': ~' + local + 'mm/year';
    if (badge) {
      badge.textContent = t('autofill_badge', 'Auto-filled');
      badge.style.display = 'inline';
    }
  }

  try {
    const res = await fetch(API + '/api/weather/' + encodeURIComponent(state),
                            { signal: AbortSignal.timeout(10000) });
    const data = await res.json();
    const mm = data.success && data.weather && data.weather.recommended_input_mm;
    if (mm) {
      rain.value = mm;
      if (hint) hint.textContent = state + ': ~' + mm + 'mm/year (live weather)';
    }
  } catch (e) { /* keep the local value */ }
}

/* ── Units and fertilizer helpers ───────────────────────── */
function farmUnitToHa(value, unit) {
  const v = parseFloat(value) || 0;
  if (unit === 'acre') return v * 0.4047;
  if (unit === 'plot') return v * 0.0648;
  return v;
}

function currentUnit() {
  const u = $('farmUnit');
  return u ? u.value : 'hectare';
}

function unitLabel(unit) {
  if (unit === 'acre') return t('unit_acre', 'Acre');
  if (unit === 'plot') return t('unit_plot', 'Plot (648 sqm Lagos standard)');
  return t('unit_hectare', 'Hectare');
}

function updateSizeHelper() {
  const el = $('sizeHelper');
  if (!el) return;
  const raw = $('farmSize') ? $('farmSize').value : '';
  const v = parseFloat(raw) || 0;
  const unit = currentUnit();
  el.textContent = fill(
    t('size_template', '{v} {unit} is about {ha} hectare for the model.'),
    { v: v, unit: unitLabel(unit), ha: farmUnitToHa(v, unit).toFixed(2) }
  );
}

function updateBagsHelper() {
  const el = $('bagsHelper');
  if (!el) return;
  const kg = parseFloat($('fertilizer') ? $('fertilizer').value : '') || 0;
  el.textContent = fill(
    t('bags_template', '{kg} kg per hectare is about {bags} bags of 50 kg.'),
    { kg: kg, bags: (kg / 50).toFixed(1) }
  );
}

function wireSoilType() {
  const sel = $('soilType'), num = $('soilPh');
  if (!sel || !num) return;
  sel.addEventListener('change', () => {
    const v = SOIL_DEFAULTS[sel.value];
    num.value = (v !== undefined) ? v : 6.0;
  });
}

function applyStaticLabels() {
  const fu = $('farmUnit');
  if (fu) {
    const map = { hectare: 'unit_hectare', acre: 'unit_acre', plot: 'unit_plot' };
    Array.from(fu.options).forEach(o => {
      if (map[o.value]) o.textContent = t(map[o.value], o.textContent);
    });
  }
  const st = $('soilType');
  if (st) {
    const map = {
      '': 'soil_prompt', sandy: 'soil_sandy', loamy: 'soil_loamy',
      clay: 'soil_clay', unknown: 'soil_unknown'
    };
    Array.from(st.options).forEach(o => {
      if (map[o.value] !== undefined) o.textContent = t(map[o.value], o.textContent);
    });
  }
}

function applyPlaceholders() {
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    el.placeholder = LANG.t(el.getAttribute('data-i18n-ph'));
  });
}

/* ── Validation and farm review ─────────────────────────── */
function validateForm(d) {
  const errors = [];
  if (!d.crop)  errors.push(t('err_no_crop', 'Please select a crop type.'));
  if (!d.state) errors.push(t('err_no_state', 'Please select your Nigerian state.'));
  if (!d.farm_size_ha || d.farm_size_ha < 0.1)
    errors.push(t('err_farm_size', 'Farm size must be at least 0.1 hectares.'));
  if (!d.rainfall_mm || d.rainfall_mm < 300)
    errors.push(t('err_rainfall', 'Rainfall must be at least 300mm. Select a state to auto-fill.'));
  if (!d.soil_ph || d.soil_ph < 4 || d.soil_ph > 9)
    errors.push(t('err_soil_ph', 'Soil pH must be between 4.0 and 9.0.'));
  return errors;
}

function confirmFarm(d, rawSize) {
  const msg = [
    t('confirm_check', 'Please check before we predict:'),
    '',
    'Crop: ' + d.crop,
    'State: ' + d.state,
    'Size: ' + rawSize + ' ' + unitLabel(currentUnit()) +
      ' (about ' + d.farm_size_ha.toFixed(2) + ' hectare)',
    'Soil pH: ' + d.soil_ph,
    'Fertilizer: ' + d.fertilizer_kg + ' kg (' + (d.fertilizer_kg / 50).toFixed(1) + ' bags)',
    '',
    t('confirm_ask', 'Is this correct? Press OK to predict, Cancel to fix.')
  ].join('\n');
  return window.confirm(msg);
}

/* ── Errors and loading state ───────────────────────────── */
function showError(message) {
  setText('errorMessage', message);
  show('errorSection');
  hide('resultsSection');
  const sec = $('errorSection');
  if (sec) sec.scrollIntoView({ behavior: 'smooth' });
}

function setLoading(on) {
  const btn = $('submitBtn');
  if (!btn) return;
  const txt = $('btnText'), spin = $('btnSpinner');
  if (txt)  txt.classList.toggle('hidden', on);
  if (spin) spin.classList.toggle('hidden', !on);
  btn.disabled = on;
  if (on) hide('errorSection');
}

/* ── Results: plain summary ─────────────────────────────── */
function renderPlainResult(crop, ha, tons) {
  let el = $('plainResult');
  if (!el) {
    const anchor = $('yieldFarm');
    if (!anchor || !anchor.parentElement) return;
    el = document.createElement('p');
    el.id = 'plainResult';
    el.style.cssText = 'font-weight:700;margin-top:.5rem;';
    anchor.parentElement.appendChild(el);
  }
  el.textContent = fill(
    t('plain_template', 'Your {crop} on {ha} hectare may give about {tons} tons, which is about {bags} bags of 50 kg. This is an estimate for planning, not a promise. Weather and pests can change it.'),
    { crop: crop, ha: Number(ha).toFixed(2), tons: tons, bags: bagsFromTons(tons) }
  );
}

/* ── Results: risks, what-if, advice, calendar ─────────── */
function renderRisks(flags) {
  const el = $('riskContent');
  if (!el) return;
  if (!flags || !flags.length) {
    el.innerHTML = '<div class="no-risk">' +
      esc(t('no_risk', 'No risk flags detected. Your farm setup looks good!')) + '</div>';
    return;
  }
  el.innerHTML = '<ul class="risk-list">' + flags.map(r =>
    '<li class="risk-item"><span>!</span><span>' + esc(r) + '</span></li>'
  ).join('') + '</ul>';
}

function renderAdvice(advice) {
  const el = $('adviceGrid');
  if (!el || !advice) return;
  const items = [
    ['adv_season',     'Planting Season', advice.season],
    ['adv_spacing',    'Spacing',         advice.spacing],
    ['adv_harvest',    'Harvest',         advice.harvest],
    ['adv_fertilizer', 'Fertilizer',      advice.fertilizer_tip],
    ['adv_water',      'Water',           advice.water],
    ['adv_soil',       'Soil',            advice.soil],
    ['adv_disease',    'Disease Watch',   advice.disease_watch],
    ['adv_market',     'Market Timing',   advice.market_tip]
  ];
  el.innerHTML = items.map(item =>
    '<div class="advice-item">' +
      '<span class="advice-label">' + esc(t(item[0], item[1])) + '</span>' +
      '<span class="advice-value">' + esc(item[2] || '-') + '</span>' +
    '</div>'
  ).join('');
}

function renderCalendar(cal) {
  const el = $('calendarContent');
  if (!el || !cal) return;
  const last = cal.last_month || {}, now = cal.this_month || {}, next = cal.next_month || {};
  el.innerHTML =
    '<div class="calendar-grid">' +
      '<div class="cal-item past">' +
        '<span class="cal-month">' + esc(last.month) + '</span>' +
        '<p class="cal-task">' + esc(last.task) + '</p></div>' +
      '<div class="cal-item current">' +
        '<span class="cal-now-badge">' + esc(t('now_badge', 'This Month')) + '</span>' +
        '<span class="cal-month">' + esc(now.month) + '</span>' +
        '<p class="cal-task">' + esc(now.task) + '</p></div>' +
      '<div class="cal-item next">' +
        '<span class="cal-month">' + esc(next.month) + '</span>' +
        '<p class="cal-task">' + esc(next.task) + '</p></div>' +
    '</div>';
}

/* ── Results: what to do now ────────────────────────────── */
function urgencyKey(task) {
  const s = String(task || '').toLowerCase();
  if (s.indexOf('harvest') !== -1) return ['urg_harvest', 'Time to harvest'];
  if (s.indexOf('plant') !== -1 || s.indexOf('sow') !== -1) return ['urg_plant', 'Time to plant'];
  if (['spray', 'fungicide', 'pest', 'armyworm', 'weedicide'].some(w => s.indexOf(w) !== -1))
    return ['urg_spray', 'Time to spray'];
  if (s.indexOf('weed') !== -1) return ['urg_weed', 'Time to weed'];
  if (['fertiliz', 'npk', 'urea', 'top-dress', 'apply'].some(w => s.indexOf(w) !== -1))
    return ['urg_fert', 'Time to fertilise'];
  return ['urg_now', 'Do this now'];
}

function renderActionCard(crop, cal, tip) {
  removeEl('actionCard');
  const section = $('resultsSection');
  if (!section || !cal) return;
  const now = cal.this_month || {}, next = cal.next_month || {};
  const urg = urgencyKey(now.task);

  const card = document.createElement('div');
  card.id = 'actionCard';
  card.style.cssText = 'background:linear-gradient(135deg,#1a6b3c,#2e8b57);color:#fff;border-radius:16px;padding:1.2rem;margin:0 0 1rem;box-shadow:0 4px 14px rgba(26,107,60,.28);';
  card.innerHTML =
    '<div style="display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;">' +
      '<h2 style="margin:0;font-size:1.25rem;">' + esc(t('action_title', 'What to do now')) + '</h2>' +
      '<span style="background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.45);padding:.2rem .7rem;border-radius:20px;font-weight:800;font-size:.8rem;">' +
        esc(t(urg[0], urg[1])) + '</span>' +
    '</div>' +
    '<div style="margin-top:.5rem;font-weight:800;font-size:1.05rem;">' +
      esc(fill(t('action_month_task', 'Your {crop} task for {month}'), { crop: crop, month: now.month || '' })) +
    '</div>' +
    '<div style="margin-top:.4rem;background:rgba(255,255,255,.15);border-radius:10px;padding:.8rem;font-weight:600;">' +
      esc(now.task || '') + '</div>' +
    (next.task ? '<div style="margin-top:.6rem;font-size:.9rem;opacity:.92;">' +
      esc(fill(t('action_next_task', 'Next month: {task}'), { task: next.task })) + '</div>' : '') +
    (tip ? '<div style="margin-top:.6rem;font-size:.9rem;background:rgba(255,255,255,.15);border-radius:10px;padding:.6rem;">' +
      '<strong>' + esc(t('action_sell', 'Best time to sell')) + ':</strong> ' + esc(cleanTip(tip)) + '</div>' : '');

  section.insertBefore(card, section.firstChild);
}

/* ── Results: market timing and money ───────────────────── */
function renderMarket(crop, tons, tip) {
  removeEl('marketPanel');
  const anchor = $('yieldFarm');
  const card = (anchor && anchor.closest('.card')) ||
               ($('resultsSection') && $('resultsSection').firstElementChild);
  if (!card || !card.parentElement) return;

  const panel = document.createElement('div');
  panel.id = 'marketPanel';
  panel.style.cssText = 'background:#fff;border-radius:14px;padding:1.2rem;margin:1rem 0;box-shadow:0 2px 10px rgba(0,0,0,.08);';
  card.parentElement.insertBefore(panel, card.nextSibling);

  const bags = bagsFromTons(tons);
  const head = '<h3 style="margin:0 0 .6rem;color:#1a6b3c;">' + esc(t('market_title', 'Market timing and money')) + '</h3>';
  const best = '<div style="margin-bottom:.8rem;font-weight:700;">' +
    esc(t('market_best', 'Best selling months')) + ': ' + esc(cleanTip(tip)) + '</div>';

  const paint = range => {
    if (!range) {
      panel.innerHTML = head + best + '<small>' + esc(t('market_offline', 'Market prices need internet. Connect to see prices.')) + '</small>';
      return;
    }
    const lowBag = range[0] / 20, highBag = range[1] / 20;
    panel.innerHTML = head + best +
      '<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem;">' +
        '<div style="background:#f7faf7;border-radius:10px;padding:.8rem;">' +
          '<div style="font-size:.8rem;color:#555;">' + esc(t('market_bag_price', 'Price per 50 kg bag')) + '</div>' +
          '<div style="font-weight:800;color:#1a6b3c;">' + naira(lowBag) + ' to ' + naira(highBag) + '</div></div>' +
        '<div style="background:#f7faf7;border-radius:10px;padding:.8rem;">' +
          '<div style="font-size:.8rem;color:#555;">' + esc(t('market_your_bags', 'Your expected bags')) + '</div>' +
          '<div style="font-weight:800;color:#1a6b3c;">' + bags + ' bags (' + esc(tons) + ' tons)</div></div>' +
      '</div>' +
      '<div style="margin-top:.8rem;background:#e8f5ec;border-radius:10px;padding:.8rem;">' +
        '<div style="font-size:.8rem;color:#555;">' + esc(t('market_money', 'Expected money if you sell')) + '</div>' +
        '<div style="font-weight:800;color:#1a6b3c;">' + naira(bags * lowBag) + ' to ' + naira(bags * highBag) + '</div></div>' +
      '<small style="display:block;margin-top:.7rem;color:#555;">' + esc(t('market_note', 'Prices are indicative. Check the local market before selling.')) + '</small>';
  };

  paint(null);
  fetch(API + '/api/advice/' + encodeURIComponent(crop), { signal: AbortSignal.timeout(15000) })
    .then(r => r.json())
    .then(d => {
      const pr = d && d.success && d.advice && d.advice.price_range_ngn_per_ton;
      paint(pr ? [pr.low, pr.high] : (FALLBACK_PRICES[crop] || null));
    })
    .catch(() => paint(FALLBACK_PRICES[crop] || null));
}

/* ── Results: estimate notice ───────────────────────────── */
function renderHonesty() {
  removeEl('honestyBadge');
  const section = $('resultsSection');
  if (!section) return;
  const el = document.createElement('div');
  el.id = 'honestyBadge';
  el.style.cssText = 'background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:12px;padding:.8rem 1rem;margin:0 0 1rem;font-weight:600;';
  el.innerHTML =
    '<div style="font-weight:800;margin-bottom:.25rem;">&#9888;&#65039; ' +
      esc(t('indicative_badge', 'Indicative example, not verified yet')) + '</div>' +
    '<div>' + esc(t('honesty_note', 'Estimate from example data. Real farm data check is in progress.')) + '</div>' +
    '<div style="font-weight:400;font-size:.9rem;margin-top:.25rem;">' +
      esc(t('honesty_detail', 'Use for planning only. Confirm with your extension officer or market before deciding.')) + '</div>';
  section.insertBefore(el, section.firstChild);
}

/* ── Results: share, copy, download, print ──────────────── */
function shareText(result) {
  const tons = result.prediction.yield_tons;
  const lines = [
    fill(t('share_for', 'Result for {crop} on {ha} hectare, {tons} tons'),
         { crop: result.crop, ha: result.farm_size_ha, tons: tons }),
    bagsFromTons(tons) + ' bags (50 kg)'
  ];
  const tip = result.advice && result.advice.market_tip;
  if (tip) lines.push('Market: ' + cleanTip(tip));
  lines.push(window.location.href);
  return lines.join('\n');
}

function doCopy(result) {
  const text = shareText(result);
  const btn = $('copyBtn');
  const done = () => {
    if (!btn) return;
    btn.textContent = t('share_copied', 'Copied');
    setTimeout(() => { btn.textContent = t('share_copy', 'Copy'); }, 1600);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => {
      window.prompt('Copy this text', text);
      done();
    });
    return;
  }
  window.prompt('Copy this text', text);
  done();
}

function doShare(result) {
  if (navigator.share) {
    navigator.share({ title: document.title, text: shareText(result) }).catch(() => {});
    return;
  }
  doCopy(result);
}

function doDownload(result) {
  const tons = result.prediction.yield_tons;
  const lines = [
    'AgriTech AI, Farmer Advisory Platform',
    fill(t('share_for', 'Result for {crop} on {ha} hectare, {tons} tons'),
         { crop: result.crop, ha: result.farm_size_ha, tons: tons }),
    'Farm: ' + result.farm_size_ha + ' ha | ' + tons + ' tons (' + bagsFromTons(tons) + ' bags of 50 kg)'
  ];
  const tip = result.advice && result.advice.market_tip;
  if (tip) lines.push('Market: ' + cleanTip(tip));
  lines.push('Estimate for planning only. Confirm with your extension officer or local market.');
  lines.push(window.location.href);

  const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'agritech-' + (result.crop || 'result') + '.txt';
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { a.remove(); URL.revokeObjectURL(url); }, 500);
}

function renderShare(result) {
  removeEl('shareActions');
  const section = $('resultsSection');
  if (!section) return;

  const card = document.createElement('div');
  card.id = 'shareActions';
  card.style.cssText = 'background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:.9rem;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin:1rem 0;';
  card.innerHTML =
    '<div style="font-weight:800;color:#1a6b3c;width:100%;margin-bottom:.35rem;">' +
      esc(t('share_title', 'Share this result')) + '</div>' +
    '<button type="button" id="shareBtn" style="' + BTN_PRIMARY + '">' + esc(t('share_share', 'Share')) + '</button>' +
    '<button type="button" id="copyBtn" style="' + BTN_OUTLINE + '">' + esc(t('share_copy', 'Copy')) + '</button>' +
    '<button type="button" id="downloadBtn" style="' + BTN_PRIMARY + '">' + esc(t('share_download', 'Download')) + '</button>' +
    '<button type="button" id="printBtn" style="' + BTN_OUTLINE + '">' + esc(t('share_print', 'Print')) + '</button>';

  card.querySelector('#shareBtn').addEventListener('click', () => doShare(result));
  card.querySelector('#copyBtn').addEventListener('click', () => doCopy(result));
  card.querySelector('#downloadBtn').addEventListener('click', () => doDownload(result));
  card.querySelector('#printBtn').addEventListener('click', () => window.print());

  section.appendChild(card);
}

/* ── Results: monthly task checklist ────────────────────── */
let checklistState = null;

function checkKey(crop, month) {
  return CHECK_PREFIX + crop + '_' + month;
}

function loadChecks(crop, month, count) {
  let arr = [];
  try {
    const raw = localStorage.getItem(checkKey(crop, month));
    const parsed = raw ? JSON.parse(raw) : null;
    if (Array.isArray(parsed)) arr = parsed;
  } catch (e) { /* start fresh */ }
  while (arr.length < count) arr.push(false);
  return arr.slice(0, count);
}

function saveChecks(crop, month, arr) {
  try { localStorage.setItem(checkKey(crop, month), JSON.stringify(arr)); } catch (e) {}
}

function buildChecklistState(crop, cal, tip) {
  if (!cal || !cal.this_month) return null;
  const tasks = [];
  if (cal.this_month.task) tasks.push(cal.this_month.task);
  if (cal.next_month && cal.next_month.task) tasks.push(cal.next_month.task);
  if (tip) tasks.push(cleanTip(tip));
  return {
    crop: crop,
    month: cal.this_month.month || 'unknown',
    tasks: tasks.slice(0, 3)
  };
}

function renderChecklist(state) {
  removeEl('checkPanel');
  checklistState = state;
  const section = $('resultsSection');
  if (!section || !state || !state.tasks.length) return;

  const crop = state.crop, month = state.month, tasks = state.tasks;
  const checks = loadChecks(crop, month, tasks.length);
  const done = checks.filter(Boolean).length;
  const pct = Math.round((done / tasks.length) * 100);

  const rows = tasks.map((task, i) =>
    '<label style="display:flex;gap:.6rem;align-items:flex-start;padding:.55rem;border:1px solid #eef2ee;border-radius:10px;margin:.45rem 0;cursor:pointer;background:' +
      (checks[i] ? '#f0fdf4' : '#fff') + ';">' +
      '<input type="checkbox" data-i="' + i + '"' + (checks[i] ? ' checked' : '') +
        ' style="width:20px;height:20px;margin-top:2px;accent-color:#1a6b3c;">' +
      '<span style="flex:1;">' + esc(task) +
        (checks[i] ? ' <strong style="color:#1a6b3c;">' + esc(t('check_done', 'Done')) + '</strong>' : '') +
      '</span></label>'
  ).join('');

  const card = document.createElement('div');
  card.id = 'checkPanel';
  card.style.cssText = 'background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:1rem;margin:1rem 0;';
  card.innerHTML =
    '<div style="font-weight:800;color:#1a6b3c;">' + esc(t('check_title', 'Tasks for this month')) + '</div>' +
    '<div style="font-size:.9rem;color:#555;margin:.25rem 0 .3rem;">' + esc(t('check_tick_first', 'Tick tasks as you finish them')) + '</div>' +
    '<div style="background:#eef2ee;border-radius:999px;height:10px;overflow:hidden;margin:.6rem 0;">' +
      '<div style="height:100%;width:' + pct + '%;background:#1a6b3c;"></div></div>' +
    '<div style="font-size:.9rem;font-weight:700;margin-bottom:.3rem;">' +
      esc(fill(t('check_progress', '{done} of {total} done'), { done: done, total: tasks.length })) + '</div>' +
    rows +
    '<div style="margin-top:.6rem;"><button type="button" id="checkResetBtn" style="' + BTN_DANGER + '">' +
      esc(t('check_reset', 'Reset')) + '</button></div>';

  card.querySelectorAll('input[type="checkbox"]').forEach(box => {
    box.addEventListener('change', () => {
      const i = Number(box.getAttribute('data-i'));
      const cur = loadChecks(crop, month, tasks.length);
      cur[i] = box.checked;
      saveChecks(crop, month, cur);
      renderChecklist(state);
    });
  });
  card.querySelector('#checkResetBtn').addEventListener('click', () => {
    saveChecks(crop, month, tasks.map(() => false));
    renderChecklist(state);
  });

  section.appendChild(card);
}

/* ── Saved farms ────────────────────────────────────────── */
function loadProfiles() {
  try {
    const arr = JSON.parse(localStorage.getItem(PROFILE_KEY) || '[]');
    return Array.isArray(arr) ? arr : [];
  } catch (e) { return []; }
}

function storeProfiles(list) {
  try { localStorage.setItem(PROFILE_KEY, JSON.stringify(list)); } catch (e) {}
}

function renderProfiles() {
  const form = $('farmForm');
  if (!form) return;
  let panel = $('profilePanel');
  if (!panel) {
    panel = document.createElement('div');
    panel.id = 'profilePanel';
    panel.style.cssText = 'background:#f0f7f2;border:1px solid #cfe3d6;border-radius:12px;padding:.9rem;margin-bottom:1.1rem;';
    form.insertBefore(panel, form.firstChild);
  }

  const list = loadProfiles();
  const options = list.map(p =>
    '<option value="' + esc(p.id) + '">' + esc(p.name) + ' · ' + esc(p.crop) + ' · ' + esc(p.state) + '</option>'
  ).join('');

  panel.innerHTML =
    '<div style="font-weight:800;color:#1a6b3c;margin-bottom:.5rem;">' + esc(t('profiles_title', 'My saved farms')) + '</div>' +
    '<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;">' +
      '<select id="profileSelect" style="flex:1;min-width:170px;padding:.55rem;border-radius:10px;border:1px solid #cbd5cc;">' +
        '<option value="">' + esc(t('profiles_pick', 'Choose a saved farm')) + '</option>' + options +
      '</select>' +
      '<button type="button" id="profileLoadBtn" style="' + BTN_PRIMARY + '">' + esc(t('profiles_load', 'Load farm')) + '</button>' +
    '</div>' +
    '<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin-top:.6rem;">' +
      '<input id="profileName" type="text" placeholder="' + esc(t('profiles_name_ph', 'Name this farm')) + '" ' +
        'style="flex:1;min-width:140px;padding:.55rem;border-radius:10px;border:1px solid #cbd5cc;">' +
      '<button type="button" id="profileSaveBtn" style="' + BTN_OUTLINE + '">' + esc(t('profiles_save', 'Save this farm')) + '</button>' +
      '<button type="button" id="profileDelBtn" style="' + BTN_DANGER + '">' + esc(t('profiles_delete', 'Delete')) + '</button>' +
    '</div>' +
    (list.length ? '' :
      '<small style="display:block;margin-top:.5rem;color:#555;">' +
        esc(t('profiles_empty', 'No saved farms yet. Fill the form, then tap Save this farm.')) + '</small>');

  panel.querySelector('#profileLoadBtn').addEventListener('click', loadProfile);
  panel.querySelector('#profileSaveBtn').addEventListener('click', saveCurrentProfile);
  panel.querySelector('#profileDelBtn').addEventListener('click', deleteProfile);
}

function loadProfile() {
  const sel = $('profileSelect');
  const p = sel && loadProfiles().find(x => x.id === sel.value);
  if (!p) {
    alert(t('profiles_empty', 'No saved farms yet. Fill the form, then tap Save this farm.'));
    return;
  }
  setVal('crop', p.crop);
  setVal('farmSize', p.size);
  setVal('farmUnit', p.unit || 'hectare');
  setVal('soilType', p.soil_type);
  setVal('soilPh', p.soil_ph);
  setVal('fertilizer', p.fertilizer_kg);
  setVal('state', p.state);
  onStateChange(p.state).then(() => {
    if (p.rainfall_mm) setVal('rainfall', p.rainfall_mm);
  });
  updateSizeHelper();
  updateBagsHelper();
  alert(t('profiles_loaded', 'Farm loaded'));
}

function saveCurrentProfile() {
  const nameEl = $('profileName');
  const name = nameEl ? nameEl.value.trim() : '';
  if (!name) {
    alert(t('profiles_name_ph', 'Name this farm'));
    return;
  }
  const list = loadProfiles();
  const existing = list.find(x => String(x.name).toLowerCase() === name.toLowerCase());
  const val = id => ($(id) ? $(id).value : '');
  const profile = {
    id: existing ? existing.id : 'pf-' + Date.now().toString(36),
    name: name,
    crop: val('crop'),
    state: val('state'),
    size: val('farmSize'),
    unit: val('farmUnit') || 'hectare',
    soil_type: val('soilType'),
    soil_ph: val('soilPh'),
    fertilizer_kg: val('fertilizer'),
    rainfall_mm: val('rainfall'),
    updated_at: new Date().toISOString()
  };
  const next = existing
    ? list.map(x => (x.id === existing.id ? profile : x))
    : [profile].concat(list);
  storeProfiles(next);
  if (nameEl) nameEl.value = '';
  renderProfiles();
  const sel = $('profileSelect');
  if (sel) sel.value = profile.id;
  alert(t('profiles_saved', 'Farm saved'));
}

function deleteProfile() {
  const sel = $('profileSelect');
  if (!sel || !sel.value) return;
  storeProfiles(loadProfiles().filter(x => x.id !== sel.value));
  renderProfiles();
}

/* ── Main results renderer ──────────────────────────────── */
let lastRender = null;

function renderResults(result, calendarData, opts) {
  const scroll = !(opts && opts.scroll === false);
  const crop = result.crop;
  const farmHa = result.farm_size_ha;
  const pred = result.prediction;
  const advice = result.advice || {};
  const cal = calendarData && calendarData.calendar ? calendarData.calendar : null;
  const tip = advice.market_tip;

  lastRender = { result: result, calendarData: calendarData };

  setText('resultCrop', crop);
  setText('yieldTons', pred.yield_tons);
  setText('yieldFarm', farmHa + ' ha');
  setText('incomeLow',  naira(pred.income_low_ngn));
  setText('incomeMid',  naira(pred.income_mid_ngn));
  setText('incomeHigh', naira(pred.income_high_ngn));

  renderPlainResult(crop, farmHa, pred.yield_tons);
  renderRisks(result.risk_flags);

  const wi = result.what_if || {};
  setText('whatifCurrent', pred.yield_tons + 't');
  setText('whatifBest', (wi.yield_tons != null ? wi.yield_tons : pred.yield_tons) + 't');
  setText('whatifUplift', '+' + (wi.uplift_percent || 0) + '% ' +
    t('uplift_text', 'potential uplift with better inputs'));

  renderAdvice(advice);
  renderCalendar(cal);
  renderMarket(crop, pred.yield_tons, tip);
  renderActionCard(crop, cal, tip);
  renderHonesty();
  renderShare(result);
  renderChecklist(buildChecklistState(crop, cal, tip));

  show('resultsSection');
  hide('errorSection');
  if (scroll) {
    const sec = $('resultsSection');
    if (sec) sec.scrollIntoView({ behavior: 'smooth' });
  }
}

/* ── Form submit ────────────────────────────────────────── */
async function onSubmit(e) {
  e.preventDefault();

  const rawSize = $('farmSize') ? $('farmSize').value : '';
  const data = {
    crop:          $('crop').value,
    state:         $('state').value,
    farm_size_ha:  farmUnitToHa(rawSize, currentUnit()),
    rainfall_mm:   parseFloat($('rainfall').value),
    soil_ph:       parseFloat($('soilPh').value),
    fertilizer_kg: parseFloat($('fertilizer').value) || 0,
    improved_seeds: checkedValue('improved_seeds') === 'true',
    irrigation:     checkedValue('irrigation') === 'true'
  };

  const errors = validateForm(data);
  if (errors.length) { showError(errors.join(' ')); return; }
  if (!confirmFarm(data, rawSize)) return;

  setLoading(true);
  try {
    const [pRes, cRes] = await Promise.all([
      fetch(API + '/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        signal: AbortSignal.timeout(60000)
      }),
      fetch(API + '/api/calendar/' + encodeURIComponent(data.crop),
            { signal: AbortSignal.timeout(60000) })
    ]);
    const pJson = await pRes.json();
    const cJson = await cRes.json();

    if (!pJson.success) {
      showError(pJson.error || t('err_server', 'The AI server is warming up. Please wait 30 seconds and try again.'));
      return;
    }
    renderResults(pJson.result, cJson);
  } catch (err) {
    showError(t('err_server', 'The AI server is warming up. Please wait 30 seconds and try again.'));
  } finally {
    setLoading(false);
  }
}

/* ── Language switching ─────────────────────────────────── */
function refreshForLanguage() {
  applyPlaceholders();
  applyStaticLabels();
  updateSizeHelper();
  updateBagsHelper();
  paintStatus();
  renderProfiles();
  if (lastRender) renderResults(lastRender.result, lastRender.calendarData, { scroll: false });
}

function wireLanguageSwitch() {
  if (typeof LANG === 'undefined' || !LANG.setLanguage) return;
  const original = LANG.setLanguage.bind(LANG);
  LANG.setLanguage = function (code) {
    original(code);
    refreshForLanguage();
  };
}

/* ── Initialise ─────────────────────────────────────────── */
function init() {
  LANG.init();
  wireLanguageSwitch();
  applyPlaceholders();
  applyStaticLabels();
  wireSoilType();

  const form = $('farmForm');
  if (form) form.addEventListener('submit', onSubmit);

  const state = $('state');
  if (state) state.addEventListener('change', function () { onStateChange(this.value); });

  const size = $('farmSize');
  if (size) size.addEventListener('input', updateSizeHelper);
  const unit = $('farmUnit');
  if (unit) unit.addEventListener('change', updateSizeHelper);
  const fert = $('fertilizer');
  if (fert) fert.addEventListener('input', updateBagsHelper);

  updateSizeHelper();
  updateBagsHelper();
  renderProfiles();
  checkServerStatus();
}

init();