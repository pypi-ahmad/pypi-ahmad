const fs = require('fs');
try {
  const graph = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  if (!graph.layers) graph.layers = JSON.parse(fs.readFileSync('.ua/intermediate/layers.json', 'utf8'));
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const byId = new Map(nodes.map(node => [node.id, node]));
  const fanIn = new Map(nodes.map(node => [node.id, 0]));
  const fanOut = new Map(nodes.map(node => [node.id, 0]));
  for (const edge of edges) {
    if (fanIn.has(edge.target)) fanIn.set(edge.target, fanIn.get(edge.target) + 1);
    if (fanOut.has(edge.source)) fanOut.set(edge.source, fanOut.get(edge.source) + 1);
  }
  const rank = (counts, key) => [...counts].map(([id, value]) => ({id, [key]: value, name: byId.get(id)?.name})).sort((a, b) => b[key] - a[key] || a.id.localeCompare(b.id)).slice(0, 20);
  const candidates = nodes.map(node => {
    let score = 0;
    if (node.id === 'document:README.md') score += 5;
    else if (node.type === 'document' && /^[^/]+\.md$/i.test(node.filePath || '')) score += 2;
    if (node.type === 'file') {
      if (/^(index|main|app|server|manage|run|__main__)\.(ts|js|py|go|rs)$/i.test(node.name || '')) score += 3;
      if ((node.filePath || '').split('/').length <= 2) score += 1;
      if (fanOut.get(node.id) > 0) score += 1;
    }
    return {id: node.id, score, name: node.name, summary: node.summary};
  }).filter(candidate => candidate.score > 0).sort((a, b) => b.score - a.score || a.id.localeCompare(b.id)).slice(0, 5);
  const start = nodes.find(node => node.id === 'file:scripts/generate_repo_cards.py') || nodes.find(node => node.type === 'file');
  const adjacency = new Map(nodes.map(node => [node.id, []]));
  for (const edge of edges) if (['imports', 'calls', 'contains'].includes(edge.type) && adjacency.has(edge.source)) adjacency.get(edge.source).push(edge.target);
  const order = [], depthMap = {}, queue = start ? [[start.id, 0]] : [];
  while (queue.length) { const [id, depth] = queue.shift(); if (depthMap[id] !== undefined) continue; depthMap[id] = depth; order.push(id); for (const next of adjacency.get(id) || []) if (byId.has(next) && depthMap[next] === undefined) queue.push([next, depth + 1]); }
  const byDepth = {}; for (const id of order) (byDepth[depthMap[id]] ||= []).push(id);
  const categories = {documentation: [], infrastructure: [], data: [], config: []};
  for (const node of nodes) {
    const item = {id: node.id, name: node.name, type: node.type, summary: node.summary};
    if (node.type === 'document') categories.documentation.push(item);
    if (['service', 'pipeline', 'resource'].includes(node.type)) categories.infrastructure.push(item);
    if (['table', 'schema', 'endpoint'].includes(node.type)) categories.data.push(item);
    if (node.type === 'config') categories.config.push(item);
  }
  const result = {scriptCompleted: true, entryPointCandidates: candidates, fanInRanking: rank(fanIn, 'fanIn'), fanOutRanking: rank(fanOut, 'fanOut'), bfsTraversal: {startNode: start?.id || null, order, depthMap, byDepth}, nonCodeFiles: categories, clusters: [], layers: {count: (graph.layers || []).length, list: graph.layers || []}, nodeSummaryIndex: Object.fromEntries(nodes.map(node => [node.id, {name: node.name, type: node.type, summary: node.summary}])), totalNodes: nodes.length, totalEdges: edges.length};
  fs.writeFileSync(process.argv[3], JSON.stringify(result, null, 2));
} catch (error) { console.error(error.message); process.exit(1); }
