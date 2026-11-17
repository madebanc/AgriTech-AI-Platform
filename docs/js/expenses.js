/* AgriTech AI Platform — Cost Tracker frontend
Day 25 of 365. Offline first. Phone saves locally, syncs when online. */

const API_BASE = (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost")
? "http://127.0.0.1:5001"
: "https://agritech-ai-platform.onrender.com";

const LOCAL_KEY = "agritech_expenses_local";
const QUEUE_KEY = "agritech_expenses_queue";

function loadLocal() {
try { return JSON.parse(localStorage.getItem(LOCAL_KEY) || "[]"); }
catch (e) { return []; }
}

function saveLocal(entries) {
localStorage.setItem(LOCAL_KEY, JSON.stringify(entries));
}

function loadQueue() {
try { return JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]"); }
catch (e) { return []; }
}

function saveQueue(queue) {
localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

function naira(amount) {
const value = Number(amount || 0);
return "₦" + value.toLocaleString("en-NG", { maximumFractionDigits: 2 });
}

function updateStatus() {
const el = document.getElementById("syncStatus");
const queue = loadQueue();
if (!navigator.onLine) {
el.innerHTML = '<span class="status-dot">Offline mode.</span> Expenses save on this phone and sync later. Queued: ' + queue.length;
return;
}
if (queue.length === 0) {
el.innerHTML = '<span class="status-dot">Online.</span> All expenses synced.';
} else {
el.innerHTML = '<span class="status-dot">Online.</span> ' + queue.length + ' expense(s) waiting to sync. Press Sync now.';
}
}

function renderStats(entries) {
const box = document.getElementById("statPills");
let total = 0;
const byCategory = {};
entries.forEach(function (e) {
const amount = Number(e.amount_ngn || 0);
total += amount;
const c = e.category || "other";
byCategory[c] = (byCategory[c] || 0) + amount;
});
let html = '<span class="pill total">Total spent: ' + naira(total) + '</span>';
html += '<span class="pill">Entries: ' + entries.length + '</span>';
Object.keys(byCategory).forEach(function (c) {
html += '<span class="pill">' + c + ': ' + naira(byCategory[c]) + '</span>';
});
const q = loadQueue();
if (q.length > 0) html += '<span class="pill">Queued: ' + q.length + '</span>';
box.innerHTML = html;
}

function escapeHtml(s) {
return String(s).replace(/[&<>"']/g, function (m) {
return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
});
}

function renderEntries() {
const local = loadLocal();
const box = document.getElementById("entries");
renderStats(local);
if (local.length === 0) {
box.innerHTML = "<p>No expenses recorded yet. Record your first cost above.</p>";
return;
}
let html = "";
local.forEach(function (e) {
html += '<div class="entry">'
+ '<span class="type-badge">' + escapeHtml(e.category || "other") + '</span> '
+ '<strong>' + naira(e.amount_ngn) + '</strong> · ' + escapeHtml(e.item || "Farm cost")
+ '<br><small>' + escapeHtml(e.expense_date || "no date") + ' · ' + escapeHtml(e.farm_name || "My Farm")
+ ' · ' + escapeHtml(e.crop || "") + ' · ' + escapeHtml(e.source || "local") + '</small>'
+ (e.notes ? '<br><small>' + escapeHtml(e.notes) + '</small>' : '')
+ '<br><button class="btn secondary" style="padding:.3rem .8rem;font-size:.85rem;" onclick="deleteExpense(\'' + e.id + '\')">Delete</button>'
+ '</div>';
});
box.innerHTML = html;
}

function collectForm() {
return {
farmer_name: document.getElementById("farmerName").value.trim(),
farm_name: document.getElementById("farmName").value.trim() || "My Farm",
crop: document.getElementById("crop").value,
category: document.getElementById("category").value,
item: document.getElementById("item").value.trim(),
amount_ngn: document.getElementById("amount").value,
expense_date: document.getElementById("expenseDate").value,
notes: document.getElementById("notes").value.trim(),
source: navigator.onLine ? "online" : "offline"
};
}

function makeLocalEntry(payload) {
return {
id: "local-" + Date.now().toString(36),
farmer_name: payload.farmer_name,
farm_name: payload.farm_name,
crop: payload.crop,
category: payload.category,
item: payload.item,
amount_ngn: Number(payload.amount_ngn || 0),
expense_date: payload.expense_date || new Date().toISOString().slice(0, 10),
notes: payload.notes,
source: payload.source,
created_at: new Date().toISOString()
};
}

async function saveExpense() {
const payload = collectForm();
const amount = Number(payload.amount_ngn);
if (!amount || amount <= 0) {
alert("Please enter an amount greater than zero.");
return;
}
const local = loadLocal();
const entry = makeLocalEntry(payload);
local.unshift(entry);
saveLocal(local);

if (!navigator.onLine) {
const queue = loadQueue();
queue.push(payload);
saveQueue(queue);
renderEntries();
updateStatus();
alert("Saved offline on your phone. It will sync when you are back online.");
return;
}

try {
const res = await fetch(API_BASE + "/api/expenses", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify(payload)
});
const data = await res.json();
if (data.success && data.entry) {
entry.id = data.entry.id;
entry.amount_ngn = data.entry.amount_ngn;
entry.source = "synced";
saveLocal(local);
} else {
const queue = loadQueue();
queue.push(payload);
saveQueue(queue);
}
} catch (err) {
const queue = loadQueue();
queue.push(payload);
saveQueue(queue);
}
renderEntries();
updateStatus();
}

async function syncNow() {
const queue = loadQueue();
if (queue.length === 0) {
await pullServer();
updateStatus();
return;
}
if (!navigator.onLine) {
alert("You are offline. Reconnect then press Sync now.");
return;
}
const remaining = [];
for (const payload of queue) {
try {
const res = await fetch(API_BASE + "/api/expenses", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify(payload)
});
const data = await res.json();
if (!data.success) remaining.push(payload);
} catch (err) {
remaining.push(payload);
}
}
saveQueue(remaining);
await pullServer();
renderEntries();
updateStatus();
alert(remaining.length === 0 ? "All expenses synced." : remaining.length + " still queued. Try again.");
}

async function pullServer() {
if (!navigator.onLine) return;
try {
const res = await fetch(API_BASE + "/api/expenses?limit=100");
const data = await res.json();
if (data.success && Array.isArray(data.expenses)) {
const serverEntries = data.expenses.map(function (e) {
e.source = "synced";
return e;
});
const localOnly = loadLocal().filter(function (e) {
return String(e.id).indexOf("local-") === 0;
});
saveLocal(localOnly.concat(serverEntries).slice(0, 100));
renderEntries();
}
} catch (err) {
console.log("Server pull skipped:", err);
}
}

function deleteExpense(id) {
const local = loadLocal().filter(function (e) { return e.id !== id; });
saveLocal(local);
renderEntries();
updateStatus();
}

window.saveExpense = saveExpense;
window.syncNow = syncNow;
window.deleteExpense = deleteExpense;

document.addEventListener("DOMContentLoaded", function () {
document.getElementById("expenseDate").value = new Date().toISOString().slice(0, 10);
document.getElementById("saveBtn").addEventListener("click", saveExpense);
document.getElementById("syncBtn").addEventListener("click", syncNow);
window.addEventListener("online", function () { updateStatus(); syncNow(); });
window.addEventListener("offline", updateStatus);
renderEntries();
updateStatus();
pullServer();
});