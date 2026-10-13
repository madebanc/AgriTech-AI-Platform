"""Day 15 Task 3: plain soil words that fill the number underneath. Automated with backups."""
import shutil

def patch_html():
    p = "docs/index.html"
    shutil.copy(p, p + ".day15_soil_backup")
    t = open(p, encoding="utf-8").read()
    if 'id="soilType"' in t:
        print("soilType already present, skipped")
        return
    old = '''            <input type="number" id="soilPh" name="soil_ph"'''
    new = '''            <select id="soilType" style="padding:.5rem; border-radius:10px; border:1px solid #cbd5cc; margin-bottom:.5rem; width:100%;">
              <option value="">What is your soil like? Pick one</option>
              <option value="sandy">Sandy, water drains fast, light colour</option>
              <option value="loamy">Loamy, soft and dark, holds water well</option>
              <option value="clay">Clay, sticky when wet, hard when dry</option>
              <option value="unknown">Not sure</option>
            </select>
            <input type="number" id="soilPh" name="soil_ph"'''
    if old in t:
        t = t.replace(old, new)
        t = t.replace("Optimal: 5.5 – 6.5 for most crops", "Pick your soil above, we fill a safe number below. For best accuracy get a strip test at the extension office. Optimal is 5.5 to 6.5 for most crops.")
        open(p, "w", encoding="utf-8").write(t)
        print("index.html soil selector added")
    else:
        print("WARNING: soil input not found")

def patch_js():
    p = "docs/js/app.js"
    shutil.copy(p, p + ".day15_soil_backup")
    t = open(p, encoding="utf-8").read()
    if "soilType" in t and "SOIL_DEFAULTS" in t:
        print("app.js soil already patched, skipped")
        return
    inject = '''
/* ── Day 15 Task 3: soil plain words ── */
const SOIL_DEFAULTS = { sandy: 5.8, loamy: 6.2, clay: 5.5, unknown: 6.0, "": 6.0 };
function wireSoilType() {
  const sel = document.getElementById("soilType");
  const num = document.getElementById("soilPh");
  if (!sel || !num) return;
  sel.addEventListener("change", () => {
    const v = SOIL_DEFAULTS[sel.value] ?? 6.0;
    num.value = v;
  });
}
wireSoilType();
'''
    marker = "/* ── 5. Validate form"
    if marker in t:
        t = t.replace(marker, inject + "\n" + marker)
        open(p, "w", encoding="utf-8").write(t)
        print("app.js soil wired")
    else:
        print("WARNING: marker not found")

patch_html()
patch_js()
print("Task 3 done")