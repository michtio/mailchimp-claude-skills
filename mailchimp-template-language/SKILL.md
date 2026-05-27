---
name: mailchimp-template-language
description: Author and edit custom-coded Mailchimp email templates using Mailchimp Template Language (MCTL). Use this skill when the user mentions Mailchimp templates, mc:edit, mc:repeatable, mc:variant, mc:hideable, merge tags like *|FNAME|* or *|UNSUB|*, conditional blocks like *|IF:...|*, importing custom HTML into Mailchimp, MCTL, or building responsive email templates for Mailchimp campaigns. Also use when the user wants to add editable regions, repeatable blocks, or A/B variants to an HTML email destined for Mailchimp. Do NOT use for MJML (MJML strips mc:* attributes during compilation), generic transactional email, Mandrill/Handlebars templates, or non-Mailchimp ESPs.
license: MIT
---

# Mailchimp Template Language (MCTL)

## What this skill covers

Authoring **custom-coded HTML email templates** for Mailchimp's classic email builder: the template language that turns a flat HTML file into a Mailchimp-editable template with drag-and-drop regions, repeatable blocks, A/B variants, and conditional content.

Two distinct concerns are merged in MCTL and you must keep them separate:

1. **Template attributes** (`mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, `mc:allowdesignmodule`) — XML-ish attributes added to HTML tags. They control what the Mailchimp **editor** can do with a template. They are evaluated once, at template import time.
2. **Merge tags** (`*|FNAME|*`, `*|UNSUB|*`, `*|IF:...|*…*|END:IF|*`) — string substitution syntax inside the HTML body and subject. Evaluated at **send time**, per recipient.

A template can use either, both, or neither. Custom-coded templates almost always use both.

## When to use this skill

Trigger this skill when:

- The user is writing or editing HTML destined for Mailchimp's "Code your own → Paste in code" or "Import zip" flow.
- The user mentions `mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, or merge tags.
- The user wants to add editable regions, repeatable cards, A/B variants, or conditional content to an existing HTML email.
- The user asks to convert a static HTML email into a Mailchimp-editable template.
- The user wants a responsive email skeleton for Mailchimp.

Do **not** use this skill for:

- MJML authoring (MJML strips `mc:*` attributes during compile; use `framix-team/skill-email-html-mjml` if MJML is what they want).
- Mandrill / Mailchimp Transactional (uses Handlebars by default, not MCTL).
- Generic HTML email for non-Mailchimp ESPs (no merge tags, no `mc:` attributes).
- Mailchimp campaign/audience management — that's an MCP server job (`damientilman/mailchimp-mcp-server`), not a template skill.

## Workflow

When asked to build or modify a Mailchimp template:

1. **Identify what's being requested**: a brand-new template, edits to an existing one, or conversion of static HTML to MCTL.
2. **Load `references/structure.md`** before generating any HTML. It contains the responsive table skeleton, the doctype, the head, and the Outlook conditionals. Do not improvise this — email HTML is unforgiving.
3. **Load `references/mc-attributes.md`** when the user wants editable regions, repeatable blocks, variants, or hideable content. Critical: placement rules for `mc:edit` (only on containing elements, never on inline elements, naming conventions for template-switching).
4. **Load `references/merge-tags.md`** when the user mentions personalization, dynamic content, conditional sections, or required footer/unsubscribe links.
5. **Load `references/responsive.md`** when the user asks about mobile rendering, fluid layouts, Outlook fallbacks, or dark mode.
6. **Use `assets/skeleton.html`** as the starting point for any new template. Copy it, then customize. Do not write a Mailchimp template from a blank file.
7. **Validate with `scripts/validate.py`** before declaring the template ready. It catches the four most common Mailchimp import failures.

## Hard rules

Things that will silently break a template if violated. Memorize these:

- **`mc:edit` on a `<td>` or `<div>` only.** Never on `<span>`, `<a>`, `<strong>`, or any inline element. Never on `<table>` itself — use the containing `<td>`.
- **`mc:edit` names must be unique within a template** AND should be **consistent across templates** if the user might switch templates on an existing campaign. `header`, `body`, `sidecolumn`, `footer`, `header_image` are the conventional names — use these.
- **Never nest `mc:edit` regions.** A `mc:edit` inside another `mc:edit` will not import.
- **`mc:repeatable` blocks require a unique `mc:repeatable` value** (the "block type" name) and every editable region inside them needs an `mc:edit` name. Mailchimp prefixes the editable names per instance automatically.
- **The required footer merge tags are non-negotiable**: `*|LIST:ADDRESS|*` and an unsubscribe link wrapping `*|UNSUB|*` (or `*|HTML:LIST:ADDRESS_HTML|*` + unsub). Omit them and Mailchimp will inject its own footer, which clients hate.
- **Use `*|MC_PREVIEW_TEXT|*` in the body**, not just rely on hidden preheader text. Mailchimp pulls preview text from this tag for the inbox preview.
- **Image dimensions are mandatory.** Every `<img>` needs `width`, `height`, and `style="display:block"`. Outlook will explode otherwise.
- **Inline all CSS that matters.** Mailchimp's CSS inliner is good but not perfect; assume Gmail's `<style>` stripping is the worst case and inline anything critical.

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
