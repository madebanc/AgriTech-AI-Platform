/* AgriTech AI Platform — Farm Activity Log frontend
Day 24 of 365. Offline first. Phone saves locally, syncs when online. */

const API_BASE = (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost")
? "http://127.0.0.1:5001"
: "https://agritech-ai-platform.onrender.com";

const LOCAL_KEY = "agritech_activity_local";
const QUEUE_KEY = "agritech_activity_queue";

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

function updateStatus() {
const el = document.getElementById("syncStatus");
const queue = loadQueue();
if (!navigator.onLine) {
el.innerHTML = '<span class="status-dot">Offline mode.</span> Activities save on this phone and sync later. Queued: ' + queue.length;
return;
}
if (queue.length === 0) {
el.innerHTML = '<span class="status-dot">Online.</span> All activities synced.';
} else {
el.innerHTML = '<span class="status-dot">Online.</span> ' + queue.length + ' activit(ies) waiting to sync. Press Sync now.';
}
}

function renderStats(entries) {
const box = document.getElementById("statPills");
const byType = {};
entries.forEach(function (e) {
const t = e.activity_type || "note";
byType[t] = (byType[t] || 0) + 1;
});
let html = '<span class="pill">Total: ' + entries.length + '</span>';
Object.keys(byType).forEach(function (t) {
html += '<span class="pill">' + t + ': ' + byType[t] + '</span>';
});
const q = loadQueue();
if (q.length > 0) html += '<span class="pill">Queued: ' + q.length + '</span>';
box.innerHTML = html;
}

function renderEntries() {
const local = loadLocal();
const box = document.getElementById("entries");
renderStats(local);
if (local.length === 0) {
box.innerHTML = "<p>No activities logged yet. Log your first activity above.</p>";
return;
}
let html = "";
local.forEach(function (e) {
html += '<div class="entry">'
+ '<span class="type-badge">' + escapeHtml(e.activity_type || "note") + '</span> '
+ '<strong>' + escapeHtml(e.farm_name || "My Farm") + '</strong> · ' + escapeHtml(e.crop || "")
+ '<br><small>' + escapeHtml(e.activity_date || "no date") + ' · ' + escapeHtml(e.source || "local") + '</small>'
+ (e.quantity ? '<br><small>Detail: ' + escapeHtml(e.quantity) + '</small>' : '')
+ (e.notes ? '<br><small>' + escapeHtml(e.notes) + '</small>' : '')
+ '<br><button class="btn secondary" style="padding:.3rem .8rem;font-size:.85rem;" onclick="deleteActivity(\'' + e.id + '\')">Delete</button>'
+ '</div>';
});
box.innerHTML = html;
}

function escapeHtml(s) {
return String(s).replace(/[&<>"']/g, function (m) {
return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
});
}

function collectForm() {
return {
farmer_name: document.getElementById("farmerName").value.trim(),
farm_name: document.getElementById("farmName").value.trim() || "My Farm",
crop: document.getElementById("crop").value,
activity_type: document.getElementById("activityType").value,
activity_date: document.getElementById("activityDate").value,
quantity: document.getElementById("quantity").value.trim(),
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
activity_type: payload.activity_type,
activity_date: payload.activity_date || new Date().toISOString().slice(0, 10),
quantity: payload.quantity,
notes: payload.notes,
source: payload.source,
created_at: new Date().toISOString()
};
}

async function saveActivity() {
const payload = collectForm();
if (!payload.activity_type) {
alert("Please choose what you did.");
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
const res = await fetch(API_BASE + "/api/activity", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify(payload)
});
const data = await res.json();
if (data.success && data.entry) {
entry.id = data.entry.id;
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
const res = await fetch(API_BASE + "/api/activity", {
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
alert(remaining.length === 0 ? "All activities synced." : remaining.length + " still queued. Try again.");
}

async function pullServer() {
if (!navigator.onLine) return;
try {
const res = await fetch(API_BASE + "/api/activity?limit=100");
const data = await res.json();
if (data.success && Array.isArray(data.activities)) {
const serverEntries = data.activities.map(function (e) {
e.source = "synced";
return e;
});
const localOnly = loadLocal().filter(function (e) {
return String(e.id).indexOf("local-") === 0;
});
const merged = localOnly.concat(serverEntries).slice(0, 100);
saveLocal(merged);
renderEntries();
}
} catch (err) {
console.log("Server pull skipped:", err);
}
}

function deleteActivity(id) {
const local = loadLocal().filter(function (e) { return e.id !== id; });
saveLocal(local);
renderEntries();
updateStatus();
}

window.saveActivity = saveActivity;
window.syncNow = syncNow;
window.deleteActivity = deleteActivity;

document.addEventListener("DOMContentLoaded", function () {
document.getElementById("activityDate").value = new Date().toISOString().slice(0, 10);
document.getElementById("saveBtn").addEventListener("click", saveActivity);
document.getElementById("syncBtn").addEventListener("click", syncNow);
window.addEventListener("online", function () { updateStatus(); syncNow(); });
window.addEventListener("offline", updateStatus);
renderEntries();
updateStatus();
pullServer();
});