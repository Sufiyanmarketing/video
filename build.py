"""Build index.html from template.html + a WebinarFuel chat export (CSV).

Usage: python3 build.py [chat.csv]
"""
import csv, json, sys

src = sys.argv[1] if len(sys.argv) > 1 else "chat.csv"
rows = list(csv.reader(open(src, encoding="utf-8")))
start = next(i for i, r in enumerate(rows) if r and r[0] == "First Name") + 1

chat = []
for r in rows[start:]:
    if len(r) < 5 or not r[4].strip():
        continue
    h, m, s = (int(x) for x in r[3].split(":"))
    name = f"{r[0].strip()} {r[1].strip()}".strip() or "Gjest"
    chat.append({"t": h * 3600 + m * 60 + s, "n": name, "m": r[4].strip()})
chat.sort(key=lambda c: c["t"])

data = json.dumps(chat, ensure_ascii=False).replace("</", "<\\/")
html = open("template.html", encoding="utf-8").read().replace("__CHAT__", data)
open("index.html", "w", encoding="utf-8").write(html)
print(f"index.html written with {len(chat)} chat messages")
