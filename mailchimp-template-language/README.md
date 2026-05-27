# mailchimp-template-language

An Anthropic Agent Skill for authoring custom-coded responsive Mailchimp email templates with full MCTL support (`mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, merge tags, conditionals).

## What this is

A folder following the [Agent Skills spec](https://github.com/anthropics/skills). When loaded, it gives Claude the knowledge to:

- Generate responsive, Outlook-hardened HTML email templates from scratch.
- Convert static HTML emails into Mailchimp-editable templates (add `mc:edit` regions, repeatables, merge tags).
- Refactor existing Mailchimp templates (split sections into variants, add hideable rows, normalize naming conventions for Switch Templates compatibility).
- Validate templates before upload to catch the four most common Mailchimp import failures.

## Why this exists

Mailchimp's custom-coded template format (MCTL) requires hand-written HTML — the `mc:*` editor attributes need to survive intact through import, and the merge-tag syntax has no preprocessor. This skill encodes the table-based responsive patterns, MCTL placement rules, and merge-tag conventions so Claude doesn't have to rediscover them every conversation.

## Install

### Claude Code

```bash
# personal scope (all your projects)
cp -r mailchimp-template-language ~/.claude/skills/

# or project scope (committed with the repo)
mkdir -p .claude/skills
cp -r mailchimp-template-language .claude/skills/
```

Claude Code auto-discovers skills in those paths. Restart your session and Claude will pick it up.

### Claude.ai

1. Zip the `mailchimp-template-language/` folder (the folder itself, with `SKILL.md` at the root).
2. Settings → Capabilities → Skills → Upload.

### Anthropic API

Upload via the Files API and reference in your skills config. See [Anthropic's skill docs](https://docs.claude.com/en/docs/agents/skills) for the current API shape.

## Folder layout

```
mailchimp-template-language/
├── SKILL.md                       # Trigger description + phased workflow
├── README.md                      # This file
├── references/
│   ├── structure.md               # Doctype, head, table skeleton, Outlook conditionals
│   ├── mc-attributes.md           # mc:edit / mc:repeatable / mc:variant / mc:hideable
│   ├── merge-tags.md              # *|TAG|* syntax, conditionals, required compliance
│   ├── responsive.md              # Fluid hybrid, media queries, dark mode, bulletproof buttons
│   ├── patterns.md                # Brand-neutral content blocks (section openers, cards, footers, etc.)
│   ├── typography.md              # Token-slot system, type scale, web-font loading
│   ├── blueprints.md              # Structural archetypes: newsletter, promo, transactional, announcement, re-engagement
│   ├── accessibility.md           # WCAG AA contrast, alt text, lang, role=presentation, semantic order
│   └── inliner.md                 # CSS inlining workflow (Juice/Premailer), what survives Gmail web
├── assets/
│   └── skeleton.html              # Working starter: 600px responsive, all MCTL features wired, brand-neutral
└── scripts/
    └── validate.py                # Pre-upload validator (Python 3.10+, stdlib only)
```

References load on demand — `SKILL.md` stays small. Claude only pulls in the relevant file when the conversation needs it.

**Brand-neutral by design.** The skill provides patterns, token slots, and structural blueprints — it does not impose a default visual direction. Real-world templates with brand-specific palettes, fonts, and content live in their own repos; the skill is the toolkit, not the example.

## Usage examples

After install, Claude will trigger this skill on prompts like:

- *"Build me a Mailchimp template for a monthly newsletter with a hero, three article cards, and a CTA"*
- *"Convert this static HTML email into a Mailchimp-editable template"*
- *"Add a hideable promo banner with editable text to my Mailchimp template"*
- *"Refactor these three Mailchimp templates so they share `mc:edit` names and the user can Switch Template without losing content"*
- *"Why won't my Mailchimp template import?"* (Claude will run the validator)

## Running the validator manually

```bash
python3 mailchimp-template-language/scripts/validate.py path/to/template.html

# strict mode: warnings become errors (use in CI)
python3 mailchimp-template-language/scripts/validate.py path/to/template.html --strict
```

Exit codes: 0 clean, 1 issues found, 2 file not found. Safe in CI pipelines.

What it catches:
- `mc:edit` on inline elements (span, a, strong, etc.)
- `mc:edit` on `<table>` itself
- Duplicate `mc:edit` names
- Nested `mc:edit` regions
- Missing required compliance tags (`*|UNSUB|*`, `*|LIST:ADDRESS|*`)
- Missing preview text tag
- `<img>` without width/height attributes
- Missing doctype or viewport meta
- HTML over Gmail's 102 KB clipping threshold

What it doesn't catch:
- Visual rendering bugs (use Litmus/EoA)
- Merge tag typos beyond required compliance tags
- Brand consistency

## Composition with other tools

This is the **authoring** half. For the **deployment** half, pair with:

- **`damientilman/mailchimp-mcp-server`** (or Composio's hosted equivalent) to upload via the Marketing API, list templates, create campaigns from a template.
- **Litmus / Email on Acid / Mailchimp Inbox Preview** for cross-client rendering tests.

A typical end-to-end flow:

1. Claude writes the template using this skill → `template.html`
2. `python3 scripts/validate.py template.html` → confirm clean
3. Claude uses the Mailchimp MCP to `POST /3.0/templates` with the HTML
4. User runs Inbox Preview in Mailchimp's UI to verify rendering

## License

MIT
