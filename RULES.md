# RULES.md — MonMS Site Library contract

These rules keep the template library small, reviewable, and safe to scale. They apply to **every** path under `sites/<category>/<slug>/`. Violations block merge.

For contributor workflow, see [CONTRIBUTING.md](CONTRIBUTING.md). For agent behavior, see [AGENTS.md](AGENTS.md).

---

## R1 — Directory placement

Every template lives at:

```
sites/<category>/<slug>/
```

| Segment | Rule |
|---------|------|
| `category` | Lowercase kebab-case (e.g. `marketing`, `portfolio`) |
| `slug` | Lowercase kebab-case; **globally unique** across the entire repo |

Do not place templates at the repo root or outside `sites/`.

### Underscore prefix (defaults)

Categories and slugs may use a leading `_` to mark **library defaults**. Underscore names sort first in file browsers and signal canonical baselines to agents.

| Path | Role |
|------|------|
| `sites/_base/_default/` | **Canonical default** — matches `monms init` when no gallery template is chosen |

Only one template may set `default: true` in `site.yaml` (see R4). Today that is `_base/_default`.

---

## R2 — Text-only artifacts

Templates must not contain binary files anywhere — not only under `assets/`.

### Allowed (text)

| Extensions | Notes |
|------------|-------|
| `.gohtml` | MonMS templates |
| `.json` | Schema, seed data, config examples |
| `.yaml`, `.yml` | Manifest (`site.yaml`) |
| `.md` | Markdown documents / doctrees |
| `.css`, `.scss` | Stylesheets |
| `.svg` | Plain-text SVG only (not base64-heavy exports) |

### Forbidden (binary)

Images (`png`, `jpg`, `jpeg`, `webp`, `gif`, `ico`, `avif`), fonts (`woff`, `woff2`, `ttf`, `otf`, `eot`), archives (`zip`, `tar`, `gz`), PDFs, and any other non-text blob.

Reviewers should treat unexpected file types as rejections. CI may add automated binary scanning later.

---

## R3 — Remote media only

All visual assets referenced by a template must be remote URLs:

- Preview thumbnails in `site.yaml` → `preview.imageUrl`
- Hero images, logos, backgrounds in templates or seed data → `https://` CDN URLs in text/HTML fields
- Optional live demo → `preview.siteUrl`

| Allowed | Forbidden |
|---------|-----------|
| `https://cdn.example.com/...` | Local image paths committed to the repo |
| Documented CDN bases | Large `data:` URIs embedded in HTML or JSON |
| Same URL on staging and production (MonMS content rail pattern) | PocketBase `file` fields for cross-environment publishable media |

See MonMS `docs/user-guide/media-urls.md` for how editorial media works at runtime. This repo adds the stronger rule: **no binary media files in Git**.

---

## R4 — `site.yaml` manifest (required)

Each template **must** include `site.yaml` at its root (`sites/<category>/<slug>/site.yaml`).

### Schema

```yaml
# sites/<category>/<slug>/site.yaml
slug: minimal-landing          # must match the <slug> directory name
category: marketing            # must match the <category> directory name
name: Minimal Landing          # human title for the gallery
description: >-
  Single-page hero site with inline HTMX editing.
version: "0.1.0"               # template semver (library item, not MonMS engine)
monms:
  minVersion: null             # optional; omit or null while MonMS is pre-RC
preview:
  imageUrl: https://cdn.example.com/monms-sites/marketing/minimal-landing.png
  siteUrl: null                # optional HTTPS demo URL
tags:
  - landing
  - minimal
author: NDX                    # person or org
license: MIT                   # SPDX identifier; defaults to repo MIT if omitted
```

### Field rules

| Field | Required | Notes |
|-------|----------|-------|
| `slug` | Yes | Matches directory name |
| `category` | Yes | Matches parent directory name |
| `name` | Yes | Short gallery title |
| `description` | Yes | One or two sentences |
| `version` | Yes | Bump on every meaningful template change |
| `monms.minVersion` | No | Engine semver when MonMS reaches RC |
| `preview.imageUrl` | Yes | Remote HTTPS only (R3) |
| `preview.siteUrl` | No | Optional hosted demo |
| `tags` | Yes | Lowercase kebab-case strings |
| `author` | Yes | |
| `license` | No | SPDX; omit for MIT |
| `default` | No | `true` only on the single canonical default template (`_base/_default`) |

---

## R5 — MonMS site shape

A template must be a valid MonMS L2 site directory.

### Minimum required paths

```
templates/layouts/base.gohtml
templates/index.gohtml
schema/
.monms/config.example.json
site.yaml
```

### Recommended (when used by the template)

```
templates/fragments/
templates/errors/
assets/                    # text-only per R2
documents/                 # markdown content rail
doctrees/
Dockerfile.example
docker-compose.example.yml
```

### Validation

Must pass against a current MonMS build:

```bash
monms validate -s sites/<category>/<slug>
```

Resolution order for the `monms` binary: `MONMS_BIN` → `$PATH` → `../../monms` relative to the site directory. When developing locally with MonMS as a sibling checkout, set `MONMS_BIN=../MonMS/monms`.

---

## R6 — No runtime or secrets

Never commit paths that belong to a running instance:

| Path (under template root) | Reason |
|----------------------------|--------|
| `.pb_data/` | PocketBase SQLite runtime |
| `.monms/config.json` | Instance URLs, publisher emails |
| `.monms/publish-state.json` | Publish checksum state |
| `.monms/logs/` | Runtime logs |
| `content/` | Ephemeral editorial exports |
| `.env`, tokens, API keys | Credentials |

Commit `.monms/config.example.json` only.

---

## R7 — Editorial seed data

Optional seed JSON in `schema/` or documented seed records is allowed.

- Use generic, licensable placeholder copy.
- Reference images via text URL fields, not PocketBase file uploads.
- Mark collections `"editorial": true` when clients should publish them (MonMS schema convention).

---

## R8 — Categories

Initial allowlist:

| Category | Intended use |
|----------|----------------|
| `_base` | Library defaults (underscore prefix); contains `_default` scaffold |
| `marketing` | Landing pages, campaigns, lead capture |
| `portfolio` | Showcases, case studies, personal sites |
| `documentation` | Docs hubs, knowledge bases, doctree-heavy sites |
| `minimal` | Bare scaffolds and starter shapes |

To add a category, open an issue or include rationale in your PR. Avoid one-off or overly narrow category names.

---

## R9 — Breaking changes

MonMS has no release candidate yet. Templates may change drastically between versions.

- Bump `site.yaml` `version` on every merge that alters templates, schema, or assets.
- Describe breaking changes in the PR body (removed collections, renamed slugs, layout overhauls).
- The gallery must not assume stable template APIs until MonMS RC.

Semantic versioning for templates: increment **major** for breaking schema/routing changes, **minor** for additive features, **patch** for fixes and copy-only seed updates.

---

## Quick reference

```
sites/<category>/<slug>/     ← only valid template location
site.yaml                    ← required manifest
text files only              ← no binaries anywhere
remote HTTPS for all imagery ← previews and content URLs
monms validate               ← must pass before merge
```
