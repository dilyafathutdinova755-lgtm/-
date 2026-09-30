import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

const requiredFiles = [
  "package.json",
  "package-lock.json",
  "src/index.ts",
  "src/Root.tsx",
  "src/Composition.tsx",
  "public/source.mp4",
  "public/audio.wav",
];

const requiredDataFiles = [
  "src/data/words.json",
  "src/data/cards.json",
  "src/data/duration.json",
  "src/data/title.json",
  "src/data/zooms.json",
  "src/data/stock_insert.json",
  "src/data/stock_videos.json",
];

const fail = (message) => {
  console.error(`ERROR: ${message}`);
  process.exitCode = 1;
};

for (const relativePath of requiredFiles) {
  const fullPath = path.join(root, relativePath);

  if (!fs.existsSync(fullPath)) {
    fail(`Required file is missing: ${relativePath}`);
  }
}

for (const relativePath of requiredDataFiles) {
  const fullPath = path.join(root, relativePath);

  if (!fs.existsSync(fullPath)) {
    fail(`Required data file is missing: ${relativePath}`);
    continue;
  }

  try {
    const raw = fs.readFileSync(fullPath, "utf8");
    JSON.parse(raw);
  } catch (error) {
    fail(`Invalid JSON in ${relativePath}: ${error.message}`);
  }
}

if (process.exitCode) {
  process.exit(process.exitCode);
}

console.log("Project structure and JSON data validation passed.");
