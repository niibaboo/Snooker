import os, json, math
from datetime import datetime

def fair(p): return round(100/p,2) if p>0 else 99
def frame_pct(e1,e2): return max(5,min(95,(1/(1+10**(-(e1-e2)/600)))*100))
def race3(p): q=1-p; return (p**3)*(1+3*q+6*q*q)
def win_best7(p): q=1-p; s=0; [exec("s:=s+__import__('math').comb(3+k,k)*(p**4)*(q**k)", {'math':math,'p':p,'q':q,'k':k}) for k in range(4)]; return s
# fixed win calc
def win_best7_fixed(p):
    q=1-p; prob=0
    for k in range(4): prob+= math.comb(3+k,k)*(p**4)*(q**k)
    return prob
def cs_4_2(p): q=1-p; return math.comb(5,2)*(p**4)*(q**2)
def over55(p): q=1-p; return 1-((p**4)*(1+4*q)+(q**4)*(1+4*p))

# YOUR RESULTS LOG - edit this, it auto-renders like your screenshot
results_log = [
    {"match": "Stuart Bingham vs Anthony McGill — McGill WON 4-3", "true": 12.5, "b365": 9.00, "edge": 12.5, "ft": "FT 3-4", "won": True},
    {"match": "Ding Junhui vs Ashley Hugill — Ding 4-2", "true": 21.8, "b365": 4.00, "edge": 14.8, "ft": "FT 4-2", "won": True},
    {"match": "Sam Craigie vs Joe O'Connor — Sam ML", "true": 41.7, "b365": 3.20, "edge": 33.3, "ft": "PENDING", "won": None},
]

ratings={}
if os.path.exists("ratings_auto.json"):
    try: ratings=json.load(open("ratings_auto.json"))
    except: pass

matches=[
    {"p1":"Sam Craigie","p2":"Joe O'Connor","elo1":785,"elo2":825},
    {"p1":"Ding Junhui","p2":"Ashley Hugill","elo1":920,"elo2":765},
    {"p1":"Zhang Anda","p2":"Mark Selby","elo1":845,"elo2":935},
]

html_head = f"""
<html><head><meta name='viewport' content='width=device-width'>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:8px;margin:0}}
.card{{background:#12291f;border-radius:14px;padding:12px;margin:14px 0;border:1px solid #1a3a2a}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 8px;float:right;font-size:11px;font-weight:bold}}
input{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:6px;width:56px;padding:5px;text-align:center;margin-left:6px}}
.badge{{display:inline-block;background:#333;color:#aaa;padding:3px 7px;border-radius:6px;font-size:11px;margin-left:6px}}
.sec{{color:#00ff88;font-weight:bold;margin-top:10px;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;border-top:1px solid #1a3a2a;padding-top:8px}}
/* YOUR LIKED INTERFACE */
.result-card{{background:#0f231a;border:1px solid #1d3a2b;border-radius:16px;padding:12px 14px;margin:10px 0}}
.result-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}}
.result-ft{{background:#ff2d2d;color:#fff;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:bold}}
.result-grid{{display:grid;grid-template-columns:1.6fr 0.6fr 0.6fr 0.6fr;gap:6px;font-size:13px;opacity:0.8}}
.result-grid b{{opacity:1}}
.edge-win{{color:#00ff88;font-weight:bold}}
</style>
<script>
function chk(id,fair){{
  let i=document.getElementById(id); let b=document.getElementById(id+'_b'); let v=parseFloat(i.value);
  if(isNaN(v)){{b.innerText='Enter B365'; b.style.background='#333'; b.style.color='#aaa'; return;}}
  let edge=((v/fair)-1)*100;
  if(v>fair){{b.style.background='#00ff88'; b.style.color='#000'; b.innerText='VALUE '+v+'>'+fair+' (+'+edge.toFixed(1)+'%)';}}
  else{{b.style.background='#ff4444'; b.style.color='#fff'; b.innerText='NO VALUE '+v+'<'+fair+' ('+edge.toFixed(1)+'%)';}}
}}
</script></head><body>
<h2>🎱 Snooker IQ V5.7 • RESULTS + 4 MARKETS</h2>
"""

# Build results section like your screenshot
results_html = "<div style='margin:10px 0'><b style='color:#00ff88'>📊 RESULTS TRACKER</b></div>"
for r in results_log:
    ft_color = "#ff2d2d" if "FT" in r['ft'] else "#555"
    check = "✅" if r['won'] else "⏳" if r['won'] is None else "❌"
    results_html += f"""
<div class='result-card'>
  <div class='result-top'><b>{r['match']}</b><span class='result-ft' style='background:{ft_color}'>{r['ft']}</span></div>
  <div class='result-grid'>
    <div style='opacity:0.5'>Score</div><div style='opacity:0.5'>True%</div><div style='opacity:0.5'>Bet365</div><div style='opacity:0.5'>EDGE</div>
    <div>{r['match'].split('—')[-1][:20]}</div><div>{r['true']}%</div><div>{r['b365']}</div><div class='edge-win'>+{r['edge']}%<br>{check}</div>
  </div>
</div>"""

body=""
for idx,m in enumerate(matches):
    e1=ratings.get(m['p1'],m['elo1']); e2=ratings.get(m['p2'],m['elo2'])
    fp=frame_pct(e1,e2); p=fp/100; q=1-p
    r1=race3(p)*100; w1=win_best7_fixed(p)*100; cs=cs_4_2(p)*100; ov=over55(p)*100
    body+=f"""<div class='card'><b>{m['p1']} vs {m['p2']}</b><span class='green'>AUTO {fp:.1f}%</span>
<div class='sec'>Race to 3</div>{m['p1']} {r1:.1f}% → Fair {fair(r1)} <input id='r1_{idx}' oninput="chk('r1_{idx}',{fair(r1)})"><span id='r1_{idx}_b' class='badge'>Enter</span>
<div class='sec'>Match Win</div>{m['p1']} {w1:.1f}% → Fair {fair(w1)} <input id='w1_{idx}' oninput="chk('w1_{idx}',{fair(w1)})"><span id='w1_{idx}_b' class='badge'>Enter</span>
<div class='sec'>Correct Score 4-2</div>{m['p1']} 4-2 {cs:.1f}% → Fair {fair(cs)} <input id='c_{idx}' oninput="chk('c_{idx}',{fair(cs)})"><span id='c_{idx}_b' class='badge'>Enter</span>
<div class='sec'>Over 5.5</div>Over {ov:.1f}% → Fair {fair(ov)} <input id='o_{idx}' oninput="chk('o_{idx}',{fair(ov)})"><span id='o_{idx}_b' class='badge'>Enter</span>
</div>"""

final_html = html_head + results_html + body + "</body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w").write(final_html)
print("V5.7 built")
