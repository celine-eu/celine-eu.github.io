# Services

## Superset

### Authentication

Superset uses `AUTH_REMOTE_USER` mode. Login and logout are fully delegated to oauth2-proxy — Superset never handles credentials directly.

The custom `OAuth2ProxySecurityManager` (in `packages/celine-superset/`) extends Superset's `RemoteUserSecurityManager`:

- Reads the `X-Auth-Request-Access-Token` header on each request
- Validates the JWT signature against the Keycloak JWKS endpoint
- Extracts user identity and group memberships from the token claims
- Auto-creates users on first login
- Synchronizes Superset roles on every login based on current group membership

### Group-to-Role Mapping

Keycloak groups are mapped to Superset roles in `packages/celine-superset/celine_superset/auth/roles.py`:

```python
GROUP_TO_SUPERSET_ROLE = {
    "admins": "Admin",
    "managers": "Alpha",
    "editors": "Beta",
    "viewers": "Gamma",
}
```

Users not in any mapped group receive no roles and cannot access Superset.

### Docker Image

```
ghcr.io/celine-eu/superset:<version>
ghcr.io/celine-eu/superset:latest
```

Version is defined in `version.txt`.

---

## Jupyter

### Authentication

Jupyter has no local passwords or tokens. All access control is enforced by the custom JWT authorizer in `packages/jupyter_jwt_auth/`.

The authorizer:
- Reads the `Authorization: Bearer <token>` header (injected by oauth2-proxy via Caddy)
- Validates the JWT signature against Keycloak JWKS
- Checks the user's group memberships from the token claims
- Grants access only to users in the configured allowed groups (default: `/admins`)

### Access Control

Edit the allowed groups in the Jupyter configuration:

```python
# config/jupyter/jupyter_server_config.py
c.JWTAuthenticator.allowed_groups = ["/admins", "/managers"]
```

### Docker Image

```
ghcr.io/celine-eu/jupyter:<version>
ghcr.io/celine-eu/jupyter:latest
```

Version is defined in `version.jupyter.txt`.

---

## Caddy

Caddy handles TLS termination and reverse proxying via virtual hosts and `forward_auth`.

Configuration is in `config/caddy/Caddyfile`. Key patterns:

- All `*.celine.localhost` traffic is routed through oauth2-proxy's `forward_auth` directive before proxying to the target service.
- The SSO endpoint (`sso.celine.localhost`) is proxied directly to oauth2-proxy for the login/callback flow.
- Keycloak (`keycloak.celine.localhost`) is proxied without auth to allow the OIDC discovery and JWKS endpoints to be reachable.
