# CELINE Dashboards

This repository contains the **CELINE BI Dashboards**, a customized deployment of **Apache Superset** integrated with **oauth2-proxy** and **Keycloak** for enterprise-grade authentication and authorization.

The goal of this repository is to provide a **production-ready, extensible, and secure Superset setup** aligned with the CELINE platform architecture.

---

## ✨ Key Features

- Apache Superset with custom security manager
- Authentication delegated to oauth2-proxy + Keycloak
- JWT-based identity propagation
- Automatic user provisioning and role synchronization
- Group-to-role mapping driven by Keycloak claims
- Docker-first development and deployment
- Local development environment with docker-compose

---

## 🏗 Architecture Overview

```
User Browser
   │
   ▼
oauth2-proxy  ──►  Keycloak (OIDC)
   │
   ▼
Apache Superset
   │
   ├─ Custom SecurityManager
   ├─ JWT validation
   └─ Role mapping
```

Authentication flow:

1. User accesses Superset
2. oauth2-proxy enforces authentication via Keycloak
3. oauth2-proxy injects identity headers / JWT
4. Superset validates the JWT
5. User is auto-created or updated
6. Roles are synced from Keycloak groups

---

## 📁 Repository Structure

```
.
├── config/
│   ├── superset/          # Superset configuration
│   ├── keycloak/          # Keycloak realm and client configuration
│   ├── oauth2-proxy/      # oauth2-proxy configuration
│   └── caddy/             # Reverse proxy configuration
│
├── packages/
│   └── celine-superset/   # Custom Superset extensions
│       └── celine_superset/
│           └── auth/      # Custom authentication logic
│
├── docker-compose.yaml
├── Dockerfile
├── taskfile.yaml
└── README.md
```

---

## 🔐 Authentication & Authorization

### Authentication

- Superset authentication is **fully delegated** to oauth2-proxy
- Superset does **not** handle passwords or login forms
- `/login/` and `/logout/` are overridden to redirect to oauth2-proxy

### Authorization

- Users are mapped automatically based on JWT claims
- Keycloak groups are mapped to Superset roles

Example mapping (configurable):

```python
GROUP_TO_SUPERSET_ROLE = {
    "admins": "Admin",
    "managers": "Alpha",
    "editors": "Beta",
    "viewers": "Gamma",
}
```

Users are:
- auto-created on first login
- updated on every login
- kept in sync with Keycloak groups

---

## 🚀 Getting Started (Local Development)

### Prerequisites

Install the following tools:

- Docker
- Docker Compose
- Task (https://taskfile.dev)

---

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

3. Start the stack

```bash
docker compose up -d
```

4. Access services

- Superset: http://superset.celine.localhost
- Keycloak: http://keycloak.celine.localhost

---

## 🧪 Development Notes

- The Superset container runs with live-mounted code
- Changes to `packages/celine-superset` are picked up immediately
- JWT verification is handled inside Superset for defense-in-depth

---

## 🧩 Extending Authentication Logic

Custom logic lives in:

```
packages/celine-superset/celine_superset/auth/
```

Key components:

- `CustomSecurityManager`
- JWT extraction and validation helpers
- Role resolution helpers
- Custom `AuthRemoteUserView` for login/logout overrides

This design allows:
- swapping identity providers
- changing claim formats
- adding custom authorization rules

---

## 📦 Docker Images

The Superset image is built and published automatically via GitHub Actions.

Image name:

```
ghcr.io/celine-eu/superset:<version>
```

Docker tags follow this pattern <superset version>-<celine customizations version> e.g. `6.0.0-0.1.0`

See `version.txt` for current released version

---

## 🤝 Contributing

Contributions are welcome.

Guidelines:

- Keep authentication logic stateless
- Do not introduce Superset-native login flows
- Ensure JWT handling remains defensive
- Add tests for any auth-related changes

---

## 📄 License

This project is part of the **CELINE** initiative and follows the licensing terms defined by the CELINE consortium.

For more information:
- Project website: https://celineproject.eu
- Open-source tools: https://celine-eu.github.io

