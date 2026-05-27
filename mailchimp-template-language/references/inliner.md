# CSS Inlining

Email clients strip or partially honor `<style>` blocks. Gmail (web) is the most aggressive — it routinely drops the whole `<style>` block, leaving only inline `style="..."` attributes intact. To survive Gmail and the most paranoid clients, every visual rule that matters must be inlined onto the element.

## Why inline?

| Client | Behavior with `<style>` |
|---|---|
| Gmail web | Often strips entirely — depends on size, position, and CSS contents |
| Gmail mobile (iOS/Android app) | Usually keeps `<style>`, but image-off mode strips it |
| Outlook desktop | Keeps `<style>` but applies subset of CSS (no flexbox, limited selectors) |
| Outlook.com web | Keeps `<style>` |
| Apple Mail (macOS/iOS) | Keeps `<style>`, full CSS support |
| Yahoo / AOL | Keeps `<style>`, with quirks |
| Outlook 365 webmail | Keeps `<style>` |

Worst case (Gmail web): only inline styles survive. If you want a button to look like a button in Gmail web, the background-color, padding, color, font, and border-radius must be inline attributes on the `<a>` or `<td>`.

## Mailchimp's built-in inliner

Mailchimp runs an inliner on every template at import time. It works for most cases — converts `<style>` rules to inline `style=""` attributes — but has gaps:

| What it inlines | What it doesn't |
|---|---|
| Class selectors (`.button { ... }`) | `@media` queries (intentional — these have to stay in `<style>`) |
| ID selectors | `@import` rules |
| Tag selectors (`p { ... }`) | Pseudo-selectors (`:hover`, `:focus`) |
| Descendant combinators (`.card p`) | Attribute selectors with complex values |
| Multiple matches per element (merges) | `!important` precedence (varies by client) |

**Mailchimp's inliner is enabled by default** — check the campaign settings before assuming it's running. The toggle is per-campaign in older accounts, per-template in newer ones.

## When to pre-inline yourself

Mailchimp's inliner is good enough for most professional sends. Pre-inline before upload when:

1. **The template uses complex descendant selectors** (`.card > tr > td.image`) — Mailchimp's inliner sometimes drops these.
2. **You want to verify the final HTML before sending** — pre-inlining gives you a deterministic artifact to test against Litmus / Email on Acid.
3. **You're sending the same HTML through both Mailchimp and Mandrill** — Mandrill (Transactional) does NOT auto-inline, so a pre-inlined source is portable.
4. **You're shipping the HTML to a client who'll upload it themselves** — they may have inliner disabled, or be on a Mailchimp plan that varies.

## Tools

### Juice (Node.js) — recommended

```bash
npm install -g juice
juice template.html template.inlined.html
```

Options worth setting:

```bash
juice template.html template.inlined.html \
  --preserve-media-queries \
  --preserve-pseudos \
  --preserve-important
```

- `--preserve-media-queries` — keeps `@media` blocks in `<style>` (they MUST stay non-inline; inlining them does nothing).
- `--preserve-pseudos` — keeps `:hover` (some clients support it on links).
- `--preserve-important` — keeps `!important` flags, which matter for dark-mode overrides.

### Premailer (Ruby)

```bash
gem install premailer
premailer template.html > template.inlined.html
```

Roughly equivalent to Juice, with slightly different defaults. Use whichever fits your existing toolchain.

### Online inliners

For one-off templates without a Node/Ruby setup, several web-based inliners exist (e.g. CSS Inliner from Campaign Monitor). Acceptable for occasional use; not for automated pipelines.

## What must stay in `<style>`

These do NOT survive inlining — keep them in the `<style>` block:

```css
/* Media queries — apply at render time, can't be inlined */
@media screen and (max-width: 600px) { ... }
@media (prefers-color-scheme: dark) { ... }

/* Pseudo-selectors — can't be inlined */
a:hover { text-decoration: underline; }

/* Web font import */
@import url('https://fonts.googleapis.com/...');

/* Client-specific resets that target tags broadly */
body { margin: 0; padding: 0; }
img { display: block; -ms-interpolation-mode: bicubic; }
```

These survive in `<style>` for clients that respect it (Apple Mail, Outlook.com, Outlook 365 web, Gmail mobile). Clients that strip `<style>` (Gmail web) won't get them — which means your responsive breakpoints and dark mode rules will silently degrade in Gmail web, falling back to whatever you inlined.

## Belt-and-braces strategy

For rules that NEED to survive Gmail web's stripping (mobile responsive collapse, dark-mode swaps), inline them AS WELL as keeping the `@media` rule:

```html
<!-- Element with default desktop sizing inline, plus media-query override in <style> -->
<td class="stack" style="display:table-cell; width:50%; padding:16px;">
  <!-- Desktop: 50% width side-by-side, inline -->
</td>

<style>
@media screen and (max-width: 600px) {
  .stack { display:block !important; width:100% !important; }
}
</style>
```

Gmail web: inline `display:table-cell; width:50%` kicks in, and the `@media` rule is gone, so it stays side-by-side. Apple Mail at narrow viewport: media query overrides inline, stacks vertically.

This is why mobile rules use `!important` — they need to win against the inline desktop value when both are present.

## Pre-upload check

Before pasting into Mailchimp's "Code your own → Paste in code":

1. **Run the validator**: `python3 scripts/validate.py template.html` — catches the structural mistakes.
2. **Optionally inline**: `juice template.html template.inlined.html` — produces deterministic output to test.
3. **Test render**: paste into Litmus / Email on Acid / Mailchimp's Inbox Preview before send.
4. **Plain-text preview**: in Mailchimp's editor, edit the auto-generated plain-text version. Send a test to your own inbox in plain text only — confirms screen reader / text-only fallback reads sensibly.

## Common inlining bugs

| Symptom | Cause | Fix |
|---|---|---|
| Mobile layout broken in Gmail web | `@media` rule was the only thing setting widths; nothing inline | Add inline widths as default, use `@media` to override |
| Dark mode swap doesn't fire | `@media (prefers-color-scheme: dark)` got inlined or stripped | Verify `--preserve-media-queries` in juice config |
| Buttons lose styling in Gmail | `.button` class was in `<style>` only, Gmail dropped `<style>` | Inline button styles, AND keep class for media-query overrides |
| Outlook ignores `text-align:center` on container | Inliner moved it to inline `style=""` on a `<div>`; Outlook reads `align="center"` HTML attribute, not CSS | Set `align="center"` as HTML attribute alongside the CSS |
| `!important` lost after inlining | Inliner stripped it; `!important` is required for `@media` rules to win | Use `--preserve-important` |
