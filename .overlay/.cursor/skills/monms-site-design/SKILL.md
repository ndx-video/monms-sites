---
name: monms-site-design
description: >-
  Honors DESIGN.md design contracts when editing CSS, layout, or visual tokens
  in a MonMS operator site. Use before any UI shaping work.
---

# MonMS Site Design

Read `DESIGN.md` at the **site root** before editing CSS, layout, or template styling.

## Workflow

1. **Read** `DESIGN.md` — YAML frontmatter (tokens) and markdown rationale
2. **Map** tokens to implementation in `assets/main.css` and template classes
3. **Validate** alignment — drift between DESIGN.md and CSS is a review concern
4. **Update** DESIGN.md frontmatter when making meaningful visual changes (same commit)

## DESIGN.md format

Uses the [design.md format](https://github.com/google-labs-code/design.md) (Apache-2.0). Two layers:

1. **YAML front matter** — `name`, `colors`, `typography`, `rounded`, `spacing`, optional `components`
2. **Markdown body** — Overview, Colors, Typography, Layout, and related sections

Optional advisory lint:

```bash
npx @google/design.md lint DESIGN.md
```

## Token → CSS alignment

| DESIGN.md | Implementation |
|-----------|----------------|
| `colors.primary` | CSS custom property or class in `assets/main.css` |
| `typography.h1` | Heading styles — font, size, weight, line-height |
| `spacing.md` | Padding/margin scale |
| `rounded.md` | Border-radius on cards, buttons |

Do not invent colors outside the contract unless the operator explicitly requests a redesign — then update DESIGN.md first.

## Template work

- Prefer semantic HTML and classes that map to DESIGN.md components
- Load `monms-site-shaping` for Go template structure and HTMX patterns
- Remote imagery: HTTPS URLs in schema/templates (not committed binaries)

## When DESIGN.md is missing

Some minimal templates ship without one. Infer from existing `assets/main.css` and document decisions in the PR/commit body. Consider adding a DESIGN.md when the visual identity stabilizes.

## Related

- [Media URLs](https://github.com/ndx-video/monms/blob/main/docs/user-guide/media-urls.md) — editorial imagery at runtime
