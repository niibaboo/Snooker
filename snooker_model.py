import os, json, math
from datetime import datetime

def fair(p): return round(100/p,2) if p>1 else 99
def frame_pct(e1,e2): return max(5,min(95,(1/(1+10**(-(e1-e2)/600)))*100))
def probs(p):
    q=1-p
    return {
        "p41": 4*(p**4)*q*100, "p42": 10*(p**4)*(q*q)*100,
        "q41": 4*(q**4)*p*100, "q42": 10*(q**4)*(p*p)*100,
        "win": (p**4 + 4*p**4*q + 10*p**4*q*q + 20*p**4*q*q*q)*100,
        "r3": (p**3)*(1+3*q+6*q*q)*100,
        "over": (1-((p**4)*(1+4*q)+(q**4)*(1+4*p)))*100
    }

ratings={}
if os.path.exists("ratings_auto.json"):
    try: ratings=json.load(open("ratings_auto.json"))
    except: pass

matches=[
    {"p1":"Sam Craigie","p2":"Joe O'Connor","elo1":785,"elo2":825},
    {"p1":"Barry Hawkins","p2":"Daniel Wells","elo1":885,"elo2":775},
    {"p1":"Ding Junhui","p2":"Ashley Hugill","elo1":920,"elo2":765},
]

html=f"""
<html><head><meta name='viewport' content='width=device-width'>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:10px;margin:0}}
.card{{background:#12291f;border-radius:16px;padding:14px;margin:14px 0;border:1px solid #1a3a2a}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 10px;float:right;font-size:11px;font-weight:bold}}
.sec{{color:#00ff88;font-weight:bold;margin-top:14px;font-size:11px;border-top:1px solid #1a3a2a;padding-top:10px}}
.row{{display:flex;align-items:center;flex-wrap:wrap;margin:6px 0;font-size:13px}}
input[type=text]{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:8px;width:62px;padding:6px;text-align:center;margin-left:8px}}
.badge{{background:#2a2a2a;color:#999;padding:4px 8px;border-radius:8px;font-size:11px;margin-left:8px;min-width:120px}}
.acca-bar{{position:sticky;bottom:0;background:#0f231a;border:2px solid #00ff88;border-radius:14px;padding:12px;margin-top:20px}}
.tick{{width:18px;height:18px;accent-color:#00ff88;margin-right:6px}}
</style>
<script>
let sel={{}};
function chk(id,f){{let i=document.getElementById(id);let b=document.getElementById(id+'_b');let v=parseFloat(i.value);if(isNaN(v)){{b.innerText='Enter';b.style.background='#2a2a2a';updateAcca();return;}}let e=((v/f)-1)*100;if(v>f){{b.style.background='#00ff88';b.style.color='#000';b.innerText='VALUE '+v+'>'+f+' (+'+e.toFixed(1)+'%)'}}else{{b.style.background='#ff4444';b.style.color='#fff';b.innerText='NO VALUE ('+e.toFixed(1)+'%)'}}updateAcca();}}
function toggleAcca(cb,id,prob,label){{if(cb.checked)sel[id]={{prob:prob,label:label}};else delete sel[id];updateAcca();}}
function updateAcca(){{
let bar=document.getElementById('acca-bar');let keys=Object.keys(sel);if(keys.length==0){{bar.innerHTML='<b>ACCA BUILDER:</b> Tick 2-3 games from DIFFERENT matches. Same-match blocked by B365.';return;}}
let tp=1;let bProd=1;let valid=true;let legs='';for(let k of keys){{let pr=sel[k].prob;tp*=(pr/100);let inp=document.getElementById(k);let bv=parseFloat(inp?inp.value:NaN);if(isNaN(bv))valid=false;else bProd*=bv;legs+='<div>'+sel[k].label+' '+pr.toFixed(1)+'% @ '+(isNaN(bv)?'--':bv)+'</div>';}}
let fair=tp>0?1/tp:0;let pct=tp*100;let h='<b>🎯 '+keys.length+'-LEG ACCA (cross-game)</b><div style=margin:6px 0>'+legs+'</div><div>True '+pct.toFixed(3)+'% → Fair '+fair.toFixed(2)+'</div>';if(!valid)h+='<div style=color:#ffaa00>Enter B365 for all ticked legs</div>';else{{let edge=((bProd/fair)-1)*100;let col=edge>0?'#00ff88':'#ff4444';let txt=edge>0?'VALUE ✅':'NO VALUE ❌';h+='<div>B365 Acca '+bProd.toFixed(2)+' → <span style=background:'+col+';color:#000;padding:3px 8px;border-radius:8px;font-weight:bold>'+txt+' '+edge.toFixed(1)+'%</span></div><div style=font-size:11px;opacity:0.7>£10 returns £'+(bProd*10).toFixed(2)+'. Yesterday: 2/3 singles +£57.50 vs treble -£10</div>';}}bar.innerHTML=h;
}}
</script></head><body><h2>🎱 V6.0 • 4 MARKETS + CROSS-GAME ACCA</h2>
<div style='opacity:0.6;font-size:11px'>Yesterday 2/3 singles +£57.50 | Treble 82.27 lost</div>
"""

for idx,m in enumerate(matches):
    e1=ratings.get(m['p1'],m['elo1']); e2=ratings.get(m['p2'],m['elo2'])
    fp=frame_pct(e1,e2); pr=probs(fp/100)
    html+=f"""<div class='card'><b>{m['p1']} vs {m['p2']}</b><span class='green'>{fp:.1f}%</span>
<div class='sec'>1. Race to 3</div><div class='row'>{m['p1']} {pr['r3']:.1f}% → Fair {fair(pr['r3'])} <input type=text id='r1_{idx}' oninput="chk('r1_{idx}',{fair(pr['r3'])})"><span id='r1_{idx}_b' class='badge'>Enter</span></div><div class='row'>{m['p2']} {100-pr['r3']:.1f}% → Fair {fair(100-pr['r3'])} <input type=text id='r2_{idx}' oninput="chk('r2_{idx}',{fair(100-pr['r3'])})"><span id='r2_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>2. Match Win</div><div class='row'>{m['p1']} {pr['win']:.1f}% → Fair {fair(pr['win'])} <input type=text id='w1_{idx}' oninput="chk('w1_{idx}',{fair(pr['win'])})"><span id='w1_{idx}_b' class='badge'>Enter</span></div><div class='row'>{m['p2']} {100-pr['win']:.1f}% → Fair {fair(100-pr['win'])} <input type=text id='w2_{idx}' oninput="chk('w2_{idx}',{fair(100-pr['win'])})"><span id='w2_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>3. Correct Score — tick for ACCA (cross-game only)</div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'a41_{idx}',{pr['p41']},'{m['p1']} 4-1')">{m['p1']} 4-1 {pr['p41']:.1f}% → Fair {fair(pr['p41'])} <input type=text id='a41_{idx}' oninput="chk('a41_{idx}',{fair(pr['p41'])})"><span id='a41_{idx}_b' class='badge'>Enter</span></div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'a42_{idx}',{pr['p42']},'{m['p1']} 4-2')">{m['p1']} 4-2 {pr['p42']:.1f}% → Fair {fair(pr['p42'])} <input type=text id='a42_{idx}' oninput="chk('a42_{idx}',{fair(pr['p42'])})"><span id='a42_{idx}_b' class='badge'>Enter</span></div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'b41_{idx}',{pr['q41']},'{m['p2']} 4-1')">{m['p2']} 4-1 {pr['q41']:.1f}% → Fair {fair(pr['q41'])} <input type=text id='b41_{idx}' oninput="chk('b41_{idx}',{fair(pr['q41'])})"><span id='b41_{idx}_b' class='badge'>Enter</span></div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'b42_{idx}',{pr['q42']},'{m['p2']} 4-2')">{m['p2']} 4-2 {pr['q42']:.1f}% → Fair {fair(pr['q42'])} <input type=text id='b42_{idx}' oninput="chk('b42_{idx}',{fair(pr['q42'])})"><span id='b42_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>4. Over 5.5</div><div class='row'>Over {pr['over']:.1f}% → Fair {fair(pr['over'])} <input type=text id='ov_{idx}' oninput="chk('ov_{idx}',{fair(pr['over'])})"><span id='ov_{idx}_b' class='badge'>Enter</span></div></div>"""

html+="<div id='acca-bar' class='acca-bar'><b>ACCA BUILDER:</b> Tick 2-3 games from DIFFERENT matches. Same-match blocked by B365.</div></body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w").write(html)
print("V6.0 built")
