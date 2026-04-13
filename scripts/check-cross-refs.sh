#!/usr/bin/env bash
# Check 2.1: Validate cross-references between skills
# - Every ~/.agents/skills/{name}/* reference resolves to an actual skill
# - Referenced files (references/foo.py) actually exist in the source repo
# - No references use nested source-repo paths (the anti-pattern)
set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
WARNINGS=0

# Build map of all known skill names (frontmatter name -> source directory)
declare_skill_map() {
  while IFS= read -r skill_file; do
    fm_name="$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_file" | sed -n 's/^name:[[:space:]]*//p' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')"
    if [[ -n "$fm_name" ]]; then
      skill_dir="$(dirname "$skill_file")"
      echo "$fm_name|$skill_dir"
    fi
  done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f)
}

SKILL_MAP="$(declare_skill_map)"

resolve_skill_dir() {
  local name="$1"
  echo "$SKILL_MAP" | grep "^${name}|" | head -1 | cut -d'|' -f2
}

# Check 1: Validate all ~/.agents/skills/{name} references in skill files
echo "--- Checking flat path references ---"
while IFS= read -r line; do
  file="$(echo "$line" | cut -d: -f1)"
  lineno="$(echo "$line" | cut -d: -f2)"
  content="$(echo "$line" | cut -d: -f3-)"
  rel_file="${file#"$REPO_ROOT/"}"

  # Extract all skill references from this line
  # Pattern: ~/.agents/skills/{name}/... or ~/.agents/skills/{name}`
  refs="$(echo "$content" | grep -o '~/.agents/skills/[^/`'"'"' )"]*/[^ `'"'"')"]*' || true)"
  if [[ -z "$refs" ]]; then
    # Try simpler pattern for just skill name references
    refs="$(echo "$content" | grep -o '~/.agents/skills/[^/`'"'"' )"]*' || true)"
  fi

  while IFS= read -r ref; do
    [[ -z "$ref" ]] && continue
    # Extract skill name from the reference
    skill_name="$(echo "$ref" | sed 's|~/.agents/skills/||' | cut -d/ -f1)"
    [[ -z "$skill_name" ]] && continue

    # Check skill exists
    skill_dir="$(resolve_skill_dir "$skill_name")"
    if [[ -z "$skill_dir" ]]; then
      echo "FAIL  $rel_file:$lineno: References skill '$skill_name' which does not exist"
      echo "       $ref"
      ((ERRORS++))
      continue
    fi

    # If reference includes a file path beyond SKILL.md, check it exists
    ref_subpath="$(echo "$ref" | sed "s|~/.agents/skills/$skill_name/||")"
    if [[ -n "$ref_subpath" && "$ref_subpath" != "SKILL.md" && "$ref_subpath" != "$ref" ]]; then
      # Strip trailing punctuation that might have been captured
      ref_subpath="$(echo "$ref_subpath" | sed 's/[.),;]*$//')"
      target="$skill_dir/$ref_subpath"
      if [[ ! -e "$target" ]]; then
        echo "FAIL  $rel_file:$lineno: References '$ref_subpath' in skill '$skill_name' but path does not exist"
        echo "       Expected: $target"
        ((ERRORS++))
      fi
    fi
  done <<< "$refs"

done < <(grep -rn '~/.agents/skills/' "$REPO_ROOT/skills/" --include="*.md" --include="*.py" 2>/dev/null || true)

# Check 2: Flag nested source-repo path references (the anti-pattern)
echo ""
echo "--- Checking for nested source-repo path anti-patterns ---"
NESTED_CATEGORIES="cli/\|custom-apps/\|app-studio/\|themes/\|connectors/\|domo-everywhere/\|documents/\|datagen/\|orchestrator-skills/\|administration/\|transformation/\|(demo-skills)/"

while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  file="$(echo "$line" | cut -d: -f1)"
  lineno="$(echo "$line" | cut -d: -f2)"
  content="$(echo "$line" | cut -d: -f3-)"
  rel_file="${file#"$REPO_ROOT/"}"

  echo "FAIL  $rel_file:$lineno: Uses nested source-repo path (should use flat ~/.agents/skills/{name}/ format)"
  echo "       $content"
  ((ERRORS++))
done < <(grep -rn "skills/\($NESTED_CATEGORIES\)" "$REPO_ROOT/skills/" --include="*.md" --include="*.py" 2>/dev/null \
  | grep -v '^Binary' \
  | grep -v 'skills/README\.md:' \
  | grep -v 'SKILL_UPDATE_PLAN' \
  || true)

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "check-cross-refs: PASS ($WARNINGS warnings)"
  exit 0
else
  echo "check-cross-refs: FAIL ($ERRORS errors, $WARNINGS warnings)"
  exit 1
fi
