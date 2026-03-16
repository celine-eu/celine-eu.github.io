# Authentication

The `celine.sdk.auth` module provides OIDC-based token management for CELINE services.

## Key Components

### OidcTokenProvider

Fetches and caches access tokens from a Keycloak-compatible OIDC provider using the client credentials flow. Automatically refreshes tokens before expiry.

```python
from celine.sdk.auth import OidcTokenProvider
from celine.sdk.settings import OidcSettings

settings = OidcSettings()
provider = OidcTokenProvider(settings)

token = await provider.get_token()
# token.access_token: str  — raw JWT
# token.expires_at: datetime
```

### StaticTokenProvider

For testing and local development, accepts a pre-configured static token:

```python
from celine.sdk.auth import StaticTokenProvider

provider = StaticTokenProvider(token="eyJ...")
```

### JWT Parsing

The `jwt` module parses tokens without re-verifying signature (for extracting claims from already-validated tokens):

```python
from celine.sdk.auth.jwt import parse_claims

claims = parse_claims(token_string)
# claims.sub, claims.groups, claims.scope, claims.exp
```

### OIDC Discovery

The `oidc_discovery` module fetches the OIDC well-known configuration from the provider's discovery endpoint, used internally to resolve the JWKS URI and token endpoint.

## AccessToken Model

```python
class AccessToken:
    access_token: str       # Raw JWT string
    token_type: str         # Always "Bearer"
    expires_in: int         # Seconds until expiry
    expires_at: datetime    # Absolute expiry timestamp
    scope: str              # Space-separated scopes
```

## Configuration

Auth settings come from `OidcSettings` (see [settings.md](https://celine-eu.github.io/projects/celine-sdk/docs/settings)):

| Variable | Description |
|---|---|
| `OIDC_ISSUER` | OIDC issuer URL (e.g., Keycloak realm URL) |
| `OIDC_CLIENT_ID` | Service client ID |
| `OIDC_CLIENT_SECRET` | Service client secret |
