/**
 * app.js
 * AgriTech AI Platform — Frontend Logic
 * Author  : Daniel Oyanogbezina
 * Purpose : Connects the HTML form to the Day 5 Flask API
 *           Reads form inputs → calls API → renders results
 */

const API = 'https://agritech-ai-api.onrender.com';

/* ── Utility helpers ──────────────────────────────────────── */

const $  = id => document.getElementById(id);
const fmt = n  => `₦${Number(n).toLocaleString('en-NG')}`;

function show(id)  { $(id).classList.remove('hidden'); }
function hide(id)  { $(id).classList.add('hidden'); }

/* ── 1. Server health check on page load ─────────────────── */

async function checkServerStatus() {
  const dot  = $('statusDot');
  const text = $('statusText');

  try {
    const res  = await fetch(`${API}/health`, { signal: AbortSignal.timeout(4000) });
    const data = await res.json();

    if (data.success && data.model_loaded) {
      dot.className  = 'status-dot online';
      text.textContent = 'AI Online';
    } else {
      dot.className  = 'status-dot offline';
      text.textContent = 'Model not loaded';
    }
  } catch {
    dot.className  = 'status-dot offline';
    text.textContent = 'Server offline';
  }
}

/* ── 2. Form validation ───────────────────────────────────── */

function validateForm(data) {
  const errors = [];

  if (!data.crop)
    errors.push('Please select a crop.');
  if (!data.farm_size_ha || data.farm_size_ha < 0.1 || data.farm_size_ha > 100)
    errors.push('Farm size must be between 0.1 and 100 hectares.');
  if (!data.rainfall_mm || data.rainfall_mm < 300 || data.rainfall_mm > 3000)
    errors.push('Rainfall must be between 300 and 3000 mm.');
  if (!data.soil_ph || data.soil_ph < 4.0 || data.soil_ph > 9.0)
    errors.push('Soil pH must be between 4.0 and 9.0.');
  if (data.fertilizer_kg === '' || data.fertilizer_kg < 0 || data.fertilizer_kg > 500)
    errors.push('Fertilizer must be between 0 and 500 kg/ha.');

  return errors;
}

/* ── 3. Render results into the DOM ───────────────────────── */

function renderResults(result, calendarData) {

  const { crop, farm_size_ha, prediction,
          advice, risk_flags, what_if } = result;

  /* Yield + income */
  $('resultCrop').textContent  = crop;
  $('yieldTons').textContent   = prediction.yield_tons;
  $('yieldFarm').textContent   = `${farm_size_ha} ha farm`;
  $('incomeLow').textContent   = fmt(prediction.income_low_ngn);
  $('incomeMid').textContent   = fmt(prediction.income_mid_ngn);
  $('incomeHigh').textContent  = fmt(prediction.income_high_ngn);

  /* Risk flags */
  const riskEl = $('riskContent');
  if (risk_flags.length === 0) {
    riskEl.innerHTML =
      `<div class="no-risk">✅ No risk flags — your farm setup looks good!</div>`;
  } else {
    riskEl.innerHTML =
      `<ul class="risk-list">` +
      risk_flags.map(r =>
        `<li class="risk-item"><span>⚠️</span><span>${r}</span></li>`
      ).join('') +
      `</ul>`;
  }

  /* What-if */
  $('whatifCurrent').textContent = `${prediction.yield_tons}t`;
  $('whatifBest').textContent    = `${what_if.yield_tons}t`;
  $('whatifUplift').textContent  =
    `+${what_if.uplift_percent}% potential uplift with better inputs`;

  /* Farming advice */
  const adviceItems = [
    { label: 'Planting Season', value: advice.season },
    { label: 'Spacing',         value: advice.spacing },
    { label: 'Harvest',         value: advice.harvest },
    { label: 'Fertilizer',      value: advice.fertilizer_tip },
    { label: 'Water',           value: advice.water },
    { label: 'Soil',            value: advice.soil },
    { label: 'Disease Watch',   value: advice.disease_watch },
    { label: 'Market Timing',   value: advice.market_tip },
  ];

  $('adviceGrid').innerHTML = adviceItems.map(item =>
    `<div class="advice-item">
       <span class="advice-label">${item.label}</span>
       <span class="advice-value">${item.value}</span>
     </div>`
  ).join('');

  /* Monthly calendar */
  const cal = calendarData?.calendar;
  if (cal) {
    $('calendarContent').innerHTML =
      `<div class="calendar-grid">
         <div class="cal-item past">
           <span class="cal-month">${cal.last_month.month}</span>
           <p class="cal-task">${cal.last_month.task}</p>
         </div>
         <div class="cal-item current">
           <span class="cal-now-badge">This Month</span>
           <span class="cal-month">${cal.this_month.month}</span>
           <p class="cal-task">${cal.this_month.task}</p>
         </div>
         <div class="cal-item next">
           <span class="cal-month">${cal.next_month.month}</span>
           <p class="cal-task">${cal.next_month.task}</p>
         </div>
       </div>`;
  } else {
    $('calendarContent').textContent = 'Calendar data unavailable.';
  }

  /* Show results, hide error */
  show('resultsSection');
  hide('errorSection');

  /* Smooth scroll to results */
  $('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── 4. Show error ────────────────────────────────────────── */

function showError(message) {
  $('errorMessage').textContent = message;
  show('errorSection');
  hide('resultsSection');
  $('errorSection').scrollIntoView({ behavior: 'smooth' });
}

/* ── 5. Form submission ───────────────────────────────────── */

$('farmForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  /* Collect form values */
  const data = {
    crop:           $('crop').value,
    farm_size_ha:   parseFloat($('farmSize').value),
    rainfall_mm:    parseFloat($('rainfall').value),
    soil_ph:        parseFloat($('soilPh').value),
    fertilizer_kg:  parseFloat($('fertilizer').value),
    improved_seeds: document.querySelector('input[name="improved_seeds"]:checked')?.value === 'true',
    irrigation:     document.querySelector('input[name="irrigation"]:checked')?.value === 'true',
  };

  /* Validate */
  const errors = validateForm(data);
  if (errors.length) {
    showError(errors.join(' '));
    return;
  }

  /* Loading state */
  const btn = $('submitBtn');
  $('btnText').classList.add('hidden');
  $('btnSpinner').classList.remove('hidden');
  btn.disabled = true;

  try {
    /* Call /api/predict */
    const [predictRes, calendarRes] = await Promise.all([
      fetch(`${API}/api/predict`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(data),
      }),
      fetch(`${API}/api/calendar/${encodeURIComponent(data.crop)}`),
    ]);

    const predictJson  = await predictRes.json();
    const calendarJson = await calendarRes.json();

    if (!predictJson.success) {
      showError(predictJson.error || 'Prediction failed. Please try again.');
      return;
    }

    renderResults(predictJson.result, calendarJson);

  } catch (err) {
    showError(
      `Could not reach the API server. ` +
      `Make sure it is running: python3 api/app.py`
    );
  } finally {
    /* Restore button */
    $('btnText').classList.remove('hidden');
    $('btnSpinner').classList.add('hidden');
    btn.disabled = false;
  }
});

/* ── 6. Initialise ────────────────────────────────────────── */
checkServerStatus();