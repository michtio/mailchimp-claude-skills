# Responsive Email

## Table of contents

1. [The two responsive strategies](#the-two-responsive-strategies)
2. [Fluid hybrid pattern](#fluid-hybrid-pattern)
3. [Media-query mobile rules](#media-query-mobile-rules)
4. [Dark mode](#dark-mode)
5. [Bulletproof buttons](#bulletproof-buttons)
6. [Images](#images)
7. [Font handling](#font-handling)
8. [Common rendering pitfalls](#common-rendering-pitfalls)
9. [Testing matrix](#testing-matrix)

---

## The two responsive strategies

1. **Fluid hybrid** (recommended): tables use percentage widths inside a max-width wrapper. Works in Gmail (which strips `<style>`) without any media queries. Default approach.
2. **Media-query responsive**: fixed-width desktop layout that collapses via `@media (max-width:600px)`. Works everywhere except Gmail's most aggressive stripping. Use as enhancement, not foundation.

Combine both: build fluid hybrid as the base, then layer media queries for nice-to-haves.

## Fluid hybrid pattern

The two-column block that collapses to one column on mobile, without media queries:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr>
    <td align="center" valign="top">

      <!-- Outlook-only fixed width -->
      <!--[if mso]>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600">
        <tr>
          <td width="290" valign="top">
      <![endif]-->

      <!-- Modern clients: inline-block, fluid -->
      <div style="display:inline-block; vertical-align:top; width:100%; max-width:290px;" class="stack">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
          <tr>
            <td mc:edit="left_column" style="padding:16px; font-family:Arial,sans-serif;">
              <h3>Left column</h3>
              <p>Content here.</p>
            </td>
          </tr>
        </table>
      </div>

      <!--[if mso]>
          </td>
          <td width="290" valign="top">
      <![endif]-->

      <div style="display:inline-block; vertical-align:top; width:100%; max-width:290px;" class="stack">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
          <tr>
            <td mc:edit="right_column" style="padding:16px; font-family:Arial,sans-serif;">
              <h3>Right column</h3>
              <p>Content here.</p>
            </td>
          </tr>
        </table>
      </div>

      <!--[if mso]>
          </td>
        </tr>
      </table>
      <![endif]-->

    </td>
  </tr>
</table>
```

How it works:
- Outlook sees fixed-width tables inside MSO conditionals.
- Everything else sees `<div>`s with `display:inline-block` and `max-width:290px`. When viewport < 580px, the second div wraps to a new line (no media query needed).
- The `.stack` class is the media-query enhancement layer — sets `display:block; width:100%` on small screens for explicit stacking.

## Media-query mobile rules

The basics that every responsive template needs:

```css
@media screen and (max-width: 600px) {
  /* Force container to full width */
  .container { width: 100% !important; max-width: 100% !important; }

  /* Stack two-column layouts */
  .stack { display: block !important; width: 100% !important; max-width: 100% !important; }

  /* Hide elements that don't make sense on mobile */
  .hide-mobile { display: none !important; }

  /* Show elements only on mobile */
  .show-mobile {
    display: block !important;
    width: auto !important;
    max-height: none !important;
    overflow: visible !important;
  }

  /* Bigger touch targets */
  .button-mobile {
    width: 100% !important;
    padding: 16px 24px !important;
    box-sizing: border-box !important;
  }

  /* Bigger headlines */
  h1 { font-size: 24px !important; line-height: 32px !important; }
  h2 { font-size: 20px !important; line-height: 28px !important; }

  /* Tighter padding */
  .padding-mobile { padding: 16px !important; }

  /* Center-align on mobile */
  .text-center-mobile { text-align: center !important; }

  /* Full-width images */
  .full-width-mobile-img {
    width: 100% !important;
    height: auto !important;
    max-width: 100% !important;
  }
}
```

The `!important` is necessary — email clients have aggressive resets.

## Dark mode

Each major client handles dark mode differently; you can't satisfy all of them perfectly. The big ones:

1. **Apple Mail (macOS, iOS)** — respects `@media (prefers-color-scheme: dark)` and the `color-scheme` meta tag. Doesn't auto-invert your colors by default; the meta tag opts you *into* dark-mode CSS so you can ship your own dark palette.
2. **Outlook.com web** — applies aggressive auto-inversion on light backgrounds. No reliable opt-out exists as of 2026; only mitigation.
3. **Gmail iOS app** — full inversion of light backgrounds, no CSS hook.
4. **Gmail Android app** — partial inversion (it touches some colors, leaves others), no CSS hook.
5. **Gmail web (desktop)** — reportedly respects `prefers-color-scheme` at the OS level since April 2024, but coverage is inconsistent — test rather than assume.

### Meta tag opt-in

```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
```

These signal that the template has been designed to handle both modes, so Apple Mail should respect your `prefers-color-scheme` CSS rather than apply its own light-mode-only adjustments. `supported-color-schemes` is the older Apple-Mail-specific name (since macOS Mojave); `color-scheme` is the cross-browser standard. Including both is defensible belt-and-braces.

### CSS for Apple Mail dark mode

```css
@media (prefers-color-scheme: dark) {
  body, .dark-bg { background-color: #1a1a1a !important; }
  .dark-text { color: #ffffff !important; }
  .dark-text-secondary { color: #bbbbbb !important; }
  .dark-link { color: #4dabf7 !important; }
  .dark-button { background-color: #4dabf7 !important; color: #1a1a1a !important; }

  /* Swap logo: hide light, show dark */
  .light-logo { display: none !important; }
  .dark-logo { display: block !important; }
}
```

### Logo swap pattern

```html
<!-- Light mode logo (default) -->
<img src="https://cdn.example.com/logo-dark.png" width="180" height="40" alt="Brand" class="light-logo" style="display:block;">

<!-- Dark mode logo (hidden by default) -->
<div class="dark-logo" style="display:none; mso-hide:all;">
  <img src="https://cdn.example.com/logo-light.png" width="180" height="40" alt="Brand" style="display:block;">
</div>
```

### Outlook.com auto-inversion

Outlook.com darkens light backgrounds to dark gray automatically. The behavior persists as of 2026 with no reliable opt-out. To preserve dark sections (where text needs to stay white), pair the `bgcolor` HTML attribute with an inline `background-color` style — Outlook.com is less likely to override a section that declares a dark background two ways:

```html
<td bgcolor="#1a1a1a" style="background-color:#1a1a1a;">
  <span style="color:#ffffff;">Stays white on dark</span>
</td>
```

Don't expect perfection — Outlook.com injects `data-ogsb`/`data-ogsc` attributes onto elements at render time and overrides colors selectively. The `bgcolor` + `style` belt-and-braces approach is the best available defense.

(Older guides sometimes recommend `mso-text-raise:0` for this. That property is real but it controls vertical text positioning in classic Outlook *desktop* — Outlook.com is the *web* client and doesn't honor MSO properties at all. It does nothing for auto-inversion.)

## Bulletproof buttons

A button that renders correctly in Outlook (which ignores `padding` on `<a>` tags), Apple Mail, Gmail, and webmail:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="#2563eb" style="border-radius:4px; mso-padding-alt:14px 28px;">
      <!--[if mso]>
      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://example.com" style="height:44px; v-text-anchor:middle; width:200px;" arcsize="10%" stroke="f" fillcolor="#2563eb">
        <w:anchorlock/>
        <center style="color:#ffffff; font-family:Arial,sans-serif; font-size:16px; font-weight:bold;">Click here</center>
      </v:roundrect>
      <![endif]-->
      <!--[if !mso]><!-- -->
      <a href="https://example.com" style="display:inline-block; padding:14px 28px; font-family:Arial,sans-serif; font-size:16px; font-weight:bold; color:#ffffff; text-decoration:none; border-radius:4px; background-color:#2563eb;">
        Click here
      </a>
      <!--<![endif]-->
    </td>
  </tr>
</table>
```

The MSO conditional uses VML (`<v:roundrect>`) to render a real button shape in Outlook. The non-MSO conditional uses standard `<a>` styling for everyone else.

Adapt:
- `arcsize="10%"` controls corner radius. Per Microsoft's VML reference, the value is a percentage of **half the smaller dimension** — on a 44px-tall button, 10% ≈ 2.2px radius (not 4-5px). Increase to 20–25% for a noticeably rounded button on small dimensions.
- `width="200"` (set on the v:roundrect's style) and `height:44px` should approximate the rendered size of the non-MSO version so the two branches line up visually.
- Colors must be duplicated in both branches.
- `mso-padding-alt` on the wrapping `<td>` is intended for the *non-VML* fallback pattern (where Outlook ignores `padding` on `<a>` and the surrounding `<td>` carries the spacing). When you already have a `<v:roundrect>` that sets its own width and height, the property is largely redundant for the Outlook branch — keep it only if you also support clients that fall through to the plain `<a>`.

## Images

### Required attributes on every `<img>`

```html
<img src="https://cdn.example.com/image.jpg"
     width="600"
     height="300"
     alt="Descriptive alt text"
     style="display:block; width:100%; max-width:600px; height:auto; border:0; outline:none; text-decoration:none;">
```

- `width` and `height` as HTML attributes (not just CSS) — Outlook ignores CSS dimensions.
- `style="display:block"` — eliminates the 3-5px ghost gap below images in webmail.
- `alt` always — clients with images-off show this, and screen readers depend on it.
- `border:0; outline:none; text-decoration:none` — kills the blue border that some Outlooks add to linked images.

### Retina images

Serve images at 2x dimensions, constrain with `width`/`height` attributes:

```html
<!-- Source image is 1200x600px -->
<img src="https://cdn.example.com/hero@2x.jpg" width="600" height="300" alt="Hero" style="display:block; width:100%; max-width:600px; height:auto;">
```

### Background images

Classic Outlook for Windows (Word rendering engine) ignores CSS `background-image`. The new Outlook for Windows (WebView2/Chromium), Outlook.com web, Outlook 365 web, and Outlook for Mac all support CSS backgrounds. For templates that need to render correctly in the still-large Classic Outlook installed base, use a VML fallback:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600">
  <tr>
    <td height="300" valign="middle" align="center" background="https://cdn.example.com/hero.jpg" bgcolor="#222" style="background-image:url('https://cdn.example.com/hero.jpg'); background-size:cover; background-position:center; height:300px;">
      <!--[if mso]>
      <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px; height:300px;">
        <v:fill type="frame" src="https://cdn.example.com/hero.jpg" color="#222"/>
        <v:textbox inset="0,0,0,0">
      <![endif]-->
      <div>
        <h1 style="color:#fff; font-family:Arial,sans-serif; font-size:32px; margin:0;">Hero headline</h1>
      </div>
      <!--[if mso]>
        </v:textbox>
      </v:rect>
      <![endif]-->
    </td>
  </tr>
</table>
```

## Font handling

Web fonts:

```html
<!--[if !mso]><!-->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
</style>
<!--<![endif]-->
```

Web-font loading coverage in 2026:

- **Apple Mail (macOS, iOS), Outlook for Mac** — load reliably.
- **Outlook 365 web** — loads for some Exchange / corporate M365 accounts; drops `@font-face` for Microsoft mailbox accounts (`outlook.com`, `live.com`, `hotmail.com`).
- **Gmail web** — does **not** load arbitrary `@import` web fonts. The renderer ships with Roboto and Google Sans preloaded; everything else falls through to the stack.
- **Classic Outlook for Windows (Word engine)** — never loads `@font-face`; always falls through.

Always provide a fallback stack:

```css
font-family: '{{ web-font }}', Arial, Helvetica, sans-serif;
```

(See `typography.md` for token conventions.)

System fonts that work everywhere without import:
- `Arial, Helvetica, sans-serif` (sans-serif)
- `Georgia, 'Times New Roman', serif` (serif)
- `'Courier New', Courier, monospace` (monospace)

Other broadly available system fonts: `Verdana`, `Trebuchet MS`, `Tahoma` (Windows / macOS / iOS). Avoid relying on `Palatino` or `Garamond` cross-platform — Palatino metrics differ between Windows ("Palatino Linotype") and macOS ("Palatino"), and neither is present on Android; Garamond ships only with Office on Windows and is missing on Android entirely.

## Common rendering pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Mystery space below images | `vertical-align: baseline` on inline images reserves descender space | `display:block` on every `<img>` (also fixable with `vertical-align: bottom` or `line-height: 0`) |
| Outlook text gigantic | Windows HiDPI scaling on the Word engine (Outlook 2007–2019 desktop) | `<o:PixelsPerInch>96</o:PixelsPerInch>` in head MSO block |
| Buttons look like links in Outlook | `padding` on `<a>` ignored | Bulletproof button pattern (VML + table) |
| Background colors missing in Outlook | CSS-only bg (Classic Outlook for Windows) | Add `bgcolor="#xxx"` attribute alongside `style` |
| Email looks fine in preview, broken when sent | CSS not inlined | Inline critical CSS via tool or by hand |
| Phone numbers turn blue in iOS | Auto-linkification | `<meta name="format-detection" content="telephone=no">` |
| Gmail clips email at ~102 KB (web; lower thresholds on some mobile clients) | Gmail's clipping limit, with mobile variants clipping smaller | Trim HTML, host images externally, no inline base64 |

## Testing matrix

Minimum coverage before sending to a client:

| Client | Why |
|---|---|
| Classic Outlook for Windows (Word engine, current M365 / LTSC perpetual) | Worst-case desktop renderer; still present in enterprise installs |
| New Outlook for Windows (WebView2/Chromium) | Microsoft's consumer default since April 2026; renders very differently from Classic Outlook — test both |
| Apple Mail (macOS) | Reference modern client |
| iOS Mail | iPhone preview, dark mode test |
| Gmail web | `<style>` size limits, sanitization edge cases |
| Gmail iOS app | Full dark-mode inversion behavior |
| Gmail Android app | Partial dark-mode inversion (different from iOS) |
| Outlook.com web | Auto-inversion behavior |

Office 2016 and 2019 reached end of extended support on 14 October 2025 and are no longer maintained — they're still in field installs but shouldn't be primary QA targets. Microsoft 365 perpetual / LTSC licenses keep Classic Outlook (Word engine) supported through at least 2029.

Use Litmus, Email on Acid, or Mailchimp's built-in Inbox Preview (paid plans). There is no substitute for actual client rendering — desktop browser tools lie.
