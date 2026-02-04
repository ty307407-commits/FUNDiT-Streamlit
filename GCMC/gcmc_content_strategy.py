import pandas as pd
import numpy as np

print("=== GCMC コンテンツ最適化戦略分析 ===\n")

# 1. ahrefsデータを読み込み（UTF-16LE エンコーディング）
print("ステップ1: ahrefsデータを読み込み")
ahrefs_file = '/Users/rk/Library/CloudStorage/Dropbox/Fundit/gcm.clinic-archives-gcmc-column-organic-keyw_2026-02-02_13-25-59.csv'
ahrefs_df = pd.read_csv(ahrefs_file, encoding='utf-16le', sep='\t')

print(f"ahrefsデータ: {len(ahrefs_df)}件のキーワード")
print(f"列: {list(ahrefs_df.columns)[:10]}")

# 2. FMMデータを読み込み
print("\nステップ2: FMMデータを読み込み")
fmm_file = '/Users/rk/Library/CloudStorage/Dropbox/Fundit/FMMデイリーモニタリング - GCMC_順位推移.csv'
fmm_df = pd.read_csv(fmm_file, skiprows=1, encoding='utf-8-sig')

# 最新順位の列インデックス
latest_rank_index = len(fmm_df.columns) - 1

# FMMデータを整理
fmm_data = []
for idx, row in fmm_df.iterrows():
    if idx == 0:  # 平均順位の行をスキップ
        continue
    
    keyword = str(row['全KWD']).strip() if pd.notna(row['全KWD']) else ''
    url = str(row['記事URL']).strip() if pd.notna(row['記事URL']) else ''
    latest_rank = row.iloc[latest_rank_index] if pd.notna(row.iloc[latest_rank_index]) else 21
    
    if keyword and keyword != 'nan' and url and url != 'nan':
        fmm_data.append({
            'keyword': keyword,
            'url': url,
            'fmm_rank': latest_rank
        })

fmm_keywords_df = pd.DataFrame(fmm_data)
print(f"FMMデータ: {len(fmm_keywords_df)}件のキーワード")

# 3. ahrefsデータをクリーニング
print("\nステップ3: ahrefsデータをクリーニング")
# 必要な列のみ抽出
ahrefs_clean = ahrefs_df[[
    'Keyword', 'Volume', 'Current position', 
    'Organic traffic', 'Current URL'
]].copy()

# データ型を変換
ahrefs_clean['Volume'] = pd.to_numeric(ahrefs_clean['Volume'], errors='coerce').fillna(0)
ahrefs_clean['Current position'] = pd.to_numeric(ahrefs_clean['Current position'], errors='coerce').fillna(100)
ahrefs_clean['Organic traffic'] = pd.to_numeric(ahrefs_clean['Organic traffic'], errors='coerce').fillna(0)

# gcmc-columnのURLのみをフィルタリング
ahrefs_clean = ahrefs_clean[ahrefs_clean['Current URL'].str.contains('gcmc-column', na=False)]

print(f"gcmc-columnのキーワード: {len(ahrefs_clean)}件")

# 4. リライト候補を抽出
print("\n" + "="*60)
print("【分析1】リライト推奨ページ")
print("="*60)

# リライト候補の条件：
# 1. 現在ページが存在する
# 2. 順位が2位以下（改善の余地あり）
# 3. 検索ボリュームまたはトラフィックが一定以上

rewrite_candidates = ahrefs_clean[
    (ahrefs_clean['Current position'] > 1) &  # 1位以外
    (ahrefs_clean['Current position'] <= 20) &  # 20位以内
    ((ahrefs_clean['Volume'] >= 100) | (ahrefs_clean['Organic traffic'] >= 10))  # ボリュームまたはトラフィックあり
].copy()

# スコアリング：検索ボリューム × (21 - 現在順位) / 20
rewrite_candidates['potential_score'] = (
    rewrite_candidates['Volume'] * 
    (21 - rewrite_candidates['Current position']) / 20
)

# 順位改善によるトラフィック増加見込み
rewrite_candidates['traffic_potential'] = np.where(
    rewrite_candidates['Current position'] <= 3,
    rewrite_candidates['Volume'] * 0.1,  # 1-3位→1位で10%増加見込み
    np.where(
        rewrite_candidates['Current position'] <= 10,
        rewrite_candidates['Volume'] * 0.3,  # 4-10位→上位で30%増加見込み
        rewrite_candidates['Volume'] * 0.5   # 11-20位→上位で50%増加見込み
    )
)

# スコアでソート
rewrite_candidates = rewrite_candidates.sort_values('potential_score', ascending=False)

print(f"\nリライト候補: {len(rewrite_candidates)}件\n")
print("上位20件:")
print(rewrite_candidates[[
    'Keyword', 'Volume', 'Current position', 
    'Organic traffic', 'traffic_potential', 'Current URL'
]].head(20).to_string(index=False))

# 5. 新規作成候補を抽出
print("\n" + "="*60)
print("【分析2】新規ページ作成推奨キーワード")
print("="*60)

# 新規作成候補の条件：
# 1. ahrefsには出てくるが、FMMで追跡されていない（=新しいキーワード）
# 2. 検索ボリュームが一定以上
# 3. 現在の順位が圏外または低い

# FMMに存在するキーワードのリスト
fmm_keywords_list = fmm_keywords_df['keyword'].str.lower().tolist()

# ahrefsキーワードを小文字に変換
ahrefs_clean['keyword_lower'] = ahrefs_clean['Keyword'].str.lower()

# FMMにないキーワードを抽出
new_keywords = ahrefs_clean[
    ~ahrefs_clean['keyword_lower'].isin(fmm_keywords_list)
].copy()

# 新規作成候補の絞り込み
new_page_candidates = new_keywords[
    (new_keywords['Volume'] >= 100) &  # 検索ボリューム100以上
    (new_keywords['Current position'] > 10)  # 現在10位以下または圏外
].copy()

# スコアリング：検索ボリューム重視
new_page_candidates['creation_score'] = new_page_candidates['Volume']

# ソート
new_page_candidates = new_page_candidates.sort_values('creation_score', ascending=False)

print(f"\n新規ページ作成候補: {len(new_page_candidates)}件\n")
print("上位20件:")
print(new_page_candidates[[
    'Keyword', 'Volume', 'Current position', 'Organic traffic'
]].head(20).to_string(index=False))

# 6. FMMで順位が下がっているページを抽出
print("\n" + "="*60)
print("【分析3】順位下降中のページ（緊急対応推奨）")
print("="*60)

# FMMデータから順位変動を分析（簡易版：最新と少し前を比較）
# 最新から10列前の順位と比較
if len(fmm_df.columns) >= 12:
    comparison_index = latest_rank_index - 10
    
    declining_pages = []
    for idx, row in fmm_df.iterrows():
        if idx == 0:
            continue
        
        keyword = str(row['全KWD']).strip() if pd.notna(row['全KWD']) else ''
        url = str(row['記事URL']).strip() if pd.notna(row['記事URL']) else ''
        
        if not keyword or keyword == 'nan' or not url or url == 'nan':
            continue
        
        latest = row.iloc[latest_rank_index] if pd.notna(row.iloc[latest_rank_index]) else 21
        previous = row.iloc[comparison_index] if pd.notna(row.iloc[comparison_index]) else 21
        
        # 順位が下がっている（数値が大きくなっている）
        if latest > previous and latest != 21 and previous != 21:
            rank_drop = latest - previous
            
            # ahrefsから検索ボリュームを取得
            ahrefs_match = ahrefs_clean[
                ahrefs_clean['keyword_lower'] == keyword.lower()
            ]
            
            volume = ahrefs_match['Volume'].values[0] if len(ahrefs_match) > 0 else 0
            
            declining_pages.append({
                'keyword': keyword,
                'url': url,
                'previous_rank': previous,
                'current_rank': latest,
                'rank_drop': rank_drop,
                'volume': volume
            })
    
    if declining_pages:
        declining_df = pd.DataFrame(declining_pages)
        declining_df = declining_df.sort_values('rank_drop', ascending=False)
        
        print(f"\n順位下降中: {len(declining_df)}件\n")
        print("上位15件:")
        print(declining_df.head(15).to_string(index=False))
    else:
        print("\n順位下降中のページはありません")

# 7. 結果をCSVに保存
print("\n" + "="*60)
print("結果を保存中...")
print("="*60)

# リライト候補を保存
rewrite_output = rewrite_candidates[[
    'Keyword', 'Volume', 'Current position', 
    'Organic traffic', 'traffic_potential', 'potential_score', 'Current URL'
]].copy()
rewrite_output.columns = [
    'キーワード', '検索ボリューム', '現在順位', 
    'オーガニックトラフィック', 'トラフィック増加見込み', '優先度スコア', 'URL'
]
rewrite_output.to_csv(
    '/Users/rk/Library/CloudStorage/Dropbox/Fundit/gcmc_rewrite_candidates.csv',
    index=False,
    encoding='utf-8-sig'
)

# 新規作成候補を保存
new_page_output = new_page_candidates[[
    'Keyword', 'Volume', 'Current position', 'Organic traffic', 'creation_score'
]].copy()
new_page_output.columns = [
    'キーワード', '検索ボリューム', '現在順位', 'オーガニックトラフィック', '優先度スコア'
]
new_page_output.to_csv(
    '/Users/rk/Library/CloudStorage/Dropbox/Fundit/gcmc_new_page_candidates.csv',
    index=False,
    encoding='utf-8-sig'
)

# 順位下降ページを保存
if declining_pages:
    declining_df.to_csv(
        '/Users/rk/Library/CloudStorage/Dropbox/Fundit/gcmc_declining_pages.csv',
        index=False,
        encoding='utf-8-sig'
    )

print("\n✅ 完了！")
print("\n作成したファイル:")
print("1. gcmc_rewrite_candidates.csv - リライト推奨ページ")
print("2. gcmc_new_page_candidates.csv - 新規作成推奨キーワード")
if declining_pages:
    print("3. gcmc_declining_pages.csv - 順位下降中のページ")

print("\n" + "="*60)
print("分析完了")
print("="*60)
