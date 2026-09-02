# Configuration

`celine.sdk.settings`. Ten repositories construct these classes, usually at import time, so
a change to a default changes ten services at once with no file in them changing.

---

### REQ-0001 — every setting is read from the environment under a `CELINE_` prefix

`OidcSettings` reads `CELINE_OIDC_*`, `MqttSettings` reads `CELINE_MQTT_*`, and
`PoliciesSettings` reads `CELINE_POLICIES_*`. The prefix is part of the contract: it is what
keeps a platform variable from colliding with a service's own.

`SdkSettings` composes the three, and each is built from the environment when the composite
is built — so `SdkSettings().oidc.client_id` and `OidcSettings().client_id` are the same
value.

All four classes are exported by `celine.sdk.settings`. (`PoliciesSettings` was reachable
only as `celine.sdk.settings.models.PoliciesSettings` until 2026-08-15; that path still
works.)

### REQ-0002 — an unknown variable in the namespace is ignored rather than rejected

Every settings class is `extra="ignore"`. A service that sets `CELINE_OIDC_SOMETHING_ELSE`
for its own purposes, or that runs beside a newer SDK, still starts.

### REQ-0003 — the SDK is usable with nothing configured

Every field has a default, and the defaults describe the local development platform
(`keycloak.celine.localhost` for the issuer and its JWKS URI, `host.docker.internal:1883`
for MQTT, `./policies` for the Rego bundle).

**These defaults are permissive, not safe.** They point at a development environment and no
audience is required (REQ-0026). A deployment that sets nothing is not protected by these
values; it is merely pointed somewhere harmless.

### REQ-0004 — the OIDC settings carry both what is needed to obtain a token and what is needed to verify one

`base_url`, `client_id`, `client_secret`, `scope`, `timeout` and `verify_ssl` serve
acquisition; `jwks_uri`, `audience`, `allowed_audiences` and
`include_client_id_as_audience` serve verification. One class, because a service is usually
both a caller and a callee.

### REQ-0005 — `load_settings()` with no path returns exactly the environment-derived settings

The YAML overlay is opt-in. Nothing reads a file unless asked to.

### REQ-0006 — a config path that does not exist is not an error

`load_settings("/missing.yaml")` returns the environment-derived settings. A service may
ship a default path and still run where the operator has provided no file.

### REQ-0007 — a YAML overlay overrides the environment key by key, and leaves the rest alone

An overlay that sets `oidc.audience` changes the audience and nothing else: the client id
that came from `CELINE_OIDC_CLIENT_ID` survives. The overlay is a layer over the
environment, not a replacement of the section it touches.

### REQ-0008 — a YAML document that is not a mapping is refused

`ValueError`, naming the type found. An empty file is a mapping of nothing and is accepted.

### REQ-0009 — YAML values interpolate `${VAR}` and `${VAR:-default}`

An unset **or empty** variable takes the default. With no default it becomes the empty
string, never the literal `${VAR}`: a value that failed to resolve must not reach a URL or a
credential looking like configuration.

### REQ-0010 — interpolation applies at every depth

Strings inside lists and nested mappings are resolved, not only the top level.

### REQ-0011 — interpolation terminates

Resolution repeats until the value stops changing, bounded at five passes. A variable whose
value is itself a placeholder resolves; one that refers to itself terminates rather than
looping.

### REQ-0012 — the policy settings locate the bundle and size its cache

`policies_dir` (a `Path`, defaulting to `./policies`), an optional `policies_data_dir`, and
the decision-cache knobs `policies_cache_enabled`, `policies_cache_ttl`,
`policies_cache_maxsize`. They configure the engine in [Policy evaluation](policy-evaluation.md);
nothing here reaches a policy service over the network.
