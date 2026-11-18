import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
FRONTEND = os.path.join(ROOT, "frontend")

PAGES = ["index.html", "analytics.html", "disease.html", "journal.html", "activity.html", "expenses.html"]

PROFIT_LINK = (
    '<a href="profit.html" style="color:rgba(255,255,255,.85); font-weight:700; '
    'text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); '
    'padding:.3rem .8rem; border-radius:20px;">Profit Calc</a>'
)

for name in PAGES:
    path = os.path.join(DOCS, name)
    if not os.path.exists(path):
        print(f"SKIP (not found): {name}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace("Day 25 of 365", "Day 26 of 365")

    if "Profit Calc" not in text:
        m = re.search(r"Cost Tracker</(?:a|strong)>", text)
        if m:
            insert_pos = m.end()
            if insert_pos < len(text) and text[insert_pos] == "\n":
                text = text[:insert_pos] + "\n" + PROFIT_LINK + text[insert_pos:]
            else:
                text = text[:insert_pos] + PROFIT_LINK + text[insert_pos:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Checked {name}")

sw_path = os.path.join(DOCS, "sw.js")
if os.path.exists(sw_path):
    with open(sw_path, "r", encoding="utf-8") as f:
        sw = f.read()

    sw = sw.replace("agritech-ai-v13", "agritech-ai-v14")

    if "Day 26" not in sw:
        sw = sw.replace(
            "// Day 25: Added expenses.html and expenses.js",
            "// Day 25: Added expenses.html and expenses.js\n// Day 26: Added profit.html and profit.js",
        )

    if "/AgriTech-AI-Platform/profit.html" not in sw:
        sw = sw.replace(
            "  '/AgriTech-AI-Platform/expenses.html',\n",
            "  '/AgriTech-AI-Platform/expenses.html',\n  '/AgriTech-AI-Platform/profit.html',\n",
        )
    if "/AgriTech-AI-Platform/js/profit.js" not in sw:
        sw = sw.replace(
            "  '/AgriTech-AI-Platform/js/expenses.js',\n",
            "  '/AgriTech-AI-Platform/js/expenses.js',\n  '/AgriTech-AI-Platform/js/profit.js',\n",
        )

    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(sw)
    print("Checked sw.js")

if os.path.exists(FRONTEND):
    for item in os.listdir(DOCS):
        src = os.path.join(DOCS, item)
        dst = os.path.join(FRONTEND, item)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print("Mirrored docs into frontend")
else:
    print("frontend/ not found, skipping mirror")