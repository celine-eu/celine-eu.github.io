# Development

## Prerequisites

- Node.js ≥ 20
- pnpm ≥ 8

```bash
npm install -g pnpm
```

## Setup

```bash
# Install all workspace dependencies
pnpm install

# Run the standalone assistant app
pnpm dev:assistant
# http://localhost:5174

# Run the webapp
pnpm dev:webapp
# http://localhost:5173

# Build all packages and apps
pnpm build
```

## Workspace Structure

```
packages/
  ui/               @celine-eu/ui
  assistant-ui/     @celine-eu/assistant-ui
apps/
  assistant/        Standalone assistant app
  webapp/           REC participant webapp
pnpm-workspace.yaml
```

## Adding an Icon

Icons are defined in `packages/ui/src/Icon.svelte`. Add a new icon by inserting its SVG path into the `icons` object:

```javascript
const icons = {
  // existing icons...
  "my-icon": "M10 10 L20 20...",  // SVG path data
};
```

Use [Lucide](https://lucide.dev/) icon paths for consistency.

## Creating a New Component

1. Choose the correct package: `ui` for generic UI components, `assistant-ui` for chat-specific components.
2. Create the `.svelte` file in `packages/<package>/src/`.
3. Export it from `packages/<package>/src/index.js`:
   ```javascript
   export { default as MyComponent } from './MyComponent.svelte';
   ```
4. Add TypeScript types to the exports in `index.d.ts` if needed.

## Build Pipeline

Each package builds via `vite build` (library mode). Apps build via `vite build` (SPA/SSR mode).

```bash
# Build only packages
pnpm --filter @celine-eu/ui build
pnpm --filter @celine-eu/assistant-ui build

# Build only apps
pnpm --filter webapp build
pnpm --filter assistant build
```

## API Requirements

The assistant components expect the celine-ai-assistant API to be available at `apiBaseUrl`. The webapp BFF proxies `/api/assistant/*` to the assistant service.

For local development of the assistant app standalone, start `celine-ai-assistant` locally and set `apiBaseUrl` to `http://localhost:8000`.
