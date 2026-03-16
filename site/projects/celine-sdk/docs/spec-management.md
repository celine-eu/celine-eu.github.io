# Spec Management

The `celine-sdk` CLI manages versioned OpenAPI specifications and generates typed Python clients from them.

## services.yaml

`services.yaml` declares which services to fetch specs from:

```yaml
services:
  digital-twin:
    package: dt
    openapi: http://dt:8000/openapi.json
  policies:
    openapi: http://policies:8000/openapi.json
  datasets:
    package: datasets
    openapi: http://datasets:8000/openapi.json
```

Fields:
- `package` — Python sub-package name under `celine.sdk.openapi.<package>`. Defaults to the service key with hyphens replaced by underscores.
- `openapi` — URL of the live OpenAPI JSON endpoint.

## Commands

### `celine-sdk spec fetch`

Fetches each service's OpenAPI spec and writes it versioned under `openapi/`:

```bash
celine-sdk spec fetch services.yaml
```

Output layout:
```
openapi/
  digital-twin/
    v1/
      openapi.json
  policies/
    v1/
      openapi.json
```

Versioning is derived from the `info.version` field in the OpenAPI document. Existing versions are not overwritten.

### `celine-sdk spec list`

Lists all discovered versions for all services:

```bash
celine-sdk spec list
```

### `celine-sdk generate`

Generates typed Python client packages from the fetched specs. Requires the `[gen]` extra:

```bash
pip install 'celine-sdk[gen]'
celine-sdk generate services.yaml
```

Generated clients are placed under `src/celine/sdk/openapi/<package>/` and expose typed request/response models and API functions.

## Using Generated Clients

```python
from celine.sdk.openapi.datasets.api.catalogue import list_catalogue_catalogue_get
from celine.sdk.auth import OidcTokenProvider

token = await provider.get_token()
result = await list_catalogue_catalogue_get.asyncio(
    client=httpx.AsyncClient(base_url="http://datasets:8000"),
    authorization=f"Bearer {token.access_token}",
)
```

## Workflow

1. Start all CELINE services locally
2. Run `celine-sdk spec fetch services.yaml` to snapshot current specs
3. Run `celine-sdk generate services.yaml` to regenerate clients
4. Commit both `openapi/` and `src/celine/sdk/openapi/` to version control
