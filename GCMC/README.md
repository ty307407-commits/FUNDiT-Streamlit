# GCMC Link Visualizer with Ahrefs Integration

GCMCドメインの内部リンク構造と広告配置を可視化し、Ahrefsのキーワードデータと統合するツールです。

## 🌟 機能

- **内部リンク構造の可視化**: D3.jsでインタラクティブなネットワークグラフを表示
- **ページタイプ分類**: 収益化ページ、フィーダーページ、ハイブリッドを自動判定
- **広告リンク分析**: 各ページの広告配置を確認
- **Ahrefsデータ統合**: CSVファイルをアップロードして上位20位以内のキーワードを表示

## 📋 使用方法

### 1. データ分析

```bash
python3 gcmc_link_analyzer.py
```

このスクリプトは`gcmc_urls_with_keywords.csv`を読み込み、`gcmc_link_analysis_report.json`を生成します。

### 2. ビジュアライザー生成

```bash
python3 generate_visualizer_with_ahrefs.py
```

スタンドアロンHTML（`gcmc_link_visualizer_with_ahrefs.html`）が生成されます。

### 3. ブラウザで開く

生成された`gcmc_link_visualizer_with_ahrefs.html`をダブルクリック、またはブラウザにドラッグ＆ドロップします。

### 4. Ahrefsデータをアップロード（オプション）

1. ビジュアライザーを開く
2. 「📊 Ahrefsデータをアップロード」ボタンをクリック
3. Ahrefs からエクスポートしたCSVファイルを選択
4. ノードをクリックすると、上位20位以内のキーワードが表示されます

## 📊 必要なCSVフォーマット

### 入力データ (gcmc_urls_with_keywords.csv)

```csv
URL,Title,Keyword,Rank
https://gcm.clinic/archives/gcmc-column/example,Example Title,example keyword,1
```

### Ahrefs CSVフォーマット

以下のカラムが必要です：
- `Keyword`: キーワード
- `Current URL`: ページURL
- `Current position`: 現在の順位
- `Volume`: 検索ボリューム

## 🎨 ページタイプの判定基準

- **収益化ページ**: 3個以上の広告リンクを含む
- **フィーダーページ**: 広告リンクなし、または1〜2個
- **ハイブリッド**: 3個以上の広告リンク + 5個以上の内部リンク

## 🔧 依存関係

- Python 3.x
- `requests`
- `beautifulsoup4`
- ブラウザ（Chrome, Firefox, Safari等）

インストール:
```bash
pip install requests beautifulsoup4
```

## 📁 ファイル構成

```
GCMC/
├── gcmc_link_analyzer.py              # リンク分析スクリプト
├── generate_visualizer_with_ahrefs.py # HTML生成スクリプト
├── gcmc_urls_with_keywords.csv        # 入力データ
├── gcmc_link_analysis_report.json     # 分析結果
└── gcmc_link_visualizer_with_ahrefs.html  # 最終成果物（スタンドアロン）
```

## 💡 使用例

1. サイトのSEO分析
2. 内部リンク構造の最適化
3. 収益化ページへの導線確認
4. キーワードランキングの可視化

## 📝 ライセンス

このツールは内部使用を目的としています。

## 🤝 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。
