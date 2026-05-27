# MCTL Attributes

The `mc:*` attribute family turns plain HTML into Mailchimp-editable templates. These are parsed by Mailchimp at template import time and converted into editor regions, repeatable blocks, and variants.

## `mc:edit` — editable region

The fundamental attribute. Marks a container as user-editable in the Mailchimp campaign editor.

```html
<td mc:edit="header_image" align="center" style="padding:24px;">
  <a href="*|ARCHIVE|*"><img src="https://cdn.example.com/logo.png" width="180" height="40" alt="Brand" style="display:block;"></a>
</td>
```

### Placement rules

Mailchimp's official template-language doc states: *"mc:edit should be used on a div, table cell, or any other element that can be considered a 'container.'"* Plus a documented exception: *"mc:edit can be placed on an `<img>` element. This will allow the image to be replaced, resized, and edited using the Mailchimp campaign editor."*

What that means in practice:

- **Container elements** are the primary target — typically `<td>` or `<div>`. `<th>` is a table cell and works the same way, though it's not named in Mailchimp's examples.
- **`<img>` is the one documented exception** — `mc:edit` on `<img>` lets the editor replace, resize, and edit the image directly.
- **Never on `<span>`, `<a>`, `<strong>`, or other text-level inline elements.** These aren't containers and Mailchimp's editor won't surface them.
- **Never on `<table>` itself** — use the containing `<td>`. Mailchimp's docs caution against this; the editor can't reliably wrap a whole table as editable content.
- Apply to a **single element wrapping the editable content**, not multiple sibling elements. The entire contents of the marked element become editable. The element itself stays put (it's the container, not the content).

### Naming rules

Names must be:

- **Unique within a template.** Two `mc:edit="body"` in the same template will silently break.
- **Consistent across templates the user might switch between.** If a campaign switches from Template A to Template B, only regions with matching `mc:edit` names will retain content. Conventional names below.

### Conventional names

Mailchimp's docs show these names in examples for Switch-Template compatibility (*"If the user switches templates after writing content, they could lose their copy if the editable space names aren't consistent"*):

| Name | Source | Purpose |
|---|---|---|
| `header` | Docs | Top section, often the logo |
| `header_image` | Docs | Hero image specifically |
| `body` | Docs | Main content area |
| `sidebar` | Docs | Right or left sidebar in multi-column layouts |
| `footer` | Docs | Bottom section, before compliance |
| `preheader` | Convention | Preview text region (if exposed in editor) |
| `footer_address` | Convention | Required physical address (if separated from main footer) |

The "Source" column distinguishes names that appear in Mailchimp's official template-language documentation from names that are community convention but stable in production. Custom names are fine for one-off templates. For agency-style template families (where the user maintains many similar templates), normalize on the documented names so Switch Templates works.

### What's NOT allowed

```html
<!-- WRONG: text-level inline element -->
<span mc:edit="cta">Click here</span>

<!-- WRONG: on the table itself -->
<table mc:edit="body" ...>...</table>

<!-- WRONG: nested (Mailchimp's docs: "You shouldn't nest editable elements within other editable elements.") -->
<td mc:edit="body">
  <p>Welcome <span mc:edit="name">Friend</span>!</p>
</td>

<!-- WRONG: duplicate names -->
<td mc:edit="content">First</td>
<td mc:edit="content">Second</td>
```

### What IS allowed

```html
<!-- Right: on a containing td -->
<td mc:edit="cta_button" align="center" style="padding:24px;">
  <a href="https://example.com" style="background:#2563eb; color:#fff; padding:12px 24px; text-decoration:none; display:inline-block;">Click here</a>
</td>

<!-- Right: on a div inside a td (also fine) -->
<td style="padding:24px;">
  <div mc:edit="cta_button">
    <a href="..." style="...">Click here</a>
  </div>
</td>

<!-- Right: directly on <img> — Mailchimp's documented inline exception -->
<img mc:edit="hero_image" src="https://cdn.example.com/hero.jpg" width="600" height="300" alt="" style="display:block;">
```

## `mc:repeatable` — repeatable block

Marks a block that the user can duplicate in the editor. Use for product cards, article previews, list items.

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr mc:repeatable="product">
    <td style="padding:16px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="180" valign="top" mc:edit="product_image">
            <img src="https://cdn.example.com/placeholder.png" width="180" height="180" alt="" style="display:block;">
          </td>
          <td valign="top" style="padding-left:16px;" mc:edit="product_details">
            <h3 style="margin:0 0 8px 0; font-size:18px;">Product name</h3>
            <p style="margin:0; font-size:14px; color:#666;">Description goes here</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

### Rules

- `mc:repeatable="<block_type>"` — the value is the **block type name**, not the instance identifier. Multiple blocks of the same type share the value (`mc:repeatable="product"` on three different `<tr>` elements means the user can add more "product" blocks).
- Mailchimp's docs: *"Use mc:repeatable on block-level elements (like `<div>` and `<p>`) with the exception of lists, or inline elements (like `<img>`, `<a>`, and `<span>`)."* In practice, table-based email templates use `<tr>` or `<table>` because that's the layout primitive; `<div>` and `<p>` work for non-table layouts. Avoid `<ul>`, `<ol>`, `<li>`.
- Mailchimp duplicates the entire marked element when the user clicks "Add block."
- Editable regions inside a repeatable get scoped per-instance by Mailchimp — you define each `mc:edit` once with its base name and Mailchimp tracks instances separately in the editor. (The exact internal naming scheme — e.g. `product_image_1`, `product_image_2` — isn't formally documented; what matters is that each repeated instance gets its own editable state.)
- **Nested repeatables are allowed.** Mailchimp's docs: *"mc:repeatable elements can be nested within each other, but use care."* Useful for sections-containing-cards patterns, but the editor UI gets denser fast.
- Different repeatable block types in the same template need different `mc:repeatable` values.

### Optional: control over what can be added

```html
<tr mc:repeatable="product" mc:variant="standard">...</tr>
<tr mc:repeatable="product" mc:variant="featured">...</tr>
```

This gives the user a dropdown of variants when adding a new block of type `product`.

## `mc:variant` — alternative block design

Pairs with `mc:repeatable` to offer multiple designs of the same block type. The user picks the variant when adding the block.

```html
<!-- Default product card -->
<tr mc:repeatable="product" mc:variant="image_left">
  <td>...</td>
</tr>

<!-- Alternative: image on right -->
<tr mc:repeatable="product" mc:variant="image_right">
  <td>...</td>
</tr>

<!-- Alternative: full-width image on top -->
<tr mc:repeatable="product" mc:variant="image_top">
  <td>...</td>
</tr>
```

In the editor, the user sees a single "Product" block in the Add Block menu, with a sub-selector for image_left / image_right / image_top.

## `mc:hideable` — user-toggleable visibility

Lets the user hide an entire block from the editor without deleting it.

```html
<tr mc:hideable>
  <td mc:edit="promo_section" style="padding:24px; background:#fff8e1;">
    <p>Special offer this month!</p>
  </td>
</tr>
```

### Documented form: valueless

Mailchimp's official template-language docs specify `mc:hideable` as a **valueless attribute**. The bare form (no `="..."`) is the spec. The empty form `mc:hideable=""` is equivalent and acceptable HTML.

### Named form: community convention

A widespread pattern in production templates labels each hideable block with a name:

```html
<tr mc:hideable="filler">
<tr mc:hideable="sustainability">
<tr mc:hideable="social_proof">
```

The named form works reliably (the editor accepts it; tested in production) and gives editors a recognizable label per block when toggling visibility. It is **not in Mailchimp's official documentation** — it's community convention, but a stable one. Use it when you have multiple hideable blocks in a template and want them distinguishable in the editor UI.

### What `mc:hideable` does NOT do

There is no documented way to default a block to hidden via the template attribute. Initial visibility (on/off per campaign) is controlled by the editor, not the template. Older community guides occasionally claim `mc:hideable="hide"` defaults hidden — this is not supported by Mailchimp's docs and should not be relied on.

## `mc:allowdesignmodule` — drag-and-drop drop zones (unverified)

Some Mailchimp documentation and community guides reference an attribute for accepting Mailchimp's built-in content blocks (image, text, divider, button, etc.) inside a custom-coded region. The exact attribute name and value syntax are **not present** on the current `templates.mailchimp.com/getting-started/template-language/` page — Mailchimp's classic versus new builder split has changed which drag-and-drop blocks are exposed and how.

If you need a template that mixes hand-coded regions with drag-and-drop authoring:

1. Don't take this section as authoritative — test against your target Mailchimp account before relying on it.
2. The pure custom-coded path with `mc:edit` regions and `mc:repeatable` blocks is fully documented and doesn't require any drag-and-drop attribute.

For most templates, skip this entirely.

## Quick reference table

| Attribute | Placement | Value | Effect |
|---|---|---|---|
| `mc:edit="name"` | `<td>`, `<div>`, `<th>`, or `<img>` (docs name `<img>` explicitly) | unique region name | Marks element as user-editable |
| `mc:repeatable="type"` | block element (`<tr>`, `<table>`, `<div>`, `<p>`) or inline (`<img>`, `<a>`, `<span>`); **not** list elements | block type name | User can duplicate this block |
| `mc:variant="name"` | same element as `mc:repeatable` | variant name | Alternative design for the block type |
| `mc:hideable` | single element | valueless (spec) or `="label"` (convention) | User can toggle block visibility |

## Order of attributes on a single element

When multiple `mc:*` attributes appear on the same element, XML attribute order is irrelevant in any spec-compliant parser. For readability, use:

```html
<tr mc:repeatable="product" mc:variant="featured" mc:hideable>
```

## Common import failures and what causes them

1. **"Editable section names must be unique"** — duplicate `mc:edit` values. Search the file for the value, deduplicate.
2. **Region present in HTML but not editable in Mailchimp** — `mc:edit` is on a text-level inline element (e.g. `<span>`, `<a>`, `<strong>`) or nested inside another `mc:edit`. Move it to the containing block element. (Note: `<img>` is an explicit exception — Mailchimp's docs permit `mc:edit` on `<img>`.)
3. **Repeatable shows up but can't be duplicated** — `mc:repeatable` is on a `<td>` rather than `<tr>` or a `<table>` (in table-based layouts), or on a list element (`<ul>`/`<ol>`/`<li>`). The repeatable target must be a complete sub-tree.
4. **Editor shows the region but content vanishes on save** — almost always a malformed HTML structure (unclosed tag, mismatched `<td>`/`<tr>`). Run the HTML through a validator.
