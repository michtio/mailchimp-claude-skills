# mailchimp-claude-skills

> [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for authoring custom-coded [Mailchimp](https://mailchimp.com/) email templates. The skill handles the correctness layer — MCTL placement, responsive tables, Outlook hardening, accessibility, compliance — so your prompt can focus on brand, content, and structure.

Built and maintained by [michtio](https://github.com/michtio) at [Bleu Chaud](https://bleuchaud.com).

## Support

If this project saves you time, consider supporting its development:

- [GitHub Sponsors](https://github.com/sponsors/michtio)
- [Buy Me a Coffee](https://buymeacoffee.com/michtio)

## Quick Start

### 1. Install

```bash
# Claude Code Plugin (recommended)
# First time: add the marketplace, then install
/plugin marketplace add michtio/mailchimp-claude-skills
/plugin install mailchimp-claude-skills@mailchimp-claude-skills

# Or clone manually
git clone https://github.com/michtio/mailchimp-claude-skills.git ~/.claude/mailchimp-claude-skills
cd ~/.claude/mailchimp-claude-skills && bash install.sh
```

`install.sh` symlinks every skill (any directory containing a `SKILL.md`) into `~/.claude/skills/`, so updates flow through with `git pull`. `bash uninstall.sh` removes the symlinks; manually-installed skills are never touched.

For Claude.ai or the Anthropic API, see [Installation methods](#installation-methods) below.

### 2. Describe Your Template

Open Claude Code in any working directory and describe what you need. Skills trigger automatically based on the prompt.

```
Build a Mailchimp newsletter template for Acme Logistics, monthly availabilities
update. Palette: foreground #1a1d2e, accent #2563eb, white background. Headings
in Manrope, body in Inter, both with Arial fallback. Sections: hero, repeatable
country blocks with 3 cards each, hideable sustainability section, footer with
address and unsubscribe. Validate before declaring done.
```

The skill loads its responsive scaffold, fills the brand inputs, places MCTL attributes correctly, hooks up compliance tags, and runs the validator.

### 3. Validate & Ship

```bash
# Validate locally before uploading
python3 mailchimp-template-language/scripts/validate.py template.html

# Exit 0 = clean, 1 = errors found, 2 = file not found
# Use --strict to fail on warnings too (CI-friendly)
```

Then paste into Mailchimp's "Code your own → Paste in code" flow, or upload programmatically via a [Mailchimp MCP server](#composition).

## Example Prompts

Just describe what you need. The skill triggers on Mailchimp / MCTL / merge-tag mentions and produces validator-clean templates.

```
Build a Mailchimp template for our quarterly product update. Single hero with
big number ("Q2 in numbers"), three stat cards (active users, exports
processed, new integrations), then a repeatable feature-highlights section,
then a compliance footer. WCAG 2.2 AA. Inter via Google Fonts with Arial
fallback.
```

```
Convert this static HTML email into a Mailchimp-editable template. Mark the
header, body, and footer as mc:edit regions. Add a repeatable card row.
The "Featured" callout should be hideable. Keep the existing styling.
```

```
Add a French-language version of this template. Copy the file, set lang to
fr-BE, translate the hero eyebrow and CTA labels, keep everything else
identical. The compliance footer copy needs to be French too.
```

```
Our current Mailchimp templates don't share mc:edit names so editors lose
content when switching templates. Audit these three templates and normalize
the editable region names so Switch Template works cleanly across them.
```

```
A subscriber reported that our last campaign's hero image is missing alt text
and the unsubscribe link is hard to find on mobile. Audit our base template
for accessibility issues — WCAG 2.2 AA — and fix what you find.
```

```
Build a re-engagement campaign template. Empathetic opener, three highlights
of what they've missed (hideable), a clear reactivation CTA, plus an explicit
soft-exit unsubscribe section with positive framing. Editorial type, no
hype.
```

## What's Inside

### Skills

| Skill | What it does |
|-------|--------------|
| `mailchimp-template-language` | Authors custom-coded responsive MCTL templates with full `mc:edit` / `mc:repeatable` / `mc:variant` / `mc:hideable` support, merge tags, conditional blocks, Outlook hardening, accessibility, and CSS inlining workflow. 9 reference files. |
| `mailchimp-multilingual` | Plans and builds multilingual campaigns — `MC_LANGUAGE` field, `IF:MC_LANGUAGE=xx` conditional content, segments-vs-conditional decision tree, multi-market template forking. Companion-loads the template-language skill for the underlying HTML. 4 reference files. |

### Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `mailchimp-template-reviewer` | Sonnet | Read-only qualitative review companion to `validate.py`. Catches what the structural validator can't: accessibility content quality (alt text content, link text, palette contrast pairs), cross-client risk patterns (VML correctness, `mso-padding-alt` scoping, dark-mode mitigation), multilingual completeness (parallel branches, `lang` attrs, localized compliance footer), brand consistency, regional compliance (CAN-SPAM / GDPR / CASL / LGPD / etc.). Reports findings by severity; doesn't edit. |
| `mailchimp-template-builder` | Opus | Builds templates feature by feature with layered build-verify gates (scaffold → hero → body → CTA → footer → final validator pass). Earns its keep on multi-template parallel orchestration — `"build NL/FR/DE/EN versions, mirrored structure"` — where structural parity across files matters. Mandatory todo list for plans over 3 steps. |

Agents compose: the builder produces, the reviewer audits, the structural validator gates. See [agents/](./agents/) for the full agent definitions.

### Reference files

Both skills use on-demand loading. The `SKILL.md` body stays small; Claude pulls in the relevant reference when the conversation needs it.

**`mailchimp-template-language/references/`** (9 files)

| Reference | Covers |
|-----------|--------|
| `structure.md` | Doctype guidance, head block, MSO conditionals, three-table body skeleton |
| `mc-attributes.md` | `mc:edit` / `mc:repeatable` / `mc:variant` / `mc:hideable` placement rules and conventional names |
| `merge-tags.md` | Merge-tag syntax (`*\|TAG\|*`), IF/ELSEIF/ELSE/IFNOT conditionals, comparison operators, required compliance tags, escape patterns |
| `responsive.md` | Fluid hybrid layout, media-query mobile rules, dark mode per client, bulletproof buttons, retina images, web-font loading |
| `typography.md` | Color and font token vocabulary, type scale by role, line-height ratios, multi-script coverage, web-font MSO pattern |
| `patterns.md` | 10 brand-neutral structural patterns: section openers, repeatable cards, multi-column footer, contact blocks, image-text rows, pull quotes, stats, dividers, button variants, feature lists |
| `blueprints.md` | 5 archetype blueprints: newsletter, promotional, transactional, announcement, re-engagement — section order, `mc:edit` taxonomy, repeatable/hideable map |
| `accessibility.md` | WCAG 2.2 AA targets (contrast, target size minimum), alt text, lang, semantic order, `role="presentation"`, link text, touch targets, RTL |
| `inliner.md` | When to pre-inline with Juice or Premailer vs rely on Mailchimp's opt-in inliner, what survives Gmail web, common pitfalls |

**`mailchimp-multilingual/references/`** (4 files)

| Reference | Covers |
|-----------|--------|
| `language-detection.md` | `MC_LANGUAGE` + `MC_LANGUAGE_LABEL`, capture paths (browser auto-detect, signup field, CSV, API), full accepted ISO code list, locale-variant gotchas (`de_CH` / `it_CH` / `rm` / `zh_Hant` collapses), `"Not yet detected"` default |
| `conditional-content.md` | `*\|IF:MC_LANGUAGE=xx\|*` patterns, per-language hero / CTA / preheader / compliance footer, worked examples for Belgian / Swiss / Canadian / Singaporean audiences |
| `segments-vs-conditional.md` | Decision tree across Mailchimp's three documented multilingual paths (segments + separate campaigns, single conditional campaign, `*\|TRANSLATE:xx\|*` link), tradeoff matrix, per-region defaults |
| `multi-market.md` | Multi-market-global-brand orientation: account topology choices, master + fork workflow, per-market regulatory footers (BE/FR/DE/UK/CA/BR/AU specifics), sync strategies, scope boundary |

### Assets and scripts

| Path | What it is |
|------|------------|
| `assets/skeleton.html` | Working brand-neutral starter: XHTML 1.0 Transitional doctype, full MSO conditionals, three-table responsive scaffold, dark-mode media query, bulletproof button (VML + non-MSO), repeatable card grid with hideable promo row, compliance-correct footer |
| `scripts/validate.py` | Pre-upload validator (Python 3.10+, stdlib only) — catches structural mistakes that silently break Mailchimp imports. Exits 0 clean / 1 issues / 2 file not found |

## Composition

This skill is the **authoring** layer. Pair it with:

- [`damientilman/mailchimp-mcp-server`](https://github.com/damientilman/mailchimp-mcp-server) — 112 tools across the Mailchimp Marketing API (campaigns, audiences, reports, segments, automations, e-commerce). Read-only and dry-run modes. `uvx mailchimp-mcp-server`.
- [Composio's hosted Mailchimp MCP](https://mcp.composio.dev/mailchimp) — OAuth alternative if you don't want to manage API keys.
- [Litmus](https://litmus.com/) / [Email on Acid](https://www.emailonacid.com/) — cross-client render testing. The skill cannot test rendering; these can.

End-to-end: Claude writes `template.html` → `validate.py` passes → Mailchimp MCP uploads via `/3.0/templates` → Litmus or Email on Acid confirms rendering → send.

## Installation methods

### Claude Code Plugin (recommended)

See [Quick Start step 1](#1-install) above.

### Manual copy / symlink

```bash
# Personal scope (all your projects)
cp -r mailchimp-template-language ~/.claude/skills/

# Or symlink during development
ln -s "$(pwd)/mailchimp-template-language" ~/.claude/skills/mailchimp-template-language

# Or project scope (committed with the client repo)
mkdir -p .claude/skills && cp -r mailchimp-template-language .claude/skills/
```

Restart your Claude Code session and the skill appears in the available skills list.

### Claude.ai

Zip the `mailchimp-template-language/` folder (the folder itself, with `SKILL.md` at root) and upload via Settings → Capabilities → Skills.

### Anthropic API

See [Anthropic's skill docs](https://docs.claude.com/en/docs/agents/skills) for the current API shape.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code), Claude.ai with Skills, or Anthropic API access
- Python 3.10+ for the validator (stdlib only — no installs)
- A Mailchimp account if you intend to upload and send the result

## Why this repo exists

Across the public Anthropic Skills ecosystem (anthropics/skills, obra/superpowers, wshobson/agents, ComposioHQ/awesome-claude-skills, and other catalogs), as of mid-2026 no skill targets Mailchimp's template language directly. Existing "Mailchimp" skills are uniformly API/MCP wrappers operating on existing templates — none help Claude *author* a custom-coded MCTL template that doesn't silently break on import.

This repo fills the gap. Templates produced via prompting + this skill pass the validator, target the major email clients, and meet WCAG 2.2 AA when the brand palette is supplied — which means brand and content become the only things to think about per project.

## Roadmap

- [ ] **`mailchimp-rss-driven`** — Templates wired for Mailchimp's RSS-to-email automations. Covers the documented merge tags: `*|RSSFEED:TITLE|*` / `*|RSSFEED:DATE|*` / `*|RSSFEED:URL|*` / `*|RSSFEED:DESCRIPTION|*` for channel-level, `*|RSSITEM:TITLE|*` / `:URL|*` / `:DATE|*` / `:AUTHOR|*` / `:CONTENT|*` / `:CONTENT_FULL|*` / `:IMAGE|*` for per-item, plus the `*|RSSITEMS:|*…*|END:RSSITEMS|*` loop block.

- [ ] **`mailchimp-transactional-handlebars`** — Separate skill for Mandrill / Mailchimp Transactional. Different syntax (Handlebars by default; MCTL configurable per account), different sending model, different deliverability concerns. Not interchangeable with the marketing-campaign skill.

- [ ] **`mailchimp-ecommerce`** *(scope under investigation)* — Mailchimp's product data integrates via the e-commerce content blocks in the new/legacy builder, not via documented merge tags. A skill here would likely focus on either (a) hand-coded product cards populated from custom merge fields synced via the Marketing API, or (b) a pattern library for the e-commerce content blocks. Whether this is a meaningful authoring surface, or whether the block editor already handles it well enough, depends on real client demand — flagged as exploratory rather than committed.

## License

MIT — see [LICENSE](./LICENSE).
