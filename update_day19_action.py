"""Day 19 Task 2: action card at top of results with timely alerts. Automated with backups."""
import re, shutil

ACTION_KEYS = {
"en": {
    "action_title": "What to do now",
    "action_now": "Do this now",
    "action_plan": "Get ready",
    "action_month_task": "Your {crop} task for {month}",
    "action_next_task": "Next month: {task}",
    "action_sell": "Best time to sell",
    "urg_now": "Do this now",
    "urg_plant": "Time to plant",
    "urg_harvest": "Time to harvest",
    "urg_spray": "Time to spray",
    "urg_weed": "Time to weed",
    "urg_fert": "Time to fertilise"
},
"yo": {
    "action_title": "Ohun tí o ṣe níbi",
    "action_now": "Ṣe é lẹ́ẹ̀kansí",
    "action_plan": "Pẹ̀lú re",
    "action_month_task": "Ọ̀rọ̀ ẹ tìlẹ̀ ẹni {crop} ní {month}",
    "action_next_task": "Oṣù tí ó tẹ̀lé: {task}",
    "action_sell": "Àkókò tí a tà jẹ́",
    "urg_now": "Ṣe é lẹ́ẹ̀kansí",
    "urg_plant": "Ìgbà ìtù",
    "urg_harvest": "Ìgbà ọjà",
    "urg_spray": "Ìgbà ilẹ̀",
    "urg_weed": "Ìgbà ẹ̀fọ̀",
    "urg_fert": "Ìgbà oṣán"
},
"ha": {
    "action_title": "Abin da za ka yi",
    "action_now": "Yi shi yanzu",
    "action_plan": "Shirya",
    "action_month_task": "Aikin {crop} na {month}",
    "action_next_task": "Wata na farko: {task}",
    "action_sell": "Mafi kyau don saye",
    "urg_now": "Yi shi yanzu",
    "urg_plant": "Lokacin planting",
    "urg_harvest": "Lokacin harvesting",
    "urg_spray": "Lokacin fesawa",
    "urg_weed": "Lokacin tsuma",
    "urg_fert": "Lokacin fertilizer"
},
"ig": {
    "action_title": "Ọrụ ị ga-eji taa",
    "action_now": "Ya mere",
    "action_plan": "Kwadebe",
    "action_month_task": "Ọrụ gị maka {crop} na {month}",
    "action_next_task": "Ọnwa na-abịa: {task}",
    "action_sell": "Oge kachịrị ire",
    "urg_now": "Ya mere",
    "urg_plant": "Oge planting",
    "urg_harvest": "Oge harvesting",
    "urg_spray": "Oge spraying",
    "urg_weed": "Oge ikpeazụ",
    "urg_fert": "Obe fertilizer"
}
}

# ── 1. translations ──
p = "docs/js/translations.js"
shutil.copy(p, p + ".day18_backup")
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
    if "action_title" in block:
        print(lang + " action keys already present")
        continue
    ma = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not ma:
        print(lang + " anchor missing")
        continue
    add = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in ACTION_KEYS[lang].items()])
    text = text[:start] + block[:ma.end()] + add + block[ma.end():] + text[nxt:]
    print(lang + " action keys added: " + str(len(ACTION_KEYS[lang])))
open(p, "w", encoding="utf-8").write(text)

# ── 2. app.js action card ──
q = "docs/js/app.js"
shutil.copy(q, q + ".day18_backup")
js = open(q, encoding="utf-8").read()
if "renderActionCard" in js:
    print("app.js action card already present, skipped")
else:
    action_js = r"""
/* Day 19: what to do now, at the very top of results */
function day19T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function day19Urgency(task) {
  var t = String(task || "").toLowerCase();
  if (t.indexOf("harvest") !== -1) return { key: "urg_harvest", fb: "Time to harvest", color: "#b45309" };
  if (t.indexOf("plant") !== -1 || t.indexOf("sow") !== -1) return { key: "urg_plant", fb: "Time to plant", color: "#15803d" };
  if (t.indexOf("spray") !== -1 || t.indexOf("fungicide") !== -1 || t.indexOf("pest") !== -1 || t.indexOf("armyworm") !== -1 || t.indexOf("weedicide") !== -1)
    return { key: "urg_spray", fb: "Time to spray", color: "#b91c1c" };
  if (t.indexOf("weed") !== -1) return { key: "urg_weed", fb: "Time to weed", color: "#a16207" };
  if (t.indexOf("fertiliz") !== -1 || t.indexOf("npk") !== -1 || t.indexOf("urea") !== -1 || t.indexOf("top-dress") !== -1 || t.indexOf("apply") !== -1)
    return { key: "urg_fert", fb: "Time to fertilise", color: "#1d4ed8" };
  return { key: "urg_now", fb: "Do this now", color: "#1a6b3c" };
}
function removeActionCard() {
  var el = document.getElementById("actionCard");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function renderActionCard(crop, calendarData, marketTip) {
  removeActionCard();
  var section = document.getElementById("resultsSection");
  if (!section) return;
  var card = document.createElement("div");
  card.id = "actionCard";
  card.style.cssText = "background:linear-gradient(135deg,#1a6b3c,#2e8b57);color:#fff;border-radius:16px;padding:1.2rem;margin:0 0 1rem;box-shadow:0 4px 14px rgba(26,107,60,.28);";
  var cal = calendarData && calendarData.calendar ? calendarData.calendar : null;
  if (!cal) return;
  var thisM = cal.this_month || {};
  var nextM = cal.next_month || {};
  var urg = day19Urgency(thisM.task);
  var head = "<div style='display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;'>"
    + "<h2 style='margin:0;font-size:1.25rem;'>" + day19T("action_title", "What to do now") + "</h2>"
    + "<span style='background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.45);padding:.2rem .7rem;border-radius:20px;font-weight:800;font-size:.8rem;'>"
    + day19T(urg.key, urg.fb) + "</span></div>";
  var monthLine = "<div style='margin-top:.5rem;font-weight:800;font-size:1.05rem;'>"
    + day19T("action_month_task", "Your {crop} task for {month}")
        .replace("{crop}", crop || "").replace("{month}", thisM.month || "") + "</div>";
  var taskLine = "<div style='margin-top:.4rem;background:rgba(255,255,255,.15);border-radius:10px;padding:.8rem;font-weight:600;'>"
    + (thisM.task || "") + "</div>";
  var nextLine = nextM.task
    ? "<div style='margin-top:.6rem;font-size:.9rem;opacity:.92;'>"
      + day19T("action_next_task", "Next month: {task}").replace("{task}", nextM.task) + "</div>"
    : "";
  var sellLine = marketTip
    ? "<div style='margin-top:.6rem;font-size:.9rem;background:rgba(255,255,255,.15);border-radius:10px;padding:.6rem;'>"
      + "<strong>" + day19T("action_sell", "Best time to sell") + ":</strong> " + marketTip + "</div>"
    : "";
  card.innerHTML = head + monthLine + taskLine + nextLine + sellLine;
  section.insertBefore(card, section.firstChild);
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day19hook) {
  var _day19render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day19render.apply(this, arguments);
    try {
      var crop = result && result.crop;
      var tip = result && result.advice && result.advice.market_tip;
      if (crop) renderActionCard(crop, calendarData, tip);
    } catch (e) {}
    return r;
  };
  window.__day19hook = true;
}
"""
    open(q, "a", encoding="utf-8").write("\n" + action_js)
    print("app.js action card appended")

print("Task 2 done")