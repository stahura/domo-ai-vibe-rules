#!/usr/bin/env bash
# Check 1.3: Verify code fence pairs are balanced in all .md files
# Every opening ``` must have a matching closing ```
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

while IFS= read -r md_file; do
  rel_path="${md_file#"$REPO_ROOT/"}"
  # Count lines that are code fences (start with ``` possibly followed by language tag)
  fence_count="$(grep -c '^```' "$md_file" || true)"

  if [[ $((fence_count % 2)) -ne 0 ]]; then
    echo "FAIL  $rel_path: Unmatched code fences ($fence_count fence lines -- odd count)"
    # Show the fence lines with line numbers to help locate the problem
    grep -n '^```' "$md_file" | tail -5 | while read -r line; do
      echo "       $line"
    done
    ((ERRORS++))
  fi
done < <(find "$REPO_ROOT/skills" "$REPO_ROOT/rules" -name "*.md" -type f | sort)

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "check-code-fences: PASS"
  exit 0
else
  echo "check-code-fences: FAIL ($ERRORS files with unmatched fences)"
  exit 1
fi
