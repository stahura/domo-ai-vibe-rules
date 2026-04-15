#!/usr/bin/env bash
# Local runner: execute all QA checks and report summary
set -eo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0
WARN=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

run_check() {
  local script="$1"
  local blocking="$2"
  local name="${script%.sh}"

  echo ""
  echo "========================================="
  echo "  Running: $name"
  echo "========================================="

  if bash "$SCRIPTS_DIR/$script" 2>&1; then
    echo -e "${GREEN}  => PASS${NC}"
    ((PASS++)) || true
  else
    if [[ "$blocking" == "blocking" ]]; then
      echo -e "${RED}  => FAIL (blocking)${NC}"
      ((FAIL++)) || true
    else
      echo -e "${YELLOW}  => ISSUES FOUND (advisory)${NC}"
      ((WARN++)) || true
    fi
  fi
}

echo "Domo Skills QA - Running all checks..."
echo ""

# Tier 1: Structural checks (blocking)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  TIER 1: Structure"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
run_check "check-frontmatter.sh" "blocking"
run_check "check-structure.sh" "blocking"
run_check "check-code-fences.sh" "blocking"

# Tier 2: Content integrity (mix)
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  TIER 2: Content Integrity"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
run_check "check-cross-refs.sh" "blocking"
run_check "check-cli-usage.sh" "blocking"
run_check "check-routing-table.sh" "blocking"
run_check "check-readme-sync.sh" "advisory"
run_check "check-json-blocks.sh" "advisory"

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  ${GREEN}Passed:${NC}   $PASS"
echo -e "  ${RED}Failed:${NC}   $FAIL"
echo -e "  ${YELLOW}Advisory:${NC} $WARN"
echo ""

if [[ $FAIL -gt 0 ]]; then
  echo -e "${RED}QA FAILED${NC} -- $FAIL blocking check(s) did not pass."
  exit 1
else
  echo -e "${GREEN}QA PASSED${NC} -- all blocking checks passed."
  exit 0
fi
