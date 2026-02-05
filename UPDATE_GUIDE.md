# 📊 Streamlitアプリの更新方法

## 🚀 自動更新スクリプト

### 使い方

データを更新したい時に、以下のコマンドを実行するだけです：

```bash
cd /Users/rk/Library/CloudStorage/Dropbox/Fundit-Streamlit
./update_streamlit.sh
```

### 何が起こるか

スクリプトは以下を自動で実行します：

1. **GCMC データ生成**
   - `Fundit/GCMC/generate_visualizer_with_ahrefs.py` を実行
   - `gcmc_link_analysis_report.json` を生成

2. **QBC データ生成**
   - `Fundit/QBC/generate_visualizer_with_ahrefs.py` を実行
   - `qbc_link_analysis_report.json` を生成

3. **ファイルコピー**
   - 生成された JSON を `Fundit-Streamlit/` フォルダにコピー

4. **Git プッシュ**
   - 変更をコミット
   - GitHub にプッシュ

5. **自動デプロイ**
   - Streamlit Cloud が自動的に再デプロイを開始
   - 数分後に更新されたアプリが表示されます

### 実行タイミング

お好きなタイミングで実行してください：
- 週に1回
- 月に1回
- サイトに大きな変更があった時

### トラブルシューティング

#### エラーが出た場合

```bash
# エラーメッセージを確認
./update_streamlit.sh
```

エラーメッセージに従って対処してください。

#### 手動更新したい場合

スクリプトを使わずに手動で更新することもできます：

```bash
# 1. データ生成
cd /Users/rk/Library/CloudStorage/Dropbox/Fundit/GCMC
python3 generate_visualizer_with_ahrefs.py

cd /Users/rk/Library/CloudStorage/Dropbox/Fundit/QBC
python3 generate_visualizer_with_ahrefs.py

# 2. コピー
cp /Users/rk/Library/CloudStorage/Dropbox/Fundit/GCMC/gcmc_link_analysis_report.json \
   /Users/rk/Library/CloudStorage/Dropbox/Fundit-Streamlit/GCMC/

cp /Users/rk/Library/CloudStorage/Dropbox/Fundit/QBC/qbc_link_analysis_report.json \
   /Users/rk/Library/CloudStorage/Dropbox/Fundit-Streamlit/QBC/

# 3. Git プッシュ
cd /Users/rk/Library/CloudStorage/Dropbox/Fundit-Streamlit
git add GCMC/gcmc_link_analysis_report.json QBC/qbc_link_analysis_report.json
git commit -m "update: Manual data update"
git push origin main
```

## 📝 ファイル一覧

- `update_streamlit.sh` - 自動更新スクリプト
- `app.py` - Streamlit アプリケーション
- `requirements.txt` - Python 依存関係
- `GCMC/gcmc_link_analysis_report.json` - GCMC データ
- `QBC/qbc_link_analysis_report.json` - QBC データ

## 🔗 リンク

- **Streamlit Cloud**: https://share.streamlit.io/
- **GitHub リポジトリ**: https://github.com/ty307407-commits/FUNDiT-Streamlit

## 💡 ヒント

- データに変更がない場合、スクリプトは自動的にスキップします
- Git プッシュ後、Streamlit Cloud のダッシュボードで再デプロイの進行状況を確認できます
- 更新は数分で完了します
