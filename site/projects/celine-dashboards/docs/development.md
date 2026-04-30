# Development

## Prerequisites

- Docker and Docker Compose
- Task (https://taskfile.dev)

## Setup

```bash
# 1. Initialize environment files (generates secrets, writes .env files)
task ensure-env

# 2. Start the full stack
docker compose up -d

# 3. Access services
#   Superset:  http://superset.celine.localhost
#   Jupyter:   http://jupyter.celine.localhost
#   SSO:       http://sso.celine.localhost
#   Keycloak:  http://keycloak.celine.localhost
```

On first run, Keycloak imports the realm from `config/keycloak/`. Demo users are provisioned automatically.

## Stopping and Resetting

```bash
# Stop all services
docker compose down

# Stop and remove all data volumes (full reset)
docker compose down -v
```

## Rebuilding Images

```bash
# Rebuild the Superset image
docker compose build superset

# Rebuild the Jupyter image
docker compose build jupyter
```

## Service URLs

| Service | Local URL |
|---|---|
| Superset | http://superset.celine.localhost |
| Jupyter | http://jupyter.celine.localhost |
| oauth2-proxy | http://sso.celine.localhost |
| Keycloak Admin | http://keycloak.celine.localhost/admin |

## Adding a New Service

To add a new service behind the SSO boundary:

1. Add the service to `docker-compose.yaml`.
2. Add a Caddy virtual host in `config/caddy/Caddyfile` using `forward_auth` to oauth2-proxy.
3. Configure the service to read identity from the injected headers (`X-Auth-Request-User`, `X-Auth-Request-Access-Token`).
4. Implement authorization logic using the JWT claims (groups, scopes).

## Extending Group-to-Role Mappings

Edit `src/celine/superset/auth/groups.py` to modify Superset role mappings, then rebuild the Superset image.

For Jupyter, edit `config/jupyter/jupyter_server_config.py` to update `allowed_groups`.

## CI and Image Publishing

Docker images are built and published automatically via GitHub Actions when source or configuration files change. Image versions are controlled by `version.txt` (Superset) and `version.jupyter.txt` (Jupyter).
