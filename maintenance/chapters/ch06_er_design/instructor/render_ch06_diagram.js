const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");
const { pathToFileURL } = require("url");


async function main() {
  const chapterDir = path.resolve(__dirname, "..");
  const input = path.join(chapterDir, "course_registration_er.svg");
  const output = path.join(chapterDir, "course_registration_er.png");
  const chromePath =
    process.env.CHROME_PATH ||
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "ch06-er-render-"));
  const result = spawnSync(
    chromePath,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-first-run",
      `--user-data-dir=${profile}`,
      "--window-size=1400,900",
      "--screenshot=course_registration_er.png",
      pathToFileURL(input).href,
    ],
    { cwd: chapterDir, encoding: "utf8" },
  );
  fs.rmSync(profile, { recursive: true, force: true });
  if (result.status !== 0 || !fs.existsSync(output)) {
    throw new Error(result.stderr || `Chrome exited with status ${result.status}`);
  }
  console.log(output);
}


main().catch((error) => {
  console.error(error);
  process.exit(1);
});
