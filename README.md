# monms-sites

The official **MonMS Site Library** — a public catalog of website templates for [MonMS](https://github.com/ndx-video/MonMS), an agent-malleable monolithic CMS.

Templates in this repo are **L2 structure** only: Go HTML templates, PocketBase schema JSON, and text-only assets. Editorial content (`.pb_data/` records) never lives here; clients publish that through their own MonMS instances.

> **Status:** The dashboard **site library / gallery** and `monms init --from-gallery` are **not implemented** in MonMS yet. This repo is being populated with example templates and contribution rules first.

## What is in this repo?

Each entry is a complete MonMS site directory:

```
sites/<category>/<slug>/
├── site.yaml              # gallery manifest (required)
├── templates/
├── schema/
├── assets/                # text-only — see RULES.md
└── .monms/config.example.json
```

Browse templates here for reference, or install one into your **operator site Git checkout** (a separate repo from this library).

### Default template

When MonMS initializes a site without a gallery choice, the shape comes from:

```
sites/_base/_default/
```

Underscore-prefixed categories and slugs sort first and mark library defaults. See [RULES.md](RULES.md) R1 and R8. This template mirrors `monms init` output in the MonMS engine (`internal/scaffold/embed/`). Keep them in sync when the scaffold changes.

## Relationship to MonMS

| Repo | Role |
|------|------|
| **monms-sites** (this repo) | Curated template library — structure shapes only |
| **MonMS** (engine) | Go binary + operator dashboard; runs against a configured site directory |

MonMS resolves one site directory per process (`-s` / `--site` / `MONMS_SITE`). That directory is often its own Git repo on the operator's machine. This library repo is **not** that checkout — it is the source catalog the gallery will draw from.

For engine architecture, four-layer model, and validation tooling, see the MonMS repository (`PROJECT.md`, `docs/`).

## Using a template

**Today (manual):**

1. Clone or sparse-checkout `sites/<category>/<slug>/` from this repo.
2. Copy or merge into your operator's site Git repository.
3. Build MonMS and run `monms validate -s <path>` then `monms serve -s <path>`.

**Planned (MonMS dashboard gallery):**

- Browse templates in `/_monms/` site library (name TBD).
- **New site:** `monms init` (default → `_base/_default`) or `monms init --from-gallery <category>/<slug>` (engine TBD).
- **Switch template:** sparse-checkout a different template into a sibling folder, re-point `monms serve -s`, and use an agent to migrate schema/template deltas as needed.

Breaking changes to templates are expected while MonMS is pre-release candidate.

## Media policy

This library is stricter than a typical MonMS site checkout:

- **No binary files** anywhere in a template (no images, fonts, PDFs, archives).
- All imagery — preview thumbnails, hero photos, logos — must use **remote HTTPS URLs** (CDN). CDN infrastructure for library assets is managed separately from this repo.

Text CSS in `assets/` deploys with the structure rail (Git tag). Raster and vector imagery does not belong in `assets/` here. For how MonMS handles media URLs in editorial content, see MonMS `docs/user-guide/media-urls.md`.

## Contributing

We welcome templates that follow the library contract.

| Doc | Audience |
|-----|----------|
| [RULES.md](RULES.md) | Non-negotiable layout, manifest, and file-type rules |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Fork, PR workflow, validation checklist |
| [AGENTS.md](AGENTS.md) | AI agent operating directives (canonical for Cursor) |
| [CLAUDE.md](CLAUDE.md) | Pointer to AGENTS.md for Anthropic tooling |

## License

This repository is [MIT](LICENSE). Individual templates may declare a different SPDX license in `site.yaml`; when omitted, MIT applies.
