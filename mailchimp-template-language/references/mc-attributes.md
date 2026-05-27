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

- Apply to **container elements only**: `<td>`, `<div>`. Never on `<table>`, `<tr>`, or any inline element.
- Apply to a **single element wrapping the editable content**, not multiple sibling elements.
- The entire contents of the marked element become editable. The element itself stays put (it's the container, not the content).

### Naming rules

Names must be:

- **Unique within a template.** Two `mc:edit="body"` in the same template will silently break.
- **Consistent across templates the user might switch between.** If a campaign switches from Template A to Template B, only regions with matching `mc:edit` names will retain content. Conventional names below.

### Conventional names

Use these wherever possible:

| Name | Purpose |
|---|---|
| `header` | Top section, often the logo |
| `header_image` | Hero image specifically |
| `preheader` | Preview text region (if exposed in editor) |
| `body` | Main content area |
| `sidecolumn` | Right or left sidebar in multi-column layouts |
| `footer` | Bottom section, before compliance |
| `footer_address` | Required physical address (if separated from main footer) |

Custom names are fine for one-off templates. For agency-style template families (where the user maintains many similar templates), normalize on these names so Switch Templates works.

### What's NOT allowed

```html
<!-- WRONG: inline element -->
<span mc:edit="cta">Click here</span>

<!-- WRONG: on the table itself -->
<table mc:edit="body" ...>...</table>

<!-- WRONG: nested -->
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
  <a href="*|MC:URL|*" style="background:#2E114B; color:#fff; padding:12px 24px; text-decoration:none; display:inline-block;">Click here</a>
</td>

<!-- Right: on a div inside a td (also fine) -->
<td style="padding:24px;">
  <div mc:edit="cta_button">
    <a href="..." style="...">Click here</a>
  </div>
</td>
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
- The repeatable element must be a single HTML element (typically `<tr>` or `<table>`). Mailchimp duplicates this entire element when the user clicks "Add block."
- Editable regions inside a repeatable get **auto-prefixed** by Mailchimp per instance. You define them once with their base name; Mailchimp generates `product_image_1`, `product_image_2`, etc. internally.
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
<tr mc:hideable="">
  <td mc:edit="promo_section" style="padding:24px; background:#fff8e1;">
    <p>Special offer this month!</p>
  </td>
</tr>
```

The empty value (`mc:hideable=""`) is correct. The user toggles visibility per-campaign in the editor.

For a section that defaults to hidden:

```html
<tr mc:hideable="hide">
  <td>...</td>
</tr>
```

## `mc:allowdesignmodule` — drag-and-drop drop zones

For templates that should accept Mailchimp's built-in content blocks (image, text, divider, button, etc.) at specific locations:

```html
<table role="presentation" width="100%">
  <tr>
    <td mc:allowdesignmodule="all">
      <!-- User can drag any content block type into this region -->
    </td>
  </tr>
</table>
```

Values: `all` (any block type), or a comma-separated list like `image,text,button`.

This is mostly relevant if you're building a template that mixes hand-coded regions with drag-and-drop authoring. For pure custom-coded templates with `mc:edit` regions, you don't need this.

## Quick reference table

| Attribute | Placement | Value | Effect |
|---|---|---|---|
| `mc:edit="name"` | `<td>` or `<div>` | unique region name | Marks contents as user-editable |
| `mc:repeatable="type"` | single element (often `<tr>`) | block type name | User can duplicate this block |
| `mc:variant="name"` | same element as `mc:repeatable` | variant name | Alternative design for the block type |
| `mc:hideable=""` | single element | empty or `"hide"` | User can toggle block visibility |
| `mc:allowdesignmodule="..."` | container | `all` or block list | Accepts drag-and-drop content blocks |

## Order of attributes on a single element

When multiple `mc:*` attributes appear on the same element, order doesn't matter to Mailchimp's parser. For readability, use:

```html
<tr mc:repeatable="product" mc:variant="featured" mc:hideable="">
```

## Common import failures and what causes them

1. **"Editable section names must be unique"** — duplicate `mc:edit` values. Search the file for the value, deduplicate.
2. **Region present in HTML but not editable in Mailchimp** — `mc:edit` is on an inline element or nested inside another `mc:edit`. Move it to the containing block element.
3. **Repeatable shows up but can't be duplicated** — `mc:repeatable` is on a `<td>` rather than `<tr>` or a `<table>`. The repeatable target must be a complete sub-tree.
4. **Editor shows the region but content vanishes on save** — almost always a malformed HTML structure (unclosed tag, mismatched `<td>`/`<tr>`). Run the HTML through a validator.
