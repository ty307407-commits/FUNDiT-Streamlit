#!/bin/bash

# ========================================
# Streamlit App Data Update Script
# ========================================
# このスクリプトは以下を自動で実行します：
# 1. GCMC/QBCのリンク分析データを生成
# 2. 生成されたJSONをStreamlitリポジトリにコピー
# 3. GitHubにプッシュ（Streamlit Cloudが自動再デプロイ）

set -e  # エラーが発生したら停止

# 色付きログ
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "  Streamlit Data Update Script"
echo "========================================"
echo -e "${NC}"

# ベースディレクトリ
FUNDIT_DIR="/Users/rk/Library/CloudStorage/Dropbox/Fundit"
STREAMLIT_DIR="/Users/rk/Library/CloudStorage/Dropbox/Fundit-Streamlit"

# ========================================
# 1. GCMCデータ生成
# ========================================
echo -e "${YELLOW}[1/5] GCMC: リンク分析データを生成中...${NC}"
cd "$FUNDIT_DIR/GCMC"

if [ -f "generate_visualizer_with_ahrefs.py" ]; then
    python3 generate_visualizer_with_ahrefs.py
    echo -e "${GREEN}✓ GCMC データ生成完了${NC}"
else
    echo -e "${RED}✗ エラー: generate_visualizer_with_ahrefs.py が見つかりません${NC}"
    exit 1
fi

# ========================================
# 2. QBCデータ生成
# ========================================
echo -e "${YELLOW}[2/5] QBC: リンク分析データを生成中...${NC}"
cd "$FUNDIT_DIR/QBC"

if [ -f "generate_visualizer_with_ahrefs.py" ]; then
    python3 generate_visualizer_with_ahrefs.py
    echo -e "${GREEN}✓ QBC データ生成完了${NC}"
else
    echo -e "${RED}✗ エラー: generate_visualizer_with_ahrefs.py が見つかりません${NC}"
    exit 1
fi

# ========================================
# 3. JSONファイルをStreamlitリポジトリにコピー
# ========================================
echo -e "${YELLOW}[3/5] JSONファイルをコピー中...${NC}"

# GCMCのJSONをコピー
if [ -f "$FUNDIT_DIR/GCMC/gcmc_link_analysis_report.json" ]; then
    cp "$FUNDIT_DIR/GCMC/gcmc_link_analysis_report.json" "$STREAMLIT_DIR/GCMC/"
    echo -e "${GREEN}✓ GCMC JSON コピー完了${NC}"
else
    echo -e "${RED}✗ エラー: gcmc_link_analysis_report.json が見つかりません${NC}"
    exit 1
fi

# QBCのJSONをコピー
if [ -f "$FUNDIT_DIR/QBC/qbc_link_analysis_report.json" ]; then
    cp "$FUNDIT_DIR/QBC/qbc_link_analysis_report.json" "$STREAMLIT_DIR/QBC/"
    echo -e "${GREEN}✓ QBC JSON コピー完了${NC}"
else
    echo -e "${RED}✗ エラー: qbc_link_analysis_report.json が見つかりません${NC}"
    exit 1
fi

# ========================================
# 4. Gitにコミット
# ========================================
echo -e "${YELLOW}[4/5] Gitにコミット中...${NC}"
cd "$STREAMLIT_DIR"

# 変更があるか確認
if git diff --quiet GCMC/gcmc_link_analysis_report.json QBC/qbc_link_analysis_report.json; then
    echo -e "${YELLOW}! データに変更がありませんでした${NC}"
    echo -e "${BLUE}更新をスキップします${NC}"
    exit 0
fi

git add GCMC/gcmc_link_analysis_report.json QBC/qbc_link_analysis_report.json

# コミットメッセージに日時を含める
COMMIT_MSG="update: Link analysis data $(date '+%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MSG"

echo -e "${GREEN}✓ Gitコミット完了${NC}"

# ========================================
# 5. GitHubにプッシュ
# ========================================
echo -e "${YELLOW}[5/5] GitHubにプッシュ中...${NC}"

git push origin main

echo -e "${GREEN}✓ GitHubプッシュ完了${NC}"

# ========================================
# 完了
# ========================================
echo -e "${BLUE}"
echo "========================================"
echo "  ✓ 更新完了！"
echo "========================================"
echo -e "${NC}"
echo -e "${GREEN}Streamlit Cloud が自動的に再デプロイを開始します。${NC}"
echo -e "${BLUE}数分後に https://share.streamlit.io/ で確認できます。${NC}"
echo ""
