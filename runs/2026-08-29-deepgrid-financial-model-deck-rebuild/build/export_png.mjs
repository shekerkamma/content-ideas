import { writeFile } from 'node:fs/promises';
const AT='file:///home/sheke/.local/artifact-tool-linux/dist';
const { PresentationFile } = await import(`${AT}/artifact_tool.mjs`);
const buf = await (await import('node:fs/promises')).readFile(process.argv[2]);
const P = await PresentationFile.importPptx(new Uint8Array(buf));
const n = P.slides.items.length;
console.log('slides:', n);
for (let i=0;i<n;i++){
  const blob = await P.export({ format:'png', slide: P.slides.getItem(i), scale: 2 });
  await writeFile(`../video/frames/slide-${String(i+1).padStart(2,'0')}.png`, Buffer.from(await blob.arrayBuffer()));
}
console.log('exported', n, 'PNGs at scale 2');
