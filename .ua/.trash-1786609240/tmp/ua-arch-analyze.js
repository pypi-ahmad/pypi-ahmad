const fs = require('fs');

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) throw new Error('Expected input and output paths');
const input = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const nodes = input.fileNodes || [];
const edges = input.allEdges || [];
const ids = new Set(nodes.map(node => node.id));
const firstGroup = path => {
  const parts = path.split('/');
  return parts.length > 1 ? parts[0] : '(root)';
};
const classify = (group, path) => {
  if (group === '.github') return path.includes('/workflows/') ? 'ci-cd' : 'config';
  if (group === 'scripts') return 'utility';
  if (group === 'graphify-out') return 'config';
  if (group === '.ua') return 'config';
  if (/\.md$/i.test(path)) return 'documentation';
  return 'root';
};
const directoryGroups = {};
const nodeTypeGroups = {};
const groupById = {};
for (const node of nodes) {
  const group = firstGroup(node.filePath || '');
  (directoryGroups[group] ||= []).push(node.id);
  (nodeTypeGroups[node.type] ||= []).push(node.id);
  groupById[node.id] = group;
}
const edgeCounts = new Map();
for (const edge of edges) {
  const source = nodes.find(node => node.id === edge.source);
  const target = nodes.find(node => node.id === edge.target);
  if (!source || !target) continue;
  const key = `${source.type}|${target.type}|${edge.type}`;
  edgeCounts.set(key, (edgeCounts.get(key) || 0) + 1);
}
const crossCategoryEdges = [...edgeCounts].map(([key, count]) => {
  const [fromType, toType, edgeType] = key.split('|');
  return { fromType, toType, edgeType, count };
});
const importCounts = new Map();
for (const edge of input.importEdges || []) {
  const from = groupById[edge.source];
  const to = groupById[edge.target];
  if (!from || !to) continue;
  const key = `${from}|${to}`;
  importCounts.set(key, (importCounts.get(key) || 0) + 1);
}
const interGroupImports = [...importCounts].map(([key, count]) => {
  const [from, to] = key.split('|');
  return { from, to, count };
});
const intraGroupDensity = {};
for (const group of Object.keys(directoryGroups)) {
  const involved = (input.importEdges || []).filter(edge => groupById[edge.source] === group || groupById[edge.target] === group);
  const internal = involved.filter(edge => groupById[edge.source] === group && groupById[edge.target] === group).length;
  intraGroupDensity[group] = { internalEdges: internal, totalEdges: involved.length, density: involved.length ? internal / involved.length : 0 };
}
const patternMatches = Object.fromEntries(Object.keys(directoryGroups).map(group => [group, classify(group, '')]));
const infraFiles = nodes.filter(node => node.type === 'pipeline' || node.type === 'service' || node.type === 'resource').map(node => node.filePath);
const documents = new Set(nodes.filter(node => node.type === 'document').map(node => firstGroup(node.filePath)));
const direction = [];
for (const entry of interGroupImports) if (entry.from !== entry.to) direction.push({ dependent: entry.from, dependsOn: entry.to });
const typeCounts = {};
for (const node of nodes) typeCounts[node.type] = (typeCounts[node.type] || 0) + 1;
const result = {
  scriptCompleted: true,
  directoryGroups,
  nodeTypeGroups,
  crossCategoryEdges,
  interGroupImports,
  intraGroupDensity,
  patternMatches,
  deploymentTopology: { hasDockerfile: false, hasCompose: false, hasK8s: false, hasTerraform: false, hasCI: infraFiles.some(path => path.includes('.github/workflows/')), infraFiles },
  dataPipeline: { schemaFiles: nodes.filter(node => node.type === 'schema').map(node => node.filePath), migrationFiles: [], dataModelFiles: [], apiHandlerFiles: [] },
  docCoverage: { groupsWithDocs: documents.size, totalGroups: Object.keys(directoryGroups).length, coverageRatio: Object.keys(directoryGroups).length ? documents.size / Object.keys(directoryGroups).length : 0, undocumentedGroups: Object.keys(directoryGroups).filter(group => !documents.has(group)) },
  dependencyDirection: direction,
  fileStats: { totalFileNodes: nodes.length, filesPerGroup: Object.fromEntries(Object.entries(directoryGroups).map(([group, values]) => [group, values.length])), nodeTypeCounts: typeCounts },
  fileFanIn: Object.fromEntries(nodes.map(node => [node.id, (input.importEdges || []).filter(edge => edge.target === node.id).length])),
  fileFanOut: Object.fromEntries(nodes.map(node => [node.id, (input.importEdges || []).filter(edge => edge.source === node.id).length]))
};
fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
