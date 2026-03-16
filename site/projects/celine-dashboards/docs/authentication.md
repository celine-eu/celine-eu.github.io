# Authentication

## Keycloak Realm Configuration

The repository ships a ready-to-import Keycloak realm definition at `config/keycloak/`.

**Realm:** `celine`

**Clients:**

| Client | Purpose |
|---|---|
| `oauth2_proxy` | Browser SSO flows |
| `celine-cli` | Service and CLI token issuance |

**Groups:**

| Group | Default Role |
|---|---|
| `/admins` | Full access |
| `/managers` | Manager-level access |
| `/editors` | Editor-level access |
| `/viewers` | Read-only access |

Demo users for each group are included in the realm export for local development.

## oauth2-proxy Setup

oauth2-proxy is the single authentication gateway for all browser sessions.

Key configuration (`config/oauth2-proxy/`):

| Setting | Value |
|---|---|
| Provider | `keycloak-oidc` |
| Client ID | `oauth2_proxy` |
| Cookie domain | `.celine.localhost` |
| Cookie secret | Set via `OAUTH2_PROXY_COOKIE_SECRET` env var |
| `skip_jwt_bearer_tokens` | `true` — allows service tokens to bypass browser SSO |
| `oidc_issuer_url` | `http://keycloak:8080/realms/celine` |

Cookie sharing across `*.celine.localhost` means a single login grants access to all subdomains.

## JWT Validation

Each application validates JWTs locally using the Keycloak JWKS endpoint:

```
http://keycloak:8080/realms/celine/protocol/openid-connect/certs
```

The JWKS is fetched once at startup and cached. JWT signatures use RS256.

## Service / CLI Tokens

Non-browser clients (scripts, pipelines) can use client credentials tokens from the `celine-cli` client:

```bash
curl -s http://keycloak.celine.localhost/realms/celine/protocol/openid-connect/token \
  -d "grant_type=client_credentials&client_id=celine-cli&client_secret=<secret>" \
  | jq .access_token
```

Pass the token as `Authorization: Bearer <token>`. oauth2-proxy will skip session validation for requests with a valid Bearer token.
