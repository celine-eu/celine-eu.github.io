# Apps

## apps/assistant

Standalone full-page AI assistant application. Provides a single-route SvelteKit app that renders `ChatCore` in full-viewport mode.

**Entry point:** `apps/assistant/src/routes/+page.svelte`

**Backend:** `celine-ai-assistant` (port 8012)

**Docker image:** `ghcr.io/celine-eu/celine-assistant`

**Dev:**
```bash
task dev:assistant
# http://localhost:3003
```

---

## apps/webapp

REC participant webapp. A full SvelteKit application for community members, including energy overview, weather, forecast, suggestions, gamification, notifications, settings, feedback, and the embedded assistant.

**Routes:**

| Route | Description |
|---|---|
| `/` | Energy overview — production, consumption, incentives |
| `/suggestions` | Flexibility window suggestions with accept/reject |
| `/assistant` | Embedded `ChatCore` in full mode |
| `/notifications` | Notification list and read/delete |
| `/settings` | User preferences (language, units) |
| `/profile` | User profile |
| `/privacy` | Privacy policy |
| `/terms` | Terms of service |
| `/accept-terms` | Terms acceptance flow |
| `/not-a-participant` | Non-participant landing |
| `/no-smart-meter` | No smart meter landing |

**Key components:** `EnergyChart`, `ForecastCard`, `WeatherWidget`, `StatCard`, `SuggestionCard`, `GamificationPanel`, `PointsChart`

**Layout:** The root layout wraps the app in `AssistantProvider` (floating assistant widget) and calls `GET /api/me` to check terms acceptance.

**Backend:** `celine-webapp` BFF (port 8014)

**Dev:**
```bash
task dev:webapp
# http://localhost:3005
```

---

## apps/grid

Grid resilience dashboard for DSO operators. Displays wind and heat risk maps, alert distributions, trend charts, substation topology, CIM asset topology, and manages alert rules and notification settings.

**Routes:**

| Route | Description |
|---|---|
| `/` | Main grid dashboard — risk maps, filters, trends |
| `/management` | Alert rules and notification settings management |
| `/denied` | Access denied page (non-DSO users) |

**Key components:** `AutocompleteSelect`, `FilterBar`, `LineInspectPanel`, `RiskDonut`, `TrendSparkline`

**Backend:** `celine-grid` (port 8015)

**Docker image:** `ghcr.io/celine-eu/celine-grid-ui`

**Dev:**
```bash
task dev:grid
# http://localhost:3006
```

---

## apps/roi

PV installation ROI calculator. Single-page application for estimating the financial return of a photovoltaic installation, including production estimates, CER incentives, CAPEX, and financial analysis. Supports PDF export of results and map-based location selection.

**Routes:**

| Route | Description |
|---|---|
| `/` | ROI calculator — input form, map picker, results |

**Package dependency:** Uses `@celine-eu/roi-ui` (`RoiCore`, `RoiWidget`) from `packages/roi-ui`.

**Backend:** `celine-roi` (port 8013)

**Dev:**
```bash
task dev:roi
# http://localhost:3004
```
