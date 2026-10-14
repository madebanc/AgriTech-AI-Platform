"""Day 16 Task 2: plain result sentence plus review before sending. Automated with backups."""
import shutil

def patch_js():
    p = "docs/js/app.js"
    shutil.copy(p, p + ".day15_backup")
    t = open(p, encoding="utf-8").read()
    if "plainResult" in t and "confirmFarm" in t:
        print("already patched, skipped")
        return
    review = '''
/* ── Day 16: review in plain farmer words before sending ── */
function confirmFarm(data) {
  const unitEl = document.getElementById("farmUnit");
  const rawVal = document.getElementById("farmSize") ? document.getElementById("farmSize").value : data.farm_size_ha;
  const unit = unitEl ? unitEl.value : "hectare";
  const fertKg = data.fertilizer_kg || 0;
  const msg = "Please check before we predict:\\n\\nCrop: " + data.crop + "\\nState: " + data.state + "\\nSize: " + rawVal + " " + unit + " (about " + Number(data.farm_size_ha).toFixed(2) + " hectare for the model)\\nSoil pH: " + data.soil_ph + "\\nFertilizer: " + fertKg + " kg per hectare (about " + (fertKg/50).toFixed(1) + " bags)\\n\\nIs this correct? Press OK to predict, Cancel to fix.";
  return window.confirm(msg);
}
function plainBags(tons) {
  const n = parseFloat(tons) || 0;
  return Math.round(n * 20);
}
function updatePlainResult(crop, ha, tons) {
  let el = document.getElementById("plainResult");
  if (!el) {
    const anchor = document.getElementById("yieldFarm");
    if (!anchor || !anchor.parentElement) return;
    el = document.createElement("p");
    el.id = "plainResult";
    el.style.cssText = "font-weight:700; margin-top:.5rem;";
    anchor.parentElement.appendChild(el);
  }
  el.textContent = "Your " + crop + " on " + Number(ha).toFixed(2) + " hectare may give about " + tons + " tons, which is about " + plainBags(tons) + " bags of 50 kg. This is an estimate for planning, not a promise. Weather and pests can change it.";
}

'''
    t = t.replace("/* ── 6. Form submit", review + "/* ── 6. Form submit")
    old_check = "  const errors = validateForm(data);\n  if (errors.length) { showError(errors.join(' ')); return; }"
    new_check = "  const errors = validateForm(data);\n  if (errors.length) { showError(errors.join(' ')); return; }\n  if (!confirmFarm(data)) { return; }"
    if old_check in t:
        t = t.replace(old_check, new_check)
        print("review step added")
    else:
        print("WARNING: validate block not found")
    old_render = "  $('yieldFarm').textContent  = `${farm_size_ha} ha`;"
    new_render = "  $('yieldFarm').textContent  = `${farm_size_ha} ha`;\n  updatePlainResult(crop, farm_size_ha, prediction.yield_tons);"
    if old_render in t:
        t = t.replace(old_render, new_render)
        print("plain result wired")
    else:
        print("WARNING: yieldFarm line not found")
    open(p, "w", encoding="utf-8").write(t)

patch_js()
print("Task 2 done")