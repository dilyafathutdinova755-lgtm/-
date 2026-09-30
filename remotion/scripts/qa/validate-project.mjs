import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// This script lives in remotion/scripts/qa/.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const publicDir = path.join(root, "public");

function check(condition, message) {
  if (!condition) throw new Error(message);
}

function requireFile(relativePath) {
  const fullPath = path.join(root, relativePath);
  check(fs.existsSync(fullPath), `Missing file: ${relativePath}`);
  const stat = fs.statSync(fullPath);
  check(stat.isFile() && stat.size > 0, `Empty or invalid file: ${relativePath}`);
  return fullPath;
}

function readJson(relativePath) {
  const fullPath = requireFile(relativePath);
  try {
    return JSON.parse(fs.readFileSync(fullPath, "utf8"));
  } catch (error) {
    throw new Error(`Invalid JSON in ${relativePath}: ${error.message}`);
  }
}

const isObject = (value) =>
  value !== null && typeof value === "object" && !Array.isArray(value);
const isNumber = (value) => typeof value === "number" && Number.isFinite(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;

try {
  for (const file of [
    "src/index.ts", "src/index.css", "src/Root.tsx", "src/Composition.tsx",
    "src/VideoBackground.tsx", "src/StockCutaway.tsx", "src/IntroTitle.tsx",
    "src/KeyCard.tsx", "src/RunningCaption.tsx", "src/AppIcon.tsx",
    "src/brand.ts", "src/fonts.ts", "tsconfig.json", "remotion.config.ts",
    "public/GolosText-Black.ttf", "public/PTSansNarrow-Bold.ttf", "public/app-icon.png",
  ]) {
    requireFile(file);
  }
  readJson("package.json");
  readJson("package-lock.json");

  const duration = readJson("src/data/duration.json");
  check(isObject(duration), "duration.json must be an object");
  const total = duration.total_duration;
  check(isNumber(total) && total > 0, "total_duration must be a positive number");

  function interval(item, label, allowZero = false) {
    check(isObject(item), `${label}: expected an object`);
    check(isNumber(item.start) && isNumber(item.end), `${label}: invalid start/end`);
    check(item.start >= 0, `${label}: start cannot be negative`);
    check(allowZero ? item.end >= item.start : item.end > item.start,
      `${label}: end must follow start`);
    check(item.end <= total + 0.000001, `${label}: end exceeds total_duration`);
  }

  function readArray(name, nonEmpty = false) {
    const value = readJson(`src/data/${name}`);
    check(Array.isArray(value), `${name} must be an array`);
    check(!nonEmpty || value.length > 0, `${name} must not be empty`);
    return value;
  }

  const words = readArray("words.json", true);
  words.forEach((item, i) => {
    // The actual ASR data contains words where start === end.
    interval(item, `words[${i}]`, true);
    check(isText(item.text), `words[${i}]: text must be a non-empty string`);
  });

  const captions = readArray("running_caption.json");
  captions.forEach((item, i) => {
    interval(item, `running_caption[${i}]`, true);
    check(isText(item.text), `running_caption[${i}]: invalid text`);
  });

  const intro = readJson("src/data/intro.json");
  check(isObject(intro), "intro.json must be an object");
  check(Array.isArray(intro.lines) && intro.lines.length > 0 && intro.lines.every(isText),
    "intro.json: lines must contain non-empty strings");
  check(isNumber(intro.end) && intro.end > 0 && intro.end <= total,
    "intro.json: invalid end");

  const cards = readArray("cards.json");
  cards.forEach((item, i) => {
    interval(item, `cards[${i}]`);
    check(Array.isArray(item.lines) && item.lines.length > 0,
      `cards[${i}]: lines must not be empty`);
    item.lines.forEach((line, j) => {
      const label = `cards[${i}].lines[${j}]`;
      check(isObject(line) && isText(line.text), `${label}: invalid text`);
      check(typeof line.accent === "boolean", `${label}: accent must be boolean`);
      check(line.size === "big" || line.size === "small", `${label}: invalid size`);
    });
  });

  const emphasis = readArray("emphasis.json");
  emphasis.forEach((item, i) => interval(item, `emphasis[${i}]`));

  const stock = readArray("stock_cutaways.json");
  stock.forEach((item, i) => {
    const label = `stock_cutaways[${i}]`;
    interval(item, label);
    check(isText(item.file), `${label}: file must be a non-empty string`);
    check(!path.isAbsolute(item.file), `${label}: file must be relative to public/`);
    const resolved = path.resolve(publicDir, item.file);
    const relative = path.relative(publicDir, resolved);
    check(relative !== "" && relative !== ".." &&
      !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative),
      `${label}: file must stay inside public/`);
    requireFile(path.join("public", relative));
    check(item.sourceStart === undefined ||
      (isNumber(item.sourceStart) && item.sourceStart >= 0),
      `${label}: invalid sourceStart`);
  });

  // source.mp4 is intentionally absent from Git; preview.sh creates it.
  // audio.wav is also replaced by synthetic audio in the separate QA preview.
  console.log(`Project validation passed: duration=${total}s, words=${words.length}, ` +
    `captions=${captions.length}, cards=${cards.length}, stock=${stock.length}`);
  console.log("QA media is generated by preview.sh. Production video/audio is not checked here.");
} catch (error) {
  console.error(`ERROR: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
}
