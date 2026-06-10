# monms-sites

The official **MonMS Site Library** — a public catalog of website templates for [MonMS](https://github.com/ndx-video/monms), an agent-malleable monolithic CMS.

Templates in this repo are **L2 structure** only: Go HTML templates, PocketBase schema JSON, and text-only assets. Gallery thumbnails and screenshots are **remote HTTPS URLs** in `site.yaml` (published to Backblaze B2). Editorial content (`.pb_data/` records) never lives here.

> **Status:** The dashboard **site library / gallery** and `monms init --from-gallery` are **not implemented** in MonMS yet. See [../MonMS/specs/site-library.md](../MonMS/specs/site-library.md) for the engine integration spec.

## Official specification

**[RULES.md](RULES.md)** is the source of truth. YAML frontmatter encodes machine-readable rules for a future MonMS site-library validator.

## What is in this repo?

Each entry is a complete MonMS site directory:

```
sites/<category>/<slug>/
├── site.yaml              # manifest — preview.thumbUrl, preview.screens
├── DESIGN.md              # optional design contract (recommended in this repo)
├── thumb.*                # local dev only (gitignored) — publish to B2
├── screen01.*             # optional screenshots (gitignored)
├── templates/
├── schema/
├── assets/                # text-only — see RULES.md
└── .monms/config.example.json
```

### Gallery publish workflow

1. Place `thumb.png` (640×360) at the site template root — gitignored.
2. Optionally add `screen01.png`, `screen02.png`, … at the same level.
3. Copy [.env.example](.env.example) to `.env` and fill B2 credentials.
4. Run `python scripts/publish_gallery_assets.py --site sites/<category>/<slug>`
5. Commit updated `site.yaml` with remote URLs — never commit the image files.

### Default template

When MonMS initializes a site without a gallery choice, the shape comes from `sites/_base/_default/`. See [RULES.md](RULES.md) R1 and R8.

### Operator overlay

The [`.overlay/`](.overlay/) directory holds agent skills and cold-start docs copied into **operator site repos** when MonMS installs a template from the library. Overlay files are not part of gallery templates under `sites/`. See [RULES.md](RULES.md) R12.

Installed operator sites receive:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Canonical agent entry (all platforms) |
| `CLAUDE.md` | Anthropic pointer to AGENTS.md |
| `.github/copilot-instructions.md` | Copilot pointer to AGENTS.md |
| `.cursor/skills/` | Five site skills: operator, shaping, design, content, instance-trajectory |

`monms-site-shaping` lives only in `.overlay/` — the MonMS engine repo does not duplicate it.

## Relationship to MonMS

| Repo | Role |
|------|------|
| **monms-sites** (this repo) | Curated template library — structure + `site.yaml` gallery URLs |
| **MonMS** (engine) | Go binary + operator dashboard |

Engine: [https://github.com/ndx-video/monms](https://github.com/ndx-video/monms)

## Media policy

| Kind | In Git | Rule |
|------|--------|------|
| Gallery thumbnail | No — URL in `site.yaml` | Local `thumb.*` → B2 via publish script |
| Gallery screenshots | No — URLs in `site.yaml` | Local `screenNN.*` → B2 |
| CSS | Yes (`assets/`) | Text only |
| Editorial imagery | URLs in templates/schema | Remote HTTPS (MonMS content rail) |

## Contributing

| Doc | Audience |
|-----|----------|
| [RULES.md](RULES.md) | Official site specification |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Fork, PR workflow, publish script |
| [AGENTS.md](AGENTS.md) | AI agent directives (Cursor) |
| [CLAUDE.md](CLAUDE.md) | Pointer to AGENTS.md (Anthropic) |

## License

[MIT](LICENSE). Per-template license in `site.yaml` when it differs.
