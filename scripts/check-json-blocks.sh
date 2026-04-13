#!/usr/bin/env bash
# Check 2.5: Validate JSON code blocks are syntactically valid (advisory)
# Skips blocks containing ..., //, or /* (intentional fragments/comments)
set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WARNINGS=0
CHECKED=0

while IFS= read -r md_file; do
  rel_path="${md_file#"$REPO_ROOT/"}"
  in_json_block=false
  json_start=0
  json_content=""

  while IFS= read -r line; do
    lineno="$(echo "$line" | cut -d: -f1)"
    content="$(echo "$line" | cut -d: -f2-)"

    if echo "$content" | grep -q '^```json'; then
      in_json_block=true
      json_start="$lineno"
      json_content=""
      continue
    fi

    if $in_json_block && echo "$content" | grep -q '^```'; then
      in_json_block=false
      ((CHECKED++))

      # Skip blocks with intentional fragments
      if echo "$json_content" | grep -qE '\.\.\.|//|/\*'; then
        continue
      fi

      # Skip empty blocks
      if [[ -z "$(echo "$json_content" | tr -d '[:space:]')" ]]; then
        continue
      fi

      # Validate JSON
      if ! echo "$json_content" | node -e "
        let d='';
        process.stdin.on('data',c=>d+=c);
        process.stdin.on('end',()=>{
          try { JSON.parse(d); process.exit(0); }
          catch(e) { console.error(e.message); process.exit(1); }
        });
      " 2>/dev/null; then
        echo "WARN  $rel_path:$json_start: Invalid JSON in code block"
        ((WARNINGS++))
      fi
      continue
    fi

    if $in_json_block; then
      json_content="$json_content"$'\n'"$content"
    fi
  done < <(grep -n '' "$md_file")

done < <(find "$REPO_ROOT/skills" "$REPO_ROOT/rules" -name "*.md" -type f | sort)

echo ""
echo "check-json-blocks: DONE (checked $CHECKED blocks, $WARNINGS invalid)"
# Always exit 0 -- this is advisory only
exit 0
