"""Day 23 Task 2: monthly task checklist with ticks. Automated with backups."""
import re, shutil

CHECK_KEYS = {
"en": {
    "check_title": "Tasks for this month",
    "check_done": "Done",
    "check_reset": "Reset",
    "check_progress": "{done} of {total} done",
    "check_tick_first": "Tick tasks as you finish them",
    "check_empty": "Make a prediction to load this month tasks"
},
"yo": {
    "check_title": "Ise fun osu yi",
    "check_done": "Ti pari",
    "check_reset": "Tun bere",
    "check_progress": "{done} ninu {total} ti pari",
    "check_tick_first": "Samisi bi o se n pari won",
    "check_empty": "Se asotele lati gba ise osu yi"
},
"ha": {
    "check_title": "Ayyukan wannan wata",
    "check_done": "An gama",
    "check_reset": "Sake farawa",
    "check_progress": "{done} daga {total} an gama",
    "check_tick_first": "Alama ayyuka yayin da ka gama su",
    "check_empty": "Yi hasashe don loda ayyukan wannan wata"
},
"ig": {
    "check_title": "Oru maka onwa a",
    "check_done": "Emechara",
    "check_reset": "Malite ozo",
    "check_progress": "{done} n'ime {total} emechara",
    "check_tick_first": "Kanye ka i na emecha ha",
    "check_empty": "Buo amuma iji budata oru onwa a"
}
}

# ── 1. translations ──
p = "docs/js/translations.js"
shutil.copy(p, p + ".day22_backup")
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
    if "check_title" in block:
        print(lang + " check keys already present")
        continue
    ma = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not ma:
        print(lang + " anchor missing")
        continue
    add = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in CHECK_KEYS[lang].items()])
    text = text[:start] + block[:ma.end()] + add + block[ma.end():] + text[nxt:]
    print(lang + " check keys added: " + str(len(CHECK_KEYS[lang])))
open(p, "w", encoding="utf-8").write(text)

# ── 2. app.js checklist ──
q = "docs/js/app.js"
shutil.copy(q, q + ".day22_backup")
js = open(q, encoding="utf-8").read()
if "renderChecklist" in js:
    print("app.js checklist already present, skipped")
else:
    check_js = r"""
/* Day 23: monthly task checklist with ticks, offline on phone */
function day23T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function esc23(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (m) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m];
  });
}
function checkKey(crop, month) {
  return "agritech_checks_" + crop + "_" + month;
}
function loadChecks(crop, month) {
  try {
    var raw = localStorage.getItem(checkKey(crop, month));
    var arr = raw ? JSON.parse(raw) : null;
    if (Array.isArray(arr)) return arr;
  } catch (e) {}
  return [false, false, false];
}
function saveChecks(crop, month, arr) {
  try { localStorage.setItem(checkKey(crop, month), JSON.stringify(arr)); } catch (e) {}
}
function buildTasks(calendarData, tip) {
  var cal = calendarData && calendarData.calendar ? calendarData.calendar : null;
  if (!cal) return [];
  var tasks = [];
  if (cal.this_month && cal.this_month.task) tasks.push(cal.this_month.task);
  if (cal.next_month && cal.next_month.task) tasks.push(cal.next_month.task);
  if (tip) tasks.push(tip.replace(/^Best selling months:\s*/i, "").replace(/^Best time to sell:\s*/i, ""));
  return tasks.slice(0, 3);
}
function removeChecklist() {
  var el = document.getElementById("checkPanel");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function renderChecklist(crop, calendarData, tip) {
  removeChecklist();
  try { window.__day23ctx = { crop: crop, cal: calendarData, tip: tip }; } catch (e) {}
  var section = document.getElementById("resultsSection");
  if (!section || !crop) return;
  var cal = calendarData && calendarData.calendar ? calendarData.calendar : null;
  if (!cal) return;
  var month = cal.month || "";
  var tasks = buildTasks(calendarData, tip);
  if (!tasks.length) return;
  var checks = loadChecks(crop, month);
  while (checks.length < tasks.length) checks.push(false);
  checks = checks.slice(0, tasks.length);
  var done = checks.filter(function (x) { return x; }).length;
  var card = document.createElement("div");
  card.id = "checkPanel";
  card.style.cssText = "background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:1rem;margin:1rem 0;";
  var rows = "";
  tasks.forEach(function (t, i) {
    var c = checks[i] ? "checked" : "";
    rows += '<label style="display:flex;gap:.6rem;align-items:flex-start;padding:.55rem;border:1px solid #eef2ee;border-radius:10px;margin:.45rem 0;cursor:pointer;background:' + (checks[i] ? "#f0fdf4" : "#fff") + ';">'
      + '<input type="checkbox" data-i="' + i + '" ' + c + ' style="width:20px;height:20px;margin-top:2px;accent-color:#1a6b3c;">'
      + '<span style="flex:1;">' + esc23(t) + (checks[i] ? ' <strong style="color:#1a6b3c;">' + esc23(day23T("check_done", "Done")) + '</strong>' : "") + '</span></label>';
  });
  var pct = tasks.length ? Math.round((done / tasks.length) * 100) : 0;
  var bar = '<div style="background:#eef2ee;border-radius:999px;height:10px;overflow:hidden;margin:.6rem 0;">'
    + '<div style="height:100%;width:' + pct + '%;background:#1a6b3c;"></div></div>';
  card.innerHTML =
    '<div style="font-weight:800;color:#1a6b3c;">' + esc23(day23T("check_title", "Tasks for this month")) + '</div>'
    + '<div style="font-size:.9rem;color:#555;margin:.25rem 0 .3rem;">' + esc23(day23T("check_tick_first", "Tick tasks as you finish them")) + '</div>'
    + bar
    + '<div style="font-size:.9rem;font-weight:700;margin-bottom:.3rem;">' + esc23(day23T("check_progress", "{done} of {total} done").replace("{done}", done).replace("{total}", tasks.length)) + '</div>'
    + rows
    + '<div style="margin-top:.6rem;"><button type="button" id="checkResetBtn" style="padding:.45rem 1rem;font-size:.85rem;font-weight:800;background:#fff;color:#b91c1c;border:2px solid #b91c1c;border-radius:24px;cursor:pointer;">' + esc23(day23T("check_reset", "Reset")) + '</button></div>';
  section.appendChild(card);
  card.querySelectorAll('input[type="checkbox"]').forEach(function (box) {
    box.addEventListener("change", function () {
      var idx = parseInt(box.getAttribute("data-i"), 10);
      var cur = loadChecks(crop, month);
      cur[idx] = box.checked;
      saveChecks(crop, month, cur);
      renderChecklist(crop, calendarData, tip);
    });
  });
  var rb = document.getElementById("checkResetBtn");
  if (rb) rb.addEventListener("click", function () {
    saveChecks(crop, month, [false, false, false]);
    renderChecklist(crop, calendarData, tip);
  });
}
/* language refresh for checklist */
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day23hooked) {
    var _d23set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d23set(code);
      try {
        var ctx = window.__day23ctx;
        if (ctx && ctx.crop) renderChecklist(ctx.crop, ctx.cal, ctx.tip);
      } catch (e) {}
      return r;
    };
    LANG.__day23hooked = true;
  }
} catch (e) {}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day23checkhook) {
  var _day23render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day23render.apply(this, arguments);
    try {
      var crop = result && result.crop;
      var tip = result && result.advice && result.advice.market_tip;
      if (crop) renderChecklist(crop, calendarData, tip);
    } catch (e) {}
    return r;
  };
  try { renderResults = window.renderResults; } catch (e) {}
  window.__day23checkhook = true;
}
"""
    open(q, "a", encoding="utf-8").write("\n" + check_js)
    print("app.js checklist appended")

print("Task 2 done")