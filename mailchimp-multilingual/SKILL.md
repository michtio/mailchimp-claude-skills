---
name: mailchimp-multilingual
description: Plan and build multilingual Mailchimp campaigns where one audience holds members in multiple languages, or where a brand sends across multiple markets. Use this skill when the user mentions multilingual email, multiple languages in one audience, language segments, MC_LANGUAGE, IF:MC_LANGUAGE conditional blocks, audience-level language preference, per-language content, NL/FR/DE Belgian sends, DE/FR/IT/RM Swiss sends, EN/FR Canadian sends, EN/ZH/MS/TA Singaporean sends, multi-market syndication, forking templates per market, per-market regulatory footers, or "we ship this email in three languages." Also use when the user has a single audience and asks how to localize the body of an email per recipient, or wants to choose between language segments + separate campaigns vs a single conditional campaign. Do NOT use for single-language Mailchimp templates (use mailchimp-template-language directly), for generic web/app i18n, or for professional translation workflow tooling.
license: MIT
---

# Mailchimp Multilingual Campaigns

## What this skill covers

Campaign- and audience-level patterns for sending multilingual emails through Mailchimp. Two distinct shapes:

1. **Single list, multiple languages** — one audience whose members speak different languages. The Belgian (NL/FR/DE), Swiss (DE/FR/IT/RM), Canadian (EN/FR), and Singaporean (EN/ZH/MS/TA) case. Use Mailchimp's audience-level `MC_LANGUAGE` field plus conditional content (or segment routing).
2. **Global brand, multiple markets** — separate audiences per market, sometimes separate Mailchimp accounts. Template syndication / forking workflow, per-market regulatory footers, multi-account orchestration. Bigger-org territory.

**Template-level concerns are handled by the sibling skill `mailchimp-template-language`.** That covers the `lang` attribute, character coverage, per-script font stacks, RTL layout, and everything inside a single template file. This skill adds the audience and campaign layer on top.

## When to use this skill

Trigger this skill when:

- The user is sending a campaign to subscribers who speak different languages.
- The user asks about `*|MC_LANGUAGE|*`, `*|IF:MC_LANGUAGE=...|*`, language segments, or per-language content blocks.
- The user is planning a multi-market send across separate audiences or Mailchimp accounts.
- The user asks "should I send one campaign with conditional content, or one campaign per language?"
- The user is in Belgium / Switzerland / Canada / Singapore / Luxembourg / South Africa / India / any market with multiple official languages and is sending email to all of them.

Do **not** use this skill for:

- A single-language Mailchimp template — load `mailchimp-template-language` directly.
- Generic web/app i18n (not Mailchimp).
- Professional translation workflow tooling (this skill orchestrates Mailchimp's built-ins; it doesn't translate text).

## The three documented paths

Mailchimp's own contact-languages doc (https://mailchimp.com/help/view-and-edit-contact-languages/) lists three sanctioned approaches for serving content in multiple languages. None is universally best — pick based on constraints.

| Path | What it is | Best for |
|---|---|---|
| **Segments + separate campaigns** | Build a Mailchimp segment per language (filter on `Language` field), send a separate campaign to each segment. Each campaign has its own subject, preheader, from-name, send-time. | When the subject line / preheader / from-name / send time must differ per language — which is *most* professional sends |
| **Single campaign with conditional content** | One campaign, one subject, one send. Body uses `*\|IF:MC_LANGUAGE=xx\|*…*\|ELSE:\|*…*\|END:IF\|*` blocks to vary content per recipient. | When the subject is universal (brand name, generic phrase) and only the body needs to switch. Lower ops cost; less subject-line flexibility |
| **TRANSLATE link** | Same campaign for everyone, include `*\|TRANSLATE:xx\|*` to insert Google Translate links pointing at the campaign archive. Recipients self-serve. | The lightweight option. Fine for low-stakes informational sends; not appropriate for branded marketing where translation quality matters |

**The bright line**: Mailchimp explicitly states *"It's not possible to translate the subject line of your email."* If the subject line must differ per language, you're on the segments path. There's no workaround.

## Hard rules

Things that will silently break a multilingual campaign:

- **`*|MC_LANGUAGE|*` returns an ISO 639-1 code** like `en`, `fr`, `nl`, `de`. Mailchimp accepts a small set of locale variants too: `fr_CA`, `es_ES`, `pt_PT`. Most variants you might expect — `de_CH`, `it_CH`, `rm`, `zh_Hant` — are **not** in Mailchimp's accepted list and collapse to the base code (or are absent entirely). See `references/language-detection.md` for the full accepted list.
- **Conditional comparisons are case-sensitive.** `*|IF:MC_LANGUAGE=fr|*` matches; `*|IF:MC_LANGUAGE=FR|*` does not. Use lowercase to match the ISO codes Mailchimp stores.
- **Always provide a `*|ELSE:|*` fallback.** New subscribers default to `"Not yet detected"` until Mailchimp's auto-detection runs (or the user sets a value manually). Without an `ELSE` branch, those recipients get an empty email body. The fallback is usually the brand's primary language.
- **A conditional block must open and close within the same `mc:edit` region.** Splitting `*|IF:MC_LANGUAGE=fr|*` across two editable regions silently breaks at send time. See `mailchimp-template-language` → `references/merge-tags.md` for the block-scope rule.
- **Compliance footer must be present in every language version.** Translate the *text* (Unsubscribe / Update preferences) but keep the merge tags as-is (`*|UNSUB|*`, `*|HTML:LIST_ADDRESS_HTML|*`). Address and unsubscribe link are not optional in any locale.
- **Language preference is a system-level field, not a custom merge field.** Don't try to set it via `*|MERGE5|*` or similar; use Mailchimp's built-in Language attribute (auto-detected from browser, exposed on signup forms, manageable via API and CSV import).

## Workflow

When asked to plan or build a multilingual campaign, work through these phases. Each phase points to the reference file that owns the detail.

### Phase 1 — Identify the shape

Single-list-multilingual (one audience, many languages) or multi-market-global-brand (multiple audiences, often multiple accounts)? Confirm with the user. The patterns and reference files differ.

For multi-market work, **load `references/multi-market.md`**.

For single-list-multilingual (the default and best-supported shape in Mailchimp), continue.

### Phase 2 — Map the constraints

Ask the user — or infer from the brief:

1. **Which languages?** Get the list and the priority (which is the "primary" / fallback).
2. **Must the subject line differ per language?** If yes → segments path is forced. If no → conditional-content path is viable.
3. **How is language preference captured today?** Browser auto-detection (Mailchimp's default), signup-form field, CSV import, or unset on all contacts? If unset, the user needs to set it before sending matters.
4. **Are there per-language regulatory differences?** Different compliance footer text, currency, jurisdiction. Single-list-multilingual generally implies one jurisdiction (Belgium has one address); multi-market implies many.

### Phase 3 — Choose the path

**Load `references/segments-vs-conditional.md`** to walk the decision tree and apply the choice to the user's constraints.

### Phase 4 — Establish how language is captured

**Load `references/language-detection.md`** to confirm how `MC_LANGUAGE` gets populated and what values are allowed. If the user's audience has mostly `"Not yet detected"` contacts, this is the gate — language-aware sends only work once language is set on contacts.

### Phase 5 — Build the template

**Load `mailchimp-template-language` (the sibling skill)** for the actual HTML scaffold, `mc:edit` placement, responsive structure, accessibility, and validation. This skill doesn't duplicate that work — it composes with it.

When the path requires conditional content blocks (single-campaign approach, or hybrid where some sections vary per language but the subject doesn't), **load `references/conditional-content.md`** for the `*|IF:MC_LANGUAGE=...|*` patterns: per-language hero, CTA, compliance footer, signature block.

### Phase 6 — Validate

Two layers:

1. **Structural**: run `mailchimp-template-language/scripts/validate.py` on each template file. Same validator as the monolingual flow.
2. **Multilingual completeness** — manual checklist:
   - Every conditional block has an `*|ELSE:|*` fallback for `"Not yet detected"` contacts.
   - Every language's content path includes the compliance footer.
   - The `lang` attribute on `<html>` matches the dominant language of the template (for the segments path, set per-segment).
   - Font stacks cover every script the languages need (see `mailchimp-template-language/references/typography.md`).

### Phase 7 — Test

Mailchimp's "Preview & Test → Enter preview mode" lets you fill merge tags with the data of a chosen subscriber. Preview against at least:

- A subscriber with `MC_LANGUAGE = <primary language>` set.
- A subscriber with `MC_LANGUAGE = <each other language>` in turn.
- A subscriber with no `MC_LANGUAGE` set (`"Not yet detected"`) — confirms the `*|ELSE:|*` fallback fires.

### Phase 8 — Report

After generating, briefly summarize: which languages are covered, which path is used (segments / single conditional / TRANSLATE), where the conditional blocks live, what the fallback path delivers, and what the editor will see in the campaign builder.

## Output expectations

When generating templates or campaign plans:

- For **single conditional campaign**: one HTML file with `*|IF:MC_LANGUAGE=...|*` blocks; one campaign in Mailchimp.
- For **segments + separate campaigns**: one HTML file per language (parallel structure, content translated), one campaign per language segment in Mailchimp. Each file's `<html lang="...">` matches its language.
- For **TRANSLATE link**: one HTML file, single language, with `*|TRANSLATE:xx|*` inserted at the top of the body so recipients can self-serve.

Always include the compliance footer in every language version. Always provide an `*|ELSE:|*` fallback for conditional blocks. Always set `<html lang="...">` correctly.

## Composability

This skill composes with:

- **`mailchimp-template-language`** (sibling) — for the actual template HTML, MCTL placement, validation. Always load alongside this skill.
- **`damientilman/mailchimp-mcp-server`** (MCP) — for creating segments, uploading templates, listing audiences with their language distribution, creating per-segment campaigns.
- **Litmus / Email on Acid** — render each language version in real clients (especially worth doing for RTL scripts and CJK).
