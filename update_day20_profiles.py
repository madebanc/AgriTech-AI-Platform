"""Day 20 Task 2: saved farm profiles, one tap fill. Automated with backups."""
import re, shutil

PROFILE_KEYS = {
"en": {
    "profiles_title": "My saved farms",
    "profiles_pick": "Choose a saved farm",
    "profiles_empty": "No saved farms yet. Fill the form, then tap Save this farm.",
    "profiles_load": "Load farm",
    "profiles_save": "Save this farm",
    "profiles_delete": "Delete",
    "profiles_name_ph": "Name this farm",
    "profiles_saved": "Farm saved",
    "profiles_loaded": "Farm loaded"
},
"yo": {
    "profiles_title": "Àwọn ọkọ̀ mi tí a fi pamọ́",
    "profiles_pick": "Yan ọkọ̀ tí a fi pamọ́",
    "profiles_empty": "Kò sí ọkọ̀ tí a fi pamọ́. Kún unu fóọ̀ sì tẹ́ ọ̀nà Save this farm.",
    "profiles_load": "Gbé ọkọ̀ náà",
    "profiles_save": "Fi ọkọ̀ yìí pamọ́",
    "profiles_delete": "Pa rẹ́",
    "profiles_name_ph": "Fi orúkọ ọkọ̀ yìí",
    "profiles_saved": "A fi ọkọ̀ náà pamọ́",
    "profiles_loaded": "A gbé ọkọ̀ náà"
},
"ha": {
    "profiles_title": "Shanina da na aji",
    "profiles_pick": "Zaɓi shanin da aka aji",
    "profiles_empty": "Babu shanin da aka aji. Cika gurbin, sannan danna Save this farm.",
    "profiles_load": "Dauke shanin",
    "profiles_save": "Aji wannan shanin",
    "profiles_delete": "Soke",
    "profiles_name_ph": "Suna wannan shanin",
    "profiles_saved": "An aji shanin",
    "profiles_loaded": "An dauke shanin"
},
"ig": {
    "profiles_title": "Aka m aka m gi",
    "profiles_pick": "Horo aka m dị adịghị",
    "profiles_empty": "Enweghị aka m dị. Jisie ihe niile, mgbe ahụ pịa Save this farm.",
    "profiles_load": "Were aka m",
    "profiles_save": "Chebekwa aka m a",
    "profiles_delete": "Hapụ",
    "profiles_name_ph": "Nyere aka m a",
    "profiles_saved": "A chebekwa aka m",
    "profiles_loaded": "A were aka m"
}
}

# ── 1. translations ──
p = "docs/js/translations.js"
shutil.copy(p, p + ".day19_backup")
text = open(p, encoding="utf-8").read()
for lang in ["ig", "ha", "yo", "en"]:
    m = re.search(r'\n\s*' + lang + r'\s*:\s*\{', text)
    if not m:
        print(lang + " not found")
        continue
    start = m.start()
    nxt = len(text)
    for l2 in ["en", "yo", "ha", "ig"]:
        if l2 == lang:
            continue
        m2 = re.search(r'\n\s*' + l2 + r'\s*:\s*\{', text[m.end():])
        if m2:
            cand = m.end() + m2.start()
            if cand < nxt:
                nxt = cand
    block = text[start:nxt]
    if "profiles_title" in block:
        print(lang + " profile keys already present")
        continue
    ma = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not ma:
        print(lang + " anchor missing")
        continue
    add = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in PROFILE_KEYS[lang].items()])
    text = text[:start] + block[:ma.end()] + add + block[ma.end():] + text[nxt:]
    print(lang + " profile keys added: " + str(len(PROFILE_KEYS[lang])))
open(p, "w", encoding="utf-8").write(text)

# ── 2. app.js saved farm profiles ──
q = "docs/js/app.js"
shutil.copy(q, q + ".day19_backup")
js = open(q, encoding="utf-8").read()
if "saveCurrentProfile" in js:
    print("app.js profiles already present, skipped")
else:
    prof_js = r"""
/* Day 20: saved farm profiles, one tap fills the form */
var DAY20_KEY = "agritech_farm_profiles";
function day20T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function esc20(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (m) {
    return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m];
  });
}
function loadProfiles() {
  try {
    var raw = localStorage.getItem(DAY20_KEY);
    var arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch (e) { return []; }
}
function saveProfiles(list) {
  try { localStorage.setItem(DAY20_KEY, JSON.stringify(list)); } catch (e) {}
}
function profilePanel() {
  var existing = document.getElementById("profilePanel");
  if (existing) return existing;
  var form = document.getElementById("farmForm");
  if (!form) return null;
  var panel = document.createElement("div");
  panel.id = "profilePanel";
  panel.style.cssText = "background:#f0f7f2;border:1px solid #cfe3d6;border-radius:12px;padding:.9rem;margin-bottom:1.1rem;";
  form.insertBefore(panel, form.firstChild);
  return panel;
}
function renderProfiles() {
  var panel = profilePanel();
  if (!panel) return;
  var list = loadProfiles();
  var opts = '<option value="">' + (list.length ? esc20(day20T("profiles_pick", "Choose a saved farm")) : "") + '</option>';
  list.forEach(function (p) {
    opts += '<option value="' + esc20(p.id) + '">' + esc20(p.name) + " — " + esc20(p.crop) + " · " + esc20(p.state) + '</option>';
  });
  panel.innerHTML =
    '<div style="font-weight:800;color:#1a6b3c;margin-bottom:.5rem;">' + esc20(day20T("profiles_title", "My saved farms")) + '</div>'
    + '<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;">'
    + '<select id="profileSelect" style="flex:1;min-width:170px;padding:.55rem;border-radius:10px;border:1px solid #cbd5cc;">' + opts + '</select>'
    + '<button type="button" id="profileLoadBtn" style="padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#1a6b3c;color:#fff;border:none;border-radius:24px;cursor:pointer;">' + esc20(day20T("profiles_load", "Load farm")) + '</button>'
    + '</div>'
    + '<div style="display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin-top:.6rem;">'
    + '<input id="profileName" type="text" placeholder="' + esc20(day20T("profiles_name_ph", "Name this farm")) + '" style="flex:1;min-width:140px;padding:.55rem;border-radius:10px;border:1px solid #cbd5cc;">'
    + '<button type="button" id="profileSaveBtn" style="padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#fff;color:#1a6b3c;border:2px solid #1a6b3c;border-radius:24px;cursor:pointer;">' + esc20(day20T("profiles_save", "Save this farm")) + '</button>'
    + '<button type="button" id="profileDelBtn" style="padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#fff;color:#b91c1c;border:2px solid #b91c1c;border-radius:24px;cursor:pointer;">' + esc20(day20T("profiles_delete", "Delete")) + '</button>'
    + '</div>'
    + (list.length ? "" : '<small style="display:block;margin-top:.5rem;color:#555;">' + esc20(day20T("profiles_empty", "No saved farms yet. Fill the form, then tap Save this farm.")) + '</small>');
  var lb = document.getElementById("profileLoadBtn");
  var sb = document.getElementById("profileSaveBtn");
  var db = document.getElementById("profileDelBtn");
  if (lb) lb.addEventListener("click", loadProfile);
  if (sb) sb.addEventListener("click", saveCurrentProfile);
  if (db) db.addEventListener("click", deleteProfile);
}
function loadProfile() {
  var sel = document.getElementByById("profileSelect");
  if (!sel || !sel.value) { alert(day20T("profiles_empty", "No saved farms yet. Fill the form, then tap Save this farm.")); return; }
  var list = loadProfiles();
  var p = null;
  list.forEach(function (x) { if (x.id === sel.value) p = x; });
  if (!p) return;
  function set(id, v) { var el = document.getElementById(id); if (el) el.value = v; }
  set("crop", p.crop || "");
  set("state", p.state || "");
  set("farmSize", p.size || "");
  set("farmUnit", p.unit || "hectare");
  set("soilType", p.soil_type || "");
  set("soilPh", p.soil_ph || "");
  set("fertilizer", p.fertilizer_kg || "");
  if (p.rainfall_mm) set("rainfall", p.rainfall_mm);
  try { if (typeof updateSizeHelper === "function") updateSizeHelper(); } catch (e) {}
  try { if (typeof updateBagsHelper === "function") updateBagsHelper(); } catch (e) {}
  try { if (typeof applyDay17Static === "function") applyDay17Static(); } catch (e) {}
  var st = document.getElementById("state");
  if (st) { try { st.dispatchEvent(new Event("change")); } catch (e) {} }
  alert(day20T("profiles_loaded", "Farm loaded"));
}
function saveCurrentProfile() {
  function g(id) { return document.getElementById(id); }
  var nameEl = g("profileName");
  var name = nameEl ? nameEl.value.trim() : "";
  if (!name) { alert(day20T("profiles_name_ph", "Name this farm")); return; }
  var list = loadProfiles();
  var existing = null;
  list.forEach(function (x) { if (String(x.name).toLowerCase() === name.toLowerCase()) existing = x; });
  var cropEl = g("crop"), stateEl = g("state"), sizeEl = g("farmSize"), unitEl = g("farmUnit");
  var soilTypeEl = g("soilType"), soilPhEl = g("soilPh"), fertEl = g("fertilizer"), rainEl = g("rainfall");
  var profile = {
    id: existing ? existing.id : "pf-" + Date.now().toString(36),
    name: name,
    crop: cropEl ? cropEl.value : "",
    state: stateEl ? stateEl.value : "",
    size: sizeEl ? sizeEl.value : "",
    unit: unitEl ? unitEl.value : "hectare",
    soil_type: soilTypeEl ? soilTypeEl.value : "",
    soil_ph: soilPhEl ? soilPhEl.value : "",
    fertilizer_kg: fertEl ? fertEl.value : "",
    rainfall_mm: rainEl ? rainEl.value : "",
    updated_at: new Date().toISOString()
  };
  if (existing) {
    list = list.map(function (x) { return x.id === existing.id ? profile : x; });
  } else {
    list.unshift(profile);
  }
  saveProfiles(list);
  if (nameEl) nameEl.value = "";
  renderProfiles();
  var sel = document.getElementById("profileSelect");
  if (sel) sel.value = profile.id;
  alert(day20T("profiles_saved", "Farm saved"));
}
function deleteProfile() {
  var sel = document.getElementById("profileSelect");
  if (!sel || !sel.value) return;
  var list = loadProfiles().filter(function (x) { return x.id !== sel.value; });
  saveProfiles(list);
  renderProfiles();
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", function () { setTimeout(renderProfiles, 0); });
} else {
  setTimeout(renderProfiles, 0);
}
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day20hooked) {
    var _d20set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d20set(code);
      try { renderProfiles(); } catch (e) {}
      return r;
    };
    LANG.__day20hooked = true;
  }
} catch (e) {}
"""
    open(q, "a", encoding="utf-8").write("\n" + prof_js)
    print("app.js profiles appended")

print("Task 2 done")