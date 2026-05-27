# Email HTML Structure

The non-negotiable scaffold for any responsive email. Email clients are 1998-era HTML engines wearing 2026 clothes. The structure below is the consensus baseline that survives Outlook 2007+, Apple Mail, iOS Mail, Gmail (web, iOS, Android, Workspace), Outlook.com, and Yahoo Mail.

## Doctype and root

Use HTML 4.01 Transitional. XHTML strict will break Outlook. HTML5 doctype works in modern clients but Outlook desktop is the lowest common denominator.

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
```

The `v:` and `o:` namespaces are required for VML (Outlook-only bulletproof buttons and background images).

## `<head>` block

```html
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>*|MC:SUBJECT|*</title>

  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
        <o:AllowPNG/>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <style>
    table, td, div, h1, h2, h3, h4, p, a { font-family: Arial, Helvetica, sans-serif !important; }
  </style>
  <![endif]-->

  <style type="text/css">
    /* CLIENT-SPECIFIC RESETS */
    body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse; }
    img { -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; }
    a { text-decoration: none; }

    /* MOBILE STYLES - applied by clients that respect <style> */
    @media screen and (max-width: 600px) {
      .container { width: 100% !important; max-width: 100% !important; }
      .stack { display: block !important; width: 100% !important; }
      .hide-mobile { display: none !important; }
      .full-width-mobile { width: 100% !important; }
      .text-center-mobile { text-align: center !important; }
      .padding-mobile { padding: 16px !important; }
      h1 { font-size: 24px !important; line-height: 30px !important; }
    }

    /* DARK MODE - Apple Mail, iOS Mail */
    @media (prefers-color-scheme: dark) {
      .dark-bg { background-color: #1a1a1a !important; }
      .dark-text { color: #ffffff !important; }
    }
  </style>
</head>
```

Notes:
- `x-apple-disable-message-reformatting` prevents iOS from auto-zooming small text.
- `format-detection` stops iOS from linkifying phone numbers and addresses, which then get blue-underlined and look broken on dark backgrounds.
- `mso-table-lspace/rspace: 0pt` removes Outlook's mystery table spacing.
- The MSO conditional inside `<head>` forces Arial in Outlook (web fonts don't load there) and tells Outlook to render at 96dpi instead of 120dpi.

## The body skeleton

Use a three-table nest: outer (full-width background), wrapper (centered container), content (the actual layout). Width: 600px is the standard. 640px is acceptable. Anything wider risks horizontal scrolling in narrow webmail panes.

```html
<body style="margin:0; padding:0; background-color:#f4f4f4; mso-line-height-rule:exactly;">

  <!-- Preview text: shows in inbox preview, hidden in body -->
  <div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">
    *|MC_PREVIEW_TEXT|*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  </div>

  <!-- Outer table: full-bleed background -->
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f4f4f4;">
    <tr>
      <td align="center" valign="top" style="padding:24px 0;">

        <!-- Wrapper: 600px max-width centered container -->
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="container" style="width:600px; max-width:600px; background-color:#ffffff;">

          <!-- Header row -->
          <tr>
            <td align="center" valign="top" mc:edit="header" style="padding:24px;">
              <!-- header content here -->
            </td>
          </tr>

          <!-- Body row -->
          <tr>
            <td align="left" valign="top" mc:edit="body" style="padding:24px; font-family:Arial,Helvetica,sans-serif; font-size:16px; line-height:24px; color:#222222;">
              <!-- body content here -->
            </td>
          </tr>

          <!-- Footer row -->
          <tr>
            <td align="center" valign="top" mc:edit="footer" style="padding:24px; font-family:Arial,Helvetica,sans-serif; font-size:12px; line-height:18px; color:#888888;">
              <!-- footer content + required compliance tags -->
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
```

## Trailing nbsp on preview text

The `&nbsp;` padding after preview text is intentional. Inboxes that show preview text often grab whatever follows the preheader from the body content; padding with non-breaking spaces and zero-width joiners suppresses that.

For extra control:

```html
<div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">
  *|MC_PREVIEW_TEXT|*
</div>
<div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">
  &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
</div>
```

## Why tables

CSS layout (flexbox, grid) does not work reliably in Outlook desktop or older Gmail. Tables with `role="presentation"` (accessibility: tells screen readers it's layout, not data) are the only universally rendering layout primitive. There is no modern alternative for the desktop Outlook market.

## Why `mso-line-height-rule:exactly` on body

Outlook ignores `line-height` on block elements unless this rule is set. Without it, text rendering is unpredictable across MSO versions.

## Why `cellpadding="0" cellspacing="0" border="0"` on every table

Outlook web (the Microsoft 365 webmail) injects default cellpadding/cellspacing/border on tables that omit these attributes. Always set them explicitly, even when you think they're redundant.
