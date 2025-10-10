# Lifeline UI Pattern Kit

This kit standardizes the look-and-feel for all list/detail pages. It contains lightweight Vue 3 components plus accompanying CSS variables.

## Design Tokens
- Typography: Inter (primary), 14px base, 20px line-height. Headings use 600 weight.
- Color palette:
  - `--color-surface: #ffffff`
  - `--color-surface-muted: #f6f8fb`
  - `--color-border: #e1e6ef`
  - `--color-text: #1f2937`
  - `--color-text-muted: #6b7280`
  - Primary `#2563eb`, Success `#059669`, Warning `#f59e0b`, Danger `#dc2626`.
- Radii: `8px` cards, `6px` buttons, `12px` badges.
- Shadows: `0 10px 30px rgba(15, 23, 42, 0.08)` for cards.

Tokens will live in `src/assets/styles/tokens.css` and be imported globally in `main.js`.

## Core Components
| Component | Purpose | Key Props |
| --- | --- | --- |
| `UiCard` | Wraps content in elevated surface. Handles headers, actions, empty state messaging. | `title`, `subtitle`, `actions`, `padding`, `variant="muted"` |
| `UiButton` | Primary/secondary/ghost buttons with consistent spacing + icons. | `variant="primary|secondary|outline|ghost|danger"`, `size="sm|md|lg"`, `loading`, `icon` |
| `UiTable` | Standard table shell with toolbar slot, sticky header, built-in loading & empty views. | `columns` (array), `rows` (array), `loading`, `emptyTitle`, `emptyMessage` |
| `UiStatusBadge` | Color-coded pill for statuses. | `status="success|warning|danger|info"`, `icon`, `label` |
| `UiFormField` | Label, helper, error message inside consistent grid. | `label`, `hint`, `error`, `required`, default slot for input |
| `UiModal` | Reusable modal shell used by banking/projects forms. | `modelValue`, `title`, `size`, `primaryLabel`, `onPrimary`, `dismissLabel` |
| `UiSkeleton` | Animated skeleton blocks for table/card placeholders. | `type="table|card|line"`, `rows`, `cols` |
| `UiToast` | Event-based notification system (simple event bus). | `type`, `message`, `timeout` |

### Layout Helpers
- `.page-shell`: max-width container with responsive padding.
- `.toolbar`: flex row with wrap, spacing, aligns filters/actions.
- `.data-grid`: CSS grid for summary cards.

## Usage Guidelines
1. Wrap every list page in `<div class="page-shell">` and start with `<PageHeader>` (coming later).
2. CRUD lists use `UiCard` containing a `UiTable`. Provide `toolbar` slot with search + filters.
3. Forms live inside `UiModal` or `UiCard` and use stacked `UiFormField` blocks.
4. Loading state: show `<UiSkeleton type="table" :rows="5">` while fetching.
5. Errors: use `<UiCard variant="muted">` with message and `<UiButton variant="outline">Retry</UiButton>`.

## Implementation Order
1. Build `tokens.css`, `ui-base.css` and register globally.
2. Implement `UiButton`, `UiCard`, `UiStatusBadge` – reuse across modules immediately.
3. Build `UiTable` with lightweight column definition API.
4. Add `UiModal`, `UiFormField`, and `UiSkeleton`.
5. Replace raw markup in modules iteratively (banking → reports → payroll → projects).

## Next Steps for Remaining Views

### Completed Refactors
- ✅ **BankAccounts.vue**: Full refactor with UiCard, UiButton, UiFormField, UiModal, loading/error states
- ✅ **IncomeStatement.vue**: Added filters, export, UiStatusBadge, responsive layout
- ✅ **Payrolls.vue**: Modal forms, improved table, API client integration
- ✅ **ProjectsView.vue**: Complete CRUD with modal, status badges, search/filter

### Remaining Views to Update
Apply the same pattern to these views for consistency:

1. **Banking Module**
   - `BankStatementLines.vue`: Transaction list with filters, pagination
   - `Reconciliations.vue`: Reconciliation workflow with status tracking

2. **Reports Module**
   - `BalanceSheet.vue`: Financial statement with period selection
   - `CashFlow.vue`: Cash flow analysis with chart integration
   - `GeneralLedger.vue`: Ledger entries with account filtering

3. **Payroll Module**
   - `Employees.vue`: Employee management with department filters
   - `Benefits.vue`: Benefits administration
   - `Deductions.vue`: Tax/deduction setup
   - `Paystubs.vue`: Paystub generation and history
   - `Taxes.vue`: Tax configuration

4. **Projects Module**
   - `ProjectsView.vue`: ✅ Completed (time entries, invoices pending)

### Migration Pattern
For each remaining view:

1. **Import Components**: Add imports for UiButton, UiCard, UiFormField, UiModal, UiStatusBadge
2. **Update Template**:
   - Replace `<div class="container">` with `<div class="page-shell">`
   - Add `<header class="page-toolbar">` with title/subtitle and actions
   - Wrap content in `<UiCard>` with title/subtitle
   - Replace `<table>` with `<div class="table-container"><table class="data-table">`
   - Add loading/error states
3. **Update Script**:
   - Add loading/saving/error data properties
   - Use apiClient instead of direct axios
   - Add proper error handling
4. **Update Styles**: Remove custom CSS, use design tokens

### Example Migration
```vue
<!-- Before -->
<div class="container">
  <h1>Transactions</h1>
  <table class="table">
    <!-- table content -->
  </table>
</div>

<!-- After -->
<div class="page-shell">
  <header class="page-toolbar">
    <div>
      <h1 class="page-title">Transactions</h1>
      <p class="page-subtitle">Review account activity and reconcile balances.</p>
    </div>
    <UiButton icon="+" variant="primary">Import</UiButton>
  </header>
  
  <UiCard title="Recent transactions">
    <div class="table-container">
      <table class="data-table">
        <!-- table content -->
      </table>
    </div>
  </UiCard>
</div>
```

### Testing Checklist
- [ ] All views load without console errors
- [ ] Search/filter functionality works
- [ ] CRUD operations (create/edit/delete) function
- [ ] Loading states display during API calls
- [ ] Error states show helpful messages
- [ ] Responsive layout on mobile/tablet
- [ ] Consistent spacing and typography across views

This document guides both development and visual QA for the partial views refresh.
