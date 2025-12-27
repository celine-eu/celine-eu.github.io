# CELINE Dashboards

This repository provides the **CELINE Dashboards stack**, a production‑ready analytics environment built around **Apache Superset** and **Jupyter**, secured through **Keycloak** and **oauth2‑proxy**, and fronted by **Caddy**.

The project is designed to deliver:
- centralized SSO authentication,
- consistent authorization across services,
- Docker‑first local development and deployment,
- extensible, auditable security logic aligned with the CELINE platform.

---

## Overview

The stack exposes multiple web services (currently **Superset** and **Jupyter**) behind a single authentication boundary. Authentication is fully delegated to Keycloak via oauth2‑proxy, while each application consumes identity and authorization data from trusted headers or JWTs.

Key goals:
- **No local passwords** in Superset or Jupyter
- **Automatic user provisioning**
- **Role and group synchronization from Keycloak**
- **Support for browser users and service / CLI tokens**

---

## Architecture

High‑level flow:

```
Browser / CLI
    |
    v
Caddy (reverse proxy)
    |
    +--> oauth2-proxy ----> Keycloak (OIDC)
    |
    +--> Superset
    |
    +--> Jupyter
```

Authentication and authorization flow:

1. User accesses a protected service (Superset or Jupyter).
2. Caddy delegates authentication to oauth2‑proxy (`forward_auth`).
3. oauth2‑proxy authenticates the user via Keycloak (OIDC).
4. Identity headers and access tokens are forwarded back to Caddy.
5. Requests are proxied to the target service.
6. Each service validates and enforces authorization locally:
   - Superset via a custom `SecurityManager`
   - Jupyter via a JWT‑based authorizer

---

## Repository Structure

```
.
├── config/
│   ├── caddy/              # Reverse proxy configuration
│   ├── keycloak/           # Realm, clients, groups, and demo users
│   ├── oauth2-proxy/       # oauth2-proxy configuration
│   ├── superset/           # Superset configuration and env files
│   └── jupyter/            # Jupyter server configuration
│
├── packages/
│   ├── celine-superset/    # Custom Superset authentication extension
│   └── jupyter_jwt_auth/   # JWT-based Jupyter authorizer
│
├── Dockerfile              # Superset image
├── Dockerfile.jupyter      # Jupyter image
├── docker-compose.yaml     # Full local stack
├── version.txt             # Superset image version
├── version.jupyter.txt     # Jupyter image version
├── taskfile.yaml           # Common developer tasks
└── README.md
```

---

## Services

### Superset

- Authentication type: `AUTH_REMOTE_USER`
- Login and logout fully delegated to oauth2‑proxy
- Custom `OAuth2ProxySecurityManager`:
  - validates JWT signatures via Keycloak JWKS
  - auto‑creates users on first login
  - synchronizes roles on each login
  - maps Keycloak groups to Superset roles

Group‑to‑role mapping is defined in:

```
packages/celine-superset/celine_superset/auth/roles.py
```

Example:

```python
GROUP_TO_SUPERSET_ROLE = {
    "admins": "Admin",
    "managers": "Alpha",
    "editors": "Beta",
    "viewers": "Gamma",
}
```

### Jupyter

- No local token or password authentication
- Access controlled by a custom JWT authorizer
- Authorization decisions based on JWT group claims
- Intended for notebook execution under the same SSO boundary

Only users in the `/admins` group currently receive full access by default.

---

## Authentication & Identity

### Keycloak

The repository ships with a ready‑to‑import Keycloak realm definition:

- Realm: `celine`
- Clients:
  - `oauth2_proxy` (browser SSO)
  - `celine-cli` (service and CLI tokens)
- Groups:
  - `/admins`
  - `/managers`
  - `/editors`
  - `/viewers`

Demo users are included for local development.

### oauth2‑proxy

oauth2‑proxy acts as the single authentication gateway:

- Handles browser login flows
- Injects identity headers and access tokens
- Supports service tokens via `skip_jwt_bearer_tokens`
- Shares cookies across `*.celine.localhost`

It is exposed through a dedicated SSO endpoint:

```
http://sso.celine.localhost
```

---

## Local Development

### Prerequisites

- Docker
- Docker Compose
- Task (https://taskfile.dev)

### Setup

1. Clone the repository

```bash
git clone https://github.com/celine-eu/celine-dashboards.git
cd celine-dashboards
```

2. Initialize environment files

```bash
task ensure-env
```

3. Start the full stack

```bash
docker compose up -d
```

4. Access services

- Superset: http://superset.celine.localhost
- Jupyter: http://jupyter.celine.localhost
- SSO / oauth2‑proxy: http://sso.celine.localhost
- Keycloak: http://keycloak.celine.localhost

---

## Docker Images & CI

Docker images are built and published automatically via GitHub Actions.

### Superset

```
ghcr.io/celine-eu/superset:<version>
ghcr.io/celine-eu/superset:latest
```

The version is defined in `version.txt`.

### Jupyter

```
ghcr.io/celine-eu/jupyter:<version>
ghcr.io/celine-eu/jupyter:latest
```

The version is defined in `version.jupyter.txt`.

Images are rebuilt automatically when relevant source or configuration files change.

---

## Extensibility

This repository is intentionally structured to allow:

- swapping or extending identity providers,
- customizing JWT claim formats,
- adding new services behind the same SSO boundary,
- refining role‑based access control logic.

Authentication logic is isolated in reusable Python packages and kept stateless.

---

## Contributing

Contributions are welcome.

Guidelines:
- Keep authentication logic stateless and defensive
- Do not introduce local login mechanisms
- Ensure JWT validation remains explicit and verifiable
- Add tests for any auth‑related changes

---

## License

Copyright © 2025 Spindox Labs

Licensed under the Apache License, Version 2.0.  
You may not use this file except in compliance with the License.

See http://www.apache.org/licenses/LICENSE-2.0 for details.
