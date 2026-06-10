# GitHub Actions — site repo

## Shape deploy

Workflow: [shape-deploy.yml](workflows/shape-deploy.yml)

Triggers on tag push (`v*`). Reads [`.monms/trajectory.json`](../.monms/trajectory.example.json) and POSTs to each host at the tag **frontier** segment.

### One-time setup

1. Copy `.monms/trajectory.example.json` → `.monms/trajectory.json` and customize stages/hosts.
2. Generate `MONMS_DEPLOY_TOKEN` (32+ random bytes) per host or one shared token.
3. Add repository secret **`MONMS_DEPLOY_TOKEN`** (or per-host `MONMS_DEPLOY_TOKEN_<HOST_ID>` where `HOST_ID` is uppercased with hyphens → underscores).
4. On each host: copy `config.example.json` → `config.json`, set `instance` block to match trajectory host id, set `MONMS_DEPLOY_TOKEN` in environment.

### Promote (shape rail)

Use dotted integer tags per trajectory segment count. Example for 3 segments (`development` → `staging` → `production`):

```bash
git tag v0.1.0   # deploy staging (segment 1)
git push origin v0.1.0

git tag v0.1.1   # deploy production (segment 2)
git push origin v0.1.1
```

After deploy, update `shapeSync.ref` on each host to the new tag (crash-recovery pin).

See MonMS skill `monms-instance-trajectory` for tag increment rules.
