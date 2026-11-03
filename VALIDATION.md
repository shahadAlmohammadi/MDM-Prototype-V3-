# Verification — 3 November 2026

Input: the user-attached Elm_Customer_Journey_Page8 (4).zip, including its latest workbook and UI changes. No earlier working copy was substituted.

## Automated checks

18 tests passed using unittest: original analytical reconciliation, customer/product scope, locked relationship, date eligibility, inactivity, assistant answers, workbook duplicate rejection and actual Streamlit AppTest mount; plus SQL reconciliation, customer and city scope, Arabic assistant, row limits, read-only SQL/CTEs, blocked writes/attachment/functions/multiple statements and execution timeout.

Latest supplied workbook totals: 75 customers, 546,530 transactions for Oct 2025–Sep 2026; Saudi National Bank 390,000; YAKEEN 12,000; seven inactive customers. Data was preserved, including the prior removal of Najd Services. Earlier 76/600,530 figures were not restored.

Python compilation and JavaScript syntax checks passed.

## Browser review

The exact frontend module/styles with Excel-derived payload was inspected at 1348px desktop content width and 375px mobile content width. English/light and Arabic/dark reviewed; no page-level horizontal overflow in inspected states. Mobile filters were revised after visual review. Dark KPI backgrounds and text contrast were corrected after visual review.

Checked: theme and language switching/persistence, SQL loading/result UI, result sorting and pagination, CSV download event, narrative modal, scenario slider calculation, map filter (15 Riyadh customers / 402,831 scoped transactions), customer selection, product active indicator, start/pause stream with incoming rows, and event cap. Motion respects OS reduced-motion and an in-app override.

The browser preview uses a static QA bridge with real Python-precomputed SQL results for starter queries; the delivered app uses the actual Streamlit SQL trigger and Python SQLite engine. Backend execution and app mounting were checked separately. A browser session against the complete Python server, Windows launcher execution and optional external AI service were not verified in this environment. The two reference Streamlit URLs could not be retrieved by the lookup service; the user's supplied screenshots informed the controls.

## Data semantics

- Active line: distinct customers with positive transactions in each month; not a forecast.
- Map: deterministic demo city assignments for the original bundled workbook only. A different workbook uses optional customer city/latitude/longitude columns; missing/invalid locations are not fabricated.
- Activity pulse: linked product with recorded recent positive transactions, using the existing four-month threshold.
- Live feed: explicit client-side demo events; opt-in, paused in hidden tabs, capped at 30, no effect on underlying totals.
- Scenario: arithmetic sensitivity calculation, explicitly not a prediction.
- SQL: SQLite, scoped Excel copy in memory, SELECT/CTE reads, allowlisted functions, 500-row result cap, one statement, 2-second execution deadline. It is not a production database connection.

## Review conclusions

Executive review: the analytical overview remains the entry point; technical features are grouped in Data studio. No unsupported churn/revenue scores added. UX review: contextual detail, minimal animation, explicit demo labels, clear selection/locked states and keyboard focus. Arabic UI copy and RTL provided; product/customer names and SQL identifiers retain their data identity where appropriate. Developer verification remains necessary when integrating enterprise authentication, real data streams or production databases.

## Focused refinement
Removed System and standalone data settings/language controls; appearance now uses one gear with light/dark and language. Data studio moved to the dashboard footer. Customer scenario and story are available below the journey only in customer detail. Rounded activity bar tracks preserve blue. Active pulse strengthened with reduced-motion support. Trend area reveal and latest count added. Map JSON now explicitly reads UTF-8 on Windows; Arabic map labels and pills checked in browser. All 18 backend tests passed again.

## Compact interaction refinement
Preferences moved to toolbar corner without a utility spacer; language has matching two-option buttons. Removed chart download tool duplicates and motion toggle (OS reduced-motion retained). Customer scenario consolidated beside customer activity; active badge background removed. Selected timeline pulses. Contribution bars use rounded tracks; chart labels now show value | percentage (trend denominator is eligible scoped customers). Shared hover highlights added to chart panels, rows, tables and facts. Browser checked actual pulse animation names and no chart download controls.

## Alignment and map polish
Removed sandbox from customer detail. Customer scenario title matches activity tile label sizing. Settings now sits inside the toolbar next to export with a transparent background. Overview row columns share identical widths (813/435px at inspected desktop viewport); no page overflow. Selected timeline animation is infinite independent of hover, subject to OS motion accessibility settings. Top customer bars now have rounded tracks retaining existing colors. Map uses an SVG depth layer and a restrained shadow; Arabic labels preserved. JavaScript syntax and browser render checked; no analytical code changed.

## Toolbar and night-theme refinement
Reset is icon-only, grouped with export and appearance. Browser measured all three SVGs at 19x19px and the same vertical coordinate; no page overflow. Customer detail label fits navigation. Dark KPI parent specificity corrected: angled silhouette restored with thin edge and layered navy fill; night background and panel hover refined. Customer activity verified below journey (journey top459px; activity top1102px in inspected view). Reference Netlify page was unavailable to the lookup service; no claim of matching unseen contents.

## Full-width inactive table
Removed the overview Top VIP customers panel. Its adjacent inactive-customer table now spans the row with larger type, aligned columns, all rows visible, subtle row entry and hover, and a proportional inactivity-duration indicator. Customer links and filter-derived values retained. JavaScript syntax checked; no analytical rules changed.
