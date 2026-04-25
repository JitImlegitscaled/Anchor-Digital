import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto('http://localhost:3000', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 2000));

// Click light mode button
await page.click('#toggle-light');
await new Promise(r => setTimeout(r, 1400)); // wait for filter transition

const hero = await page.$('#hero');
if (hero) {
  await hero.screenshot({ path: 'temporary screenshots/hero-light.png' });
  console.log('Light hero screenshot saved');
}
await browser.close();
