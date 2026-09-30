#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

echo "== Avatar Montage QA =="

echo "1/4 Validate project structure and data"
node scripts/qa/validate-project.mjs

echo "2/4 ESLint"
npm run lint

echo "3/4 TypeScript"
npx tsc --noEmit

echo "4/4 Remotion bundle"
npx remotion bundle src/index.ts --out-dir=out/qa/bundle

echo "Avatar montage project checks passed."
