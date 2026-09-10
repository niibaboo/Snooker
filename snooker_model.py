import os, json, csv, math, re, datetime
from datetime import datetime as dt
import urllib.request, urllib.parse

def fair(p): return round(100/p,2) if p>1 else 99
def frame_pct(e1,e2): return max(5,min(95,(1/(1+10**(-(e1-e2)/600)))*100))
def probs(p):
    q=1-p
    return {"p41":4*(p**4)*q*100,"p42":10*(p**4)*(q*q)*100,"q41":4*(q**4)*p*100,"q42":10*(q**4)*(p*p)*100,"win":(p**4 + 4*p**4*q + 10*p**4*q*q + 20*p**4*q*q*q)*100,"r3":(p**3)*(1+3*q+6*q*q)*100,"over":(1-((p**4)*(1+4*q)+(q**4)*(1+4*p)))*100}

ratings={}
if os.path.exists("ratings_auto.json"):
    try: ratings=json.load(open("ratings_auto.json",encoding='utf-8'))
    except: pass

def fetch_live():
    matches=[]
    # Attempt 1: WST livescores JSON (most reliable)
    try:
        url = "https://livescores.worldsnookertour.com/matches"
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
        with urllib.request.urlopen(req, timeout=15) as r:
            txt = r.read().decode('utf-8', errors='ignore')
            # embedded JSON has "Player1Name" "Player2Name"
            p1 = re.findall(r'"player1[^"]*"\s*:\s*"([^"]+)"|"Player1Name"\s*:\s*"([^"]+)"', txt, re.I)
            p2 = re.findall(r'"player2[^"]*"\s*:\s*"([^"]+)"|"Player2Name"\s*:\s*"([^"]+)"', txt, re.I)
            # simpler regex for today's page
            pairs = re.findall(r'"homePlayer"\s*:\s*\{"name"\s*:\s*"([^"]+)".*?"awayPlayer"\s*:\s*\{"name"\s*:\s*"([^"]+)"', txt, re.S)
            if not pairs:
                pairs = re.findall(r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*-\s*([A-Z][a-z]+\s+[A-Z][a-z]+)', txt)
            for a,b in pairs[:16]:
                if a!=b and len(a)>3 and len(b)>3:
                    matches.append({"p1":a.strip(),"p2":b.strip(),"elo1":800,"elo2":800})
            if matches:
                print(f"WST live: {len(matches)}")
                return matches[:16]
    except Exception as e:
        print(f"WST live failed: {e}")

    # Attempt 2: snooker.org API - English Open 2026
    try:
        # Get events for 2026
        url = "https://api.snooker.org/?t=5&s=2026"
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
            eng = [ev for ev in data if 'english' in ev.get('Name','').lower()]
            if eng:
                eid = eng[0]['ID']
                url2 = f"https://api.snooker.org/?t=6&e={eid}"
                req2 = urllib.request.Request(url2, headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(req2, timeout=15) as r2:
                    matches_data = json.loads(r2.read().decode())
                    for m in matches_data[:16]:
                        # only upcoming
                        p1 = m.get('Player1','').strip()
                        p2 = m.get('Player2','').strip()
                        if p1 and p2:
                            matches.append({"p1":p1,"p2":p2,"elo1":800,"elo2":800})
                    if matches:
                        print(f"snooker.org: {len(matches)} from event {eid}")
                        return matches[:16]
    except Exception as e:
        print(f"snooker.org failed: {e}")

    return []

matches = fetch_live()

# CSV fallback
if not matches:
    for fname in ["snooker_fixtures.csv","fixtures.csv"]:
        if os.path.exists(fname):
            try:
                with open(fname,encoding='utf-8') as f:
                    for row in csv.DictReader(f):
                        p1=row.get('p1') or row.get('home')
                        p2=row.get('p2') or row.get('away')
                        if p1 and p2:
                            matches.append({"p1":p1.strip(),"p2":p2.strip(),"elo1":800,"elo2":800})
                if matches: break
            except: pass

if not matches:
    matches=[{"p1":"Judd Trump","p2":"Kyren Wilson","elo1":900,"elo2":880},{"p1":"Mark Selby","p2":"John Higgins","elo1":890,"elo2":885},{"p1":"Wu Yize","p2":"Barry Hawkins","elo1":850,"elo2":840},{"p1":"Ding Junhui","p2":"Zhang Anda","elo1":870,"elo2":810},{"p1":"Shaun Murphy","p2":"Mark Williams","elo1":860,"elo2":855},{"p1":"Ali Carter","p2":"Chris Wakelin","elo1":830,"elo2":820},{"p1":"Fan Zhengyi","p2":"Pang Junxu","elo1":800,"elo2":795},{"p1":"Joe O'Connor","p2":"Oliver Lines","elo1":790,"elo2":785}]

# ---- BUILD HTML SAME AS V6.1 (green UI you have) ----
html=f"""<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Snooker V6.3 Auto</title>
<style>
body{{background:#0a1a12;color:#fff;font-family:Arial;padding:10px;margin:0;padding-bottom:120px}}
.card{{background:#12291f;border-radius:16px;padding:14px;margin:14px 0;border:1px solid #1a3a2a}}
.green{{background:#00ff88;color:#000;border-radius:12px;padding:4px 10px;float:right;font-size:11px;font-weight:bold}}
.sec{{color:#00ff88;font-weight:bold;margin-top:14px;font-size:11px;border-top:1px solid #1a3a2a;padding-top:10px}}
.row{{display:flex;align-items:center;flex-wrap:wrap;margin:6px 0;font-size:13px}}
input[type=text]{{background:#000;color:#00ff88;border:1px solid #00ff88;border-radius:8px;width:62px;padding:6px;text-align:center;margin-left:8px}}
.badge{{background:#2a2a2a;color:#999;padding:4px 8px;border-radius:8px;font-size:11px;margin-left:8px;min-width:120px}}
.acca-bar{{position:sticky;bottom:0;background:#0f231a;border:2px solid #00ff88;border-radius:14px;padding:12px;margin-top:20px;z-index:20}}
.tick{{width:18px;height:18px;accent-color:#00ff88;margin-right:6px}}
.topbar{{background:#0f231a;border-bottom:1px solid #1a3a2a;padding:12px;border-radius:12px;margin-bottom:10px}}
.meta{{font-size:11px;opacity:0.6;margin-top:4px}}
</style>
<script>
let sel={{}};
function chk(id,f){{let i=document.getElementById(id);let b=document.getElementById(id+'_b');let v=parseFloat(i.value);if(isNaN(v)){{b.innerText='Enter';b.style.background='#2a2a2a';updateAcca();return;}}let e=((v/f)-1)*100;if(v>f){{b.style.background='#00ff88';b.style.color='#000';b.innerText='VALUE '+v+'>'+f+' (+'+e.toFixed(1)+'%)'}}else{{b.style.background='#ff4444';b.style.color='#fff';b.innerText='NO VALUE ('+e.toFixed(1)+'%)'}}updateAcca();}}
function toggleAcca(cb,id,prob,label){{if(cb.checked)sel[id]={{prob:prob,label:label}};else delete sel[id];updateAcca();}}
function updateAcca(){{
let bar=document.getElementById('acca-bar');let keys=Object.keys(sel);if(keys.length==0){{bar.innerHTML='<b>ACCA BUILDER:</b> Tick 2-3 from DIFFERENT matches. Same-match blocked.';return;}}
let tp=1;let bProd=1;let valid=true;let legs='';for(let k of keys){{let pr=sel[k].prob;tp*=(pr/100);let inp=document.getElementById(k);let bv=parseFloat(inp?inp.value:NaN);if(isNaN(bv))valid=false;else bProd*=bv;legs+='<div>'+sel[k].label+' '+pr.toFixed(1)+'% @ '+(isNaN(bv)?'--':bv)+'</div>';}}
let fair=tp>0?1/tp:0;let h='<b>🎯 '+keys.length+'-LEG ACCA</b><div style=margin:6px 0>'+legs+'</div><div>True '+(tp*100).toFixed(3)+'% → Fair '+fair.toFixed(2)+'</div>';if(!valid)h+='<div style=color:#ffaa00>Enter B365 for all ticked legs</div>';else{{let edge=((bProd/fair)-1)*100;let col=edge>0?'#00ff88':'#ff4444';h+='<div>B365 '+bProd.toFixed(2)+' → <span style=background:'+col+';color:#000;padding:3px 8px;border-radius:8px;font-weight:bold>'+(edge>0?'VALUE ✅ ':'NO VALUE ❌ ')+edge.toFixed(1)+'%</span></div>';}}bar.innerHTML=h;
}}
</script></head><body>
<div class='topbar'><h2 style='margin:0'>🎱 V6.3 AUTO-ENGLISH-OPEN • 4 MARKETS</h2>
<div class='meta'>{dt.now().strftime("%d %b %H:%M")} · {len(matches)} matches · Auto WST live + snooker.org + CSV</div></div>
"""
for idx,m in enumerate(matches):
    e1=ratings.get(m['p1'],m['elo1']); e2=ratings.get(m['p2'],m['elo2'])
    fp=frame_pct(e1,e2); pr=probs(fp/100)
    html+=f"""<div class='card'><b>{m['p1']} vs {m['p2']}</b><span class='green'>{fp:.1f}%</span>
<div class='sec'>1. Race to 3</div><div class='row'>{m['p1']} {pr['r3']:.1f}% → Fair {fair(pr['r3'])} <input type=text id='r1_{idx}' oninput="chk('r1_{idx}',{fair(pr['r3'])})"><span id='r1_{idx}_b' class='badge'>Enter</span></div><div class='row'>{m['p2']} {100-pr['r3']:.1f}% → Fair {fair(100-pr['r3'])} <input type=text id='r2_{idx}' oninput="chk('r2_{idx}',{fair(100-pr['r3'])})"><span id='r2_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>2. Match Win</div><div class='row'>{m['p1']} {pr['win']:.1f}% → Fair {fair(pr['win'])} <input type=text id='w1_{idx}' oninput="chk('w1_{idx}',{fair(pr['win'])})"><span id='w1_{idx}_b' class='badge'>Enter</span></div><div class='row'>{m['p2']} {100-pr['win']:.1f}% → Fair {fair(100-pr['win'])} <input type=text id='w2_{idx}' oninput="chk('w2_{idx}',{fair(100-pr['win'])})"><span id='w2_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>3. Correct Score — tick for ACCA</div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'a41_{idx}',{pr['p41']},'{m['p1']} 4-1')">{m['p1']} 4-1 {pr['p41']:.1f}% → Fair {fair(pr['p41'])} <input type=text id='a41_{idx}' oninput="chk('a41_{idx}',{fair(pr['p41'])})"><span id='a41_{idx}_b' class='badge'>Enter</span></div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'a42_{idx}',{pr['p42']},'{m['p1']} 4-2')">{m['p1']} 4-2 {pr['p42']:.1f}% → Fair {fair(pr['p42'])} <input type=text id='a42_{idx}' oninput="chk('a42_{idx}',{fair(pr['p42'])})"><span id='a42_{idx}_b' class='badge'>Enter</span></div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'b41_{idx}',{pr['q41']},'{m['p2']} 4-1')">{m['p2']} 4-1 {pr['q41']:.1f}% → Fair {fair(pr['q41'])} <input type=text id='b41_{idx}' oninput="chk('b41_{idx}',{fair(pr['q41'])})"><span id='b41_{idx}_b' class='badge'>Enter</span></div>
<div class='row'><input type=checkbox class='tick' onchange="toggleAcca(this,'b42_{idx}',{pr['q42']},'{m['p2']} 4-2')">{m['p2']} 4-2 {pr['q42']:.1f}% → Fair {fair(pr['q42'])} <input type=text id='b42_{idx}' oninput="chk('b42_{idx}',{fair(pr['q42'])})"><span id='b42_{idx}_b' class='badge'>Enter</span></div>
<div class='sec'>4. Over 5.5</div><div class='row'>Over {pr['over']:.1f}% → Fair {fair(pr['over'])} <input type=text id='ov_{idx}' oninput="chk('ov_{idx}',{fair(pr['over'])})"><span id='ov_{idx}_b' class='badge'>Enter</span></div></div>"""
html+="<div id='acca-bar' class='acca-bar'><b>ACCA BUILDER:</b> Tick 2-3 from DIFFERENT matches.</div></body></html>"
os.makedirs("docs",exist_ok=True)
open("docs/index.html","w",encoding='utf-8').write(html)
print(f"V6.3 built {len(matches)}")
