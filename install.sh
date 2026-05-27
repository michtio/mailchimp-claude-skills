#!/usr/bin/env bash
#
# Mailchimp Claude Skills — Installer
#
# Symlinks every skill in this repo (any directory containing a SKILL.md
# at the top level) into ~/.claude/skills/ without overwriting existing
# files. Run from the repository root: bash install.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo ""
echo "Mailchimp Claude Skills — Installer"
echo "===================================="
echo ""

mkdir -p "${SKILLS_DIR}"

linked=0
skipped=0

echo "Skills:"
for skill_dir in "${SCRIPT_DIR}/"*/; do
    [ -d "${skill_dir}" ] || continue
    [ -f "${skill_dir}SKILL.md" ] || continue

    skill_name="$(basename "${skill_dir}")"
    target="${SKILLS_DIR}/${skill_name}"

    # Strip trailing slash so the symlink target matches what uninstall.sh expects
    source="${skill_dir%/}"

    if [ -e "${target}" ] || [ -L "${target}" ]; then
        echo -e "  ${YELLOW}⚠ ${skill_name}${NC} — already exists, skipping"
        ((skipped++))
    else
        ln -s "${source}" "${target}"
        echo -e "  ${GREEN}✓ ${skill_name}${NC}"
        ((linked++))
    fi
done

echo ""
echo "===================================="
echo -e "  ${GREEN}Linked:${NC}  ${linked}"
echo -e "  ${YELLOW}Skipped:${NC} ${skipped}"
echo ""

if [ ${skipped} -gt 0 ]; then
    echo "Skipped items already exist in ~/.claude/skills/."
    echo "To force reinstall, run uninstall.sh first, then install.sh again."
    echo ""
fi

echo "Validator available at:"
echo "  ${SCRIPT_DIR}/mailchimp-template-language/scripts/validate.py"
echo ""
echo "Done."
