# celine-sdk

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

## Installation

```bash
# Core SDK
pip install celine-sdk

# With client generation support
pip install 'celine-sdk[gen]'
```

## CLI Quick Reference

```bash
# Fetch and version OpenAPI specs (writes to ./openapi/)
celine-sdk spec fetch services.yaml

# List discovered spec versions
celine-sdk spec list

# Generate typed Python clients (requires [gen] extra)
celine-sdk generate services.yaml
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
| [Auth](https://celine-eu.github.io/projects/celine-sdk/docs/auth.md) | OIDC token provider, JWT parsing, AccessToken model |
| [Broker](https://celine-eu.github.io/projects/celine-sdk/docs/broker.md) | MQTT client, auto-reconnect, JWT auth, subscription handling |
| [Settings](https://celine-eu.github.io/projects/celine-sdk/docs/settings.md) | OidcSettings, MqttSettings, PoliciesSettings, env var config |
| [Spec Management](https://celine-eu.github.io/projects/celine-sdk/docs/spec-management.md) | services.yaml format, spec fetch, versioning, client generation |

## License

Apache 2.0 — Copyright © 2025 Spindox Labs
