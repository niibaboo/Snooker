import requests, json, math
from datetime import datetime

# --- YOUR V5 AUTO LOGIC STAYS SAME ---
# Elo etc from snooker.org (keep your existing fetch code here)
# For this fix I only changed the HTML part below

def fair(p):
    return round(1/(p/100), 2) if p>1 else 99

def build_html(matches):
    html = f"""
<html><head><meta name='viewport' content='width=device-width'>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial}}
.card{{background:#12291f;border-radius:12px;padding:12px;margin:10px}}
.bet{{background:#00ff88;color:#000;border-radius:6px;padding:2px 6px;font-weight:bold}}
.green{{background:#0f4;color:#000;border-radius:12px;padding:2px 8px;float:right}}
</style></head><body>
<h2>🎱 Snooker IQ V5.1 AUTO</h2>
<div style='opacity:0.7;font-size:12px'>Frame% → Our Fair Odds • Built {datetime.now().strftime('%d %b %H:%M')} BST • Auto every 5m</div>
"""
    for m in matches:
        f = m['frame_pct']
        html += f"""
<div class='card'>
<b>{m['p1']} vs {m['p2']}</b> <span class='green'>frame {f}% | Elo {m['elo1']} vs {m['elo2']}</span><br><br>
To Win: {m['p1']} {m['win1']}% @ Fair {fair(m['win1'])}<br>
To Win: {m['p2']} {m['win2']}% @ Fair {fair(m['win2'])}<br><br>
Correct 4-2 {m['p1']} {m['cs1']}% @ Fair {fair(m['cs1'])}<br>
Over 5.5 {m['over']}% @ Fair {fair(m['over'])}
</div>"""
    html += "</body></html>"
    open('docs/index.html','w').write(html)
    print("V5.1 built - no Bet365 odds")

# Example call - keep your existing matches loop and then call build_html(matches)
