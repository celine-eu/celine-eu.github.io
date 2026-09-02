# Identity

`celine.sdk.auth`. Twelve repositories import it, and it is where every CELINE service
decides whether a token is genuine. A permissive change here is permissive everywhere.

---

## Verifying a token

### REQ-0020 — a token is verified, never merely decoded

`JwtUser.from_token` checks the signature against the issuer's published keys and enforces
`exp`, `nbf` and `iss`. There is no unverified decode path in the public surface: a caller
holding a token and settings either gets a verified `JwtUser` or an exception.

`RS256`, `HS256` and `ES256` are accepted unless the caller names a narrower set.

### REQ-0021 — signing keys come from the configured JWKS URI, over a client cached per URI

`OidcSettings.jwks_uri` is the source. The `PyJWKClient` is memoised per URI so a service
verifying thousands of requests fetches the key set once, and the key set is itself cached
for an hour.

**This memoisation is the single seam for testing.** A test replaces the JWKS *fetch* and
leaves every check above live; substituting a mocked validator instead proves only that the
mock was called.

### REQ-0022 — an expired token is rejected, with thirty seconds of leeway

The leeway exists for clock skew between a service and the identity provider. A token
expired by less than it is still accepted; one expired by more is not.

### REQ-0023 — a token signed by a key the issuer does not publish is rejected

Signature verification is the point of the exercise: a well-formed token carrying correct
claims and a foreign signature must not parse.

### REQ-0024 — a token from another issuer is rejected

`iss` must equal `OidcSettings.base_url`. A token that is genuine elsewhere is not genuine
here.

### REQ-0025 — an `Authorization` header value is accepted as well as a bare token

`Bearer <token>` is stripped, in any case. Services pass the header through unchanged often
enough that requiring them to split it produced the bug this absorbs.

### REQ-0026 — the audience is validated only when one is configured

With `OidcSettings.audience` set, `aud` must contain it. With it unset, **audience
validation is skipped entirely** — a permissive default, and the reason a service that never
declares an audience is not checking one.

`get_expected_audiences()` composes `audience` with `client_id` (when
`include_client_id_as_audience` is on) and returns `None` when there is nothing to check.
It is a helper **for callers that build their own validation**; `from_token` does not use
it, so `allowed_audiences` and `include_client_id_as_audience` have no effect on
`from_token`. Anything relying on them must apply them itself.

### REQ-0027 — a token without a subject is refused

`sub` identifies the principal; a verified token that names nobody is useless and is a
`ValueError` rather than a `JwtUser` with an empty id.

### REQ-0028 — a missing or empty token is refused before any network call

`None`, `""` or whitespace raises `ValueError` without touching the JWKS endpoint. An
unauthenticated request must not be able to cause an outbound fetch.

---

## Reading a verified token

### REQ-0029 — organization memberships are parsed from the `organization` claim

Each key becomes an `Organization` with that key as its `alias` — which is used directly as
the Digital Twin network id. `type` is a single-element list in Keycloak and is flattened to
a string; `attributes` are normalised so every value is a list, whatever the claim shape.

`organization_aliases`, `get_organization(alias)` and `is_member_of(alias)` read them. An
unparseable or absent claim yields no memberships rather than an error.

### REQ-0030 — groups are read from both the realm level and the organization level

`extract_groups` merges the top-level `groups` claim with every
`organization.<alias>.groups` into one deduplicated list, leading slashes stripped,
first-seen order preserved. Non-list claims and non-string entries are skipped rather than
raising.

**Merging is correct only for a single-tenant service.** For a service acting for several
communities, flattening lets a badge held in one community satisfy a check about another;
such a service must read the two levels apart and not call this function.

### REQ-0031 — a service account is distinguished from a user

`is_service_account` treats a `preferred_username` beginning `service-account-` as
authoritative (Keycloak's client-credentials convention) and `gty=client-credentials` as an
equivalent signal from other providers. An email, any group, or any other
`preferred_username` marks a human. Failing all of those, a token carrying a client id and
no email is a service.

The platform authorises services by scope and users by group membership; this is the
function that decides which of the two a caller is.

### REQ-0032 — claims are reachable by name, role and scope

`get_claim`, `has_role` (a list or a bare string), `has_scope` (a space-separated string or
a list), `display_name` (name, then username, then email, then `user-<sub>`), `get_username`
(username, else `user-<sub>`) and `to_dict`. Each tolerates the claim being absent or of the
wrong shape, because the claim set is the identity provider's to change.

### REQ-0033 — a parsed token can report its own expiry

`is_expired(leeway)` and `is_valid(leeway)` read `exp`. A token with no `exp` is treated as
not expired — the verification step has already refused an expired one, so these serve
callers holding a token they intend to reuse.

---

## Obtaining a token

### REQ-0034 — an access token carries its expiry and answers whether it is still usable

`AccessToken(access_token, expires_at, refresh_token=None, token_type="Bearer")`.

**There is one such class, whatever path it is imported by.** `celine.sdk.auth.AccessToken`,
`celine.sdk.auth.models.AccessToken` and `celine.sdk.auth.jwt.AccessToken` are the same
object; `celine.sdk.auth.jwt` carried a second, byte-identical definition until 2026-08-15,
which made an `isinstance` check across the two paths fail for reasons that read as
impossible.

`expires_at` is an epoch float. `is_valid(leeway=30)` is false once the token is within the
leeway of expiring — early, deliberately, so a token is replaced before it is refused.
`to_header()` renders `"<token_type> <access_token>"`.

### REQ-0035 — a forwarded token is used as-is

`StaticTokenProvider` wraps a token a caller already holds — the case for every service that
forwards its user's JWT downstream. A `Bearer ` prefix is stripped; nothing is refreshed and
nothing is verified, because whoever accepted the request already verified it.

It is exported by `celine.sdk.auth`, beside the provider it is an alternative to. (It was
reachable only as `celine.sdk.auth.static.StaticTokenProvider` until 2026-08-15; that path
still works.)

### REQ-0036 — a provider notifies its listeners when a new token is issued

`add_token_renewed_listener` registers an async callback, fired after each issuance. This is
what lets a long-lived MQTT connection rebuild itself on fresh credentials (REQ-0080).

**A failing listener does not fail the issuance**, and does not stop the remaining
listeners: the exception is logged and the loop continues. A token was still obtained, and
dropping it because a subscriber misbehaved would be worse.

### REQ-0037 — the client-credentials provider reuses a token until it is close to expiring

`OidcClientCredentialsProvider.get_token()` returns the cached token while `is_valid()`
holds, so the common path makes no network call.

### REQ-0038 — a refresh is attempted before re-authenticating, and its failure is not fatal

Holding a refresh token, the provider tries the refresh grant; if that fails for any reason
it falls back to a full client-credentials authentication. Either way the renewal listeners
are fired with the new token.

### REQ-0039 — endpoints are discovered from the issuer, once

`OidcDiscoveryClient` reads `<issuer>/.well-known/openid-configuration` and caches the
`issuer`, `token_endpoint` and `jwks_uri` it finds for the life of the client. A trailing
slash on the configured issuer is not a second URL.

`expires_in` from the token response fixes `expires_at`; a response omitting it is treated
as five minutes.
