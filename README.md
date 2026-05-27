# mailchimp-claude-skills

> Anthropic Agent Skills for authoring [Mailchimp](https://mailchimp.com/) email templates from [Claude Code](https://docs.anthropic.com/en/docs/claude-code), Claude.ai, or the Anthropic API. The skills handle the boring-but-critical correctness layer — MCTL placement, responsive tables, Outlook hardening, accessibility, compliance — so prompts can focus on brand, design, and structure.

Built and maintained by [michtio](https://github.com/michtio) at [Bleu Chaud](https://bleuchaud.com).

## Support

If this project saves you time, consider supporting its development:

- [GitHub Sponsors](https://github.com/sponsors/michtio)
- [Buy Me a Coffee](https://buymeacoffee.com/michtio)

## Skills

| Skill | What it does |
|---|---|
| [`mailchimp-template-language`](./mailchimp-template-language/) | Author and edit custom-coded responsive Mailchimp templates with full MCTL support (`mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, merge tags, conditionals). Brand-neutral; includes Outlook-hardened skeleton, structural pattern library, and pre-upload validator. |

## How to use

### The pattern

Tell Claude what you want, including the brand inputs. The skill provides the correctness floor — responsive design, semantic HTML, accessibility, Outlook compatibility, valid MCTL — automatically. Your prompt decides the rest.

A productive prompt covers four things:

1. **What kind of email** — newsletter, promotional, transactional, announcement, or re-engagement. The skill maps these to structural blueprints with sensible defaults for sections, repeatable blocks, and hideable elements.
2. **Brand basics** — name, audience, language(s), tone.
3. **Visual direction** — colors (foreground, muted, accent, on-accent, background, optional subtle/footer bg, divider), fonts (heading + body with system fallbacks), type scale if you have one.
4. **Structure and features** — sections in order, which should be repeatable (editor adds/removes/reorders per send), which should be hideable (editor toggles on/off), what merge tags or conditionals are needed.

### Worked example

A prompt like this produces a complete, validator-clean template:

> Build a Mailchimp newsletter template for **Acme Logistics**, a Belgian/Dutch logistics company sending a monthly availabilities update. Audience reads NL, FR, and EN — set `lang="nl-BE"` on this version, we'll fork for FR/EN separately.
>
> **Palette:**
> - foreground `#1a1d2e`
> - muted `#6b6e7a`
> - accent `#2563eb`
> - on-accent `#ffffff`
> - background `#ffffff`
> - subtle-bg `#f5f6f8`
> - divider `#e3e5ea`
>
> **Type:** Headings in **Manrope** (weights 300, 500, 700) via Google Fonts with Arial fallback. Body in **Inter** (400, 600) with Arial fallback. Scale: display 36/40, h1 28/34, h2 22/28, body 15/24, meta 12/18, micro 10/15 uppercase tracked 0.15em.
>
> **Structure:**
> 1. Preheader with current month / issue number
> 2. Top nav: logo + language switcher (EN · NL · FR)
> 3. Hero: eyebrow ("May 2026 — Issue 27") + headline + subhead + primary CTA + hero image
> 4. **Repeatable country sections**, each containing: country name + unit count + 3 card slots (image, eyebrow, title, sqm, specs, CTA) + 1 hideable "coming soon" filler slot + per-country contact blurb
> 5. **Hideable sustainability section** (eyebrow, image, headline, body, CTA)
> 6. **Hideable market signal section** containing **repeatable signal blocks** (eyebrow + body each)
> 7. **Repeatable contact blocks** in a "Get in touch" footer area
> 8. Compliance footer with address, unsubscribe, update prefs, copyright
>
> Validate the output before declaring done.

What the skill brings to that prompt — without you having to ask:

- Responsive design via fluid hybrid + `@media (max-width: 600px)` rules
- `@media (prefers-color-scheme: dark)` dark-mode swaps
- `role="presentation"` on every layout table
- `lang="nl-BE"` on `<html>`, `mso-line-height-rule:exactly` on `<body>`
- MSO conditionals forcing Arial in Outlook, 96 DPI rendering, VML buttons
- `*|UNSUB|*`, `*|LIST:ADDRESS|*` (or `*|HTML:LIST:ADDRESS_HTML|*`), `*|MC_PREVIEW_TEXT|*` correctly placed
- Every `mc:edit` on a `<td>` or `<div>` (never on `<img>`, `<a>`, `<span>` — the #1 cause of silent Mailchimp import failures)
- Unique `mc:edit` names; conventional names where applicable (so the template survives Switch Template)
- Every `<img>` with `width`, `height`, `alt`, `display:block`
- WCAG AA contrast checked against the palette you provide
- HTML size under Gmail's 102 KB clipping threshold
- Final pass through `scripts/validate.py` — output is upload-ready

### Iterating

Treat the first generation as a draft. Conversational follow-ups work:

- *"Swap the accent to `#7c3aed` and verify contrast on the CTA."*
- *"Add a 'Featured property' section between hero and country sections — single card, hideable."*
- *"The hero image is too tall on mobile — reduce its rendered height to 200px below 600px wide."*
- *"Add a French-language version: copy the file, change `lang` to `fr-BE`, translate the hero eyebrow and CTA labels, keep everything else identical."*
- *"This is missing alt text on the map image — fix it."*

### What you don't need to provide

The skill handles these without prompting:

- The doctype, head block, MSO conditionals, viewport meta
- The three-table responsive scaffold
- Default CSS resets for Outlook / Apple Mail / Gmail
- Bulletproof button structure (VML + non-MSO branches)
- Multi-column footer with dark-mode-friendly styling
- Compliance footer structure (you provide the address; the merge tags are automatic)

## Installation

### Claude Code Plugin (recommended)

```bash
# First time: add the marketplace, then install
/plugin marketplace add michtio/mailchimp-claude-skills
/plugin install mailchimp-claude-skills@michtio/mailchimp-claude-skills
```

### Clone and run `install.sh`

```bash
git clone https://github.com/michtio/mailchimp-claude-skills.git ~/.claude/mailchimp-claude-skills
cd ~/.claude/mailchimp-claude-skills && bash install.sh
```

`install.sh` symlinks every skill in this repo (any directory containing a `SKILL.md`) into `~/.claude/skills/`, so updates flow through automatically when you `git pull`. Run `bash uninstall.sh` to remove the symlinks. Manually-installed skills are never touched.

### Manual copy / symlink

```bash
# Copy into personal scope
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

## From Claude output to a sent campaign

Each generated template goes through this flow:

1. **Claude generates `template.html`** using the skill.
2. **Validate locally**: `python3 mailchimp-template-language/scripts/validate.py template.html`
   - Exit 0 = clean. Exit 1 = errors found. Use `--strict` to fail on warnings too (good for CI).
3. **(Optional) Inline CSS**: `juice template.html template.inlined.html --preserve-media-queries --preserve-pseudos --preserve-important`
   - Skip unless you have specific reasons (see `references/inliner.md`); Mailchimp's built-in inliner handles most cases.
4. **Upload to Mailchimp**:
   - Manual: Templates → Create Template → Code your own → Paste in code.
   - Programmatic: use a Mailchimp MCP server (see [Composition](#composition) below) to `POST /3.0/templates`.
5. **Preview rendering**: Mailchimp's built-in Inbox Preview (paid plans), Litmus, or Email on Acid before sending.
6. **Send test**: always send a test to a real inbox and a screen reader before launching a campaign.

## Composition

The skill is the **authoring** layer. Pair with these for **deployment** and **rendering verification**:

- [`damientilman/mailchimp-mcp-server`](https://github.com/damientilman/mailchimp-mcp-server) — 112 tools across the Mailchimp Marketing API (campaigns, audiences, reports, segments, automations, e-commerce). Read-only and dry-run safety modes. Install via `uvx mailchimp-mcp-server`.
- [Composio's hosted Mailchimp MCP](https://mcp.composio.dev/mailchimp) — OAuth alternative if you don't want to manage API keys.
- [Litmus](https://litmus.com/) / [Email on Acid](https://www.emailonacid.com/) — cross-client render testing. The skill cannot test rendering itself; these can.

End-to-end: Claude writes `template.html` → `validate.py` passes → Mailchimp MCP uploads via `/3.0/templates` → Litmus/EoA confirms rendering → send.

## Why this repo exists

Across the public Anthropic Skills ecosystem (anthropics/skills, obra/superpowers, wshobson/agents, ComposioHQ/awesome-claude-skills, and other catalogs), as of mid-2026 no skill targets Mailchimp's template language directly. Existing "Mailchimp" skills are uniformly API/MCP wrappers operating on existing templates — none help Claude *author* a custom-coded MCTL template that doesn't silently break on import.

This repo fills the gap with hand-authored MCTL tooling tuned to Mailchimp's quirks. Templates produced via prompting + this skill pass the validator, render across the major email clients, and are accessible by default — which means brand and content become the only things you need to think about per project.

## Roadmap

Likely future skills (built when real client demand drives them):

- `mailchimp-multilingual` — Campaign-level patterns for sending in multiple languages. Two distinct shapes:
  - **Single list, multiple languages** (one audience, members speak different languages): `*|TRANSLATE|*`, audience groups, conditional content blocks. Common in countries with multiple official languages — Switzerland (DE/FR/IT/RM), Belgium (NL/FR/DE), Canada (EN/FR), Singapore (EN/ZH/MS/TA).
  - **Global brand, multiple markets** (separate audiences per market, often separate Mailchimp accounts or sub-accounts): template syndication / forking workflow, per-market regional adaptations (currency, regulations, product lineup, brand voice), multi-account orchestration. Common in international consumer brands.

  Template-level concerns (`lang` attribute, character coverage, per-script font stacks, RTL handling) are already handled by `mailchimp-template-language` for both shapes — what this skill adds is the audience and campaign orchestration on top.
- `mailchimp-rss-driven` — Templates wired for Mailchimp's RSS-to-email automations, with `*|RSSITEM|*` patterns.
- `mailchimp-product-feed` — E-commerce templates with product-grid merge tags for Shopify/WooCommerce integrations.
- `mailchimp-transactional-handlebars` — Separate skill for Mandrill/Transactional (different syntax: Handlebars, not MCTL).

## License

MIT — see [LICENSE](./LICENSE).

## Author

Built by [michtio](https://github.com/michtio) at [Bleu Chaud](https://bleuchaud.com).
