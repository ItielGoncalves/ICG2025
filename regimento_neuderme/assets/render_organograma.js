const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome',
  }).catch(async () => await chromium.launch());
  const ctx = await browser.newContext({ deviceScaleFactor: 3 });
  const page = await ctx.newPage();
  const file = 'file://' + path.resolve(__dirname, 'organograma.html');
  await page.goto(file, { waitUntil: 'networkidle' });
  const el = await page.$('#stage');
  await el.screenshot({ path: path.resolve(__dirname, 'organograma.png') });
  await browser.close();
  console.log('OK organograma.png');
})().catch(e => { console.error(e); process.exit(1); });
