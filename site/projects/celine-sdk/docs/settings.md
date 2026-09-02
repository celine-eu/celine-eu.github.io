# Settings

`celine.sdk.settings` provides typed, environment-driven configuration using
`pydantic-settings`. What it must do is stated in
[specifications/configuration.md](specifications/configuration.md).

**Every variable is prefixed `CELINE_`.** The prefix is per section:
`CELINE_OIDC_*`, `CELINE_MQTT_*`, `CELINE_POLICIES_*`. Unknown variables inside a namespace
are ignored rather than rejected.

## OidcSettings — `CELINE_OIDC_*`

```python
from celine.sdk.settings import OidcSettings

settings = OidcSettings()
```

| Variable | Type | Default | Description |
|---|---|---|---|
| `CELINE_OIDC_BASE_URL` | `str` | `http://keycloak.celine.localhost/realms/celine` | Issuer URL; also the expected `iss` |
| `CELINE_OIDC_JWKS_URI` | `str` | `…/protocol/openid-connect/certs` | Key set used to verify signatures |
| `CELINE_OIDC_CLIENT_ID` | `str \| None` | `None` | Client id |
| `CELINE_OIDC_CLIENT_SECRET` | `str \| None` | `None` | Client secret |
| `CELINE_OIDC_AUDIENCE` | `str \| None` | `None` | Expected `aud`. **Unset means audience is not checked** |
| `CELINE_OIDC_ALLOWED_AUDIENCES` | `str \| None` | `None` | Extra accepted audiences, comma-separated. Not used by `JwtUser.from_token` |
| `CELINE_OIDC_INCLUDE_CLIENT_ID_AS_AUDIENCE` | `bool` | `true` | Fold the client id in. Not used by `JwtUser.from_token` |
| `CELINE_OIDC_SCOPE` | `str \| None` | `None` | Scope requested when obtaining a token |
| `CELINE_OIDC_TIMEOUT` | `float` | `10.0` | HTTP timeout for token and discovery calls |
| `CELINE_OIDC_VERIFY_SSL` | `bool` | `true` | Verify TLS certificates |

## MqttSettings — `CELINE_MQTT_*`

```python
from celine.sdk.settings import MqttSettings

settings = MqttSettings()
```

| Variable | Type | Default |
|---|---|---|
| `CELINE_MQTT_HOST` | `str` | `host.docker.internal` |
| `CELINE_MQTT_PORT` | `int` | `1883` |
| `CELINE_MQTT_CLIENT_ID` | `str \| None` | `None` (auto-generated) |
| `CELINE_MQTT_TOPIC_PREFIX` | `str` | `""` |
| `CELINE_MQTT_USERNAME` / `CELINE_MQTT_PASSWORD` | `str \| None` | `None` |
| `CELINE_MQTT_USE_TLS` | `bool` | `false` |
| `CELINE_MQTT_CA_CERTS` / `CERTFILE` / `KEYFILE` | `str \| None` | `None` |
| `CELINE_MQTT_KEEPALIVE` | `int` | `60` |
| `CELINE_MQTT_CLEAN_SESSION` | `bool` | `true` |
| `CELINE_MQTT_RECONNECT_INTERVAL` | `float` | `0.0` |
| `CELINE_MQTT_MAX_RECONNECT_ATTEMPTS` | `int` | `10` |
| `CELINE_MQTT_TOKEN_REFRESH_MARGIN` | `float` | `30.0` |

`MqttSettings` configures the deployment; `MqttBroker` takes an `MqttConfig` — see
[broker.md](broker.md), whose defaults differ (`localhost`, unlimited reconnects).

## PoliciesSettings — `CELINE_POLICIES_*`

Policies are evaluated **in process** from the service's own Rego bundle. There is no policy
service to point at.

```python
from celine.sdk.settings import PoliciesSettings
```

| Variable | Type | Default | Description |
|---|---|---|---|
| `CELINE_POLICIES_POLICIES_DIR` | `Path` | `./policies` | Directory of `.rego` files |
| `CELINE_POLICIES_POLICIES_DATA_DIR` | `Path \| None` | `None` | Optional directory of policy data JSON |
| `CELINE_POLICIES_POLICIES_CACHE_ENABLED` | `bool` | `true` | Decision caching |
| `CELINE_POLICIES_POLICIES_CACHE_TTL` | `int` | `300` | Cache TTL, seconds |
| `CELINE_POLICIES_POLICIES_CACHE_MAXSIZE` | `int` | `10000` | Maximum entries |

## SdkSettings

Composes all three; each section is still read from its own prefix.

```python
from celine.sdk.settings import SdkSettings

settings = SdkSettings()
settings.oidc.client_id
settings.mqtt.host
settings.policies.policies_dir
```

## The optional YAML overlay

```python
from celine.sdk.settings import load_settings

settings = load_settings("config.yaml")   # or load_settings() for environment only
```

- A path that does not exist is not an error — the environment-derived settings are returned.
- YAML values override the environment key by key; keys the file does not mention keep their
  environment values.
- Values interpolate `${VAR}` and `${VAR:-default}`. An unset *or empty* variable takes the
  default; with no default the result is an empty string, never the literal `${VAR}`.

```yaml
# config.yaml
oidc:
  audience: ${SERVICE_AUDIENCE:-svc-digital-twin}
mqtt:
  host: ${MQTT_HOST:-mqtt.celine.local}
```

## The defaults are for development, not for production

They point at `*.celine.localhost` and require no audience. A deployment that sets nothing is
not protected by them.
