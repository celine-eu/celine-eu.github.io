# Policy evaluation

`celine.sdk.policies`. Seven repositories import it. Rego is evaluated **in process** via
regorus — there is no OPA server in the request path, so a policy decision costs no network
hop and no service can be "up but unauthorised" because OPA is down.

Each service ships its own `*.rego` bundle. This module loads and evaluates it; it never
supplies policy of its own.

---

## The bundle

### REQ-0050 — the bundle is read once, frozen, and evaluated many times

`load()` reads the policies and data into an immutable bundle at startup. Evaluating before
`load()` is a `PolicyEngineError`, not a silent deny: a service whose policies never loaded
is misconfigured, and answering "denied" would hide that.

### REQ-0051 — every `.rego` under the directory is loaded, except the tests

The search is recursive. Files ending `_test.rego` are Rego's own unit tests and are
excluded — loading them would put test rules in the production decision path.

### REQ-0052 — a missing policy directory is a startup failure

`PolicyEngineError` naming the path. The alternative — an engine that loads nothing and
denies everything — is indistinguishable at runtime from a correctly restrictive policy.

### REQ-0053 — the loaded packages are inspectable without evaluating anything

`has_package`, `get_packages` and `policy_count` report what the bundle contains, read from
each file's `package` declaration. A service uses this to fail fast when the policy it
intends to query is not in the image.

### REQ-0054 — policy data is optional

A data directory may supply JSON documents, loaded recursively alongside the policies. No
directory, or a configured directory that does not exist, means no data — not an error.

---

## Deciding

### REQ-0055 — each thread evaluates on its own engine, built from the shared frozen bundle

The bundle is immutable and shared; the engine is per-thread and never mutated across
threads. This is what makes the engine safe inside a threaded server without a lock on the
request path.

### REQ-0056 — the input document has one fixed shape

`subject`, `resource`, `action`, `environment`. Enum values are serialised as their string
values, so a policy matches `"user"` and not `"SubjectType.USER"`. An anonymous request is
`subject: null` rather than a missing key, so a policy can test for it.

`Subject.anonymous()` builds the anonymous principal; it is a subject of type `anonymous`
with the id `anonymous`, never `None` pretending to be a user.

### REQ-0057 — a decision is an allow, a reason and optional filters, and an undefined rule denies

`data.<package>.allow` decides. A rule that is undefined for this input, or a result of any
non-boolean shape, yields **`allowed=False`** with an empty reason: the default is deny at
every failure mode inside the bundle, including a malformed result.

`data.<package>.reason` is carried through when it is a string, for logs and for the
message a user sees.

**Querying a package the bundle does not contain is not a reliable deny.** Where some
loaded package shares its path, the rule is merely undefined and the decision is a denial;
where nothing shares it, the query is an error and the exception reaches the caller. Neither
is a contract worth depending on: a service querying a package it never shipped is
misconfigured rather than unauthorised, which is what REQ-0053 exists to catch — at startup,
not per request.

### REQ-0058 — filters are optional and never fail a decision

`data.<package>.filters` supplies row-level predicates for data queries. A bundle that
defines none, or whose filters are unusable, produces an empty list — the allow decision
stands on its own.

---

## The decision cache

### REQ-0059 — decisions are cached on the semantic content of the request

The key is a hash of subject, resource and action, scoped by policy package. Two identical
requests hit; a request differing in any of them misses.

### REQ-0060 — volatile environment fields are excluded from the key

`timestamp`, `request_id` and `trace_id` change on every request and change no decision.
Including them would give a cache with a hit rate of zero, which is worse than no cache
because it also costs memory.

### REQ-0061 — a cached decision says that it is cached

The returned decision carries `cached=True` while the stored one is left untouched, so the
next reader is not told the decision came from a cache of a cache. A freshly evaluated
decision reports `cached=False`.

### REQ-0062 — the cache can be bypassed for one call or disabled entirely

`skip_cache=True` evaluates and — deliberately — does not populate the cache either. A
disabled cache passes every call through. Both leave the wrapped engine's behaviour
identical.

### REQ-0063 — entries can be invalidated by policy or wholesale, and the count is reported

`invalidate(policy)` drops that policy's entries; `invalidate()` drops everything. The
number removed is returned so the caller can log it.

### REQ-0064 — the cache reports hits, misses and its own size

`stats` gives `size`, `maxsize`, `hits`, `misses` and a rounded `hit_rate`. A cache nobody
can measure is a cache nobody can size.

### REQ-0065 — the cached engine is a drop-in for the engine

`is_loaded`, `policy_count`, `load`, `has_package`, `get_packages` and `evaluate` are
delegated unchanged, so a service can wrap or unwrap the cache without touching call sites.
`evaluate()` — the raw query path — is never cached, because its query string is arbitrary.
