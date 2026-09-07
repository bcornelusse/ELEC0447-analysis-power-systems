#!/usr/bin/env bash
# ==============================================================================
# Script: compile_all.sh
# Description: Compiles all or selected LaTeX beamer slide decks in Lectures/
# ==============================================================================

set -u

# Ensure standard TeX paths on macOS / Linux are in PATH
export PATH="/Library/TeX/texbin:/usr/local/texlive/2023/bin/universal-darwin:/usr/local/texlive/2024/bin/universal-darwin:/usr/local/bin:/usr/bin:/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ANSI Color Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Detect TeX compiler
LATEXMK_BIN="$(command -v latexmk 2>/dev/null || true)"
PDFLATEX_BIN="$(command -v pdflatex 2>/dev/null || true)"
BIBTEX_BIN="$(command -v bibtex 2>/dev/null || true)"

# Options
USE_PDFLATEX_ONLY=false
CLEAN_AFTER=false
CLEAN_ONLY=false
VERBOSE=false

# Helper: Detect main tex file for a given deck directory
get_main_file() {
    local dir="$1"
    local dirname
    dirname="$(basename "$dir")"

    if [ -f "$dir/main.tex" ]; then
        echo "main.tex"
    elif [ -f "$dir/${dirname}.tex" ]; then
        echo "${dirname}.tex"
    else
        # Find any tex file with \documentclass[...]{beamer}
        local beamer_file
        beamer_file="$(grep -l '\\documentclass.*{beamer}' "$dir"/*.tex 2>/dev/null | head -n 1 || true)"
        if [ -n "$beamer_file" ]; then
            basename "$beamer_file"
        fi
    fi
}

# Helper: Clean auxiliary files in a deck directory
clean_aux_files() {
    local dir="$1"
    local base="$2"
    rm -f "$dir"/*.aux "$dir"/*.log "$dir"/*.nav "$dir"/*.out \
          "$dir"/*.snm "$dir"/*.toc "$dir"/*.vrb "$dir"/*.fls \
          "$dir"/*.fdb_latexmk "$dir"/*.blg 2>/dev/null || true
}

# Helper: Print usage
print_usage() {
    echo -e "${BOLD}Usage:${NC} $0 [OPTIONS] [DECK1 DECK2 ...]"
    echo ""
    echo -e "${BOLD}Options:${NC}"
    echo "  -h, --help        Show this help message and exit"
    echo "  -c, --clean       Clean auxiliary files (.aux, .log, .toc, etc.) after compilation"
    echo "  --clean-only      Clean auxiliary files without compiling"
    echo "  --pdflatex        Force using pdflatex directly instead of latexmk"
    echo "  -v, --verbose     Show full compiler output in the terminal"
    echo ""
    echo -e "${BOLD}Available slide decks in Lectures/:${NC}"
    for d in "$SCRIPT_DIR"/*/; do
        [ -d "$d" ] || continue
        deck_name="$(basename "$d")"
        main_file="$(get_main_file "$d")"
        if [ -n "$main_file" ]; then
            echo "  - $deck_name ($main_file)"
        fi
    done
    echo ""
    echo -e "${BOLD}Examples:${NC}"
    echo "  $0                      # Compile all decks"
    echo "  $0 Introduction HVDC    # Compile only Introduction and HVDC"
    echo "  $0 -c                   # Compile all and clean auxiliary files"
    echo "  $0 --clean-only         # Clean auxiliary files only"
}

# Parse Arguments
TARGET_DECKS=()
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            print_usage
            exit 0
            ;;
        -c|--clean)
            CLEAN_AFTER=true
            shift
            ;;
        --clean-only)
            CLEAN_ONLY=true
            shift
            ;;
        --pdflatex)
            USE_PDFLATEX_ONLY=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            echo -e "${RED}Error: Unknown option '$1'${NC}" >&2
            print_usage
            exit 1
            ;;
        *)
            TARGET_DECKS+=("$1")
            shift
            ;;
    esac
done

# Check compiler availability
if [ "$CLEAN_ONLY" = false ]; then
    if [ -z "$PDFLATEX_BIN" ]; then
        echo -e "${RED}Error: 'pdflatex' was not found in PATH.${NC}" >&2
        echo "Please ensure MacTeX or TeX Live is installed and available in PATH." >&2
        exit 1
    fi
fi

# Determine decks to process
ALL_DECKS=()
for d in "$SCRIPT_DIR"/*/; do
    [ -d "$d" ] || continue
    deck_name="$(basename "$d")"
    main_file="$(get_main_file "$d")"
    if [ -n "$main_file" ]; then
        ALL_DECKS+=("$deck_name")
    fi
done

DECKS_TO_RUN=()
if [ ${#TARGET_DECKS[@]} -eq 0 ]; then
    DECKS_TO_RUN=("${ALL_DECKS[@]}")
else
    for req in "${TARGET_DECKS[@]}"; do
        # Trim trailing slash if present
        req="${req%/}"
        if [ -d "$SCRIPT_DIR/$req" ]; then
            main_file="$(get_main_file "$SCRIPT_DIR/$req")"
            if [ -n "$main_file" ]; then
                DECKS_TO_RUN+=("$req")
            else
                echo -e "${YELLOW}Warning: No beamer presentation found in '$req'. Skipping.${NC}"
            fi
        else
            echo -e "${RED}Error: Directory '$SCRIPT_DIR/$req' does not exist.${NC}" >&2
            exit 1
        fi
    done
fi

# Clean-only mode
if [ "$CLEAN_ONLY" = true ]; then
    echo -e "${BLUE}${BOLD}Cleaning auxiliary files for ${#DECKS_TO_RUN[@]} deck(s)...${NC}"
    for deck in "${DECKS_TO_RUN[@]}"; do
        clean_aux_files "$SCRIPT_DIR/$deck" "$(get_main_file "$SCRIPT_DIR/$deck")"
        echo -e "  ${GREEN}✓${NC} Cleaned $deck"
    done
    echo -e "${GREEN}${BOLD}Done!${NC}"
    exit 0
fi

# Compilation mode
TOTAL=${#DECKS_TO_RUN[@]}
CURRENT=0
SUCCEEDED=()
FAILED=()

COMPILER="latexmk"
if [ "$USE_PDFLATEX_ONLY" = true ] || [ -z "$LATEXMK_BIN" ]; then
    COMPILER="pdflatex"
fi

echo -e "${BLUE}${BOLD}======================================================${NC}"
echo -e "${BLUE}${BOLD} Compiling ${TOTAL} Slide Deck(s) using ${COMPILER}${NC}"
echo -e "${BLUE}${BOLD}======================================================${NC}"

for deck in "${DECKS_TO_RUN[@]}"; do
    CURRENT=$((CURRENT + 1))
    deck_dir="$SCRIPT_DIR/$deck"
    main_file="$(get_main_file "$deck_dir")"
    base_name="${main_file%.tex}"

    printf "[%2d/%2d] Compiling %-22s (%s)... " "$CURRENT" "$TOTAL" "$deck" "$main_file"

    build_log="$deck_dir/.compile_build.log"
    compile_success=true

    if [ "$COMPILER" = "latexmk" ]; then
        if [ "$VERBOSE" = true ]; then
            echo ""
            (cd "$deck_dir" && "$LATEXMK_BIN" -pdf -interaction=nonstopmode "$main_file") || compile_success=false
        else
            (cd "$deck_dir" && "$LATEXMK_BIN" -pdf -interaction=nonstopmode "$main_file" > "$build_log" 2>&1) || compile_success=false
        fi
    else
        # Fallback to pdflatex (2 passes, running bibtex if .bib exists)
        if [ "$VERBOSE" = true ]; then
            echo ""
            (cd "$deck_dir" && "$PDFLATEX_BIN" -interaction=nonstopmode "$main_file") || compile_success=false
            if [ -f "$deck_dir/demo.bib" ] || grep -q '\\bibliography' "$deck_dir"/*.tex 2>/dev/null; then
                if [ -n "$BIBTEX_BIN" ]; then
                    (cd "$deck_dir" && "$BIBTEX_BIN" "$base_name" >/dev/null 2>&1 || true)
                fi
            fi
            (cd "$deck_dir" && "$PDFLATEX_BIN" -interaction=nonstopmode "$main_file") || compile_success=false
        else
            (cd "$deck_dir" && "$PDFLATEX_BIN" -interaction=nonstopmode "$main_file" > "$build_log" 2>&1) || compile_success=false
            if [ -f "$deck_dir/demo.bib" ] || grep -q '\\bibliography' "$deck_dir"/*.tex 2>/dev/null; then
                if [ -n "$BIBTEX_BIN" ]; then
                    (cd "$deck_dir" && "$BIBTEX_BIN" "$base_name" >> "$build_log" 2>&1 || true)
                fi
            fi
            (cd "$deck_dir" && "$PDFLATEX_BIN" -interaction=nonstopmode "$main_file" >> "$build_log" 2>&1) || compile_success=false
        fi
    fi

    if [ "$compile_success" = true ] && [ -f "$deck_dir/${base_name}.pdf" ]; then
        echo -e "${GREEN}${BOLD}SUCCESS${NC}"
        SUCCEEDED+=("$deck")
        rm -f "$build_log" 2>/dev/null || true

        if [ "$CLEAN_AFTER" = true ]; then
            clean_aux_files "$deck_dir" "$main_file"
        fi
    else
        echo -e "${RED}${BOLD}FAILED${NC}"
        FAILED+=("$deck")
        if [ -f "$build_log" ]; then
            echo -e "${RED}--- Error excerpt from $build_log ---${NC}"
            grep -E "^!|Error:" "$build_log" | head -n 10 || tail -n 15 "$build_log"
            echo -e "${RED}-----------------------------------${NC}"
        fi
    fi
done

# Final Summary
echo ""
echo -e "${BOLD}======================================================${NC}"
echo -e "${BOLD} Summary:${NC}"
echo -e "  Total:     ${TOTAL}"
echo -e "  Succeeded: ${GREEN}${#SUCCEEDED[@]}${NC}"
echo -e "  Failed:    ${RED}${#FAILED[@]}${NC}"
echo -e "${BOLD}======================================================${NC}"

if [ ${#FAILED[@]} -gt 0 ]; then
    echo -e "${RED}The following deck(s) failed to compile:${NC}"
    for f in "${FAILED[@]}"; do
        echo -e "  - $f"
    done
    exit 1
else
    echo -e "${GREEN}All slide decks compiled successfully!${NC}"
    exit 0
fi
