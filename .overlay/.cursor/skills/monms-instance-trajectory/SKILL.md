---
name: monms-instance-trajectory
description: >-
  Site instance roles, trajectory.json promotion map, dotted shape tags, and
  GitHub Actions shape deploy. Use when editing trajectory, tagging releases,
  configuring multi-instance deploy, or promoting shape/content between stages.
---

# MonMS instance trajectory

Load `monms-site-operator` first if site path or rails are unclear.

## Concepts

| Term | Location | Meaning |
|------|----------|---------|
| **Site** | `trajectory.site` | Human project identity (slug + displayName) |
| **Instance role** | `config.json` → `instance.role` | Fixed enum: `development`, `test`, `staging`, `production` |
| **Instance id** | `config.json` → `instance.id` | Host label matching `trajectory.stages[n].hosts[].id` |
| **Trajectory** | `.monms/trajectory.json` (committed) | Identical promotion map on every host |

`production` is reserved: terminal audience-facing role; shape deploy API allowed on `staging` and `production` only.

## Files in this repo

```
.monms/
├── trajectory.json          # committed (from trajectory.example.json)
├── trajectory.example.json  # template reference
├── config.example.json      # committed per-host template
└── config.json              # gitignored live host config
```

See also `DEPLOY.md` at the site root and `.github/README.md` for operator setup.

## Trajectory stages

Each `stages[]` entry:

| Field | Purpose |
|-------|---------|
| `index` | 0-based position in chain |
| `role` | Instance role literal at this stage |
| `shape.mode` | `none`, `sequential`, or `parallel` |
| `shape.tagSegment` | Which tag segment activates this stage |
| `content.publishesTo` | Downstream stage index for L3 publish |
| `hosts[]` | Deploy targets (`id`, `siteUrl`, `deploy.systemdUnit`) |

- **sequential** — tag frontier at this segment triggers deploy to this stage's hosts only.
- **parallel** — when frontier equals `tagSegment`, deploy **all** hosts in the stage.

## Shape tag format

`{prefix}{int}.{int}...` — segment count = `trajectory.tag.segments`. Integers only; no pre-release suffixes on the shape rail.

**Increment rule (agent checklist):**

1. Parse tag after prefix into `[s0, s1, …, sN-1]`.
2. To promote shape **to stage k**, increment `s(k)` where `k = stage.shape.tagSegment`.
3. Leave `s(i)` for `i < k` unchanged from the previous tag.
4. Set `s(i) = 0` for `i > k` unless re-deploying the same stage (increment `s(k)` only).

**3-stage example** (`tag.segments: 3`, staging=segment 1, production=segment 2):

| Tag | Action |
|-----|--------|
| `v0.1.0` | First staging shape deploy (increment segment 1) |
| `v0.1.1` | Promote to production (increment segment 2) |
| `v0.1.2` | Re-deploy production only (increment segment 2 again) |

**1-stage example** (production-only): `tag.segments: 1` → tags `v1`, `v2`, …

## Content rail

Upstream instance sets `productionUrl` to the production stage host `siteUrl`. Clients use `/_monms/publish`. Shape and content rails are independent.

## GitHub Actions

Workflow: `.github/workflows/shape-deploy.yml`

1. Tag push `v*` triggers workflow.
2. `.github/scripts/resolve-shape-deploy-hosts.sh` reads trajectory + tag frontier.
3. `POST {siteUrl}/api/monms/shape/deploy` with `MONMS_DEPLOY_TOKEN` repository secret.
4. Update `shapeSync.ref` on each host after successful deploy.

## Validation

```bash
monms validate -s .
```

Checks `config.json` instance vs `trajectory.json` when both exist on the host.

## Related docs

- [GitHub App deploy](https://github.com/ndx-video/monms/blob/main/docs/operators/github-app-deploy.md)
- [MonMS API — shape deploy](https://github.com/ndx-video/monms/blob/main/docs/reference/monms-api.md)
