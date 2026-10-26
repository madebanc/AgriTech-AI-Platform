"""Day 21 Task 2: honesty labels on results. Automated with backups."""
import re, shutil

HONESTY_KEYS = {
"en": {
    "honesty_note": "Estimate from example data. Real farm data check is in progress.",
    "honesty_detail": "Use for planning only. Confirm with your extension officer or market before deciding.",
    "indicative_badge": "Indicative example, not verified yet"
},
"yo": {
    "honesty_note": "Isiro lati inu awon apeere. Ayeye data oko gidi n lo.",
    "honesty_detail": "Lo fun eto nikan. Jeri pelu osise itesiwaju tabi oja ki o to pinnu.",
    "indicative_badge": "Apeere ti a ko tii jeri"
},
"ha": {
    "honesty_note": "Kiyasi daga bayanan misali. Ana duba bayanan gona na gaskiya.",
    "honesty_detail": "Don tsarawa kawai. Tabbatar da maaikacin extension ko kasuwa kafin yanke shawara.",
    "indicative_badge": "Misali ne, ba a tabbatar ba tukuna"
},
"ig": {
    "honesty_note": "Ntule site na data atu. A na enyocha data ubi ezigbo.",
    "honesty_detail": "Maka nhazi naani. Kwenye na onye extension ma obu ahia tupu ikpebi.",
    "indicative_badge": "Atu na egosi, akwadobeghi"
}
}

p = "docs/js/translations.js"
shutil.copy(p, p + ".day20_backup")
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
    if "honesty_note" in block:
        print(lang + " honesty keys already present")
        continue
    ma = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not ma:
        print(lang + " anchor missing")
        continue
    add = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in HONESTY_KEYS[lang].items()])
    text = text[:start] + block[:ma.end()] + add + block[ma.end():] + text[nxt:]
    print(lang + " honesty keys added: " + str(len(HONESTY_KEYS[lang])))
open(p, "w", encoding="utf-8").write(text)

q = "docs/js/app.js"
shutil.copy(q, q + ".day20_backup")
js = open(q, encoding="utf-8").read()
if "ensureHonestyBadge" in js:
    print("app.js honesty already present, skipped")
else:
    hon_js = r"""
/* Day 21: honesty badge, example data until verified */
function day21HT(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function ensureHonestyBadge() {
  var section = document.getElementById("resultsSection");
  if (!section) return;
  var el = document.getElementById("honestyBadge");
  if (!el) {
    el = document.createElement("div");
    el.id = "honestyBadge";
    el.style.cssText = "background:#fff7ed;border:1px solid #fdba74;color:#7c2d12;border-radius:12px;padding:.8rem 1rem;margin:0 0 1rem;font-weight:600;";
    section.insertBefore(el, section.firstChild);
  }
  var badge = day21HT("indicative_badge", "Indicative example, not verified yet");
  var note = day21HT("honesty_note", "Estimate from example data. Real farm data check is in progress.");
  var detail = day21HT("honesty_detail", "Use for planning only. Confirm with your extension officer or market before deciding.");
  el.innerHTML = "<div style='font-weight:800;margin-bottom:.25rem;'>&#9888;&#65039; " + badge + "</div>"
    + "<div>" + note + "</div>"
    + "<div style='font-weight:400;font-size:.9rem;margin-top:.25rem;'>" + detail + "</div>";
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day21honhook) {
  var _day21render = window.renderResults || renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day21render.apply(this, arguments);
    try { ensureHonestyBadge(); } catch (e) {}
    return r;
  };
  try { renderResults = window.renderResults; } catch (e) {}
  window.__day21honhook = true;
}
try {
  if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day21honhooked) {
    var _d21set = LANG.setLanguage.bind(LANG);
    LANG.setLanguage = function (code) {
      var r = _d21set(code);
      try { ensureHonestyBadge(); } catch (e) {}
      return r;
    };
    LANG.__day21honhooked = true;
  }
} catch (e) {}
"""
    open(q, "a", encoding="utf-8").write("\n" + hon_js)
    print("app.js honesty badge appended")

print("Task 2 done")