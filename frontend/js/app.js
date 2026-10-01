/**
 * app.js — AgriTech AI Platform Frontend
 * Author : Daniel Oyanogbezina
 * Purpose: Connects the form to the Flask API
 *          Handles state selection, rainfall auto-fill,
 *          prediction requests, and result rendering
 */

/* ── Configuration ─────────────────────────────────────── */
const API = 'https://agritech-ai-platform.onrender.com';

/* ── Rainfall defaults by state (fallback if API fails) ── */
const STATE_RAINFALL = {
  "Abia": 1500, "Adamawa": 900, "Akwa Ibom": 2000,
  "Anambra": 1500, "Bauchi": 850, "Bayelsa": 2200,
  "Benue": 1100, "Borno": 700, "Cross River": 1800,
  "Delta": 1800, "Ebonyi": 1500, "Edo": 1600,
  "Ekiti": 1300, "Enugu": 1400, "FCT Abuja": 1100,
  "Gombe": 800, "Imo": 1600, "Jigawa": 600,
  "Kaduna": 900, "Kano": 650, "Katsina": 600,
  "Kebbi": 550, "Kogi": 1100, "Kwara": 1000,
  "Lagos": 1450, "Nasarawa": 1100, "Niger": 1100,
  "Ogun": 1200, "Ondo": 1400, "Osun": 1200,
  "Oyo": 1200, "Plateau": 1300, "Rivers": 2000,
  "Sokoto": 500, "Taraba": 1000, "Yobe": 600,
  "Zamfara": 600
};

/* ── Helper functions ──────────────────────────────────── */
const $   = id => document.getElementById(id);
const fmt = n  => '\u20a6' + Number(n).toLocaleString('en-NG');

function show(id) { $(id).classList.remove('hidden'); }
function hide(id) { $(id).classList.add('hidden');    }

/* ── 1. Server health check ────────────────────────────── */
async function checkServerStatus() {
  const dot  = $('statusDot');
  const text = $('statusText');

  dot.className    = 'status-dot';
  text.textContent = 'Connecting...';

  try {
    const res  = await fetch(`${API}/health`,
                   { signal: AbortSignal.timeout(20000) });
    const data = await res.json();

    if (data.success && data.model_loaded) {
      dot.className    = 'status-dot online';
      text.textContent = 'AI Online';
    } else {
      dot.className    = 'status-dot offline';
      text.textContent = 'Model not loaded';
    }
  } catch {
    dot.className    = 'status-dot offline';
    text.textContent = 'Server offline';
  }
}

/* ── 2. Auto-fill rainfall when state is selected ──────── */
async function onStateChange(selectedState) {
  const rainfallInput = $('rainfall');
  const hint          = $('rainfallHint');
  const badge         = $('autoFillBadge');

  /* Clear if placeholder selected */
  if (!selectedState) {
    rainfallInput.value       = '';
    rainfallInput.placeholder = 'Select state above to auto-fill';
    if (hint)  hint.textContent = 'Auto-filled from weather data when you select a state';
    if (badge) badge.style.display = 'none';
    return;
  }

  /* Step 1: Immediately fill from local lookup (instant) */
  const localRainfall = STATE_RAINFALL[selectedState];
  if (localRainfall) {
    rainfallInput.value = localRainfall;
    if (hint)  hint.textContent = `${selectedState}: ~${localRainfall}mm/year (regional estimate)`;
    if (badge) badge.style.display = 'inline';
  }

  /* Step 2: Try to improve with live API data */
  try {
    const res  = await fetch(
      `${API}/api/weather/${encodeURIComponent(selectedState)}`,
      { signal: AbortSignal.timeout(10000) }
    );
    const data = await res.json();

    if (data.success && data.weather &&
        data.weather.recommended_input_mm) {
      const mm = data.weather.recommended_input_mm;
      rainfallInput.value = mm;
      if (hint) {
        hint.textContent =
          `${selectedState}: ~${mm}mm/year (live weather data)`;
      }
    }
    /* If API fails, keep the local value already filled */

  } catch {
    /* Keep local value — no need to show error */
    if (hint && localRainfall) {
      hint.textContent =
        `${selectedState}: ~${localRainfall}mm/year (estimated)`;
    }
  }
}

/* ── 3. Render prediction results ──────────────────────── */
function renderResults(result, calendarData) {
  const { crop, farm_size_ha, prediction,
          advice, risk_flags, what_if } = result;

  /* Yield + income */
  $('resultCrop').textContent = crop;
  $('yieldTons').textContent  = prediction.yield_tons;
  $('yieldFarm').textContent  = `${farm_size_ha} ha farm`;
  $('incomeLow').textContent  = fmt(prediction.income_low_ngn);
  $('incomeMid').textContent  = fmt(prediction.income_mid_ngn);
  $('incomeHigh').textContent = fmt(prediction.income_high_ngn);

  /* Risk flags */
  const riskEl = $('riskContent');
  if (!risk_flags || risk_flags.length === 0) {
    riskEl.innerHTML =
      `<div class="no-risk">
         No risk flags detected — your farm setup looks good!
       </div>`;
  } else {
    riskEl.innerHTML =
      `<ul class="risk-list">` +
      risk_flags.map(r =>
        `<li class="risk-item">
           <span>!</span><span>${r}</span>
         </li>`
      ).join('') +
      `</ul>`;
  }

  /* What-if */
  $('whatifCurrent').textContent = `${prediction.yield_tons}t`;
  $('whatifBest').textContent    = `${what_if.yield_tons}t`;
  $('whatifUplift').textContent  =
    `+${what_if.uplift_percent}% potential uplift with better inputs`;

  /* Farming advice grid */
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

  /* Crop calendar */
  const cal = calendarData && calendarData.calendar;
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
    $('calendarContent').textContent = 'Calendar unavailable.';
  }

  show('resultsSection');
  hide('errorSection');
  $('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

/* ── 4. Show error ─────────────────────────────────────── */
function showError(message) {
  $('errorMessage').textContent = message;
  show('errorSection');
  hide('resultsSection');
  $('errorSection').scrollIntoView({ behavior: 'smooth' });
}

/* ── 5. Form validation ────────────────────────────────── */
function validateForm(data) {
  const errors = [];
  if (!data.crop)
    errors.push('Please select a crop type.');
  if (!data.state)
    errors.push('Please select your Nigerian state.');
  if (!data.farm_size_ha || data.farm_size_ha < 0.1)
    errors.push('Farm size must be at least 0.1 hectares.');
  if (!data.rainfall_mm || data.rainfall_mm < 300)
    errors.push('Rainfall must be at least 300mm. Select a state to auto-fill.');
  if (!data.soil_ph || data.soil_ph < 4.0 || data.soil_ph > 9.0)
    errors.push('Soil pH must be between 4.0 and 9.0.');
  if (data.fertilizer_kg === undefined || data.fertilizer_kg === '')
    errors.push('Please enter fertilizer amount (enter 0 if none used).');
  return errors;
}

/* ── 6. Form submission ────────────────────────────────── */
$('farmForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  /* Collect values */
  const data = {
    crop:          $('crop').value,
    state:         $('state').value,
    farm_size_ha:  parseFloat($('farmSize').value),
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
  hide('errorSection');

  try {
    /* Call API */
    const [predictRes, calendarRes] = await Promise.all([
      fetch(`${API}/api/predict`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(data),
        signal:  AbortSignal.timeout(60000),
      }),
      fetch(
        `${API}/api/calendar/${encodeURIComponent(data.crop)}`,
        { signal: AbortSignal.timeout(60000) }
      ),
    ]);

    const predictJson  = await predictRes.json();
    const calendarJson = await calendarRes.json();

    if (!predictJson.success) {
      showError(
        predictJson.error ||
        'Prediction failed. Please check your inputs and try again.'
      );
      return;
    }

    renderResults(predictJson.result, calendarJson);

  } catch (err) {
    showError(
      'The AI server is warming up. ' +
      'Please wait 30 seconds and try again. ' +
      'This only happens on the first request of the day.'
    );
  } finally {
    $('btnText').classList.remove('hidden');
    $('btnSpinner').classList.add('hidden');
    btn.disabled = false;
  }
});

/* ── 7. State change listener ──────────────────────────── */
$('state').addEventListener('change', function () {
  onStateChange(this.value);
});

/* ── 8. Initialise on page load ────────────────────────── */
checkServerStatus();