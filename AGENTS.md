# AGENTS.md — MonMS Site Library orchestrator

You are an autonomous agent working in **monms-sites** — the public template library for MonMS. You shape **site templates** (L2 structure), not the MonMS Go engine.

MonMS lives in a sibling repository (`../MonMS/` on a typical dev machine). Load engine skills from there when editing template internals.

## Cold start

Read in order:

1. [README.md](README.md) — purpose and gallery status
2. [RULES.md](RULES.md) — non-negotiable library contract
3. [CONTRIBUTING.md](CONTRIBUTING.md) — PR workflow and checklist

Then load MonMS skills from the engine repo as needed (see Skill routing below).

## Your role

| You do | You do not |
|--------|------------|
| Add or edit templates under `sites/<category>/<slug>/` | Edit `../MonMS/internal/*` or engine CLI |
| Write `site.yaml` manifests | Commit `.pb_data/`, secrets, or binaries |
| Run `monms validate` against template paths | Push editorial copy as if it were structure |
| Follow text-only and remote-media rules | Invent repo layouts outside `sites/` |

Templates are **L2 structure** in MonMS terminology: `templates/`, `schema/`, text `assets/`, optional `documents/` and `doctrees/`. Content records live in `.pb_data/` on operator instances — never in this repo.

## Repo map

```
monms-sites/
├── AGENTS.md              ← you are here (canonical agent entry)
├── CLAUDE.md              ← thin pointer for Anthropic tooling
├── RULES.md               ← hard library rules
├── CONTRIBUTING.md        ← human + agent PR workflow
├── README.md
└── sites/
    ├── _base/
    │   └── _default/      ← canonical default (monms init baseline)
    └── <category>/
        └── <slug>/        ← one MonMS site template + site.yaml
```

Every template requires `site.yaml`. See [RULES.md](RULES.md) R4 for the schema.

**Default template:** `sites/_base/_default/` is the single source of truth for bare `monms init` scaffolding. When the engine embed changes (`../MonMS/internal/scaffold/embed/`), update `_default` here in the same PR cycle. Only `_default` may set `default: true` in `site.yaml`.

## Hard boundaries

These apply on every task. Details and rationale are in [RULES.md](RULES.md).

1. **No binaries** — text files only across the entire template tree (R2).
2. **Remote media** — all imagery via HTTPS URLs; no committed images or fonts (R3).
3. **No runtime artifacts** — never commit `.pb_data/`, `.monms/config.json`, `.monms/publish-state.json`, `content/`, logs, or secrets (R6).
4. **Validate before PR** — `monms validate -s sites/<category>/<slug>` must pass.
5. **One template focus** — prefer one `sites/<category>/<slug>/` per PR; no drive-by refactors across categories.

### MonMS binary for validation

```bash
# Typical local layout (sibling repos)
export MONMS_BIN=../MonMS/monms
monms validate -s sites/<category>/<slug>
```

Build the engine first if needed: `cd ../MonMS && go build -o monms .`

## Gallery and migration context (future)

The MonMS dashboard **site library / gallery** is not built yet. Do not invent incompatible install paths or manifest formats — follow this repo's layout so the gallery can consume it later.

### Expected operator flows

| Scenario | Expected approach |
|----------|-------------------|
| **New site from template** | `monms init --from-gallery <category>/<slug>` (engine TBD) or copy/sparse-checkout from `sites/<category>/<slug>/` into operator site Git repo |
| **Switch template** | Sparse-checkout a different `sites/<category>/<slug>/` into a sibling folder; re-point `monms serve -s <new-path>`; agent migrates schema/template deltas |
| **Deploy shape** | Operator tags their site Git repo; `monms site sync --ref TAG` on staging/production (MonMS operator rail) |

Breaking changes to templates are allowed while MonMS is pre-RC. Bump `site.yaml` `version` and document migration notes in PRs.

This library repo is **not** the operator's site Git checkout. Templates are copied or checked out **into** a separate repo that MonMS serves.

## Skill routing

Skills for MonMS engine and site shaping live in the **MonMS** repo, not here. Read skill frontmatter first; load full files only when relevant.

| Task | Load from `../MonMS/.cursor/skills/` |
|------|--------------------------------------|
| Any MonMS terminology or layers | `monms-architecture/SKILL.md` |
| Templates, schema, HTMX, validate | `monms-site-shaping/SKILL.md` |
| Markdown / doctrees | `monms-doctree/SKILL.md` |
| Docker, site sync, config.json | `monms-operators-deploy/SKILL.md` |

Stay in this repo's docs (`RULES.md`, `CONTRIBUTING.md`) for library-specific rules. Do not duplicate engine architecture in template PRs.

This repo has no `.cursor/skills/` yet. Add monms-sites-specific skills here only when recurring patterns justify them.

## Schema and template work

When mutating template internals, follow MonMS site-shaping conventions:

- **Schema dual-write:** PocketBase API + `schema/{name}.json` in the template (when a running server is available for API steps).
- **Page templates:** `{{define "body"}}…{{end}}` only — shell in `templates/layouts/base.gohtml`.
- **HTMX inline edit:** gate on `{{if .IsLoggedIn}}`; use `hx-swap="none"` and `hx-ext="json-enc"`.
- **Editorial flag:** `"editorial": true` on collections clients publish.

Full checklists: `../MonMS/.cursor/skills/monms-site-shaping/SKILL.md` and `../MonMS/docs/operators/shaping-and-agents.md`.

## PR hygiene

- Match path `sites/<category>/<slug>/` per [RULES.md](RULES.md) R1.
- Include or update `site.yaml`; bump `version` on meaningful changes.
- Confirm no binary files before opening PR.
- Run `monms validate` and report result in PR description.
- Propose new categories with rationale (R8).

## Universal boundaries (MonMS-aligned)

- Self-hosted, sovereign infrastructure over managed cloud defaults.
- Never hardcode secrets.
- Use `vi` for terminal file edits — not `nano`.

## Related MonMS docs

| Topic | Location |
|-------|----------|
| Cold start / commands | `../MonMS/PROJECT.md` |
| Four layers & promotion rails | `../MonMS/.cursor/skills/monms-architecture/SKILL.md` |
| Template routing & validation | `../MonMS/docs/operators/shaping-and-agents.md` |
| Media URLs at runtime | `../MonMS/docs/user-guide/media-urls.md` |
| `monms site sync` | `../MonMS/docs/reference/cli.md` |
