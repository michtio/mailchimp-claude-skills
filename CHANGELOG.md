# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0 -- 2026-05-27

Initial release of `mailchimp-claude-skills`. Ships two brand-neutral skills, two agents, and supporting infrastructure for authoring custom-coded Mailchimp email templates and orchestrating multilingual campaigns.

Templates produced via these skills pass the included structural validator, target the major email clients, and meet WCAG 2.2 AA targets (contrast, target size, link semantics) when the brand palette is supplied. The bundled skeleton ships with WCAG 2.2 AA-clean defaults (`#2563eb` placeholder accent, `#595959` footer/link text) so brands forking it inherit a known-good baseline.

### Skills

- **`mailchimp-template-language`** — Custom-coded MCTL template authoring. Covers `mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, merge tags, conditional blocks, the responsive table scaffold, Outlook hardening, dark mode, accessibility, CSS inlining workflow.

  - **9 reference files** loading on demand: `structure.md`, `mc-attributes.md`, `merge-tags.md`, `responsive.md`, `patterns.md`, `typography.md`, `blueprints.md`, `accessibility.md`, `inliner.md`.
  - **Pattern library** (`patterns.md`) — 10 brand-neutral structural patterns: section openers, repeatable card grids with hideable filler, multi-column footer with social row, contact / signature blocks, image-text alternating rows, pull quotes, stat / counter rows, divider variants, button variants (solid / ghost / underline / full-width-mobile), stacked feature lists.
  - **Five archetype blueprints** (`blueprints.md`) — newsletter, promotional, transactional, announcement, re-engagement. Each defines section order, `mc:edit` taxonomy, recommended repeatable / hideable placement, archetype-specific pitfalls.
  - **Typography token system** (`typography.md`) — color and font slot vocabulary, type-scale shape by role, line-height ratios, letter-spacing semantics, web-font loading via MSO conditional, multi-script character coverage (extended Latin, Cyrillic, Greek, CJK, Arabic/Hebrew RTL, Indic).
  - **Accessibility section** (`accessibility.md`) — WCAG 2.2 AA targets including contrast (1.4.3 / 1.4.11), target size minimum (2.5.8, new in 2.2), alt-text patterns (decorative vs informative), `lang` attribute with region-specific codes, semantic heading order, `role="presentation"` (and `role="none"` synonym), link text, touch targets, RTL handling.
  - **Brand-neutral skeleton** (`assets/skeleton.html`) — XHTML 1.0 Transitional doctype, full MSO conditionals, three-table responsive scaffold, dark-mode media query, bulletproof button (VML + non-MSO), repeatable card grid with hideable promo row, compliance-correct footer. WCAG 2.2 AA-clean defaults: `#2563eb` placeholder accent (5.17:1 on white — passes 4.5:1 at all weights) and `#595959` footer/link text (6.4–7.0:1 on white/`#fafafa`).
  - **Pre-upload validator** (`scripts/validate.py`, Python 3, stdlib only) — catches the structural mistakes that silently break Mailchimp imports: `mc:edit` on text-level inline elements (`<img>` excluded per Mailchimp's documented exception), `mc:edit` on `<table>`, duplicate `mc:edit` names, nested `mc:edit` regions, `mc:repeatable` on list elements or other unusual placements, missing required compliance tags (`*|UNSUB|*`, `*|LIST:ADDRESS|*` or `*|HTML:LIST_ADDRESS_HTML|*` — underscore between LIST and ADDRESS), missing `*|MC_PREVIEW_TEXT|*`, missing doctype, missing viewport meta, images without `width`/`height`, HTML over Gmail's ~102 KB web clipping threshold. Exits 0 clean / 1 issues / 2 file not found; `--strict` promotes warnings to errors for CI.

- **`mailchimp-multilingual`** — Campaign- and audience-level patterns for sending multilingual emails. Composes with `mailchimp-template-language` for the underlying HTML; sibling skill, not a replacement.

  - **4 reference files** loading on demand: `language-detection.md`, `conditional-content.md`, `segments-vs-conditional.md`, `multi-market.md`.
  - **Single-list-multilingual** (one audience, multiple languages — Belgian / Swiss / Canadian / Singaporean case) as the primary focus. Covers the `MC_LANGUAGE` field (capture paths, full accepted ISO code list, locale-variant gotchas like `de_CH` / `it_CH` / `rm` / `zh_Hant` collapsing to base codes, the `"Not yet detected"` default), `*|IF:MC_LANGUAGE=xx|*` conditional-content patterns (per-language hero / CTA / preheader / compliance footer with regional worked examples), and the decision tree across Mailchimp's three documented multilingual paths (segments + separate campaigns, single conditional campaign, `*|TRANSLATE:xx|*` link).
  - **Multi-market-global-brand** (separate audiences per market) as a lighter orientation reference — account topology choices, template syndication / forking workflow, per-market regulatory footers (CAN-SPAM, GDPR, CASL, LGPD, Spam Act, plus jurisdiction specifics for BE/FR/DE/UK/CA/BR/AU), sync strategies, scope boundary acknowledgments.

### Agents

- **`mailchimp-template-reviewer`** (Sonnet, read-only) — qualitative review companion to the structural validator. Reports findings by severity (Critical / High / Medium / Low) across five areas: accessibility content quality (alt text, link text, palette contrast on actual pairs), cross-client risk patterns (VML correctness, `mso-padding-alt` scoping, dark-mode mitigation), multilingual completeness (parallel branches across language versions, `lang` attrs match content, localized compliance), brand consistency (palette adherence, type-scale discipline), regional compliance. Doesn't edit. Verified against the bundled skeleton through three review loops (final iteration: contrast clean across all weight classes).

- **`mailchimp-template-builder`** (Opus) — production-quality template builder with layered build-verify gates (scaffold → hero → body → CTA → footer → final validator pass). Mandatory todo list for plans over 3 steps. Earns its keep on multi-template parallel orchestration (NL/FR/DE/EN versions, multi-market forks, multilingual splits) where structural parity across files matters — builds the canonical version first, then forks to avoid drift.

### Infrastructure

- `install.sh` / `uninstall.sh` — symlink-based install of skills into `~/.claude/skills/` and agents into `~/.claude/agents/`. Detects any top-level directory containing `SKILL.md` plus any `agents/*.md` file, so adding new skills or agents to the repo doesn't require updating the installer. Sandbox-tested with a clean install + uninstall round-trip.
- `bin/release.sh` — version-bump script that updates the manifest sites (`plugin.json`, `marketplace.json`) and stamps the CHANGELOG date for the matching version heading. Companion `.github/workflows/release-validation.yml` validates the pushed tag matches the manifests, runs the validator against the bundled skeleton in `--strict` mode, and publishes a GitHub Release with the matching CHANGELOG section as release notes.

### Verified against Mailchimp documentation

The following factual claims have been verified against Mailchimp's live help docs and `templates.mailchimp.com` (May 2026):

- Conditional merge-tag operators `=`, `!=`, `<`, `>`, `<=`, `>=` are all supported (number-type fields recommended for numeric comparisons — Mailchimp's docs note text-field comparisons may not behave as expected).
- `IFNOT` is the documented inverse-condition form; closes with the same `*|END:IF|*`.
- No boolean AND/OR inside a single IF — chain with `*|ELSEIF:|*` or nest.
- `mc:hideable` is officially a valueless attribute per `templates.mailchimp.com`; the named form (`mc:hideable="filler"`) is community convention that works in production but isn't in Mailchimp's docs.
- `mc:edit` placement: container elements (div / table cell / "any other element that can be considered a container") plus the documented inline exception for `<img>`.
- `mc:repeatable` placement: block-level elements like `<div>` and `<p>` (plus `<tr>` and `<table>` for table-based email layouts) and certain inline elements (`<img>`, `<a>`, `<span>`); list elements (`<ul>`, `<ol>`, `<li>`) are explicitly excluded.
- Physical-address compliance tag is `*|HTML:LIST_ADDRESS_HTML|*` (underscore between LIST and ADDRESS) per Mailchimp's merge-tag cheat sheet.
- "View in browser" URL is `*|ARCHIVE|*`; Mailchimp does not document a `*|MC:URL|*` tag.
- `*|TRANSLATE:XX|*` is a single tag that emits a Google Translate URL for the campaign archive; it is **not** a block wrapper.
- `*|MC_LANGUAGE|*` returns an ISO 639-1 code from a closed accepted set (50 codes plus locale variants `fr_CA`, `pt_PT`, `es_ES`); `*|MC_LANGUAGE_LABEL|*` returns the English name. Several BCP 47 variants (`de_CH`, `it_CH`, `rm`, `zh_Hant`, English/German locale variants beyond US/Brazil) are not accepted and collapse to the base code.
- Mailchimp explicitly states *"It's not possible to translate the subject line of your email."* — per-language subject lines require the segments + separate campaigns path.
- Mailchimp's CSS Inliner is opt-in (per-campaign checkbox in "Code your own"), not automatic.

### Documentation

- Repository `README.md` with Quick Start (install, describe template, validate & ship), Example Prompts spanning all major archetypes, What's Inside (Skills + Agents tables), Composition guidance, Installation methods, Requirements, and Roadmap (`mailchimp-rss-driven`, `mailchimp-transactional-handlebars`, `mailchimp-ecommerce`).
- Per-skill `README.md` with folder layout, install instructions per platform, usage examples, composition with sibling tools.
