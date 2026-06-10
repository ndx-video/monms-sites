---
name: monms-site-content
description: >-
  Separates MonMS structure rail (Git) from editorial rail (client publish).
  Use when deciding what agents commit vs what clients publish to production.
---

# MonMS Site Content

MonMS has two content rails. Agents work on **structure**; clients work on **editorial**.

## Structure rail (agents)

Committed to Git via `agent:` prefixed commits:

| Artifact | Examples |
|----------|----------|
| Templates | `templates/**/*.gohtml` |
| Schema | `schema/*.json` — collection shapes, field types |
| Assets | `assets/main.css` — text-only stylesheets |
| Seed data | Generic placeholder records in `schema/seed/` |

Agents define **what can be published** — collection names, field shapes, template bindings.

## Editorial rail (clients)

Shipped to production via `/_monms/publish` — **not** routine agent Git commits:

| Content | Examples |
|---------|----------|
| Page copy | Headlines, body text, CTAs |
| Blog posts | Press releases, news items |
| Media URLs | Hero images, logos (HTTPS text fields) |

Do not push production editorial copy through agent commits unless the operator explicitly requests a one-off seed or migration.

## Editorial collections

Mark client-publishable collections in schema JSON:

```json
{
  "name": "press_releases",
  "editorial": true,
  ...
}
```

`"editorial": true` is a MonMS-only key — PocketBase strips it on import. Without it, the collection is excluded from the publish rail.

## Credentials

| Use case | Credential |
|----------|------------|
| Collection management (dual-write) | `POCKETBASE_ADMIN_TOKEN` — short-lived JWT |
| MCP shaping helpers | MonMS API key (`monms_…`) from `/_monms/api-keys` |
| Production import (consultant setup) | `MONMS_PUBLISH_TOKEN` |

Never commit tokens. See [Security](https://github.com/ndx-video/monms/blob/main/docs/operators/security.md).

## Related docs

- [Shaping and agents](https://github.com/ndx-video/monms/blob/main/docs/operators/shaping-and-agents.md)
- [MCP and API keys](https://github.com/ndx-video/monms/blob/main/docs/operators/mcp-and-api-keys.md)
- [Media URLs](https://github.com/ndx-video/monms/blob/main/docs/user-guide/media-urls.md)
