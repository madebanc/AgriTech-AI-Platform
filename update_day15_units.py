"""Day 15 Task 2: add plot acre hectare choice plus bags helper. Automated, with backups."""
import shutil, re

def patch_html():
    p = "docs/index.html"
    shutil.copy(p, p + ".day14_backup")
    t = open(p, encoding="utf-8").read()
    if 'id="farmUnit"' in t:
        print("index.html already has farmUnit, skipped size patch")
    else:
        old_size = '''            <input type="number" id="farmSize" name="farm_size_ha"
                   min="0.1" max="100" step="0.1"
                   data-i18n-ph="ph_farm_size"
                   placeholder="e.g. 2.5" required />'''
        new_size = '''            <input type="number" id="farmSize" name="farm_size_input"
                   min="0.1" max="1500" step="0.1"
                   data-i18n-ph="ph_farm_size"
                   placeholder="e.g. 2.5" required />
            <div style="display:flex; gap:.5rem; margin-top:.5rem; align-items:center;">
              <select id="farmUnit" style="padding:.5rem; border-radius:10px; border:1px solid #cbd5cc;">
                <option value="hectare">Hectare</option>
                <option value="acre">Acre</option>
                <option value="plot">Plot (648 sqm Lagos standard)</option>
              </select>
            </div>
            <small class="field-hint" id="sizeHelper">15 plots is about 1 hectare. 6 plots is about 1 acre. Plot sizes differ by town, confirm with extension officer if unsure.</small>'''
        if old_size in t:
            t = t.replace(old_size, new_size)
            print("index.html size block patched")
        else:
            print("WARNING: size block not found, no patch")
    if 'id="bagsHelper"' in t:
        print("index.html already has bagsHelper, skipped")
    else:
        old_fert = '''            <input type="number" id="fertilizer" name="fertilizer_kg"
                   min="0" max="500" step="5"
                   data-i18n-ph="ph_fertilizer"
                   placeholder="e.g. 100" required />'''
        new_fert = '''            <input type="number" id="fertilizer" name="fertilizer_kg"
                   min="0" max="500" step="5"
                   data-i18n-ph="ph_fertilizer"
                   placeholder="e.g. 100" required />
            <small class="field-hint" id="bagsHelper">100 kg is 2 bags of 50 kg. Enter kg per hectare here, we show bags to help.</small>'''
        if old_fert in t:
            t = t.replace(old_fert, new_fert)
            print("index.html fertilizer helper patched")
        else:
            print("WARNING: fertilizer block not found")
    open(p, "w", encoding="utf-8").write(t)

def patch_js():
    p = "docs/js/app.js"
    shutil.copy(p, p + ".day14_backup")
    t = open(p, encoding="utf-8").read()
    if "farmUnitToHa" in t:
        print("app.js already patched, skipped")
        return
    helper = '''
/* ── Day 15: land unit conversion, model always gets hectares ── */
function farmUnitToHa(value, unit) {
  const v = parseFloat(value) || 0;
  if (unit === "acre") return v * 0.4047;
  if (unit === "plot") return v * 0.0648;
  return v;
}
function updateSizeHelper() {
  const el = document.getElementById("sizeHelper");
  if (!el) return;
  const v = parseFloat(document.getElementById("farmSize").value) || 0;
  const u = document.getElementById("farmUnit") ? document.getElementById("farmUnit").value : "hectare";
  const ha = farmUnitToHa(v, u);
  el.textContent = v + " " + u + " is about " + ha.toFixed(2) + " hectare for the model. Note: 15 plots is about 1 hectare, 6 plots is about 1 acre. Plot sizes differ by town.";
}
function updateBagsHelper() {
  const el = document.getElementById("bagsHelper");
  if (!el) return;
  const kg = parseFloat(document.getElementById("fertilizer").value) || 0;
  el.textContent = kg + " kg per hectare is about " + (kg/50).toFixed(1) + " bags of 50 kg. Enter kg per hectare here, we show bags to help.";
}

'''
    t = t.replace("/* ── 5. Validate form", helper + "/* ── 5. Validate form")
    old_data = "    farm_size_ha:  parseFloat($('farmSize').value),"
    new_data = '''    farm_size_ha:  farmUnitToHa($('farmSize').value, document.getElementById("farmUnit") ? document.getElementById("farmUnit").value : "hectare"),'''
    if old_data in t:
        t = t.replace(old_data, new_data)
        print("app.js conversion patched")
    else:
        print("WARNING: farm_size line not found")
    old_listener = "$('farmForm').addEventListener('submit', async function (e) {"
    if "farmSize' ).addEventListener" not in t:
        t = t.replace(old_listener, '''document.getElementById("farmSize").addEventListener("input", updateSizeHelper);
document.getElementById("farmUnit").addEventListener("change", updateSizeHelper);
document.getElementById("fertilizer").addEventListener("input", updateBagsHelper);
updateSizeHelper();
updateBagsHelper();
''' + old_listener)
        print("app.js helpers wired")
    open(p, "w", encoding="utf-8").write(t)

patch_html()
patch_js()
print("Day 15 Task 2 done. Backups saved.")