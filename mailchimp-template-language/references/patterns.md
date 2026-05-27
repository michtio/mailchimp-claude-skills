# Email Patterns

Brand-neutral building blocks that compose into professional Mailchimp templates. Each pattern shows the structural bones — colors, fonts, and exact spacing are placeholders to fill in per project. Pair these with the type scale and palette tokens you define for the brand (see `typography.md`).

All patterns use `role="presentation"` on layout tables, `cellpadding="0" cellspacing="0" border="0"` on every table, and include the `mc:edit` placement that survives Mailchimp's import.

## Table of contents

1. [Eyebrow → headline → subhead → CTA (section opener)](#1-section-opener)
2. [Repeatable card grid with hideable filler](#2-repeatable-card-grid-with-hideable-filler)
3. [Multi-column footer with social row](#3-multi-column-footer-with-social-row)
4. [Contact / signature block (repeatable)](#4-contact--signature-block)
5. [Image-text alternating row](#5-image-text-alternating-row)
6. [Pull quote / testimonial](#6-pull-quote--testimonial)
7. [Stat / counter row](#7-stat--counter-row)
8. [Divider variants](#8-divider-variants)
9. [Button variants](#9-button-variants)
10. [Stacked feature list (icon + text)](#10-stacked-feature-list)

---

## 1. Section opener

The canonical typographic rhythm used by most professional editorial templates: a small uppercase tracked **eyebrow**, a large **headline**, a softer **subhead**, and a CTA. The hierarchy reads in two seconds even when the recipient is scanning.

```html
<tr>
  <td align="left" valign="top" style="padding:32px 24px;">
    <div mc:edit="section_eyebrow"
         style="font-family:{{ heading-font }}, Arial, sans-serif;
                font-size:11px;
                letter-spacing:0.15em;
                text-transform:uppercase;
                color:{{ color-muted }};
                margin-bottom:12px;">
      Section eyebrow
    </div>

    <h2 mc:edit="section_headline"
        style="margin:0 0 12px 0;
               font-family:{{ heading-font }}, Arial, sans-serif;
               font-size:32px;
               line-height:1.1;
               font-weight:300;
               letter-spacing:-0.015em;
               color:{{ color-foreground }};">
      The section headline goes here
    </h2>

    <p mc:edit="section_subhead"
       style="margin:0 0 20px 0;
              font-family:{{ body-font }}, Arial, sans-serif;
              font-size:14px;
              line-height:1.55;
              color:{{ color-muted }};">
      A subhead paragraph that adds context in one or two sentences.
    </p>

    <!-- CTA: see Pattern 9 -->
  </td>
</tr>
```

**Notes:**
- Letter-spacing `0.15em` on the eyebrow is the convention for small uppercase labels; without it they read as cramped.
- Headline `letter-spacing:-0.015em` tightens large type — counters the visual gap that appears at 32px+.
- `mc:edit` on the eyebrow `<div>` and subhead `<p>` keeps each editable separately in the editor without making the entire section one giant rich-text region.

## 2. Repeatable card grid with hideable filler

Generalized newsletter-section pattern: a section heading plus a horizontal row of cards, where empty card slots get a "coming soon" filler that the editor can toggle off when the slot fills.

```html
<!-- One repeatable "section" containing a 3-card grid -->
<tr mc:repeatable="section">
  <td style="padding:24px;">

    <!-- Section header (mc:edit names auto-scope per repeat instance) -->
    <div mc:edit="section_label" style="...">Section name</div>

    <!-- Card row -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <!-- Card 1 -->
        <td valign="top" width="33%" class="stack" style="padding:8px;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr><td><img mc:edit="card_1_image" src="..." width="175" height="99" alt="" style="display:block; width:100%; height:auto;"></td></tr>
            <tr><td style="padding:12px 0;">
              <div mc:edit="card_1_eyebrow" style="...">Eyebrow</div>
              <div mc:edit="card_1_title" style="...">Card title</div>
              <div mc:edit="card_1_meta" style="...">Meta detail</div>
              <a mc:edit="card_1_cta" href="#" style="...">Read more &rarr;</a>
            </td></tr>
          </table>
        </td>

        <!-- Card 2: same structure, card_2_* names -->
        <!-- Card 3: same structure, card_3_* names -->

        <!-- Filler slot — editor toggles off when card 4 lands -->
        <td valign="top" width="33%" class="stack" mc:hideable="filler" style="padding:8px;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"
                 style="border:1px dashed {{ color-muted }}; border-radius:3px;">
            <tr><td style="padding:24px; text-align:center;">
              <div mc:edit="filler_title" style="...">Coming soon</div>
              <div mc:edit="filler_description" style="...">More items launching next quarter.</div>
            </td></tr>
          </table>
        </td>
      </tr>
    </table>

  </td>
</tr>
```

**Notes:**
- The outer `<tr mc:repeatable="section">` lets the editor clone, reorder, and delete entire sections.
- `mc:edit` names inside a repeatable get **auto-scoped per instance** by Mailchimp — `card_1_title` in instance 1 and instance 2 are independent editable regions in the editor.
- The filler `<td mc:hideable="filler">` is per-section: each repeated section has its own filler toggle.
- `class="stack"` collapses the cards to full width on mobile (defined in `responsive.md`).

## 3. Multi-column footer with social row

Universal footer pattern: brand mark, two or three link columns, social icons, then required compliance block.

```html
<tr>
  <td style="padding:48px 24px 24px 24px; background-color:{{ color-footer-bg }};">

    <!-- Brand + tagline -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td align="left" valign="top" style="padding-bottom:24px;">
          <img mc:edit="footer_logo" src="..." width="120" height="32" alt="Brand" style="display:block;">
          <div mc:edit="footer_tagline" style="margin-top:8px; font-family:{{ body-font }}; font-size:13px; color:{{ color-muted }};">One-line tagline</div>
        </td>
      </tr>
    </table>

    <!-- Link columns -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td valign="top" width="50%" class="stack" mc:edit="footer_col_1" style="padding-right:16px; padding-bottom:24px; font-family:{{ body-font }}; font-size:13px; line-height:1.8;">
          <strong>Product</strong><br>
          <a href="#">Feature one</a><br>
          <a href="#">Feature two</a><br>
          <a href="#">Pricing</a>
        </td>
        <td valign="top" width="50%" class="stack" mc:edit="footer_col_2" style="padding-bottom:24px; font-family:{{ body-font }}; font-size:13px; line-height:1.8;">
          <strong>Company</strong><br>
          <a href="#">About</a><br>
          <a href="#">Careers</a><br>
          <a href="#">Contact</a>
        </td>
      </tr>
    </table>

    <!-- Social row -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="left" style="padding-top:16px;">
      <tr>
        <td style="padding-right:12px;"><a href="#"><img src="..." width="24" height="24" alt="LinkedIn" style="display:block;"></a></td>
        <td style="padding-right:12px;"><a href="#"><img src="..." width="24" height="24" alt="X (Twitter)" style="display:block;"></a></td>
        <td style="padding-right:12px;"><a href="#"><img src="..." width="24" height="24" alt="Instagram" style="display:block;"></a></td>
      </tr>
    </table>

    <!-- Compliance: see merge-tags.md "Minimal compliant footer" -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="padding-top:32px; border-top:1px solid {{ color-divider }};">
      <tr>
        <td mc:edit="footer_compliance" style="padding-top:16px; font-family:{{ body-font }}; font-size:11px; line-height:1.6; color:{{ color-muted }};">
          &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*<br>
          *|HTML:LIST:ADDRESS_HTML|*<br>
          <a href="*|UNSUB|*">Unsubscribe</a> &middot; <a href="*|UPDATE_PROFILE|*">Update preferences</a>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

**Notes:**
- Each link column is one `mc:edit` region — gives the editor rich-text control over an entire column without breaking the layout.
- Social icons stay as a separate row outside the `mc:edit` columns so the editor can't accidentally delete them.
- The compliance block is separated by a divider line and uses its own `mc:edit` so the editor can localize copy (e.g. translate "Unsubscribe") without touching the structural links.

## 4. Contact / signature block

Repeatable, useful for newsletters that name a contact person, multi-author signatures, or per-section contact attribution.

```html
<tr mc:repeatable="contact">
  <td style="padding:16px 24px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td valign="top" width="48" style="padding-right:12px;">
          <img mc:edit="contact_avatar" src="..." width="48" height="48" alt="" style="display:block; border-radius:24px;">
        </td>
        <td valign="top">
          <div mc:edit="contact_label" style="font-family:{{ body-font }}; font-size:11px; text-transform:uppercase; letter-spacing:0.12em; color:{{ color-muted }};">Questions about X?</div>
          <div mc:edit="contact_name" style="font-family:{{ heading-font }}; font-size:15px; font-weight:600; color:{{ color-foreground }};">Person name</div>
          <div mc:edit="contact_meta" style="font-family:{{ body-font }}; font-size:13px; color:{{ color-muted }};">
            <a href="tel:+1234567890">+1 (234) 567-890</a> &middot; <a href="mailto:name@brand.com">name@brand.com</a>
          </div>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

**Notes:**
- `border-radius` on the avatar works in Apple Mail, iOS Mail, modern Outlook; falls back to a square in Outlook 2007–2016. If circular avatars matter, use a pre-cropped circular PNG with transparent corners.
- `tel:` and `mailto:` links — clients on mobile turn these into native actions.

## 5. Image-text alternating row

Newsletter staple: image on one side, copy on the other, alternating direction per row. Mobile collapses to image-on-top.

```html
<!-- Row 1: image left, text right -->
<tr>
  <td style="padding:24px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td valign="middle" width="240" class="stack" style="padding-right:24px;">
          <img mc:edit="row_image" src="..." width="240" height="160" alt="" style="display:block; width:100%; max-width:240px; height:auto; border-radius:4px;">
        </td>
        <td valign="middle" class="stack">
          <div mc:edit="row_eyebrow" style="...">Eyebrow</div>
          <h3 mc:edit="row_title" style="...">Row title</h3>
          <p mc:edit="row_body" style="...">Short body copy.</p>
          <a mc:edit="row_cta" href="#" style="...">Learn more &rarr;</a>
        </td>
      </tr>
    </table>
  </td>
</tr>

<!-- Row 2: text left, image right — swap the two td's -->
```

**Notes:**
- The `class="stack"` cells become full-width on mobile (`<= 600px`), stacking image above text.
- On the alternating row, swap the two `<td>` positions and keep `class="stack"` on both — on mobile both rows look identical (image-on-top), preserving readability.
- `border-radius:4px` on the image is a soft modern touch; Outlook ignores it, modern clients honor it.

## 6. Pull quote / testimonial

```html
<tr>
  <td style="padding:32px 24px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td align="center" style="padding:24px; border-left:3px solid {{ color-accent }};">
          <p mc:edit="quote_body" style="margin:0 0 16px 0; font-family:{{ heading-font }}; font-size:22px; line-height:1.4; font-style:italic; color:{{ color-foreground }};">
            "The quote, set in a generous size, ideally 1–3 short sentences. Long quotes lose impact."
          </p>
          <div mc:edit="quote_attribution" style="font-family:{{ body-font }}; font-size:13px; color:{{ color-muted }};">
            &mdash; Attribution name, Role at Company
          </div>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

**Notes:**
- The `border-left` accent works in all clients; Outlook respects it on `<td>`.
- Em dash (`&mdash;`) before the attribution is the editorial standard.

## 7. Stat / counter row

```html
<tr>
  <td style="padding:32px 24px; background-color:{{ color-subtle-bg }};">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td valign="top" width="33%" align="center" class="stack" style="padding:16px;">
          <div mc:edit="stat_1_value" style="font-family:{{ heading-font }}; font-size:36px; font-weight:300; color:{{ color-foreground }}; line-height:1;">128</div>
          <div mc:edit="stat_1_label" style="font-family:{{ body-font }}; font-size:12px; text-transform:uppercase; letter-spacing:0.12em; color:{{ color-muted }}; margin-top:8px;">Active items</div>
        </td>
        <td valign="top" width="33%" align="center" class="stack" style="padding:16px;">
          <div mc:edit="stat_2_value" style="...">42%</div>
          <div mc:edit="stat_2_label" style="...">Growth YoY</div>
        </td>
        <td valign="top" width="33%" align="center" class="stack" style="padding:16px;">
          <div mc:edit="stat_3_value" style="...">7</div>
          <div mc:edit="stat_3_label" style="...">Countries</div>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

**Notes:**
- Big number + small tracked label is the universal "stat" look. Keep the number font-weight light (200–300) for editorial feel, heavy (600–700) for aggressive marketing feel.
- Stack on mobile.

## 8. Divider variants

```html
<!-- Hairline divider -->
<tr><td style="padding:16px 24px;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr><td style="border-top:1px solid {{ color-divider }}; height:1px; line-height:1px; font-size:1px;">&nbsp;</td></tr>
  </table>
</td></tr>

<!-- Spaced ornament divider -->
<tr><td align="center" style="padding:24px;">
  <span style="font-family:{{ body-font }}; font-size:12px; color:{{ color-muted }}; letter-spacing:0.5em;">&middot; &middot; &middot;</span>
</td></tr>

<!-- Label divider (text in middle of line) -->
<tr><td style="padding:24px;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td width="40%" style="border-bottom:1px solid {{ color-divider }};">&nbsp;</td>
      <td align="center" style="padding:0 12px; font-family:{{ body-font }}; font-size:11px; text-transform:uppercase; letter-spacing:0.15em; color:{{ color-muted }}; white-space:nowrap;">Section break</td>
      <td width="40%" style="border-bottom:1px solid {{ color-divider }};">&nbsp;</td>
    </tr>
  </table>
</td></tr>
```

**Notes:**
- The hairline pattern uses `height:1px; line-height:1px; font-size:1px;` plus `&nbsp;` so Outlook doesn't collapse the row.
- The label divider uses table cells rather than CSS pseudo-elements (which don't work in email).

## 9. Button variants

All bulletproof — render correctly in Outlook desktop, Apple Mail, Gmail, and webmail. The VML branch handles Outlook 2007–2019; the non-MSO branch handles everyone else.

### Solid button (most common)

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="{{ color-accent }}" style="border-radius:4px; mso-padding-alt:12px 24px;">
      <!--[if mso]>
      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="#" style="height:42px; v-text-anchor:middle; width:180px;" arcsize="10%" stroke="f" fillcolor="{{ color-accent }}">
        <w:anchorlock/>
        <center style="color:{{ color-on-accent }}; font-family:{{ body-font }}, Arial, sans-serif; font-size:14px; font-weight:600;">Take action</center>
      </v:roundrect>
      <![endif]-->
      <!--[if !mso]><!-->
      <a href="#" style="display:inline-block; padding:12px 24px; font-family:{{ body-font }}, Arial, sans-serif; font-size:14px; font-weight:600; color:{{ color-on-accent }}; text-decoration:none; border-radius:4px; background-color:{{ color-accent }};">
        Take action
      </a>
      <!--<![endif]-->
    </td>
  </tr>
</table>
```

### Ghost / outlined button (secondary CTA)

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" style="border:1px solid {{ color-accent }}; border-radius:4px; mso-padding-alt:11px 23px;">
      <a href="#" style="display:inline-block; padding:11px 23px; font-family:{{ body-font }}, Arial, sans-serif; font-size:14px; font-weight:600; color:{{ color-accent }}; text-decoration:none;">
        Secondary action
      </a>
    </td>
  </tr>
</table>
```

Outlook will not honor the border via CSS reliably on this one — if Outlook fidelity matters for ghost buttons, fall back to a VML rectangle with `stroke="t"` and `strokecolor="{{ color-accent }}"`.

### Underline-link button (lowest emphasis)

```html
<a href="#" style="font-family:{{ body-font }}, Arial, sans-serif; font-size:13px; font-weight:500; color:{{ color-accent }}; text-decoration:none; border-bottom:1px solid {{ color-accent }}; padding-bottom:1px;">
  Read more &rarr;
</a>
```

For inline tertiary CTAs (read more, view details). The `border-bottom` gives a tight underline that doesn't pick up descender clipping the way `text-decoration:underline` does in some clients.

### Full-width mobile button

Add `class="button-mobile"` to the `<a>` — the mobile CSS in the template (`responsive.md`) expands it to full width with bigger padding for touch targets.

## 10. Stacked feature list

Icon-led feature list, common in transactional confirmations ("here's what's included") and announcement emails.

```html
<tr>
  <td style="padding:24px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">

      <tr mc:repeatable="feature">
        <td valign="top" width="48" style="padding:12px 16px 12px 0;">
          <img mc:edit="feature_icon" src="..." width="32" height="32" alt="" style="display:block;">
        </td>
        <td valign="top" style="padding:12px 0;">
          <div mc:edit="feature_title" style="font-family:{{ heading-font }}; font-size:15px; font-weight:600; color:{{ color-foreground }}; margin-bottom:4px;">Feature title</div>
          <div mc:edit="feature_body" style="font-family:{{ body-font }}; font-size:13px; line-height:1.55; color:{{ color-muted }};">
            One or two sentences describing the feature.
          </div>
        </td>
      </tr>

    </table>
  </td>
</tr>
```

**Notes:**
- `mc:repeatable="feature"` makes the row clonable.
- Icons should be PNG (transparent bg) at 64×64 source dimensions, displayed at 32×32 — retina-sharp on iOS / Apple Mail.
- Keep titles short (3–6 words) and body to one or two lines; if more is needed, the section opener pattern is a better fit.
