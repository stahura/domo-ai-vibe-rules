#!/usr/bin/env bash
# Check 2.4: Verify README.md skill catalog matches actual skills (advisory)
set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WARNINGS=0

README_FILE="$REPO_ROOT/README.md"

if [[ ! -f "$README_FILE" ]]; then
  echo "WARN  README.md not found"
  exit 0
fi

# Extract all skill names from frontmatter across the repo
ACTUAL_SKILLS=""
while IFS= read -r skill_file; do
  fm_name="$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_file" | sed -n 's/^name:[[:space:]]*//p' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')"
  if [[ -n "$fm_name" ]]; then
    ACTUAL_SKILLS="$ACTUAL_SKILLS$fm_name"$'\n'
  fi
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f)
ACTUAL_SKILLS="$(echo "$ACTUAL_SKILLS" | sort -u)"

# Extract skill names mentioned in README (backtick-quoted names in skill listings)
# Pattern: `skill-name` in the context of skill tables/lists
README_SKILLS="$(grep -o '`[a-z][a-z0-9-]*`' "$README_FILE" | tr -d '`' | sort -u)"

echo "--- Skills in repo but not mentioned in README ---"
while IFS= read -r actual; do
  [[ -z "$actual" ]] && continue
  if ! echo "$README_SKILLS" | grep -qx "$actual"; then
    echo "WARN  Skill '$actual' not found in README.md"
    ((WARNINGS++))
  fi
done <<< "$ACTUAL_SKILLS"

echo ""
echo "check-readme-sync: DONE ($WARNINGS potential gaps found)"
# Always exit 0 -- this is advisory only
exit 0
