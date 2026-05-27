#!/usr/bin/env python3
"""
Mailchimp template validator.

Catches common MCTL mistakes BEFORE you upload to Mailchimp.
Exits 0 if clean, 1 if errors found.

Usage:
    python validate.py path/to/template.html
    python validate.py path/to/template.html --strict   # warnings become errors
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


# Inline elements where mc:edit is invalid.
# NOTE: <img> is intentionally absent — Mailchimp's docs explicitly permit
# mc:edit on <img> ("This will allow the image to be replaced, resized, and
# edited..."), so we don't flag it here. See VALID_MC_EDIT_PARENTS.
INLINE_ELEMENTS = {
    "a", "span", "strong", "em", "b", "i", "u", "small", "sub", "sup",
    "code", "br", "label", "input", "button", "abbr", "cite", "q",
}

# Elements where mc:edit is valid.
# Mailchimp's docs say mc:edit goes on "a div, table cell, or any other
# element that can be considered a 'container'", plus explicitly on <img>.
VALID_MC_EDIT_PARENTS = {"td", "div", "th", "img"}

# Required merge tags for compliance
REQUIRED_TAGS = ["*|UNSUB|*", "*|LIST:ADDRESS|*"]
# Either *|LIST:ADDRESS|* or *|HTML:LIST_ADDRESS_HTML|* covers physical address.
# Note the underscore (not colon) between LIST and ADDRESS in the HTML variant —
# this is the form documented in Mailchimp's merge-tag cheat sheet.
ALT_ADDRESS_TAG = "*|HTML:LIST_ADDRESS_HTML|*"


def strip_inert_regions(html: str) -> str:
    """Replace content of <code>, <pre>, and HTML comments with spaces of equal length.
    Preserves line numbers and overall structure so error reporting stays accurate.
    mc:edit strings appearing as documentation inside these regions are not real attributes.
    """
    def blank_keep_newlines(match):
        return re.sub(r"[^\n]", " ", match.group(0))

    # Comments
    html = re.sub(r"<!--.*?-->", blank_keep_newlines, html, flags=re.DOTALL)
    # <code>...</code>
    html = re.sub(r"<code\b[^>]*>.*?</code>", blank_keep_newlines, html, flags=re.DOTALL | re.IGNORECASE)
    # <pre>...</pre>
    html = re.sub(r"<pre\b[^>]*>.*?</pre>", blank_keep_newlines, html, flags=re.DOTALL | re.IGNORECASE)
    return html


def find_mc_edits(html: str) -> list[tuple[str, str, int]]:
    """Return list of (element_name, edit_name, line_number)."""
    results = []
    pattern = re.compile(
        r"<\s*([a-zA-Z0-9]+)\b[^>]*?mc:edit\s*=\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(html):
        line = html[:match.start()].count("\n") + 1
        results.append((match.group(1).lower(), match.group(2), line))
    return results


def find_mc_repeatables(html: str) -> list[tuple[str, str, int]]:
    results = []
    pattern = re.compile(
        r"<\s*([a-zA-Z0-9]+)\b[^>]*?mc:repeatable\s*=\s*['\"]([^'\"]*)['\"]",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(html):
        line = html[:match.start()].count("\n") + 1
        results.append((match.group(1).lower(), match.group(2), line))
    return results


def check_nested_mc_edits(html: str) -> list[tuple[int, int]]:
    """Find mc:edit regions nested inside other mc:edit regions.
    Returns list of (outer_line, inner_line).
    Note: this is heuristic — regex can't perfectly parse HTML — but catches the obvious cases.
    """
    nested = []
    # Find every mc:edit position
    edits = list(re.finditer(r'mc:edit\s*=\s*[\'"]([^\'"]+)[\'"]', html, re.IGNORECASE))
    for i, outer in enumerate(edits):
        # Find the closing tag for whatever element this lives in
        # Walk forward from outer.end() looking for the next mc:edit before a balanced close
        outer_tag_match = re.search(
            r"<\s*([a-zA-Z0-9]+)[^>]*" + re.escape(outer.group(0)),
            html[:outer.end()],
            re.IGNORECASE,
        )
        if not outer_tag_match:
            continue
        tag = outer_tag_match.group(1).lower()
        # Walk forward, tracking depth of this same tag, until we close it
        depth = 1
        pos = outer.end()
        tag_open = re.compile(rf"<\s*{tag}\b", re.IGNORECASE)
        tag_close = re.compile(rf"<\s*/\s*{tag}\s*>", re.IGNORECASE)
        edit_re = re.compile(r'mc:edit\s*=\s*[\'"]([^\'"]+)[\'"]', re.IGNORECASE)

        while depth > 0 and pos < len(html):
            next_open = tag_open.search(html, pos)
            next_close = tag_close.search(html, pos)
            next_edit = edit_re.search(html, pos)

            # Pick earliest event
            candidates = [(m.start(), m, kind) for m, kind in
                          [(next_open, "open"), (next_close, "close"), (next_edit, "edit")] if m]
            if not candidates:
                break
            candidates.sort()
            start, m, kind = candidates[0]

            if kind == "edit" and depth >= 1 and m.start() != outer.start():
                # nested mc:edit found before our tag closed
                outer_line = html[:outer.start()].count("\n") + 1
                inner_line = html[:m.start()].count("\n") + 1
                nested.append((outer_line, inner_line))
                pos = m.end()
            elif kind == "open":
                depth += 1
                pos = m.end()
            elif kind == "close":
                depth -= 1
                pos = m.end()
            else:
                pos = m.end()

    return nested


def validate(html: str, strict: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # Strip code blocks and comments so documentation references to mc:edit don't trigger checks.
    # The required-tag and size checks below run against the ORIGINAL html, not this stripped version.
    scan_html = strip_inert_regions(html)

    # 1. mc:edit placement
    edits = find_mc_edits(scan_html)
    for element, name, line in edits:
        if element in INLINE_ELEMENTS:
            errors.append(
                f"line {line}: mc:edit='{name}' on inline element <{element}>. "
                f"Move it to the containing <td> or <div>."
            )
        elif element not in VALID_MC_EDIT_PARENTS and element != "table":
            warnings.append(
                f"line {line}: mc:edit='{name}' on <{element}> — unusual placement. "
                f"Convention: use <td> or <div>."
            )
        elif element == "table":
            errors.append(
                f"line {line}: mc:edit='{name}' on <table>. "
                f"Mailchimp expects mc:edit on the containing <td>, not <table> itself."
            )

    # 2. Duplicate mc:edit names
    edit_names = [name for _, name, _ in edits]
    duplicates = [name for name, count in Counter(edit_names).items() if count > 1]
    for dupe in duplicates:
        lines = [str(line) for _, name, line in edits if name == dupe]
        errors.append(
            f"duplicate mc:edit name '{dupe}' on lines {', '.join(lines)}. "
            f"Each editable region name must be unique within a template."
        )

    # 3. Nested mc:edit
    nested = check_nested_mc_edits(scan_html)
    for outer_line, inner_line in nested:
        errors.append(
            f"nested mc:edit detected: outer on line {outer_line}, inner on line {inner_line}. "
            f"Mailchimp will fail to import nested editable regions."
        )

    # 4. mc:repeatable placement
    # Mailchimp's docs name <div> and <p> as primary examples and also
    # permit inline elements like <img>, <a>, <span>; lists are the only
    # element family explicitly excluded. In table-based email layouts the
    # practical unit is <tr> or <table>, so we accept the union.
    repeatables = find_mc_repeatables(scan_html)
    for element, name, line in repeatables:
        if element in {"ul", "ol", "li"}:
            warnings.append(
                f"line {line}: mc:repeatable='{name}' on <{element}>. "
                f"Mailchimp's docs exclude list elements from mc:repeatable."
            )
        elif element not in {"tr", "table", "div", "p", "img", "a", "span"}:
            warnings.append(
                f"line {line}: mc:repeatable='{name}' on <{element}>. "
                f"Convention for table-based email: <tr> or a full <table>. "
                f"Mailchimp also accepts <div>, <p>, and certain inline elements."
            )

    # 5. Required merge tags
    if "*|UNSUB|*" not in html:
        errors.append("required tag *|UNSUB|* missing. Mailchimp will reject the campaign.")
    if "*|LIST:ADDRESS|*" not in html and ALT_ADDRESS_TAG not in html:
        errors.append(
            f"physical address required: include either *|LIST:ADDRESS|* or {ALT_ADDRESS_TAG}. "
            f"CAN-SPAM compliance — Mailchimp will inject its own footer if missing."
        )

    # 6. Preview text recommendation
    if "*|MC_PREVIEW_TEXT|*" not in html:
        warnings.append(
            "*|MC_PREVIEW_TEXT|* not found. Without it, inbox preview will scrape body content unpredictably."
        )

    # 7. Doctype check
    if not re.search(r"<!DOCTYPE\s+html", html, re.IGNORECASE):
        warnings.append(
            "no DOCTYPE declaration. Use XHTML 1.0 Transitional (matches the "
            "bundled skeleton) or HTML5. Without one, Outlook drops to quirks mode."
        )

    # 8. Images without dimensions
    img_tags = re.findall(r"<img\s+[^>]*>", html, re.IGNORECASE)
    for img in img_tags:
        has_width = bool(re.search(r"\bwidth\s*=", img, re.IGNORECASE))
        has_height = bool(re.search(r"\bheight\s*=", img, re.IGNORECASE))
        if not (has_width and has_height):
            line = html[:html.find(img)].count("\n") + 1
            warnings.append(
                f"line {line}: <img> missing width and/or height attribute. "
                f"Outlook ignores CSS dimensions — add HTML attributes."
            )

    # 9. Viewport meta
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.IGNORECASE):
        warnings.append("no viewport meta tag. Mobile rendering will be inconsistent.")

    # 10. Size check (Gmail clips at ~102KB)
    size_kb = len(html.encode("utf-8")) / 1024
    if size_kb > 102:
        errors.append(
            f"HTML size is {size_kb:.1f} KB. Gmail clips emails over 102 KB. "
            f"Trim content or move inline base64 to external URLs."
        )
    elif size_kb > 80:
        warnings.append(
            f"HTML size is {size_kb:.1f} KB. Approaching Gmail's 102 KB clipping threshold."
        )

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Mailchimp template HTML.")
    parser.add_argument("file", type=Path, help="Path to the HTML template")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    html = args.file.read_text(encoding="utf-8")
    errors, warnings = validate(html, strict=args.strict)

    if errors:
        print(f"\n{len(errors)} ERROR(S):", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
    if warnings:
        print(f"\n{len(warnings)} WARNING(S):", file=sys.stderr)
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)

    if errors or (args.strict and warnings):
        sys.exit(1)
    if not errors and not warnings:
        print("✓ Template looks good. No errors or warnings.")
    else:
        print(f"\n✓ {len(errors)} errors, {len(warnings)} warnings. Non-strict mode: passing.")
    sys.exit(0)


if __name__ == "__main__":
    main()
