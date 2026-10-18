const fs = require('fs');
const path = require('path');
const { Resvg } = require('./tools/node_modules/@resvg/resvg-js');

const root = process.argv[2];
if (!root) {
  console.error('usage: node render_chars.js <characters-dir>');
  process.exit(1);
}

const dirs = fs.readdirSync(root, { withFileTypes: true })
  .filter(entry => entry.isDirectory() && entry.name.startsWith('U+'))
  .map(entry => entry.name)
  .sort();

for (const name of dirs) {
  const svgPath = path.join(root, name, 'keycap.svg');
  const pngPath = path.join(root, name, 'preview.png');
  const svg = fs.readFileSync(svgPath, 'utf8');
  const match = svg.match(/\bwidth="([0-9.]+)"/);
  if (!match) throw new Error(`no width in ${svgPath}`);
  const width = Math.max(160, Math.round(parseFloat(match[1]) * 4));
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: width },
    background: '#F7F5F0',
  });
  fs.writeFileSync(pngPath, resvg.render().asPng());
}

console.log(`rendered ${dirs.length} character previews`);
