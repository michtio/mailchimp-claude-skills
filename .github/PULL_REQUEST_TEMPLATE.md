## Summary

Brief description of what this PR changes and why.

## Type

- [ ] New skill
- [ ] New reference file (added to existing skill)
- [ ] New pattern / blueprint / token slot
- [ ] Skill/reference content fix (factual correction, doc accuracy)
- [ ] Validator improvement (new check, fewer false positives)
- [ ] Documentation / README
- [ ] CI / repo maintenance

## Files changed

<!--
  Common patterns — delete the sections that don't apply:
-->

**Skills (SKILL.md)**
- `{skill-name}/SKILL.md` —

**Reference files**
- `{skill-name}/references/{file}.md` —

**Skeleton / assets**
- `{skill-name}/assets/...` —

**Validator**
- `{skill-name}/scripts/validate.py` —

**Other**
-

## Quality checklist

### Content accuracy
- [ ] Factual claims about Mailchimp behavior verified against Mailchimp's live docs or production-tested
- [ ] Code examples produce valid HTML that the validator accepts (strict mode)
- [ ] MCTL syntax matches Mailchimp's current spec (operators, conditionals, escape patterns)
- [ ] No deprecated patterns or removed features documented as current

### Skill structure
- [ ] Brand-neutral — no specific palette, font, or visual direction baked in
- [ ] Patterns reference `{{ token-name }}` placeholders, not concrete brand values
- [ ] Cross-references between reference files resolve to real files / anchors
- [ ] TOC entries match actual heading slugs (relevant for files over ~300 lines)

### Validator
- [ ] If adding a new check: includes a positive and negative test case
- [ ] Strict mode still passes on `mailchimp-template-language/assets/skeleton.html`

### Testing
- [ ] Tested with Claude Code on a representative prompt
- [ ] Generated template uploads cleanly via Mailchimp's "Code your own → Paste in code"

## Notes

Any additional context for reviewers — links to Mailchimp docs that informed the change, screenshots of editor / inbox preview, etc.
