# celine-eu.github.io

Documentation aggregator for the CELINE project. Produces a unified MkDocs Material site at [celine-eu.github.io](https://celine-eu.github.io) by cloning external repositories, copying their docs, and building a merged navigation.

## How it works

1. `repos.yaml` declares each source repository: git URL, file globs to copy (`paths`), navigation structure (`nav`), and optional cross-site links (`links`).
2. `scripts/build.py` is the build orchestrator. It clones/pulls each repo into `.work/<slug>`, copies matching paths into `site/projects/<slug>`, generates a tools index, materializes symlink-style links (ontology, schema), renders `mkdocs.yml` from `mkdocs.tpl.yml`, and runs `mkdocs build`.
3. `mkdocs.tpl.yml` is the MkDocs config template. The build script merges the `Tools` nav section from `repos.yaml` into this template and writes the final `mkdocs.yml` (gitignored, regenerated every build).
4. `docs/` is the MkDocs output directory (committed to the repo for GitHub Pages serving). `site/` is the MkDocs source directory (`docs_dir`).

### Build trigger

The GitHub Actions workflow (`.github/workflows/build-site.yml`) runs on:
- push to `main`
- `repository_dispatch` with type `celine-docs-update` (sent by `update-docs.yml` workflows in other CELINE repos)
- manual `workflow_dispatch`

It runs `task ci` (install + clean + build), then commits and pushes any changes in `docs/`.

### Directory layout

```
.work/              # gitignored, cloned repos
site/               # mkdocs source (docs_dir)
  index.md          # landing page (committed, hand-authored)
  projects/         # generated per-repo docs (generated at build time)
  ontologies/       # materialized from celine-ontologies release
  schema/           # materialized from celine-utils schema
docs/               # mkdocs output (site_dir, committed for GitHub Pages)
scripts/
  build.py          # main build orchestrator
  generate_ontology_docs.py  # RDF/TTL to markdown index generator
  dump_source.py    # LLM context dump utility (reads dump.yaml)
```

### Key conventions

- `README.md` in any source repo is always renamed to `index.md` during copy (MkDocs landing page convention).
- `links` entries in `repos.yaml` copy content from one `site/` path to another (e.g. ontology releases to `site/ontologies/`). Widoco HTML output gets an `index.md` wrapper with a link to `index-en.html`.
- `links` with a `list` config auto-generate an `index.md` listing files by extension.
- The nav in `repos.yaml` uses `README` as a sentinel for the repo root index, dict entries for explicit titles, and bare strings for auto-titled entries.

## Editing guide

### Adding a new repository

Add an entry to `repos.yaml` with `name`, `slug`, `git`, `paths`, and `nav`. The build script handles the rest. No changes to `mkdocs.tpl.yml` needed unless adding a new top-level nav section.

### Changing the landing page or top-level nav

Edit `site/index.md` for landing page content. Edit `mkdocs.tpl.yml` for top-level navigation structure. Do not edit `mkdocs.yml` directly — it is regenerated.

### Adding ontology or schema links

Use the `links` key in `repos.yaml` to expose nested content at a top-level `site/` path.

## Local development

```
task install     # uv sync
task build       # clone repos + generate mkdocs.yml + mkdocs build
task serve       # build + mkdocs serve on :9901
task rebuild     # clean + build from scratch
```

Requires `uv` and `task` (go-task).

## Rules

- Never edit `mkdocs.yml` — it is generated. Edit `mkdocs.tpl.yml` for template changes or `repos.yaml` for per-repo nav.
- Never edit files under `docs/` — they are build output. Edit sources under `site/` or in the upstream repo.
- Never edit files under `.work/` or `site/projects/` — they are cloned/generated at build time.
- `site/index.md` and `site/ontologies/` static assets are committed and hand-maintained.
- Keep `repos.yaml` as the single source of truth for which repos and docs are included.
