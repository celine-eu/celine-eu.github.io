# Broker

`celine.sdk.broker` provides an MQTT client for CELINE services, built on `aiomqtt`. What it
must do is stated in [specifications/messaging.md](specifications/messaging.md).

It handles the parts that are easy to get wrong in a long-lived, token-authenticated
connection: reconnection, resubscription, refreshing credentials before they expire, and
shutting down without reconnecting on the way out.

## Usage

```python
from celine.sdk.broker import BrokerMessage, MqttBroker, MqttConfig, QoS

broker = MqttBroker(
    MqttConfig(host="mqtt.celine.local", port=1883, topic_prefix="celine"),
    token_provider=provider,          # optional; see auth.md
)

await broker.connect()                # returns once connected and subscribed

result = await broker.publish(
    BrokerMessage(topic="events/community/rec-1", payload={"kwh": 12.4})
)
if not result.success:
    ...                               # a broker outage is a result, not an exception

async def handle(message) -> None:
    print(message.topic, message.payload)

sub = await broker.subscribe(["events/#"], handle, qos=QoS.AT_LEAST_ONCE)
...
await broker.unsubscribe(sub.subscription_id)
await broker.disconnect()
```

`MqttBroker` is also an async context manager, and `create_mqtt_broker(**kwargs)` builds one
from keyword arguments.

Subscribing before `connect()` is fine: subscriptions are recorded and applied when the
connection comes up, and re-applied after every reconnect.

## MqttConfig

`MqttBroker` takes an `MqttConfig`, not `MqttSettings`. Build one from settings where you
want the deployment to drive it:

```python
from celine.sdk.settings import MqttSettings

s = MqttSettings()
config = MqttConfig(host=s.host, port=s.port, topic_prefix=s.topic_prefix)
```

| Field | Default | Notes |
|---|---|---|
| `host` / `port` | `localhost` / `1883` | |
| `client_id` | auto | `celine-<8 hex>` when unset |
| `username` / `password` | `None` | Ignored when a token provider is supplied |
| `use_tls`, `ca_certs`, `certfile`, `keyfile` | off | Standard TLS context when enabled |
| `keepalive` / `clean_session` | `60` / `true` | |
| `reconnect_interval` | `5.0` | Wait between attempts |
| `max_reconnect_attempts` | `0` | `0` is unlimited |
| `topic_prefix` | `""` | Applied to publish, subscribe **and** matching |
| `token_refresh_margin` | `30.0` | Must be ≥ the provider's `is_valid` leeway |
| `connect_timeout` | `10.0` | aiomqtt has no default |

## Authentication

With a `TokenProvider`, the broker authenticates by putting the **JWT in the username** and
the literal `jwt` in the password — this is what the platform's broker expects. Without one,
the configured username and password are used.

Credentials are presented only at connect time, so:

- a watcher asks the provider for a token before the current one expires, and
- a renewal rebuilds the connection immediately, skipping the reconnect interval.

## Messages

```python
@dataclass
class BrokerMessage:          # what you publish
    topic: str
    payload: dict
    qos: QoS = QoS.AT_LEAST_ONCE
    retain: bool = False
    headers: dict[str, str] = {}
    correlation_id: str | None = None
    timestamp: datetime | None = None

@dataclass
class ReceivedMessage:        # what a handler receives
    topic: str
    payload: dict
    raw_payload: bytes
    qos: QoS
    timestamp: datetime
```

A published payload gains `created` (UTC ISO-8601) and, when set, `correlation_id` — neither
overwrites a key already in the payload. Serialisation falls back to `str`, so a `datetime`
or a domain object is sent as its string form rather than failing.

A received payload that is not JSON arrives as `{"_raw": "<text>"}`, with the untouched bytes
in `raw_payload`. A handler that raises is logged and counted; the other handlers still run.

`publish_event(event)` publishes a Pydantic model, deriving the topic from `event.type` and
`event.payload.community_id` when no topic is given.

## Contracts

`contracts.py` defines the transport-independent surface: the `Broker` protocol and
`BrokerBase`, plus `BrokerMessage`, `ReceivedMessage`, `PublishResult`, `SubscribeResult`,
`QoS` and `MessageHandler`. `MqttBroker` is one implementation.

## Stats

```python
broker.get_stats()
# {"connected": bool, "publish_count": int, "receive_count": int,
#  "error_count": int, "subscription_count": int, "subscriptions": [...]}
```
