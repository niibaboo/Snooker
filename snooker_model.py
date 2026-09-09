import datetime
from pathlib import Path
import math

# === YOUR MODEL CORE ===
# This is your real model. Edit ratings here, or make it read your CSV/API.
ratings = {
    "Ding Junhui": 920, "Ashley Hugill": 765,
    "Zhang Anda": 845, "Mark Selby": 935,
    "Chang Bingyu": 710, "Kyren Wilson": 945,
    "Judd Trump": 985, "Ashley Carty": 725,
    "Oliver Lines": 795, "Yuan Sijun": 805,
    "Chris Wakelin": 835, "Zhou Yuelong": 815,
    "Sam Craigie": 785, "Joe O'Connor": 825,
    "Barry Hawkins": 885, "Daniel Wells": 775,
}

matches_bet365 = [
    (["Ding Junhui","Ashley Hugill"], {"win":[1.28,5.5],"cs42":[6.0,8.5],"hcp":[1.35,3.0],"over":1.55}),
    (["Zhang Anda","Mark Selby"], {"win":[2.20,1.66],"cs42":[6.50,6.00],"hcp":[1.57,2.25],"over":1.53}),
    (["Kyren Wilson","Chang Bingyu"], {"win":[1.18,5.00],"cs42":[5.5,9.0],"hcp":[1.30,3.30],"over":1.70}),
    (["Judd Trump","Ashley Carty"], {"win":[1.10,7.00],"cs42":[5.0,10.0],"hcp":[1.25,3.80],"over":1.80}),
    (["Yuan Sijun","Oliver Lines"], {"win":[1.85,1.95],"cs42":[6.50,6.50],"hcp":[1.57,2.25],"over":1.53}),
    (["Chris Wakelin","Zhou Yuelong"], {"win":[2.20,1.66],"cs42":[6.50,6.00],"hcp":[1.57,2.25],"over":1.53}),
    (["Joe O'Connor","Sam Craigie"], {"win":[1.72,2.10],"cs42":[6.50,6.50],"hcp":[1.50,2.50],"over":1.53}),
    (["Barry Hawkins","Daniel Wells"], {"win":[1.45,2.75],"cs42":[6.00,7.00],"hcp":[1.40,2.80],"over":1.60}),
]

def comb(n,k):
    r=1
    for i in range(1,k+1): r=r*(n-i+1)/i
    return r

def score_probs(p):
    return {
        "4-0": p**4,
        "4-1": comb(4,1)*p**4*(1-p),
        "4-2": comb(5,2)*p**4*(1-p)**2,
        "4-3": comb(6,3)*p**4*(1-p)**3,
        "3-4": comb(6,3)*p**3*(1-p)**4,
        "2-4": comb(5,2)*p**2*(1-p)**4,
        "1-4": comb(4,1)*p*(1-p)**4,
        "0-4": (1-p)**4,
    }

def p_frame(r1,r2): return 1/(1+10**((r2-r1)/400))

now = datetime.datetime.now(datetime.timezone.utc).astimezone()
built = now.strftime("%d %b %H:%M BST")

cards=""
for (m1,m2), o in matches_bet365:
    pf = p_frame(ratings[m1], ratings[m2])
    pr = score_probs(pf)
    pMatch = pr["4-0"]+pr["4-1"]+pr["4-2"]+pr["4-3"]
    over = pr["4-2"]+pr["4-3"]+pr["3-4"]+pr["2-4"]

    def edge(mp,odd): return mp*100 - 100/odd
    e1 = edge(pMatch, o["win"][0])
    e2 = edge(1-pMatch, o["win"][1])
    e_over = edge(over, o["over"])
    e_cs1 = edge(pr["4-2"], o["cs42"][0])

    def tag(e): return f'<span style="background:#00ff88;color:#05220f;padding:2px 6px;border-radius:10px;font-size:9px;font-weight:800;margin-left:4px">BET {e:+.1f}%</span>' if e>=3 else ''

    cards+=f"""
    <div class="card">
      <div class="head"><span>{m1} vs {m2} — frame {pf*100:.1f}%</span><span class="live">AUTO</span></div>
      <div class="m"><div class="mt">To Win Match</div><div class="g">
        <div class="b">{m1} {pMatch*100:.1f}% vs {100/o['win'][0]:.1f}% <b style="color:{'#00ff88' if e1>=2 else '#ff6b6b'}">{e1:+.1f}%</b> {tag(e1)}<br>Bet365 {o['win'][0]}</div>
        <div class="b">{m2} {(1-pMatch)*100:.1f}% vs {100/o['win'][1]:.1f}% <b style="color:{'#00ff88' if e2>=2 else '#ff6b6b'}">{e2:+.1f}%</b> {tag(e2)}<br>Bet365 {o['win'][1]}</div>
      </div></div>
      <div class="m"><div class="mt">Correct Score / Total (your screenshot markets)</div><div class="g">
        <div class="b">{m1} 4-2 {pr['4-2']*100:.1f}% vs {100/o['cs42'][0]:.1f}% <b style="color:{'#00ff88' if e_cs1>=2 else '#ff6b6b'}">{e_cs1:+.1f}%</b><br>Bet365 {o['cs42'][0]}</div>
        <div class="b">Over 5.5 {over*100:.1f}% vs {100/o['over']:.1f}% <b style="color:{'#00ff88' if e_over>=2 else '#ff6b6b'}">{e_over:+.1f}%</b> {tag(e_over)}<br>Bet365 {o['over']}</div>
      </div></div>
    </div>"""

html=f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Snooker IQ V4 AUTO</title>
<style>body{{background:#08120c;color:#eafff0;font-family:-apple-system,sans-serif;margin:0;padding:12px}}h1{{text-align:center;font-size:20px;margin-top:20px}}.sub{{text-align:center;opacity:.6;font-size:11px;margin:6px 0 14px}}.card{{background:#12261a;border:1px solid #1e4a2f;border-radius:14px;max-width:680px;margin:0 auto 12px;overflow:hidden}}.head{{display:flex;justify-content:space-between;padding:10px 12px;background:#0e2115;border-bottom:1px solid #1e4a2f;font-weight:800;font-size:12px}}.live{{background:#00ff88;color:#05220f;padding:3px 8px;border-radius:20px;font-size:9px}}.m{{padding:8px 10px;border-bottom:1px solid #132a1d}}.mt{{font-weight:800;font-size:11px;margin-bottom:6px;opacity:.85}}.g{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}.b{{background:#0a1a12;border:1px solid #1d3d2a;border-radius:8px;padding:6px 8px;font-size:10px;line-height:1.3}}.foot{{text-align:center;opacity:.3;font-size:10px;margin-top:12px}}</style></head><body>
<h1>🎱 Snooker IQ V4 FULL MARKETS</h1><div class="sub">Model auto-generates ALL markets from frame % • Built {built} • Best of 7</div>
<div id="root">{cards}</div>
<div class="foot"><a href="https://niibaboo.github.io/" style="color:#00ff88;text-decoration:none">← Hub</a> • Auto-updates every 5 min from snooker_model.py</div>
<script>setTimeout(()=>location.reload(),300000);</script>
</body></html>"""

Path("docs").mkdir(exist_ok=True)
Path("docs/index.html").write_text(html)
print("BUILT", built)
