# Contributing to monms-sites

Thank you for helping build the MonMS Site Library. This repo is public and [MIT licensed](LICENSE). Contributions must follow [RULES.md](RULES.md) — reviewers treat that file as the merge contract.

AI agents should also read [AGENTS.md](AGENTS.md).

## Before you start

1. **Fork** this repository on GitHub.
2. **Clone** your fork and add the upstream remote if you plan to sync often.
3. **Build MonMS** from the engine repository (sibling checkout `../MonMS/` is typical):

   ```bash
   cd ../MonMS
   go build -o monms .
   export MONMS_BIN="$(pwd)/monms"
   ```

4. Read [RULES.md](RULES.md) in full — especially text-only artifacts (R2), remote media (R3), and `site.yaml` (R4).

## Adding a new template

1. **Pick a category** from the allowlist in [RULES.md](RULES.md) R8, or propose a new one with rationale in your PR.

2. **Create the directory:**

   ```
   sites/<category>/<slug>/
   ```

   Use lowercase kebab-case. `slug` must be unique across the entire repo.

3. **Scaffold the MonMS site shape.** Start from `monms init` output in a temp directory, or hand-author the minimum required paths (R5):

   ```
   templates/layouts/base.gohtml
   templates/index.gohtml
   schema/
   .monms/config.example.json
   ```

   For template conventions, see MonMS `docs/operators/shaping-and-agents.md` and `.cursor/skills/monms-site-shaping/SKILL.md`.

4. **Add `site.yaml`** at the template root. Fields and examples are in [RULES.md](RULES.md) R4. Ensure `slug` and `category` match directory names.

5. **Strip binaries.** No images, fonts, PDFs, or archives anywhere in the template. Replace local media references with remote HTTPS URLs.

6. **Validate:**

   ```bash
   export MONMS_BIN=../MonMS/monms   # adjust path as needed
   monms validate -s sites/<category>/<slug>
   ```

7. **Open a pull request** against `main`. Describe the template purpose, category choice, and validation output. Use remote preview URLs only — do not attach binary screenshots to the PR; link `preview.imageUrl` or a hosted demo instead.

Prefer **one new template per PR** when possible.

### Changing the default scaffold

`sites/_base/_default/` mirrors `monms init` in the MonMS engine (`internal/scaffold/embed/`). When you change `_default`:

1. Diff against `../MonMS/internal/scaffold/embed/` and keep them aligned (or note intentional divergence in the PR).
2. Bump `site.yaml` `version`.
3. Validate all templates:

   ```bash
   cd sites/_base/_default
   monms validate -s "$(pwd)" \
     "$(pwd)/templates/index.gohtml" \
     "$(pwd)/templates/layouts/base.gohtml" \
     "$(pwd)/templates/doc.gohtml" \
     "$(pwd)/templates/errors/errors.gohtml"
   ```

Only `_default` may set `default: true` in `site.yaml`.

## Updating an existing template

1. Bump `version` in `site.yaml` per [RULES.md](RULES.md) R9.
2. Note breaking changes in the PR description (removed pages, renamed collections, routing changes).
3. Re-run `monms validate -s sites/<category>/<slug>`.
4. Keep changes scoped to that template unless a cross-cutting rule change requires repo-wide updates.

## PR checklist

Copy into your PR description and check each item:

- [ ] Path is `sites/<category>/<slug>/` with kebab-case names
- [ ] `site.yaml` present; `slug` and `category` match directories
- [ ] `site.yaml` `version` bumped for this change
- [ ] No binary files anywhere in the template
- [ ] `preview.imageUrl` is a remote HTTPS URL
- [ ] `monms validate -s sites/<category>/<slug>` passes (paste command output or note `MONMS_BIN` used)
- [ ] No `.pb_data/`, `.monms/config.json`, `content/`, secrets, or runtime logs
- [ ] Placeholder copy is generic and appropriately licensed
- [ ] New category (if any) justified in PR description

## Review

Maintainers: **NDX** (initial stewardship).

Reviews focus on:

- [RULES.md](RULES.md) compliance
- Template quality and MonMS idioms (layout pattern, schema shape, HTMX if used)
- Whether the template fills a distinct gallery niche

## Local development tips

```bash
# Validate from repo root
export MONMS_BIN=../MonMS/monms
monms validate -s sites/<category>/<slug>

# Optional: serve the template directly for manual testing
monms serve -s sites/<category>/<slug> --http=127.0.0.1:8090
```

Serving creates `.pb_data/` locally — never commit it.

### Checking for accidental binaries

```bash
# From repo root — inspect suspicious files before PR
find sites/<category>/<slug> -type f ! -name '*.gohtml' ! -name '*.json' \
  ! -name '*.yaml' ! -name '*.yml' ! -name '*.md' ! -name '*.css' \
  ! -name '*.scss' ! -name '*.svg' -print
```

Future CI may automate binary scanning and `monms validate` across all templates.

## What we do not merge

- Binary assets (images, fonts, archives) — [RULES.md](RULES.md) R2
- Templates outside `sites/<category>/<slug>/` — R1
- Missing or invalid `site.yaml` — R4
- Secrets, production config, or `.pb_data/` — R6
- Engine changes (belong in the MonMS repository)

## Questions

Open a GitHub issue for category proposals, manifest schema changes, or gallery integration questions. Engine feature work (dashboard gallery, `monms init --from-gallery`) belongs in the MonMS repository.
