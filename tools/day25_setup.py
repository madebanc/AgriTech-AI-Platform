import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
FRONTEND = os.path.join(ROOT, "frontend")

PAGES = ["index.html", "analytics.html", "disease.html",
         "journal.html", "activity.html"]

FOOTER_LINK = (
    '<a href="expenses.html" style="color:rgba(255,255,255,.85); '
    'font-weight:700; text-decoration:none; font-size:.875rem; '
    'border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; '
    'border-radius:20px;">Cost Tracker</a>'
)

def add_footer_link(text, name):
    if 'href="expenses.html"' in text:
        return text
    marker = "Farm Journal</a>" if name == "activity.html" else "Activity Log</a>"
    pos = text.rfind(marker)
    if pos == -1:
        raise SystemExit("No footer marker in " + name)
    nl = "\r\n" if "\r\n" in text else "\n"
    end = text.find(nl, pos)
    at = end + len(nl) if end >= 0 else len(text)
    return text[:at] + FOOTER_LINK + nl + text[at:]

for name in PAGES:
    path = os.path.join(DOCS, name)
    with open(path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    text = text.replace("Day 24 of 365", "Day 25 of 365")
    text = add_footer_link(text, name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("Checked", name)

sw_path = os.path.join(DOCS, "sw.js")
with open(sw_path, "r", encoding="utf-8", newline="") as f:
    sw = f.read()

sw = sw.replace("agritech-ai-v12", "agritech-ai-v13")
if "Day 25 : Adds cost tracker" not in sw:
    sw = sw.replace(
        "* Day 24 : Adds activity log page to offline cache",
        "* Day 24 : Adds activity log page to offline cache\n"
        "* Day 25 : Adds cost tracker page to offline cache",
        1,
    )
if "'/AgriTech-AI-Platform/expenses.html'" not in sw:
    sw = sw.replace(
        "'/AgriTech-AI-Platform/activity.html',",
        "'/AgriTech-AI-Platform/activity.html',\n"
        "'/AgriTech-AI-Platform/expenses.html',",
        1,
    )
if "'/AgriTech-AI-Platform/js/expenses.js'" not in sw:
    sw = sw.replace(
        "'/AgriTech-AI-Platform/js/activity.js',",
        "'/AgriTech-AI-Platform/js/activity.js',\n"
        "'/AgriTech-AI-Platform/js/expenses.js',",
        1,
    )
with open(sw_path, "w", encoding="utf-8", newline="") as f:
    f.write(sw)
print("Checked sw.js")

os.makedirs(FRONTEND, exist_ok=True)
for item in os.listdir(DOCS):
    src = os.path.join(DOCS, item)
    dst = os.path.join(FRONTEND, item)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)
print("Mirrored docs into frontend")