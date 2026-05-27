---
name: mailchimp-template-language
description: Author and edit custom-coded Mailchimp email templates using Mailchimp Template Language (MCTL). Use this skill when the user mentions Mailchimp templates, mc:edit, mc:repeatable, mc:variant, mc:hideable, merge tags like *|FNAME|* or *|UNSUB|*, conditional blocks like *|IF:...|*, importing custom HTML into Mailchimp, MCTL, or building responsive email templates for Mailchimp campaigns. Also use when the user wants to add editable regions, repeatable blocks, or block design variants to an HTML email destined for Mailchimp. Do NOT use for generic transactional email, Mandrill/Handlebars templates, or non-Mailchimp ESPs.
license: MIT
---

# Mailchimp Template Language (MCTL)

## What this skill covers

Authoring **custom-coded HTML email templates** for Mailchimp's "Code your own" template flow: the template language that turns a flat HTML file into a Mailchimp-editable template with drag-and-drop regions, repeatable blocks, block design variants, and conditional content.

Two distinct concerns are merged in MCTL and you must keep them separate:

1. **Template attributes** (`mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, `mc:allowdesignmodule`) — XML-ish attributes added to HTML tags. They control what the Mailchimp **editor** can do with a template. They are evaluated once, at template import time.
2. **Merge tags** (`*|FNAME|*`, `*|UNSUB|*`, `*|IF:...|*…*|END:IF|*`) — string substitution syntax inside the HTML body and subject. Evaluated at **send time**, per recipient.

A template can use either, both, or neither. Custom-coded templates almost always use both.

## When to use this skill

Trigger this skill when:

- The user is writing or editing HTML destined for Mailchimp's "Code your own → Paste in code" or "Import zip" flow.
- The user mentions `mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, or merge tags.
- The user wants to add editable regions, repeatable cards, block design variants, or conditional content to an existing HTML email.
- The user asks to convert a static HTML email into a Mailchimp-editable template.
- The user wants a responsive email skeleton for Mailchimp.

Do **not** use this skill for:

- Mandrill / Mailchimp Transactional (uses Handlebars by default, not MCTL).
- Generic HTML email for non-Mailchimp ESPs (no merge tags, no `mc:` attributes).
- Mailchimp campaign/audience management — that's an MCP server job (`damientilman/mailchimp-mcp-server`), not a template skill.

## Workflow

When asked to build or modify a Mailchimp template, work through these phases. Each phase points to the reference file that owns its concern — load only what's relevant to the current request.

### Phase 1 — Identify the work

What is being requested? A brand-new template, edits to an existing one, conversion of static HTML to MCTL, or refactor of an existing Mailchimp template? Confirm with the user before assuming.

### Phase 2 — Pick the archetype (new templates)

For new templates, **load `references/blueprints.md`** and pick the archetype that matches the campaign type (newsletter, promotional, transactional, announcement, re-engagement). The blueprint defines section order, the `mc:edit` taxonomy, and which blocks should be repeatable or hideable.

### Phase 3 — Establish the scaffold

**Load `references/structure.md`** before generating any HTML. It contains the doctype, the head block, the Outlook MSO conditionals, and the three-table body nest. Do not improvise — email HTML is unforgiving and the head block has client-specific requirements you can't infer.

Then **start from `assets/skeleton.html`** as the structural baseline. Copy it, don't recreate it.

### Phase 4 — Define the visual layer (per project)

**Load `references/typography.md`** to set up the token slots (colors, fonts, type scale, line-height ratios). Fill in the brand's actual values — the skill does not impose a default palette or font.

### Phase 5 — Compose content blocks

**Load `references/patterns.md`** when assembling sections: the eyebrow→headline→subhead rhythm, repeatable card grids with hideable filler, multi-column footer, contact blocks, pull quotes, stat rows, dividers, button variants, feature lists.

**Load `references/mc-attributes.md`** alongside, to confirm placement rules for `mc:edit` (containers like `<td>`/`<div>` plus the documented inline exception for `<img>`), `mc:repeatable` (block-level elements like `<tr>`/`<table>`/`<div>`/`<p>` or inline elements like `<img>`/`<a>`/`<span>` per the docs), `mc:variant`, and `mc:hideable`. Naming conventions matter for Switch-Template compatibility.

### Phase 6 — Personalization and dynamic content

**Load `references/merge-tags.md`** when the user mentions personalization, conditional sections, dynamic content, or required compliance tags (`*|UNSUB|*`, `*|LIST:ADDRESS|*`). Includes operator support, IFNOT, conditional nesting, and the escape syntax for displaying literal merge tags.

### Phase 7 — Mobile, dark mode, Outlook hardening

**Load `references/responsive.md`** when the template needs to render across viewports: fluid hybrid pattern, media-query mobile rules, dark mode (Apple Mail + Outlook.com auto-inversion mitigation), bulletproof buttons, retina images, web font loading.

### Phase 8 — Accessibility pass

**Load `references/accessibility.md`** for any template that will ship to a real audience. Covers WCAG 2.2 AA targets (contrast, target size minimum), alt text patterns (decorative vs informative), `lang` attribute, semantic heading order, `role="presentation"` on layout tables, link text, and email-specific patterns (preview text, view-in-browser, plain-text alternative). Not optional for professional output.

### Phase 9 — Inline and validate

**Load `references/inliner.md`** if the template uses complex selectors or will be sent through multiple ESPs. Mailchimp's built-in inliner is sufficient for most cases; pre-inline with Juice or Premailer when you need a deterministic artifact.

**Run `scripts/validate.py`** before declaring the template ready. It catches the structural mistakes that silently break Mailchimp imports — `mc:edit` on text-level inline elements (with `<img>` correctly excluded per Mailchimp's documented exception), `mc:edit` on `<table>`, nested `mc:edit`, duplicate names, missing compliance tags, oversized HTML.

### Phase 10 — Report

After generating, briefly summarize the editable regions, repeatable blocks, hideable sections, and merge tags used. The user needs to know what the Mailchimp editor will expose before they hand the template to a non-technical editor.

## Hard rules

Things that will silently break a template if violated. Memorize these:

- **`mc:edit` goes on a container (`<td>`, `<div>`, `<th>`) or on an `<img>`.** Per Mailchimp's docs: *"mc:edit should be used on a div, table cell, or any other element that can be considered a 'container'"* plus the documented inline exception *"mc:edit can be placed on an `<img>` element."* Never on `<span>`, `<a>`, `<strong>`, or other text-level inline elements. Never on `<table>` itself — use the containing `<td>`.
- **`mc:edit` names must be unique within a template** AND should be **consistent across templates** if the user might switch templates on an existing campaign. `header`, `header_image`, `body`, `sidebar`, `footer` are the names Mailchimp's docs show in examples — use these where applicable so Switch Template works.
- **Never nest `mc:edit` regions.** Mailchimp's docs: *"You shouldn't nest editable elements within other editable elements."*
- **`mc:repeatable` blocks require a unique `mc:repeatable` value** (the "block type" name) and every editable region inside them needs an `mc:edit` name. Mailchimp scopes the editable names per instance automatically. Per the docs, `mc:repeatable` goes on block-level elements like `<div>` and `<p>` (and `<tr>`/`<table>` for table-based layouts), or on inline elements like `<img>`, `<a>`, `<span>`. Avoid list elements (`<ul>`, `<ol>`, `<li>`).
- **The required footer merge tags are non-negotiable**: an unsubscribe link wrapping `*|UNSUB|*` plus the audience address via either `*|LIST:ADDRESS|*` (plain text) or `*|HTML:LIST_ADDRESS_HTML|*` (HTML version — note the underscore, not colon, between `LIST` and `ADDRESS`). Omit them and Mailchimp will inject its own footer, which clients hate.
- **Use `*|MC_PREVIEW_TEXT|*` in the body**, not just rely on hidden preheader text. Mailchimp pulls preview text from this tag for the inbox preview.
- **Image dimensions are mandatory.** Every `<img>` needs `width`, `height`, and `style="display:block"`. Outlook will mis-size images sent without explicit attribute dimensions.
- **Critical CSS must survive as inline `style=""` attributes on the element.** Mailchimp's CSS Inliner is **opt-in**, not automatic — see `references/inliner.md` for when to pre-inline with Juice or Premailer rather than rely on the toggle. The reason it matters: Gmail web has size limits and sanitization on `<style>` blocks and the Gmail mobile apps remap class names internally, so any visual rule that has to render reliably in Gmail must already be inlined.

## Output expectations

When generating a template:

- Output a single HTML file. No external CSS, no external JS (it won't run anyway).
- All images use absolute URLs (no relative paths — emails leave your domain).
- Include the required footer block with `*|LIST:ADDRESS|*` and `*|UNSUB|*`.
- Include `*|MC_PREVIEW_TEXT|*` as the first child of `<body>`, hidden via styling.
- Set `mc:edit` regions on conventional names (`header`, `body`, `footer`, etc.) so the template survives a "Switch template" operation.
- Wrap Outlook-specific fallbacks in `<!--[if mso]>...<![endif]-->` conditionals where needed for VML buttons, MSO line-height fixes, or font fallbacks.
- After generating, briefly summarize the editable regions and any merge tags used, so the user knows what the Mailchimp editor will expose.

## Composability

This skill is the authoring half. Pair it with:

- **`damientilman/mailchimp-mcp-server`** (MCP) — to upload the resulting HTML to Mailchimp via `/3.0/templates`, list existing templates, or create a campaign from the template. Don't reinvent the upload flow.
- **Litmus / Email on Acid / Mailchimp's own Inbox Preview** — for cross-client rendering tests. This skill cannot test rendering itself.
