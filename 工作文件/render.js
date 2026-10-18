const fs = require('fs');
const { Resvg } = require('./tools/node_modules/@resvg/resvg-js');
const inFile = process.argv[2];
const outFile = process.argv[3];
const width = parseInt(process.argv[4] || '1047', 10);
const svg = fs.readFileSync(inFile, 'utf8');
const resvg = new Resvg(svg, {
  fitTo: { mode: 'width', value: width },
  background: 'rgba(0,0,0,0)',
});
const png = resvg.render().asPng();
fs.writeFileSync(outFile, png);
console.log('rendered', outFile, png.length, 'bytes', width + 'px');
