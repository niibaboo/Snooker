import os, json, math
from datetime import datetime

def fair(p): return round(100/p,2) if p>0 else 99
def frame_pct(e1,e2): return max(5,min(95,(1/(1+10**(-(e1-e2)/600)))*100))
def race3(p): q=1-p; return (p**3)*(1+3*q+6*q*q)
def win_best7(p): q=1-p; s=0
def win_best7_fixed(p):
    q=1-p; prob=0
    for k in range(4): prob+= math.comb(3+k,k)*(p**4)*(q**k)
    return prob
def cs(p,q,n):
    # n=1 for 4-1 (C4,1), n=2 for 4-2 (C5,2)
    import math
    c = 4 if n==1 else 10
    return c*(p**4)*(q**n)
def over55(p): q=1-p; return 1-((p**4)*(1+4*q)+(q**4)*(1+4*p))

ratings={}
if os.path.exists("ratings_auto.json"):
    try: ratings=json.load(open("ratings_auto.json"))
    except: pass

matches=[
    {"p1":"Sam Craigie","p2":"Joe O'Connor","elo1":785,"elo2":825},
    {"p1":"Barry Hawkins","p2":"Daniel Wells","elo1":885,"elo2":775},
    {"p1":"Ding Junhui","p2":"Ashley Hugill","elo1":920,"elo2":765},
]

html = f"""
<html><head><meta name='viewport' content='width=device-width'>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:8px}}
.card{{background:#12291f;border-radius:14px;padding:12px;margin:14px 0;border:1px solid #1a3a2a}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 8px;float:right;font-size:11px;font-weight:bold}}
input{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:6px;width:58px;padding:5px;text-align:center;margin-left:6px}}
.badge{{display:inline-block;background:#333;color:#aaa;padding:3px 7px;border-radius:6px;font-size:11px;margin-left:6px;min-width:120px}}
.sec{{color:#00ff88;font-weight:bold;margin-top:10px;font-size:11px;border-top:1px solid #1a3a2a;padding-top:8px}}
.combo{{background:#0a2a1a;border:1px dashed #00ff88;border-radius:8px;padding:6px 8px;margin-top:6px;font-size:11px}}
</style>
<script>
function chk(id,fair){{let i=document.getElementById(id);let b=document.getElementById(id+'_b');let v=parseFloat(i.value);if(isNaN(v)){{b.innerText='Enter B365';b.style.background='#333';return;}}let e=((v/fair)-1)*100;if(v>fair){{b.style.background='#00ff88';b.style.color='#000';b.innerText='VALUE '+v+'>'+fair+' (+'+e.toFixed(1)+'%)'}}else{{b.style.background='#ff4444';b.style.color='#fff';b.innerText='NO VALUE ('+e.toFixed(1)+'%)'}} let idx=id.split('_')[1]; let a1=document.getElementById('a41_'+idx);let a2=document.getElementById('a42_'+idx);let box=document.getElementById('combo_'+idx);if(a1&&a2&&box){{let v1=parseFloat(a1.value);let v2=parseFloat(a2.value);if(!isNaN(v1)&&!isNaN(v2)){{let w=Math.min(v1*5,v2*5);let p=w-10;box.style.background=p>0?'#00ff8822':'#0a2a1a';box.innerHTML='COMBO £5+£5=£10 → Returns £'+w.toFixed(2)+' = '+(p>0?'+£'+p.toFixed(2)+' PROFIT':'-£'+Math.abs(p).toFixed(2))}}}}
</script></head><body><h2>🎱 V5.9 FULL • 4 MARKETS + DUAL</h2>
"""

for idx,m in enumerate(matches):
    e1=ratings.get(m['p1'],m['elo1']); e2=ratings.get(m['p2'],m['elo2'])
    fp=frame_pct(e1,e2); p=fp/100; q=1-p
    r1=race3(p)*100; w1=win_best7_fixed(p)*100
    c41=cs(p,q,1)*100; c42=cs(p,q,2)*100; c41b=cs(q,p,1)*100; c42b=cs(q,p,2)*100
    ov=over55(p)*100
    html+=f"""
<div class='card'><b>{m['p1']} vs {m['p2']}</b><span class='green'>{fp:.1f}%</span>
<div class='sec'>1. Race to 3</div>{m['p1']} {r1:.1f}% → Fair {fair(r1)} <input id='r1_{idx}' oninput="chk('r1_{idx}',{fair(r1)})"><span id='r1_{idx}_b' class='badge'>Enter</span><br>{m['p2']} {100-r1:.1f}% → Fair {fair(100-r1)} <input id='r2_{idx}' oninput="chk('r2_{idx}',{fair(100-r1)})"><span id='r2_{idx}_b' class='badge'>Enter</span>
<div class='sec'>2. Match Win</div>{m['p1']} {w1:.1f}% → Fair {fair(w1)} <input id='w1_{idx}' oninput="chk('w1_{idx}',{fair(w1)})"><span id='w1_{idx}_b' class='badge'>Enter</span><br>{m['p2']} {100-w1:.1f}% → Fair {fair(100-w1)} <input id='w2_{idx}' oninput="chk('w2_{idx}',{fair(100-w1)})"><span id='w2_{idx}_b' class='badge'>Enter</span>
<div class='sec'>3. Correct Score DUAL COVER</div>{m['p1']} 4-1 {c41:.1f}% → Fair {fair(c41)} <input id='a41_{idx}' oninput="chk('a41_{idx}',{fair(c41)})"><span id='a41_{idx}_b' class='badge'>Enter</span><br>{m['p1']} 4-2 {c42:.1f}% → Fair {fair(c42)} <input id='a42_{idx}' oninput="chk('a42_{idx}',{fair(c42)})"><span id='a42_{idx}_b' class='badge'>Enter</span><div id='combo_{idx}' class='combo'>Enter both B365 for combo profit</div>{m['p2']} 4-1 {c41b:.1f}% → Fair {fair(c41b)} <input id='b41_{idx}' oninput="chk('b41_{idx}',{fair(c41b)})"><span id='b41_{idx}_b' class='badge'>Enter</span><br>{m['p2']} 4-2 {c42b:.1f}% → Fair {fair(c42b)} <input id='b42_{idx}' oninput="chk('b42_{idx}',{fair(c42b)})"><span id='b42_{idx}_b' class='badge'>Enter</span>
<div class='sec'>4. Over 5.5 Frames</div>Over {ov:.1f}% → Fair {fair(ov)} <input id='o_{idx}' oninput="chk('o_{idx}',{fair(ov)})"><span id='o_{idx}_b' class='badge'>Enter</span>
</div>"""

html+="</body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w").write(html)
print("V5.9 built")
