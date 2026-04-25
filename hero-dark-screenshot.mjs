import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto('http://localhost:3000', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 2000));

// Click dark mode button
await page.click('#toggle-dark');
await new Promise(r => setTimeout(r, 800)); // wait for crossfade

const hero = await page.$('#hero');
if (hero) {
  await hero.screenshot({ path: 'temporary screenshots/hero-dark.png' });
  console.log('Dark hero screenshot saved');
}
await browser.close();
