# Architecture

## Service Flow

The CELINE Dashboards stack layers several components to deliver SSO-protected analytics services:

1. The user's browser (or CLI) makes a request to a service URL.
2. Caddy receives the request and calls oauth2-proxy via `forward_auth` to verify the session.
3. If the session is valid, oauth2-proxy injects identity headers (`X-Auth-Request-User`, `X-Auth-Request-Access-Token`) and Caddy proxies the request to the target service.
4. If no valid session exists, oauth2-proxy redirects the browser to Keycloak for OIDC login.
5. On successful login, Keycloak issues tokens, oauth2-proxy creates a session cookie, and the user is redirected back.

## Component Roles

| Component | Port (local) | Purpose |
|---|---|---|
| Caddy | 80 / 443 | Reverse proxy, forward_auth, virtual hosting |
| oauth2-proxy | internal | OIDC session management, header injection |
| Keycloak | 8080 | Identity provider, realm management |
| Superset | internal | Analytics dashboards |
| Jupyter | internal | Notebook execution |

## Auth Chain

```
Request → Caddy
  → oauth2-proxy (forward_auth)
    → Keycloak (if no session)
  → inject headers
  → Superset / Jupyter
    → local SecurityManager / JWT authorizer
```

## Identity Propagation

oauth2-proxy injects the following headers into upstream requests:

| Header | Content |
|---|---|
| `X-Auth-Request-User` | Username from Keycloak |
| `X-Auth-Request-Email` | Email from Keycloak |
| `X-Auth-Request-Access-Token` | Keycloak access token (JWT) |
| `X-Auth-Request-Groups` | Comma-separated group memberships |

Superset and Jupyter each consume these headers to establish the user session and enforce authorization locally. No direct Keycloak calls are made by the applications at request time.

## Multi-Host Setup

Services are exposed under `*.celine.localhost` subdomains for local development:

| Subdomain | Service |
|---|---|
| `superset.celine.localhost` | Apache Superset |
| `jupyter.celine.localhost` | Jupyter |
| `sso.celine.localhost` | oauth2-proxy |
| `keycloak.celine.localhost` | Keycloak |

oauth2-proxy is configured with `skip_jwt_bearer_tokens = true` to allow service/CLI tokens to bypass the browser SSO flow.
