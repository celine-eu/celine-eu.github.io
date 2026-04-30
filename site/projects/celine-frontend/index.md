# CELINE Frontend Monorepo

This monorepo contains the frontend applications and shared packages for the CELINE project.

## Structure

```
├── packages/
│   ├── ui/                      # @celine-eu/ui - Shared UI components
│   │   ├── src/
│   │   │   ├── theme.css        # Design tokens & CSS variables
│   │   │   ├── Icon.svelte      # Lucide-based icon component
│   │   │   ├── Button.svelte    # Button variants
│   │   │   ├── Skeleton.svelte  # Loading skeletons
│   │   │   ├── Panel.svelte     # Slide-over panel
│   │   │   ├── Modal.svelte     # Modal dialog
│   │   │   └── ThemeToggle.svelte
│   │   └── package.json
│   │
│   ├── roi-ui/                  # @celine-eu/roi-ui - ROI calculator UI components
│   │   └── package.json
│   │
│   └── assistant-ui/            # @celine-eu/assistant-ui - AI chat components
│       ├── src/
│       │   ├── ChatCore.svelte          # Main chat component
│       │   ├── AssistantWidget.svelte   # Floating chat button + modal
│       │   ├── AssistantProvider.svelte # Context provider
│       │   ├── AskAssistantButton.svelte# Contextual trigger button
│       │   ├── api.ts                   # Configurable API client
│       │   ├── types.ts
│       │   └── internal/                # Internal components
│       │       ├── MessageList.svelte
│       │       ├── Composer.svelte
│       │       ├── ChatHeader.svelte
│       │       ├── HistoryPanel.svelte
│       │       ├── AttachmentsPanel.svelte
│       │       ├── DropOverlay.svelte
│       │       └── Markdown.svelte
│       └── package.json
│
├── apps/
│   ├── assistant/               # Standalone AI Assistant app
│   │   ├── src/routes/
│   │   │   ├── +layout.svelte
│   │   │   └── +page.svelte     # Full-page chat
│   │   └── package.json
│   │
│   ├── grid/                    # Grid Resilience Dashboard
│   │   └── package.json
│   │
│   ├── roi/                     # PV ROI Calculator
│   │   └── package.json
│   │
│   └── webapp/                  # REC Participant Webapp
│       ├── src/
│       │   ├── lib/
│       │   │   ├── api.ts       # Webapp-specific API
│       │   │   ├── stores.ts
│       │   │   └── components/
│       │   │       ├── EnergyChart.svelte
│       │   │       └── StatCard.svelte
│       │   └── routes/
│       │       ├── +layout.svelte     # App shell with AssistantProvider
│       │       ├── +page.svelte       # Overview with AskAssistantButtons
│       │       ├── assistant/+page.svelte  # Embedded ChatCore
│       │       ├── notifications/
│       │       └── settings/
│       └── package.json
│
├── pnpm-workspace.yaml
└── package.json
```

## Documentation

| Document | Description |
|---|---|
| [Packages](https://celine-eu.github.io/projects/celine-frontend/docs/packages) | @celine-eu/ui components, @celine-eu/assistant-ui exports |
| [Apps](https://celine-eu.github.io/projects/celine-frontend/docs/apps) | assistant, webapp, grid, roi apps |
| [Theming](https://celine-eu.github.io/projects/celine-frontend/docs/theming) | CSS custom properties, design tokens, dark mode |
| [Development](https://celine-eu.github.io/projects/celine-frontend/docs/development) | pnpm workspace setup, adding icons, creating components, build pipeline |

## Setup

```bash
# Install pnpm if needed
npm install -g pnpm

# Install all dependencies
pnpm install

# Run individual apps
pnpm dev:assistant
pnpm dev:webapp
pnpm dev:grid
pnpm dev:roi

# Build all
pnpm build
```

## Package Usage

### @celine-eu/ui

Shared design system with theme variables and base components.

```svelte
<script>
  import { Icon, Button, Skeleton, Panel, Modal, ThemeToggle } from '@celine-eu/ui';
  import '@celine-eu/ui/theme.css';
</script>

<Button variant="primary" onclick={handleClick}>
  <Icon name="zap" size={16} />
  Click me
</Button>
```

### @celine-eu/assistant-ui

AI assistant chat interface that can be embedded anywhere.

```svelte
<script>
  import { 
    ChatCore,
    AssistantProvider,
    AssistantWidget,
    AskAssistantButton 
  } from '@celine-eu/assistant-ui';
</script>

<!-- Option 1: Full page chat -->
<ChatCore apiBaseUrl="/api" mode="full" />

<!-- Option 2: Floating widget with provider -->
<AssistantProvider apiBaseUrl="/api">
  <YourApp />
  <!-- Widget auto-included by provider -->
</AssistantProvider>

<!-- Option 3: Contextual trigger buttons -->
<AskAssistantButton 
  context={{ page: 'dashboard', section: 'stats' }}
  prompt="Explain these statistics"
/>
```

## Architecture

### ChatCore Modes

| Mode | Description |
|------|-------------|
| `full` | Full viewport, used in standalone app |
| `modal` | Centered modal dialog |
| `floating` | Floating window (for widget) |

### ChatCore Props

```typescript
interface ChatCoreProps {
  apiBaseUrl?: string;           // API base URL, default "/api"
  mode?: 'full' | 'modal' | 'floating';
  embedded?: boolean;            // Embedded in another app
  showHeader?: boolean;          // Show header bar
  enableHistory?: boolean;       // Enable history panel
  enableAttachments?: boolean;   // Enable attachments panel
  enableUpload?: boolean;        // Allow file uploads
  enableCitations?: boolean;     // Show source citations
  conversationId?: string;       // Load existing conversation
  initialContext?: AssistantContext;
  initialPrompt?: string;
  onConversationChange?: (id: string | null) => void;
  onError?: (error: Error) => void;
  onClose?: () => void;
}
```

### Assistant Context

When using `AskAssistantButton` or the widget, you can provide context:

```typescript
interface AssistantContext {
  page?: string;        // Current page identifier
  section?: string;     // Specific section/component
  data?: object;        // Structured data to include
  hint?: string;        // Natural language hint for the AI
}
```

## API Requirements

The assistant components expect these endpoints at `apiBaseUrl`:

```
POST /chat              - Chat stream (SSE)
POST /upload            - File upload
GET  /user              - Current user info
GET  /conversations     - List conversations
GET  /conversations/:id/messages - Get messages
DELETE /conversations/:id - Delete conversation
GET  /attachments       - List attachments
GET  /attachments/:id/raw - Get attachment file
DELETE /attachments/:id - Delete attachment
POST /admin/ingest      - Reindex (admin only)
POST /admin/reload      - Reload (admin only)
```

## Theme Customization

The theme uses CSS custom properties. Override in your app:

```css
:root {
  --celine-primary: #0d9488;
  --celine-primary-hover: #0f766e;
  /* ... see theme.css for full list */
}
```

## Development

### Adding a new icon

Edit `packages/ui/src/Icon.svelte` and add the path to the `icons` object.
Use [Lucide](https://lucide.dev/) icon paths.

### Creating a new component

1. Create in appropriate package (`ui` for generic, `assistant-ui` for chat-specific)
2. Export from `src/index.js`
3. Add TypeScript types if needed

## Backend Services

Each app connects to its corresponding backend service:

| App | Backend | Port |
|---|---|---|
| assistant | celine-ai-assistant | 8012 |
| webapp | celine-webapp (BFF) | 8014 |
| grid | celine-grid | 8015 |
| roi | celine-roi | 8013 |

