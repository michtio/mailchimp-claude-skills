# Template Blueprints

Five structural archetypes for the most common Mailchimp campaign types. Each blueprint specifies the **section order**, **required `mc:edit` regions**, **recommended `mc:repeatable` / `mc:hideable` placement**, and **archetype-specific pitfalls**. No styling — pair with `patterns.md` and `typography.md` to fill in the visual layer.

## Choosing a blueprint

| User says... | Use blueprint |
|---|---|
| "monthly newsletter", "digest", "roundup", "issue" | **Newsletter** |
| "promo", "sale", "campaign", "product launch", "limited time" | **Promotional** |
| "order confirmation", "receipt", "invoice", "booking confirmation" | **Transactional** (note: usually goes via Mandrill, not regular Mailchimp campaigns) |
| "we're launching", "announcement", "important update", "we shipped" | **Announcement** |
| "winback", "we miss you", "haven't seen you", "re-engage" | **Re-engagement** |

If the brief mixes archetypes (e.g. "newsletter with a featured product"), pick the dominant archetype and compose patterns from `patterns.md` for the secondary content.

---

## 1. Newsletter

A periodic digest with multiple sections, often per-topic or per-category. Editor needs to add/remove sections each issue.

### Section order

1. **Preheader** — hidden inbox-preview text (`*|MC_PREVIEW_TEXT|*` + padding)
2. **Top nav** — logo, optional language switcher or archive link
3. **Hero** — issue eyebrow ("May 2026 · Issue 27"), headline, subhead, optional CTA, optional hero media
4. **Index / map** *(optional)* — visual overview of what's inside
5. **Repeatable section blocks** — one per topic/category, each containing its own header + content
6. **Featured / sponsored** *(optional, hideable)* — promoted item
7. **Contact / signature block** — newsletter editor or contact person
8. **Footer** — links, social row, compliance

### `mc:edit` taxonomy

```
preheader
nav_logo, nav_lang
hero_eyebrow, hero_headline, hero_subhead, hero_cta, hero_media
index_eyebrow, index_image                                 (optional)

[ within tr mc:repeatable="section" ]
  section_label, section_unit_count, section_meta
  card_1_image, card_1_eyebrow, card_1_title, card_1_meta, card_1_cta
  card_2_*, card_3_*  (repeat structure)
  filler_title, filler_description, filler_cta             (mc:hideable="filler")
  section_contact_blurb

[ within tr mc:repeatable="contact" ]
  contact_label, contact_name, contact_meta, contact_avatar

footer_logo, footer_tagline, footer_col_1, footer_col_2, footer_compliance
```

### Repeatable / hideable map

| Block | Attribute | Why |
|---|---|---|
| Each section | `mc:repeatable="section"` | Editor adds/removes/reorders sections per issue |
| Contact block | `mc:repeatable="contact"` | Multiple contacts (per region, per role) |
| Filler card slot | `mc:hideable="filler"` | Hidden when the section is fully populated |
| Featured / sponsored section | `mc:hideable="featured"` | Toggle off when no featured content |

### Key merge tags

- `*|MC:DATE:F Y|*` — "May 2026" in the hero eyebrow if you don't hand-edit the date.
- `*|ARCHIVE|*` — "View in browser" link for clipped Gmail recipients.
- `*|MC_PREVIEW_TEXT|*` — preheader.

### Pitfalls

- Long newsletters approach Gmail's 102 KB clipping limit fast. Host all images externally, no inline base64.
- `mc:edit` inside repeatable sections auto-scopes per-instance — don't reuse the same name across non-repeatable sections expecting separate editors.
- Multi-language newsletters: pick one language per send, OR use audience groups + conditional merge tags. Don't try to render all languages in one template body.

---

## 2. Promotional

A focused sales push — single hero offer, supporting product grid, single primary CTA repeated near the bottom.

### Section order

1. **Preheader**
2. **Top nav** — logo only (don't dilute the CTA with link clutter)
3. **Hero** — image-led, large headline, subhead, prominent CTA, optional countdown / urgency phrase
4. **Offer details** — what's included, terms, deadlines
5. **Product grid** *(if applicable)* — repeatable products with price + CTA
6. **Social proof** *(optional, hideable)* — testimonial, stat row, or review snippets
7. **Secondary CTA** — same target as the hero CTA, reinforced near the bottom for scanners
8. **Footer** — compliance only; keep visual emphasis on the offer above

### `mc:edit` taxonomy

```
preheader
nav_logo
hero_image, hero_eyebrow (e.g. "LIMITED TIME"), hero_headline, hero_subhead, hero_cta
offer_intro, offer_terms, offer_deadline

[ within tr mc:repeatable="product" ]
  product_image, product_name, product_price, product_meta, product_cta

[ mc:hideable="social_proof" ]
  proof_quote, proof_attribution
  OR
  stat_1_value, stat_1_label, stat_2_*, stat_3_*

secondary_cta_headline, secondary_cta

footer_compliance
```

### Repeatable / hideable map

| Block | Attribute | Why |
|---|---|---|
| Each product | `mc:repeatable="product"` | Variable lineup per campaign |
| Social proof section | `mc:hideable="social_proof"` | Often omitted if no relevant proof |

### Key merge tags

- `*|IF:DISCOUNT_CODE|*Use code *|DISCOUNT_CODE|* at checkout*|END:IF|*` — personalized code if available.
- `*|FNAME|fallback:|*` — personalized greeting, but watch for awkward fallback ("Hi ,").

### Pitfalls

- One primary CTA. Multiple CTAs with different targets dilute conversion. Use the secondary-CTA slot to *reinforce* the primary, not introduce a competing action.
- Hero image: don't bury the offer in the image alone. The same message must read as text for image-off recipients (and screen readers).
- Urgency phrases ("Today only", "Ends Friday") date the email — useful for short campaigns, dangerous for archived sends. If the campaign repeats, parameterize the date with `*|DATE:|*` or a custom merge field.

---

## 3. Transactional

Order confirmation, booking confirmation, receipt, invoice. **Note**: high-volume transactional email usually goes through Mandrill (Mailchimp Transactional) with Handlebars, not MCTL — but small-volume transactional via Mailchimp campaigns happens, and the structure is the same.

### Section order

1. **Preheader** — order number or receipt summary
2. **Top header** — logo, document reference (order # / invoice #)
3. **Greeting block** — personalized salutation, short summary sentence
4. **Line-item table** — itemized list with quantity / description / total
5. **Totals block** — subtotal, tax/VAT, total
6. **Next steps** — shipping info, delivery dates, payment status, support contact
7. **Footer** — compliance, business registration details (KBO/BTW in BE, SIRET in FR, etc.)

### `mc:edit` taxonomy

```
preheader
header_logo, header_reference (e.g. "Order #1042")
greeting_salutation, greeting_summary

[ within tr mc:repeatable="line_item" ]
  item_name, item_description, item_quantity, item_total

totals_subtotal, totals_tax_label, totals_tax, totals_total
next_steps_heading, next_steps_body, next_steps_support

footer_compliance, footer_business_id
```

### Repeatable / hideable map

| Block | Attribute | Why |
|---|---|---|
| Each line item | `mc:repeatable="line_item"` | Variable per order |

### Key merge tags

- Most transactional data comes from merge fields populated via the API at send time: `*|ORDER_ID|*`, `*|ORDER_TOTAL|*`, etc.
- `*|CURRENT_YEAR|*` for the footer copyright.
- For real Mandrill/Transactional templates, Handlebars `{{order_total}}` replaces MCTL — same blueprint, different syntax.

### Pitfalls

- Receipts must look correct without web fonts (recipients save them, forward them, print them). Use system fonts or test the font-loaded version against the Outlook fallback rigorously.
- Don't include marketing CTAs ("Check out our new arrivals!") in receipts in jurisdictions with strict transactional/marketing separation (e.g. CAN-SPAM, RGPD for hybrid content).
- Business registration footer must include: legal name, address, BTW/VAT/KBO/SIRET number, in the format required by the jurisdiction.

---

## 4. Announcement

Single-focus message: a launch, a milestone, an important update, a leadership change. Minimal structure, high signal.

### Section order

1. **Preheader**
2. **Top nav** — logo only, optionally a small "Announcement" label
3. **Big statement** — headline-only block (no eyebrow, no subhead) for highest impact
4. **Body** — 2–4 short paragraphs of context
5. **Supporting media** *(optional)* — single image, video thumbnail, or quote
6. **CTA** — single action ("Read more", "Watch the announcement", "Join the launch event")
7. **Signature** — from a person (often a founder/leader), with name + role
8. **Footer** — compliance

### `mc:edit` taxonomy

```
preheader
nav_logo, nav_label (e.g. "Company news")
big_statement                                       (one large headline only)
body_1, body_2, body_3                              (separate mc:edit per paragraph
                                                     so the editor can split, reorder)
supporting_media                                    (optional)
cta_headline, cta                                   (cta_headline is optional context)
signature_name, signature_role, signature_avatar

footer_compliance
```

### Repeatable / hideable map

Minimal — announcements are intentionally short and focused. The only optional block is supporting media:

| Block | Attribute | Why |
|---|---|---|
| Supporting media | `mc:hideable="supporting_media"` | Not every announcement has an image |

### Key merge tags

- `*|FNAME|fallback:there|*` for the greeting in body_1 if you want personalization.
- `*|MC:DATE:F j, Y|*` — formal date format for "Today, May 27, 2026" openings.

### Pitfalls

- Resist adding sections. The discipline of a single-focus email is the point.
- The big-statement block should pass the "read it in 3 seconds" test. If it requires reading 30 words to understand the headline, it's too long.
- The signature should be a real person; "The Team at X" is weaker than a named individual with a role ("Jordan Lee, CEO").

---

## 5. Re-engagement

Sent to subscribers who haven't engaged in 60/90/180 days. Tone is gentle, retention-focused, and offers a clear exit (unsubscribe) so the audience self-cleans.

### Section order

1. **Preheader** — "We've missed you" or similar empathetic line
2. **Top nav** — logo
3. **Empathetic opener** — short, human, recognizes the absence without guilt
4. **What's new** *(brief)* — 2–3 highlights of what the subscriber missed, hideable
5. **Reactivation CTA** — primary action ("Confirm you still want to hear from us", "Update your preferences")
6. **Soft exit** — explicit unsubscribe link, framed positively ("Or, if our updates aren't useful anymore, unsubscribe with one click — no hard feelings")
7. **Footer** — compliance

### `mc:edit` taxonomy

```
preheader
nav_logo
opener_greeting, opener_body

[ mc:hideable="whats_new" ]
  whats_new_heading
  highlight_1_title, highlight_1_body
  highlight_2_title, highlight_2_body
  highlight_3_title, highlight_3_body

reactivation_headline, reactivation_subhead, reactivation_cta

soft_exit_headline, soft_exit_body                  (NB: still link *|UNSUB|* explicitly)

footer_compliance
```

### Repeatable / hideable map

| Block | Attribute | Why |
|---|---|---|
| "What's new" section | `mc:hideable="whats_new"` | Sometimes the message is just "are you still there?" without recapping |

### Key merge tags

- `*|FNAME|fallback:there|*` for the empathetic opener.
- `*|UNSUB|*` for both the soft-exit CTA and the compliance footer.
- `*|UPDATE_PROFILE|*` for the reactivation CTA if the goal is preference recapture rather than confirmation.

### Pitfalls

- Don't shame the recipient. Phrases like "It's been a while..." land; "You've been ignoring us!" doesn't.
- Make the unsubscribe action genuinely easy and prominent — the goal of a re-engagement send is *list health*, not just retention. A clear exit reduces spam complaints from disengaged subscribers.
- After the send, segment: those who clicked the reactivation CTA stay; those who didn't are candidates for sunset (auto-unsubscribe after N more days without engagement).
