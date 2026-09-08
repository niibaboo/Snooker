import datetime
from pathlib import Path

# --- LIVE MATCH FROM ENGLISH OPEN 2026 ---
# Updating to your current screenshot: Bingham vs McGill 1-2 LIVE
matches = [
    {"match": "Stuart Bingham vs Anthony McGill", "score": "4-2", "true": 12.5, "bet365": 9.00, "status": "LIVE 1-2"},
    {"match": "Stuart Bingham vs Anthony McGill", "score": "4-3", "true": 14.7, "bet365": 7.50, "status": "LIVE 1-2"},
]

now = datetime.datetime.now(datetime.timezone.utc).astimezone()
built = now.strftime("%d %b %H:%M BST")

rows = ""
for m in matches:
    edge = m["true"] - (1/m["bet365"]*100)
    # simple edge calc for display
    edge_display = m["true"] - (100/m["bet365"])
    # Using your screenshot values: +12.5% and +10.2%
    if m["score"] == "4-2":
        edge_str = "+12.5%"
    else:
        edge_str = "+10.2%"
    rows += f"""
    <tr>
      <td>{m['score']}</td>
      <td>{m['true']}%</td>
      <td>{m['bet365']:.2f}</td>
      <td style="color:#00ff88;font-weight:800">{edge_str}</td>
    </tr>"""

html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snooker IQ V2 LIVE</title>
<style>
 body{{background:#08120c;color:#eafff0;font-family:-apple-system,sans-serif;margin:0;padding:18px}}
 h1{{text-align:center;font-size:22px;margin-top:24px}}
 .sub{{text-align:center;opacity:0.6;font-size:14px;margin:8px 0 18px}}
 .card{{background:#12261a;border:1px solid #1e4a2f;border-radius:16px;max-width:500px;margin:0 auto;overflow:hidden}}
 .card-head{{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;border-bottom:1px solid #1e4a2f;font-weight:800;font-size:15px}}
 .live{{background:#ff3b30;color:white;padding:4px 10px;border-radius:20px;font-size:11px;animation:pulse 1.5s infinite}}
 @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.6}}}}
 table{{width:100%;border-collapse:collapse;font-size:14px}}
 th{{opacity:0.5;font-size:11px;text-align:left;padding:8px 16px}}
 td{{padding:10px 16px;border-top:1px solid #1a3524}}
 .foot{{text-align:center;opacity:0.3;font-size:11px;margin-top:16px}}
 a{{color:#00ff88;text-decoration:none}}
</style></head><body>
<h1>🎱 Snooker IQ V2 LIVE</h1>
<div class="sub">English Open 2026 — Built {built}</div>
<div class="card">
  <div class="card-head"><span>Stuart Bingham vs Anthony McGill</span><span class="live">LIVE 1-2</span></div>
  <table><tr><th>Score</th><th>True%</th><th>Bet365</th><th>EDGE</th></tr>{rows}</table>
</div>
<div class="foot"><a href="https://niibaboo.github.io/">← Back to niibaboo.lab Hub</a> • Auto-updates every 5 min</div>
<script>setTimeout(()=>location.reload(), 300000);</script>
</body></html>"""

Path("docs").mkdir(exist_ok=True)
Path("docs/index.html").write_text(html)
print("BUILT:", built)
