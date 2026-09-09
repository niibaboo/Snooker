import os, json, math
from datetime import datetime

def fair(p): return round(1/(p/100),2) if p>0.5 else round(1/(p/100),2)
def frame_pct(e1,e2):
    diff=e1-e2
    p=1/(1+10**(-diff/600))
    return max(5,min(95,p*100))
def race3(p):
    q=1-p
    return (p**3)*(1+3*q+6*q*q)
def win_best7(p):
    q=1-p
    # first to 4: sum k=0..3 C(3+k,k) p^4 q^k
    prob=0
    for k in range(4):
        prob+= math.comb(3+k,k) * (p**4)*(q**k)
    return prob
def cs_4_2(p):
    q=1-p
    return math.comb(5,2)*(p**4)*(q**2) # 10 * p^4 q^2

ratings={}
if os.path.exists("ratings_auto.json"):
    try: ratings=json.load(open("ratings_auto.json"))
    except: pass

matches_auto=[
    {"p1":"Sam Craigie","p2":"Joe O'Connor"},
    {"p1":"Ding Junhui","p2":"Ashley Hugill"},
    {"p1":"Zhang Anda","p2":"Mark Selby"},
    {"p1":"Kyren Wilson","p2":"Chang Bingyu"},
    {"p1":"Judd Trump","p2":"Ashley Carty"},
]

final=[]
for m in matches_auto:
    e1=ratings.get(m['p1'], 800 if 'Craigie' in m['p1'] else 850)
    e2=ratings.get(m['p2'], 825)
    # override with your live Elos from screenshot
    if m['p1']=='Sam Craigie': e1=785
    if m['p2']=="Joe O'Connor": e2=825
    if m['p1']=='Ding Junhui': e1=920; e2=765
    if m['p1']=='Zhang Anda': e1=845; e2=935
    if m['p1']=='Kyren Wilson': e1=945; e2=710
    if m['p1']=='Judd Trump': e1=985; e2=725
    fp=frame_pct(e1,e2)
    final.append({**m,"elo1":e1,"elo2":e2,"frame":fp})

now=datetime.now().strftime("%d %b %H:%M BST")
html=f"""<html><head><meta name='viewport' content='width=device-width'>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:8px;margin:0}}
.card{{background:#12291f;border-radius:14px;padding:12px;margin:14px 0;border:1px solid #1a3a2a}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 8px;float:right;font-size:11px;font-weight:bold}}
input{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:6px;width:56px;padding:5px;text-align:center;margin-left:6px}}
.badge{{display:none;background:#00ff88;color:#000;font-weight:bold;padding:3px 7px;border-radius:6px;font-size:11px;margin-left:6px}}
.sec{{color:#00ff88;font-weight:bold;margin-top:10px;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;border-top:1px solid #1a3a2a;padding-top:8px}}
</style>
<script>
function chk(id,fair){{let i=document.getElementById(id);let b=document.getElementById(id+'_b');let v=parseFloat(i.value);if(!isNaN(v)&&v>fair){{b.style.display='inline';b.innerText='VALUE '+v+'>'+fair;}}else{{b.style.display='none';}}}}
</script></head><body>
<h2>🎱 Snooker IQ V5.5 • 3 MARKETS</h2>
<div style='opacity:0.6;font-size:11px;margin:0 10px 10px'>AUTO frame% • Type B365 only • Built {now}</div>
"""

for idx,m in enumerate(final):
    p=m['frame']/100; q=1-p
    r1=race3(p)*100; r2=100-r1
    w1=win_best7(p)*100; w2=100-w1
    cs1=cs_4_2(p)*100; cs2=cs_4_2(q)*100

    html+=f"""
<div class='card'>
<b>{m['p1']} vs {m['p2']}</b> <span class='green'>AUTO {m['frame']:.1f}% | {m['elo1']} vs {m['elo2']}</span>

<div class='sec'>1. Race to 3 Frames</div>
{m['p1']} {r1:.1f}% → Fair {fair(r1)} <input id='r1_{idx}' placeholder='B365' oninput="chk('r1_{idx}',{fair(r1)})"><span id='r1_{idx}_b' class='badge'></span><br>
{m['p2']} {r2:.1f}% → Fair {fair(r2)} <input id='r2_{idx}' placeholder='B365' oninput="chk('r2_{idx}',{fair(r2)})"><span id='r2_{idx}_b' class='badge'></span>

<div class='sec'>2. Match Win (First to 4)</div>
{m['p1']} {w1:.1f}% → Fair {fair(w1)} <input id='w1_{idx}' placeholder='B365' oninput="chk('w1_{idx}',{fair(w1)})"><span id='w1_{idx}_b' class='badge'></span><br>
{m['p2']} {w2:.1f}% → Fair {fair(w2)} <input id='w2_{idx}' placeholder='B365' oninput="chk('w2_{idx}',{fair(w2)})"><span id='w2_{idx}_b' class='badge'></span>

<div class='sec'>3. Correct Score 4-2</div>
{m['p1']} 4-2 {cs1:.1f}% → Fair {fair(cs1)} <input id='c1_{idx}' placeholder='B365' oninput="chk('c1_{idx}',{fair(cs1)})"><span id='c1_{idx}_b' class='badge'></span><br>
{m['p2']} 4-2 {cs2:.1f}% → Fair {fair(cs2)} <input id='c2_{idx}' placeholder='B365' oninput="chk('c2_{idx}',{fair(cs2)})"><span id='c2_{idx}_b' class='badge'></span>
</div>"""

html+="</body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w").write(html)
print("V5.5 3 markets built")
