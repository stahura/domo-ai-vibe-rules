#!/usr/bin/env bash
# Check 2.3: Validate routing table in core-custom-apps-rule.md
# - Every routed skill name maps to an actual skill in the repo
# - Reports unrouted skills (exist but not in routing table) as warnings
set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
WARNINGS=0

RULES_FILE="$REPO_ROOT/rules/core-custom-apps-rule.md"

if [[ ! -f "$RULES_FILE" ]]; then
  echo "FAIL  rules/core-custom-apps-rule.md not found"
  exit 1
fi

# Extract all skill names from frontmatter across the repo
ACTUAL_SKILLS=""
while IFS= read -r skill_file; do
  fm_name="$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_file" | sed -n 's/^name:[[:space:]]*//p' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')"
  if [[ -n "$fm_name" ]]; then
    ACTUAL_SKILLS="$ACTUAL_SKILLS$fm_name"$'\n'
  fi
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f)

# Extract routed skill names from the routing table
# Pattern: `~/.agents/skills/{name}/SKILL.md`
ROUTED_SKILLS="$(grep '~/.agents/skills/' "$RULES_FILE" | sed 's|.*~/.agents/skills/||' | sed 's|/SKILL\.md.*||' | sed 's|`.*||' | sort -u)"

echo "--- Checking routing table for phantom entries ---"
while IFS= read -r routed; do
  [[ -z "$routed" ]] && continue
  if ! echo "$ACTUAL_SKILLS" | grep -qx "$routed"; then
    echo "FAIL  Routing table references '$routed' but no skill with this name exists"
    ((ERRORS++))
  fi
done <<< "$ROUTED_SKILLS"

echo ""
echo "--- Checking for unrouted skills ---"
while IFS= read -r actual; do
  [[ -z "$actual" ]] && continue
  if ! echo "$ROUTED_SKILLS" | grep -qx "$actual"; then
    echo "WARN  Skill '$actual' exists but is not in the routing table"
    ((WARNINGS++))
  fi
done <<< "$(echo "$ACTUAL_SKILLS" | sort -u)"

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "check-routing-table: PASS ($WARNINGS warnings)"
  exit 0
else
  echo "check-routing-table: FAIL ($ERRORS phantom entries, $WARNINGS unrouted skills)"
  exit 1
fi
