# Deploy trajectory

MonMS sites promote on two independent rails:

| Rail | Artifact | Mechanism |
|------|----------|-----------|
| **Shape (L2)** | templates, schema, assets | Git tag → GitHub Actions → `POST /api/monms/shape/deploy` |
| **Content (L3)** | `.pb_data/` editorial records | `/_monms/publish` → production `POST /api/monms/content/import` |

## Trajectory map

Commit `.monms/trajectory.json` (copy from `trajectory.example.json`). The map is **identical on every host**. Each host’s gitignored `config.json` declares:

- `instance.id` — matches `trajectory.stages[n].hosts[].id`
- `instance.role` — `development`, `test`, `staging`, or `production`
- `instance.stageIndex` — position in the chain

Tag format: `{prefix}{int}.{int}...` with segment count = `trajectory.tag.segments`. Increment `stage.shape.tagSegment` for the stage you are promoting to (e.g. `v0.1.0` staging, `v0.1.1` production in a 3-segment map).

GitHub Actions: see [`.github/README.md`](.github/README.md).
