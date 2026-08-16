# celine-eu.github.io

Documentation aggregator for the CELINE project. Produces a unified MkDocs Material site
at [celine-eu.github.io](https://celine-eu.github.io) by cloning the component
repositories, copying their documentation, and building a merged navigation.

This repository publishes other repositories' documentation. It authors almost none of
its own.

## ⚠️ `site/` is the source; `docs/` is the output

The two are the opposite way round from every other repository here:

| Directory | Is | Edit it? |
|---|---|---|
| `site/` | MkDocs `docs_dir` — the **source** | yes, where it is hand-authored |
| `docs/` | MkDocs `site_dir` — the **build output**, committed so GitHub Pages can serve it | **never** |

`scripts/build.py` runs `mkdocs build --clean`, which removes anything in `docs/` that the
build did not produce. A file placed there by hand is deleted by the next build, without
warning and without a diff anyone reads.

## How it works

1. **`repos.yaml`** declares each source repository: git URL, file globs to copy (`paths`),
   navigation structure (`nav`), and optional cross-site links (`links`).
2. **`scripts/build.py`** orchestrates. It clones or pulls each repository into
   `.work/<slug>`, copies matching paths into `site/projects/<slug>`, generates a tools
   index, materialises link-style content (ontology, schema), renders `mkdocs.yml` from
   `mkdocs.tpl.yml`, and runs `mkdocs build --clean`.
3. **`mkdocs.tpl.yml`** is the config template. The build merges the `Tools` nav section
   from `repos.yaml` into it and writes `mkdocs.yml`, which is gitignored and regenerated
   every build.

### Directory layout

```text
repos.yaml          which repositories are published, and how
mkdocs.tpl.yml      config template — edit this, never mkdocs.yml
scripts/
  build.py          the orchestrator
  generate_ontology_docs.py   RDF/TTL to markdown index
  check_staleness.py          documentation staleness across repositories
  dump_source.py              LLM context dump, reads dump.yaml
.work/              gitignored — cloned source repositories
site/               MkDocs source
  index.md          landing page, hand-authored
  projects/         per-repository docs, generated at build time
  ontologies/       materialised from the ontologies release
  schema/           materialised from celine-utils
docs/               MkDocs output, committed for GitHub Pages
```

### Build trigger

`.github/workflows/build-site.yml` runs on push to `main`, on `repository_dispatch` of
type `celine-docs-update` (sent by the `update-docs.yml` workflow in each component
repository), and on manual dispatch. It runs `task ci`, then commits and pushes whatever
changed under `docs/`.

## Local development

```bash
task install    # uv sync
task build      # clone, generate mkdocs.yml, mkdocs build
task serve      # build, then serve on :9901
task rebuild    # clean, then build from scratch
task ci         # what GitHub Actions runs
task docs:stale # documentation staleness across repositories
```

Requires `uv` and `task` (go-task).

## Conventions and traps

The behaviours that are not visible from reading `build.py` once — the `README.md` to
`index.md` rename, how `links` and `nav` are interpreted, and which trees must never be
edited — are in `.agents/knowledge/`. Read them before changing the build.
