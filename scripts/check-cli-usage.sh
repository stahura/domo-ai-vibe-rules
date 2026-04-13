#!/usr/bin/env bash
# Check 2.2: Enforce CLI boundary -- no `domo` followed by Product API subcommands
# Only community-domo-cli should be used for API operations.
# Allowed: domo login, domo dev, domo publish, domo.get(), domo.post(), etc.
set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

# Product API subcommands that should ONLY follow community-domo-cli, never domo
API_SUBCOMMANDS="datasets\?|appdb|app-studio|cards|pages|filesets\?|code-engine|workflows\?|dataflows\?|beast-modes\?|variables\?|users\?|pdp|domoapps|files"

# Scan all SKILL.md files for the anti-pattern within code blocks
while IFS= read -r skill_file; do
  rel_path="${skill_file#"$REPO_ROOT/"}"
  in_code_block=false

  while IFS= read -r line; do
    lineno="$(echo "$line" | cut -d: -f1)"
    content="$(echo "$line" | cut -d: -f2-)"

    # Track code block state
    if echo "$content" | grep -q '^```'; then
      if $in_code_block; then
        in_code_block=false
      else
        in_code_block=true
      fi
      continue
    fi

    # Only check inside code blocks (where CLI commands live)
    if $in_code_block; then
      # Check for: domo <api-subcommand> (but not community-domo-cli or domo.method())
      if echo "$content" | grep -qE "\bdomo ($API_SUBCOMMANDS) "; then
        # Exclude if it's actually community-domo-cli
        if ! echo "$content" | grep -q "community-domo-cli"; then
          echo "FAIL  $rel_path:$lineno: Code block uses 'domo' with API subcommand (should be 'community-domo-cli')"
          echo "       $content"
          ((ERRORS++))
        fi
      fi
    fi
  done < <(grep -n '' "$skill_file")

done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -type f | sort)

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "check-cli-usage: PASS"
  exit 0
else
  echo "check-cli-usage: FAIL ($ERRORS violations)"
  exit 1
fi
