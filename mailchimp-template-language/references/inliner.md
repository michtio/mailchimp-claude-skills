# CSS Inlining

Email clients vary in how much of a `<style>` block they honour. Apple Mail respects almost everything; Classic Outlook for Windows applies a narrow subset of CSS; Gmail web has size limits and sanitization; the Gmail mobile apps remap class/ID names internally and then sometimes fail to match. The safe default is: every visual rule that **must** render in every client should be inlined onto the element. The `<style>` block is for rules that can safely degrade — media queries, dark-mode swaps, `:hover` states.

## Why inline?

| Client | Behavior with `<style>` |
|---|---|
| Gmail web | Keeps `<style>` since 2016, with caveats: drops the block on parse errors, sanitizes selectors, has a ~8 KB style budget, and strips `<style>` entirely when delivering non-Gmail accounts proxied through Gmail (GANGA) |
| Gmail mobile (iOS / Android app) | Prefixes class and ID selectors at render time; class-name mismatches between inline-rendered HTML and the prefixed `<style>` break some rules — feels like stripping but isn't literally |
| Classic Outlook for Windows (Word engine) | Keeps `<style>` but applies a narrow subset of CSS (no flex/grid, limited selectors, no shorthand for many properties) |
| New Outlook for Windows (WebView2) | Keeps `<style>`, modern CSS support |
| Outlook.com web | Keeps `<style>` |
| Outlook 365 web | Keeps `<style>` |
| Outlook for Mac | Keeps `<style>`, near-modern CSS support |
| Apple Mail (macOS / iOS) | Keeps `<style>`, full CSS support |
| Yahoo / AOL | Keeps `<style>`, with selector quirks (strips `<body>` styles, mangles a few advanced selectors) |

Worst case for `<style>` survival is Gmail web with a parse error or over-budget stylesheet — only inline styles survive that path. So: if a rule **must** render everywhere (button background, primary text color, padding on a `<td>`), inline it onto the element.

## Mailchimp's built-in inliner

Mailchimp ships an optional CSS Inliner that converts `<style>` rules to inline `style=""` attributes at campaign-send time. **It is opt-in, not automatic** — you enable it via a checkbox in the campaign's code-paste settings ("Code your own → Paste in code → Settings → Enable CSS Inliner"). Older templates and most accounts default to **off**.

If you're shipping a Mailchimp template and want CSS inlined, either (a) enable the toggle on every campaign, (b) pre-inline with Juice or Premailer before paste-in so the artifact is deterministic, or (c) hand-inline the rules that matter.

When Mailchimp's inliner is enabled, it handles class selectors, ID selectors, descendant combinators, and pseudo-classes; media queries and `@import` are left alone in the `<style>` block (which is correct — media queries can't be inlined). Mailchimp's docs describe the behaviour at https://mailchimp.com/help/use-the-css-inliner/.

## When to pre-inline yourself

Since Mailchimp's inliner is opt-in, pre-inlining is the safer default for any send where you want a deterministic artifact. Pre-inline when:

1. **You want consistent output regardless of campaign settings** — pre-inlined HTML doesn't depend on whether the editor remembered to tick the CSS Inliner box.
2. **You want to test the final HTML before sending** — pre-inlining gives you a deterministic artifact to run through Litmus / Email on Acid / Mailchimp's own Inbox Preview.
3. **You're sending the same HTML through both Mailchimp and Mandrill** — Mandrill (Mailchimp Transactional) doesn't run an inliner, so a pre-inlined source is portable.
4. **You're shipping the HTML to a client who'll upload it themselves** — they may not enable the inliner toggle, or may be on a Mailchimp plan or account where behaviour varies.

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
img { display: block; border: 0; outline: none; text-decoration: none; }
```

These survive in `<style>` for clients that respect it (Apple Mail, Outlook.com, Outlook 365 web, Gmail mobile). When a client strips or drops `<style>` (Gmail web on parse error, the GANGA non-Gmail account path), your responsive breakpoints and dark mode rules silently degrade — the email falls back to whatever you inlined.

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
| Mobile layout broken in Gmail web | `@media` rule was the only thing setting widths; nothing inline. Gmail web may also have dropped the `<style>` block on a parse error or size budget. | Add inline widths as default, use `@media` to override |
| Dark mode swap doesn't fire | `@media (prefers-color-scheme: dark)` got inlined or stripped | Verify `--preserve-media-queries` in juice config |
| Buttons lose styling in Gmail | `.button` class was in `<style>` only, Gmail mobile remapped the class name and broke the match | Inline button styles directly on the `<a>` / `<td>`, AND keep the class for media-query overrides |
| Classic Outlook ignores `text-align:center` on a `<div>` | Word rendering engine reads the HTML `align="center"` attribute, not CSS `text-align` on a `<div>` | Set `align="center"` as an HTML attribute alongside the CSS (does not affect other Outlooks) |
| `!important` lost after inlining | Inliner stripped it; `!important` is required so the inlined desktop value doesn't beat the `@media` override at the breakpoint | Use `--preserve-important` |
