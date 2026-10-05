/**
 * disease.js — AgriTech AI Platform
 * Author : Daniel Oyanogbezina
 * Purpose: Crop Disease Encyclopedia
 *          Fetches disease data from API and renders cards
 */

const API = 'https://agritech-ai-platform.onrender.com';

const CROPS = [
  'Cassava', 'Maize', 'Yam', 'Rice', 'Groundnut', 'Cocoa'
];

const SEVERITY_LABELS = {
  critical: '🔴 Critical',
  high:     '🟠 High',
  medium:   '🟡 Medium',
  low:      '🟢 Low',
};

const SEVERITY_COLORS = {
  critical: '#d94f3d',
  high:     '#e07b00',
  medium:   '#f4a900',
  low:      '#1a6b3c',
};

/* ── Helpers ─────────────────────────────────────────────── */
const $ = id => document.getElementById(id);

/* ── Status badge ────────────────────────────────────────── */
async function checkStatus() {
  const dot  = $('statusDot');
  const text = $('statusText');
  try {
    const res  = await fetch(`${API}/health`,
                   { signal: AbortSignal.timeout(10000) });
    const data = await res.json();
    if (data.success) {
      dot.className    = 'status-dot online';
      text.textContent = 'AI Online';
    } else {
      dot.className    = 'status-dot offline';
      text.textContent = 'Offline';
    }
  } catch {
    dot.className    = 'status-dot offline';
    text.textContent = 'Offline';
  }
}

/* ── Load summary (disease counts per crop) ──────────────── */
async function loadSummary() {
  const row = $('summaryRow');
  try {
    const res  = await fetch(`${API}/api/diseases`,
                   { signal: AbortSignal.timeout(15000) });
    const data = await res.json();

    if (data.success && data.summary) {
      const total = data.total_diseases || 0;
      let html = `<div class="summary-pill">
                    <span>${total}</span> Total Diseases Documented
                  </div>`;

      Object.entries(data.summary).forEach(([crop, count]) => {
        html += `<div class="summary-pill">
                   <span>${count}</span> ${crop}
                 </div>`;
      });
      row.innerHTML = html;
    }
  } catch {
    row.innerHTML =
      `<div class="summary-pill">Disease database loading...</div>`;
  }
}

/* ── Build crop tabs ─────────────────────────────────────── */
function buildCropTabs() {
  const tabsEl = $('cropTabs');
  tabsEl.innerHTML = CROPS.map(crop =>
    `<button class="crop-tab"
             onclick="loadDiseases('${crop}')"
             id="tab-${crop}">${crop}</button>`
  ).join('');
}

/* ── Load diseases for selected crop ─────────────────────── */
async function loadDiseases(crop) {

  /* Update active tab */
  document.querySelectorAll('.crop-tab').forEach(tab => {
    tab.classList.toggle('active', tab.id === `tab-${crop}`);
  });

  const grid = $('diseaseGrid');
  grid.innerHTML = `<div class="empty-msg">⏳ Loading ${crop} diseases...</div>`;

  try {
    const res  = await fetch(
      `${API}/api/diseases/${encodeURIComponent(crop)}`,
      { signal: AbortSignal.timeout(20000) }
    );
    const data = await res.json();

    if (!data.success || !data.diseases || data.diseases.length === 0) {
      grid.innerHTML =
        `<div class="empty-msg">No disease data found for ${crop}.</div>`;
      return;
    }

    renderDiseases(data.diseases, crop);

  } catch {
    /* API offline — use fallback local message */
    grid.innerHTML =
      `<div class="empty-msg">
         ⚠️ Could not load disease data.<br>
         The server may be waking up — try again in 30 seconds.
         <br><br>
         <button onclick="loadDiseases('${crop}')"
                 style="background:var(--green-dark);color:white;
                        border:none;padding:.5rem 1rem;
                        border-radius:6px;cursor:pointer;
                        font-weight:600;">
           Retry
         </button>
       </div>`;
  }
}

/* ── Render disease cards ────────────────────────────────── */
function renderDiseases(diseases, crop) {
  const grid = $('diseaseGrid');

  grid.innerHTML = diseases.map((disease, index) => {
    const severityColor = SEVERITY_COLORS[disease.severity] || '#777';
    const severityLabel = SEVERITY_LABELS[disease.severity] || disease.severity;

    /* Symptoms list */
    const symptoms = (disease.symptoms || []).map(s =>
      `<li>${s}</li>`
    ).join('');

    /* Treatment steps */
    const treatment = (disease.treatment || []).map((t, i) =>
      `<li>${t}</li>`
    ).join('');

    /* Prevention */
    const prevention = (disease.prevention || []).map(p =>
      `<li>${p}</li>`
    ).join('');

    /* Local names */
    const localNames = disease.local_names
      ? `<div class="local-names">
           <strong>Local names:</strong>&nbsp;
           <span>🔵 Yoruba: <em>${disease.local_names.yoruba}</em></span>
           <span>🟢 Hausa: <em>${disease.local_names.hausa}</em></span>
           <span>🔴 Igbo: <em>${disease.local_names.igbo}</em></span>
         </div>`
      : '';

    return `
      <div class="disease-card" id="disease-${index}">

        <!-- Clickable header -->
        <div class="disease-header"
             onclick="toggleDisease(${index})">
          <div>
            <div class="disease-name">${disease.name}</div>
            <div class="disease-pathogen">${disease.pathogen}</div>
          </div>
          <div style="display:flex;align-items:center;gap:.75rem;">
            <span class="severity-badge"
                  style="background:${severityColor};">
              ${severityLabel}
            </span>
            <span class="chevron" id="chevron-${index}">▼</span>
          </div>
        </div>

        <!-- Expandable body -->
        <div class="disease-body" id="body-${index}">

          <h4>🔍 Symptoms</h4>
          <ul>${symptoms}</ul>

          <h4>💊 Treatment Steps</h4>
          <ul>${treatment}</ul>

          <h4>🛡️ Prevention</h4>
          <ul>${prevention}</ul>

          <div class="yield-loss-banner">
            ⚠️ <strong>Potential Yield Loss:</strong>
            ${disease.yield_loss || 'Variable'}
          </div>

          ${localNames}

        </div>
      </div>
    `;
  }).join('');

  /* Auto-open first card */
  if (diseases.length > 0) {
    setTimeout(() => toggleDisease(0), 100);
  }
}

/* ── Toggle disease card open/closed ─────────────────────── */
function toggleDisease(index) {
  const body    = $(`body-${index}`);
  const chevron = $(`chevron-${index}`);
  if (!body) return;

  const isOpen = body.classList.contains('open');
  body.classList.toggle('open', !isOpen);
  if (chevron) chevron.classList.toggle('open', !isOpen);
}

/* ── Initialise ──────────────────────────────────────────── */
checkStatus();
buildCropTabs();
loadSummary();

/* Auto-load Cassava on first visit */
setTimeout(() => loadDiseases('Cassava'), 300);