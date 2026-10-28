"""Day 22 Task 2: share, copy, download. Automated with backups."""
import re, shutil

SHARE_KEYS = {
"en": {
    "share_title": "Share this result",
    "share_share": "Share",
    "share_copy": "Copy",
    "share_download": "Download",
    "share_print": "Print",
    "share_copied": "Copied",
    "share_for": "Result for {crop} on {ha} hectare, {tons} tons"
},
"yo": {
    "share_title": "Pin nkan apa yi",
    "share_share": "Pin",
    "share_copy": "Da dida",
    "share_download": "Gbe lasan",
    "share_print": "Te",
    "share_copied": "A da",
    "share_for": "Esi fun {crop} lori hektari {ha}, {tons} toonu"
},
"ha": {
    "share_title": "Raba wannan sakamako",
    "share_share": "Raba",
    "share_copy": "Kwafa",
    "share_download": "Sauke",
    "share_print": "Buga",
    "share_copied": "An kwafa",
    "share_for": "Sakamako na {crop} a kan hekta {ha}, ton {tons}"
},
"ig": {
    "share_title": "K kesaa nsonaazu a",
    "share_share": "K kesa",
    "share_copy": "Depu tagharia",
    "share_download": "Budata",
    "share_print": "Ibiputa",
    "share_copied": "E deputara",
    "share_for": "Nsonaazu {crop} na hekta {ha}, tan {tons}"
}
}

p = "docs/js/translations.js"
shutil.copy(p, p + ".day21_backup")
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
    if "share_title" in block:
        print(lang + " share keys already present")
        continue
    ma = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not ma:
        print(lang + " anchor missing")
        continue
    add = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in SHARE_KEYS[lang].items()])
    text = text[:start] + block[:ma.end()] + add + block[ma.end():] + text[nxt:]
    print(lang + " share keys added: " + str(len(SHARE_KEYS[lang])))
open(p, "w", encoding="utf-8").write(text)

q = "docs/js/app.js"
shutil.copy(q, q + ".day21_backup")
js = open(q, encoding="utf-8").read()
if "shareActions" in js:
    print("app.js share already present, skipped")
else:
    share_js = r"""
/* Day 22: share, copy, download, print */
function day22T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function buildShareText(result) {
  if (!result) return document.title;
  var crop = result.crop || "";
  var farm = result.farm_size_ha != null ? String(result.farm_size_ha) : "";
  var tons = result.prediction ? String(result.prediction.yield_tons) : "";
  var tpl = day22T("share_for", "Result for {crop} on {ha} hectare, {tons} tons");
  var line = tpl.replace("{crop}", crop).replace("{ha}", farm).replace("{tons}", tons);
  var bags = result.prediction ? Math.round((parseFloat(tons) || 0) * 20) + " bags (50 kg)" : "";
  var marketTip = result.advice && result.advice.market_tip ? result.advice.market_tip : "";
  var out = line;
  if (bags) out += "\n" + bags;
  if (marketTip) out += "\nMarket: " + marketTip;
  out += "\n" + window.location.href;
  return out;
}
function removeShareActions() {
  var el = document.getElementById("shareActions");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function shareActions(result) {
  removeShareActions();
  try { window.__day22lastResult = result; } catch (e) {}
  var section = document.getElementById("resultsSection");
  if (!section) return;
  var card = document.createElement("div");
  card.id = "shareActions";
  card.style.cssText = "background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:.9rem;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin:1rem 0;";
  var title = document.createElement("div");
  title.textContent = day22T("share_title", "Share this result");
  title.style.cssText = "font-weight:800;color:#1a6b3c;width:100%;margin-bottom:.35rem;";
  card.appendChild(title);
  var btns = [
    { id: "shareBtn", t: "share_share", fb: "Share", fn: function () { doShare(result); } },
    { id: "copyBtn", t: "share_copy", fb: "Copy", fn: function () { doCopy(result); } },
    { id: "downloadBtn", t: "share_download", fb: "Download", fn: function () { doDownload(result); } },
    { id: "printBtn", t: "share_print", fb: "Print", fn: function () { window.print(); } }
  ];
  btns.forEach(function (b) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = b.id;
    btn.textContent = day22T(b.t, b.fb);
    btn.style.cssText = "padding:.55rem 1rem;font-size:.9rem;font-weight:800;background:#1a6b3c;color:#fff;border:none;border-radius:24px;cursor:pointer;";
    if (b.id === "copyBtn" || b.id === "printBtn") {
      btn.style.background = "#fff";
      btn.style.color = "#1a6b3c";
      btn.style.border = "2px solid #1a6b3c";
    }
    btn.addEventListener("click", b.fn);
    card.appendChild(btn);
  });
  section.appendChild(card);
}
function doShare(result) {
  var text = buildShareText(result);
  var url = window.location.href;
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: url }).catch(function () {});
    return;
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).catch(function () {});
  }
  window.prompt("Copy this text", text);
}
function doCopy(result) {
  var text = buildShareText(result);
  var btn = document.getElementById("copyBtn");
  function done() {
    if (btn) {
      btn.textContent = day22T("share_copied", "Copied");
      setTimeout(function () { btn.textContent = day22T("share_copy", "Copy"); }, 1600);
    }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(function () {
      window.prompt("Copy this text", text);
      done();
    });
    return;
  }
  window.prompt("Copy this text", text);
  done();
}
function doDownload(result) {
  if (!result) return;
  var crop = result.crop || "";
  var ha = result.farm_size_ha != null ? String(result.farm_size_ha) : "";
  var tons = result.prediction ? String(result.prediction.yield_tons) : "";
  var bags = result.prediction ? String(Math.round((parseFloat(tons) || 0) * 20)) : "";
  var lines = [];
  lines.push("AgriTech AI, Farmer Advisory Platform, Day 22");
  lines.push(day22T("share_for", "Result for {crop} on {ha} hectare, {tons} tons").replace("{crop}", crop).replace("{ha}", ha).replace("{tons}", tons));
  lines.push("Farm: " + ha + " ha | " + tons + " tons (" + bags + " bags of 50 kg)");
  var tip = result.advice && result.advice.market_tip ? result.advice.market_tip : "";
  if (tip) lines.push("Market: " + tip);
  lines.push("Note: Iseyin Oyo cassava field point, 60 acres TME 419 May/June 2025 rain-fed, held as Oyo and South-West price indicator in review, not verified live.");
  lines.push(window.location.href);
  var body = lines.join("\n");
  var blob = new Blob([body], { type: "text/plain;charset=utf-8" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = "agritech-" + (crop || "result") + ".txt";
  document.body.appendChild(a);
  a.click();
  setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(url); }, 500);
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day22sharehook) {
  var _day22render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day22render.apply(this, arguments);
    try { shareActions(result); } catch (e) {}
    return r;
  };
  try { renderResults = window.renderResults; } catch (e) {}
  window.__day22sharehook = true;
}
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day22sharehooked) {
    var _d22set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d22set(code);
      try {
        var res = window.__day22lastResult;
        if (res) shareActions(res);
      } catch (e) {}
      return r;
    };
    LANG.__day22sharehooked = true;
  }
} catch (e) {}
"""
    open(q, "a", encoding="utf-8").write("\n" + share_js)
    print("app.js share appended")

print("Task 2 done")