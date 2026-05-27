# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0 -- 2026-05-27

Initial release of `mailchimp-claude-skills`. Ships the `mailchimp-template-language` skill — a brand-neutral toolkit for authoring custom-coded responsive Mailchimp email templates with full MCTL support.

The skill provides the correctness floor (responsive scaffolding, Outlook hardening, accessibility, compliance tags, valid MCTL placement) so prompts can focus on brand, design, and structure. Templates produced via this skill pass the included validator, render across the major email clients, and meet WCAG 2.1 AA contrast targets when the brand palette is supplied.

### Skills

- **`mailchimp-template-language`** — Custom-coded MCTL template authoring. Covers `mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, merge tags, conditional blocks, the responsive table scaffold, Outlook hardening, dark mode, accessibility, CSS inlining workflow.

  - **9 reference files** loading on demand: `structure.md`, `mc-attributes.md`, `merge-tags.md`, `responsive.md`, `patterns.md`, `typography.md`, `blueprints.md`, `accessibility.md`, `inliner.md`.
  - **Pattern library** (`patterns.md`) — 10 brand-neutral structural patterns: section openers, repeatable card grids with hideable filler, multi-column footer with social row, contact / signature blocks, image-text alternating rows, pull quotes, stat / counter rows, divider variants, button variants (solid / ghost / underline / full-width-mobile), stacked feature lists.
  - **Five archetype blueprints** (`blueprints.md`) — newsletter, promotional, transactional, announcement, re-engagement. Each defines section order, `mc:edit` taxonomy, recommended repeatable / hideable placement, archetype-specific pitfalls.
  - **Typography token system** (`typography.md`) — color and font slot vocabulary, type-scale shape by role, line-height ratios, letter-spacing semantics, web-font loading via MSO conditional, multi-script character coverage (extended Latin, Cyrillic, Greek, CJK, Arabic/Hebrew RTL, Indic).
  - **Accessibility section** (`accessibility.md`) — WCAG 2.1 AA contrast targets, alt-text patterns (decorative vs informative), `lang` attribute with region-specific codes, semantic heading order, `role="presentation"`, link text, touch targets, RTL handling.
  - **Brand-neutral skeleton** (`assets/skeleton.html`) — XHTML 1.0 Transitional doctype, full MSO conditionals, three-table responsive scaffold, dark-mode media query, bulletproof button (VML + non-MSO), repeatable card grid with hideable promo row, compliance-correct footer. Uses `#3b82f6` placeholder accent that's clearly meant to be replaced.
  - **Pre-upload validator** (`scripts/validate.py`, Python 3, stdlib only) — catches the structural mistakes that silently break Mailchimp imports: `mc:edit` on inline elements, `mc:edit` on `<table>`, duplicate `mc:edit` names, nested `mc:edit` regions, `mc:repeatable` on `<td>` (should be `<tr>` or `<table>`), missing required compliance tags (`*|UNSUB|*`, `*|LIST:ADDRESS|*` or `*|HTML:LIST:ADDRESS_HTML|*`), missing `*|MC_PREVIEW_TEXT|*`, missing doctype, missing viewport meta, images without `width`/`height`, HTML over Gmail's 102 KB clipping threshold. Exits 0 clean / 1 issues / 2 file not found; `--strict` promotes warnings to errors for CI.

### Verified against Mailchimp documentation

The following factual claims have been verified against Mailchimp's live help docs (May 2026):

- Conditional merge-tag operators `=`, `!=`, `<`, `>`, `<=`, `>=` are all supported (number-type fields recommended for numeric comparisons).
- `IFNOT` is the documented inverse-condition form.
- No boolean AND/OR inside a single IF — chain with `*|ELSEIF:|*` or nest.
- `mc:hideable` is officially a valueless attribute per `templates.mailchimp.com`; the named form (`mc:hideable="filler"`) is community convention that works in production.
- UTF-8 character encoding required; `*|UNSUB|*` required in every campaign; JPG/PNG/GIF for images; ZIP imports under 1MB with no subfolders.

### Documentation

- Repository `README.md` with worked-example prompt covering brand basics, palette, typography, structure, and what the skill brings without prompting.
- Skill `README.md` with folder layout, install instructions per platform, usage examples, validator reference, composition with other tools.
- `install.sh` / `uninstall.sh` — symlink-based install into `~/.claude/skills/`. Detects any directory containing `SKILL.md` so adding new skills to the repo doesn't require updating the installer.
- `bin/release.sh` — version-bump script that updates the manifest sites and stamps the CHANGELOG; companion `.github/workflows/release-validation.yml` validates the pushed tag matches the manifests and publishes a GitHub Release.
- Roadmap with planned skills: `mailchimp-multilingual` (single-list-multilingual *and* multi-market-global-brand patterns), `mailchimp-rss-driven`, `mailchimp-product-feed`, `mailchimp-transactional-handlebars`.
