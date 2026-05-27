# Conditional Content per Language

The `*|IF:MC_LANGUAGE=...|*` pattern: how to vary content in the body of a single campaign so each recipient sees their own language. Use this when the segments-vs-conditional decision (see `segments-vs-conditional.md`) lands on the conditional-content path or a hybrid.

## The core pattern

The documented syntax, verbatim from https://mailchimp.com/help/use-conditional-merge-tag-blocks/:

```
*|IF:MC_LANGUAGE=es|*
  Spanish content here.
*|ELSE:|*
  Display English content for everyone else.
*|END:IF|*
```

Extended to multiple languages with `*|ELSEIF:|*`:

```
*|IF:MC_LANGUAGE=fr|*
  French content here.
*|ELSEIF:MC_LANGUAGE=nl|*
  Dutch content here.
*|ELSEIF:MC_LANGUAGE=de|*
  German content here.
*|ELSE:|*
  English fallback for everyone else (including "Not yet detected").
*|END:IF|*
```

## Hard rules

These are the same rules that govern any `*|IF:...|*` block in MCTL, applied to language. See `mailchimp-template-language → references/merge-tags.md` for the underlying conditional grammar.

- **Case sensitive.** Mailchimp's doc: *"Conditional merge tags are case sensitive, and won't work if there are typos, extra spaces, or missing spaces."* Match the lowercase ISO codes Mailchimp stores. `MC_LANGUAGE=FR` won't match anyone.
- **Always provide `*|ELSE:|*`.** Without one, subscribers whose language doesn't match any branch — including the entire `"Not yet detected"` cohort — get no content for that block. An empty hero section is worse than the wrong language.
- **A block must open and close in the same `mc:edit` region.** Splitting an `IF` across two editable regions silently breaks at send time. If a long block spans what would naturally be two sections, restructure the `mc:edit` regions to keep the conditional whole, or split the conditional into per-region copies.
- **Locale variants don't fall through.** `*|IF:MC_LANGUAGE=fr|*` matches `fr` exactly, not `fr_CA`. If you want both, check both: `*|IF:MC_LANGUAGE=fr|**|ELSEIF:MC_LANGUAGE=fr_CA|*…` — or chain them with `*|IFNOT|*`. There's no string-prefix match in MCTL.
- **No boolean AND/OR in a single `IF`.** Nesting or `ELSEIF` is the only way to combine conditions. For "French OR French-Canadian," use `*|IF:MC_LANGUAGE=fr|*…*|ELSEIF:MC_LANGUAGE=fr_CA|*…` with identical content in both branches, or extract the shared content to a wrapping conditional.

## Common patterns

### Per-language greeting

```html
<h1 style="...">
  *|IF:MC_LANGUAGE=fr|*Bonjour *|FNAME|fallback:|*,*|END:IF|*
  *|IF:MC_LANGUAGE=nl|*Hallo *|FNAME|fallback:|*,*|END:IF|*
  *|IF:MC_LANGUAGE=de|*Hallo *|FNAME|fallback:|*,*|END:IF|*
  *|IFNOT:MC_LANGUAGE|*Hello *|FNAME|fallback:there|*,*|END:IF|*
</h1>
```

`*|IFNOT:MC_LANGUAGE|*` catches the unset case explicitly. (The skill flagged `|fallback:` as undocumented community lore — feel free to substitute the documented `*|IF:FNAME|*…*|ELSE:|*…*|END:IF|*` form if you want guaranteed behavior.)

### Per-language hero block (full section)

```html
<tr>
  <td mc:edit="hero" align="center" style="padding:32px 24px;">

    *|IF:MC_LANGUAGE=fr|*
      <h1 style="margin:0 0 16px 0; ...">Nouveautés du mois</h1>
      <p style="margin:0 0 24px 0; ...">Découvrez ce que nous avons préparé pour vous.</p>
      <a href="..." style="...">Lire la suite</a>
    *|ELSEIF:MC_LANGUAGE=nl|*
      <h1 style="margin:0 0 16px 0; ...">Nieuws van de maand</h1>
      <p style="margin:0 0 24px 0; ...">Ontdek wat we voor u hebben voorbereid.</p>
      <a href="..." style="...">Lees verder</a>
    *|ELSEIF:MC_LANGUAGE=de|*
      <h1 style="margin:0 0 16px 0; ...">Neuigkeiten des Monats</h1>
      <p style="margin:0 0 24px 0; ...">Entdecken Sie, was wir für Sie vorbereitet haben.</p>
      <a href="..." style="...">Weiterlesen</a>
    *|ELSE:|*
      <h1 style="margin:0 0 16px 0; ...">This month's update</h1>
      <p style="margin:0 0 24px 0; ...">Discover what we've prepared for you.</p>
      <a href="..." style="...">Read more</a>
    *|END:IF|*

  </td>
</tr>
```

Notes on this shape:
- All four branches sit inside one `mc:edit="hero"` region — the conditional doesn't span editable boundaries.
- Each branch contains parallel structure (same heading level, same CTA pattern) so the rendered result has matching visual weight across languages.
- The `*|ELSE:|*` branch is the brand's primary language and serves as the fallback for `"Not yet detected"` contacts.

### Per-language CTA (small block)

```html
<a href="https://example.com/sign-up?lang=*|MC_LANGUAGE|*" style="...display:inline-block;...">
  *|IF:MC_LANGUAGE=fr|*S'inscrire*|END:IF|*
  *|IF:MC_LANGUAGE=nl|*Inschrijven*|END:IF|*
  *|IF:MC_LANGUAGE=de|*Anmelden*|END:IF|*
  *|IFNOT:MC_LANGUAGE|*Sign up*|END:IF|*
</a>
```

The `lang=*|MC_LANGUAGE|*` query parameter passes the recipient's language to the landing page, useful for keeping the experience consistent post-click. Use `*|URL:MC_LANGUAGE|*` if the value needs URL-encoding (it doesn't here — ISO codes are URL-safe).

### Per-language compliance footer

```html
<td mc:edit="footer" style="...">
  <p style="margin:0 0 12px 0;">
    &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*
  </p>
  <p style="margin:0 0 12px 0;">
    *|HTML:LIST_ADDRESS_HTML|*
  </p>
  <p style="margin:0;">
    *|IF:MC_LANGUAGE=fr|*
      <a href="*|UNSUB|*">Se désinscrire</a>
      &middot;
      <a href="*|UPDATE_PROFILE|*">Modifier les préférences</a>
    *|ELSEIF:MC_LANGUAGE=nl|*
      <a href="*|UNSUB|*">Uitschrijven</a>
      &middot;
      <a href="*|UPDATE_PROFILE|*">Voorkeuren wijzigen</a>
    *|ELSEIF:MC_LANGUAGE=de|*
      <a href="*|UNSUB|*">Abmelden</a>
      &middot;
      <a href="*|UPDATE_PROFILE|*">Einstellungen bearbeiten</a>
    *|ELSE:|*
      <a href="*|UNSUB|*">Unsubscribe</a>
      &middot;
      <a href="*|UPDATE_PROFILE|*">Update preferences</a>
    *|END:IF|*
  </p>
</td>
```

Notes:
- The merge tags (`*|UNSUB|*`, `*|HTML:LIST_ADDRESS_HTML|*`, `*|CURRENT_YEAR|*`, `*|LIST:COMPANY|*`) are **not translated** — they're substitutions. Only the link *labels* (Unsubscribe / Update preferences) change per language.
- The compliance footer must appear for **every** language version. Don't tuck it inside a single-language branch.
- Address line `*|HTML:LIST_ADDRESS_HTML|*` is the audience's mailing address, formatted by Mailchimp — same for all languages.

### Per-language preheader

The preview text is hidden body content; it can be conditional like any other body block:

```html
<div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">
  *|IF:MC_LANGUAGE=fr|*Découvrez nos nouveautés du mois.*|END:IF|*
  *|IF:MC_LANGUAGE=nl|*Ontdek onze nieuws van de maand.*|END:IF|*
  *|IF:MC_LANGUAGE=de|*Entdecken Sie unsere Neuigkeiten des Monats.*|END:IF|*
  *|IFNOT:MC_LANGUAGE|*Discover this month's update.*|END:IF|*
</div>
```

But: the `*|MC_PREVIEW_TEXT|*` tag (set in campaign settings) **cannot** be made conditional — campaign settings are global per campaign. If you need per-language preview text alongside the subject line, you're on the segments-with-separate-campaigns path, not the conditional-content path.

## Worked examples by region

### Belgium — single audience, NL/FR

```
*|IF:MC_LANGUAGE=nl|*…Nederlandse inhoud…*|ELSEIF:MC_LANGUAGE=fr|*…contenu français…*|ELSE:|*…fallback (typically NL or FR depending on majority audience)…*|END:IF|*
```

Decide the `*|ELSE:|*` based on which language is the larger share of the audience or which is the brand's primary. German (`de`) covers the small German-speaking community in eastern Belgium — add a fourth branch if relevant.

### Switzerland — single audience, DE/FR/IT (RM unsupported)

```
*|IF:MC_LANGUAGE=de|*…Deutscher Inhalt…*|ELSEIF:MC_LANGUAGE=fr|*…contenu français…*|ELSEIF:MC_LANGUAGE=it|*…contenuto italiano…*|ELSE:|*…German fallback or whichever is dominant…*|END:IF|*
```

Romansh (`rm`) is not in Mailchimp's accepted set (see `language-detection.md`). Romansh-speaking contacts will either be set to `de` (their second-most-likely language) or `"Not yet detected"`. There's no clean way to address them separately via `MC_LANGUAGE` alone.

### Canada — single audience, EN/FR

```
*|IF:MC_LANGUAGE=fr_CA|*…contenu français (Canada)…*|ELSEIF:MC_LANGUAGE=fr|*…contenu français (France)…*|ELSE:|*…English fallback…*|END:IF|*
```

Note `fr_CA` is in Mailchimp's accepted set (one of the few locale variants). Decide whether to fold France-French and Canadian-French into one branch or distinguish them based on whether the copy differs (vocabulary, currency references, regulatory language).

### Singapore — single audience, EN/ZH/MS/TA

```
*|IF:MC_LANGUAGE=zh|*…中文内容…*|ELSEIF:MC_LANGUAGE=ms|*…kandungan Melayu…*|ELSEIF:MC_LANGUAGE=ta|*…தமிழ் உள்ளடக்கம்…*|ELSE:|*…English fallback…*|END:IF|*
```

All four languages are in Mailchimp's accepted set. The `lang` attribute on `<html>` should reflect the dominant language of the campaign (likely `en` for fallback) — set per-segment if you split into separate campaigns later.

## Template-level concerns to remember

The conditional content makes the body multilingual. The *template* must still support all the languages it'll carry. Pass these to the template-language skill's typography reference:

- **Character coverage**: every script must have a viable font in the stack. For Tamil (`ta`), Khmer (`km`), or Thai (`th`), Arial alone won't render correctly — see `mailchimp-template-language/references/typography.md` for per-script stacks.
- **RTL languages**: Arabic (`ar`), Hebrew (`he`), Persian (`fa`), and Urdu (none in Mailchimp's accepted set) need `dir="rtl"`. In a conditional-content campaign with mixed LTR and RTL, the page-level `<html dir="...">` can't switch — set `dir="rtl"` on the conditional element instead, or accept that mixed-direction in one campaign is hard and split into separate campaigns per direction.
- **`lang` attribute**: on `<html>`, the value should match the *primary* (fallback) language of the campaign. For finer granularity, set `lang` on each conditional block: `<div lang="fr">…French content…</div>`.

## When NOT to use conditional content

Reach for the segments-with-separate-campaigns path instead when:

- The subject line / preheader (the *|MC_PREVIEW_TEXT|* tag's value, set in campaign settings) / from-name / send time must differ per language. Conditional content can't reach those.
- Per-language reporting matters (open rate per language, click rate per language). Conditional content reports as one campaign; segments report independently.
- The languages are very long-form (whole article, not a section) and stuffing all of them into one HTML body would push the campaign past Gmail's ~102 KB clipping threshold.
- The languages need significantly different *layouts*, not just different copy.

See `segments-vs-conditional.md` for the full decision tree.
