# mailchimp-multilingual

An Anthropic Agent Skill for planning and building multilingual Mailchimp campaigns — single-list-multilingual (one audience, multiple languages) and multi-market-global-brand (separate audiences per market) shapes.

## What this is

A folder following the [Agent Skills spec](https://github.com/anthropics/skills). When loaded, it gives Claude the knowledge to:

- Choose between Mailchimp's three documented multilingual paths: language segments + separate campaigns, single conditional campaign, or `*|TRANSLATE:xx|*` link.
- Build `*|IF:MC_LANGUAGE=xx|*` conditional content blocks correctly — case-sensitive, with `*|ELSE:|*` fallback for `"Not yet detected"` contacts, scoped within `mc:edit` regions.
- Capture language preference on signup forms or via Mailchimp's browser auto-detection.
- Navigate the multi-market shape: forking templates per market, per-market compliance footers, account topology choices.

## Why this exists

Mailchimp gives you the building blocks for multilingual sends (the `MC_LANGUAGE` field, conditional merge tags, segments) but doesn't make the right combinations obvious. Most teams default to "one campaign per language" because it's the path of least surprise — even when a single conditional campaign would be lower ops cost. This skill captures the decision tree and the patterns so the trade-offs are clear, and the conditional-content templates are correctly built.

Template-level multilingual concerns (`lang` attribute, character coverage, per-script font stacks, RTL handling) are handled by the sibling skill `mailchimp-template-language`. This skill adds the audience and campaign layer on top.

## Install

Same as the other skills in this repo. See the [repo README](../README.md#quick-start) for the full options. Briefly:

```bash
# Symlink-install all skills via the repo's install.sh
bash install.sh

# Or manually
cp -r mailchimp-multilingual ~/.claude/skills/
```

## Folder layout

```
mailchimp-multilingual/
├── SKILL.md                              # Trigger description + phased workflow
├── README.md                             # This file
└── references/
    ├── language-detection.md             # MC_LANGUAGE + MC_LANGUAGE_LABEL, capture paths, ISO codes, gotchas
    ├── conditional-content.md            # IF:MC_LANGUAGE=xx patterns, multi-language hero/CTA/footer
    ├── segments-vs-conditional.md        # Decision tree across the three documented paths
    └── multi-market.md                   # Multi-market-global-brand: forking, account topology, regulatory differences
```

References load on demand. SKILL.md stays small — Claude pulls in the relevant file when the conversation needs it.

## Usage examples

After install, Claude will trigger this skill on prompts like:

- *"Build a Mailchimp newsletter for our Belgian audience — NL/FR with German fallback. One campaign, conditional content per language."*
- *"We're sending a product announcement to our Swiss audience (DE/FR/IT). Should we use segments or a single conditional campaign?"*
- *"Our Canadian audience is mixed EN/FR. Build a re-engagement template that handles both, with per-language subject lines."*
- *"Audit this conditional-content template — make sure every IF block has an ELSE fallback and the compliance footer is present in every language."*
- *"We're a Belgian agency setting up email for a global SaaS brand with markets in BE, FR, DE, UK, US. What's the audience structure and how do we keep templates aligned across markets?"*
- *"Convert this single-language NL template into a conditional-content version that handles NL/FR/DE in one send."*

The skill loads its references on demand and, for the actual template HTML, composes with the sibling `mailchimp-template-language` skill.

## Composition with other tools

This skill pairs with:

- **`mailchimp-template-language`** (sibling skill, always companion-loaded) — the template HTML, MCTL placement, accessibility, validator.
- **`damientilman/mailchimp-mcp-server`** — for creating language-based segments, uploading per-language templates, scheduling per-segment campaigns.
- **Litmus / Email on Acid** — cross-client render testing per language, especially for RTL scripts and CJK.
- **Translation services** (Lokalise, Phrase, human translators) — the prose. The skill scaffolds structure; humans handle linguistic quality.

## License

MIT
