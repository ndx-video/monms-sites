# Contributing to monms-sites

Contributions must follow [RULES.md](RULES.md). AI agents: [AGENTS.md](AGENTS.md).

MonMS engine: [https://github.com/ndx-video/monms](https://github.com/ndx-video/monms) — integration spec: [../MonMS/specs/site-library.md](../MonMS/specs/site-library.md).

## Before you start

1. Fork and clone this repository.
2. Build MonMS from `../MonMS/`:

   ```bash
   cd ../MonMS && go build -o monms .
   export MONMS_BIN="$(pwd)/monms"
   ```

3. Read [RULES.md](RULES.md) — especially R2 (text-only Git), R4 (`site.yaml`), R10 (gallery publish), R11 (`DESIGN.md`).

## Gallery assets

Gallery images are **not** committed. Workflow:

1. Add `thumb.png` (640×360) at `sites/<category>/<slug>/thumb.png` (gitignored).
2. Optionally add `screen01.png`, `screen02.png`, … at the same level.
3. Copy [.env.example](.env.example) to `.env` and fill Backblaze B2 credentials.
4. Install script dependencies (venv recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r scripts/requirements.txt
   ```

5. Publish and patch `site.yaml`:

   ```bash
   python scripts/publish_gallery_assets.py --site sites/<category>/<slug>
   ```

   Use `--dry-run` to preview uploads and URL changes without writing.

6. Commit only `site.yaml` (with `preview.thumbUrl` and optional `preview.screens`) — not the image files.

Remote URL shape: `{B2_PUBLIC_BASE_URL}/{category}/{slug}/{filename}`

## Adding a new template

1. Pick a category from [RULES.md](RULES.md) R8 or propose a new one in your PR.

2. Create `sites/<category>/<slug>/` with minimum paths (R5):

   ```
   site.yaml
   DESIGN.md
   templates/layouts/base.gohtml
   templates/index.gohtml
   schema/
   .monms/config.example.json
   ```

3. Scaffold from `sites/_base/_default/` or `monms init` output.

4. Write `DESIGN.md` describing this template's visual system (R11). Use the [DESIGN.md format](https://github.com/google-labs-code/design.md) — see `sites/_base/_default/DESIGN.md` for an example. Align tokens with `assets/main.css` and template classes.

5. Add gallery assets (workflow above).

6. Validate:

   ```bash
   monms validate -s sites/<category>/<slug>
   ```

7. Open a PR — one template per PR when possible.

### DESIGN.md lint (advisory)

Templates with `DESIGN.md` can be checked against the upstream spec:

```bash
npx @google/design.md lint sites/<category>/<slug>/DESIGN.md
```

Or lint every template in the repo:

```bash
./scripts/lint_design_md.sh
```

Lint is **advisory** — it does not block validation or merge.

## PR checklist

- [ ] Path is `sites/<category>/<slug>/`
- [ ] `site.yaml`: `slug`/`category` match directories; `preview.thumbUrl` is HTTPS
- [ ] `DESIGN.md` present and describes this template's visual system (R11)
- [ ] No `preview.imageUrl` (legacy)
- [ ] No committed binary files (`thumb.*`, `screenNN.*`, images, fonts)
- [ ] Publish script run if gallery assets changed
- [ ] `monms validate` passes
- [ ] No `.pb_data/`, secrets, or runtime logs
- [ ] `version` bumped in `site.yaml` for this change

## What we do not merge

- Committed image or binary files — R2
- Missing `preview.thumbUrl` on gallery-ready templates — R4
- `preview.imageUrl` — legacy
- Templates outside `sites/<category>/<slug>/` — R1

## Questions

Open a GitHub issue for spec changes. Engine gallery implementation: MonMS repo (`specs/site-library.md`).
