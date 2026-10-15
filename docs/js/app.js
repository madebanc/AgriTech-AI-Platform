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
