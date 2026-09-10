// Render the local first-meeting previews and inspect diagram geometry.
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
const { chromium } = require(process.env.PLAYWRIGHT_PATH ||
  'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const output = path.join(__dirname, 'output', 'first_meeting');
const verified = JSON.parse(fs.readFileSync(path.join(output, 'verification.json'), 'utf8'));
(async () => {
  const browser = await chromium.launch({headless: true,
    executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const results = [];
  try {
    for (const width of [1440, 390]) {
      for (const name of ['home', 'syllabus', ...verified.chapters.map(c => c.chapter)]) {
        const page = await browser.newPage({viewport: {width, height: 1000}});
        await page.goto(pathToFileURL(path.join(output, `${name}.html`)).href);
        await page.evaluate(() => Promise.all(Array.from(document.images).map(img => img.decode())));
        const check = await page.evaluate(() => ({
          pageOverflow: document.documentElement.scrollWidth > innerWidth + 1,
          images: document.images.length,
          brokenImages: Array.from(document.images).filter(img => !img.naturalWidth).length,
          overflowingText: Array.from(document.querySelectorAll('p,h1,h2,h3')).filter(el =>
            el.getBoundingClientRect().right > innerWidth + 1).length
        }));
        if (check.pageOverflow || check.brokenImages || check.overflowingText) throw new Error(JSON.stringify({name, width, ...check}));
        await page.screenshot({path: path.join(output, `${name}-${width}.png`)});
        if (name === 'syllabus' && width === 1440) {
          await page.locator('table').first().screenshot({path: path.join(output, 'syllabus-schedule.png')});
        }
        if (name.startsWith('ch')) {
          await page.locator('img').first().scrollIntoViewIfNeeded();
          await page.screenshot({path: path.join(output, `${name}-${width}-diagram.png`)});
        }
        results.push({name, width, ...check});
        if (name === 'ch08') {
          await page.getByRole('heading', {name: '2. SELECT Keeps Rows That Satisfy a Condition', exact: true}).scrollIntoViewIfNeeded();
          await page.screenshot({path: path.join(output, `ch08-${width}-notation.png`)});
        }
        if (name === 'ch03') {
          for (const [label, heading] of [
            ['weak', '12.1. Order Items: the Same Number under Different Owners'],
            ['ternary', '14.1. Section 3.9.2: Fix Two Participants before Reading a 1'],
            ['university', '16. Section 3.10: A UNIVERSITY Database']
          ]) {
            await page.getByRole('heading', {name: heading, exact: true}).scrollIntoViewIfNeeded();
            await page.screenshot({path: path.join(output, `ch03-${width}-${label}.png`)});
          }
        }
        await page.close();
      }
    }
    const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
    await page.goto(pathToFileURL(path.join(output, 'figures.html')).href);
    const geometry = await page.evaluate(() => {
      const failures = [];
      for (const svg of document.querySelectorAll('svg')) {
        const vb = svg.viewBox.baseVal;
        for (const text of svg.querySelectorAll('text')) {
          const b = text.getBBox();
          if (b.x < -1 || b.y < -1 || b.x + b.width > vb.width + 1 || b.y + b.height > vb.height + 1)
            failures.push({figure: svg.parentElement.id, text: text.textContent, type: 'outside SVG'});
        }
        for (const rect of svg.querySelectorAll('.network-node')) {
          const r = rect.getBBox();
          for (const text of svg.querySelectorAll('text')) {
            const b = text.getBBox();
            if (b.x >= r.x && b.x < r.x + r.width && b.y >= r.y && b.y < r.y + r.height &&
                (b.x + b.width > r.x + r.width + 1 || b.y + b.height > r.y + r.height + 1))
              failures.push({figure: svg.parentElement.id, text: text.textContent, type: 'outside node'});
          }
        }
        for (const group of svg.querySelectorAll('.er-node')) {
          const shape = group.querySelector('rect,ellipse,polygon');
          const text = group.querySelector('text');
          const b = text.getBBox();
          for (const [x, y] of [[b.x,b.y], [b.x+b.width,b.y],
                                [b.x,b.y+b.height], [b.x+b.width,b.y+b.height]]) {
            if (!shape.isPointInFill(new DOMPoint(x, y)))
              failures.push({figure: svg.parentElement.id, text: text.textContent, type: 'outside ER shape'});
          }
        }
        if (svg.querySelector('.er-node')) {
          const labels = Array.from(svg.querySelectorAll('text'));
          for (let i=0; i<labels.length; i++) for (let j=i+1; j<labels.length; j++) {
            const a=labels[i].getBBox(), b=labels[j].getBBox();
            if (a.x < b.x+b.width && a.x+a.width > b.x && a.y < b.y+b.height && a.y+a.height > b.y)
              failures.push({figure: svg.parentElement.id, text: labels[i].textContent,
                other: labels[j].textContent, type: 'overlapping ER labels'});
          }
        }
      }
      return failures;
    });
    if (geometry.length) throw new Error(JSON.stringify(geometry));
    for (const figure of await page.locator('.figure').all()) {
      const id = await figure.getAttribute('id');
      await figure.locator('svg').screenshot({path: path.join(output, `${id}.png`)});
    }
    await page.close();
    fs.writeFileSync(path.join(output, 'rendering.json'), JSON.stringify({previews: results, geometry}, null, 2));
    console.log(JSON.stringify({previews: results, geometry}));
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
