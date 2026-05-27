# Language Detection & the `MC_LANGUAGE` Field

How Mailchimp captures, stores, and exposes the language preference for each contact. The full surface that the conditional-content and segments paths both depend on.

## What the field is

Language is a **system-level contact attribute**, not a custom merge field. Every contact in every audience has one. Its value is either an ISO 639-1 language code (with optional locale suffix) or the string `"Not yet detected"` if Mailchimp hasn't determined a value yet.

Two merge tags read it (https://mailchimp.com/help/all-the-merge-tags-cheat-sheet/):

| Tag | Returns |
|---|---|
| `*\|MC_LANGUAGE\|*` | The ISO code — e.g. `en`, `fr`, `nl`, `de`, `fr_CA` |
| `*\|MC_LANGUAGE_LABEL\|*` | The English-language name — e.g. `English`, `French`, `Dutch`, `Canadian French`. Note: always English label text, regardless of the recipient's language |

The cheat sheet entry for the code: *"Displays the language code for a particular contact. For example, if your contact's language is set to English, the merge tag output will display the code **en**."*

## How it gets set

Per https://mailchimp.com/help/view-and-edit-contact-languages/, Mailchimp populates this field through five paths:

1. **Browser language auto-detection** — *"Mailchimp attempts to detect each contact's browser language when they join your audience, update their profile, or click links in your emails."* Default behavior; runs on three events (signup / profile update / link click). Contacts created via API or import without a language stay `"Not yet detected"` until one of those events triggers detection.
2. **Hosted / embedded signup form field** — add a "Language" field to the form. Subscriber picks at signup.
3. **CSV import** — include a `Language` column in the import file with valid ISO codes. Mailchimp will set the field on each imported contact.
4. **Manual edit** — set on a single contact via their profile page in the audience.
5. **API** — set via the Marketing API's `language` field on the subscriber object.

Mailchimp's UI shows `"Not yet detected"` for contacts whose language hasn't been set. In conditional content, that maps to `*|MC_LANGUAGE|*` returning an empty / non-matching value — which is why every conditional block needs an `*|ELSE:|*` fallback.

## Accepted ISO codes

The full set Mailchimp documents, copied verbatim from the help doc:

```
en   English (default)
ar   Arabic
af   Afrikaans
be   Belarusian
bg   Bulgarian
ca   Catalan
zh   Chinese
hr   Croatian
cs   Czech
da   Danish
nl   Dutch
et   Estonian
fa   Persian (Farsi)
fi   Finnish
fr   French (France)
fr_CA  French (Canada)
de   German
el   Greek
he   Hebrew
hi   Hindi
hu   Hungarian
is   Icelandic
id   Indonesian
ga   Irish
it   Italian
ja   Japanese
km   Khmer
ko   Korean
lv   Latvian
lt   Lithuanian
mt   Maltese
ms   Malay
mk   Macedonian
no   Norwegian
pl   Polish
pt   Portuguese (Brazil)
pt_PT  Portuguese (Portugal)
ro   Romanian
ru   Russian
sr   Serbian
sk   Slovak
sl   Slovenian
es   Spanish (Mexico)
es_ES  Spanish (Spain)
sw   Swahili
sv   Swedish
ta   Tamil
th   Thai
tr   Turkish
uk   Ukrainian
vi   Vietnamese
```

Mailchimp's doc is emphatic: *"To function correctly, language codes must be formatted exactly as shown."* Underscore — not hyphen — separates locale variants (`fr_CA`, not `fr-CA`). Case matters.

## What's NOT in the accepted set

Several variants you might expect from BCP 47 are absent. Treat the absence as the rule, not an oversight:

| Expected | Actually accepted | Implication |
|---|---|---|
| `de_CH` (Swiss German) | `de` only | Swiss German contacts get the German variant for segment matching |
| `it_CH` (Swiss Italian) | `it` only | Same — collapses to base |
| `rm` (Romansh) | not in list | Romansh-speaking Swiss contacts can't be distinguished at the field level |
| `zh_Hant` / `zh-TW` (Traditional Chinese) | `zh` only | All Chinese readers collapse to one code; no way to distinguish Simplified vs Traditional in `MC_LANGUAGE` |
| `en_GB`, `en_AU`, `en_IN` | `en` only | English locale variants collapse |
| `de_AT`, `de_DE` | `de` only | German locale variants collapse |
| `nl_BE` (Flemish) | `nl` only | Flemish collapses to Dutch |

If the user needs to distinguish at finer granularity than Mailchimp's accepted set allows — e.g. NL-BE Flemish vs NL-NL Dutch — the field alone won't do it. Options:

- Use a **custom merge field** ("Country" or "Region") in parallel with `MC_LANGUAGE`, then write conditionals against both: `*|IF:MC_LANGUAGE=nl|**|IF:COUNTRY=BE|*Flemish content*|END:IF|**|END:IF|*`.
- Use **audience groups** (e.g. "Region" group with members per country) and reference them via `*|INTERESTED:Region:Belgium|*…*|END:INTERESTED|*`.
- Use **segments** based on a combination of `Language` + custom field, and send separate campaigns.

This is one of the cases where the `MC_LANGUAGE` field's coarseness matters.

## The "Not yet detected" default

For a contact whose language isn't set:

- The UI shows `"Not yet detected"`.
- `*|MC_LANGUAGE|*` returns an empty / non-matching value at send time (Mailchimp's docs don't formally specify the exact return value; treat any conditional comparison against it as failing).
- `*|MC_LANGUAGE_LABEL|*` is similarly empty.
- Conditional blocks that only check for specific languages will fall through to the `*|ELSE:|*` branch (or render nothing if no `ELSE` is provided).

This is the single most important reason every conditional block needs a fallback — newly imported audiences can have a meaningful chunk of `"Not yet detected"` contacts until they engage with an email or update their profile.

## Capturing language at signup

Two patterns:

### Auto-detection (default, no UI changes)

The browser-language path: Mailchimp captures the browser's `Accept-Language` header when the contact submits the signup form or clicks a campaign link. No work on the brand's part. Good enough for many cases; weakness is that it captures the contact's *browser* language, not necessarily their *preferred reading* language (someone using English-language Chrome may still prefer French).

### Explicit "Language" field on the signup form

Add a Language field to the hosted/embedded signup form:

1. In Mailchimp: Audience → Signup forms → Form builder → Add a field → Language.
2. The field renders as a dropdown of Mailchimp's accepted languages.
3. Subscriber's choice is written to the system Language field on submission.

Recommended for any audience where language matters editorially. The choice is conscious, not inferred from browser headers.

## Surfacing it in conditional content

Once `MC_LANGUAGE` is populated, the conditional syntax is the standard `*|IF:...|*` family:

```
*|IF:MC_LANGUAGE=fr|*
  Bonjour *|FNAME|fallback:there|*,
*|ELSEIF:MC_LANGUAGE=nl|*
  Hallo *|FNAME|fallback:there|*,
*|ELSEIF:MC_LANGUAGE=de|*
  Hallo *|FNAME|fallback:there|*,
*|ELSE:|*
  Hello *|FNAME|fallback:there|*,
*|END:IF|*
```

See `conditional-content.md` for the full set of patterns: per-language hero, CTA, compliance footer, signature, fallback strategy.

## Quick checklist before relying on `MC_LANGUAGE`

Before building a campaign that depends on this field, confirm:

- [ ] The audience has been sending email long enough for browser auto-detection to populate values (or an explicit signup-form Language field has been collecting values).
- [ ] You can answer "what percent of this audience has `Language = Not yet detected`?" — if it's high, the `*|ELSE:|*` fallback becomes the *primary* delivery for those contacts.
- [ ] The languages you plan to target are all in Mailchimp's accepted set (or you've planned a custom-field workaround for the unsupported variants).
- [ ] The fallback language is acceptable as a delivery for unknown-language contacts.
