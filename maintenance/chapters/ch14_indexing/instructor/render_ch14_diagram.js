const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");
const { pathToFileURL } = require("url");


function main() {
  const chapterDir = path.resolve(__dirname, "..");
  const input = path.join(chapterDir, "bplus_tree_example.svg");
  const output = path.join(chapterDir, "bplus_tree_example.png");
  const chromePath =
    process.env.CHROME_PATH ||
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "ch14-index-render-"));
  const temporaryOutput = path.join(profile, "bplus_tree_example.png");
  const result = spawnSync(
    chromePath,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-first-run",
      `--user-data-dir=${profile}`,
      "--window-size=1200,620",
      `--screenshot=${temporaryOutput}`,
      pathToFileURL(input).href,
    ],
    { cwd: chapterDir, encoding: "utf8" },
  );
  if (result.status === 0 && fs.existsSync(temporaryOutput)) {
    fs.copyFileSync(temporaryOutput, output);
  }
  fs.rmSync(profile, { recursive: true, force: true });
  if (result.status !== 0 || !fs.existsSync(output)) {
    throw new Error(result.stderr || `Chrome exited with status ${result.status}`);
  }
  console.log(output);
}


try {
  main();
} catch (error) {
  console.error(error);
  process.exit(1);
}
