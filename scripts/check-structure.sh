#!/usr/bin/env bash
# Check 1.2: Validate directory structure invariants
# - Every skill directory (2 levels deep under skills/) has a SKILL.md
# - No unexpected deep nesting (3+ levels with SKILL.md)
# - No .DS_Store files committed
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
WARNINGS=0

# Check: every directory that looks like a skill dir has SKILL.md
# Skill dirs are 2 levels deep: skills/{category}/{skill-name}/
while IFS= read -r dir; do
  rel_dir="${dir#"$REPO_ROOT/"}"
  # Skip if this is a category dir (has subdirectories with SKILL.md)
  has_sub_skill=false
  for sub in "$dir"/*/; do
    if [[ -f "$sub/SKILL.md" ]]; then
      has_sub_skill=true
      break
    fi
  done
  if $has_sub_skill; then
    continue
  fi

  # Skip the skills/ root directory
  if [[ "$dir" == "$REPO_ROOT/skills" ]]; then
    continue
  fi

  # Skip references/ and assets/ subdirectories (expected supporting files)
  base_dir="$(basename "$dir")"
  if [[ "$base_dir" == "references" || "$base_dir" == "assets" || "$base_dir" == "themes" ]]; then
    continue
  fi

  # This looks like a leaf directory -- it should have SKILL.md
  if [[ ! -f "$dir/SKILL.md" ]]; then
    # Only flag if it contains at least one non-directory file
    file_count="$(find "$dir" -maxdepth 1 -type f | wc -l | tr -d ' ')"
    if [[ "$file_count" -gt 0 ]]; then
      echo "WARN  $rel_dir: Contains files but no SKILL.md"
      ((WARNINGS++))
    fi
  fi
done < <(find "$REPO_ROOT/skills" -mindepth 1 -type d | sort)

# Check: no SKILL.md at unexpected depths (3+ levels of skill nesting)
while IFS= read -r skill_file; do
  rel_path="${skill_file#"$REPO_ROOT/"}"
  # Count directory depth from skills/: skills/cat/skill/SKILL.md = 3 parts
  depth="$(echo "$rel_path" | tr '/' '\n' | wc -l | tr -d ' ')"
  # Expected: skills/{cat}/{skill}/SKILL.md = 4 parts
  if [[ "$depth" -gt 4 ]]; then
    echo "FAIL  $rel_path: SKILL.md nested too deep (expected skills/{category}/{skill}/SKILL.md)"
    ((ERRORS++))
  fi
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f | sort)

# Check: no .DS_Store files in the repo
ds_store_count="$(find "$REPO_ROOT" -name ".DS_Store" -not -path "*/.git/*" | wc -l | tr -d ' ')"
if [[ "$ds_store_count" -gt 0 ]]; then
  echo "WARN  Found $ds_store_count .DS_Store file(s) in repo:"
  find "$REPO_ROOT" -name ".DS_Store" -not -path "*/.git/*" | while read -r f; do
    echo "       ${f#"$REPO_ROOT/"}"
  done
  ((WARNINGS++))
fi

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "check-structure: PASS ($WARNINGS warnings)"
  exit 0
else
  echo "check-structure: FAIL ($ERRORS errors, $WARNINGS warnings)"
  exit 1
fi
