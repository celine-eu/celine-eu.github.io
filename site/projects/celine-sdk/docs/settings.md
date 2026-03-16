# Settings

The `celine.sdk.settings` module provides typed, environment-driven configuration using `pydantic-settings`.

## Settings Classes

### OidcSettings

```python
from celine.sdk.settings import OidcSettings

settings = OidcSettings()
```

| Variable | Type | Description |
|---|---|---|
| `OIDC_ISSUER` | `str` | OIDC issuer base URL (e.g., `http://keycloak:8080/realms/celine`) |
| `OIDC_CLIENT_ID` | `str` | Client ID for this service |
| `OIDC_CLIENT_SECRET` | `str` | Client secret |
| `OIDC_SCOPE` | `str` | Requested token scopes (space-separated) |

### MqttSettings

```python
from celine.sdk.settings import MqttSettings

settings = MqttSettings()
```

| Variable | Type | Default | Description |
|---|---|---|---|
| `MQTT_HOST` | `str` | `localhost` | Broker hostname |
| `MQTT_PORT` | `int` | `1883` | Broker port |
| `MQTT_TLS` | `bool` | `false` | Enable TLS |
| `MQTT_CLIENT_ID` | `str` | auto | MQTT client identifier |

### PoliciesSettings

```python
from celine.sdk.settings import PoliciesSettings

settings = PoliciesSettings()
```

| Variable | Type | Description |
|---|---|---|
| `POLICIES_URL` | `str` | Base URL of the celine-policies service |

### SdkSettings

Composite settings combining all of the above:

```python
from celine.sdk.settings import SdkSettings

settings = SdkSettings()
# settings.oidc: OidcSettings
# settings.mqtt: MqttSettings
# settings.policies: PoliciesSettings
```

## Environment Variable Naming

All variables follow the `SCREAMING_SNAKE_CASE` pattern. `pydantic-settings` loads them from the process environment and optionally from a `.env` file if present.

```bash
# Example .env
OIDC_ISSUER=http://keycloak:8080/realms/celine
OIDC_CLIENT_ID=my-service
OIDC_CLIENT_SECRET=secret
MQTT_HOST=mqtt.celine.local
POLICIES_URL=http://policies:8009
```
