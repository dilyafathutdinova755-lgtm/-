#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPO_DIR="$(cd "$PROJECT_DIR/.." && pwd)"
cd "$PROJECT_DIR"
mkdir -p out/qa

# This project uses an Ubuntu x86_64 GitHub runner.
if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "ERROR: This QA script requires Linux x86_64."
  exit 1
fi

for tool in curl tar sha256sum node npm; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "ERROR: Required tool is missing: $tool"
    exit 1
  fi
done

TOOLS_DIR="$(mktemp -d)"
trap 'rm -rf -- "$TOOLS_DIR"' EXIT

VERSION="1.7.12"
EXPECTED_SHA256="8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8"
ARCHIVE="$TOOLS_DIR/actionlint.tar.gz"

curl --fail --location --silent --show-error \
  --connect-timeout 15 --max-time 120 --retry 2 \
  "https://github.com/rhysd/actionlint/releases/download/v${VERSION}/actionlint_${VERSION}_linux_amd64.tar.gz" \
  --output "$ARCHIVE"

printf '%s  %s\n' "$EXPECTED_SHA256" "$ARCHIVE" | sha256sum --check -
tar -xzf "$ARCHIVE" -C "$TOOLS_DIR" actionlint

# Check workflow syntax and GitHub expressions.
# External ShellCheck/Pyflakes integrations are not enabled here.
LINT=("$TOOLS_DIR/actionlint" -no-color -shellcheck= -pyflakes=)
"$TOOLS_DIR/actionlint" -version

shopt -s nullglob
WORKFLOWS=(
  "$REPO_DIR"/.github/workflows/*.yml
  "$REPO_DIR"/.github/workflows/*.yaml
)
shopt -u nullglob

if (( ${#WORKFLOWS[@]} == 0 )); then
  echo "ERROR: No GitHub workflow files found."
  exit 1
fi

MONTAGE="$REPO_DIR/.github/workflows/auto-montage.yml"
if [[ ! -s "$MONTAGE" ]]; then
  echo "ERROR: auto-montage.yml is missing or empty."
  exit 1
fi

echo "1/6 Check all GitHub workflow YAML files"
(
  cd "$REPO_DIR"
  "${LINT[@]}" "${WORKFLOWS[@]}"
)
echo "Workflow YAML validation passed."

echo "2/6 Regression test: reject duplicated Auto Montage"
BROKEN="$TOOLS_DIR/duplicated-auto-montage.yml"

# Reproduce the original --clobbername: Auto Montage concatenation.
# Only a temporary file is changed, never the real workflow.
node - "$MONTAGE" "$BROKEN" <<'JS'
const fs = require('node:fs');
const [source, destination] = process.argv.slice(2);
const text = fs.readFileSync(source, 'utf8');
fs.writeFileSync(destination, text.trimEnd() + text);
JS

REGRESSION_LOG="$PROJECT_DIR/out/qa/workflow-duplicate-regression.log"
if "${LINT[@]}" "$BROKEN" > "$REGRESSION_LOG" 2>&1; then
  echo "ERROR: The checker incorrectly accepted a duplicated workflow."
  exit 1
else
  lint_status=$?
  if [[ "$lint_status" -ne 1 ]] || ! grep -qi 'duplicat' "$REGRESSION_LOG"; then
    cat "$REGRESSION_LOG"
    echo "ERROR: The test did not confirm duplicate-key detection."
    exit 1
  fi
fi

echo "Duplicate workflow regression passed: broken copy was rejected."

echo "3/6 Validate project structure and data"
node scripts/qa/validate-project.mjs

echo "4/6 Existing project lint"
npm run lint

echo "5/6 TypeScript"
./node_modules/.bin/tsc --noEmit

echo "6/6 Remotion bundle"
./node_modules/.bin/remotion bundle src/index.ts --out-dir=out/qa/bundle

echo "Avatar montage project checks passed."
