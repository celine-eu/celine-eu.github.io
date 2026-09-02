# Specifications

What this SDK must do, stated so that a test can name it.

These requirements were **extracted from the implementation** on 2026-08-15, not written
ahead of it. That direction matters when reading them: each one says what the code already
does and what consumers therefore depend on. Where the extraction found the published
documentation disagreeing with the code, the code won and `docs/` was corrected — the
disagreements are listed at the end of this file.

Twelve repositories import `celine.sdk.auth` and ten import `celine.sdk.settings`
(the companion's knowledge). A requirement here is therefore
a promise to those repositories, and changing one is a platform change, not a local one.

| Document | Covers |
|---|---|
| [Configuration](configuration.md) | `celine.sdk.settings` — environment, YAML overlay, interpolation |
| [Identity](identity.md) | `celine.sdk.auth` — token verification, claims, token providers |
| [Policy evaluation](policy-evaluation.md) | `celine.sdk.policies` — bundle loading, decisions, decision cache |
| [Messaging](messaging.md) | `celine.sdk.broker` — MQTT lifecycle, topics, dispatch |
| [REC registry client](rec-registry-client.md) | `celine.sdk.rec_registry` — the batch asset lookups |
| [Spec management](spec-management.md) | the CLI, spec versioning, generated-client conversion |

## Identifiers

`REQ-` followed by four digits, the harness default. A test declares what it covers with
`@verifies REQ-####` in its docstring, and the mapping between the two is generated —
never written by hand. the companion's testing playbook states how.

Numbers are allocated in blocks per document so a new requirement can be appended without
renumbering: configuration `0001–0019`, identity `0020–0049`, policy evaluation
`0050–0069`, messaging `0070–0099`, spec management `0100–0119`, REC registry client
`0120–0139`.

## What is deliberately not specified here

- **The generated tree.** `src/celine/sdk/openapi` is 454 files produced by `task gen`;
  requiring anything of it would be requiring something of its generator. What *is*
  specified is the conversion boundary around it (REQ-0110, REQ-0111) and the versioning
  that feeds it.
- **The service APIs themselves.** Those belong to the services. This SDK requires only
  that a spec is fetched, versioned and turned into a client.
- **Compatibility with the repositories that import this one.** Nothing in this repository
  can answer it.

## Where the documentation disagreed with the code

Found while extracting, and corrected in `docs/` in the same change. Listed because a
consumer may have written code against the documented version:

| Documented | Actual |
|---|---|
| `OIDC_ISSUER`, `MQTT_HOST`, `POLICIES_URL` env vars | `CELINE_OIDC_BASE_URL`, `CELINE_MQTT_HOST`; no `POLICIES_URL` exists (REQ-0001) |
| `OidcTokenProvider(settings)` | `OidcClientCredentialsProvider(base_url=…, client_id=…, client_secret=…)` (REQ-0037) |
| `from celine.sdk.auth import StaticTokenProvider` | it was not exported there — the **export was added** rather than the document changed (REQ-0035) |
| `AccessToken` carrying `expires_in`, `scope`, a `datetime` expiry | `access_token`, `expires_at` (epoch float), `refresh_token`, `token_type` (REQ-0034) |
| MQTT username is the client id, password the token | username **is** the token, password the literal `jwt` (REQ-0080) |
| `BrokerProtocol`, `MqttMessage`, `broker.stats()` | `Broker`, `BrokerMessage`/`ReceivedMessage`, `get_stats()` (REQ-0090) |
| "existing spec versions are not overwritten" | a re-fetch of the same `info.version` overwrites it (REQ-0104) |

Three of these were fixed in the code rather than absorbed into the documentation, because
the documented behaviour was the right one: `StaticTokenProvider` and `PoliciesSettings` are
now exported where they were documented to be, and version ordering is numeric (REQ-0105).
