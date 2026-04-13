#!/usr/bin/env bash
# Check 1.1: Validate YAML frontmatter in every SKILL.md
# - Has --- delimiters
# - Contains name: and description: fields
# - name: matches parent directory name (with allowlist for known exceptions)
set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
WARNINGS=0

# Known exceptions: directory name=expected frontmatter name (one per line)
EXCEPTIONS="filesets=fileset-cli"

get_exception() {
  echo "$EXCEPTIONS" | grep "^$1=" | cut -d= -f2 || true
}

while IFS= read -r skill_file; do
  rel_path="${skill_file#"$REPO_ROOT/"}"
  # Parent directory name is the skill name
  dir_name="$(basename "$(dirname "$skill_file")")"

  # Check line 1 is ---
  first_line="$(head -1 "$skill_file")"
  if [[ "$first_line" != "---" ]]; then
    echo "FAIL  $rel_path: Missing opening --- (line 1 is: '$first_line')"
    ((ERRORS++))
    continue
  fi

  # Extract frontmatter (between first and second ---)
  frontmatter="$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_file")"

  if [[ -z "$frontmatter" ]]; then
    echo "FAIL  $rel_path: Empty or missing frontmatter block"
    ((ERRORS++))
    continue
  fi

  # Check closing ---
  has_closing="$(awk 'NR==1{next} /^---$/{print "yes"; exit}' "$skill_file")"
  if [[ "$has_closing" != "yes" ]]; then
    echo "FAIL  $rel_path: Missing closing --- delimiter"
    ((ERRORS++))
    continue
  fi

  # Check for blank lines inside frontmatter (causes YAML parse issues)
  blank_lines="$(echo "$frontmatter" | grep -c '^$' || true)"
  if [[ "$blank_lines" -gt 0 ]]; then
    echo "FAIL  $rel_path: Blank lines inside frontmatter block (found $blank_lines)"
    ((ERRORS++))
  fi

  # Extract name field (compatible with macOS and Linux grep)
  fm_name="$(echo "$frontmatter" | sed -n 's/^name:[[:space:]]*//p' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')"
  if [[ -z "$fm_name" ]]; then
    echo "FAIL  $rel_path: Missing 'name:' field in frontmatter"
    ((ERRORS++))
    continue
  fi

  # Extract description field
  fm_desc="$(echo "$frontmatter" | sed -n 's/^description:[[:space:]]*//p' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')"
  if [[ -z "$fm_desc" ]]; then
    echo "FAIL  $rel_path: Missing 'description:' field in frontmatter"
    ((ERRORS++))
    continue
  fi

  # Check name matches directory
  expected_name="$dir_name"
  exception="$(get_exception "$dir_name")"
  if [[ -n "$exception" ]]; then
    expected_name="$exception"
  fi

  if [[ "$fm_name" != "$expected_name" ]]; then
    if [[ -n "$exception" ]]; then
      echo "WARN  $rel_path: name '$fm_name' != dir '$dir_name' (allowlisted -> '$expected_name')"
      ((WARNINGS++))
    else
      echo "FAIL  $rel_path: name '$fm_name' does not match directory '$dir_name'"
      ((ERRORS++))
    fi
  fi

done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f | sort)

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "check-frontmatter: PASS ($WARNINGS warnings)"
  exit 0
else
  echo "check-frontmatter: FAIL ($ERRORS errors, $WARNINGS warnings)"
  exit 1
fi
