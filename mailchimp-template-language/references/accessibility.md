# Accessibility

WCAG 2.1 AA targets and the email-specific quirks that change how to meet them. Most professional clients now require AA compliance for marketing email — this is no longer optional.

## Contrast

Two thresholds matter:

| Text | Ratio | Notes |
|---|---|---|
| Body text (< 18pt, or < 14pt bold) | **4.5:1** | Most copy in a template |
| Large text (≥ 18pt, or ≥ 14pt bold) | **3:1** | Display headlines often pass this; small subheads might not |
| Non-text UI (button borders, focus indicators, meaningful icons) | **3:1** | A button's border vs its background |

Verify every token pair:
- `color-foreground` on `color-background` — body copy
- `color-muted` on `color-background` — meta, captions, footer compliance
- `color-on-accent` on `color-accent` — CTA contrast (this is the one most often broken when the brand accent is a mid-saturation color)
- `color-foreground` on `color-subtle-bg` — copy inside callout/stat blocks
- Dark mode: same pairs against `color-dark-*` tokens

Tools: WebAIM Contrast Checker, Stark (Figma plugin), Colorable. Test the actual hex values; don't eyeball.

### Subtle-grey body text

A common professional-looking choice is muted grey body copy (e.g. `#5a5a5a` on `#ffffff`). At small sizes this often fails 4.5:1. Two options:

1. Darken the grey until it passes (typically `#595959` minimum on white).
2. Keep the lighter grey for **non-essential meta only** (timestamps, captions, footer compliance) and use a darker token for everything important.

The second is professional and pragmatic — the visual hierarchy comes through, and the essential reading path stays accessible.

## Alt text

Every `<img>` needs `alt`. The question is whether the alt is **informative** or **empty**.

### Decorative — empty alt

Hero patterns, decorative dividers, background flourishes, repeated brand ornaments:

```html
<img src="..." width="600" height="200" alt="" style="display:block;">
```

The empty `alt=""` tells screen readers "skip this." Better than no alt at all (which makes screen readers read the filename) and better than a fake description ("decorative image").

### Informative — describe the content

Logos, content images, photographs, charts:

```html
<img src="..." width="180" height="40" alt="Brand wordmark" style="display:block;">
<img src="..." width="600" height="400" alt="Aerial view of the Aalst warehouse, 18,400 m²" style="display:block;">
<img src="..." width="600" height="400" alt="Bar chart: Q4 2025 occupancy by region — Belgium 92%, Netherlands 88%, France 76%" style="display:block;">
```

Rules:
- **Logo**: `alt="Brand name"` — not "Brand logo" (redundant).
- **Photo / illustration**: describe what's shown, not what it looks like. "Aerial view of warehouse" not "Square image with grey building."
- **Chart / infographic**: include the data being shown. Screen reader users miss the visual; alt is their access.
- **Icon next to text**: empty alt — the text already conveys the meaning, the icon is decoration.
- **Icon alone (no nearby text)**: describe the action. `alt="Open menu"` not `alt="Three lines."`

Mailchimp's editor also lets editors set alt per-image; document this in the editor handover doc so each campaign isn't shipped with default alt text.

## Lang attribute

```html
<html lang="en">     <!-- generic English -->
<html lang="en-GB">  <!-- British English -->
<html lang="fr-CA">  <!-- Canadian French -->
<html lang="de-CH">  <!-- Swiss German -->
<html lang="zh-TW">  <!-- Traditional Chinese (Taiwan) -->
```

The `lang` attribute on `<html>` tells screen readers which pronunciation rules to use. Without it, an English screen reader reading French content sounds bizarre. Use **region-specific codes** wherever pronunciation, spelling, or convention differs by region — `en-US` vs `en-GB`, `fr-FR` vs `fr-CA` vs `fr-BE`, `de-DE` vs `de-CH` vs `de-AT`, `pt-PT` vs `pt-BR`, `zh-CN` vs `zh-TW`, etc. The generic `lang="en"` is a fallback when the region doesn't matter or is unknown.

For mixed-language templates (rare but happens — e.g. an English newsletter with a French testimonial, or a Spanish announcement quoting an English source), set `lang` on the language-switched element:

```html
<p lang="fr">«&nbsp;Excellent service, équipe réactive.&nbsp;»</p>
<blockquote lang="en">"Best logistics partner we've worked with."</blockquote>
```

For right-to-left scripts (Arabic, Hebrew, Persian, Urdu), set `dir="rtl"` alongside `lang`:

```html
<html lang="ar" dir="rtl">
```

This flips the layout direction at the HTML level. RTL email layouts also need mirrored padding / alignment in CSS — beyond `dir="rtl"`, expect to swap `padding-left` ↔ `padding-right` and `text-align:left` ↔ `text-align:right` throughout.

## Semantic structure

### Heading order

`<h1>` once per email (the hero headline). Then `<h2>`, `<h3>` in document order. Don't skip levels (`<h1>` → `<h3>` with no `<h2>`) — screen readers use heading nav to skim.

```html
<h1>Issue 27 — May 2026</h1>          <!-- hero, once -->
<h2>This month's updates</h2>          <!-- main section -->
<h3>Product</h3>                       <!-- subsection -->
<h3>Engineering</h3>
<h2>Community spotlight</h2>           <!-- next main section -->
```

Don't use heading tags for visual styling. A "looks like a heading but isn't structurally one" should be a styled `<div>` or `<p>`, not `<h2>`.

### `role="presentation"` on layout tables

Every layout table in an email uses tables for visual structure, not data. Mark them so screen readers don't announce them as data tables:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
```

Without `role="presentation"`, JAWS / NVDA / VoiceOver read "Table with 1 row, 3 columns" for every layout table — exhausting on a multi-section newsletter.

**Exception**: actual data tables (line items in a receipt, comparison grids) should NOT have `role="presentation"` — they ARE data and the table semantics help.

### Link text

Descriptive, not "click here":

```html
<!-- Bad -->
<a href="...">Click here</a> to read the May availabilities.

<!-- Good -->
Read the <a href="...">May availabilities</a>.

<!-- Also good (link wraps the whole phrase) -->
<a href="...">Read the May availabilities</a>
```

Screen reader users navigate by link list; "Click here, click here, click here" is useless. The link text should make sense out of context.

For "Read more →" patterns where the link target is implied by surrounding content, add `aria-label`:

```html
<a href="..." aria-label="Read more about Aalst">Read more &rarr;</a>
```

Most email clients respect `aria-label`; the screen reader hears the full label, sighted users see the short text.

## Color is not the only signal

Status colors (red error, green success, amber warning) must also carry an icon or label:

```html
<!-- Bad: green text alone -->
<p style="color:green;">Order confirmed</p>

<!-- Good: green text + checkmark icon -->
<p style="color:green;"><img src="check.png" alt="" width="16" height="16"> Order confirmed</p>

<!-- Also good: label -->
<p style="color:green;">Status: Confirmed</p>
```

Colorblind recipients miss the green-vs-red distinction; the second signal carries them through.

## Touch targets

On mobile, tap targets should be **at least 44×44px** (Apple HIG / WCAG 2.5.5 AAA recommendation; AA target is 24×24px minimum).

```css
@media screen and (max-width: 600px) {
  .button-mobile {
    width: 100% !important;
    padding: 16px 24px !important;
    /* Total touch area: full width × ~50px tall = comfortable tap */
  }
  /* Scope to a class — global `a` would over-space inline links inside copy. */
  .nav-link-mobile,
  .footer-link-mobile {
    line-height: 1.8 !important;
    display: inline-block;
    padding: 4px 0;
  }
}
```

Apply `class="nav-link-mobile"` or `class="footer-link-mobile"` on `<a>` elements in stacked nav rows and footer link columns. Don't put line-height on the bare `a` selector — inline body links would wrap with awkward leading.

## Email-specific accessibility patterns

### Preview text as plain language

`*|MC_PREVIEW_TEXT|*` is what screen reader users hear first in their inbox triage. Use it like a one-sentence summary, not a teaser:

```
Bad:  "You won't believe what's inside..."
Good: "Q2 product update — 3 new features, faster exports, new API endpoints."
```

### View-in-browser link near the top

`*|ARCHIVE|*` linked as "View in browser" at the top of the email matters more for image-off / clipped-Gmail recipients than for sighted recipients with full rendering. Keep it accessible:

```html
<a href="*|ARCHIVE|*" aria-label="View this email in a browser window">View in browser</a>
```

### Plain-text alternative

Mailchimp generates a plain-text version automatically from your HTML, but the auto-generated version is often messy. For important sends, edit the plain-text version in the campaign editor before sending. Screen reader users on text-mode mail clients depend on it; spam filters score lower when the HTML and plain-text versions disagree wildly.

## What to test before sending

| Tool | Checks |
|---|---|
| WebAIM Contrast Checker | Contrast on all token pairs |
| Wave (free browser extension) | Run on the campaign archive URL — flags missing alt, heading order, lang |
| VoiceOver (macOS) / NVDA (Windows) | Read through the email; does it make sense? |
| Litmus / Email on Acid | Render across clients including image-off views |
| Mailchimp's own "Inbox Preview" | Final paid sanity check, mirrors real clients |

A 5-minute pass with Wave + VoiceOver catches 90% of real issues. Don't skip it.
