# Segments vs Conditional Content vs TRANSLATE

The decision tree for the three paths Mailchimp documents to serve multilingual content from a single audience. The choice has real cost implications — ops, deliverability, reporting — so this is worth taking time over.

## The three paths

From https://mailchimp.com/help/view-and-edit-contact-languages/, Mailchimp lists three approaches:

1. **Segments + separate campaigns** — build a Mailchimp segment per language (filter on the `Language` field), send a separate campaign to each segment.
2. **Single campaign + conditional content** — one campaign, body uses `*|IF:MC_LANGUAGE=xx|*` blocks (see `conditional-content.md`).
3. **TRANSLATE link** — `*|TRANSLATE:xx|*` inserts Google Translate links pointing at the campaign archive. One campaign, recipients self-serve translation.

Mailchimp doesn't rank them. The right pick depends on what you need to vary per language.

## Decision tree

Answer the questions top-down. The first "yes" determines the path.

### Q1. Must the subject line, preheader text, from-name, or send time differ per language?

> *"It's not possible to translate the subject line of your email."* — https://mailchimp.com/help/translate-content-in-a-campaign/

The `*|MC_PREVIEW_TEXT|*` value, from-name, subject, and send time are **campaign-level settings** in Mailchimp. They're set once per campaign and can't be conditionally varied per recipient. If any of these must differ per language → **segments path. No alternative.**

This is the single most common reason to be on the segments path. Marketing emails almost always benefit from a localized subject line ("Welcome to Acme" vs "Bienvenue chez Acme"); even when the body is short, opening rates are tightly tied to subject relevance.

### Q2. Do you need per-language reporting (open rate, click rate, revenue) as first-class campaign metrics?

A single conditional campaign reports as **one campaign**. You can't natively see "the French version got 22% open rate, the Dutch version got 31%." Mailchimp doesn't slice campaign reports by `MC_LANGUAGE` automatically.

Workarounds exist:
- Segment-based reporting in Audience views (after the fact).
- Per-language UTM parameters in links → external analytics.
- Click tracking by branch (each `*|IF|*` branch carries its own URL → distinguishable in Mailchimp's click report by URL).

If per-language reporting is a hard requirement, **segments path**.

### Q3. Are the language bodies so long that a single conditional campaign would push past Gmail's ~102 KB clipping threshold?

For a typical newsletter (~30–50 KB single-language), three languages of body content can fit comfortably in one campaign. For long-form content (a multi-section announcement, an embedded annual report summary, etc.), three or four language branches stacked in one body can exceed 100 KB.

If size is a risk, **segments path** (each campaign carries only one language's content).

Estimate: a single language version's HTML weight × number of languages. If that approaches 80+ KB, plan for the segments path.

### Q4. Do the languages need substantially different layouts, not just different copy?

Examples where layout differs by language:
- RTL languages (Arabic, Hebrew, Persian) need mirrored padding and alignment across the entire template, not just translated copy.
- CJK languages often need taller line-height and different font scales than Latin scripts.
- Cultural differences in CTA placement, image choices, color conventions.

A conditional-content campaign with mixed LTR and RTL is hard — `<html dir="...">` is set once at template level and can't be made conditional. If layout differs meaningfully, **segments path** (one template per direction / per language family).

### Q5. Is this a low-stakes informational send where translation quality is secondary?

If the answer is yes (and only yes) — the **TRANSLATE link path** is the lightweight option. Insert `*|TRANSLATE:xx|*` near the top of the body, point everyone at the same English (or whatever primary language) content, let recipients click through to a Google Translate view of the campaign archive if they want it.

Don't use TRANSLATE for branded marketing. Google Translate output isn't on-brand — strange phrasing, missing nuance, no editorial review. It's fine for "here's a community update" type sends; not fine for sales / lifecycle / retention campaigns where copy quality matters.

### Q6. If none of Q1–Q5 forced segments or TRANSLATE — does the body need to differ per recipient?

If yes → **single conditional campaign**. Same subject, same preheader, same send time, but the body switches per language via `*|IF:MC_LANGUAGE=xx|*` blocks. Lower ops cost (one campaign to build, schedule, monitor), no per-language reporting, but works for most "body differs, container doesn't" cases.

If the body is also identical (everyone gets the same email), there's nothing to do — it's a single-language campaign and the multilingual skill doesn't apply.

## Tradeoff matrix

| Concern | Segments + separate campaigns | Single conditional | TRANSLATE link |
|---|---|---|---|
| **Subject line per language** | Yes | No (one subject) | No |
| **Preheader per language** | Yes | No (single `*\|MC_PREVIEW_TEXT\|*`) | No |
| **From-name per language** | Yes | No | No |
| **Send time per language** | Yes (schedule each independently) | No (one send time) | No |
| **Body per language** | Yes (separate template files) | Yes (`*\|IF:MC_LANGUAGE=xx\|*`) | No (one body) |
| **Per-language reporting** | Yes (native) | Workaround via URL tracking | N/A |
| **Layout per language** | Yes (separate templates) | Limited (same `lang`, same `dir`) | No |
| **Ops cost** | High — one campaign per language to build, test, schedule, monitor | Low — one campaign | Lowest — one campaign, no translation work |
| **Translation quality** | Editorial control per language | Editorial control per language | Auto-translated (Google) |
| **Falls back on `"Not yet detected"`** | Excluded from all segments unless explicitly included | Hits `*\|ELSE:\|*` branch | Sees the primary-language content with translate links |
| **Gmail 102 KB risk** | Per campaign — same as single-language | Multiplied by number of branches | Single body |
| **Brand surface in spam folder** | Localized subject improves opens | One subject limits localization | One subject limits localization |

## Hybrid patterns

The paths aren't mutually exclusive. Common hybrids:

### Segments path + minimal conditional content

Send a separate campaign per language segment (each with its own subject, preheader, send time), but inside each campaign use one or two `*|IF:MC_LANGUAGE=xx|*` blocks for content that varies *within* a language segment (e.g. region-specific compliance text where the segment is by language but the audience spans multiple countries).

Why: gets you the segments path's benefits (per-language subject, per-language reporting) plus fine-grained variation inside each campaign. Cost: more conditional blocks to maintain.

### Single conditional campaign + a TRANSLATE link

Build a single conditional campaign with full per-language content blocks for the languages you support natively (NL/FR/DE for Belgium), plus a `*|TRANSLATE:xx|*` link in the header for languages you don't support natively (a Spanish-speaking subscriber to a Belgian audience can click through to a Google Translate view of the campaign archive).

Why: gives non-primary-language subscribers *something* without forcing you to translate into every possible language. Cost: the translate link sends them off-brand to Google Translate.

### Default to one language, opt-in to others

Send everyone the brand's primary-language campaign (no conditional, no TRANSLATE). Add a banner or preferences-page CTA pointing to "Read this in your language" and link to the campaign archive with a TRANSLATE parameter, or to a hosted page that lets the recipient set their preference for future sends.

Why: minimum ops cost for sends, redirects multilingual concerns to the preferences flow. Cost: every send is in the primary language only.

## Per-region defaults (rough guidance)

Where the user's brief doesn't specify, these are reasonable starting points by region. Not prescriptive — the decision tree above always wins.

| Region | Default path | Why |
|---|---|---|
| Belgium (NL/FR sometimes DE) | Single conditional campaign for newsletters; segments for marketing | Subjects often translate well between NL/FR for B2B; segments earn their cost for B2C where open rate matters |
| Switzerland (DE/FR/IT) | Segments + separate campaigns | Three languages plus subject-line localization is hard to do well in one campaign |
| Canada (EN/FR) | Segments + separate campaigns | Quebec French is culturally distinct enough from English that one shared subject feels off |
| Singapore (EN/ZH/MS/TA) | Segments + separate campaigns | Four languages, mixed scripts, layout concerns; segments are the practical default |
| Global brand, multiple markets | Multi-market path entirely (see `multi-market.md`) | Different audiences, often different accounts; not single-list-multilingual |

## When you have no `MC_LANGUAGE` data on the audience yet

If most contacts have `"Not yet detected"` (a new audience, or one imported without language data), all three paths effectively deliver the fallback content. Two steps before multilingual sends matter:

1. **Set up explicit Language capture on signup forms** (see `language-detection.md`). Going forward, new subscribers self-identify.
2. **Either backfill** (CSV import, Marketing API update) using whatever data the brand has on existing contacts — past purchase region, country, prior engagement — or **wait for the auto-detection** to populate values as existing contacts engage.

Until language is populated, run as single-language and design for the language migration ahead, not the language strategy you wish you had today.
