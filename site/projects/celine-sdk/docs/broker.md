# Broker

The `celine.sdk.broker` module provides an MQTT client abstraction for CELINE services.

## Overview

The MQTT client wraps `aiomqtt` (or `paho-mqtt`) with:
- Automatic reconnection on connection loss
- JWT-based authentication (token refreshed before each reconnect)
- Structured subscription handling
- Connection statistics

## Usage

```python
from celine.sdk.broker import MqttBroker
from celine.sdk.settings import MqttSettings

settings = MqttSettings()
broker = MqttBroker(settings, token_provider=provider)

async with broker.connect() as client:
    # Publish
    await client.publish("celine/events/community/COMM1", payload=json_bytes)

    # Subscribe
    async with client.subscribe("celine/events/#") as messages:
        async for message in messages:
            print(message.topic, message.payload)
```

## Contracts

The `contracts.py` module defines the `BrokerProtocol` interface:

```python
class BrokerProtocol(Protocol):
    async def publish(self, topic: str, payload: bytes, qos: int = 1) -> None: ...
    async def subscribe(self, topic: str) -> AsyncContextManager: ...
```

## Authentication

The broker uses JWT tokens for MQTT authentication:
- Username is set to the OIDC client ID
- Password is set to the current access token
- On reconnect, a fresh token is fetched from the OIDC provider

## Models

```python
class MqttMessage:
    topic: str
    payload: bytes
    qos: int
    retain: bool
```

## Stats

The broker tracks connection statistics:

```python
stats = broker.stats()
# stats.connected: bool
# stats.reconnect_count: int
# stats.messages_sent: int
# stats.messages_received: int
```

## Configuration

| Variable | Description | Default |
|---|---|---|
| `MQTT_HOST` | Broker hostname | `localhost` |
| `MQTT_PORT` | Broker port | `1883` |
| `MQTT_TLS` | Enable TLS | `false` |
| `MQTT_CLIENT_ID` | MQTT client identifier | auto-generated |
