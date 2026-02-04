import pandas as pd
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import time

# XMLサイトマップの内容（提供されたXML）
sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" data-google-analytics-opt-out="">
<!--  created with Free Online Sitemap Generator www.xml-sitemaps.com  -->
<url>
<loc>https://gcm.clinic/archives/gcmc-column</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>1.00</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/column</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/clinicfor-reputation</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/levcli-reputation</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/finasteride-effect</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/minoxidil-finasteride-can-be-used-together</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/minoxidil-side-effect</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/when-does-minoxidil-start-to-work</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/finasteride-dutasteride-difference</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/dutasteride-effect</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/dutasteride-side-effect</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/page/2</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/page/7</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5293</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5299</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5286</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5289</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5234</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5229</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5224</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5219</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/4984</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/column/page/2</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/column/page/3</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-covered-by-insurance</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-countermeasure</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-kawasaki</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-fukushima</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-akita</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-okinawa</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/people-with-high-levels-of-dihydrotestosterone</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-gifu</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/complete-recovery-from-aga-treatment</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/page/3</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/time-to-stop-aga-treatment</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/is-aga-treatment-ineffective</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/better-not-to-treat-aga</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-medicine</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-cost</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-recommend</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/page/6</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.64</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/category/cancer-immunotherapy</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/4986</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/4987</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/4994</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5000</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/4997</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5004</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/5007</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/1292</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/1280</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/1002</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/1212</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/962</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/920</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/862</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/812</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/784</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/finasteride-mailorder</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/dutasteride-mailorder</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/minoxidil-mailorder</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/what-is-aga</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-online</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-tachikawa</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-kagoshima</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-shinagawa</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-miyazaki</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-okayama</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-yamagata</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-shizuoka</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-takasaki</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/page/4</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/propecia-stop</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-period</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-fukuoka</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-nagoya</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-clinicfor</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-oosaka</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-tokyo</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/page/5</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.51</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/category/cancer-immunotherapy/page/2</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/category/cancer-immunotherapy/page/3</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-chiba</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-kobe</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/minoxidil-stop</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/finasteride-yabai</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-akihabara</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-ikebukuro</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-yokohama</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-dmm</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-clinicfor-reputation</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-sideeffect</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-hiroshima</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-sendai</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-sapporo</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-kyoto</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
<url>
<loc>https://gcm.clinic/archives/gcmc-column/aga-shinjuku</loc>
<lastmod>2026-02-02T04:18:45+00:00</lastmod>
<priority>0.41</priority>
</url>
</urlset>'''

print("=== ステップ1: XMLサイトマップからURL一覧を抽出 ===")
# XMLをパース
root = ET.fromstring(sitemap_xml)
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]
print(f"抽出したURL数: {len(urls)}")

# gcmc-columnパスのURLのみをフィルタリング（コンテンツページのみ）
content_urls = [url for url in urls if '/gcmc-column/' in url and '/page/' not in url]
print(f"コンテンツページURL数: {len(content_urls)}")

print("\n=== ステップ2: 各URLからページタイトルを取得 ===")
# ページタイトルを取得
url_data = []
for i, url in enumerate(content_urls, 1):
    try:
        print(f"[{i}/{len(content_urls)}] {url}")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # タイトルを取得（<title>タグまたは<h1>タグ）
        title = soup.find('title')
        title_text = title.text.strip() if title else ''
        
        # h1タグも取得してみる
        h1 = soup.find('h1')
        h1_text = h1.text.strip() if h1 else ''
        
        url_data.append({
            'url': url,
            'title': title_text if title_text else h1_text
        })
        
        # サーバーに負荷をかけないよう少し待機
        time.sleep(0.5)
    except Exception as e:
        print(f"  エラー: {e}")
        url_data.append({
            'url': url,
            'title': ''
        })

print(f"\nタイトル取得完了: {len(url_data)}件")

# DataFrameに変換
urls_df = pd.DataFrame(url_data)
print("\n取得したデータのサンプル:")
print(urls_df.head(10))

print("\n=== ステップ3: FMMデータからキーワードと最新順位を取得 ===")
# FMMデータを読み込み
fmm_file = '/Users/rk/Library/CloudStorage/Dropbox/Fundit/FMMデイリーモニタリング - GCMC_順位推移.csv'
fmm_df = pd.read_csv(fmm_file, skiprows=1, encoding='utf-8-sig')

# GCMCは203列なので、最後の列（01/29）を使用
# 列数を確認
total_columns = len(fmm_df.columns)
latest_rank_index = total_columns - 1  # 最後の列

print(f"総列数: {total_columns}")
print(f"最新順位の列インデックス: {latest_rank_index}")
print(f"最新順位の列名: {fmm_df.columns[latest_rank_index]}")

# キーワードとURLと最新順位を抽出
fmm_data = []
for idx, row in fmm_df.iterrows():
    if idx == 0:  # 平均順位の行をスキップ
        continue
    
    keyword = str(row['全KWD']).strip() if pd.notna(row['全KWD']) else ''
    url = str(row['記事URL']).strip() if pd.notna(row['記事URL']) else ''
    
    # 最新順位を取得（01/29列 = 最後の列）
    if latest_rank_index < len(fmm_df.columns):
        latest_rank = row.iloc[latest_rank_index]
    else:
        latest_rank = ''
    
    # 空行をスキップ
    if keyword and keyword != 'nan' and url and url != 'nan':
        fmm_data.append({
            'keyword': keyword,
            'url': url,
            'latest_rank': latest_rank if pd.notna(latest_rank) else ''
        })

print(f"\nFMMデータ: {len(fmm_data)}件のキーワード")

# URLをキーとした辞書を作成
url_to_keyword_rank = {}
for item in fmm_data:
    url_to_keyword_rank[item['url']] = {
        'keyword': item['keyword'],
        'latest_rank': item['latest_rank']
    }

print("\n=== ステップ4: マッチング ===")
# URLsデータにキーワードと順位を追加
urls_df['keyword'] = urls_df['url'].apply(
    lambda x: url_to_keyword_rank.get(x, {}).get('keyword', '')
)
urls_df['latest_rank'] = urls_df['url'].apply(
    lambda x: url_to_keyword_rank.get(x, {}).get('latest_rank', '')
)

# 結果を保存
output_file = '/Users/rk/Library/CloudStorage/Dropbox/Fundit/gcmc_urls_with_keywords.csv'
urls_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ 完了！")
print(f"出力ファイル: {output_file}")
print(f"\nマッチング結果:")
matched = len(urls_df[urls_df['keyword'] != ''])
print(f"- マッチしたURL: {matched}/{len(urls_df)}")
print(f"- マッチしなかったURL: {len(urls_df) - matched}/{len(urls_df)}")

# 結果のサンプルを表示
print("\n\n結果のサンプル（最初の10行）:")
print(urls_df[['url', 'title', 'keyword', 'latest_rank']].head(10).to_string(index=False))
