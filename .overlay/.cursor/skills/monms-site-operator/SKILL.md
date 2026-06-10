---
name: monms-site-operator
description: >-
  Operator-site identity and guardrails for MonMS L2 repos. Use at session
  start or when unsure which directory, rails, or commit rules apply.
---

# MonMS Site Operator

You are shaping a **deployed MonMS site** — not the engine repo, not the monms-sites library.

## Role

| Rail | What goes here | How it ships |
|------|----------------|--------------|
| **Structure (L2)** | Templates, schema JSON, CSS/assets | Git commits (`agent:` prefix) |
| **Editorial** | Page copy, blog posts, media records | Client `/_monms/publish` — not agent Git pushes |

## Site path

Confirm the active site directory before editing:

```bash
# Resolved by -s / --site, then MONMS_SITE, then ./site
monms validate -s .
```

Do not assume the folder is named `site`. Staging and production often use different paths.

## Never commit

| Path | Reason |
|------|--------|
| `.pb_data/` | PocketBase SQLite runtime |
| `.monms/config.json` | Instance URLs, publisher emails |
| `.monms/publish-state.json` | Publish checksum state |
| `.monms/logs/` | Runtime logs |
| `content/` | Ephemeral editorial exports |
| `.env`, tokens, API keys | Credentials |

Commit `.monms/config.example.json`, `.monms/trajectory.json` (or `trajectory.example.json` until customized), and `DEPLOY.md` when present.

## Commits

- Prefix: `agent:` (D-45)
- Run `monms validate` before template commits
- Never use `git commit --no-verify` routinely

## When to load other skills

| Task | Skill |
|------|-------|
| New collection, template, HTMX pattern | `monms-site-shaping` |
| CSS, layout, visual tokens | `monms-site-design` |
| What clients publish vs what agents shape | `monms-site-content` |
| Trajectory, tags, instance deploy | `monms-instance-trajectory` |

## Related docs

- [Shaping and agents](https://github.com/ndx-video/monms/blob/main/docs/operators/shaping-and-agents.md)
- [Security](https://github.com/ndx-video/monms/blob/main/docs/operators/security.md)
