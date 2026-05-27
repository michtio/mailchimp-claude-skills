# mailchimp-claude-skills

Anthropic Agent Skills for working with Mailchimp from Claude (Claude Code, Claude.ai, API).

## Skills

| Skill | What it does |
|---|---|
| [`mailchimp-template-language`](./mailchimp-template-language/) | Author and edit custom-coded responsive Mailchimp templates with full MCTL support (`mc:edit`, `mc:repeatable`, `mc:variant`, `mc:hideable`, merge tags, conditionals). Includes Outlook-hardened skeleton and pre-upload validator. |

## Why this repo exists

Across the public Anthropic Skills ecosystem (anthropics/skills, obra/superpowers, wshobson/agents, ComposioHQ/awesome-claude-skills, and several smaller catalogs), as of mid-2026 there is no skill that targets Mailchimp's template language directly. Skills named "Mailchimp" are uniformly API/MCP wrappers that operate on existing templates — none of them help Claude *author* a custom-coded MCTL template. MJML, the popular abstraction for responsive email, can't fill the gap either because its parser strips `mc:*` attributes during compilation.

This repo fills that gap with hand-authored MCTL skills tuned to Mailchimp's quirks.

## Install (per-skill)

Each skill folder is a self-contained Agent Skill following the [SKILL.md spec](https://github.com/anthropics/skills). To install one in Claude Code:

```bash
# personal scope (all your projects)
cp -r mailchimp-template-language ~/.claude/skills/

# or project scope (committed with the client repo)
mkdir -p .claude/skills
cp -r mailchimp-template-language .claude/skills/
```

For Claude.ai, zip the skill folder and upload via Settings → Capabilities → Skills.

For the Anthropic API, see [Anthropic's skill docs](https://docs.claude.com/en/docs/agents/skills).

## Composition

These skills are the **authoring** layer. Pair with an MCP server for **deployment**:

- [`damientilman/mailchimp-mcp-server`](https://github.com/damientilman/mailchimp-mcp-server) — 53 tools across the Marketing API (templates, campaigns, audiences). `uvx mailchimp-mcp-server`.
- [Composio's hosted Mailchimp MCP](https://mcp.composio.dev/mailchimp) — OAuth-flow alternative if you don't want to manage API keys directly.

End-to-end flow: skill writes the HTML → validator confirms it's clean → MCP uploads it to Mailchimp via `POST /3.0/templates` → user runs Inbox Preview in Mailchimp's UI.

## Roadmap

Possible future skills (build when there's a real client need driving them):

- `mailchimp-nieuwsbrief` — Belgian-bilingual newsletter patterns using `*|TRANSLATE|*` and audience groups for NL/FR/EN.
- `mailchimp-rss-driven` — Templates wired for Mailchimp's RSS-to-email automations, with `*|RSSITEM|*` patterns.
- `mailchimp-product-feed` — E-commerce templates with product-grid merge tags for Shopify/WooCommerce integrations.
- `mailchimp-transactional-handlebars` — Separate skill for Mandrill/Transactional (different syntax: Handlebars, not MCTL).

## License

MIT — see [LICENSE](./LICENSE).

## Author

Built by [michtio](https://github.com/michtio) at [Bleu Chaud](https://bleuchaud.com).
