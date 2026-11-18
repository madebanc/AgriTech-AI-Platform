/* AgriTech AI Platform — Profit Calculator frontend
Day 26 of 365. Combines expenses with yield and price to show profit/loss. */

const API_BASE = (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost")
  ? "http://127.0.0.1:5001"
  : "https://agritech-ai-platform.onrender.com";

let costByCrop = {};
let marketPrices = {};

function naira(amount) {
  const value = Number(amount || 0);
  return "₦" + value.toLocaleString("en-NG", { maximumFractionDigits: 2 });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, function (m) {
    return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
  });
}

async function loadCosts() {
  const statusEl = document.getElementById("syncStatus");
  try {
    const res = await fetch(API_BASE + "/api/profit");
    const data = await res.json();
    if (data.success) {
      costByCrop = {};
      data.crops.forEach(function (c) {
        costByCrop[c.crop] = c.total_cost;
      });
      marketPrices = data.market_prices || {};
      statusEl.innerHTML = '<span class="status-dot">Online.</span> Expense data loaded. Total recorded: ' + naira(data.total_expenses);
      renderCostTable(data.crops);
      renderPills(data);
      updateCostField();
      updatePriceField();
    } else {
      statusEl.innerHTML = '<span class="status-dot">Could not load expenses.</span>';
    }
  } catch (err) {
    statusEl.innerHTML = '<span class="status-dot">Offline.</span> Could not reach server.';
    console.log("Load costs failed:", err);
  }
}

function renderPills(data) {
  const box = document.getElementById("statPills");
  let html = '<span class="pill total">Total expenses: ' + naira(data.total_expenses) + '</span>';
  html += '<span class="pill">Crops tracked: ' + data.crops.length + '</span>';
  box.innerHTML = html;
}

function renderCostTable(crops) {
  const box = document.getElementById("costTable");
  let html = "<table><thead><tr><th>Crop</th><th>Total cost (₦)</th><th>Market price (₦/kg)</th></tr></thead><tbody>";
  crops.forEach(function (c) {
    html += "<tr><td>" + escapeHtml(c.crop) + "</td><td>" + naira(c.total_cost) + "</td><td>" + naira(c.market_price_per_kg) + "</td></tr>";
  });
  html += "</tbody></table>";
  box.innerHTML = html;
}

function updateCostField() {
  const crop = document.getElementById("crop").value;
  const field = document.getElementById("totalCost");
  field.value = (costByCrop[crop] || 0).toFixed(2);
}

function updatePriceField() {
  const crop = document.getElementById("crop").value;
  const field = document.getElementById("sellingPrice");
  const price = marketPrices[crop];
  if (price) {
    field.value = price;
  }
}

async function calculateProfit() {
  const crop = document.getElementById("crop").value;
  const yieldKg = document.getElementById("expectedYield").value;
  const price = document.getElementById("sellingPrice").value;
  const cost = document.getElementById("totalCost").value;
  const resultBox = document.getElementById("result");

  if (!yieldKg || Number(yieldKg) <= 0) {
    alert("Please enter an expected yield greater than zero.");
    return;
  }
  if (!price || Number(price) <= 0) {
    alert("Please enter a selling price greater than zero.");
    return;
  }

  try {
    const res = await fetch(API_BASE + "/api/profit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        crop: crop,
        yield_kg: Number(yieldKg),
        price_per_kg: Number(price),
        total_cost: Number(cost || 0)
      })
    });
    const data = await res.json();
    if (data.success) {
      const isLoss = data.profit < 0;
      const cls = isLoss ? "loss" : "profit";
      let html = '<div class="result-box ' + (isLoss ? 'loss' : '') + '">';
      html += '<span class="type-badge ' + cls + '">' + escapeHtml(data.verdict) + '</span> ';
      html += '<strong>' + escapeHtml(data.crop) + '</strong><br><br>';
      html += '<table>';
      html += '<tr><td>Expected yield</td><td>' + Number(data.yield_kg).toLocaleString() + ' kg</td></tr>';
      html += '<tr><td>Selling price</td><td>' + naira(data.price_per_kg) + ' / kg</td></tr>';
      html += '<tr><td><strong>Revenue</strong></td><td><strong>' + naira(data.revenue) + '</strong></td></tr>';
      html += '<tr><td>Total cost</td><td>' + naira(data.total_cost) + '</td></tr>';
      html += '<tr><td><strong>Profit / Loss</strong></td><td><strong>' + naira(data.profit) + '</strong></td></tr>';
      html += '<tr><td>Profit margin</td><td>' + data.profit_margin_pct + '%</td></tr>';
      html += '</table>';
      html += '</div>';
      resultBox.innerHTML = html;
    } else {
      resultBox.innerHTML = "<p>Could not calculate. Please try again.</p>";
    }
  } catch (err) {
    resultBox.innerHTML = "<p>Server unreachable. Please check your connection.</p>";
    console.log("Calculate failed:", err);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("crop").addEventListener("change", function () {
    updateCostField();
    updatePriceField();
  });
  document.getElementById("calcBtn").addEventListener("click", calculateProfit);
  document.getElementById("refreshBtn").addEventListener("click", loadCosts);
  loadCosts();
});