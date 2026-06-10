# AGENTS.md — MonMS operator site

You are an autonomous agent working in a **deployed MonMS site repository** — the operator's L2 checkout (templates, schema, assets). This is not the MonMS engine and not the monms-sites template library.

## Cold start

Read in order:

1. This file — role and boundaries
2. `DESIGN.md` at the site root — before any CSS or layout work
3. `.monms/trajectory.json` — when tagging, deploying, or editing instance config
4. Load skills from `.cursor/skills/` as needed (see routing below)

## Your role

| You do | You do not |
|--------|------------|
| Shape templates, schema, and text-only assets | Edit the MonMS Go engine |
| Dual-write schema (PocketBase API + `schema/*.json`) | Push routine editorial copy via Git |
| Run `monms validate` before commits | Commit runtime artifacts or secrets |
| Use `agent:` commit prefix (D-45) | Edit monms-sites gallery templates |

## Skill routing

| Task | Skill |
|------|-------|
| Repo identity, guardrails, site path | `monms-site-operator` |
| Templates, schema, HTMX, validation | `monms-site-shaping` |
| CSS, layout, design tokens | `monms-site-design` |
| Editorial vs structure boundary | `monms-site-content` |
| Trajectory, instance roles, shape tags, GH deploy | `monms-instance-trajectory` |

Skills live at `.cursor/skills/<name>/SKILL.md`. Customize them for this site after install.

## Cross-platform entry points

| File | Audience |
|------|----------|
| `AGENTS.md` | All agents (canonical) |
| `CLAUDE.md` | Anthropic — pointer to AGENTS.md |
| `.github/copilot-instructions.md` | GitHub Copilot — pointer to AGENTS.md |

## Validation

```bash
export MONMS_BIN=/path/to/monms   # optional; else PATH
monms validate -s .
```

Resolution order for the `monms` binary: `MONMS_BIN` → `$PATH` → `../../monms` relative to the site directory.

## Operator docs

- [Shaping and agents](https://github.com/ndx-video/monms/blob/main/docs/operators/shaping-and-agents.md)
- [Templates and routing](https://github.com/ndx-video/monms/blob/main/docs/operators/templates-and-routing.md)
- [Security](https://github.com/ndx-video/monms/blob/main/docs/operators/security.md)
- [MCP and API keys](https://github.com/ndx-video/monms/blob/main/docs/operators/mcp-and-api-keys.md)
- [GitHub App deploy](https://github.com/ndx-video/monms/blob/main/docs/operators/github-app-deploy.md)
