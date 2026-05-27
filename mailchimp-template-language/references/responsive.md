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

Three independent dark mode systems exist; you can't satisfy all of them perfectly. Priorities:

1. **Apple Mail (macOS, iOS)** — respects `@media (prefers-color-scheme: dark)`. Mostly opt-in via meta tag.
2. **Outlook.com web** — applies aggressive auto-inversion on light backgrounds. Cannot be fully prevented, only mitigated.
3. **Gmail (Android, iOS)** — partial color shifting, no CSS hook.

### Meta tag opt-in

```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
```

These tell Apple Mail "I designed for both modes, don't auto-invert."

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

Outlook.com darkens light backgrounds to dark gray automatically. To preserve dark backgrounds (where text needs to stay white), wrap the section's background color in a way that won't be inverted:

```html
<td bgcolor="#1a1a1a" style="background-color:#1a1a1a;">
  <span style="color:#ffffff; mso-text-raise:0;">Stays white on dark</span>
</td>
```

The `bgcolor` attribute + `style` belt-and-braces approach is the best available defense. Don't expect perfection.

## Bulletproof buttons

A button that renders correctly in Outlook (which ignores `padding` on `<a>` tags), Apple Mail, Gmail, and webmail:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="#3b82f6" style="border-radius:4px; mso-padding-alt:14px 28px;">
      <!--[if mso]>
      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://example.com" style="height:44px; v-text-anchor:middle; width:200px;" arcsize="10%" stroke="f" fillcolor="#3b82f6">
        <w:anchorlock/>
        <center style="color:#ffffff; font-family:Arial,sans-serif; font-size:16px; font-weight:bold;">Click here</center>
      </v:roundrect>
      <![endif]-->
      <!--[if !mso]><!-- -->
      <a href="https://example.com" style="display:inline-block; padding:14px 28px; font-family:Arial,sans-serif; font-size:16px; font-weight:bold; color:#ffffff; text-decoration:none; border-radius:4px; background-color:#3b82f6;">
        Click here
      </a>
      <!--<![endif]-->
    </td>
  </tr>
</table>
```

The MSO conditional uses VML (`<v:roundrect>`) to render a real button shape in Outlook. The non-MSO conditional uses standard `<a>` styling for everyone else.

Adapt:
- `arcsize="10%"` controls corner radius (10% of height = ~4-5px on a 44px button).
- `width="200"` and `height:44px` should approximate the rendered size of the non-MSO version.
- Colors must be duplicated in both branches.

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

Outlook desktop ignores CSS `background-image`. For hero sections with text over an image, use VML fallback:

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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
</style>
<!--<![endif]-->
```

Outlook will fall through to your `font-family` stack. Always provide a fallback stack:

```css
font-family: '{{ web-font }}', Arial, Helvetica, sans-serif;
```

(See `typography.md` for token conventions.)

System fonts that work everywhere without import:
- `Arial, Helvetica, sans-serif` (sans-serif)
- `Georgia, 'Times New Roman', serif` (serif)
- `'Courier New', Courier, monospace` (monospace)

Common web fonts that work in many clients without `@import` (system-installed): `Verdana`, `Trebuchet MS`, `Tahoma`, `Palatino`, `Garamond`.

## Common rendering pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Mystery space below images | inline-block default | `display:block` on every `<img>` |
| Outlook text gigantic | DPI scaling | `<o:PixelsPerInch>96</o:PixelsPerInch>` in head MSO block |
| Buttons look like links in Outlook | `padding` on `<a>` ignored | Bulletproof button pattern (VML + table) |
| Background colors missing in Outlook | CSS-only bg | Add `bgcolor="#xxx"` attribute alongside `style` |
| Email looks fine in preview, broken when sent | CSS not inlined | Inline critical CSS via tool or by hand |
| Phone numbers turn blue in iOS | Auto-linkification | `<meta name="format-detection" content="telephone=no">` |
| Gmail clips email at 102KB | Gmail's hard limit | Trim HTML, host images externally, no inline base64 |

## Testing matrix

Minimum coverage before sending to a client:

| Client | Why |
|---|---|
| Outlook 2016/2019/365 desktop (Windows) | Worst-case desktop renderer |
| Apple Mail (macOS) | Reference modern client |
| iOS Mail | iPhone preview, dark mode test |
| Gmail web | CSS stripping, common webmail |
| Gmail Android app | Mobile webmail behavior |
| Outlook.com web | Auto-inversion behavior |

Use Litmus, Email on Acid, or Mailchimp's built-in Inbox Preview (paid plans). There is no substitute for actual client rendering — desktop browser tools lie.
