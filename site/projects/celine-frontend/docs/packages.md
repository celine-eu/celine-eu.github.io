# Packages

## @celine-eu/ui

Shared design system and base component library for CELINE frontends.

### Components

| Component | Description |
|---|---|
| `Button` | Button with variants (`primary`, `secondary`, `ghost`, `danger`) |
| `Icon` | Lucide-based SVG icon component |
| `Modal` | Centered modal dialog with slot content |
| `Panel` | Slide-over side panel |
| `Skeleton` | Loading skeleton placeholder |
| `ThemeToggle` | Dark/light theme switcher |
| `FeedbackWidget` | User feedback submission widget |

### Usage

```svelte
<script>
  import { Icon, Button, Skeleton, Panel, Modal, ThemeToggle, FeedbackWidget } from '@celine-eu/ui';
  import '@celine-eu/ui/theme.css';
</script>

<Button variant="primary" onclick={handleClick}>
  <Icon name="zap" size={16} />
  Click me
</Button>
```

Import `theme.css` once at the app root to load CSS custom properties.

---

## @celine-eu/assistant-ui

AI assistant chat interface. Provides a full chat experience that can be embedded in any SvelteKit app.

### Exports

| Export | Type | Description |
|---|---|---|
| `ChatCore` | Component | Main chat component with configurable modes |
| `AssistantProvider` | Component | Context provider — wraps the app and includes the floating widget |
| `AssistantWidget` | Component | Floating button that opens a chat modal |
| `AskAssistantButton` | Component | Context-aware trigger button for inline assistant access |
| `AttachmentsPanel` | Component | Attachments list panel (internal, re-exported) |
| `HistoryPanel` | Component | Conversation history panel (internal, re-exported) |
| `createAssistantApi` | Function | Factory for typed API client |
| `AssistantApi` | Type | API client interface |
| `AssistantContext` | Type | Context payload shape |

### ChatCore Modes

| Mode | Description |
|---|---|
| `full` | Full-viewport chat, used in standalone apps |
| `modal` | Centered modal dialog |
| `floating` | Floating window, used by the widget |

### ChatCore Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `apiBaseUrl` | `string` | `/api` | API base URL |
| `mode` | `full / modal / floating` | `full` | Display mode |
| `embedded` | `boolean` | `false` | Embedded in another app |
| `showHeader` | `boolean` | `true` | Show header bar |
| `enableHistory` | `boolean` | `true` | Enable history panel |
| `enableAttachments` | `boolean` | `true` | Enable attachments panel |
| `enableUpload` | `boolean` | `true` | Allow file uploads |
| `enableCitations` | `boolean` | `true` | Show source citations |
| `conversationId` | `string` | none | Load an existing conversation |
| `initialContext` | `AssistantContext` | none | Pre-load assistant context |
| `initialPrompt` | `string` | none | Pre-fill the composer |

### AssistantContext Shape

```typescript
interface AssistantContext {
  page?: string;    // Current page identifier
  section?: string; // Section within the page
  data?: object;    // Structured data for the AI
  hint?: string;    // Natural language hint
}
```

---

## @celine-eu/roi-ui

ROI calculator components for the PV installation ROI app.

### Exports

| Export | Type | Description |
|---|---|---|
| `RoiCore` | Component | Main ROI calculator with input form, map picker, and results display |
| `RoiWidget` | Component | Embeddable ROI calculator widget |
| `createRoiApi` | Function | Factory for typed API client |

### Usage

```svelte
<script>
  import { RoiCore } from '@celine-eu/roi-ui';
</script>

<RoiCore apiBaseUrl="/api/v1" />
```

Consumed by `apps/roi`. Supports PDF export of results and smartphone-friendly map selection.
