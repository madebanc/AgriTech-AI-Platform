/**
 * analytics.js — AgriTech AI Platform
 * Author : Daniel Oyanogbezina
 * Purpose: Fetches analytics data and renders Chart.js charts
 */

const API = 'https://agritech-ai-platform.onrender.com';

/* ── Colour palette ─────────────────────────────────────── */
const COLORS = {
  green:  ['#1a6b3c','#2d8a4e','#4aab6b','#6cc98a','#8fe0a5','#b2f0c0'],
  amber:  ['#f4a900','#e09800','#cc8800','#b87800','#a46800','#905800'],
  mixed:  ['#1a6b3c','#f4a900','#2d8a4e','#e07b00','#4aab6b','#cc8800',
           '#6cc98a','#a46800'],
};

const FONT = { family: "'Segoe UI', Arial, sans-serif", size: 12 };

Chart.defaults.font = FONT;
Chart.defaults.color = '#555';

/* ── Helpers ─────────────────────────────────────────────── */
const $ = id => document.getElementById(id);
const fmt = n => '\u20a6' + Number(n).toLocaleString('en-NG');

function show(id) { $(id).classList.remove('hidden'); }
function hide(id) { $(id).classList.add('hidden');    }

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

/* ── Render key metrics row ──────────────────────────────── */
function renderMetrics(analytics) {
  const m = analytics.key_metrics || {};
  const metrics = [
    {
      number: analytics.total_predictions.toLocaleString(),
      label:  'Total Predictions'
    },
    {
      number: m.avg_yield ? `${m.avg_yield}t` : '—',
      label:  'Avg Predicted Yield'
    },
    {
      number: m.avg_income ? fmt(m.avg_income) : '—',
      label:  'Avg Est. Income'
    },
    {
      number: m.avg_uplift ? `+${m.avg_uplift}%` : '—',
      label:  'Avg Yield Uplift'
    },
    {
      number: m.pct_improved_seeds
              ? `${Math.round(m.pct_improved_seeds)}%`
              : '—',
      label:  'Using Improved Seeds'
    },
    {
      number: m.pct_irrigation
              ? `${Math.round(m.pct_irrigation)}%`
              : '—',
      label:  'Have Irrigation'
    },
  ];

  $('metricsGrid').innerHTML = metrics.map(m => `
    <div class="metric-box">
      <span class="metric-number">${m.number}</span>
      <span class="metric-label">${m.label}</span>
    </div>
  `).join('');
}

/* ── Chart 1: Predictions by crop ────────────────────────── */
function renderCropChart(byCrop) {
  const labels = byCrop.map(r => r.crop);
  const values = byCrop.map(r => r.count);

  new Chart($('cropChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Predictions',
        data: values,
        backgroundColor: COLORS.green.slice(0, labels.length),
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
          grid: { color: '#f0f0f0' }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

/* ── Chart 2: Predictions by state ───────────────────────── */
function renderStateChart(byState) {
  const labels = byState.map(r => r.state);
  const values = byState.map(r => r.count);

  new Chart($('stateChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Predictions',
        data: values,
        backgroundColor: COLORS.amber.slice(0, labels.length),
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',    // horizontal bar chart
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
          grid: { color: '#f0f0f0' }
        },
        y: { grid: { display: false } }
      }
    }
  });
}

/* ── Chart 3: Predictions over time ──────────────────────── */
function renderTimeChart(overTime) {
  const labels = overTime.map(r => {
    // Format date: "2025-12-20" → "Dec 20"
    const d = new Date(r.day + 'T00:00:00');
    return d.toLocaleDateString('en-GB',
      { month: 'short', day: 'numeric' });
  });
  const values = overTime.map(r => r.count);

  new Chart($('timeChart'), {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Predictions',
        data: values,
        borderColor: '#1a6b3c',
        backgroundColor: 'rgba(26,107,60,.1)',
        borderWidth: 2.5,
        pointBackgroundColor: '#1a6b3c',
        pointRadius: 4,
        fill: true,
        tension: 0.3,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
          grid: { color: '#f0f0f0' }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

/* ── Chart 4: Average yield by crop ──────────────────────── */
function renderYieldChart(avgYield) {
  const labels = avgYield.map(r => r.crop);
  const values = avgYield.map(r => r.avg_yield);

  new Chart($('yieldChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Avg Yield (tons)',
        data: values,
        backgroundColor: COLORS.mixed.slice(0, labels.length),
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.parsed.y} tons/ha`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: '#f0f0f0' },
          ticks: { callback: v => `${v}t` }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

/* ── Chart 5: Risk flag distribution ─────────────────────── */
function renderRiskChart(riskSummary) {
  const labels = ['No Risks', '1 Risk', '2 Risks', '3+ Risks'];
  const values = [
    riskSummary.no_risk    || 0,
    riskSummary.one_risk   || 0,
    riskSummary.two_risk   || 0,
    riskSummary.three_plus || 0,
  ];
  const bgColors = ['#1a6b3c', '#f4a900', '#e07b00', '#d94f3d'];

  new Chart($('riskChart'), {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: bgColors,
        borderWidth: 2,
        borderColor: '#fff',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { padding: 16, font: FONT }
        },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed} predictions`
          }
        }
      }
    }
  });
}

/* ── Main: load all data and render ──────────────────────── */
async function loadDashboard() {
  try {
    const res  = await fetch(`${API}/api/analytics`,
                   { signal: AbortSignal.timeout(30000) });
    const data = await res.json();

    hide('loadingState');

    if (!data.success) {
      show('emptyState');
      return;
    }

    const analytics = data.analytics;

    if (analytics.total_predictions === 0) {
      show('emptyState');
      return;
    }

    // Render everything
    renderMetrics(analytics);
    if (analytics.by_crop.length)           renderCropChart(analytics.by_crop);
    if (analytics.by_state.length)          renderStateChart(analytics.by_state);
    if (analytics.over_time.length)         renderTimeChart(analytics.over_time);
    if (analytics.avg_yield_by_crop.length) renderYieldChart(analytics.avg_yield_by_crop);
    if (Object.keys(analytics.risk_summary).length)
                                            renderRiskChart(analytics.risk_summary);

    show('dashboardContent');

  } catch (err) {
    hide('loadingState');
    $('loadingState').innerHTML =
      `<div style="color:#d94f3d; padding:2rem;">
         ⚠️ Could not load analytics. The server may be waking up.
         <br><br>
         <a href="javascript:location.reload()"
            style="color:#1a6b3c; font-weight:700;">
           Try again
         </a>
       </div>`;
    show('loadingState');
  }
}

/* ── Init ────────────────────────────────────────────────── */
checkStatus();
loadDashboard();