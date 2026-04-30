# Development

## Prerequisites

- Node.js >= 20
- pnpm >= 8
- `task` (go-task)

```bash
npm install -g pnpm
```

## Setup

```bash
# Install all workspace dependencies
task setup
# or: pnpm install
```

## Dev Servers

```bash
task dev:assistant    # http://localhost:3003
task dev:roi          # http://localhost:3004
task dev:webapp       # http://localhost:3005
task dev:grid         # http://localhost:3006
```

## Workspace Structure

```
packages/
  ui/               @celine-eu/ui          — shared design system
  assistant-ui/     @celine-eu/assistant-ui — AI chat components
  roi-ui/           @celine-eu/roi-ui      — ROI calculator components
apps/
  assistant/        Standalone AI assistant     (v0.15.0)
  roi/              PV ROI calculator           (v0.14.0)
  webapp/           REC participant webapp      (v0.17.0)
  grid/             Grid resilience dashboard   (v0.12.0)
pnpm-workspace.yaml
taskfile.yaml
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

1. Choose the correct package: `ui` for generic UI, `assistant-ui` for chat, `roi-ui` for ROI calculator.
2. Create the `.svelte` file in `packages/<package>/src/`.
3. Export it from `packages/<package>/src/index.ts`:
   ```typescript
   export { default as MyComponent } from './MyComponent.svelte';
   ```

## Build

```bash
# Build all
task build

# Build individual apps
task build:webapp
task build:assistant
task build:roi
task build:grid
```

## Docker

```bash
task docker:webapp      # Build webapp image
task docker:assistant   # Build assistant image
task docker:grid        # Build grid image
task docker:all         # Build all images
```

## Release

Each app is independently versioned via `release-it` with conventional commits. Tags follow `<app>-v<version>`.

```bash
task release:<app>          # bump, changelog, tag, push
task release:<app>:dry      # preview (assistant, webapp, grid)
task release                # release all apps
```

## API Requirements

Each app connects to its backend service:

| App | Backend | API Port |
|---|---|---|
| assistant | celine-ai-assistant | 8012 |
| webapp | celine-webapp (BFF) | 8014 |
| roi | celine-roi | 8013 |
| grid | celine-grid | 8015 |
