const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const root = path.join(__dirname, 'output', 'visual_review');
  const figures = JSON.parse(fs.readFileSync(path.join(root, 'figures.json'), 'utf8'));
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
    const violations = [];
    for (const figure of figures) {
      await page.goto(pathToFileURL(path.join(root, `${figure.name}.svg`)).href);
      const checks = await page.evaluate(() => {
        const svg = document.documentElement;
        const width = svg.viewBox.baseVal.width;
        const height = svg.viewBox.baseVal.height;
        const texts = [...svg.querySelectorAll('text')].map(el => ({text: el.textContent, b: el.getBBox()}));
        const errors = [];
        for (const {text, b} of texts) {
          if (b.x < 0 || b.y < 0 || b.x + b.width > width || b.y + b.height > height) errors.push(`Outside figure: ${text}`);
        }
        for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
          const a = texts[i].b, b = texts[j].b;
          if (Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>2 && Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>2) errors.push(`Overlapping text: ${texts[i].text} / ${texts[j].text}`);
        }
        return errors;
      });
      for (const error of checks) violations.push({figure: figure.name, error});
    }
    fs.writeFileSync(path.join(root, 'geometry_checks.json'), JSON.stringify(violations, null, 2));
    if (violations.length) throw new Error(JSON.stringify(violations));
    console.log('SVG_TEXT_GEOMETRY_PASS', figures.length);
    for (const chapter of [...new Set(figures.map(f => f.chapter))]) {
      await page.goto(pathToFileURL(path.join(root, `${chapter}.html`)).href);
      const images = await page.locator('img').evaluateAll(nodes => nodes.map(el => ({loaded: el.complete && el.naturalWidth > 0})));
      if (!images.length || images.some(img => !img.loaded)) throw new Error(`${chapter}: missing image`);
      for (const width of [1440, 390]) {
        await page.setViewportSize({width, height: 1100});
        const dimensions = await page.evaluate(() => ({width: innerWidth, page: document.documentElement.scrollWidth}));
        if (dimensions.page > width) throw new Error(`${chapter}: page overflow at ${width}`);
        const first = page.locator('img').first();
        await first.scrollIntoViewIfNeeded();
        await page.screenshot({path: path.join(root, `${chapter}_${width}.png`)});
      }
      console.log(chapter, 'NOTEBOOK_IMAGES_AND_VIEWPORTS_PASS', images.length);
    }
    await page.setViewportSize({width: 1920, height: 1200});
    await page.goto(pathToFileURL(path.join(root, 'gallery.html')).href);
    const count = await page.locator('figure').count();
    for (let start = 0; start < count; start += 6) {
      await page.locator('figure').evaluateAll((nodes, start) => nodes.forEach((node, i) => node.style.display = i >= start && i < start + 6 ? '' : 'none'), start);
      await page.screenshot({path: path.join(root, `gallery_${start}.png`), fullPage: true});
    }
    console.log('VISUAL_REVIEW_RENDERED');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
