const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require(process.env.PLAYWRIGHT_PATH ||
  'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const output = process.argv[2] ? path.resolve(process.argv[2]) : path.join(__dirname, 'output', 'pdf');
const destination = path.resolve(__dirname, '../../Intro DB');
(async () => {
  const items = JSON.parse(fs.readFileSync(path.join(output, 'inputs.json'), 'utf8'));
  const browser = await chromium.launch({headless: true, executablePath: process.env.CHROME_PATH ||
    'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  try {
    for (const item of items) {
      if (!/^ch\d{2}(?:_answer)?$/.test(item.chapter)) throw Error('Invalid PDF filename');
      const page = await browser.newPage({viewport: {width: 673, height: 980}});
      await page.goto(pathToFileURL(path.join(output, item.chapter + '.html')).href);
      await page.evaluate(() => Promise.all([...document.images].map(image => image.decode())));
      await page.evaluate(() => document.fonts.ready);
      await page.emulateMedia({media: 'print'});
      const result = await page.evaluate(() => ({
        text: document.querySelector('main').innerText,
        images: document.images.length,
        broken: [...document.images].filter(i => !i.naturalWidth).length,
        overflow: document.documentElement.scrollWidth > innerWidth + 1
      }));
      if (result.broken || result.images !== item.images || result.overflow) throw Error(JSON.stringify(result));
      fs.writeFileSync(path.join(output, item.chapter + '_browser.json'), JSON.stringify(result));
      await page.pdf({path: path.join(destination, item.chapter + '.pdf'), format: 'A4',
        preferCSSPageSize: true, printBackground: true, displayHeaderFooter: true,
        headerTemplate: `<div style="font:8px Arial;color:#52646b;width:100%;padding:0 16mm">Database Management | ${item.chapter.toUpperCase().replace('_', ' ')} | WenYi Lee</div>`,
        footerTemplate: '<div style="font:9px Arial;color:#52646b;text-align:center;width:100%"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
        tagged: true, outline: true});
      await page.close();
    }
  } finally {await browser.close();}
})().catch(error => {console.error(error); process.exitCode = 1;});
