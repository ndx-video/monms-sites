#!/usr/bin/env bash
# Advisory lint for DESIGN.md files using the upstream @google/design.md CLI.
# Does not block validation or merge — exits 0 unless a file fails lint.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
shopt -s globstar nullglob

found=0
failed=0

for file in "$ROOT"/sites/**/DESIGN.md; do
  found=1
  rel="${file#"$ROOT"/}"
  echo "lint: $rel"
  if ! npx --yes @google/design.md lint "$file"; then
    failed=1
  fi
done

if [[ "$found" -eq 0 ]]; then
  echo "lint_design_md: no DESIGN.md files under sites/"
  exit 0
fi

if [[ "$failed" -ne 0 ]]; then
  echo "lint_design_md: one or more DESIGN.md files failed lint (advisory)"
  exit 1
fi

echo "lint_design_md: OK"
