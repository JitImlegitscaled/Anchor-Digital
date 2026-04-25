import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto('http://localhost:3000', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 3000));

const info = await page.evaluate(() => {
  const paths = document.querySelectorAll('.hero-paths-svg path');
  const p = paths[5]; // pick one mid-way that should be partly visible
  if (!p) return { error: 'no path' };
  const cs = window.getComputedStyle(p);
  return {
    strokeDasharray: cs.strokeDasharray,
    strokeDashoffset: cs.strokeDashoffset,
    animationName: cs.animationName,
    animationPlayState: cs.animationPlayState,
    stroke: cs.stroke,
    opacity: cs.opacity,
    visibility: cs.visibility,
    display: cs.display,
  };
});
console.log(JSON.stringify(info, null, 2));

await browser.close();
