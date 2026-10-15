"""Day 17 Task 2: add Yoruba Hausa Igbo for plot acre soil bags review. Automated with backups."""
import re, shutil

NEW_KEYS = {
"en": {
    "unit_hectare": "Hectare",
    "unit_acre": "Acre",
    "unit_plot": "Plot (648 sqm Lagos standard)",
    "soil_prompt": "What is your soil like? Pick one",
    "soil_sandy": "Sandy, water drains fast, light colour",
    "soil_loamy": "Loamy, soft and dark, holds water well",
    "soil_clay": "Clay, sticky when wet, hard when dry",
    "soil_unknown": "Not sure",
    "confirm_check": "Please check before we predict:",
    "confirm_ask": "Is this correct? Press OK to predict, Cancel to fix.",
    "plain_template": "Your {crop} on {ha} hectare may give about {tons} tons, which is about {bags} bags of 50 kg. This is an estimate for planning, not a promise. Weather and pests can change it.",
    "size_template": "{v} {unit} is about {ha} hectare for the model.",
    "bags_template": "{kg} kg per hectare is about {bags} bags of 50 kg.",
    "helper_size_full": "15 plots is about 1 hectare. 6 plots is about 1 acre. Plot sizes differ by town, confirm with extension officer if unsure."
},
"yo": {
    "unit_hectare": "Hektari",
    "unit_acre": "Eka",
    "unit_plot": "Plot (648 sqm, iwon Lagos)",
    "soil_prompt": "Iru ile re bawo? Yan okan",
    "soil_sandy": "Iyanrin, omi nsan yarayara, awo feere",
    "soil_loamy": "Alemo, riro ati dudu, o dan omi duro daradara",
    "soil_clay": "Amo, o lemo nigbati o tutu, o le nigbati o gbe",
    "soil_unknown": "Ko da loju",
    "confirm_check": "Jowo sayewo saju ki a to sotele:",
    "confirm_ask": "Se eyi to? Te OK lati sotele, Cancel lati satunse.",
    "plain_template": "Irugbin {crop} re lori hektari {ha} le fun ni to {tons} toonu, eyi ti o je to apo {bags} ti 50 kg. Eyi je isiro fun eto, kii se ileri. Oju ojo ati kokoro le yi i pada.",
    "size_template": "{v} {unit} je to {ha} hektari fun awose.",
    "bags_template": "{kg} kg fun hektari kan je to apo {bags} ti 50 kg.",
    "helper_size_full": "Plot 15 je to hektari 1. Plot 6 je to eka 1. Iwon plot yato si ilu si ilu, beere lowo osise itesiwaju ti o ko ba da loju."
},
"ha": {
    "unit_hectare": "Hekta",
    "unit_acre": "Eka",
    "unit_plot": "Fili (648 sqm, ma'aunin Legas)",
    "soil_prompt": "Kasarka fa ta ke? Zabi daya",
    "soil_sandy": "Yashi, ruwa yana tafiya da sauri, launi mai haske",
    "soil_loamy": "Laka, mai laushi da duhu, tana rike ruwa da kyau",
    "soil_clay": "Yumbu, tana likewa da jika, tana tauri da bushewa",
    "soil_unknown": "Ban da tabbas",
    "confirm_check": "Da fatan a duba kafin a yi hasashe:",
    "confirm_ask": "Shin daidai ne? Danna OK don hasashe, Cancel don gyarawa.",
    "plain_template": "Amfanin gonarka {crop} a kan hekta {ha} na iya ba da kusan tan {tons}, wanda kusan jaka {bags} ne na 50 kg. Wannan kiyasi ne don tsarawa, ba alkawari ba. Yanayi da kwari na iya canza shi.",
    "size_template": "{v} {unit} kusan {ha} hekta ne don tsarin.",
    "bags_template": "{kg} kg a kowace hekta kusan jaka {bags} ne na 50 kg.",
    "helper_size_full": "Fili 15 kusan hekta 1 ne. Fili 6 kusan eka 1 ne. Girman fili ya bambanta da gari zuwa gari, tambayi ma'aikacin extension idan ba ka da tabbas."
},
"ig": {
    "unit_hectare": "Hekta",
    "unit_acre": "Eka",
    "unit_plot": "Plot (648 sqm, okoloto Lagos)",
    "soil_prompt": "Ala gi di ka gini? Horo otu",
    "soil_sandy": "Aja, mmiri na-agbapu ngwa ngwa, ocha",
    "soil_loamy": "Udavuu, di nro ma gbaa ochichiri, na-ejide mmiri nke oma",
    "soil_clay": "Uro, na-arapara mgbe mmiri di, na-esi ike mgbe o kporo nku",
    "soil_unknown": "Amaghi m",
    "confirm_check": "Biko lelee anya tupu anyi ebuo amuma:",
    "confirm_ask": "Nke a o ziri ezi? Pia OK iji buo amuma, Cancel iji mezie.",
    "plain_template": "Ihe ubi {crop} gi na hekta {ha} nwere ike inye ihe di ka tan {tons}, nke di ka akpa {bags} nke 50 kg. Nke a bu atumatu maka nhazi, obughi nkwa. Ihu igwe na pests nwere ike igbanwe ya.",
    "size_template": "{v} {unit} di ka {ha} hekta maka model.",
    "bags_template": "{kg} kg kwa hekta di ka akpa {bags} nke 50 kg.",
    "helper_size_full": "Plot 15 di ka hekta 1. Plot 6 di ka eka 1. Ogo plot di iche site n'obodo ruo n'obodo, juo onye oru extension ma oburu na imaghi."
}
}

p = "docs/js/translations.js"
shutil.copy(p, p + ".day16_backup")
text = open(p, encoding="utf-8").read()

for lang in ["ig", "ha", "yo", "en"]:
    m_start = re.search(r'\n\s*' + lang + r'\s*:\s*\{', text)
    if not m_start:
        print(lang + " block not found")
        continue
    start_idx = m_start.start()
    next_idx = len(text)
    for l2 in ["en", "yo", "ha", "ig"]:
        if l2 == lang:
            continue
        m2 = re.search(r'\n\s*' + l2 + r'\s*:\s*\{', text[m_start.end():])
        if m2:
            cand = m_start.end() + m2.start()
            if cand < next_idx:
                next_idx = cand
    block = text[start_idx:next_idx]
    if "unit_hectare" in block:
        print(lang + " already has keys, skipped")
        continue
    m_auto = re.search(r'autofill_badge:\s*"[^"]*",', block)
    if not m_auto:
        print(lang + " autofill not found")
        continue
    additions = "".join(['\n    ' + k + ': "' + v.replace('"', "'") + '",' for k, v in NEW_KEYS[lang].items()])
    block2 = block[:m_auto.end()] + additions + block[m_auto.end():]
    text = text[:start_idx] + block2 + text[next_idx:]
    print(lang + " keys added: " + str(len(NEW_KEYS[lang])))

open(p, "w", encoding="utf-8").write(text)
print("translations patched")

q = "docs/js/app.js"
shutil.copy(q, q + ".day16_backup")
js = open(q, encoding="utf-8").read()
if "applyDay17Static" in js:
    print("app.js already has Day 17, skipped")
else:
    override = r"""
/* Day 17: multilingual overrides for units soil bags review */
function updateSizeHelper() {
  var el = document.getElementById("sizeHelper");
  if (!el) return;
  var fv = document.getElementById("farmSize");
  var fu = document.getElementById("farmUnit");
  var v = parseFloat(fv && fv.value) || 0;
  var uVal = fu ? fu.value : "hectare";
  var ha = (typeof farmUnitToHa === "function") ? farmUnitToHa(v, uVal) : v;
  var unitName = uVal;
  try {
    if (uVal === "hectare") unitName = LANG.t("unit_hectare");
    else if (uVal === "acre") unitName = LANG.t("unit_acre");
    else if (uVal === "plot") unitName = LANG.t("unit_plot");
  } catch (e) {}
  var tpl = "{v} {unit} is about {ha} hectare for the model.";
  try { tpl = LANG.t("size_template") || tpl; } catch (e) {}
  el.textContent = tpl.replace("{v}", v).replace("{unit}", unitName).replace("{ha}", ha.toFixed(2));
}
function updateBagsHelper() {
  var el = document.getElementById("bagsHelper");
  if (!el) return;
  var f = document.getElementById("fertilizer");
  var kg = parseFloat(f && f.value) || 0;
  var bags = (kg / 50).toFixed(1);
  var tpl = "{kg} kg per hectare is about {bags} bags of 50 kg.";
  try { tpl = LANG.t("bags_template") || tpl; } catch (e) {}
  el.textContent = tpl.replace("{kg}", kg).replace("{bags}", bags);
}
function plainBags(tons) {
  var n = parseFloat(tons) || 0;
  return Math.round(n * 20);
}
function updatePlainResult(crop, ha, tons) {
  var el = document.getElementById("plainResult");
  if (!el) {
    var anchor = document.getElementById("yieldFarm");
    if (!anchor || !anchor.parentElement) return;
    el = document.createElement("p");
    el.id = "plainResult";
    el.style.cssText = "font-weight:700; margin-top:.5rem;";
    anchor.parentElement.appendChild(el);
  }
  var tpl = "Your {crop} on {ha} hectare may give about {tons} tons, which is about {bags} bags of 50 kg.";
  try { tpl = LANG.t("plain_template") || tpl; } catch (e) {}
  el.textContent = tpl.replace("{crop}", crop).replace("{ha}", Number(ha).toFixed(2)).replace("{tons}", tons).replace("{bags}", plainBags(tons));
}
function confirmFarm(data) {
  var rawVal = document.getElementById("farmSize") ? document.getElementById("farmSize").value : data.farm_size_ha;
  var fu = document.getElementById("farmUnit");
  var unit = fu ? fu.value : "hectare";
  var fertKg = data.fertilizer_kg || 0;
  var t = function (k, fb) { try { var v = LANG.t(k); return (v && v !== k) ? v : fb; } catch (e) { return fb; } };
  var msg = t("confirm_check", "Please check before we predict:") + "\n\nCrop: " + data.crop + "\nState: " + data.state + "\nSize: " + rawVal + " " + unit + " (about " + Number(data.farm_size_ha).toFixed(2) + " hectare)\nSoil pH: " + data.soil_ph + "\nFertilizer: " + fertKg + " kg (" + (fertKg / 50).toFixed(1) + " bags)\n\n" + t("confirm_ask", "Is this correct? Press OK to predict, Cancel to fix.");
  return window.confirm(msg);
}
function applyDay17Static() {
  try {
    var fu = document.getElementById("farmUnit");
    if (fu && fu.options && fu.options.length >= 3) {
      fu.options[0].text = LANG.t("unit_hectare");
      fu.options[1].text = LANG.t("unit_acre");
      fu.options[2].text = LANG.t("unit_plot");
    }
    var st = document.getElementById("soilType");
    if (st && st.options) {
      for (var i = 0; i < st.options.length; i++) {
        var v = st.options[i].value;
        if (v === "") st.options[i].text = LANG.t("soil_prompt");
        else if (v === "sandy") st.options[i].text = LANG.t("soil_sandy");
        else if (v === "loamy") st.options[i].text = LANG.t("soil_loamy");
        else if (v === "clay") st.options[i].text = LANG.t("soil_clay");
        else if (v === "unknown") st.options[i].text = LANG.t("soil_unknown");
      }
    }
  } catch (e) {}
}
if (typeof LANG !== "undefined" && LANG.setLanguage && !LANG.__day17hooked) {
  var _origSet = LANG.setLanguage.bind(LANG);
  LANG.setLanguage = function (code) {
    var r = _origSet(code);
    try { applyDay17Static(); updateSizeHelper(); updateBagsHelper(); } catch (e) {}
    return r;
  };
  LANG.__day17hooked = true;
}
document.addEventListener("DOMContentLoaded", function () { try { applyDay17Static(); } catch (e) {} });
try { applyDay17Static(); } catch (e) {}
"""
    open(q, "a", encoding="utf-8").write("\n" + override)
    print("app.js Day 17 overrides appended")

print("Task 2 done")