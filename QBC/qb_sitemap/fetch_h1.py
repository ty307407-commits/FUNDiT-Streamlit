import csv, time
import requests
from bs4 import BeautifulSoup

IN_CSV  = "qb_clinic_urls_with_title_placeholder.csv"  # url,title の形なら何でもOK
OUT_CSV = "qb_clinic_urls_with_h1.csv"

def extract_first_h1(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.find("h1")
    if not h1:
        return ""
    # 見出し内の余計な改行・スペースを整形
    return " ".join(h1.get_text(" ", strip=True).split())

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

rows = []
with open(IN_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        url = row["url"]
        h1_text = ""
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding or r.encoding
            h1_text = extract_first_h1(r.text)
        except Exception:
            h1_text = ""

        rows.append({"url": url, "h1": h1_text})
        time.sleep(0.2)  # 負荷軽減（必要なら0.5〜1.0に）

with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["url", "h1"])
    w.writeheader()
    w.writerows(rows)

print("done:", OUT_CSV, "rows:", len(rows))
