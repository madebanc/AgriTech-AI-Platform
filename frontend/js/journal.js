/* AgriTech AI Platform — Farm Journal frontend
   Day 13 of 365. Offline first. Phone saves locally, syncs when online. */

const API_BASE = (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost")
  ? "http://127.0.0.1:5001"
  : "https://agritech-ai-platform.onrender.com";

const LOCAL_KEY = "agritech_journal_local";
const QUEUE_KEY = "agritech_journal_queue";

const NIGERIAN_STATES = ["Abia","Adamawa","Akwa Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu","FCT Abuja","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Lagos","Nasarawa","Niger","Ogun","Ondo","Osun","Oyo","Plateau","Rivers","Sokoto","Taraba","Yobe","Zamfara"];

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
    el.innerHTML = '<span class="status-dot">Offline mode.</span> Farms save on this phone and sync later. Queued: ' + queue.length;
    return;
  }
  if (queue.length === 0) {
    el.innerHTML = '<span class="status-dot">Online.</span> All farms synced.';
  } else {
    el.innerHTML = '<span class="status-dot">Online.</span> ' + queue.length + ' farm(s) waiting to sync. Press Sync now.';
  }
}

function renderStats(entries) {
  const box = document.getElementById("statPills");
  const byCrop = {};
  entries.forEach(function (e) {
    const c = e.crop || "Unknown";
    byCrop[c] = (byCrop[c] || 0) + 1;
  });
  let html = '<span class="pill">Total: ' + entries.length + '</span>';
  Object.keys(byCrop).forEach(function (c) {
    html += '<span class="pill">' + c + ': ' + byCrop[c] + '</span>';
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
    box.innerHTML = "<p>No farms saved yet. Add your first farm above.</p>";
    return;
  }
  let html = "";
  local.forEach(function (e) {
    html += '<div class="entry">'
      + '<strong>' + escapeHtml(e.farm_name || "My Farm") + '</strong> · ' + escapeHtml(e.crop || "")
      + '<br><small>' + escapeHtml(e.state || "") + ' · ' + escapeHtml(String(e.size_hectares || "")) + ' ha · '
      + escapeHtml(e.planting_date || "no date") + ' · ' + escapeHtml(e.source || "local") + '</small>'
      + '<br><small>' + escapeHtml(e.notes || "") + '</small>'
      + '<br><button class="btn secondary" style="padding:.3rem .8rem;font-size:.85rem;" onclick="deleteFarm(\'' + e.id + '\')">Delete</button>'
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
    state: document.getElementById("state").value,
    size_hectares: parseFloat(document.getElementById("size").value || "0"),
    planting_date: document.getElementById("plantingDate").value,
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
    state: payload.state,
    size_hectares: payload.size_hectares,
    planting_date: payload.planting_date,
    notes: payload.notes,
    source: payload.source,
    created_at: new Date().toISOString()
  };
}

async function saveFarm() {
  const payload = collectForm();
  if (!payload.farm_name) {
    alert("Please enter a farm name.");
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
    const res = await fetch(API_BASE + "/api/journal", {
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
      const res = await fetch(API_BASE + "/api/journal", {
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
  alert(remaining.length === 0 ? "All farms synced." : remaining.length + " still queued. Try again.");
}

async function pullServer() {
  if (!navigator.onLine) return;
  try {
    const res = await fetch(API_BASE + "/api/journal?limit=50");
    const data = await res.json();
    if (data.success && Array.isArray(data.entries)) {
      const serverEntries = data.entries.map(function (e) {
        e.source = "synced";
        return e;
      });
      const localOnly = loadLocal().filter(function (e) {
        return String(e.id).indexOf("local-") === 0;
      });
      const merged = localOnly.concat(serverEntries).slice(0, 50);
      saveLocal(merged);
      renderEntries();
    }
  } catch (err) {
    console.log("Server pull skipped:", err);
  }
}

function deleteFarm(id) {
  const local = loadLocal().filter(function (e) { return e.id !== id; });
  saveLocal(local);
  renderEntries();
  updateStatus();
}

window.saveFarm = saveFarm;
window.syncNow = syncNow;
window.deleteFarm = deleteFarm;

document.addEventListener("DOMContentLoaded", function () {
  const stateSel = document.getElementById("state");
  NIGERIAN_STATES.forEach(function (s) {
    const opt = document.createElement("option");
    opt.value = s;
    opt.textContent = s;
    stateSel.appendChild(opt);
  });
  document.getElementById("saveBtn").addEventListener("click", saveFarm);
  document.getElementById("syncBtn").addEventListener("click", syncNow);
  window.addEventListener("online", function () { updateStatus(); syncNow(); });
  window.addEventListener("offline", updateStatus);
  renderEntries();
  updateStatus();
  pullServer();
});