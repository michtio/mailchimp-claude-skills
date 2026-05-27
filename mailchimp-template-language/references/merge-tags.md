# Merge Tags

Merge tags are `*|TAG|*` strings that Mailchimp substitutes per recipient at send time. They work in the subject line, preheader, body content, and (for some tags) link URLs.

## Required tags — must be in every campaign

These are compliance-mandated. Omitting them either fails the send or causes Mailchimp to inject its own footer over your design.

| Tag | What it produces | Required? |
|---|---|---|
| `*|UNSUB|*` | One-click unsubscribe URL | YES — must be in a clickable link |
| `*|LIST:ADDRESS|*` | Audience's physical mailing address (CAN-SPAM, GDPR) | YES |
| `*|HTML:LIST:ADDRESS_HTML|*` | Same address, pre-formatted HTML | Alternative to above |
| `*|LIST:COMPANY|*` | Audience's organization name | Recommended |
| `*|CURRENT_YEAR|*` | Current 4-digit year | Recommended (copyright lines) |

### Minimal compliant footer

```html
<tr>
  <td mc:edit="footer" align="center" style="padding:24px; font-family:Arial,Helvetica,sans-serif; font-size:12px; line-height:18px; color:#888;">
    <p style="margin:0 0 12px 0;">
      &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*. All rights reserved.
    </p>
    <p style="margin:0 0 12px 0;">
      *|HTML:LIST:ADDRESS_HTML|*
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
| `*|MC:DATE|*` | Send date in default format |
| `*|MC:DATE:m/d/Y|*` | Send date with PHP-style format string |
| `*|ARCHIVE|*` | URL to the web-archived version of the email |
| `*|FORWARD|*` | URL to "forward to a friend" form |
| `*|UPDATE_PROFILE|*` | URL to subscriber's preferences page |
| `*|REWARDS|*` | "Powered by Mailchimp" referral link (free plans only) |
| `*|MC:TOC|*` | Table of contents (legacy, rarely used) |
| `*|MC:TOC_ANCHOR|*` | Anchor marker for the TOC |

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
| `*|BIRTHDAY|*` | Birthday |
| `*|MMERGE3|*`, `*|MMERGE4|*`, etc. | Custom fields by index (legacy) |

Custom field tags use whatever was set in audience settings — e.g., `*|COMPANY|*`, `*|JOBTITLE|*`. Check the audience's merge fields before assuming tags exist.

### Default values

Always provide a fallback for personalization. `Hi *|FNAME|*` produces `Hi ` when the field is blank — ugly. Use:

```
Hi *|FNAME|*,    →    Hi *|IF:FNAME|**|FNAME|**|ELSE:|*there*|END:IF|*,
```

Or the shorter syntax:

```
Hi *|FNAME|fallback:there|*,
```

Either way produces "Hi Friend," for known recipients and "Hi there," for unknowns.

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

*|IF:COUNTRY=BE|*Verzending naar België.*|END:IF|*
*|IF:PLAN!=FREE|*Premium content here.*|END:IF|*
```

**Important caveat:** for numeric comparisons (`<`, `>`, `<=`, `>=`) to behave predictably, the merge field must be configured as a **number-type field** in the audience settings. Comparing text-type fields with numeric operators produces inconsistent results because Mailchimp's parser falls back to string comparison.

### No AND / OR inside a single condition

Mailchimp evaluates the entire string inside `*|IF:...|*` literally. There is no boolean AND/OR — `*|IF:COUNTRY=BE AND PLAN=PRO|*` will not work. Chain conditions with `*|ELSEIF:|*` or nest:

```
*|IF:COUNTRY=BE|*
  *|IF:PLAN=PRO|*Pro content for Belgian subscribers*|END:IF|*
*|END:IF|*
```

### Truthy/falsy (when no operator is used)

- Empty string, missing field, or literal `0` → falsy.
- Any non-empty value → truthy.

So `*|IF:DISCOUNT_CODE|*Use code *|DISCOUNT_CODE|* at checkout.*|END:IF|*` shows nothing for subscribers without a discount code.

### Nesting

Conditionals can nest. Keep nesting shallow — Mailchimp's parser tolerates two or three levels but readability collapses fast. If you need more, restructure with `*|ELSEIF|*`.

### Block-scope requirement

A conditional must open and close within the same content block (the same `mc:edit` region, or the same top-level body if no editable regions). Splitting an `*|IF:...|*` across two `mc:edit` regions silently breaks at send time.

## Date and number formatting

```
*|DATE:Y|*               4-digit year
*|DATE:F j, Y|*          March 22, 2026
*|DATE:d/m/Y|*           22/03/2026
*|DATE:Y-m-d|*           2026-03-22
```

PHP date format characters. The `*|DATE|*` tag without a format gives the send date in audience-localized format.

For arithmetic on dates:

```
*|DATE_ADD:+1 week:F j, Y|*    Date one week from send
*|DATE_ADD:-30 days|*           30 days ago
```

## URL tags

Tags in `href` attributes get expanded too:

```html
<a href="https://example.com/?email=*|URL:EMAIL|*">View your account</a>
<a href="*|MC:URL|*">View in browser</a>
```

`*|URL:TAG|*` URL-encodes the value. Use it for query parameters; without it, special characters break links.

## Audience and campaign metadata

| Tag | Output |
|---|---|
| `*|LIST:NAME|*` | Audience name |
| `*|LIST:COMPANY|*` | Audience's company name |
| `*|LIST:DESCRIPTION|*` | Audience description |
| `*|LIST:SUBSCRIBE|*` | Signup form URL |
| `*|LIST:UNSUBSCRIBE|*` | Hosted unsubscribe page URL |
| `*|TRANSLATE:lang|*` | Translation of a sentence to a target language |
| `*|INTERESTS|*` | List of subscriber's interests (group memberships) |

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
