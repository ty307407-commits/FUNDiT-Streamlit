#!/usr/bin/env python3
"""QBC用HTMLビジュアライザーにJSONデータを埋め込む"""
import json

# JSONデータを読み込み
with open('qbc_link_analysis_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# HTMLテンプレート
html_template = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QBC 内部リンク構造 & 広告配置分析</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; font-weight: 700; }
        .subtitle { font-size: 1.1em; opacity: 0.9; }
        .controls {
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        .control-group { display: flex; align-items: center; gap: 10px; }
        label { font-weight: 600; color: #495057; }
        input, select {
            padding: 8px 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 14px;
        }
        .stats {
            padding: 20px 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .stat-card {
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stat-card.total { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .stat-card.monetization { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); }
        .stat-card.feeder { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); }
        .stat-card.hybrid { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
        .stat-value { font-size: 2.5em; font-weight: 700; }
        .stat-label { font-size: 0.9em; opacity: 0.8; }
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            min-height: 800px;
        }
        #network-graph { background: #fafbfc; position: relative; }
        .detail-panel {
            background: white;
            border-left: 2px solid #e9ecef;
            padding: 30px;
            overflow-y: auto;
            max-height: 800px;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge.monetization { background: #84fab0; color: #065f46; }
        .badge.feeder { background: #a1c4fd; color: #1e40af; }
        .badge.hybrid { background: #ffecd2; color: #92400e; }
        .link-list { list-style: none; margin-top: 10px; }
        .link-list li {
            padding: 8px 12px;
            margin-bottom: 5px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 0.9em;
        }
        .ad-link { background: #fff3cd !important; border-left: 3px solid #ffc107; }
        .ad-type {
            padding: 2px 8px;
            background: #f093fb;
            color: white;
            border-radius: 4px;
            font-size: 0.75em;
            margin-left: 8px;
        }
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 100;
        }
        .legend-item { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .legend-circle { width: 20px; height: 20px; border-radius: 50%; border: 2px solid #333; }
        .node { cursor: pointer; }
        .link { stroke: #999; stroke-opacity: 0.3; stroke-width: 1.5px; }
        svg { width: 100%; height: 100%; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔗 QBC 内部リンク構造 & 広告配置分析</h1>
            <p class="subtitle">収益化ページとフィーダーページの可視化</p>
        </header>
        <div class="controls">
            <div class="control-group">
                <label>フィルター:</label>
                <select id="typeFilter">
                    <option value="all">全て表示</option>
                    <option value="monetization">収益化ページのみ</option>
                    <option value="feeder">フィーダーページのみ</option>
                    <option value="hybrid">ハイブリッドのみ</option>
                </select>
            </div>
            <div class="control-group">
                <label>検索:</label>
                <input type="text" id="searchInput" placeholder="キーワードまたはURL...">
            </div>
        </div>
        <div class="stats" id="stats"></div>
        <div class="main-content">
            <div id="network-graph">
                <div class="legend">
                    <h4>凡例</h4>
                    <div class="legend-item">
                        <div class="legend-circle" style="background: #84fab0;"></div>
                        <span>収益化ページ</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-circle" style="background: #a1c4fd;"></div>
                        <span>フィーダーページ</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-circle" style="background: #ffecd2;"></div>
                        <span>ハイブリッド</span>
                    </div>
                </div>
            </div>
            <div class="detail-panel">
                <div style="text-align: center; color: #6c757d; padding: 40px;">
                    <div style="font-size: 3em;">👆</div>
                    <p>ノードをクリックして詳細を表示</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        const DATA = ''' + json.dumps(data, ensure_ascii=False) + ''';
        let allData = DATA;
        let filteredData = DATA;
        let simulation = null;

        initializeApp();

        function initializeApp() {
            renderStats();
            renderGraph();
            setupEventListeners();
        }

        function renderStats() {
            const s = allData.summary;
            document.getElementById('stats').innerHTML = `
                <div class="stat-card total"><div class="stat-value">${s.total_pages}</div><div class="stat-label">総ページ数</div></div>
                <div class="stat-card monetization"><div class="stat-value">${s.monetization_pages}</div><div class="stat-label">収益化ページ</div></div>
                <div class="stat-card feeder"><div class="stat-value">${s.feeder_pages}</div><div class="stat-label">フィーダーページ</div></div>
                <div class="stat-card hybrid"><div class="stat-value">${s.hybrid_pages}</div><div class="stat-label">ハイブリッド</div></div>
                <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);"><div class="stat-value">${s.total_ad_links}</div><div class="stat-label">総広告リンク数</div></div>
                <div class="stat-card" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); color: white;"><div class="stat-value">${s.avg_internal_links}</div><div class="stat-label">平均内部リンク数</div></div>
            `;
        }

        function renderGraph() {
            const container = document.getElementById('network-graph');
            const width = container.clientWidth;
            const height = 800;
            d3.select('#network-graph svg').remove();
            const svg = d3.select('#network-graph').append('svg').attr('width', width).attr('height', height);
            const g = svg.append('g');
            svg.call(d3.zoom().scaleExtent([0.1, 4]).on('zoom', e => g.attr('transform', e.transform)));

            const nodes = filteredData.pages.map(p => ({...p, id: p.url}));
            const links = [];
            const urlMap = new Map(nodes.map(n => [n.id, n]));
            filteredData.pages.forEach(p => {
                p.internal_links.forEach(link => {
                    if (urlMap.has(link)) links.push({source: p.url, target: link});
                });
            });

            const color = d3.scaleOrdinal().domain(['monetization', 'feeder', 'hybrid']).range(['#84fab0', '#a1c4fd', '#ffecd2']);
            const size = d3.scaleLinear().domain([0, d3.max(nodes, d => d.inbound_count) || 1]).range([5, 20]);

            simulation = d3.forceSimulation(nodes)
                .force('link', d3.forceLink(links).id(d => d.id).distance(100))
                .force('charge', d3.forceManyBody().strength(-300))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('collision', d3.forceCollide().radius(d => size(d.inbound_count) + 5));

            const link = g.append('g').selectAll('line').data(links).join('line').attr('class', 'link');
            const node = g.append('g').selectAll('circle').data(nodes).join('circle')
                .attr('class', 'node')
                .attr('r', d => size(d.inbound_count))
                .attr('fill', d => color(d.type))
                .attr('stroke', '#333')
                .attr('stroke-width', 2)
                .on('click', (e, d) => showDetails(d))
                .call(d3.drag()
                    .on('start', e => { if (!e.active) simulation.alphaTarget(0.3).restart(); e.subject.fx = e.subject.x; e.subject.fy = e.subject.y; })
                    .on('drag', e => { e.subject.fx = e.x; e.subject.fy = e.y; })
                    .on('end', e => { if (!e.active) simulation.alphaTarget(0); e.subject.fx = null; e.subject.fy = null; }));

            simulation.on('tick', () => {
                link.attr('x1', d => d.source.x).attr('y1', d => d.source.y).attr('x2', d => d.target.x).attr('y2', d => d.target.y);
                node.attr('cx', d => d.x).attr('cy', d => d.y);
            });
        }

        function showDetails(node) {
            const labels = {monetization: '収益化ページ', feeder: 'フィーダーページ', hybrid: 'ハイブリッド'};
            
            // 内部リンクをページタイトル表示+クリック可能に
            const internalLinks = node.internal_links.slice(0, 20).map(l => {
                const linkedPage = allData.pages.find(p => p.url === l);
                const displayText = linkedPage ? (linkedPage.h1 || l.split('/').pop()) : l.split('/').pop();
                return `<li><a href="${l}" target="_blank" style="color: #667eea; text-decoration: none;">${displayText}</a></li>`;
            }).join('');
            
            const adLinks = node.ad_links.slice(0, 10).map(a => `<li class="ad-link">${a.text || 'リンク'}<span class="ad-type">${a.type}</span></li>`).join('');
            
            document.querySelector('.detail-panel').innerHTML = `
                <h2>ページ詳細</h2>
                <div><span class="badge ${node.type}">${labels[node.type]}</span></div>
                <div style="margin: 15px 0;"><a href="${node.url}" target="_blank" style="color: #f093fb; text-decoration: none;">${node.h1 || node.url}</a></div>
                <div><h3 style="color: #f093fb;">📊 基本情報</h3>
                <ul class="link-list">
                    ${node.keyword ? `<li><strong>キーワード:</strong> ${node.keyword}</li>` : ''}
                    ${node.rank ? `<li><strong>順位:</strong> ${node.rank}</li>` : ''}
                    <li><strong>被リンク数:</strong> ${node.inbound_count}</li>
                </ul></div>
                ${adLinks ? `<div><h3 style="color: #f093fb;">💰 広告リンク (${node.ad_links.length})</h3><ul class="link-list">${adLinks}</ul></div>` : ''}
                ${internalLinks ? `<div><h3 style="color: #f093fb;">🔗 内部リンク (${node.internal_links.length})</h3><ul class="link-list">${internalLinks}</ul></div>` : ''}
            `;
        }

        function setupEventListeners() {
            document.getElementById('typeFilter').addEventListener('change', e => {
                filteredData = e.target.value === 'all' ? allData : {...allData, pages: allData.pages.filter(p => p.type === e.target.value)};
                renderGraph();
            });
            document.getElementById('searchInput').addEventListener('input', e => {
                const term = e.target.value.toLowerCase();
                filteredData = term === '' ? allData : {...allData, pages: allData.pages.filter(p => 
                    p.url.toLowerCase().includes(term) || (p.h1 && p.h1.toLowerCase().includes(term)) || (p.keyword && p.keyword.toLowerCase().includes(term))
                )};
                renderGraph();
            });
        }
    </script>
</body>
</html>'''

# HTMLファイルを書き込み
with open('qbc_link_visualizer_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✓ HTMLファイルを生成しました: qbc_link_visualizer_standalone.html")
