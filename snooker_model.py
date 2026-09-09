import os, json, requests, math
from datetime import datetime

# --- AUTO ELO ---
def get_elo(p):
    # simple Elo diff to frame% - no typing needed
    return ratings.get(p, 750)

def frame_pct(elo1, elo2):
    diff = elo1 - elo2
    # 600 divisor = snooker frame variance, 50% baseline
    p = 1 / (1 + 10**(-diff/600))
    return max(5, min(95, p*100))

def race_to_3(p):
    q=1-p
    return (p**3)*(1 + 3*q + 6*q*q)

def fair(p): 
    return round(1/(p/100),2) if p>1 else 99

# load ratings
ratings = {}
if os.path.exists("ratings_auto.json"):
    try: ratings = json.load(open("ratings_auto.json"))
    except: ratings = {}

# --- AUTO MATCHES TODAY - no typing ---
# Try fetch from snooker.org, fallback to yesterday's list
matches_auto = []
try:
    r = requests.get("https://api.snooker.org/?t=6&s=2025", timeout=15).json()
    # r is list of matches, parse next 10
    for ev in r[:15]:
        if isinstance(ev, dict) and 'Player1ID' in ev:
            p1 = ev.get('Player1','Player1')
            p2 = ev.get('Player2','Player2')
            matches_auto.append({"p1":p1,"p2":p2})
except Exception as e:
    print(f"API fail {e}")

if not matches_auto:
    # fallback - your current card, will be auto-replaced when API works
    matches_auto = [
        {"p1":"Sam Craigie","p2":"Joe O'Connor"},
        {"p1":"Ding Junhui","p2":"Ashley Hugill"},
        {"p1":"Zhang Anda","p2":"Mark Selby"},
        {"p1":"Kyren Wilson","p2":"Chang Bingyu"},
    ]

# build final with auto frame%
final = []
for m in matches_auto:
    e1 = get_elo(m['p1']); e2 = get_elo(m['p2'])
    fp = frame_pct(e1,e2)
    final.append({**m, "elo1":e1, "elo2":e2, "frame":fp})

now = datetime.now().strftime("%d %b %H:%M BST")
html=f"""<html><head><meta name='viewport' content='width=device-width'>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:8px}}
.card{{background:#12291f;border-radius:12px;padding:12px;margin:12px 0}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 8px;float:right;font-size:11px;font-weight:bold}}
input{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:6px;width:60px;padding:5px;text-align:center;margin-left:6px;font-size:14px}}
.badge{{display:none;background:#00ff88;color:#000;font-weight:bold;padding:3px 8px;border-radius:6px;font-size:12px;margin-left:6px}}
.title{{color:#00ff88;font-weight:bold;margin-top:10px;font-size:12px}}
</style>
<script>
function check(id,fair){{let inp=document.getElementById(id);let badge=document.getElementById(id+'_b');let v=parseFloat(inp.value);if(v>fair){{badge.style.display='inline';badge.innerText='VALUE @ '+v+' > '+fair;}}else{{badge.style.display='none';}}}}
</script></head><body>
<h2>🎱 Snooker IQ V5.4 AUTO</h2>
<div style='opacity:0.6;font-size:11px;margin:0 10px'>Frame% = AUTO from Elo • You ONLY type Bet365 • Built {now}</div>
"""

for i,m in enumerate(final):
    p=m['frame']/100
    r1=race_to_3(p)*100; r2=100-r1
    f_r1=fair(r1); f_r2=fair(r2)
    html+=f"""
<div class='card'>
<b>{m['p1']} vs {m['p2']}</b> <span class='green'>AUTO frame {m['frame']:.1f}% | Elo {m['elo1']} vs {m['elo2']}</span><br>
<div class='title'>RACE TO 3 (Your screenshot)</div>
{m['p1']} {r1:.1f}% → Fair {f_r1} <input id='r1_{i}' placeholder='B365' oninput="check('r1_{i}',{f_r1})"><span id='r1_{i}_b' class='badge'></span><br>
{m['p2']} {r2:.1f}% → Fair {f_r2} <input id='r2_{i}' placeholder='B365' oninput="check('r2_{i}',{f_r2})"><span id='r2_{i}_b' class='badge'></span>
</div>"""

html+="</body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w").write(html)
print(f"V5.4 built {len(final)} matches auto frame%")
