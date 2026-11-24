/* AgriTech AI Platform — Profit Calculator frontend
Day 28 of 365. Profit and loss plus a combined farm report. */

const API_BASE = (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost")
? "http://127.0.0.1:5001"
: "https://agritech-ai-platform.onrender.com";

let costByCrop = {};
let marketPrices = {};
let lastReportText = "";

function naira(amount) {
const value = Number(amount || 0);
return "₦" + value.toLocaleString("en-NG", { maximumFractionDigits: 2 });
}

function escapeHtml(s) {
return String(s).replace(/[&<>"']/g, function (m) {
return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
});
}

function safeArray(value) {
return Array.isArray(value) ? value : [];
}

function fieldText(value, fallback) {
const text = String(value === undefined || value === null ? "" : value).trim();
return text || fallback;
}

function tinyDate(value) {
if (!value) return "No date";
return String(value).slice(0, 10);
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
if (price && !field.value) {
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
html += '<tr><td>Expected yield</td><td>' + data.yield_kg.toLocaleString() + ' kg</td></tr>';
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

async function fetchJson(path) {
try {
const res = await fetch(API_BASE + path);
if (!res.ok) return null;
const data = await res.json();
return data && data.success ? data : null;
} catch (err) {
console.log("Report fetch failed:", path, err);
return null;
}
}

function tableFrom(headers, rows) {
if (!rows.length) return '<p class="empty">Nothing recorded yet.</p>';
let html = "<table><thead><tr>";
headers.forEach(function (title) {
html += "<th>" + escapeHtml(title) + "</th>";
});
html += "</tr></thead><tbody>";
rows.forEach(function (row) {
html += "<tr>";
row.forEach(function (cell) {
html += "<td>" + cell + "</td>";
});
html += "</tr>";
});
html += "</tbody></table>";
return html;
}

async function buildFarmReport() {
const statusEl = document.getElementById("reportStatus");
const box = document.getElementById("report");
statusEl.textContent = "Loading your farm data...";

const results = await Promise.all([
fetchJson("/api/activity?limit=5"),
fetchJson("/api/expenses?limit=5"),
fetchJson("/api/profit"),
fetchJson("/api/journal?limit=3")
]);

const activityRes = results[0];
const expenseRes = results[1];
const profitRes = results[2];
const journalRes = results[3];

if (!activityRes && !expenseRes && !profitRes && !journalRes) {
statusEl.textContent = "Could not reach the server. Connect to the internet and try again.";
box.innerHTML = '<p class="empty">Your saved farm data will appear here when the server is available.</p>';
return;
}

const activities = safeArray(activityRes && activityRes.activities);
const expenses = safeArray(expenseRes && expenseRes.expenses);
const cropRows = safeArray(profitRes && profitRes.crops);
const notes = safeArray(journalRes && journalRes.entries);

const activityRows = activities.slice(0, 5).map(function (a) {
return [
escapeHtml(tinyDate(a.activity_date)),
escapeHtml(fieldText(a.activity_type, "note")),
escapeHtml(fieldText(a.crop, "Not set")),
escapeHtml(fieldText(a.notes, fieldText(a.quantity, "No details")))
];
});

const expenseRows = expenses.slice(0, 5).map(function (e) {
return [
escapeHtml(tinyDate(e.expense_date)),
escapeHtml(fieldText(e.item, fieldText(e.category, "other"))),
escapeHtml(fieldText(e.crop, "Not set")),
naira(e.amount_ngn)
];
});

const costRows = cropRows.map(function (c) {
return [
escapeHtml(fieldText(c.crop, "Not set")),
naira(c.total_cost),
naira(c.market_price_per_kg)
];
});

const noteRows = notes.slice(0, 3).map(function (n) {
const note = fieldText(n.notes, fieldText(n.note, "No note"));
return [
escapeHtml(tinyDate(n.entry_date || n.date || n.created_at)),
escapeHtml(fieldText(n.crop, "Not set")),
escapeHtml(note.slice(0, 120))
];
});

let html = '<div class="report-section">';
html += '<h3>Work in the farm</h3>';
html += tableFrom(["Date", "Activity", "Crop", "Details"], activityRows);
html += '</div>';

html += '<div class="report-section">';
html += '<h3>Money spent</h3>';
html += tableFrom(["Date", "Item", "Crop", "Amount"], expenseRows);
html += '</div>';

html += '<div class="report-section">';
html += '<h3>Crop cost summary</h3>';
html += tableFrom(["Crop", "Total cost", "Market price per kg"], costRows);
html += '</div>';

html += '<div class="report-section">';
html += '<h3>Journal notes</h3>';
html += tableFrom(["Date", "Crop", "Note"], noteRows);
html += '</div>';

html += '<p class="muted">Showing the latest 5 activities, 5 expenses, all crop costs and 3 journal notes.</p>';

let text = "AGRITECH AI FARM REPORT\n";
text += "Generated: " + new Date().toLocaleString("en-NG") + "\n\n";

text += "WORK IN THE FARM\n";
if (activities.length === 0) {
text += "No activities recorded yet.\n";
} else {
activities.slice(0, 5).forEach(function (a) {
text += tinyDate(a.activity_date) + " | " + fieldText(a.activity_type, "note") + " | " +
fieldText(a.crop, "Not set") + " | " + fieldText(a.notes, fieldText(a.quantity, "No details")) + "\n";
});
}
text += "\n";

text += "MONEY SPENT\n";
if (expenses.length === 0) {
text += "No expenses recorded yet.\n";
} else {
expenses.slice(0, 5).forEach(function (e) {
text += tinyDate(e.expense_date) + " | " + fieldText(e.item, fieldText(e.category, "other")) + " | " +
fieldText(e.crop, "Not set") + " | " + naira(e.amount_ngn) + "\n";
});
}
text += "\n";

text += "CROP COST SUMMARY\n";
if (cropRows.length === 0) {
text += "No crop costs recorded yet.\n";
} else {
cropRows.forEach(function (c) {
text += fieldText(c.crop, "Not set") + " | total cost " + naira(c.total_cost) +
" | market price " + naira(c.market_price_per_kg) + " per kg\n";
});
}
text += "\n";

text += "JOURNAL NOTES\n";
if (notes.length === 0) {
text += "No journal notes recorded yet.\n";
} else {
notes.slice(0, 3).forEach(function (n) {
text += tinyDate(n.entry_date || n.date || n.created_at) + " | " +
fieldText(n.crop, "Not set") + " | " +
fieldText(n.notes, fieldText(n.note, "No note")).slice(0, 120) + "\n";
});
}
text += "\nBuilt by Daniel Oyanogbezina, AgriTech AI Platform, Day 28 of 365.\n";

box.innerHTML = html;
lastReportText = text;
document.getElementById("downloadBtn").disabled = false;
document.getElementById("printBtn").disabled = false;
statusEl.textContent = "Report ready. Download it or print it for your records.";
}

function downloadReport() {
if (!lastReportText) {
alert("Build your farm report first.");
return;
}
const blob = new Blob([lastReportText], { type: "text/plain;charset=utf-8" });
const url = URL.createObjectURL(blob);
const link = document.createElement("a");
link.href = url;
link.download = "agritech-farm-report-" + new Date().toISOString().slice(0, 10) + ".txt";
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
URL.revokeObjectURL(url);
}

function printReport() {
if (!lastReportText) {
alert("Build your farm report first.");
return;
}
window.print();
}

document.addEventListener("DOMContentLoaded", function () {
document.getElementById("crop").addEventListener("change", function () {
updateCostField();
updatePriceField();
});
document.getElementById("calcBtn").addEventListener("click", calculateProfit);
document.getElementById("refreshBtn").addEventListener("click", loadCosts);
document.getElementById("reportBtn").addEventListener("click", buildFarmReport);
document.getElementById("downloadBtn").addEventListener("click", downloadReport);
document.getElementById("printBtn").addEventListener("click", printReport);
loadCosts();
});