import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto('http://localhost:3000', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 2500));

const hero = await page.$('#hero');
if (hero) {
  await hero.screenshot({ path: 'temporary screenshots/hero-crop.png' });
  console.log('Hero screenshot saved');
} else {
  // fallback: clip to viewport
  await page.screenshot({ path: 'temporary screenshots/hero-crop.png', clip: { x: 0, y: 0, width: 1440, height: 900 } });
  console.log('Hero screenshot saved (viewport fallback)');
}
await browser.close();
