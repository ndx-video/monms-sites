---
spec: monms-site-library
specVersion: "1"
engine:
  repo: https://github.com/ndx-video/monms
layout:
  root: sites/{category}/{slug}
  categoryPattern: "^[a-z][a-z0-9-]*$"
  slugPattern: "^[a-z_][a-z0-9_-]*$"
  requiredPaths:
    - site.yaml
    - templates/layouts/base.gohtml
    - templates/index.gohtml
    - schema/
    - .monms/config.example.json
gallery:
  localDevBasenames:
    - thumb
    - "^screen\\d{2}$"
  localDevAtSiteRoot: true
  formats: [svg, png, jpg, jpeg]
  formatPreference: [svg, png, jpg, jpeg]
  thumbDimensions: [640, 360]
  remoteKeyTemplate: "{category}/{slug}/{filename}"
  remoteUrlTemplate: "{publicBase}/{category}/{slug}/{filename}"
  siteYaml:
    thumbUrl: preview.thumbUrl
    screens: preview.screens
    siteUrl: preview.siteUrl
artifacts:
  textOnly: true
  forbiddenExtensions: [woff, woff2, ttf, otf, eot, webp, gif, ico, avif, pdf, zip, tar, gz]
media:
  editorial: remoteHttps
  gallery: remoteUrlsInSiteYaml
manifest: site.yaml
publish:
  script: scripts/publish_gallery_assets.py
validation:
  templates: monms validate
  librarySpec: pending
---

# RULES.md — MonMS Site Library specification

This file is the **official source of truth** for what constitutes a valid library site template. The YAML frontmatter above is the machine-readable contract — a future MonMS site-library validator will parse it. Human detail lives in the numbered rules below; terse frontmatter keys **imply** those sections.

MonMS engine repository: [https://github.com/ndx-video/monms](https://github.com/ndx-video/monms)

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

## R2 — Text-only artifacts in Git

The repository must not contain binary files. Gallery imagery is published to Backblaze B2 and referenced by URL in `site.yaml` (R3a, R10).

### Allowed (text)

| Extensions | Notes |
|------------|-------|
| `.gohtml` | MonMS templates |
| `.json` | Schema, seed data, config examples |
| `.yaml`, `.yml` | Manifest (`site.yaml`) |
| `.md` | Markdown documents / doctrees |
| `.css`, `.scss` | Stylesheets |
| `.svg` | Plain-text SVG only where used as text assets (not base64-heavy exports) |

### Forbidden (committed)

Images (`png`, `jpg`, `jpeg`, `webp`, `gif`, `ico`, `avif`), fonts (`woff`, `woff2`, `ttf`, `otf`, `eot`), archives (`zip`, `tar`, `gz`), PDFs, and any other binary blob.

Local gallery dev files (`thumb.*`, `screenNN.*`) at the site template root are **gitignored** — see R10.

Reviewers should treat unexpected file types as rejections. CI may add automated scanning later.

---

## R3 — Media policy

### R3a — Gallery assets (remote URLs in `site.yaml`)

Gallery thumbnails and screenshots are **remote HTTPS URLs** in `site.yaml`:

- `preview.thumbUrl` — required for gallery-ready templates
- `preview.screens` — optional ordered list of screenshot URLs
- `preview.siteUrl` — optional live demo

URLs point at a public object store (Backblaze B2). Path shape: `{publicBase}/{category}/{slug}/{filename}`.

Publish local dev blobs with [scripts/publish_gallery_assets.py](scripts/publish_gallery_assets.py) (see R10). Reject legacy `preview.imageUrl`.

### R3b — Editorial and runtime media (templates and schema)

Hero images, logos, backgrounds referenced in templates or seed data must use **remote HTTPS URLs** in text/HTML fields.

| Allowed | Forbidden |
|---------|-----------|
| `https://...` in schema/templates | Local image paths committed to Git |
| Documented CDN bases | Large `data:` URIs embedded in HTML or JSON |
| Same URL on staging and production (MonMS content rail) | PocketBase `file` fields for cross-environment publishable media |

See MonMS `docs/user-guide/media-urls.md` for editorial media at runtime.

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
  thumbUrl: https://{public-base}/marketing/minimal-landing/thumb.png
  screens:                     # optional, ordered
    - https://{public-base}/marketing/minimal-landing/screen01.png
  siteUrl: null                # optional HTTPS live demo URL
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
| `preview.thumbUrl` | Yes | Remote HTTPS; gallery thumbnail (R10) |
| `preview.screens` | No | Ordered list of remote HTTPS screenshot URLs |
| `preview.siteUrl` | No | Optional hosted demo |
| `tags` | Yes | Lowercase kebab-case strings |
| `author` | Yes | |
| `license` | No | SPDX; omit for MIT |
| `default` | No | `true` only on the single canonical default template (`_base/_default`) |

Do not use `preview.imageUrl` (legacy).

---

## R5 — MonMS site shape

A template must be a valid MonMS L2 site directory.

### Minimum required paths

```
site.yaml                       # includes preview.thumbUrl (R4)
templates/layouts/base.gohtml
templates/index.gohtml
schema/
.monms/config.example.json
```

### Recommended (when used by the template)

```
templates/fragments/
templates/errors/
assets/                         # text-only per R2
documents/                      # markdown content rail
doctrees/
Dockerfile.example
docker-compose.example.yml
```

### Validation

**Template lint** (today) — must pass against a current MonMS build:

```bash
monms validate -s sites/<category>/<slug>
```

**Library spec** (future) — a separate validator will check frontmatter rules, `site.yaml` preview URLs, and text-only Git tree.

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
- Reference images via text URL fields (R3b), not PocketBase file uploads.
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

## R10 — Gallery assets (local dev + remote publish)

Gallery imagery is **not** committed to Git. Contributors maintain local files at the **site template root**, upload to B2, and commit the resulting URLs in `site.yaml`.

### Local dev files (gitignored)

At `sites/<category>/<slug>/` (not in a subfolder):

| File pattern | Required locally | Notes |
|--------------|------------------|-------|
| `thumb.{svg,png,jpg,jpeg}` | Before publish | 640×360 thumbnail |
| `screen01.{ext}`, `screen02.{ext}`, … | Optional | Two-digit, **one-based** sequence |

### Thumbnail dimensions

| Format | Rule |
|--------|------|
| Raster (`png`, `jpg`, `jpeg`) | Exactly **640 × 360** pixels |
| SVG | `width="640"` `height="360"` and `viewBox="0 0 640 360"` (or equivalent) |

### Format preference

When multiple local files share a basename (e.g. `thumb.png` and `thumb.jpg`), the publish script uploads **one** file using this order:

1. `svg`
2. `png`
3. `jpg`
4. `jpeg`

### Remote object layout

| Property | Value |
|----------|-------|
| Object key | `{category}/{slug}/{basename}.{ext}` (optional `B2_PATH_PREFIX/` prepended) |
| Public URL | `{B2_PUBLIC_BASE_URL}/[{B2_PATH_PREFIX}/]{category}/{slug}/{basename}.{ext}` |

Example: `_base/_default/thumb.png` → `https://cdn.example.com/_base/_default/thumb.png`

### Publish workflow

```bash
cp .env.example .env   # fill B2 credentials once
python scripts/publish_gallery_assets.py --site sites/<category>/<slug>
```

The script uploads resolved local files and patches `site.yaml` → `preview.thumbUrl` and `preview.screens`.

Use `--dry-run` to preview uploads and YAML changes without writing.

### Accepted upload formats

`svg`, `png`, `jpg`, `jpeg` only. No fonts, archives, or other formats.

---

## Quick reference

```
sites/<category>/<slug>/     ← only valid template location
site.yaml                    ← preview.thumbUrl + optional preview.screens
thumb.* / screenNN.*         ← local dev only (gitignored); publish to B2
text-only in Git             ← no committed binaries
remote HTTPS                 ← gallery + editorial imagery
publish_gallery_assets.py    ← upload local blobs, patch site.yaml
monms validate               ← template lint before merge
RULES.md frontmatter         ← machine-readable spec for library validator
```
