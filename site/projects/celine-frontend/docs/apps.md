# Apps

## apps/assistant

Standalone full-page AI assistant application. Provides a single-route SvelteKit app that renders `ChatCore` in full-viewport mode.

**Entry point:** `apps/assistant/src/routes/+page.svelte`

```svelte
<ChatCore apiBaseUrl="/api" mode="full" />
```

This app is deployed as part of the celine-ai-assistant service, served at the root path. The layout provides no navigation or chrome — just the chat interface.

**Docker image:** `ghcr.io/celine-eu/assistant-ui`

**Dev:**
```bash
pnpm dev:assistant
# http://localhost:5174
```

---

## apps/webapp

REC participant webapp. A full SvelteKit application for community members, including an energy overview, notifications, settings, and the embedded assistant.

**Routes:**

| Route | Description |
|---|---|
| `/` | Energy overview — production, consumption, incentives |
| `/assistant` | Embedded `ChatCore` in full mode |
| `/notifications` | Notification list and read/delete |
| `/settings` | Notification preferences and push subscription |

**Layout:** `apps/webapp/src/routes/+layout.svelte`

The root layout wraps the app in `AssistantProvider`, which injects the floating assistant widget. It also calls `GET /api/me` to check terms acceptance before rendering child routes.

**BFF proxy pattern:**

The webapp proxies assistant requests through its FastAPI BFF:

```python
# webapp BFF
@router.api_route("/assistant/{path:path}", methods=["GET", "POST", "DELETE"])
async def proxy_assistant(path: str, request: Request):
    return await proxy_to(f"{ASSISTANT_URL}/api/{path}", request)
```

This keeps the assistant's API behind the same origin as the webapp, forwarding the user's identity automatically.

**Dev:**
```bash
pnpm dev:webapp
# http://localhost:5173
```
