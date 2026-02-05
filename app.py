"""
GCMC/QBC Link Visualizer with Ahrefs Integration
Streamlit App
"""
import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="Link Visualizer - GCMC/QBC",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .keyword-badge {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .rank-1-10 {
        background: #e8f5e9;
        color: #2e7d32;
        border: 2px solid #4caf50;
    }
    .rank-11-20 {
        background: #fff3e0;
        color: #e65100;
        border: 2px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<h1 class="main-title">🔗 Link Visualizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">GCMC & QBC 内部リンク構造 + Ahrefsデータ統合</p>', unsafe_allow_html=True)

# サイドバー
st.sidebar.header("⚙️ 設定")

# ドメイン選択
domain = st.sidebar.radio(
    "ドメインを選択",
    ["GCMC", "QBC"],
    help="分析するドメインを選択してください"
)

# データ読み込み
@st.cache_data
def load_data(domain):
    """JSONデータを読み込む"""
    # 絶対パスを使用（Streamlit Cloud対応）
    import os
    base_dir = Path(__file__).parent
    
    file_map = {
        "GCMC": base_dir / "GCMC" / "gcmc_link_analysis_report.json",
        "QBC": base_dir / "QBC" / "qbc_link_analysis_report.json"
    }
    
    file_path = file_map[domain]
    if not file_path.exists():
        st.error(f"❌ データファイルが見つかりません: {file_path}")
        st.info(f"📁 現在のディレクトリ: {os.getcwd()}")
        st.info(f"📂 探しているパス: {file_path}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data(domain)

if data is None:
    st.stop()

# Ahrefsファイルアップロード
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Ahrefsデータ")
uploaded_file = st.sidebar.file_uploader(
    "CSVファイルをアップロード",
    type=['csv'],
    help="Ahrefsからエクスポートしたキーワードデータ"
)

# Ahrefsデータ解析
ahrefs_data = {}
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = ['Keyword', 'Current URL', 'Current position', 'Volume']
        
        if all(col in df.columns for col in required_cols):
            # 20位以内のみフィルター
            df_filtered = df[df['Current position'] <= 20].copy()
            
            # URLごとにグループ化
            for url, group in df_filtered.groupby('Current URL'):
                ahrefs_data[url] = group.sort_values('Volume', ascending=False)[
                    ['Keyword', 'Current position', 'Volume']
                ].to_dict('records')
            
            st.sidebar.success(f"✅ {len(ahrefs_data)} ページのデータを読み込みました")
        else:
            st.sidebar.error("❌ 必要なカラムが見つかりません")
    except Exception as e:
        st.sidebar.error(f"❌ エラー: {str(e)}")

# フィルター
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 フィルター")

page_type_filter = st.sidebar.multiselect(
    "ページタイプ",
    ["monetization", "feeder", "hybrid"],
    default=["monetization", "feeder", "hybrid"],
    format_func=lambda x: {"monetization": "収益化", "feeder": "フィーダー", "hybrid": "ハイブリッド"}[x]
)

# 検索
search_query = st.sidebar.text_input("🔎 キーワード検索", placeholder="URLやタイトルで検索...")

# データフィルタリング
filtered_pages = [
    p for p in data['pages']
    if p['type'] in page_type_filter
    and (not search_query or 
         search_query.lower() in p['url'].lower() or
         search_query.lower() in p.get('title', p.get('h1', '')).lower())
]

# 統計情報
st.header("📊 サマリー統計")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("総ページ数", data['summary']['total_pages'])
with col2:
    st.metric("収益化ページ", data['summary']['monetization_pages'])
with col3:
    st.metric("フィーダーページ", data['summary']['feeder_pages'])
with col4:
    st.metric("総広告リンク数", data['summary']['total_ad_links'])

# ネットワークグラフ
st.header("🕸️ リンク構造の可視化")

if len(filtered_pages) == 0:
    st.warning("⚠️ 表示するページがありません。フィルターを調整してください。")
else:
    # NetworkXグラフ作成
    G = nx.DiGraph()
    
    # ノード追加
    for page in filtered_pages:
        G.add_node(
            page['url'],
            title=page.get('title', page.get('h1', page['url'])),
            type=page['type'],
            inbound_count=page['inbound_count']
        )
    
    # エッジ追加
    url_set = set(p['url'] for p in filtered_pages)
    for page in filtered_pages:
        for link in page['internal_links']:
            if link in url_set:
                G.add_edge(page['url'], link)
    
    # レイアウト計算
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Plotlyグラフ作成
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                showlegend=False
            )
        )
    
    # ノードトレース
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    color_map = {
        'monetization': '#84fab0',
        'feeder': '#a1c4fd',
        'hybrid': '#ffecd2'
    }
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        title = node_data['title']
        # ホバーテキストを簡潔に（クリック可能にするため）
        short_title = title[:30] + '...' if len(title) > 30 else title
        node_text.append(f"{short_title}<br>被リンク: {node_data['inbound_count']}")
        node_color.append(color_map[node_data['type']])
        node_size.append(max(10, min(50, node_data['inbound_count'] * 2)))
    
    # ノードのURL順序を保存（クリック時に使用）
    node_urls_list = list(G.nodes())
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',  # ホバー有効化
        text=node_text,
        customdata=node_urls_list,
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='#333')
        ),
        showlegend=False
    )
    
    # グラフ表示
    fig = go.Figure(
        data=edge_trace + [node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',  # ホバー有効
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            plot_bgcolor='#fafbfc'
        )
    )
    
    # グラフ表示（視覚化専用）
    st.plotly_chart(fig, use_container_width=True)
    
    # 凡例と説明
    col_legend1, col_legend2, col_legend3 = st.columns(3)
    with col_legend1:
        st.markdown("🟢 **収益化ページ** - コンバージョン重視")
    with col_legend2:
        st.markdown("🔵 **フィーダーページ** - トラフィック獲得")
    with col_legend3:
        st.markdown("🟠 **ハイブリッド** - 両方の役割")
    
    st.caption("💡 ノードの大きさ = 被リンク数 | ノードにマウスを乗せるとページ情報が表示されます")
    st.info("📋 **ページ詳細は下の一覧をクリックして展開** または 🔍 **セレクトボックスから選択**")



# ページ一覧
st.header("📄 ページ詳細リスト")

# ページ選択（デフォルトは「全て表示」）
page_urls = ['__all__'] + [p['url'] for p in filtered_pages]
page_options = {
    '__all__': '📋 全ページ一覧を表示',
    **{p['url']: p.get('title', p.get('h1', p['url'])) for p in filtered_pages}
}

# session_stateから現在の選択を取得（ボタンクリックで変更されている可能性がある）
current_selection = st.session_state.get('selected_url', '__all__')

# 現在の選択がpage_urlsにない場合（フィルター変更時など）、デフォルトに戻す
if current_selection not in page_urls:
    current_selection = '__all__'

# デフォルトインデックスを設定
default_index = page_urls.index(current_selection) if current_selection in page_urls else 0

selected_page_url = st.selectbox(
    "ページを選択してください",
    page_urls,
    index=default_index,
    format_func=lambda url: page_options[url],
    key='page_selector'
)

# セレクトボックスの選択をsession_stateに保存
st.session_state['selected_url'] = selected_page_url

# 全ページ一覧表示
if selected_page_url == '__all__':
    st.subheader(f"📋 全ページ一覧（{len(filtered_pages)}ページ）")
    st.info("💡 タイトルをクリックして展開すると、詳細情報（内部リンク、広告リンク、キーワードなど）が表示されます")
    
    # ページタイプごとにグループ化
    type_labels = {
        'monetization': '💰 収益化ページ',
        'feeder': '📝 フィーダーページ',
        'hybrid': '🔄 ハイブリッド'
    }
    
    for page_type in ['monetization', 'feeder', 'hybrid']:
        pages_of_type = [p for p in filtered_pages if p['type'] == page_type]
        if pages_of_type:
            st.markdown(f"### {type_labels[page_type]} ({len(pages_of_type)})")
            
            # カード形式で表示（展開可能）
            for page in pages_of_type:
                title = page.get('title', page.get('h1', page['url']))
                
                # 展開可能なカード
                with st.expander(f"**{title}** | 被リンク:{page['inbound_count']} | 内部:{len(page['internal_links'])} | 広告:{len(page['ad_links'])}", expanded=False):
                    # ページ詳細
                    st.markdown(f"**URL:** [{page['url']}]({page['url']})")
                    
                    # 統計
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("被リンク数", page['inbound_count'])
                    with col2:
                        st.metric("内部リンク数", len(page['internal_links']))
                    with col3:
                        st.metric("広告リンク数", len(page['ad_links']))
                    
                    # Ahrefsキーワード
                    if page['url'] in ahrefs_data:
                        st.markdown("#### 🎯 上位キーワード（20位以内）")
                        keywords = ahrefs_data[page['url']]
                        
                        keyword_html = ""
                        for kw in keywords[:20]:
                            rank_class = "rank-1-10" if kw['Current position'] <= 10 else "rank-11-20"
                            keyword_html += f'<span class="keyword-badge {rank_class}">' \
                                          f'<strong>{kw["Current position"]}位</strong> ' \
                                          f'{kw["Keyword"]} ({kw["Volume"]})</span> '
                        
                        st.markdown(keyword_html, unsafe_allow_html=True)
                    
                    # 被リンク（このページにリンクしているページ）
                    inbound_pages = [p for p in data['pages'] if page['url'] in p.get('internal_links', [])]
                    if inbound_pages:
                        st.markdown(f"#### 🔙 被リンク（{len(inbound_pages)}件）")
                        st.caption("このページにリンクしているページ一覧")
                        
                        inbound_data = []
                        for inbound_page in inbound_pages[:20]:
                            inbound_title = inbound_page.get('title', inbound_page.get('h1', inbound_page['url']))
                            inbound_data.append({
                                'タイトル': inbound_title,
                                'URL': inbound_page['url'],
                                'タイプ': type_labels.get(inbound_page['type'], inbound_page['type'])
                            })
                        
                        df_inbound = pd.DataFrame(inbound_data)
                        st.dataframe(df_inbound, use_container_width=True, hide_index=True)
                    
                    # 内部リンク
                    if page['internal_links']:
                        st.markdown("#### 🔗 内部リンク")
                        
                        link_data = []
                        for link in page['internal_links'][:20]:
                            linked_page = next((p for p in data['pages'] if p['url'] == link), None)
                            link_title = linked_page.get('title', linked_page.get('h1', link)) if linked_page else link.split('/')[-1]
                            link_data.append({'タイトル': link_title, 'URL': link})
                        
                        df_links = pd.DataFrame(link_data)
                        st.dataframe(df_links, use_container_width=True, hide_index=True)
                    
                    # 広告リンク
                    if page['ad_links']:
                        st.markdown("#### 💰 広告リンク")
                        df_ads = pd.DataFrame([
                            {'テキスト': ad.get('text', 'リンク'), 'タイプ': ad['type']}
                            for ad in page['ad_links'][:10]
                        ])
                        st.dataframe(df_ads, use_container_width=True, hide_index=True)


# 個別ページ詳細表示
elif selected_page_url:
    page = next(p for p in filtered_pages if p['url'] == selected_page_url)
    
    # ページ詳細
    st.subheader(f"🔍 {page.get('title', page.get('h1', 'ページ詳細'))}")
    
    # バッジ
    type_labels = {
        'monetization': '収益化ページ',
        'feeder': 'フィーダーページ',
        'hybrid': 'ハイブリッド'
    }
    st.markdown(f"**タイプ:** `{type_labels[page['type']]}`")
    st.markdown(f"**URL:** [{page['url']}]({page['url']})")
    
    # 統計
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("被リンク数", page['inbound_count'])
    with col2:
        st.metric("内部リンク数", len(page['internal_links']))
    with col3:
        st.metric("広告リンク数", len(page['ad_links']))
    
    # Ahrefsキーワード
    if page['url'] in ahrefs_data:
        st.markdown("### 🎯 上位キーワード（20位以内）")
        keywords = ahrefs_data[page['url']]
        
        keyword_html = ""
        for kw in keywords[:20]:
            rank_class = "rank-1-10" if kw['Current position'] <= 10 else "rank-11-20"
            keyword_html += f'<span class="keyword-badge {rank_class}">' \
                          f'<strong>{kw["Current position"]}位</strong> ' \
                          f'{kw["Keyword"]} ({kw["Volume"]})</span> '
        
        st.markdown(keyword_html, unsafe_allow_html=True)
    
    # 内部リンク
    if page['internal_links']:
        st.markdown("### 🔗 内部リンク")
        
        # リンク先のタイトルを取得
        link_data = []
        for link in page['internal_links'][:20]:
            linked_page = next((p for p in data['pages'] if p['url'] == link), None)
            title = linked_page.get('title', linked_page.get('h1', link)) if linked_page else link.split('/')[-1]
            link_data.append({'タイトル': title, 'URL': link})
        
        df_links = pd.DataFrame(link_data)
        st.dataframe(df_links, use_container_width=True, hide_index=True)
    
    # 広告リンク
    if page['ad_links']:
        st.markdown("### 💰 広告リンク")
        df_ads = pd.DataFrame([
            {'テキスト': ad.get('text', 'リンク'), 'タイプ': ad['type']}
            for ad in page['ad_links'][:10]
        ])
        st.dataframe(df_ads, use_container_width=True, hide_index=True)

# フッター
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #6c757d;">Made with ❤️ for SEO analysis | '
    '<a href="https://github.com/ty307407-commits/FUNDiT" target="_blank">GitHub</a></p>',
    unsafe_allow_html=True
)
