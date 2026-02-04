import csv, time, re
import requests

IN_CSV  = "qb_clinic_urls_with_title_placeholder.csv"
OUT_CSV = "qb_clinic_urls_with_titles.csv"

def extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>\s*(.*?)\s*</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

rows = []
with open(IN_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        url = row["url"]
        title = ""
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding or r.encoding
            title = extract_title(r.text)
        except Exception:
            title = ""
        rows.append({"url": url, "title": title})
        time.sleep(0.2)

with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["url", "title"])
    w.writeheader()
    w.writerows(rows)

print("done:", OUT_CSV, "rows:", len(rows))
