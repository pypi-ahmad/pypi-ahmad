const fs = require('fs');
const path = require('path');

const root = process.argv[2];
const ua = path.join(root, '.ua');
const graph = JSON.parse(fs.readFileSync(path.join(ua, 'intermediate', 'assembled-graph.json'), 'utf8'));
const scan = JSON.parse(fs.readFileSync(path.join(ua, 'intermediate', 'scan-result.json'), 'utf8'));
const layers = JSON.parse(fs.readFileSync(path.join(ua, 'intermediate', 'layers.json'), 'utf8'));
const tour = JSON.parse(fs.readFileSync(path.join(ua, 'intermediate', 'tour.json'), 'utf8'));
const commit = process.argv[3];

const finalGraph = {
  version: '1.0.0',
  project: {
    name: scan.name,
    languages: scan.languages,
    frameworks: scan.frameworks,
    description: scan.description,
    analyzedAt: new Date().toISOString(),
    gitCommitHash: commit,
  },
  nodes: graph.nodes,
  edges: graph.edges,
  layers: Array.isArray(layers) ? layers : layers.layers,
  tour: Array.isArray(tour) ? tour : tour.steps,
};

fs.writeFileSync(path.join(ua, 'intermediate', 'assembled-graph.json'), JSON.stringify(finalGraph, null, 2));
