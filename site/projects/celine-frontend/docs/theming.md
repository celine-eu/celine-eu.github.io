# Theming

## CSS Custom Properties

The `@celine-eu/ui` package ships a `theme.css` file that defines all design tokens as CSS custom properties. Import it once at the root of your app:

```svelte
<!-- app +layout.svelte -->
<script>
  import '@celine-eu/ui/theme.css';
</script>
```

## Design Tokens

Key tokens defined in `packages/ui/src/theme.css`:

| Token | Default | Description |
|---|---|---|
| `--celine-primary` | `#0d9488` | Primary brand color (teal) |
| `--celine-primary-hover` | `#0f766e` | Primary hover state |
| `--celine-bg` | `#ffffff` | Background color |
| `--celine-bg-secondary` | `#f8fafc` | Secondary background |
| `--celine-text` | `#0f172a` | Primary text |
| `--celine-text-secondary` | `#64748b` | Secondary text |
| `--celine-border` | `#e2e8f0` | Border color |
| `--celine-shadow` | `0 1px 3px ...` | Box shadow |
| `--celine-radius` | `0.5rem` | Border radius |
| `--celine-font` | `system-ui, sans-serif` | Font family |

## Overriding Tokens

Override any token in your app's global CSS:

```css
/* app/src/app.css */
:root {
  --celine-primary: #2563eb;        /* Blue instead of teal */
  --celine-primary-hover: #1d4ed8;
  --celine-radius: 0.25rem;         /* Tighter radius */
}
```

Or scope overrides to a specific component:

```css
.my-section {
  --celine-primary: #7c3aed;
}
```

## Dark Mode

The theme supports dark mode via the `data-theme="dark"` attribute on the `<html>` element. `ThemeToggle` toggles this attribute automatically.

Dark mode tokens are defined in `theme.css` under `[data-theme="dark"]`. Override them the same way as light mode tokens:

```css
[data-theme="dark"] {
  --celine-bg: #0f172a;
  --celine-text: #f8fafc;
}
```
