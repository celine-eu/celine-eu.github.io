# Spec Management

The `celine-sdk` CLI snapshots the OpenAPI specifications of CELINE services and generates
typed Python clients from them. What it must do is stated in
[specifications/spec-management.md](specifications/spec-management.md); the procedure for
doing it in this repository, with its traps, is the companion's playbook for regenerating the clients.

Fetching and generating are **two steps on purpose**: what is generated is always
reproducible from the specs committed under `openapi/`, without the services running.

## services.yaml

```yaml
services:
  digital-twin:
    package: dt
    openapi: http://api.celine.localhost/dt/openapi.json
  rec-registry:
    package: rec_registry
    openapi: http://api.celine.localhost/rec-registry/openapi.json
  datasets:
    openapi: http://api.celine.localhost/datasets/openapi.json
```

- `openapi` — URL of the service's OpenAPI document. JSON or YAML.
- `package` — Python sub-package under `celine.sdk.openapi.<package>`. Defaults to the
  service key, normalised to a Python identifier (`rec-registry` → `rec_registry`).

## Commands

```bash
task gen        # both steps: spec fetch, then generate
```

### `celine-sdk spec fetch [services.yaml] [--out-dir openapi] [--clean]`

Fetches each declared spec and writes it under its `info.version`:

```text
openapi/
  digital-twin/
    v0.4.1/
      openapi.json
  rec-registry/
    v1.2.0/
      openapi.json
```

- The file is written with sorted keys and a fixed indent, so an unchanged spec produces no
  diff.
- **Re-fetching the same `info.version` overwrites the stored spec.** A service that changed
  its API without bumping its version replaces the snapshot in place, and the diff is the
  only signal you get. Check for that before assuming a large diff is noise.
- A spec with no `info.version` is refused.
- A service that cannot be reached is reported and skipped; the others still fetch. Read the
  output — a skipped service means the client you generate next is the *previous* snapshot.

### `celine-sdk spec list [--out-dir openapi]`

Lists the versions on disk and which is considered latest.

Ordering is numeric per component, so `v0.9.0` precedes `v0.10.0`. It is not full semantic
versioning: a component that does not start with a digit sorts after every numeric one, and
a pre-release suffix sorts after the release it qualifies.

### `celine-sdk generate [services.yaml] [--specs-dir openapi] [--dest-root src/celine/sdk/openapi]`

Generates a client per service from the **latest spec on disk** — no network.

It needs the code generators, which are declared in this repository's `pyproject.toml` — the
`dev` dependency group, marked `python_version >= "3.11"`. `uv sync` in a checkout installs
them; they are not published with the package, because regeneration is a maintainer task
performed here and a consuming service never does it
([ADR-0001](decisions/ADR-0001-no-published-generation-extra.md)).

So one being absent means the environment is wrong — an unsynced group, or a 3.10
interpreter. Generation says that, rather than dying on a bare "command not found".

Per service it runs `openapi-python-client` for the client and `datamodel-codegen` for
`schemas.py`, then replaces `src/celine/sdk/openapi/<package>/` **wholesale** — anything the
service deleted upstream disappears here too. A declared service with no stored spec is an
error naming the service.

## Using a generated client

The generated packages expose `Client` / `AuthenticatedClient`, `api.<tag>.<operation>` and
`models`. Most services should use the curated wrappers (`celine.sdk.dt`,
`celine.sdk.rec_registry`, `celine.sdk.nudging`, `celine.sdk.flexibility`,
`celine.sdk.ai_assistant`) rather than the generated surface directly.

```python
from celine.sdk.openapi.rec_registry import AuthenticatedClient
from celine.sdk.openapi.rec_registry.api.me import get_me_user_get

client = AuthenticatedClient(base_url="http://rec-registry:8000", token=token.access_token)
response = await get_me_user_get.asyncio_detailed(client=client)
```

### Crossing the boundary

`celine.sdk.utils.convert` converts between generated classes and Pydantic schemas so a
service can hold typed models over a wire type that is regenerated beneath it:

```python
from celine.sdk.utils.convert import to_schema, to_client

schema = to_schema(generated_obj, MyModelSchema)   # None in, None out
generated = to_client(schema, GeneratedModel)      # sends only fields that were set
```

`celine.sdk.dt.util.unwrap(response)` returns the parsed payload or raises `DTApiError`
carrying the status code and the raw body.

## Workflow

1. Start the CELINE services locally (or point `services.yaml` at published specs).
2. `uv run celine-sdk spec fetch` — snapshot the specs.
3. `uv run celine-sdk generate` — regenerate the clients.
4. Commit `openapi/` and `src/celine/sdk/openapi/` **in their own commit**: the diff is
   large and reviewers skim it, which is exactly where an unrelated change hides.

the companion's playbook for regenerating the clients covers what to check afterwards — the wrappers
that reference renamed operations, and the consumers this repository cannot test.
