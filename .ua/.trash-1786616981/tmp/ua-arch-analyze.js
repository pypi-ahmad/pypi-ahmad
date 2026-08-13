const fs = require('fs');
const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) { console.error('usage: node ua-arch-analyze.js input output'); process.exit(1); }
try {
  const input = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const nodes = input.fileNodes || [], imports = input.importEdges || [], all = input.allEdges || [];
  const byId = new Map(nodes.map(n => [n.id, n]));
  const segments = nodes.map(n => (n.filePath || '').split('/'));
  let prefix = [];
  for (let i = 0; ; i++) { const v = segments[0]?.[i]; if (!v || !segments.every(s => s[i] === v)) break; prefix.push(v); }
  const group = n => { const s=(n.filePath||'').split('/'); const rest=s.slice(prefix.length); return rest.length > 1 ? rest[0] : 'root'; };
  const directoryGroups = {}, nodeTypeGroups = {}, fanIn = {}, fanOut = {}, patterns = {};
  for (const n of nodes) { const g=group(n); (directoryGroups[g]??=[]).push(n.id); (nodeTypeGroups[n.type]??=[]).push(n.id); fanIn[n.id]=0; fanOut[n.id]=0; }
  const pattern = g => ({'.github':'ci-cd',scripts:'utility',docs:'documentation',config:'config',assets:'assets',public:'assets'}[g] || (g==='root' ? 'root' : 'unclassified'));
  for (const g of Object.keys(directoryGroups)) patterns[g]=pattern(g);
  const inter = new Map(), involved = {}, internal = {};
  for (const e of imports) { if (!byId.has(e.source)||!byId.has(e.target)) continue; fanOut[e.source]++; fanIn[e.target]++; const a=group(byId.get(e.source)),b=group(byId.get(e.target)),k=a+'\u0000'+b; inter.set(k,(inter.get(k)||0)+1); involved[a]=(involved[a]||0)+1; involved[b]=(involved[b]||0)+1; if(a===b) internal[a]=(internal[a]||0)+1; }
  const interGroupImports=[...inter].map(([k,count])=>{const [from,to]=k.split('\u0000');return {from,to,count};});
  const intraGroupDensity=Object.fromEntries(Object.keys(directoryGroups).map(g=>[g,{internalEdges:internal[g]||0,totalEdges:involved[g]||0,density:(internal[g]||0)/((involved[g]||0)||1)}]));
  const cross=new Map(); for (const e of all) {const s=byId.get(e.source),t=byId.get(e.target);if(!s||!t)continue;const k=s.type+'\u0000'+t.type+'\u0000'+e.type;cross.set(k,(cross.get(k)||0)+1)}
  const crossCategoryEdges=[...cross].map(([k,count])=>{const [fromType,toType,edgeType]=k.split('\u0000');return {fromType,toType,edgeType,count};});
  const files=nodes.map(n=>n.filePath); const infraFiles=files.filter(p=>p.includes('.github/workflows/')||/docker|terraform|k8s|helm/i.test(p));
  const groupsWithDocs=Object.keys(directoryGroups).filter(g=>directoryGroups[g].some(id=>/\.md$/i.test(byId.get(id).filePath))).length;
  const dependencyDirection=interGroupImports.filter(x=>x.from!==x.to).map(x=>({dependent:x.from,dependsOn:x.to}));
  const result={scriptCompleted:true,directoryGroups,nodeTypeGroups,crossCategoryEdges,interGroupImports,intraGroupDensity,patternMatches:patterns,deploymentTopology:{hasDockerfile:files.some(p=>/Dockerfile$/i.test(p)),hasCompose:files.some(p=>/docker-compose/i.test(p)),hasK8s:files.some(p=>/k8s|kubernetes|helm/i.test(p)),hasTerraform:files.some(p=>/\.tf(vars)?$/i.test(p)),hasCI:files.some(p=>p.includes('.github/workflows/')),infraFiles},dataPipeline:{schemaFiles:files.filter(p=>/\.(sql|graphql|gql|proto)$/i.test(p)),migrationFiles:files.filter(p=>/migrations?\//i.test(p)),dataModelFiles:[],apiHandlerFiles:[]},docCoverage:{groupsWithDocs,totalGroups:Object.keys(directoryGroups).length,coverageRatio:groupsWithDocs/Object.keys(directoryGroups).length,undocumentedGroups:Object.keys(directoryGroups).filter(g=>!directoryGroups[g].some(id=>/\.md$/i.test(byId.get(id).filePath)))},dependencyDirection,fileStats:{totalFileNodes:nodes.length,filesPerGroup:Object.fromEntries(Object.entries(directoryGroups).map(([g,ids])=>[g,ids.length])),nodeTypeCounts:Object.fromEntries(Object.entries(nodeTypeGroups).map(([t,ids])=>[t,ids.length]))},fileFanIn:fanIn,fileFanOut:fanOut};
  fs.writeFileSync(outputPath, JSON.stringify(result,null,2));
} catch (error) { console.error(error.stack || error); process.exit(1); }
