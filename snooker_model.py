# Snooker IQ V2 - Live Model
import os
from datetime import datetime

MATCHES = [
    {
        "match": "Stuart Bingham vs Anthony McGill",
        "format": "FT7 (English Open 2026)",
        "status": "LIVE 1-2",
        "markets": [
            {"score": "4-2", "true": 12.5, "bet365": 9.00},
            {"score": "4-3", "true": 14.7, "bet365": 7.50},
            {"score": "4-1", "true": 8.1,  "bet365": 12.00},
            {"score": "4-0", "true": 6.2,  "bet365": 15.00},
            {"score": "3-4", "true": 10.1, "bet365": 5.00},
        ]
    },
    {
        "match": "Mark Selby vs Kyren Wilson",
        "format": "FT7",
        "status": "19:30 BST",
        "markets": [
            {"score": "4-2", "true": 12.9, "bet365": 8.00},
            {"score": "4-3", "true": 13.4, "bet365": 7.00},
            {"score": "4-1", "true": 11.2, "bet365": 9.50},
            {"score": "4-0", "true": 7.1,  "bet365": 13.00},
            {"score": "2-4", "true": 11.4, "bet365": 4.80},
        ]
    }
]

def build_html():
    cards_html = ""
    for m in MATCHES:
        rows = ""
        for mk in m["markets"]:
            fair = 100 / mk["true"]
            edge = (mk["bet365"] / fair - 1) * 100
            edge_class = "edge-pos" if edge > 0 else "edge-neg"
            sign = "+" if edge > 0 else ""
            rows += f"<tr><td class='score'>{mk['score']}</td><td>{mk['true']}%</td><td class='fair'>{fair:.2f}</td><td class='bet'>{mk['bet365']:.2f}</td><td class='{edge_class}'>{sign}{edge:.1f}%</td></tr>"
        badge_class = "live" if "LIVE" in m["status"] else "ft"
        cards_html += f"<div class='card'><div class='match-head'><div><div class='match-title'>{m['match']}</div><div class='format'>{m['format']}</div></div><div class='badge {badge_class}'>{m['status']}</div></div><table><tr><th>Score</th><th>True%</th><th>Fair</th><th>Bet365</th><th>EDGE</th></tr>{rows}</table></div>"

    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width'><title>Snooker IQ V2</title><style>body{{background:#0a1a12;color:#e8ffe8;font-family:sans-serif;margin:0;padding:16px}}h1{{text-align:center}} .sub{{text-align:center;opacity:.7;font-size:13px;margin-bottom:18px}} .card{{background:#122a1e;border:1px solid #1f4a33;border-radius:16px;padding:14px;margin:14px auto;max-width:520px}} .match-head{{display:flex;justify-content:space-between}} .match-title{{font-weight:700}} .format{{font-size:11px;opacity:.6}} .badge{{font-size:10px;padding:3px 8px;border-radius:20px;font-weight:700}} .live{{background:#ff3b30;color:#fff}} .ft{{background:#1a4d2e;color:#8cffb0}} table{{width:100%;border-collapse:collapse;font-size:13px}} th{{opacity:.6;text-align:left;padding:6px;border-bottom:1px solid #204a32;font-size:11px}} td{{padding:8px;border-bottom:1px solid #152d20}} .score{{font-weight:700}} .edge-pos{{color:#00ff88;font-weight:800}} .edge-neg{{color:#ff6b6b}} .bet{{color:#ffcc00;font-weight:700}}</style></head><body><h1>🎱 Snooker IQ V2</h1><div class='sub'>Live English Open 2026 • {datetime.now().strftime('%d %b %H:%M')}</div>{cards_html}<div style='text-align:center;opacity:.5;font-size:11px;margin-top:24px'>niibaboo.github.io/Snooker/ • No DEMO</div></body></html>"
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html","w", encoding="utf-8") as f: f.write(html)
    print("✅ Built docs/index.html")

if __name__ == "__main__":
    build_html()
