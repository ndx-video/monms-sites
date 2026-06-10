# AGENTS.md — MonMS Site Library orchestrator

You are an autonomous agent working in **monms-sites** — the public template library for MonMS. You shape **site templates** (L2 structure), not the MonMS Go engine.

MonMS lives in a sibling repository (`../MonMS/`). Engine integration spec: `../MonMS/specs/site-library.md`.

## Cold start

Read in order:

1. [README.md](README.md) — purpose and gallery status
2. [RULES.md](RULES.md) — official spec (frontmatter + body)
3. [CONTRIBUTING.md](CONTRIBUTING.md) — PR workflow and publish script
4. `sites/<category>/<slug>/DESIGN.md` — when shaping or editing a specific template's UI (R11)

## Your role

| You do | You do not |
|--------|------------|
| Add or edit templates under `sites/<category>/<slug>/` | Edit `../MonMS/internal/*` unless implementing site-library spec |
| Write `site.yaml` with `preview.thumbUrl` / `preview.screens` | Commit binaries or gallery image files |
| Read and maintain `DESIGN.md` when shaping UI; keep CSS aligned with tokens | Require `DESIGN.md` for external validation (optional per R11) |
| Run `scripts/publish_gallery_assets.py` before PRs with gallery changes | Commit `.pb_data/`, secrets, or local `thumb.*` / `screenNN.*` |
| Run `monms validate` against template paths | Invent repo layouts outside `sites/` |

## Repo map

```
monms-sites/
├── RULES.md               ← official spec (YAML frontmatter + rules)
├── .overlay/              ← operator-site files (copied at install — R12)
├── scripts/publish_gallery_assets.py
├── .env.example           ← B2 credentials template (.env gitignored)
└── sites/
    ├── _base/_default/    ← canonical default
    └── <category>/<slug>/ ← template + site.yaml + DESIGN.md
```

**Operator overlay (R12):** `.overlay/` contains agent skills and `AGENTS.md` for deployed site repos. MonMS copies these on template install — they are not part of gallery templates and are not validated with `monms validate`.

Every gallery-ready template requires `preview.thumbUrl` in `site.yaml`. See [RULES.md](RULES.md) R4 and R10.

Every template in this repo should include `DESIGN.md` (R11) — read it before editing CSS or layout.

**Default template:** `sites/_base/_default/` mirrors `monms init` (`../MonMS/internal/scaffold/embed/`). Only `_default` may set `default: true`.

## Hard boundaries

1. **Text-only in Git** — no committed binaries (R2).
2. **Gallery via B2** — local `thumb.*` / `screenNN.*` at site root are gitignored; publish script uploads and patches yaml (R10).
3. **Editorial media** — remote HTTPS in templates/schema (R3b).
4. **No runtime artifacts** — never commit `.pb_data/`, `.monms/config.json`, `content/`, secrets (R6).
5. **Validate before PR** — `monms validate -s sites/<category>/<slug>`.

```bash
export MONMS_BIN=../MonMS/monms
monms validate -s sites/<category>/<slug>
```

## Gallery publish (contributors)

```bash
cp .env.example .env   # fill once
pip install -r scripts/requirements.txt
python scripts/publish_gallery_assets.py --site sites/<category>/<slug>
```

Use `--dry-run` to preview without uploading or writing yaml.

## Skill routing

Load `.overlay/.cursor/skills/monms-site-shaping` when editing template internals. Load `../MonMS/.cursor/skills/monms-architecture` for engine terminology. Library rules stay in this repo's `RULES.md`.

## PR hygiene

- Match `sites/<category>/<slug>/`
- `preview.thumbUrl` set; no `preview.imageUrl`
- `DESIGN.md` present and aligned with `assets/main.css`
- No committed image files
- Run publish script when gallery assets change
- Bump `site.yaml` `version` on meaningful changes

## Related

| Topic | Location |
|-------|----------|
| Engine site-library spec | `../MonMS/specs/site-library.md` |
| Template shaping | `.overlay/.cursor/skills/monms-site-shaping/SKILL.md` |
| Media URLs at runtime | `../MonMS/docs/user-guide/media-urls.md` |
