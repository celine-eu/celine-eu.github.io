# ADR-0001 — The code generators are not published as an extra

**Date:** 2026-08-15
**Status:** accepted

## Context

`README.md` and `docs/spec-management.md` told users to run `pip install 'celine-sdk[gen]'`
before `celine-sdk generate`. No such extra exists: `pyproject.toml` declares no
`[project.optional-dependencies]` at all. The generators — `openapi-python-client` and
`datamodel-code-generator` — are in the `dev` dependency group, which is a PEP 735 group
that `uv sync` installs in a checkout and that is invisible to anyone installing from an
index. So the documented command installed nothing and the next one died on a missing
binary.

Two things had already been decided elsewhere and constrain this one:

- **The supported floor is Python 3.10**, proven by the CI matrix. Both generators require
  ≥ 3.11, which is why they carry markers in the `dev` group — without them `uv lock` was
  unsolvable at 3.10, and that is what had kept `requires-python` artificially high.
- **The generated tree is committed** (454 files). Consumers install a package that already
  contains the clients; nothing at their end regenerates anything.

Measured across the twenty repositories in the workspace: **no repository other than this
one invokes `celine-sdk generate` or `celine-sdk spec fetch`.** The only caller is this
repository's own `task gen`.

## Decision

Do not publish a `gen` extra. Generation is a maintainer task performed in a checkout of
this repository, with `uv sync`, and the documentation says so.

Make the failure legible instead: when a generator is not on `PATH`, `celine-sdk generate`
raises an error naming the command, stating that no such extra exists, and pointing at
`uv sync` (REQ-0113).

## Consequences

- The published documentation had to change rather than the packaging — including the copies
  on the documentation site, which are hand-copied from here and were still wrong at the
  time of writing.
- An extra would have needed the same `python_version >= "3.11"` markers as the `dev` group,
  so `pip install 'celine-sdk[gen]'` on 3.10 — the supported floor — would install nothing
  and fail exactly as before. A packaging feature that silently no-ops on a supported
  interpreter is worse than not having it.
- Someone will propose adding the extra again, because the command reads as though it should
  exist. The answer is the measurement above: publish it when a repository other than this
  one needs to generate a client, and deal with the 3.10 gap then.
- If that day comes, this ADR is superseded rather than edited.
