# Multi-Market Global Brand

The other multilingual shape: a brand that runs **separate audiences per market**, sometimes across **separate Mailchimp accounts or sub-accounts**. Not the same problem as single-list-multilingual — different audience boundaries, different regulatory contexts, different ops models.

This file is intentionally lighter than the single-list-multilingual references. The shape varies more by brand than by Mailchimp surface, and the heavy lifting tends to be in process design and template syndication rather than in MCTL features. Treat this as orientation, not a finished playbook.

## When this shape applies

- An international brand (consumer goods, hospitality, SaaS) sends to subscribers in multiple countries.
- Audience lists are split per market — `acme-uk`, `acme-de`, `acme-fr`, `acme-us`, etc. — usually because the markets are run by separate marketing teams, have different product catalogs, or are subject to different regulations.
- Sometimes the audiences live in separate Mailchimp accounts (one account per market). Sometimes they're separate audiences within a single account. Sometimes they're sub-accounts under a parent account.
- Multilingual concerns are usually downstream of multi-market: each market's audience is largely single-language, but the brand still produces parallel templates across markets that need to stay visually and structurally aligned.

If the answer to "is there one audience or several?" is *several* — this is your file. If *one*, see `segments-vs-conditional.md` and `conditional-content.md`.

## Account topology choices

Three documented Mailchimp account models:

1. **Single account, multiple audiences** — one Mailchimp account, one billing relationship, multiple audiences (one per market). Easiest to administer; reporting rolls up at the account level. Common for mid-size brands.
2. **Sub-accounts under a parent** — Mailchimp's "Multi-Account Management" feature lets larger plans manage child accounts from a parent. Each child has its own audience, templates, and reporting; the parent oversees billing and access. Common for franchise / dealer / regional-office models.
3. **Fully separate accounts** — different markets pay separately, manage independently, share only the brand. Common when markets are operated by different legal entities or were acquired separately.

The skill doesn't push a topology — that's a business decision. But the multi-market workflow differs:

| Concern | Single account, multi-audience | Sub-accounts | Separate accounts |
|---|---|---|---|
| Template sharing | Copy/paste or "Save as template" within the account | Templates per child account; manual sync | Manual sync between accounts |
| Brand consistency | Easiest (all in one place) | Mixed (each child has autonomy) | Hardest (no shared surface) |
| Reporting roll-up | Native | Parent dashboard | External (no native cross-account view) |
| Billing | One bill | One bill | Separate bills |
| Ops cost of a new market | Low | Medium (set up child account) | High (full account spin-up) |

## Template syndication / forking workflow

Most multi-market brands settle on some version of "the brand keeps a master template; each market forks it and adapts." Patterns that work:

### Master + fork

1. **Brand HQ maintains a canonical template** in a code repo (or in one Mailchimp account) — the visual system, structural blueprint, MCTL placement, accessibility patterns.
2. **Each market forks** the template for their account: adapts the language, swaps copy, plugs in market-specific compliance footer, regional images, currency formatting.
3. **HQ pushes updates** to the canonical template; market teams pull and re-merge into their fork. Cadence: typically quarterly or per-campaign-family, not per-send.

This is much closer to how software teams handle internationalization than to how single-list-multilingual works. The skill that helps here is less about MCTL features and more about:

- Keeping the structural skeleton consistent across forks (so updates merge cleanly).
- Documenting which sections are market-locked vs centrally-managed.
- Having a validator (`mailchimp-template-language/scripts/validate.py`) run against every fork before send.

### Per-market regulatory footer

Each market has its own compliance requirements. Examples of what differs:

| Market | Compliance element |
|---|---|
| Belgium | KBO/BCE number, BTW/TVA number, language-specific unsubscribe wording |
| France | SIRET number, RGPD (GDPR-FR) language, RCS registration |
| Germany | Handelsregister number, Umsatzsteuer-Identifikationsnummer, Impressum link |
| UK | Company number (Companies House), VAT number |
| US | CAN-SPAM physical address (mandatory), state-specific privacy notices (CCPA in California, etc.) |
| Canada | CASL compliance language, English/French parity in Quebec, business address |
| Brazil | LGPD compliance language, CNPJ |
| Australia | ACN, Spam Act compliance |

These are not interchangeable. A French market's footer needs SIRET, not KBO. A German market's footer needs an Impressum link, which other markets don't. The footer is one of the strongest reasons to fork per market rather than try to handle multi-market in a single conditional template.

### Per-market currency, product, regulatory differences

Beyond compliance:

- **Currency**: prices, totals, shipping costs vary per market. Don't try to convert at send time; bake the market's currency into the templates and merge fields for that market.
- **Product lineup**: not every market sells every SKU. The product grid in a UK template might be different from the German one even when the campaign concept is the same.
- **Regulatory language**: alcohol marketing language varies by country, financial services disclosures vary, pharmaceutical claims vary. The market team's legal review is what enforces this; the template's job is to leave space for it.
- **Brand voice variation**: some brands run different tones in different markets. The skill doesn't push uniformity — it pushes parallel *structure* with adapted *content*.

## Sync strategy between markets

Three rough approaches, in increasing rigor:

1. **Drift tolerated** — HQ provides templates as a starting point, markets adapt freely, no enforcement. Common for small brands and federations of regional businesses. Drawback: brand inconsistency creeps in.
2. **Periodic re-sync** — HQ updates the canonical template, markets re-merge on a cadence (quarterly, per-campaign-family). Drawback: ops cost per market per merge.
3. **Active syndication** — HQ runs a pipeline (often outside Mailchimp — a code repo, a CMS, or a workflow tool) that generates per-market templates from a shared source. Each market's template is a build artifact, not a manual fork. Drawback: requires engineering investment, hardest to set up.

Which one fits depends on the brand's size, the markets' autonomy, and how often the master template changes.

## What this skill *doesn't* do for multi-market

To be honest about scope: multi-market global brand work is a much broader operations problem than a Claude Code skill can fully address. The skill helps with:

- Generating per-market templates from a description that includes the market's constraints (compliance, currency, language).
- Auditing existing templates across markets for structural consistency.
- Refactoring a single-market template into a multi-market-friendly form (extracting market-locked sections, normalizing the structural skeleton).

It does *not*:

- Manage multi-account Mailchimp API operations (use a Mailchimp MCP server for that — though most don't yet handle cross-account flows cleanly).
- Translate copy professionally (use a translation service; the skill can scaffold the structure but the prose belongs to humans).
- Track which markets have which version of the template (build a CMS or use a workflow tool — outside the skill's surface).
- Replace legal review of per-market compliance footers (always have local counsel sign off).

## When to escalate to a dedicated multi-market workflow

Signs the brand has outgrown ad-hoc forking and needs real syndication tooling:

- More than ~5 markets.
- More than ~12 campaigns per year per market.
- HQ template changes that have to roll out to all markets within a week.
- A history of markets drifting visually or structurally from the brand standard.
- Compliance review failures in specific markets traceable to outdated forks.

At that scale, the skill's job is to inform the templates themselves; the rest of the workflow (master/source, build pipeline, market hand-off) lives in the brand's marketing-ops stack.

## Composability

For multi-market work, this skill pairs with:

- **`mailchimp-template-language`** — same as always; per-market templates are still MCTL templates underneath, just multiplied.
- **Mailchimp MCP server** — for uploading templates per audience or per account, listing audiences across accounts (where the MCP supports it).
- **Translation services** — Lokalise, Phrase, Smartling, or human translators for the prose. The skill scaffolds; humans translate.

The single-list-multilingual references (`language-detection.md`, `conditional-content.md`, `segments-vs-conditional.md`) are mostly *not* applicable to multi-market: each audience is single-language, conditional content per language inside one audience isn't the pattern. The exception is when a single market itself has multiple languages (a Belgian audience inside a multi-market brand), in which case both shapes apply — that audience uses single-list-multilingual patterns, the parent brand uses multi-market patterns.
