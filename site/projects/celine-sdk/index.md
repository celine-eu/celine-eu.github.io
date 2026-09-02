# CELINE SDK 

Shared SDK for the CELINE platform. Provides OIDC authentication, MQTT broker abstraction, Pydantic settings, and OpenAPI spec management with generated typed clients.

## Modules

| Module | Description |
|---|---|
| `celine.sdk.auth` | OIDC token provider, JWKS-based JWT parsing, token refresh |
| `celine.sdk.broker` | MQTT client with auto-reconnect and JWT authentication |
| `celine.sdk.settings` | Shared Pydantic settings: OIDC, MQTT, policies |
| `celine.sdk.openapi.*` | Generated typed clients for CELINE services |
| `celine.sdk.dt` | Digital Twin domain client helpers |
| `celine.sdk.nudging` | Nudging service client |
| `celine.sdk.policies` | OPA policy evaluation over a service's own `*.rego` bundle |
| `celine.sdk.rec_registry` | REC registry client helpers |
| `celine.sdk.flexibility` | Flexibility service client helpers |
| `celine.sdk.ai_assistant` | AI assistant client helpers |

`celine.sdk.clients`, `celine.sdk.utils` and `celine.sdk.cli` are internal: they support
the modules above and the spec-management CLI, and are not part of the public surface.

## Installation

```bash
pip install celine-sdk
```

Client generation needs the code generators from this repository's `dev` dependency group
(Python ≥ 3.11) — `uv sync` in a checkout. It is a maintainer task performed here, not
something a consuming service does.

## CLI Quick Reference

```bash
# Fetch and version OpenAPI specs (writes to ./openapi/)
celine-sdk spec fetch services.yaml

# List discovered spec versions
celine-sdk spec list

# Generate typed Python clients (needs the dev dependency group)
celine-sdk generate services.yaml

# Both steps, in a checkout
task gen
```

## services.yaml Format

```yaml
services:
  digital-twin:
    package: dt
    openapi: http://dt:8000/openapi.json
  policies:
    openapi: http://policies:8000/openapi.json
```

## Documentation

| Document | Description |
|---|---|
| [Auth](https://celine-eu.github.io/projects/celine-sdk/docs/auth) | OIDC token provider, JWT parsing, AccessToken model |
| [Broker](https://celine-eu.github.io/projects/celine-sdk/docs/broker) | MQTT client, auto-reconnect, JWT auth, subscription handling |
| [Settings](https://celine-eu.github.io/projects/celine-sdk/docs/settings) | OidcSettings, MqttSettings, PoliciesSettings, env var config |
| [Spec Management](https://celine-eu.github.io/projects/celine-sdk/docs/spec-management) | services.yaml format, spec fetch, versioning, client generation |
| [Specifications](docs/specifications/index.md) | What the SDK must do, as numbered requirements each named by a test |

## License

Apache 2.0 — Copyright © 2025 Spindox Labs
