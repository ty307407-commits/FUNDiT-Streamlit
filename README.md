<<<<<<< HEAD
# FUNDiT - SEO Link Visualizer

GCMCとQBCドメインの内部リンク構造を可視化し、Ahrefsのキーワードデータと統合するStreamlitアプリです。

## 🌐 デモ

**Streamlit Cloud（誰でも使える）:**
```
https://fundit-visualizer.streamlit.app
```
*上記URLをブラウザで開くだけで使用できます！*

## ✨ 主な機能

### 📊 インタラクティブ分析
- ページタイプの自動分類（収益化/フィーダー/ハイブリッド）
- リンク構造のネットワークグラフ
- リアルタイムフィルタリングと検索

### 🎨 可視化
- Plotlyによる美しいグラフ
- ドラッグ&ドロップでノード移動
- ズーム/パン操作

### 🔍 Ahrefs統合
- CSVファイルアップロード
- 上位20位以内のキーワード表示
- 検索ボリュームと順位の可視化

## 🚀 使い方

### オプション1: Streamlit Cloud（推奨・超簡単）

1. **URLを開く**: https://fundit-visualizer.streamlit.app
2. **ドメイン選択**: サイドバーでGCMCまたはQBCを選択
3. **Ahrefsアップロード**: CSVファイルをドラッグ&ドロップ
4. **分析**: ページをクリックして詳細を確認

### オプション2: ローカルで実行

```bash
# リポジトリをクローン
git clone https://github.com/ty307407-commits/FUNDiT.git
cd FUNDiT

# 依存関係をインストール
pip install -r requirements.txt

# アプリを起動
streamlit run app.py
```

## 📋 データ準備

### 1. リンク分析データの生成

#### GCMC:
```bash
cd GCMC
python3 gcmc_link_analyzer.py
```

#### QBC:
```bash
cd QBC
python3 qbc_link_analyzer.py
```

### 2. Ahrefsデータのエクスポート

1. Ahrefsでドメインを検索
2. "Organic keywords"セクションへ
3. CSVでエクスポート（必須カラム: Keyword, Current URL, Current position, Volume）

## 📊 必要なファイル

### リンク分析用CSV

**GCMC:** `GCMC/gcmc_urls_with_keywords.csv`
```csv
URL,Title,Keyword,Rank
https://gcm.clinic/archives/gcmc-column/example,Example Title,example keyword,1
```

**QBC:** `QBC/qb_clinic_urls_with_h1_keywords.csv`
```csv
URL,H1,Keyword,Rank
https://qb-clinic.com/qbc-column/example,Example H1,example keyword,1
```

### Ahrefs CSV

必須カラム:
- `Keyword`: キーワード
- `Current URL`: ページURL
- `Current position`: 現在の順位
- `Volume`: 検索ボリューム

## 🎨 ページタイプの判定基準

- **収益化ページ**: 3個以上の広告リンク
- **フィーダーページ**: 0〜2個の広告リンク
- **ハイブリッド**: 3個以上の広告リンク + 5個以上の内部リンク

## 🔧 技術スタック

- **フレームワーク**: Streamlit
- **可視化**: Plotly, NetworkX
- **データ処理**: Pandas
- **分析**: BeautifulSoup4, Requests
=======
# AthReebo - WordPress用LLM記事生成テンプレート

LLMで生成したMarkdownをそのままWordPressにコピペして、美しいブログ記事を作成できるテンプレートシステムです。
>>>>>>> 5f448ea0e3e5d6a7893fe406fef5672e69ccf74b

## 📁 プロジェクト構成

```
<<<<<<< HEAD
FUNDiT/
├── app.py                       # Streamlitメインアプリ
├── requirements.txt             # Python依存関係
├── .streamlit/
│   └── config.toml             # Streamlit設定
├── GCMC/
│   ├── gcmc_link_analyzer.py
│   ├── generate_visualizer_with_ahrefs.py
│   ├── gcmc_link_analysis_report.json
│   └── README.md
├── QBC/
│   ├── qbc_link_analyzer.py
│   ├── generate_visualizer_with_ahrefs.py
│   ├── qbc_link_analysis_report.json
│   └── README.md
└── README.md                    # このファイル
```

## 🚢 Streamlit Cloudへのデプロイ

1. **GitHubにプッシュ**:
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

2. **Streamlit Cloudでデプロイ**:
   - https://share.streamlit.io/ にアクセス
   - "New app"をクリック
   - リポジトリを選択: `ty307407-commits/FUNDiT`
   - メインファイル: `app.py`
   - デプロイ！

## 💡 使用例

### ケース1: 内部リンク構造の分析
1. ネットワークグラフで孤立ページを発見
2. フィーダーページから収益化ページへの導線を確認

### ケース2: キーワード戦略の最適化
1. Ahrefsデータをアップロード
2. 11-20位のキーワードを持つページを特定
3. 内部リンクを強化してランキング向上

### ケース3: 広告配置の最適化
1. ハイブリッドページを特定
2. コンテンツと広告のバランスを確認

## 🔒 セキュリティとプライバシー

- データはブラウザ内で処理されます
- アップロードされたファイルはセッション終了時に削除されます
- GitHubには分析ツールのみをコミット（データは含まない）

## 📝 ライセンス

このツールは内部使用を目的としています。

## 🤝 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いてください。

## 📞 サポート

問題や質問があれば、GitHubのIssuesセクションで報告してください。

---

Made with ❤️ for SEO analysis | [GitHub](https://github.com/ty307407-commits/FUNDiT)
=======
AthReebo/
├── css/
│   └── article-style.css    # WordPressに追加するCSS
├── templates/
│   └── sample-article.md    # 記事サンプル（参考用）
└── README.md                # このファイル
```

## 🚀 使い方

### 1. CSSをWordPressに追加

`css/article-style.css` の内容を以下のいずれかに追加：

- **テーマカスタマイザー** → 追加CSS
- **子テーマ** → style.css
- **プラグイン** → Custom CSS プラグイン

### 2. LLMに記事を生成させる

以下のプロンプトをLLM（ChatGPT、Claude等）に渡して記事を生成：

```
以下のテンプレート構造に従って、「[トピック]」についての記事を書いてください。

【記事構造】
- カテゴリバッジ
- タイトル（h1）
- 著者バイライン
- アイキャッチ画像
- 導入文
- 目次
- 本文（h2, h3で構成）
- Q&Aセクション
- まとめ
- CTAボタン
- 監修者ボックス
- 関連記事

【使用可能なHTMLクラス】
（下記「コンポーネント一覧」を参照）

出力は<div class="article-content">で囲んでください。
```

### 3. WordPressに貼り付け

生成されたMarkdown/HTMLを、WordPressの**カスタムHTML**ブロックまたは**クラシックエディタ（HTML表示）**に貼り付け。

---

## 🎨 コンポーネント一覧

### カテゴリバッジ
```html
<span class="category-badge">カテゴリ名</span>
```

### 著者バイライン（記事上部）
```html
<div class="author-byline">
  <img src="著者画像URL" alt="著者">
  <div class="info">
    <p class="name">著者名（肩書き）</p>
    <p class="title">専門分野・資格</p>
  </div>
  <span class="date">2024年1月15日更新</span>
</div>
```

### 目次
```html
<div class="toc">
  <p class="toc-title">この記事の目次</p>
  <ol>
    <li><a href="#section1">セクション1</a></li>
    <li><a href="#section2">セクション2</a></li>
  </ol>
</div>
```

### Q&Aセクション
```html
<div class="qa-section">
  <div class="qa-item">
    <div class="question">質問テキスト</div>
    <div class="answer">
      <div class="answer-content">
        <p>回答テキスト</p>
      </div>
    </div>
  </div>
</div>
```

### ポイントボックス（5色）
```html
<!-- green / blue / yellow / pink / gray が使用可能 -->
<div class="point-box green">
  <p class="point-box-title">💡 タイトル</p>
  <p>内容テキスト</p>
</div>
```

### 警告ボックス
```html
<div class="warning-box">
  <p class="warning-box-title">注意タイトル</p>
  <p>警告内容</p>
</div>
```

### 危険ボックス
```html
<div class="danger-box">
  <p class="danger-box-title">危険タイトル</p>
  <p>危険内容</p>
</div>
```

### ステップ（手順）
```html
<div class="steps">
  <div class="step">
    <span class="step-number">1</span>
    <div class="step-content">
      <p class="step-title">ステップタイトル</p>
      <p class="step-desc">説明文</p>
    </div>
  </div>
</div>
```

### 専門家コメント（ボックススタイル）
```html
<!-- doctor / supervisor / (なし=デフォルト) が使用可能 -->
<div class="expert-comment doctor">
  <div class="expert-avatar">
    <img src="専門家画像URL" alt="専門家名">
  </div>
  <div class="expert-body">
    <p class="expert-name">専門家名（所属・肩書き）</p>
    <p class="expert-title">資格・専門分野</p>
    <div class="expert-text">
      <p>コメント内容をここに記載します。</p>
      <p>複数段落も可能です。</p>
    </div>
  </div>
</div>
```

### 専門家コメント（吹き出しスタイル）
```html
<!-- green / blue / pink / (なし=白) が使用可能 -->
<div class="expert-balloon green">
  <div class="balloon-avatar">
    <img src="専門家画像URL" alt="専門家名">
    <span class="balloon-name">専門家名</span>
  </div>
  <div class="balloon-content">
    <p>吹き出し形式のコメントです。会話調のコメントに適しています。</p>
  </div>
</div>
```

### CTAボタン
```html
<div class="cta-container">
  <a href="#" class="cta-button">ボタンテキスト</a>
</div>

<!-- 紫色バリエーション -->
<a href="#" class="cta-button secondary">ボタンテキスト</a>
```

### 監修者ボックス（記事下部）
```html
<div class="author-box">
  <span class="author-box-label">この記事の監修者</span>
  <div class="author-box-header">
    <img src="監修者画像URL" alt="監修者">
    <div class="author-info">
      <p class="author-name">監修者名</p>
      <p class="author-title">肩書き</p>
      <div class="author-credentials">
        <span class="credential">資格1</span>
        <span class="credential">資格2</span>
      </div>
    </div>
  </div>
  <p class="author-bio">経歴・プロフィール文</p>
</div>
```

### 関連記事
```html
<div class="related-articles">
  <p class="related-title">関連記事</p>
  <div class="related-grid">
    <a href="#" class="related-card">
      <img src="サムネイルURL" alt="関連記事">
      <div class="related-card-body">
        <p class="related-card-title">記事タイトル</p>
        <p class="related-card-desc">記事の説明文</p>
      </div>
    </a>
  </div>
</div>
```

### テーブル
```html
<table>
  <tr>
    <th>見出し1</th>
    <th>見出し2</th>
  </tr>
  <tr>
    <td>データ1</td>
    <td>データ2</td>
  </tr>
</table>
```

---

## 📝 LLM向けプロンプト例

### 基本プロンプト

```
あなたはWordPress用のブログ記事を生成するライターです。
以下の構造とHTMLクラスを使用して、「[トピック]」についての記事を生成してください。

【必須構造】
1. <div class="article-content">で全体を囲む
2. <span class="category-badge">でカテゴリ表示
3. <h1>でタイトル
4. <div class="author-byline">で著者情報
5. <div class="toc">で目次
6. <h2 id="section1">などでセクション見出し
7. 適宜ポイントボックスや警告ボックスを使用
8. <div class="qa-section">でQ&A
9. <div class="author-box">で監修者情報
10. <div class="related-articles">で関連記事

【画像について】
画像URLはプレースホルダー（https://placehold.co/幅x高さ/背景色/文字色?text=説明）を使用。
後で実際の画像に差し替え可能。

【トーン】
- 専門的だが読みやすい
- 具体例を交える
- SEOを意識した構成
```

### 医療・健康系プロンプト追加

```
【追加要件】
- 必ず「監修者」情報を含める
- 医学的に正確な情報を記載
- 「個人差があります」「医師に相談してください」などの注意喚起を含める
- 危険な行為には<div class="danger-box">を使用
```

---

## 🎨 カラーカスタマイズ

CSSの以下の値を変更してブランドカラーを調整：

```css
/* メインカラー（緑）を変更する場合 */
#2eb67d → お好みの色に変更

/* 例：青に変更 */
#2eb67d → #2196f3
```

---

## 📱 レスポンシブ対応

CSSには768px以下のモバイル対応スタイルが含まれています。追加の調整が必要な場合は、メディアクエリを編集してください。

---

## ライセンス

MIT License - 自由にご利用ください。
>>>>>>> 5f448ea0e3e5d6a7893fe406fef5672e69ccf74b
