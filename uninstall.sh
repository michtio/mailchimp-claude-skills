#!/usr/bin/env bash
#
# Mailchimp Claude Skills — Uninstaller
#
# Removes symlinks created by install.sh from ~/.claude/skills/ and
# ~/.claude/agents/. Only removes symlinks that point back to this repository
# — manually created files are never touched.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo ""
echo "Mailchimp Claude Skills — Uninstaller"
echo "======================================"
echo ""

removed=0
skipped=0

echo "Skills:"
for skill_dir in "${SCRIPT_DIR}/"*/; do
    [ -d "${skill_dir}" ] || continue
    [ -f "${skill_dir}SKILL.md" ] || continue

    skill_name="$(basename "${skill_dir}")"
    target="${SKILLS_DIR}/${skill_name}"
    source="${skill_dir%/}"

    if [ -L "${target}" ] && [ "$(readlink "${target}")" = "${source}" ]; then
        rm "${target}"
        echo -e "  ${GREEN}✓ Removed ${skill_name}${NC}"
        ((removed++))
    elif [ -e "${target}" ]; then
        echo -e "  ${YELLOW}⚠ ${skill_name}${NC} — not a symlink to this repo, skipping"
        ((skipped++))
    fi
done

if [ -d "${SCRIPT_DIR}/agents" ]; then
    echo ""
    echo "Agents:"
    for agent_file in "${SCRIPT_DIR}/agents/"*.md; do
        [ -f "${agent_file}" ] || continue

        agent_name="$(basename "${agent_file}")"
        target="${AGENTS_DIR}/${agent_name}"

        if [ -L "${target}" ] && [ "$(readlink "${target}")" = "${agent_file}" ]; then
            rm "${target}"
            echo -e "  ${GREEN}✓ Removed ${agent_name%.md}${NC}"
            ((removed++))
        elif [ -e "${target}" ]; then
            echo -e "  ${YELLOW}⚠ ${agent_name%.md}${NC} — not a symlink to this repo, skipping"
            ((skipped++))
        fi
    done
fi

echo ""
echo "======================================"
echo -e "  ${GREEN}Removed:${NC} ${removed}"
echo -e "  ${YELLOW}Skipped:${NC} ${skipped}"
echo ""
echo "Done. Symlinks have been removed."
echo "The repository at ${SCRIPT_DIR} has not been deleted."
