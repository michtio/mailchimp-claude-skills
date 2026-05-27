# Typography & Design Tokens

This file describes the **system** for typography and color in a Mailchimp template — not specific values. The brand picks the fonts, colors, and scale; this document defines the slot structure they fill.

## Token slots

A professional template separates **what looks like what** (semantic intent) from **the exact value** (brand decision). Define tokens once at the top of `<style>` and in a comment block, then reference them by name in the body. Inline-CSS email can't use CSS custom properties reliably across all clients, so the "tokens" are really a documented vocabulary the author keeps consistent by hand or with an inliner pre-process step.

### The minimal slot set

```
/* COLOR TOKENS — fill in per brand
   color-foreground         primary text (large headlines, body)
   color-muted              secondary text (subheads, meta, captions)
   color-accent             brand accent (CTAs, links, highlights)
   color-on-accent          text color sitting on the accent background
   color-background         page background (often #ffffff or off-white)
   color-subtle-bg          section panel background (e.g. stat row, callout)
   color-footer-bg          footer background (often a deeper shade)
   color-divider            hairline rule color
   color-dark-bg            dark-mode body background
   color-dark-foreground    dark-mode primary text
   color-dark-muted         dark-mode secondary text

   TYPOGRAPHY TOKENS
   heading-font             display + heading stack (with system fallback)
   body-font                paragraph + UI stack (with system fallback)
   mono-font                numeric / code stack (optional)
*/
```

Patterns in this skill reference these by `{{ token-name }}`. When generating a template, substitute the brand's actual values.

## Type scale

A scale is **a finite ladder of sizes used consistently**. Picking 6–8 steps and using nothing else makes a template feel composed; using 14 ad-hoc sizes makes it feel improvised.

### Scale shape (not values)

Define the scale by **role**, not by pixel:

| Role | Use | Typical size range |
|---|---|---|
| `display` | Hero headlines, one per template | 36–48px |
| `heading-1` | Section openers | 28–36px |
| `heading-2` | Sub-section titles | 20–24px |
| `heading-3` | Card titles, inline section labels | 15–18px |
| `body` | Paragraph copy | 14–16px |
| `meta` | Captions, descriptions, supporting text | 12–14px |
| `micro` | Eyebrows, footer compliance, legal | 10–11px |

The brand picks where in the range each role sits — editorial brands lean smaller and lighter; marketing brands lean larger and heavier. Stay inside the role table when scaling per-section.

### Modular ratios

If unsure, generate the scale from a single base size and a ratio:
- **1.2 (minor third)** — quiet, editorial, tight rhythm
- **1.25 (major third)** — modern, balanced
- **1.333 (perfect fourth)** — bolder, more contrast
- **1.5 (perfect fifth)** — aggressive, marketing-led

Start with body=14 or 16 and walk up. Round to nearest pixel; subpixels render unpredictably in email.

## Line-height ratios

Email rendering varies more than web; conservative line-heights protect against client breakage.

| Role | Ratio | Why |
|---|---|---|
| Display / heading-1 | 1.05–1.15 | Tight; large type breathes already |
| Heading-2 / heading-3 | 1.2–1.3 | Mid-range; readable but composed |
| Body | 1.5–1.6 | Comfortable for paragraphs; the email standard |
| Meta / micro | 1.4–1.55 | Slightly tighter than body since type is smaller |

Always set line-height in `<style>` AND inline on the element — Outlook ignores `<style>`-only line-height on block elements unless `mso-line-height-rule:exactly` is set on `<body>` (already in the skeleton).

## Letter-spacing (tracking)

Tracking has two semantic uses in email:

### Uppercase tracking — for eyebrows, labels, micro type

```
font-size: 10–11px;
text-transform: uppercase;
letter-spacing: 0.12em – 0.18em;
```

Uppercase without tracking looks cramped at small sizes. The `em`-based value scales with font-size — `0.15em` reads consistently whether the eyebrow is 10px or 14px.

### Headline tightening — for display type

```
font-size: 32–48px;
letter-spacing: -0.01em – -0.02em;
```

Large type leaves visual gaps at default kerning. Negative tracking tightens it. Don't apply to body — it makes text harder to read at small sizes.

Body and meta use `letter-spacing: 0` (default).

## Web font loading

Web-font support in 2026 is patchier than it looks. Treat the following as the working model:

- **Apple Mail (macOS, iOS), Outlook for Mac** — load reliably.
- **Outlook 365 web** — loads for some corporate Exchange / M365 accounts; drops `@font-face` for Microsoft mailbox accounts (`outlook.com`, `live.com`, `hotmail.com`).
- **Gmail web** — does **not** load arbitrary `@import` web fonts. The renderer has Roboto and Google Sans preloaded; everything else falls through to the stack.
- **Classic Outlook for Windows (Word engine)** — never loads `@font-face`.
- **Gmail mobile apps** — inconsistent; do not rely on web fonts.

Always design assuming the fallback stack will render — web fonts are an enhancement.

### The MSO-conditional pattern

```html
<head>
  ...
  <!--[if !mso]><!-->
  <link href="https://fonts.googleapis.com/css2?family={{ font-name }}:wght@{{ weights }}&display=swap" rel="stylesheet">
  <style>
    @import url('https://fonts.googleapis.com/css2?family={{ font-name }}:wght@{{ weights }}&display=swap');
  </style>
  <!--<![endif]-->

  <!-- Outlook fallback — force a system font everywhere -->
  <!--[if mso]>
  <style>
    table, td, div, h1, h2, h3, h4, p, a, span {
      font-family: Arial, Helvetica, sans-serif !important;
    }
  </style>
  <![endif]-->
</head>
```

Inside the conditional we use `<link>` *and* `<style>@import` for defensive reasons: some clients sanitize `<link>` in `<head>` while still honouring `@import`, and a few historic clients did the reverse. Litmus and Email on Acid both recommend `<link>` as the primary form with `@import` as a fallback for sanitized-`<link>` clients.

### Mandatory fallback stack

Every `font-family` in the body MUST include a system fallback:

```css
font-family: '{{ web-font }}', Arial, Helvetica, sans-serif;
font-family: '{{ web-serif }}', Georgia, 'Times New Roman', serif;
font-family: '{{ web-mono }}', 'Courier New', Courier, monospace;
```

If the web font fails to load (Outlook always, Gmail sometimes), the system font picks up. Don't list the web font alone.

### System-installed alternatives (no @import needed)

When you want a non-default look but can't rely on web fonts in critical regions:

| Style | System stack | Notes |
|---|---|---|
| Modern sans | `Verdana, Geneva, sans-serif` | Highly legible at small sizes; on every major platform |
| Geometric sans | `'Trebuchet MS', sans-serif` | Windows / macOS / iOS |
| Humanist sans | `Tahoma, sans-serif` | Windows / macOS / iOS |
| Serif | `Georgia, 'Times New Roman', serif` | Everywhere |
| Monospace | `'Courier New', Courier, monospace` | Everywhere |

Cross-platform-safe is the goal here. `Palatino Linotype` (Windows) and `Palatino` (macOS) are metrically different fonts under similar names and neither is present on Android, so they're not a safe cross-platform stack. `Garamond` ships with Microsoft Office on Windows (not as a system font) and is absent on Android; treat it as a desktop-only choice, not a universal fallback.

## Multi-language and character coverage

Pick fonts with the script and glyph coverage your audiences need. Common cases:

- **Extended Latin** — accented characters (é è ç ñ ü), ligatures (œ æ), extended currency (€ £). Covers French, Spanish, German, Dutch, Italian, Portuguese, Polish, Czech, Turkish, and more.
- **Vietnamese** — extended Latin with stacked diacritics. **Verify per-platform.** Stock Arial has imperfect Vietnamese diacritic stacking; reliable coverage typically requires Arial Unicode MS, a Vietnamese-aware variant of the family (e.g. Helvetica Neue on macOS), or a Noto font. Don't assume "extended Latin" coverage is sufficient.
- **Cyrillic** for Russian, Ukrainian, Bulgarian, Serbian, Macedonian.
- **Greek** for Greek-language sends.
- **CJK** (Chinese, Japanese, Korean) — usually needs dedicated CJK fonts with much larger file sizes; prefer per-platform system stacks (see below) over web fonts for size reasons.
- **Arabic / Hebrew** — right-to-left scripts; also affects layout direction (`dir="rtl"` on `<html>` or the language-switched element).
- **Devanagari / Tamil / Thai / other Indic and South-East Asian scripts** — verify per-script with real content.

How to get the coverage:

- **Google Fonts**: include the script subset in the family request. The CSS2 API (`fonts.googleapis.com/css2?...`) serves a `unicode-range`-partitioned stylesheet that lets modern browsers pick subsets per glyph automatically — in browser contexts, the legacy `subset=` parameter is now a no-op. **In email**, where `unicode-range` support is patchy, the `subset=` parameter still affects which subsets are delivered. Common subset names: `latin-ext`, `cyrillic`, `cyrillic-ext`, `greek`, `greek-ext`, `vietnamese`. Bigger subsets mean bigger CSS files — only request what the audience uses.
- **System fonts**: Arial, Georgia, Verdana, Tahoma cover most extended-Latin diacritics on Windows / macOS / iOS reliably. Helvetica's coverage varies by platform build. For non-Latin scripts, fall back to platform-native stacks (next section).
- **CJK system stacks**:
  - **Simplified Chinese** — `'PingFang SC'` (macOS / iOS), `'Microsoft YaHei'` (Windows), `'Noto Sans SC'` (Linux / Android fallback)
  - **Traditional Chinese** — `'PingFang TC'` (macOS / iOS), `'Microsoft JhengHei'` (Windows), `'Noto Sans TC'`
  - **Japanese** — `'Hiragino Sans'` (macOS / iOS), `'Yu Gothic'` / `'Meiryo'` (Windows), `'Noto Sans JP'`
  - **Korean** — `'Apple SD Gothic Neo'` (macOS / iOS), `'Malgun Gothic'` (Windows), `'Noto Sans KR'`
- **Always test with real content.** A subhead that reads "café français" in proof can render as "caf□ fran□ais" with tofu (missing-glyph boxes) if the font subset is wrong.

Set the `lang` attribute on `<html>` per audience, using region-specific codes where pronunciation or convention differs (`en-US` vs `en-GB`, `fr-FR` vs `fr-CA` vs `fr-BE`, `de-DE` vs `de-CH` vs `de-AT`, `zh-CN` vs `zh-TW`). For multi-language sends from a single template (rare — most multilingual programs use per-language audience groups or fully separate campaigns), set on the language-switched element instead:

```html
<p lang="fr">«&nbsp;Excellent service, équipe réactive.&nbsp;»</p>
```

## Color: contrast and dark mode

Specific contrast targets are covered in `accessibility.md` (WCAG 4.5:1 normal text / 3:1 large text). For the token system itself:

- `color-foreground` on `color-background` MUST clear 4.5:1.
- `color-muted` on `color-background` SHOULD clear 4.5:1 — if it doesn't (common with subtle grey-on-white), reserve it for non-essential meta, never for important copy.
- `color-on-accent` on `color-accent` MUST clear 4.5:1 — this is the CTA contrast pair.
- `color-dark-*` tokens are activated by the `@media (prefers-color-scheme: dark)` block in the head. See `responsive.md` for the dark-mode strategy.

## Spacing rhythm

Email layouts feel professional when padding follows a consistent base unit. Pick 4px or 8px as the base, then use multiples: 8, 16, 24, 32, 48, 64. Mixing 13px and 17px and 22px reads as sloppy even when the proportions are otherwise fine.

The canonical email spacing is the **8px scale**: section padding 24px or 32px, card padding 16px or 24px, inline element gaps 8px or 12px, dividers 32px or 48px above/below.

## A worked example (placeholders only)

This is what a token block at the top of a real template might look like — note every value is a slot to fill, not a recommended value:

```html
<style type="text/css">
  /* ============================================================
     BRAND TOKENS — fill in per project
     ============================================================ */
  /*
     color-foreground:    {{ color-foreground }}
     color-muted:         {{ color-muted }}
     color-accent:        {{ color-accent }}
     color-on-accent:     {{ color-on-accent }}
     color-background:    {{ color-background }}
     color-subtle-bg:     {{ color-subtle-bg }}
     color-divider:       {{ color-divider }}

     heading-font:        '{{ heading-font }}', Arial, sans-serif
     body-font:           '{{ body-font }}', Arial, sans-serif

     Scale (base 14, ratio 1.25):
       display    36 / 1.1
       heading-1  28 / 1.2
       heading-2  22 / 1.3
       heading-3  16 / 1.4
       body       14 / 1.55
       meta       12 / 1.5
       micro      10 / 1.5 uppercase 0.15em
  */
</style>
```

When generating a template, fill in the actual brand values where placeholders sit, and use the documented scale throughout.
