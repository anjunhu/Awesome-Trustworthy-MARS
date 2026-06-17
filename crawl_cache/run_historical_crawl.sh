#!/usr/bin/env bash
# Run arXiv crawler for each LoA tier and each year 2020-2026.
# --no-dedup ensures papers already in papers.json are NOT excluded from counts.
# --save-raw + --dry-run: write raw JSON but don't modify papers.json.
#
# Output files (per-tier, per-year):
#   crawl_cache/loa1_YYYY_raw.json  — Pre-LLM+ICL adversarial RecSys/IR (broad)
#   crawl_cache/loa2_YYYY_raw.json  — Single-agent LLM systems (broad)
#   crawl_cache/loa3_YYYY_raw.json  — Multi-agent LLM systems (broad)
#
# panel (b) = all is_relevant=True in raw JSON
# panel (a) = RecSys+IR subset, computed by compile_crawl_cache.py
#
# Run from the repo root: bash crawl_cache/run_historical_crawl.sh [loa1|loa2|loa3|all]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$SCRIPT_DIR/.."

TARGET="${1:-all}"
years=(2020 2021 2022 2023 2024 2025 2026)

run_loa() {
    local loa="$1"
    case "$loa" in
        1) flag="--classical" ;;
        2) flag="--loa2"      ;;
        3) flag="--loa3"      ;;
    esac

    for year in "${years[@]}"; do
        from="${year}0101"
        if [[ "$year" == "2026" ]]; then
            to="20260615"
        else
            to="${year}1231"
        fi
        out="$SCRIPT_DIR/loa${loa}_${year}_raw.json"

        echo ""
        echo "========================================"
        echo "  LoA-${loa}  |  $year  ($from → $to)"
        echo "========================================"
        python3 "$REPO/crawler.py" \
            $flag \
            --from "$from" \
            --to   "$to" \
            --save-raw "$out" \
            --no-dedup \
            --dry-run
        echo "  Saved: $out"
    done
}

if [[ "$TARGET" == "all" ]]; then
    for loa in 1 2 3; do run_loa "$loa"; done
else
    run_loa "${TARGET#loa}"
fi

echo ""
echo "Crawl done. Running compile step..."
python3 "$SCRIPT_DIR/compile_crawl_cache.py"
echo "Done."
