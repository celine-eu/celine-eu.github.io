# Messaging

`celine.sdk.broker`. Four repositories import it. An MQTT connection here is long-lived and
authenticated with a token that expires, so most of what follows is about surviving a
reconnection without losing a subscription or a shutdown.

---

## Lifecycle

### REQ-0070 — one task owns the client

A single connection loop creates, holds and closes the `aiomqtt.Client`. Everything else —
a token renewal, a listener error, a caller — posts a request and lets the loop act. No
second path touches the client, which is what keeps a reconnect from racing a publish.

### REQ-0071 — subscriptions survive reconnection

The subscription registry is the source of truth and is never cleared on reconnect. Every
tracked subscription is re-applied to each new connection before the broker is reported
ready. A consumer that reconnects silently loses nothing.

### REQ-0072 — a subscription registered before connecting is honoured

Subscribing while disconnected records the subscription and succeeds; it is applied when the
connection comes up. Callers do not have to sequence their startup around the broker.

### REQ-0073 — a subscription that the broker refuses is not left registered

If the live subscribe call fails, the registration is rolled back and the failure is
returned. A registry entry that was never accepted would be silently re-applied on the next
reconnect and reported as active.

### REQ-0074 — unsubscribing something unknown is false, not an error

### REQ-0075 — disconnecting stops every task and clears the registry

The connection loop, the listen task and the token watcher are all cancelled — cancellation
is requested synchronously, before any await, so a `disconnect()` that is itself cancelled
(Ctrl+C during shutdown) still stops them.

### REQ-0076 — a reconnect signal raised during a connect attempt is not lost

The request flag is cleared at the top of each attempt rather than after teardown, so a
signal posted while connecting is still pending when the loop reaches its wait.

### REQ-0077 — connecting has a timeout

`aiomqtt` has no default. Without one, a broker that accepts a TCP connection and never
completes the MQTT handshake hangs the service at startup instead of failing into the retry
loop. Timing out is a `ConnectionError` naming the host and port.

### REQ-0078 — connection attempts are retried, bounded only when asked

Failures retry after `reconnect_interval`. `max_reconnect_attempts` of `0` — the default —
means unlimited: a service should outlive its broker's restart.

### REQ-0079 — every client has an identifier

Configured, or auto-generated as `celine-<8 hex>`. Two instances of the same service must
not silently take over each other's session.

---

## Credentials

### REQ-0080 — a token provider authenticates by putting the token in the username

Username is the access token; password is the literal `jwt`. That is what the platform's
MQTT broker expects. Without a provider, the configured username and password are used
unchanged.

### REQ-0081 — a renewed token reconnects immediately with the new credentials

MQTT credentials are presented at connect time only, so a token renewal is acted on by
rebuilding the connection — without waiting out the reconnect interval, since nothing is
broken.

The renewal callback is ignored while shutting down or before the first successful connect:
the initial issuance must not trigger a reconnect of the connection it was fetched for.

### REQ-0082 — the token is refreshed ahead of expiry rather than on failure

The provider fires its renewal callback only from inside `get_token()`, so the broker runs
a watcher that sleeps until `expires_at - token_refresh_margin` and asks again. The margin
must be at least the provider's own validity leeway (both default to 30 seconds) or the
cached token is still considered valid and no renewal happens.

A failure to obtain a token is retried, not fatal.

### REQ-0083 — deliberate teardown never triggers a reconnect

The listen task requests a reconnect when it ends abnormally — that is how a dropped
connection is noticed. It must **not** request one when it is cancelled as part of a
reconnect already in progress or of a shutdown. A clean shutdown that starts reconnecting
to a broker nobody wants is the failure this distinction prevents.

---

## Messages

### REQ-0084 — topics are prefixed consistently

A configured `topic_prefix` is applied when publishing, when subscribing and when matching a
received topic against a subscription — with exactly one separator, whatever the slashes on
either side. A prefix applied in one place and not another delivers nothing and reports no
error.

### REQ-0085 — publishing while disconnected fails as a result, not an exception

Every publish returns a `PublishResult`. A broker outage is an expected condition on this
path and callers must be able to handle it without a try block. A payload that cannot be
serialised fails the same way.

### REQ-0086 — a published payload carries its own timestamp and correlation id

`created` is set from the message timestamp, or now, in UTC ISO-8601; a correlation id is
added when the message has one. Neither overwrites a key the caller already put in the
payload.

### REQ-0087 — MQTT wildcards decide which handlers see a message

`+` matches one segment and `#` matches the rest. A topic is delivered to every subscription
whose pattern matches it, and to none whose does not.

### REQ-0088 — a message that is not JSON is delivered, not dropped

An undecodable payload arrives as `{"_raw": <best-effort text>}` alongside the untouched
bytes. Discarding it would lose the only evidence of a misbehaving publisher.

### REQ-0089 — a handler that raises does not affect the others

The exception is logged and counted; the remaining handlers still receive the message and
the connection is unaffected.

### REQ-0090 — the broker reports its own counters

`get_stats()` gives connection state, publish, receive and error counts, and the active
subscriptions. It is the only view a service has of a connection that is otherwise silent
when healthy.
