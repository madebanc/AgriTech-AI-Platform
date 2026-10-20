"""Day 18 Task 2: market panel with price per bag and money in hand. Automated with backups."""
import re, shutil

PRICE_FALLBACK = {
    "Cassava":  [40000, 80000],
    "Yam":      [200000, 400000],
    "Maize":    [150000, 250000],
    "Rice":     [180000, 320000],
    "Groundnut":[120000, 220000],
    "Cocoa":    [800000, 1500000],
}

MARKET_KEYS = {
"en": {
    "market_title": "Market timing and money",
    "market_best": "Best selling months",
    "market_bag_price": "Price per 50 kg bag",
    "market_your_bags": "Your expected bags",
    "market_money": "Expected money if you sell",
    "market_note": "Prices are indicative. Check the local market before selling.",
    "market_offline": "Market prices need internet. Connect to see prices."
},
"yo": {
    "market_title": "Ìjì Ìtajà àti Owó",
    "market_best": "Oṣù tàbí nípa tàbí jẹ́",
    "market_bag_price": "Iyá ọjọ́ 50 kg",
    "market_your_bags": "Àpò apá ọjọ́ rẹ",
    "market_money": "Owó tí o yẹ̀ kí o tà",
    "market_note": "Iye owó yí ni àtúnṣe. Ṣàyẹ̀wò ọjà ilé rẹ kí o tà.",
    "market_offline": "Iye owó ọjà nílò internet. Sopọ̀ ọjọ́ kan kí o rí i."
},
"ha": {
    "market_title": "Kasuwanni da kuɗi",
    "market_best": "Wata mafi kyau ga saye",
    "market_bag_price": "Kudin jiga 50 kg",
    "market_your_bags": "Jigajinkin da za ka yi",
    "market_money": "Kudinka da za ka samu idan ka saye",
    "market_note": "Kudin wannan ana nuna ne kawai. Duba kasuwanninka kafin ka saye.",
    "market_offline": "Kudin kasuwanni yana buƙatar intanet. Haɗa don gan shi."
},
"ig": {
    "market_title": "Ozi ahụ ọrụ na ego",
    "market_best": "Ọnwa kachịrị ihe niile",
    "market_bag_price": "Ọnọda obi 50 kg",
    "market_your_bags": "Akwụụ obi ị ga-atụta",
    "market_money": "Ego ị ga-ahụ maka ị rere",
    "market_note": "Ọnọdụ ego a dị n'akụkụ mere. Lelee ọka ahụ tupu ị rere.",
    "market_offline": "Ọnọdụ ego ahụ chọrọ internet. Jiri ikpeazụka ka ị hụ ya."
}
}

# ── 1. translations ──
p = "docs/js/translations.js"
shutil.copy(p, p + ".day17_backup")
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
    if "market_title" in block:
        print(lang + " market keys already present")
        continue
    ma = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not ma:
        print(lang + " anchor missing")
        continue
    add = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in MARKET_KEYS[lang].items()])
    text = text[:start] + block[:ma.end()] + add + block[ma.end():] + text[nxt:]
    print(lang + " market keys added: " + str(len(MARKET_KEYS[lang])))
open(p, "w", encoding="utf-8").write(text)

# ── 2. app.js market panel ──
q = "docs/js/app.js"
shutil.copy(q, q + ".day17_backup")
js = open(q, encoding="utf-8").read()
if "renderMarket" in js:
    print("app.js market already present, skipped")
else:
    market_js = r"""
/* Day 18: market timing and money in hand */
var DAY18_PRICES = {
  "Cassava": [40000, 80000], "Yam": [200000, 400000], "Maize": [150000, 250000],
  "Rice": [180000, 320000], "Groundnut": [120000, 220000], "Cocoa": [800000, 1500000]
};
function day18T(k, fb) {
  try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; }
}
function day18Money(n) {
  return "₦" + Math.round(n).toLocaleString("en-NG");
}
function removeMarketPanel() {
  var el = document.getElementById("marketPanel");
  if (el && el.parentElement) el.parentElement.removeChild(el);
}
function marketPanelShell() {
  removeMarketPanel();
  var anchor = document.getElementById("yieldFarm");
  if (!anchor || !anchor.parentElement) return null;
  var greenCard = anchor.parentElement;
  var section = greenCard.parentElement;
  var panel = document.createElement("div");
  panel.id = "marketPanel";
  panel.style.cssText = "background:#fff;border-radius:14px;padding:1.2rem;margin:1rem 0;box-shadow:0 2px 10px rgba(0,0,0,.08);";
  if (section && section.insertBefore) section.insertBefore(panel, greenCard.nextSibling);
  else greenCard.parentElement.appendChild(panel);
  return panel;
}
function renderMarket(crop, tons, marketTip) {
  var panel = marketPanelShell();
  if (!panel) return;
  var bags = Math.round((parseFloat(tons) || 0) * 20);
  var head = "<h3 style='margin:0 0 .6rem; color:#1a6b3c;'>" + day18T("market_title", "Market timing and money") + "</h3>";
  var best = "<div style='margin-bottom:.8rem; font-weight:700;'>" + day18T("market_best", "Best selling months") + ": " + (marketTip || "-") + "</div>";
  var body = "";
  var range = DAY18_PRICES[crop];
  var useFallback = true;
  fetch(API + "/api/advice/" + encodeURIComponent(crop))
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d && d.success && d.advice && d.advice.price_range_ngn_per_ton) {
        useFallback = false;
        range = [d.advice.price_range_ngn_per_ton.low, d.advice.price_range_ngn_per_ton.high];
        paintMarket(range, bags, tons);
      }
    })
    .catch(function () { paintMarket(range, bags, tons); });
  function paintMarket(r, b, t) {
    var lowBag = r[0] / 20, highBag = r[1] / 20;
    var lowMoney = b * lowBag, highMoney = b * highBag;
    body = "<div style='display:grid;grid-template-columns:1fr 1fr;gap:.8rem;'>"
      + "<div style='background:#f7faf7;border-radius:10px;padding:.8rem;'>"
      + "<div style='font-size:.8rem;color:#555;'>" + day18T("market_bag_price", "Price per 50 kg bag") + "</div>"
      + "<div style='font-weight:800;color:#1a6b3c;'>" + day18Money(lowBag) + " - " + day18Money(highBag) + "</div></div>"
      + "<div style='background:#f7faf7;border-radius:10px;padding:.8rem;'>"
      + "<div style='font-size:.8rem;color:#555;'>" + day18T("market_your_bags", "Your expected bags") + "</div>"
      + "<div style='font-weight:800;color:#1a6b3c;'>" + b + " bags (" + t + " tons)</div></div></div>"
      + "<div style='margin-top:.8rem;background:#e8f5ec;border-radius:10px;padding:.8rem;'>"
      + "<div style='font-size:.8rem;color:#555;'>" + day18T("market_money", "Expected money if you sell") + "</div>"
      + "<div style='font-weight:800;color:#1a6b3c;'>" + day18Money(lowMoney) + " - " + day18Money(highMoney) + "</div></div>"
      + "<small style='display:block;margin-top:.7rem;color:#555;'>" + day18T("market_note", "Prices are indicative. Check the local market before selling.") + "</small>";
    panel.innerHTML = head + best + body;
  }
  panel.innerHTML = head + best + "<small>" + day18T("market_offline", "Market prices need internet. Connect to see prices.") + "</small>";
}
if (typeof window !== "undefined" && typeof renderResults === "function" && !window.__day18hook) {
  var _day18render = renderResults;
  window.renderResults = function (result, calendarData) {
    var r = _day18render.apply(this, arguments);
    try {
      var crop = result && result.crop;
      var tons = result && result.prediction && result.prediction.yield_tons;
      var tip = result && result.advice && result.advice.market_tip;
      if (crop && tons) renderMarket(crop, tons, tip);
    } catch (e) {}
    return r;
  };
  window.__day18hook = true;
}
"""
    open(q, "a", encoding="utf-8").write("\n" + market_js)
    print("app.js market panel appended")

print("Task 2 done")