const fs = require('fs');

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  console.error('Usage: node ua-tour-analyze.js INPUT OUTPUT');
  process.exit(1);
}
try {
  const graph = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const layers = JSON.parse(fs.readFileSync('.ua/intermediate/layers.json', 'utf8'));
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const byId = new Map(nodes.map(n => [n.id, n]));
  const inCount = new Map(nodes.map(n => [n.id, 0]));
  const outCount = new Map(nodes.map(n => [n.id, 0]));
  const adjacency = new Map(nodes.map(n => [n.id, []]));
  for (const edge of edges) {
    if (byId.has(edge.source) && byId.has(edge.target)) {
      inCount.set(edge.target, inCount.get(edge.target) + 1);
      outCount.set(edge.source, outCount.get(edge.source) + 1);
      if (edge.type === 'imports' || edge.type === 'calls') adjacency.get(edge.source).push(edge.target);
    }
  }
  const ranked = (counts, key) => [...nodes].sort((a,b) => counts.get(b.id) - counts.get(a.id) || a.id.localeCompare(b.id)).slice(0,20).map(n => ({id:n.id,[key]:counts.get(n.id),name:n.name}));
  const outValues = [...outCount.values()].sort((a,b)=>a-b);
  const inValues = [...inCount.values()].sort((a,b)=>a-b);
  const highOut = outValues[Math.max(0, Math.ceil(outValues.length * .9) - 1)] || 0;
  const lowIn = inValues[Math.min(inValues.length - 1, Math.floor(inValues.length * .25))] || 0;
  const entryPointCandidates = nodes.map(n => {
    let score = 0;
    const p = n.filePath || '';
    const base = p.split('/').pop();
    if (n.type === 'document' && p === 'README.md') score += 5;
    else if (n.type === 'document' && !p.includes('/')) score += 2;
    if (n.type === 'file') {
      if (/^(index|main|app|server|manage|run|__main__)\.(ts|js|py|go|rs|java|cs|php|swift|kt|cpp|c)$/.test(base)) score += 3;
      if (p && p.split('/').length <= 2) score += 1;
      if (outCount.get(n.id) >= highOut) score += 1;
      if (inCount.get(n.id) <= lowIn) score += 1;
    }
    return {id:n.id,score,name:n.name,summary:n.summary};
  }).filter(x => x.score > 0).sort((a,b)=>b.score-a.score || a.id.localeCompare(b.id)).slice(0,5);
  const start = entryPointCandidates.find(x => byId.get(x.id)?.type === 'file')?.id || null;
  const order = [], depthMap = {}, queue = start ? [[start, 0]] : [];
  while (queue.length) { const [id,d] = queue.shift(); if (id in depthMap) continue; depthMap[id]=d; order.push(id); for (const next of adjacency.get(id)||[]) if (!(next in depthMap)) queue.push([next,d+1]); }
  const byDepth = {}; for (const id of order) (byDepth[depthMap[id]] ||= []).push(id);
  const nonCodeFiles = {documentation:[], infrastructure:[], data:[], config:[]};
  for (const n of nodes) { const x={id:n.id,name:n.name,type:n.type,summary:n.summary}; if(n.type==='document') nonCodeFiles.documentation.push(x); else if(['service','pipeline','resource'].includes(n.type)) nonCodeFiles.infrastructure.push(x); else if(['table','schema','endpoint'].includes(n.type)) nonCodeFiles.data.push(x); else if(n.type==='config') nonCodeFiles.config.push(x); }
  const pairEdges = new Set(edges.filter(e => e.type==='imports'||e.type==='calls').map(e=>`${e.source}|${e.target}`));
  const clusters=[]; for(const edge of edges){ if(pairEdges.has(`${edge.target}|${edge.source}`)){ const key=[edge.source,edge.target].sort().join('|'); if(!clusters.some(c=>c.key===key)) clusters.push({key,nodes:key.split('|'),edgeCount:2}); } }
  const nodeSummaryIndex = Object.fromEntries(nodes.map(n=>[n.id,{name:n.name,type:n.type,summary:n.summary}]));
  fs.writeFileSync(outputPath, JSON.stringify({scriptCompleted:true,entryPointCandidates,fanInRanking:ranked(inCount,'fanIn'),fanOutRanking:ranked(outCount,'fanOut'),bfsTraversal:{startNode:start,order,depthMap,byDepth},nonCodeFiles,clusters:clusters.slice(0,10).map(({key,...c})=>c),layers:{count:layers.length,list:layers.map(({id,name,description})=>({id,name,description}))},nodeSummaryIndex,totalNodes:nodes.length,totalEdges:edges.length}, null, 2));
} catch (error) { console.error(error.stack || error); process.exit(1); }
