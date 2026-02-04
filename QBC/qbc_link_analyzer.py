#!/usr/bin/env python3
"""
QBC Link Analyzer
内部リンク構造と広告配置を分析し、収益化ページとフィーダーページを判別する
"""

import csv
import json
import time
import re
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import requests
from bs4 import BeautifulSoup


# 広告ドメインのパターン
AD_DOMAINS = [
    'googleads.g.doubleclick.net',
    'googlesyndication.com',
    'doubleclick.net',
    'amazon-adsystem.com',
    'a8.net',
    'valuecommerce.com',
    'accesstrade.net',
    'rentracks.jp',
    'affiliate-b.com',
    'felmat.net',
    'impact.com',
    'shareasale.com',
    'cj.com',
    'rakuten.co.jp/affiliate',
    'linksynergy.com',
    'afb.com',
    'track.affiliate-b.com',
    'allmedia-platform.com',
    'daicon-link.com',
]

# 広告URLパターン
AD_URL_PATTERNS = [
    r'/ad/',
    r'/ads/',
    r'/click/',
    r'/track/',
    r'/affiliate/',
    r'/aff/',
    r'\?utm_',
    r'redirect',
]


class QBCLinkAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.pages_data = []
        self.domain = 'qb-clinic.com'
        self.base_url = f'https://{self.domain}'
        
    def load_urls(self):
        """CSVからURLリストを読み込む"""
        urls = []
        with open(self.csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                urls.append({
                    'url': row['url'],
                    'h1': row['h1'],
                    'keyword': row['keyword'],
                    'rank': row['latest_rank']
                })
        return urls
    
    def is_internal_link(self, url):
        """内部リンクかどうかを判定"""
        parsed = urlparse(url)
        return self.domain in parsed.netloc or parsed.netloc == ''
    
    def is_ad_link(self, url, link_element):
        """広告リンクかどうかを判定"""
        # rel属性チェック
        rel = link_element.get('rel', [])
        if 'sponsored' in rel or 'nofollow' in rel:
            return True
        
        # ドメインチェック
        parsed = urlparse(url)
        for ad_domain in AD_DOMAINS:
            if ad_domain in parsed.netloc:
                return True
        
        # URLパターンチェック
        for pattern in AD_URL_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    def classify_ad_type(self, url):
        """広告の種類を分類"""
        parsed = urlparse(url)
        
        if 'google' in parsed.netloc or 'doubleclick' in parsed.netloc:
            return 'Google Ads'
        elif 'a8.net' in parsed.netloc:
            return 'A8.net'
        elif 'amazon' in parsed.netloc:
            return 'Amazon'
        elif 'rakuten' in parsed.netloc:
            return 'Rakuten'
        elif 'valuecommerce' in parsed.netloc:
            return 'ValueCommerce'
        elif 'accesstrade' in parsed.netloc:
            return 'AccessTrade'
        elif 'allmedia-platform' in parsed.netloc:
            return 'AllMedia Platform'
        elif 'daicon-link' in parsed.netloc:
            return 'Daicon Link'
        else:
            return 'Other'
    
    def extract_links(self, html, base_url):
        """HTMLから内部リンクと広告リンクを抽出"""
        soup = BeautifulSoup(html, 'html.parser')
        
        internal_links = set()
        ad_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(base_url, href)
            
            # フラグメント（#）を除去
            full_url = full_url.split('#')[0]
            
            if self.is_internal_link(full_url):
                # 内部リンク
                internal_links.add(full_url)
            elif self.is_ad_link(full_url, link):
                # 広告リンク
                ad_links.append({
                    'url': full_url,
                    'text': link.get_text(strip=True),
                    'type': self.classify_ad_type(full_url)
                })
        
        return list(internal_links), ad_links
    
    def fetch_page(self, url):
        """ページを取得"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def classify_page(self, ad_links, internal_links):
        """ページタイプを分類"""
        has_ads = len(ad_links) > 0
        has_internal = len(internal_links) > 0
        
        if has_ads and has_internal:
            return 'hybrid'
        elif has_ads:
            return 'monetization'
        else:
            return 'feeder'
    
    def analyze(self):
        """全URLを分析"""
        urls = self.load_urls()
        print(f"Analyzing {len(urls)} URLs...")
        
        for i, url_data in enumerate(urls, 1):
            url = url_data['url']
            print(f"[{i}/{len(urls)}] Analyzing: {url}")
            
            html = self.fetch_page(url)
            if html is None:
                # 取得失敗した場合もデータに含める
                self.pages_data.append({
                    'url': url,
                    'h1': url_data['h1'],
                    'keyword': url_data['keyword'],
                    'rank': url_data['rank'],
                    'type': 'error',
                    'internal_links': [],
                    'ad_links': [],
                    'inbound_count': 0
                })
                continue
            
            internal_links, ad_links = self.extract_links(html, url)
            page_type = self.classify_page(ad_links, internal_links)
            
            self.pages_data.append({
                'url': url,
                'h1': url_data['h1'],
                'keyword': url_data['keyword'],
                'rank': url_data['rank'],
                'type': page_type,
                'internal_links': internal_links,
                'ad_links': ad_links,
                'inbound_count': 0  # 後で計算
            })
            
            # サーバー負荷軽減のため1秒待機
            time.sleep(1)
        
        # 被リンク数を計算
        self.calculate_inbound_counts()
        
        return self.pages_data
    
    def calculate_inbound_counts(self):
        """各ページの被リンク数を計算"""
        url_to_index = {page['url']: i for i, page in enumerate(self.pages_data)}
        
        for page in self.pages_data:
            for link in page['internal_links']:
                if link in url_to_index:
                    self.pages_data[url_to_index[link]]['inbound_count'] += 1
    
    def generate_summary(self):
        """サマリー統計を生成"""
        total = len(self.pages_data)
        monetization = sum(1 for p in self.pages_data if p['type'] == 'monetization')
        feeder = sum(1 for p in self.pages_data if p['type'] == 'feeder')
        hybrid = sum(1 for p in self.pages_data if p['type'] == 'hybrid')
        error = sum(1 for p in self.pages_data if p['type'] == 'error')
        
        total_internal_links = sum(len(p['internal_links']) for p in self.pages_data)
        avg_internal_links = total_internal_links / total if total > 0 else 0
        
        total_ad_links = sum(len(p['ad_links']) for p in self.pages_data)
        
        # 広告タイプ別集計
        ad_types = defaultdict(int)
        for page in self.pages_data:
            for ad in page['ad_links']:
                ad_types[ad['type']] += 1
        
        return {
            'total_pages': total,
            'monetization_pages': monetization,
            'feeder_pages': feeder,
            'hybrid_pages': hybrid,
            'error_pages': error,
            'avg_internal_links': round(avg_internal_links, 2),
            'total_ad_links': total_ad_links,
            'ad_types': dict(ad_types)
        }
    
    def save_report(self, output_path):
        """分析結果をJSONで保存"""
        report = {
            'pages': self.pages_data,
            'summary': self.generate_summary()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\nReport saved to: {output_path}")
        print(f"\nSummary:")
        print(json.dumps(report['summary'], indent=2, ensure_ascii=False))


def main():
    csv_path = '/Users/rk/Library/CloudStorage/Dropbox/Fundit/qb_clinic_urls_with_h1_keywords.csv'
    output_path = '/Users/rk/Library/CloudStorage/Dropbox/Fundit/qbc_link_analysis_report.json'
    
    analyzer = QBCLinkAnalyzer(csv_path)
    analyzer.analyze()
    analyzer.save_report(output_path)


if __name__ == '__main__':
    main()
