# Merge Tags

Merge tags are `*|TAG|*` strings that Mailchimp substitutes per recipient at send time. They work in the subject line, preheader, body content, and (for some tags) link URLs.

## Required tags — must be in every campaign

These are compliance-mandated. Omitting them either fails the send or causes Mailchimp to inject its own footer over your design.

| Tag | What it produces | Required? |
|---|---|---|
| `*|UNSUB|*` | One-click unsubscribe URL | YES — must be in a clickable link |
| `*|LIST:ADDRESS|*` | Audience's physical mailing address, plain text (CAN-SPAM, GDPR) | YES |
| `*|HTML:LIST_ADDRESS_HTML|*` | Same address, pre-formatted HTML, with "Add us to your address book" vCard link | Alternative to above |
| `*|LIST:ADDRESSLINE|*` | Address on a single line | Alternative to above |
| `*|LIST:COMPANY|*` | Audience's organization name | Recommended |
| `*|CURRENT_YEAR|*` | Current 4-digit year | Recommended (copyright lines) |

**Note the underscore in `*|HTML:LIST_ADDRESS_HTML|*`** — between `LIST` and `ADDRESS`, not a colon. This is how Mailchimp's cheat sheet writes it; the colon form (`HTML:LIST:ADDRESS_HTML`) is widely seen in third-party docs but doesn't match Mailchimp's documentation.

### Minimal compliant footer

```html
<tr>
  <td mc:edit="footer" align="center" style="padding:24px; font-family:Arial,Helvetica,sans-serif; font-size:12px; line-height:18px; color:#888;">
    <p style="margin:0 0 12px 0;">
      &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*. All rights reserved.
    </p>
    <p style="margin:0 0 12px 0;">
      *|HTML:LIST_ADDRESS_HTML|*
    </p>
    <p style="margin:0;">
      <a href="*|UNSUB|*" style="color:#888; text-decoration:underline;">Unsubscribe</a>
      &nbsp;|&nbsp;
      <a href="*|UPDATE_PROFILE|*" style="color:#888; text-decoration:underline;">Update preferences</a>
      &nbsp;|&nbsp;
      <a href="*|FORWARD|*" style="color:#888; text-decoration:underline;">Forward to a friend</a>
    </p>
  </td>
</tr>
```

## System tags — populated by Mailchimp

These reflect campaign/audience state. Use them, don't redefine them.

| Tag | Output |
|---|---|
| `*|MC_PREVIEW_TEXT|*` | The preview text set in campaign settings. **Put this in a hidden div as first body child.** |
| `*|MC:SUBJECT|*` | Campaign subject line (useful in the `<title>` tag and "view in browser" headers) |
| `*|MC:DATE|*` | **Send date** in the account-level locale format (MM/DD/YYYY or DD/MM/YYYY). No format argument. |
| `*|DATE:X|*` | **Current date** (at render time) with PHP-style format string `X`. E.g. `*|DATE:Y|*`, `*|DATE:F j, Y|*`. Not the send date — see below. |
| `*|ARCHIVE|*` | URL to the web-archived version of the email. This is also the "view in browser" URL — Mailchimp does not document a separate `*|MC:URL|*` tag despite what some third-party guides suggest. |
| `*|FORWARD|*` | URL to "forward to a friend" form |
| `*|UPDATE_PROFILE|*` | URL to subscriber's preferences page |
| `*|REWARDS|*` | Adds Mailchimp's referral badge to the email |
| `*|MC:TOC|*` | Table of contents — auto-generated from `*|MC:TOC_TEXT|*` markers in the body |
| `*|MC:TOC_TEXT|*` | Companion marker placed on headings; populates the TOC entry text |

`*|MC:DATE|*` ≠ `*|DATE|*`. The first returns the send date in account locale, no format option. The second returns the current date and accepts a format string. The skill's earlier conflation of these was wrong; use the right tag for the right purpose.

### Preview text placement

```html
<body>
  <div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">
    *|MC_PREVIEW_TEXT|*
  </div>
  <!-- rest of email -->
```

Always the first child of `<body>`. Hidden via CSS but read by inbox previewers.

## Subscriber-data tags

Drawn from audience fields. The tag name matches the **merge field tag** (visible in the audience field settings), not the field name.

| Default tag | Field |
|---|---|
| `*|FNAME|*` | First name |
| `*|LNAME|*` | Last name |
| `*|EMAIL|*` | Email address |
| `*|PHONE|*` | Phone |
| `*|ADDRESS|*` | Address |
| `*|MERGE3|*`, `*|MERGE4|*`, etc. | Custom fields by index |

`*|BIRTHDAY|*` and other named tags work *only* if the audience field was explicitly named `BIRTHDAY` (or whatever) in audience settings. Mailchimp's default custom-field pattern is `*|MERGE1|*`, `*|MERGE2|*`, etc., until you rename them. Some older Mailchimp interfaces and API contexts show `MMERGE` (double M) — check the actual audience configuration before assuming a tag exists.

### Default values

Always provide a fallback for personalization. `Hi *|FNAME|*` produces `Hi ` when the field is blank — ugly. Use the conditional form:

```
Hi *|IF:FNAME|**|FNAME|**|ELSE:|*there*|END:IF|*,
```

For audience-wide defaults, Mailchimp also supports setting a **default merge value** in audience field settings — anyone without a `FNAME` value sees the default at send time. See https://mailchimp.com/help/set-default-merge-values/ for the configuration path.

A shorter inline fallback syntax (`*|FNAME|fallback:there|*`) is widely shared in community guides and appears to work in production, but it is **not documented in Mailchimp's current help center**. The `IF/ELSE` form above and the audience-level default are the two documented mechanisms; prefer those if you need certainty.

## Conditional content

The full conditional syntax:

```
*|IF:TAGNAME|*
  Content shown if TAGNAME has a truthy value
*|ELSEIF:OTHERTAG|*
  Content shown if OTHERTAG has a truthy value
*|ELSE:|*
  Content shown otherwise
*|END:IF|*
```

The `ELSEIF` and `ELSE` clauses are optional. Note the trailing colons (`*|ELSE:|*`, `*|END:IF|*`) — those are required by the parser.

### IFNOT — inverse condition

For "show this only when the field is empty/falsy", use `IFNOT` instead of writing an empty IF branch:

```
*|IFNOT:FNAME|*Hey there! It looks like we're missing your name.*|END:IF|*
```

`IFNOT` is what Mailchimp's docs use for the "missing data" pattern. Closes with the same `*|END:IF|*`.

### Comparison operators

Mailchimp supports six operators:

| Operator | Meaning |
|---|---|
| `=` | equal to |
| `!=` | not equal to |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |

Examples (drawn directly from Mailchimp's documentation):

```
*|IF:AGE >= 18|*Don't forget to vote this Tuesday!*|END:IF|*

*|IF:TRANSACTIONS >= 20|*
  Enjoy this 40% off coupon! *|COUPON40|*
*|ELSEIF:TRANSACTIONS >= 10|*
  Enjoy this 20% off coupon! *|COUPON20|*
*|END:IF|*

*|IF:COUNTRY=CA|*Free shipping across Canada.*|END:IF|*
*|IF:PLAN!=FREE|*Premium content here.*|END:IF|*
```

**Important caveat:** for numeric comparisons (`<`, `>`, `<=`, `>=`) to behave predictably, the merge field must be configured as a **number-type field** in the audience settings. Comparing text-type fields with numeric operators produces inconsistent results because Mailchimp's parser falls back to string comparison.

### No AND / OR inside a single condition

Mailchimp evaluates the entire string inside `*|IF:...|*` literally. There is no boolean AND/OR — `*|IF:COUNTRY=BE AND PLAN=PRO|*` will not work. Chain conditions with `*|ELSEIF:|*` or nest:

```
*|IF:COUNTRY=DE|*
  *|IF:PLAN=PRO|*Pro content for subscribers in Germany*|END:IF|*
*|END:IF|*
```

### Truthy/falsy (when no operator is used)

Mailchimp's conditional-blocks doc describes IF in terms of whether the field "has a value": empty / missing → false, present → true. The behavior of edge values like the literal string `0` is not specified in the docs; if the distinction matters for your audience, test it against a real subscriber first.

So `*|IF:DISCOUNT_CODE|*Use code *|DISCOUNT_CODE|* at checkout.*|END:IF|*` shows nothing for subscribers without a discount code.

### Nesting

Conditionals can nest. Keep nesting shallow — Mailchimp's parser tolerates two or three levels but readability collapses fast. If you need more, restructure with `*|ELSEIF|*`.

### Block-scope requirement

A conditional must open and close within the same content block (the same `mc:edit` region, or the same top-level body if no editable regions). Splitting an `*|IF:...|*` across two `mc:edit` regions silently breaks at send time.

## Date and number formatting

```
*|DATE:Y|*               4-digit year (current date at render time)
*|DATE:F j, Y|*          March 22, 2026
*|DATE:d/m/Y|*           22/03/2026
*|DATE:Y-m-d|*           2026-03-22
```

PHP-style date format characters. `*|DATE:X|*` returns the **current date** at render time, formatted by `X`. For the **send date** in the account's locale format, use `*|MC:DATE|*` (no format argument accepted).

Some community guides reference a `*|DATE_ADD:...|*` arithmetic helper for relative dates ("one week from now," "30 days ago"). It is **not documented in Mailchimp's current help center** — if you need date arithmetic, compute the value externally and pass it in as a merge field, or use audience automations that compute relative dates server-side.

## URL tags

Tags in `href` attributes get expanded too:

```html
<a href="https://example.com/?email=*|URL:EMAIL|*">View your account</a>
<a href="*|ARCHIVE|*">View in browser</a>
```

`*|URL:YOUR_MERGETAG|*` URL-encodes the value. Use it for query parameters; without it, special characters break links.

The "view in browser" / web-archive URL is `*|ARCHIVE|*`. Mailchimp does not document a `*|MC:URL|*` tag, despite the name surfacing in some third-party guides — `*|ARCHIVE|*` is the documented form.

## Audience and campaign metadata

| Tag | Output |
|---|---|
| `*|LIST:NAME|*` | Audience name |
| `*|LIST:COMPANY|*` | Audience's company name |
| `*|LIST:DESCRIPTION|*` | Audience description |
| `*|LIST:SUBSCRIBE|*` | Signup form URL |
| `*|TRANSLATE:XX|*` | **Single tag** that inserts a Google Translate link for the campaign archive in language `XX` (e.g. `*|TRANSLATE:fr|*` for French). Not a wrapping block — it does **not** translate inline content. |
| `*|INTERESTED:GroupTitle:GroupName|*…*|END:INTERESTED|*` | Block conditional. Content between the open/close shows only to subscribers in the named interest group. |

The `*|TRANSLATE|*` tag is often misdescribed as a block tag in third-party guides; Mailchimp's docs make it clear it's a single substitution producing a translate-link URL. For per-language content blocks within a campaign, use `*|IF:MC_LANGUAGE=...|*…*|END:IF|*` or audience groups + conditional blocks (the `INTERESTED` pattern).

## Tags Mailchimp does NOT support (common mistakes)

- No loops. `*|FOREACH|*` doesn't exist. Repeatable blocks (`mc:repeatable`) are the editor-side equivalent.
- No template includes/partials. Each template is self-contained.
- No boolean AND/OR inside a single IF. Chain with `*|ELSEIF:|*` or nest. (Comparison operators `<`, `>`, `<=`, `>=`, `=`, `!=` are supported — see above.)
- No tag inside a tag. `*|IF:*|FNAME|*|*` is invalid; you'd write `*|IF:FNAME|*`.
- No arithmetic expressions. `*|IF:AGE+1>=18|*` won't evaluate. Compute the value before sending if you need it, or use `*|DATE_ADD:...|*` for date math (the only documented arithmetic helper).

## Displaying a literal merge tag (escaping)

Mailchimp does not officially document an escape syntax. To display the literal string `*|FNAME|*` in an email body (rare — most often when writing documentation about MCTL inside an email), use **HTML entity encoding** to break the parser's pattern match without changing the rendered output:

```html
*&#124;FNAME|*
```

`&#124;` is the HTML entity for `|`. Mailchimp's parser scans the raw source for the literal byte sequence `*|...|*` and skips this token, but the email client renders the entity as a pipe — so the recipient sees `*|FNAME|*` exactly as intended.

The same trick works for the asterisk if you need it: `&#42;|FNAME|&#42;`. Encode either of the boundary characters; you don't need to encode both pipes.

Alternative: embed the literal text as an image. Heavier but bulletproof for any future parser changes.

## Testing merge tags

Mailchimp's campaign editor has "Preview & Test → Enter preview mode" which fills tags with the data of a chosen subscriber. Always preview against:

1. A subscriber with all custom fields populated.
2. A subscriber with only required fields (email).
3. A test subscriber created via the audience signup form (worst case).

Conditional logic only reveals itself when one of these three diverges from the others.
