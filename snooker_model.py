import os, json, csv, math, re, datetime
from datetime import datetime as dt
import urllib.request

def fair(p):
    return round(100/p, 2) if p > 0.5 else 99.0

def frame_pct(e1, e2):
    raw = 1 / (1 + 10 ** (-(e1 - e2) / 400))
    shrunk = 0.5 + (raw - 0.5) * 0.65
    return max(12.0, min(88.0, shrunk * 100))

def probs(p):
    q = 1-p
    p40 = (p**4)*100
    p41 = 4*(p**4)*q*100
    p42 = 10*(p**4)*(q*q)*100
    p43 = 20*(p**4)*(q**3)*100
    q40 = (q**4)*100
    q41 = 4*(q**4)*p*100
    q42 = 10*(q**4)*(p*p)*100
    q43 = 20*(q**4)*(p**3)*100
    win = p40+p41+p42+p43
    r3 = (p**3)*(1+3*q+6*q*q)*100
    over = 100 - (p40+p41+q40+q41)
    all_s = {"p40":p40,"p41":p41,"p42":p42,"p43":p43,"q40":q40,"q41":q41,"q42":q42,"q43":q43}
    best = max(all_s, key=lambda k: all_s[k])
    return {"p40":p40,"p41":p41,"p42":p42,"p43":p43,"q40":q40,"q41":q41,"q42":q42,"q43":q43,"win":win,"r3":r3,"over":over,"best_key":best,"best_prob":all_s[best]}

ratings = {}
if os.path.exists("ratings_auto.json"):
    try: ratings = json.load(open("ratings_auto.json", encoding='utf-8'))
    except: pass

matches = []
for fname in ["snooker_fixtures.csv","fixtures.csv"]:
    if os.path.exists(fname):
        try:
            with open(fname, encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    p1 = (row.get('p1') or row.get('home') or '').strip()
                    p2 = (row.get('p2') or row.get('away') or '').strip()
                    if p1 and p2: matches.append({"p1":p1,"p2":p2,"elo1":800,"elo2":800})
            if matches: break
        except: pass

if not matches:
    matches = [{"p1":"Mark Selby","p2":"Kyren Wilson","elo1":900,"elo2":880},{"p1":"Yuan Sijun","p2":"Zhou Yuelong","elo1":810,"elo2":815},{"p1":"Joe O'Connor","p2":"Ding Junhui","elo1":790,"elo2":870},{"p1":"Liam Davies","p2":"Wu Yize","elo1":750,"elo2":850}]

html = f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Snooker V6.8 Calibrated Standalone</title>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:10px;margin:0;padding-bottom:120px}}
.card{{background:#12291f;border-radius:16px;padding:14px;margin:14px 0;border:1px solid #1a3a2a}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 10px;float:right;font-size:11px;font-weight:bold}}
.sec{{color:#00ff88;font-weight:bold;margin-top:14px;font-size:11px;border-top:1px solid #1a3a2a;padding-top:10px}}
.row{{display:flex;align-items:center;flex-wrap:wrap;margin:6px 0;font-size:13px}}
input[type=text]{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:8px;width:62px;padding:6px;text-align:center;margin-left:8px}}
.badge{{background:#2a2a2a;color:#999;padding:4px 8px;border-radius:8px;font-size:11px;margin-left:8px;min-width:120px}}
.topbar{{background:#0f231a;border-bottom:1px solid #1a3a2a;padding:12px;border-radius:12px;margin-bottom:10px}}
.meta{{font-size:11px;opacity:0.6;margin-top:4px}}
</style>
<script>
function chk(id,f){{let i=document.getElementById(id);let b=document.getElementById(id+'_b');let v=parseFloat(i.value);if(isNaN(v)){{b.innerText='Enter';b.style.background='#2a2a2a';return;}}let e=((v/f)-1)*100;if(v>f){{b.style.background='#00ff88';b.style.color='#000';b.innerText='VALUE '+v+'>'+f+' (+'+e.toFixed(1)+'%)'}}else{{b.style.background='#ff4444';b.style.color='#fff';b.innerText='NO VALUE ('+e.toFixed(1)+'%)'}}}}
</script></head><body>
<div class='topbar'><h2 style='margin:0'>🎱 V6.8 CALIBRATED STANDALONE</h2>
<div class='meta'>{dt.now().strftime("%d %b %H:%M")} · {len(matches)} matches · Shrink 0.65 · Max 88% frame · Fixed 4-0/4-3 bug</div></div>
"""
for idx,m in enumerate(matches):
    e1=ratings.get(m['p1'],m['elo1']); e2=ratings.get(m['p2'],m['elo2'])
    fp=frame_pct(e1,e2); pr=probs(fp/100)
    best_map={"p40":f"{m['p1']} 4-0","p41":f"{m['p1']} 4-1","p42":f"{m['p1']} 4-2","p43":f"{m['p1']} 4-3","q40":f"{m['p2']} 4-0","q41":f"{m['p2']} 4-1","q42":f"{m['p2']} 4-2","q43":f"{m['p2']} 4-3"}
    html+=f"""<div class='card'><b>{m['p1']} vs {m['p2']}</b><span class='green'>{fp:.1f}% frame</span>
<div style='font-size:11px;opacity:0.7'>Best {best_map[pr['best_key']]} {pr['best_prob']:.1f}% Fair {fair(pr['best_prob'])} · Match {pr['win']:.1f}%</div>
<div class='sec'>Correct Score — ALL 8 SCORES</div>
<div class='row'>{m['p1']} 4-0 {pr['p40']:.1f}% Fair {fair(pr['p40'])} <input type=text id='a40_{idx}' oninput="chk('a40_{idx}',{fair(pr['p40'])})"><span id='a40_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p1']} 4-1 {pr['p41']:.1f}% Fair {fair(pr['p41'])} <input type=text id='a41_{idx}' oninput="chk('a41_{idx}',{fair(pr['p41'])})"><span id='a41_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p1']} 4-2 {pr['p42']:.1f}% Fair {fair(pr['p42'])} <input type=text id='a42_{idx}' oninput="chk('a42_{idx}',{fair(pr['p42'])})"><span id='a42_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p1']} 4-3 {pr['p43']:.1f}% Fair {fair(pr['p43'])} <input type=text id='a43_{idx}' oninput="chk('a43_{idx}',{fair(pr['p43'])})"><span id='a43_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p2']} 4-0 {pr['q40']:.1f}% Fair {fair(pr['q40'])} <input type=text id='b40_{idx}' oninput="chk('b40_{idx}',{fair(pr['q40'])})"><span id='b40_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p2']} 4-1 {pr['q41']:.1f}% Fair {fair(pr['q41'])} <input type=text id='b41_{idx}' oninput="chk('b41_{idx}',{fair(pr['q41'])})"><span id='b41_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p2']} 4-2 {pr['q42']:.1f}% Fair {fair(pr['q42'])} <input type=text id='b42_{idx}' oninput="chk('b42_{idx}',{fair(pr['q42'])})"><span id='b42_{idx}_b' class='badge'>Enter</span></div>
<div class='row'>{m['p2']} 4-3 {pr['q43']:.1f}% Fair {fair(pr['q43'])} <input type=text id='b43_{idx}' oninput="chk('b43_{idx}',{fair(pr['q43'])})"><span id='b43_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>Race to 3 + Over 5.5</div>
<div class='row'>Over 5.5 {pr['over']:.1f}% Fair {fair(pr['over'])} <input type=text id='ov_{idx}' oninput="chk('ov_{idx}',{fair(pr['over'])})"><span id='ov_{idx}_b' class='badge'>Enter</span></div>
</div>"""
html+="</body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w",encoding='utf-8').write(html)
print(f"V6.8 built {len(matches)} matches")
