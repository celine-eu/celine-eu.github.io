# Spec management

The `celine-sdk` CLI and the conversion helpers around the generated clients. This is the
machinery that turns a running service's OpenAPI document into a typed Python client
committed in `src/celine/sdk/openapi/`.

The procedure for running it is the companion's playbook for regenerating the clients; what it must do
is here.

---

## Declaring services

### REQ-0100 — the services are declared in one manifest

`services.yaml` maps a service name to its spec URL and, optionally, the Python package the
client should occupy. A document that is not a mapping, or that does not validate, is
refused rather than partially honoured.

### REQ-0101 — a package name is normalised to a Python identifier

The declared override, else the service name, lowercased with every non-alphanumeric
character reduced to `_`, runs collapsed, and edges trimmed. A name that reduces to nothing
becomes `service`. So `rec-registry` becomes `rec_registry` and is importable as
`celine.sdk.openapi.rec_registry`.

---

## Fetching and versioning specs

### REQ-0102 — a spec is accepted as JSON or as YAML

JSON is tried first, YAML is the fallback, and anything that is not a mapping is refused.
Services publish either.

### REQ-0103 — a spec without `info.version` is refused

The version is what the spec is filed under. Without it there is nothing to compare against
the next fetch, so it is a `ValueError` rather than an unnamed snapshot.

### REQ-0104 — a spec is stored under its service and version, byte-stable

`openapi/<service>/v<version>/openapi.json`, written with sorted keys and a fixed indent so
that re-fetching an unchanged spec produces no diff.

**A re-fetch of the same `info.version` overwrites the stored spec.** A service that changed
its API without bumping its version replaces the snapshot in place, and the only signal is
the diff. That is the moment to check whether the version should have moved.

### REQ-0105 — stored versions are ordered by number, and the latest is the last of them

`list_versions` returns the `v*` directories in order; `latest_version` is the last. Each
dotted component is compared **numerically**, so `v0.2.0` precedes `v0.10.0` — plain
character ordering reversed those, and generation would then have built clients from an
older spec without saying so.

Full semantic-version precedence is not implemented: a component that does not begin with a
digit sorts after every numeric one, and a pre-release suffix sorts *after* the release it
qualifies. The guarantee is a stable total order that gets the numbers right, not semver.

### REQ-0106 — one service's failure does not stop the others

A spec that cannot be fetched or parsed is reported and the fetch continues. One service
being down must not prevent snapshotting the rest.

---

## Generating clients

### REQ-0107 — generation reads the stored specs, never the network

`celine-sdk generate` uses the latest spec on disk. Fetching and generating are separate
steps so that what was generated is always reproducible from what is committed.

### REQ-0108 — a missing spec fails generation loudly

No stored version for a declared service, or a missing `openapi.json`, is a `RuntimeError`
naming the service and the command to run. Generating a client from nothing would produce a
package that imports and does nothing.

### REQ-0115 — a change reports which repositories it reaches, and fails on a name it removed

This package is imported by most of the platform and tested by none of it, so the question
its own suite cannot answer is *who would notice?* `task impact` answers it from the sibling
repositories in the workspace, and runs as the third step of `task gen`.

Three readings, and the last two are a gate:

1. **Reach** — the repositories importing each module the change touched.
2. **Removed public names still imported somewhere** — names that existed at the base
   revision, do not exist now, and are named by a consumer.
3. **Unresolved imports** — every `(module, name)` any consumer imports, resolved against
   this working tree. Independent of the diff, so it catches what a diff cannot: a name that
   moved between packages, a module that now fails at import time, a generated model that
   vanished in a regeneration.

Finding anything in 2 or 3 exits non-zero.

Precision matters more than recall here, because a report that cries wolf is one nobody runs:

- A name that moved and is **re-exported** from where it was is not removed. Removal is
  measured against everything importable from the module now, not only what it defines.
- A module's **imports are not its public surface** for this purpose: `Any` vanishing from a
  deleted module is not a loss anyone can suffer.
- **Vendored code is not a consumer.** Dot-directories especially — the documentation site
  keeps checkouts of every other repository under `.work/`, which counted naively makes it
  appear to import everything and double-counts every real consumer through it.

What it cannot see is stated in its own output: a consumer outside the workspace, a name
reached through `getattr`, and any behaviour change that keeps its signature. Those need a
consumer's own suite, which is what `task dev:link` in the workspace exists for.

### REQ-0114 — the generated packages are exactly the declared services

Every subpackage of `celine.sdk.openapi` corresponds to an entry in `services.yaml`, and
every entry has a subpackage. Neither half is decoration:

- **A package with no entry is never regenerated.** Generation replaces packages per manifest
  entry, so an orphan is frozen at whenever it was last produced while still looking current.
  `celine.sdk.openapi.policies` sat that way long enough to describe an API the platform no
  longer serves.
- **An entry with no package means the fetch has been failing.** A spec URL the platform does
  not route returns an empty body rather than a 404, and `spec fetch` reports it in one line
  and carries on (REQ-0106). `ai_assistant` was missing for exactly that reason.

Both are silent by construction, which is why this is asserted rather than reviewed.

### REQ-0113 — a missing code generator is reported as a broken environment

The generators are external commands, and they are **declared in this project** —
`pyproject.toml`, the `dev` dependency group, marked `python_version >= "3.11"`. One of them
missing therefore means the environment is wrong: the group was never synced, or the
interpreter is 3.10, where they do not install.

When one is not on `PATH`, generation fails with an error that names the command, says where
it is declared, and points at `uv sync`. The bare `FileNotFoundError` this replaces named the
binary and nothing else.

Why the generators are not installable from an index at all:
`docs/decisions/ADR-0001-no-published-generation-extra.md`.

### REQ-0109 — the destination package is replaced wholesale

The previous package directory is removed before the new one is copied in, so a route or a
model deleted upstream disappears here too. Merging would leave clients for endpoints that
no longer exist.

---

## The boundary around generated code

### REQ-0110 — a generated object converts to a Pydantic schema and back

`to_schema` validates a generated client object's `to_dict()` into a schema class;
`to_client` renders a schema back into a generated class via `from_dict`. `None` in is
`None` out on both, so an optional field needs no branch at every call site.

This pair is the whole reason services can hold typed Pydantic models while the wire types
are regenerated beneath them.

### REQ-0111 — converting to a client sends only what was set

`to_client` dumps in JSON mode, by alias, excluding unset fields — so an omitted field stays
omitted rather than being transmitted as its default and overwriting a value on the server.

### REQ-0112 — an unparsed response becomes a typed error carrying the evidence

`unwrap` returns the parsed payload, or raises `DTApiError` with the status code and the raw
body. The body is kept because a failed call's only diagnosis is usually what the service
actually said.
