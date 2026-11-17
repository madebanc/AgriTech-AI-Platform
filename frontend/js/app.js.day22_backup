/**
 * app.js — AgriTech AI Platform
 * Author : Daniel Oyanogbezina
 * Day 9  : Uses LANG.t() for all user-facing text
 *          Supports EN, YO, HA, IG languages
 */

const API = 'https://agritech-ai-platform.onrender.com';

/* ── Rainfall by state (instant local fallback) ─────────── */
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

/* ── Helpers ─────────────────────────────────────────────── */
const $   = id => document.getElementById(id);
const fmt = n  => '\u20a6' + Number(n).toLocaleString('en-NG');

function show(id) { $(id).classList.remove('hidden'); }
function hide(id) { $(id).classList.add('hidden');    }

/* ── Apply placeholder translations ─────────────────────── */
function applyPlaceholders() {
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    el.placeholder = LANG.t(key);
  });
}

/* ── 1. Server health check ──────────────────────────────── */
async function checkServerStatus() {
  const dot  = $('statusDot');
  const text = $('statusText');

  dot.className    = 'status-dot';
  text.textContent = LANG.t('status_connecting');

  try {
    const res  = await fetch(`${API}/health`,
                   { signal: AbortSignal.timeout(20000) });
    const data = await res.json();

    if (data.success && data.model_loaded) {
      dot.className    = 'status-dot online';
      text.textContent = LANG.t('status_online');
    } else {
      dot.className    = 'status-dot offline';
      text.textContent = LANG.t('status_offline');
    }
  } catch {
    dot.className    = 'status-dot offline';
    text.textContent = LANG.t('status_offline');
  }
}

/* ── 2. Auto-fill rainfall when state changes ────────────── */
async function onStateChange(selectedState) {
  const rainfallInput = $('rainfall');
  const hint          = $('rainfallHint');
  const badge         = $('autoFillBadge');

  if (!selectedState) {
    rainfallInput.value       = '';
    rainfallInput.placeholder = LANG.t('ph_rainfall');
    if (hint)  hint.textContent = LANG.t('hint_rainfall');
    if (badge) badge.style.display = 'none';
    return;
  }

  /* Step 1: Fill immediately from local table */
  const local = STATE_RAINFALL[selectedState];
  if (local) {
    rainfallInput.value = local;
    if (hint)  hint.textContent = `${selectedState}: ~${local}mm/year`;
    if (badge) {
      badge.textContent    = LANG.t('autofill_badge');
      badge.style.display  = 'inline';
    }
  }

  /* Step 2: Improve with live weather API */
  try {
    const res  = await fetch(
      `${API}/api/weather/${encodeURIComponent(selectedState)}`,
      { signal: AbortSignal.timeout(10000) }
    );
    const data = await res.json();

    if (data.success && data.weather?.recommended_input_mm) {
      const mm = data.weather.recommended_input_mm;
      rainfallInput.value = mm;
      if (hint) {
        hint.textContent =
          `${selectedState}: ~${mm}mm/year (live weather)`;
      }
    }
  } catch { /* keep local value */ }
}

/* ── 3. Render results ───────────────────────────────────── */
function renderResults(result, calendarData) {
  const { crop, farm_size_ha, prediction,
          advice, risk_flags, what_if } = result;

  $('resultCrop').textContent = crop;
  $('yieldTons').textContent  = prediction.yield_tons;
  $('yieldFarm').textContent  = `${farm_size_ha} ha`;
  updatePlainResult(crop, farm_size_ha, prediction.yield_tons);
  $('incomeLow').textContent  = fmt(prediction.income_low_ngn);
  $('incomeMid').textContent  = fmt(prediction.income_mid_ngn);
  $('incomeHigh').textContent = fmt(prediction.income_high_ngn);

  /* Risk flags */
  const riskEl = $('riskContent');
  if (!risk_flags || risk_flags.length === 0) {
    riskEl.innerHTML =
      `<div class="no-risk">${LANG.t('no_risk')}</div>`;
  } else {
    riskEl.innerHTML =
      `<ul class="risk-list">` +
      risk_flags.map(r =>
        `<li class="risk-item"><span>!</span><span>${r}</span></li>`
      ).join('') + `</ul>`;
  }

  /* What-if */
  $('whatifCurrent').textContent = `${prediction.yield_tons}t`;
  $('whatifBest').textContent    = `${what_if.yield_tons}t`;
  $('whatifUplift').textContent  =
    `+${what_if.uplift_percent}% ${LANG.t('uplift_text')}`;

  /* Advice grid — labels come from translation */
  const adviceItems = [
    { label: LANG.t('adv_season'),    value: advice.season },
    { label: LANG.t('adv_spacing'),   value: advice.spacing },
    { label: LANG.t('adv_harvest'),   value: advice.harvest },
    { label: LANG.t('adv_fertilizer'),value: advice.fertilizer_tip },
    { label: LANG.t('adv_water'),     value: advice.water },
    { label: LANG.t('adv_soil'),      value: advice.soil },
    { label: LANG.t('adv_disease'),   value: advice.disease_watch },
    { label: LANG.t('adv_market'),    value: advice.market_tip },
  ];

  $('adviceGrid').innerHTML = adviceItems.map(item =>
    `<div class="advice-item">
       <span class="advice-label">${item.label}</span>
       <span class="advice-value">${item.value}</span>
     </div>`
  ).join('');

  /* Calendar */
  const cal = calendarData?.calendar;
  if (cal) {
    $('calendarContent').innerHTML =
      `<div class="calendar-grid">
         <div class="cal-item past">
           <span class="cal-month">${cal.last_month.month}</span>
           <p class="cal-task">${cal.last_month.task}</p>
         </div>
         <div class="cal-item current">
           <span class="cal-now-badge"
                 data-i18n="now_badge">${LANG.t('now_badge')}</span>
           <span class="cal-month">${cal.this_month.month}</span>
           <p class="cal-task">${cal.this_month.task}</p>
         </div>
         <div class="cal-item next">
           <span class="cal-month">${cal.next_month.month}</span>
           <p class="cal-task">${cal.next_month.task}</p>
         </div>
       </div>`;
  }

  show('resultsSection');
  hide('errorSection');
  $('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

/* ── 4. Show error ───────────────────────────────────────── */
function showError(message) {
  $('errorMessage').textContent = message;
  show('errorSection');
  hide('resultsSection');
  $('errorSection').scrollIntoView({ behavior: 'smooth' });
}


/* ── Day 15: land unit conversion, model always gets hectares ── */
function farmUnitToHa(value, unit) {
  const v = parseFloat(value) || 0;
  if (unit === "acre") return v * 0.4047;
  if (unit === "plot") return v * 0.0648;
  return v;
}
function updateSizeHelper() {
  const el = document.getElementById("sizeHelper");
  if (!el) return;
  const v = parseFloat(document.getElementById("farmSize").value) || 0;
  const u = document.getElementById("farmUnit") ? document.getElementById("farmUnit").value : "hectare";
  const ha = farmUnitToHa(v, u);
  el.textContent = v + " " + u + " is about " + ha.toFixed(2) + " hectare for the model. Note: 15 plots is about 1 hectare, 6 plots is about 1 acre. Plot sizes differ by town.";
}
function updateBagsHelper() {
  const el = document.getElementById("bagsHelper");
  if (!el) return;
  const kg = parseFloat(document.getElementById("fertilizer").value) || 0;
  el.textContent = kg + " kg per hectare is about " + (kg/50).toFixed(1) + " bags of 50 kg. Enter kg per hectare here, we show bags to help.";
}


/* ── Day 15 Task 3: soil plain words ── */
const SOIL_DEFAULTS = { sandy: 5.8, loamy: 6.2, clay: 5.5, unknown: 6.0, "": 6.0 };
function wireSoilType() {
  const sel = document.getElementById("soilType");
  const num = document.getElementById("soilPh");
  if (!sel || !num) return;
  sel.addEventListener("change", () => {
    const v = SOIL_DEFAULTS[sel.value] ?? 6.0;
    num.value = v;
  });
}
wireSoilType();

/* ── 5. Validate form ────────────────────────────────────── */
function validateForm(data) {
  const errors = [];
  if (!data.crop)          errors.push(LANG.t('err_no_crop'));
  if (!data.state)         errors.push(LANG.t('err_no_state'));
  if (!data.farm_size_ha || data.farm_size_ha < 0.1)
                           errors.push(LANG.t('err_farm_size'));
  if (!data.rainfall_mm || data.rainfall_mm < 300)
                           errors.push(LANG.t('err_rainfall'));
  if (!data.soil_ph || data.soil_ph < 4 || data.soil_ph > 9)
                           errors.push(LANG.t('err_soil_ph'));
  return errors;
}


/* ── Day 16: review in plain farmer words before sending ── */
function confirmFarm(data) {
  const unitEl = document.getElementById("farmUnit");
  const rawVal = document.getElementById("farmSize") ? document.getElementById("farmSize").value : data.farm_size_ha;
  const unit = unitEl ? unitEl.value : "hectare";
  const fertKg = data.fertilizer_kg || 0;
  const msg = "Please check before we predict:\n\nCrop: " + data.crop + "\nState: " + data.state + "\nSize: " + rawVal + " " + unit + " (about " + Number(data.farm_size_ha).toFixed(2) + " hectare for the model)\nSoil pH: " + data.soil_ph + "\nFertilizer: " + fertKg + " kg per hectare (about " + (fertKg/50).toFixed(1) + " bags)\n\nIs this correct? Press OK to predict, Cancel to fix.";
  return window.confirm(msg);
}
function plainBags(tons) {
  const n = parseFloat(tons) || 0;
  return Math.round(n * 20);
}
function updatePlainResult(crop, ha, tons) {
  let el = document.getElementById("plainResult");
  if (!el) {
    const anchor = document.getElementById("yieldFarm");
    if (!anchor || !anchor.parentElement) return;
    el = document.createElement("p");
    el.id = "plainResult";
    el.style.cssText = "font-weight:700; margin-top:.5rem;";
    anchor.parentElement.appendChild(el);
  }
  el.textContent = "Your " + crop + " on " + Number(ha).toFixed(2) + " hectare may give about " + tons + " tons, which is about " + plainBags(tons) + " bags of 50 kg. This is an estimate for planning, not a promise. Weather and pests can change it.";
}

/* ── 6. Form submit ──────────────────────────────────────── */
document.getElementById("farmSize").addEventListener("input", updateSizeHelper);
document.getElementById("farmUnit").addEventListener("change", updateSizeHelper);
document.getElementById("fertilizer").addEventListener("input", updateBagsHelper);
updateSizeHelper();
updateBagsHelper();
$('farmForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const data = {
    crop:          $('crop').value,
    state:         $('state').value,
    farm_size_ha:  farmUnitToHa($('farmSize').value, document.getElementById("farmUnit") ? document.getElementById("farmUnit").value : "hectare"),
    rainfall_mm:   parseFloat($('rainfall').value),
    soil_ph:       parseFloat($('soilPh').value),
    fertilizer_kg: parseFloat($('fertilizer').value) || 0,
    improved_seeds:
      document.querySelector('input[name="improved_seeds"]:checked')
              ?.value === 'true',
    irrigation:
      document.querySelector('input[name="irrigation"]:checked')
              ?.value === 'true',
  };

  const errors = validateForm(data);
  if (errors.length) { showError(errors.join(' ')); return; }
  if (!confirmFarm(data)) { return; }

  /* Loading state */
  const btn = $('submitBtn');
  $('btnText').classList.add('hidden');
  $('btnSpinner').classList.remove('hidden');
  btn.disabled = true;
  hide('errorSection');

  try {
    const [predictRes, calendarRes] = await Promise.all([
      fetch(`${API}/api/predict`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(data),
        signal:  AbortSignal.timeout(60000),
      }),
      fetch(`${API}/api/calendar/${encodeURIComponent(data.crop)}`,
            { signal: AbortSignal.timeout(60000) }),
    ]);

    const predictJson  = await predictRes.json();
    const calendarJson = await calendarRes.json();

    if (!predictJson.success) {
      showError(predictJson.error || LANG.t('err_server'));
      return;
    }

    renderResults(predictJson.result, calendarJson);

  } catch {
    showError(LANG.t('err_server'));
  } finally {
    $('btnText').classList.remove('hidden');
    $('btnSpinner').classList.add('hidden');
    btn.disabled = false;
  }
});

/* ── 7. State change listener ────────────────────────────── */
$('state').addEventListener('change', function () {
  onStateChange(this.value);
});

/* ── 8. Initialise ───────────────────────────────────────── */
LANG.init();           // load saved language + translate page
applyPlaceholders();   // translate input placeholders
checkServerStatus();   // ping the API

/* Day 17: multilingual overrides for units soil bags review */
function updateSizeHelper() {
  var el = document.getElementById("sizeHelper");
  if (!el) return;
  var fv = document.getElementById("farmSize");
  var fu = document.getElementById("farmUnit");
  var v = parseFloat(fv && fv.value) || 0;
  var uVal = fu ? fu.value : "hectare";
  var ha = (typeof farmUnitToHa === "function") ? farmUnitToHa(v, uVal) : v;
  var unitName = uVal;
  try {
    if (uVal === "hectare") unitName = LANG.t("unit_hectare");
    else if (uVal === "acre") unitName = LANG.t("unit_acre");
    else if (uVal === "plot") unitName = LANG.t("unit_plot");
  } catch (e) {}
  var tpl = "{v} {unit} is about {ha} hectare for the model.";
  try { tpl = LANG.t("size_template") || tpl; } catch (e) {}
  el.textContent = tpl.replace("{v}", v).replace("{unit}", unitName).replace("{ha}", ha.toFixed(2));
}
function updateBagsHelper() {
  var el = document.getElementById("bagsHelper");
  if (!el) return;
  var f = document.getElementById("fertilizer");
  var kg = parseFloat(f && f.value) || 0;
  var bags = (kg / 50).toFixed(1);
  var tpl = "{kg} kg per hectare is about {bags} bags of 50 kg.";
  try { tpl = LANG.t("bags_template") || tpl; } catch (e) {}
  el.textContent = tpl.replace("{kg}", kg).replace("{bags}", bags);
}
function plainBags(tons) {
  var n = parseFloat(tons) || 0;
  return Math.round(n * 20);
}
function updatePlainResult(crop, ha, tons) {
  var el = document.getElementById("plainResult");
  if (!el) {
    var anchor = document.getElementById("yieldFarm");
    if (!anchor || !anchor.parentElement) return;
    el = document.createElement("p");
    el.id = "plainResult";
    el.style.cssText = "font-weight:700; margin-top:.5rem;";
    anchor.parentElement.appendChild(el);
  }
  var tpl = "Your {crop} on {ha} hectare may give about {tons} tons, which is about {bags} bags of 50 kg.";
  try { tpl = LANG.t("plain_template") || tpl; } catch (e) {}
  el.textContent = tpl.replace("{crop}", crop).replace("{ha}", Number(ha).toFixed(2)).replace("{tons}", tons).replace("{bags}", plainBags(tons));
}
function confirmFarm(data) {
  var rawVal = document.getElementById("farmSize") ? document.getElementById("farmSize").value : data.farm_size_ha;
  var fu = document.getElementById("farmUnit");
  var unit = fu ? fu.value : "hectare";
  var fertKg = data.fertilizer_kg || 0;
  var t = function (k, fb) { try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; } };
  var msg = t("confirm_check", "Please check before we predict:") + "\n\nCrop: " + data.crop + "\nState: " + data.state + "\nSize: " + rawVal + " " + unit + " (about " + Number(data.farm_size_ha).toFixed(2) + " hectare)\nSoil pH: " + data.soil_ph + "\nFertilizer: " + fertKg + " kg (" + (fertKg / 50).toFixed(1) + " bags)\n\n" + t("confirm_ask", "Is this correct? Press OK to predict, Cancel to fix.");
  return window.confirm(msg);
}
function applyDay17Static() {
  try {
    var fu = document.getElementById("farmUnit");
    if (fu && fu.options && fu.options.length >= 3) {
      fu.options[0].text = LANG.t("unit_hectare");
      fu.options[1].text = LANG.t("unit_acre");
      fu.options[2].text = LANG.t("unit_plot");
    }
    var st = document.getElementById("soilType");
    if (st && st.options) {
      for (var i = 0; i < st.options.length; i++) {
        var v = st.options[i].value;
        if (v === "") st.options[i].text = LANG.t("soil_prompt");
        else if (v === "sandy") st.options[i].text = LANG.t("soil_sandy");
        else if (v === "loamy") st.options[i].text = LANG.t("soil_loamy");
        else if (v === "clay") st.options[i].text = LANG.t("soil_clay");
        else if (v === "unknown") st.options[i].text = LANG.t("soil_unknown");
      }
    }
  } catch (e) {}
}
if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day17hooked) {
  var _origSet = LANG.setLanguage.bind(LANG);
  LANG.setLanguage = function (code) {
    var r = _origSet(code);
    try { applyDay17Static(); updateSizeHelper(); updateBagsHelper(); } catch (e) {}
    return r;
  };
  LANG.__day17hooked = true;
}
document.addEventListener("DOMContentLoaded", function () { try { applyDay17Static(); } catch (e) {} });
try { applyDay17Static(); } catch (e) {}


/* Day 18: market timing and money in hand */
var DAY18_PRICES = {
  "Cassava": [40000, 80000], "Yam": [200000, 400000], "Maize": [150000, 250000],
  "Rice": [180000, 320000], "Groundnut": [120000, 220000], "Cocoa": [800000, 1500000]
};
function day18T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function day18Money(n) {
  return "₦" + Math.round(n).toLocaleString("en-NG");
}
function removeMarketPanel() {
  var el = document.getElementById("marketPanel");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function marketPanelShell() {
  removeMarketPanel();
  var anchor = document.getElementById("yieldFarm");
  if (!anchor || !anchor.parentElement) return null;
  var greenCard = anchor.parentElement;
  var section = greenCard.parentElement;
  var panel = document.createElement("div");
  panel.id = "marketPanel";
  panel.style.cssText = "background:#fff;border-radius:14px;padding:1.2rem;margin:1rem 0;box-shadow:0 2px 10px rgba(0,0,0,.08);";
  if (section && section.insertBefore) section.insertBefore(panel, greenCard.nextSibling);
  else greenCard.parentElement.appendChild(panel);
  return panel;
}
function renderMarket(crop, tons, marketTip) {
  var panel = marketPanelShell();
  if (!panel) return;
  var bags = Math.round((parseFloat(tons) || 0) * 20);
  var head = "<h3 style='margin:0 0 .6rem; color:#1a6b3c;'>" + day18T("market_title", "Market timing and money") + "</h3>";
  var best = "<div style='margin-bottom:.8rem; font-weight:700;'>" + day18T("market_best", "Best selling months") + ": " + day19CleanTip(marketTip) + "</div>";
  var body = "";
  var range = DAY18_PRICES[crop];
  var useFallback = true;
  fetch(API + "/api/advice/" + encodeURIComponent(crop))
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d && d.success && d.advice && d.advice.price_range_ngn_per_ton) {
        useFallback = false;
        range = [d.advice.price_range_ngn_per_ton.low, d.advice.price_range_ngn_per_ton.high];
        paintMarket(range, bags, tons);
      }
    })
    .catch(function () { paintMarket(range, bags, tons); });
  function paintMarket(r, b, t) {
    var lowBag = r[0] / 20, highBag = r[1] / 20;
    var lowMoney = b * lowBag, highMoney = b * highBag;
    body = "<div style='display:grid;grid-template-columns:1fr 1fr;gap:.8rem;'>"
      + "<div style='background:#f7faf7;border-radius:10px;padding:.8rem;'>"
      + "<div style='font-size:.8rem;color:#555;'>" + day18T("market_bag_price", "Price per 50 kg bag") + "</div>"
      + "<div style='font-weight:800;color:#1a6b3c;'>" + day18Money(lowBag) + " - " + day18Money(highBag) + "</div></div>"
      + "<div style='background:#f7faf7;border-radius:10px;padding:.8rem;'>"
      + "<div style='font-size:.8rem;color:#555;'>" + day18T("market_your_bags", "Your expected bags") + "</div>"
      + "<div style='font-weight:800;color:#1a6b3c;'>" + b + " bags (" + t + " tons)</div></div></div>"
      + "<div style='margin-top:.8rem;background:#e8f5ec;border-radius:10px;padding:.8rem;'>"
      + "<div style='font-size:.8rem;color:#555;'>" + day18T("market_money", "Expected money if you sell") + "</div>"
      + "<div style='font-weight:800;color:#1a6b3c;'>" + day18Money(lowMoney) + " - " + day18Money(highMoney) + "</div></div>"
      + "<small style='display:block;margin-top:.7rem;color:#555;'>" + day18T("market_note", "Prices are indicative. Check the local market before selling.") + "</small>";
    panel.innerHTML = head + best + body;
  }
  panel.innerHTML = head + best + "<small>" + day18T("market_offline", "Market prices need internet. Connect to see prices.") + "</small>";
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day18hook) {
  var _day18render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day18render.apply(this, arguments);
    try {
      var crop = result && result.crop;
      var tons = result && result.prediction && result.prediction.yield_tons;
      var tip = result && result.advice && result.advice.market_tip;
      if (crop && tons) renderMarket(crop, tons, tip);
    } catch (e) {}
    return r;
  };
  window.__day18hook = true;
}


/* Day 19: what to do now, at the very top of results */
function day19T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function day19Urgency(task) {
  var t = String(task || "").toLowerCase();
  if (t.indexOf("harvest") !== -1) return { key: "urg_harvest", fb: "Time to harvest", color: "#b45309" };
  if (t.indexOf("plant") !== -1 || t.indexOf("sow") !== -1) return { key: "urg_plant", fb: "Time to plant", color: "#15803d" };
  if (t.indexOf("spray") !== -1 || t.indexOf("fungicide") !== -1 || t.indexOf("pest") !== -1 || t.indexOf("armyworm") !== -1 || t.indexOf("weedicide") !== -1)
    return { key: "urg_spray", fb: "Time to spray", color: "#b91c1c" };
  if (t.indexOf("weed") !== -1) return { key: "urg_weed", fb: "Time to weed", color: "#a16207" };
  if (t.indexOf("fertiliz") !== -1 || t.indexOf("npk") !== -1 || t.indexOf("urea") !== -1 || t.indexOf("top-dress") !== -1 || t.indexOf("apply") !== -1)
    return { key: "urg_fert", fb: "Time to fertilise", color: "#1d4ed8" };
  return { key: "urg_now", fb: "Do this now", color: "#1a6b3c" };
}
function day19CleanTip(t) {
  return String(t || "-").replace(/^Best selling months:\s*/i, "").replace(/^Best time to sell:\s*/i, "");
}
function removeActionCard() {
  var el = document.getElementById("actionCard");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function renderActionCard(crop, calendarData, marketTip) {
  removeActionCard();
  var section = document.getElementById("resultsSection");
  if (!section) return;
  var card = document.createElement("div");
  card.id = "actionCard";
  card.style.cssText = "background:linear-gradient(135deg,#1a6b3c,#2e8b57);color:#fff;border-radius:16px;padding:1.2rem;margin:0 0 1rem;box-shadow:0 4px 14px rgba(26,107,60,.28);";
  var cal = calendarData && calendarData.calendar ? calendarData.calendar : null;
  if (!cal) return;
  var thisM = cal.this_month || {};
  var nextM = cal.next_month || {};
  var urg = day19Urgency(thisM.task);
  var head = "<div style='display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;'>"
    + "<h2 style='margin:0;font-size:1.25rem;'>" + day19T("action_title", "What to do now") + "</h2>"
    + "<span style='background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.45);padding:.2rem .7rem;border-radius:20px;font-weight:800;font-size:.8rem;'>"
    + day19T(urg.key, urg.fb) + "</span></div>";
  var monthLine = "<div style='margin-top:.5rem;font-weight:800;font-size:1.05rem;'>"
    + day19T("action_month_task", "Your {crop} task for {month}")
        .replace("{crop}", crop || "").replace("{month}", thisM.month || "") + "</div>";
  var taskLine = "<div style='margin-top:.4rem;background:rgba(255,255,255,.15);border-radius:10px;padding:.8rem;font-weight:600;'>"
    + (thisM.task || "") + "</div>";
  var nextLine = nextM.task
    ? "<div style='margin-top:.6rem;font-size:.9rem;opacity:.92;'>"
      + day19T("action_next_task", "Next month: {task}").replace("{task}", nextM.task) + "</div>"
    : "";
  var sellLine = marketTip
    ? "<div style='margin-top:.6rem;font-size:.9rem;background:rgba(255,255,255,.15);border-radius:10px;padding:.6rem;'>"
      + "<strong>" + day19T("action_sell", "Best time to sell") + ":</strong> " + day19CleanTip(marketTip) + "</div>"
    : "";
  card.innerHTML = head + monthLine + taskLine + nextLine + sellLine;
  section.insertBefore(card, section.firstChild);
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day19hook) {
  var _day19render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day19render.apply(this, arguments);
    try {
      var crop = result && result.crop;
      var tip = result && result.advice && result.advice.market_tip;
      if (crop) renderActionCard(crop, calendarData, tip);
    } catch (e) {}
    return r;
  };
  window.__day19hook = true;
}


/* Day 20: saved farm profiles, one tap fills the form */
var DAY20_KEY = "agritech_farm_profiles";
function day20T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function esc20(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (m) {
    return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
  });
}
function loadProfiles() {
  try {
    var raw = localStorage.getItem(DAY20_KEY);
    var arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch (e) { return []; }
}
function saveProfiles(list) {
  try { localStorage.setItem(DAY20_KEY, JSON.stringify(list)); } catch (e) {}
}
function profilePanel() {
  var existing = document.getElementById("profilePanel");
  if (existing) return existing;
  var form = document.getElementById("farmForm");
  if (!form) return null;
  var panel = document.createElement("div");
  panel.id = "profilePanel";
  panel.style.cssText = "background:#f0f7f2;border:1px solid #cfe3d6;border-radius:12px;padding:.9rem;margin-bottom:1.1rem;";
  form.insertBefore(panel, form.firstChild);
  return panel;
}
function renderProfiles() {
  var panel = profilePanel();
  if (!panel) return;
  var list = loadProfiles();
  var opts = '<option value="">' + (list.length ? esc20(day20T("profiles_pick", "Choose a saved farm")) : "") + '</option>';
  list.forEach(function (p) {
    opts += '<option value="' + esc20(p.id) + '">' + esc20(p.name) + " — " + esc20(p.crop) + " · " + esc20(p.state) + '</option>';
  });
  panel.innerHTML =
    '<div style="font-weight:800;color:#1a6b3c;margin-bottom:.5rem;">' + esc20(day20T("profiles_title", "My saved farms")) + '</div>'
    + '<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;">'
    + '<select id="profileSelect" style="flex:1;min-width:170px;padding:.55rem;border-radius:10px;border:1px solid #cbd5cc;">' + opts + '</select>'
    + '<button type="button" id="profileLoadBtn" style="padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#1a6b3c;color:#fff;border:none;border-radius:24px;cursor:pointer;">' + esc20(day20T("profiles_load", "Load farm")) + '</button>'
    + '</div>'
    + '<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin-top:.6rem;">'
    + '<input id="profileName" type="text" placeholder="' + esc20(day20T("profiles_name_ph", "Name this farm")) + '" style="flex:1;min-width:140px;padding:.55rem;border-radius:10px;border:1px solid #cbd5cc;">'
    + '<button type="button" id="profileSaveBtn" style="padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#fff;color:#1a6b3c;border:2px solid #1a6b3c;border-radius:24px;cursor:pointer;">' + esc20(day20T("profiles_save", "Save this farm")) + '</button>'
    + '<button type="button" id="profileDelBtn" style="padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#fff;color:#b91c1c;border:2px solid #b91c1c;border-radius:24px;cursor:pointer;">' + esc20(day20T("profiles_delete", "Delete")) + '</button>'
    + '</div>'
    + (list.length ? "" : '<small style="display:block;margin-top:.5rem;color:#555;">' + esc20(day20T("profiles_empty", "No saved farms yet. Fill the form, then tap Save this farm.")) + '</small>');
  var lb = document.getElementById("profileLoadBtn");
  var sb = document.getElementById("profileSaveBtn");
  var db = document.getElementById("profileDelBtn");
  if (lb) lb.addEventListener("click", loadProfile);
  if (sb) sb.addEventListener("click", saveCurrentProfile);
  if (db) db.addEventListener("click", deleteProfile);
}
function loadProfile() {
  var sel = document.getElementById("profileSelect");
  if (!sel || !sel.value) { alert(day20T("profiles_empty", "No saved farms yet. Fill the form, then tap Save this farm.")); return; }
  var list = loadProfiles();
  var p = null;
  list.forEach(function (x) { if (x.id === sel.value) p = x; });
  if (!p) return;
  function set(id, v) { var el = document.getElementById(id); if (el) el.value = v; }
  set("crop", p.crop || "");
  set("state", p.state || "");
  set("farmSize", p.size || "");
  set("farmUnit", p.unit || "hectare");
  set("soilType", p.soil_type || "");
  set("soilPh", p.soil_ph || "");
  set("fertilizer", p.fertilizer_kg || "");
  if (p.rainfall_mm) set("rainfall", p.rainfall_mm);
  try { if (typeof updateSizeHelper === "function") updateSizeHelper(); } catch (e) {}
  try { if (typeof updateBagsHelper === "function") updateBagsHelper(); } catch (e) {}
  try { if (typeof applyDay17Static === "function") applyDay17Static(); } catch (e) {}
  var st = document.getElementById("state");
  if (st) { try { st.dispatchEvent(new Event("change")); } catch (e) {} }
  alert(day20T("profiles_loaded", "Farm loaded"));
}
function saveCurrentProfile() {
  function g(id) { return document.getElementById(id); }
  var nameEl = g("profileName");
  var name = nameEl ? nameEl.value.trim() : "";
  if (!name) { alert(day20T("profiles_name_ph", "Name this farm")); return; }
  var list = loadProfiles();
  var existing = null;
  list.forEach(function (x) { if (String(x.name).toLowerCase() === name.toLowerCase()) existing = x; });
  var cropEl = g("crop"), stateEl = g("state"), sizeEl = g("farmSize"), unitEl = g("farmUnit");
  var soilTypeEl = g("soilType"), soilPhEl = g("soilPh"), fertEl = g("fertilizer"), rainEl = g("rainfall");
  var profile = {
    id: existing ? existing.id : "pf-" + Date.now().toString(36),
    name: name,
    crop: cropEl ? cropEl.value : "",
    state: stateEl ? stateEl.value : "",
    size: sizeEl ? sizeEl.value : "",
    unit: unitEl ? unitEl.value : "hectare",
    soil_type: soilTypeEl ? soilTypeEl.value : "",
    soil_ph: soilPhEl ? soilPhEl.value : "",
    fertilizer_kg: fertEl ? fertEl.value : "",
    rainfall_mm: rainEl ? rainEl.value : "",
    updated_at: new Date().toISOString()
  };
  if (existing) {
    list = list.map(function (x) { return x.id === existing.id ? profile : x; });
  } else {
    list.unshift(profile);
  }
  saveProfiles(list);
  if (nameEl) nameEl.value = "";
  renderProfiles();
  var sel = document.getElementById("profileSelect");
  if (sel) sel.value = profile.id;
  alert(day20T("profiles_saved", "Farm saved"));
}
function deleteProfile() {
  var sel = document.getElementById("profileSelect");
  if (!sel || !sel.value) return;
  var list = loadProfiles().filter(function (x) { return x.id !== sel.value; });
  saveProfiles(list);
  renderProfiles();
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", function () { setTimeout(renderProfiles, 0); });
} else {
  setTimeout(renderProfiles, 0);
}
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day20hooked) {
    var _d20set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d20set(code);
      try { renderProfiles(); } catch (e) {}
      return r;
    };
    LANG.__day20hooked = true;
  }
} catch (e) {}


/* Day 21: honesty badge, example data until verified */
function day21HT(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function ensureHonestyBadge() {
  var section = document.getElementById("resultsSection");
  if (!section) return;
  var el = document.getElementById("honestyBadge");
  if (!el) {
    el = document.createElement("div");
    el.id = "honestyBadge";
    el.style.cssText = "background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:12px;padding:.8rem 1rem;margin:0 0 1rem;font-weight:600;";
    section.insertBefore(el, section.firstChild);
  }
  var badge = day21HT("indicative_badge", "Indicative example, not verified yet");
  var note = day21HT("honesty_note", "Estimate from example data. Real farm data check is in progress.");
  var detail = day21HT("honesty_detail", "Use for planning only. Confirm with your extension officer or market before deciding.");
  el.innerHTML = "<div style='font-weight:800;margin-bottom:.25rem;'>&#9888;&#65039; " + badge + "</div>"
    + "<div>" + note + "</div>"
    + "<div style='font-weight:400;font-size:.9rem;margin-top:.25rem;'>" + detail + "</div>";
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day21honhook) {
  var _day21render = window.renderResults || renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day21render.apply(this, arguments);
    try { ensureHonestyBadge(); } catch (e) {}
    return r;
  };
  try { renderResults = window.renderResults; } catch (e) {}
  window.__day21honhook = true;
}
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day21honhooked) {
    var _d21set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d21set(code);
      try { ensureHonestyBadge(); } catch (e) {}
      return r;
    };
    LANG.__day21honhooked = true;
  }
} catch (e) {}


/* Day 22: share, copy, download, print */
function day22T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function buildShareText(result) {
  if (!result) return document.title;
  var crop = result.crop || "";
  var farm = result.farm_size_ha != null ? String(result.farm_size_ha) : "";
  var tons = result.prediction ? String(result.prediction.yield_tons) : "";
  var tpl = day22T("share_for", "Result for {crop} on {ha} hectare, {tons} tons");
  var line = tpl.replace("{crop}", crop).replace("{ha}", farm).replace("{tons}", tons);
  var bags = result.prediction ? Math.round((parseFloat(tons) || 0) * 20) + " bags (50 kg)" : "";
  var marketTip = result.advice && result.advice.market_tip ? result.advice.market_tip : "";
  var out = line;
  if (bags) out += "\n" + bags;
  if (marketTip) out += "\nMarket: " + marketTip;
  out += "\n" + window.location.href;
  return out;
}
function removeShareActions() {
  var el = document.getElementById("shareActions");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function shareActions(result) {
  removeShareActions();
  try { window.__day22lastResult = result; } catch (e) {}
  var section = document.getElementById("resultsSection");
  if (!section) return;
  var card = document.createElement("div");
  card.id = "shareActions";
  card.style.cssText = "background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:.9rem;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin:1rem 0;";
  var title = document.createElement("div");
  title.textContent = day22T("share_title", "Share this result");
  title.style.cssText = "font-weight:800;color:#1a6b3c;width:100%;margin-bottom:.35rem;";
  card.appendChild(title);
  var btns = [
    { id: "shareBtn", t: "share_share", fb: "Share", fn: function () { doShare(result); } },
    { id: "copyBtn", t: "share_copy", fb: "Copy", fn: function () { doCopy(result); } },
    { id: "downloadBtn", t: "share_download", fb: "Download", fn: function () { doDownload(result); } },
    { id: "printBtn", t: "share_print", fb: "Print", fn: function () { window.print(); } }
  ];
  btns.forEach(function (b) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = b.id;
    btn.textContent = day22T(b.t, b.fb);
    btn.style.cssText = "padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#1a6b3c;color:#fff;border:none;border-radius:24px;cursor:pointer;";
    if (b.id === "copyBtn" || b.id === "printBtn") {
      btn.style.background = "#fff";
      btn.style.color = "#1a6b3c";
      btn.style.border = "2px solid #1a6b3c";
    }
    btn.addEventListener("click", b.fn);
    card.appendChild(btn);
  });
  section.appendChild(card);
}
function doShare(result) {
  var text = buildShareText(result);
  var url = window.location.href;
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: url }).catch(function () {});
    return;
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).catch(function () {});
  }
  window.prompt("Copy this text", text);
}
function doCopy(result) {
  var text = buildShareText(result);
  var btn = document.getElementById("copyBtn");
  function done() {
    if (btn) {
      btn.textContent = day22T("share_copied", "Copied");
      setTimeout(function () { btn.textContent = day22T("share_copy", "Copy"); }, 1600);
    }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(function () {
      window.prompt("Copy this text", text);
      done();
    });
    return;
  }
  window.prompt("Copy this text", text);
  done();
}
function doDownload(result) {
  if (!result) return;
  var crop = result.crop || "";
  var ha = result.farm_size_ha != null ? String(result.farm_size_ha) : "";
  var tons = result.prediction ? String(result.prediction.yield_tons) : "";
  var bags = result.prediction ? String(Math.round((parseFloat(tons) || 0) * 20)) : "";
  var lines = [];
  lines.push("AgriTech AI, Farmer Advisory Platform, Day 22");
  lines.push(day22T("share_for", "Result for {crop} on {ha} hectare, {tons} tons").replace("{crop}", crop).replace("{ha}", ha).replace("{tons}", tons));
  lines.push("Farm: " + ha + " ha | " + tons + " tons (" + bags + " bags of 50 kg)");
  var tip = result.advice && result.advice.market_tip ? result.advice.market_tip : "";
  if (tip) lines.push("Market: " + tip);
  lines.push("Note: Iseyin Oyo cassava field point, 60 acres TME 419 May/June 2025 rain-fed, held as Oyo and South-West price indicator in review, not verified live.");
  lines.push(window.location.href);
  var body = lines.join("\n");
  var blob = new Blob([body], { type: "text/plain;charset=utf-8" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = "agritech-" + (crop || "result") + ".txt";
  document.body.appendChild(a);
  a.click();
  setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(url); }, 500);
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day22sharehook) {
  var _day22render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day22render.apply(this, arguments);
    try { shareActions(result); } catch (e) {}
    return r;
  };
  try { renderResults = window.renderResults; } catch (e) {}
  window.__day22sharehook = true;
}
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day22sharehooked) {
    var _d22set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d22set(code);
      try {
        var res = window.__day22lastResult;
        if (res) shareActions(res);
      } catch (e) {}
      return r;
    };
    LANG.__day22sharehooked = true;
  }
} catch (e) {}
