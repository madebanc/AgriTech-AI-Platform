"""Day 14 footer updater. No manual edits. Run once."""
import re, shutil, os

FOOTERS = {
"docs/index.html": """  <!-- FOOTER -->
  <footer class="footer">
    <p>
      <span data-i18n="footer_built">Built by</span>
      <strong> Daniel Oyanogbezina</strong> —
      AgriTech AI Platform — Day 14 of 365
    </p>
    <p class="footer-sub" data-i18n="footer_mission">
      Empowering Nigerian farmers with AI — MSc Agroforestry, FUNAAB
    </p>
    <p style="margin-top:.75rem; display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
      <a href="analytics.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Analytics</a>
      <a href="disease.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Disease Guide</a>
      <a href="journal.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Farm Journal</a>
    </p>
  </footer>""",
"docs/analytics.html": """  <!-- FOOTER -->
  <footer class="footer">
    <p>
      Built by <strong>Daniel Oyanogbezina</strong> —
      AgriTech AI Platform — Day 14 of 365
    </p>
    <p class="footer-sub">
      Empowering Nigerian farmers with AI — MSc Agroforestry, FUNAAB
    </p>
    <p style="margin-top:.75rem; display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
      <a href="index.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Yield Predictor</a>
      <a href="disease.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Disease Guide</a>
      <a href="journal.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Farm Journal</a>
    </p>
  </footer>""",
"docs/disease.html": """  <!-- FOOTER -->
  <footer class="footer">
    <p>
      Built by <strong>Daniel Oyanogbezina</strong> —
      AgriTech AI Platform — Day 14 of 365
    </p>
    <p class="footer-sub">
      Empowering Nigerian farmers with AI — MSc Agroforestry, FUNAAB
    </p>
    <p style="margin-top:.75rem; display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
      <a href="index.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Yield Predictor</a>
      <a href="analytics.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Analytics</a>
      <a href="journal.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Farm Journal</a>
    </p>
  </footer>""",
"docs/journal.html": """  <!-- FOOTER -->
  <footer class="footer">
    <p>
      Built by <strong>Daniel Oyanogbezina</strong> —
      AgriTech AI Platform — Day 14 of 365
    </p>
    <p class="footer-sub">
      Empowering Nigerian farmers with AI — MSc Agroforestry, FUNAAB
    </p>
    <p style="margin-top:.75rem; display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
      <a href="index.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Yield Predictor</a>
      <a href="analytics.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Analytics</a>
      <a href="disease.html" style="color:rgba(255,255,255,.85); font-weight:700; text-decoration:none; font-size:.875rem; border:1px solid rgba(255,255,255,.4); padding:.3rem .8rem; border-radius:20px;">Disease Guide</a>
    </p>
  </footer>"""
}

for path, new_footer in FOOTERS.items():
    if not os.path.exists(path):
        print(f"Missing {path}, skipped")
        continue
    shutil.copy(path, path + ".day13_backup")
    text = open(path, encoding="utf-8").read()
    updated, n = re.subn(r"<!-- FOOTER -->.*?</footer>", lambda m: new_footer, text, flags=re.DOTALL)
    if n == 0:
        updated, n = re.subn(r"<footer.*?</footer>", lambda m: new_footer, text, flags=re.DOTALL)
    open(path, "w", encoding="utf-8").write(updated)
    print(f"{path}: replaced {n} footer, backup saved")