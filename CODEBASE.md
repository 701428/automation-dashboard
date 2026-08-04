# Automation Dashboard — Complete Code & Flow Reference

> Polaris Grids · Streamlit app · v2.0  
> Last updated: 2026-07-14

---

## 1. File Structure

```
Automation_Dash/
├── app.py                          # Home page — Executive Overview
├── pages/
│   ├── 1_Portfolio.py              # Portfolio page — all project cards
│   └── 2_Project_Detail.py         # Project detail — 5 tabs
├── utils/
│   ├── auth.py                     # Login / role / session helpers
│   ├── data_loader.py              # All file I/O and Excel parsing
│   ├── calculations.py             # Pure business logic (coverage, pending, etc.)
│   ├── exports.py                  # Excel + HTML/PDF export generators
│   └── styles.py                   # CSS injection, color tokens, layout helpers
├── components/
│   ├── charts.py                   # All Plotly chart functions
│   ├── gantt.py                    # Gantt / sprint timeline charts
│   ├── kpi_cards.py                # KPI metric row renderers
│   └── tables.py                   # Table helpers
├── data/
│   ├── automation_data.xlsx        # Internal normalized store (4 sheets)
│   ├── Automation tracker.xlsx     # Raw uploaded tracker (preserved as-is)
│   └── completion_settings.json    # Editable per-project plan settings (JSON)
├── static/
│   ├── logo.svg                    # Light-mode logo
│   └── logo-dark.svg               # Dark-mode / login logo
├── credentials.yaml                # bcrypt-hashed user credentials + roles
└── requirements.txt
```

---

## 2. Data Files

### `data/automation_data.xlsx` — Internal Store (4 sheets)

The dashboard never reads the raw tracker directly at runtime. It always reads from this normalized file.

| Sheet | Key Columns |
|---|---|
| `Projects` | `id, name, total_cases, automatable, non_automatable, automated, in_progress, team_size, start_date, target_date, daily_avg, status, priority, color, notes` |
| `Non_Automatable` | `project_id, module, count, reason, approach` |
| `Day_Plan` | `project_id, date, module, planned_cases, actual_cases, cumulative, assigned_to, remarks, status` |
| `Completion_Plan` | `project_id, name, total_cases, automatable, duration_days, daily_avg, start_date, expected_completion, status` |

### `data/completion_settings.json` — Editable Plan Settings

Stores only the user-editable fields per project so tracker re-uploads don't overwrite user plans:
```json
{
  "1p": { "daily_avg": 8.0, "start_date": "2026-07-13", "status": "On Track" },
  "hes": { "daily_avg": 3.0, "start_date": "2026-06-19", "status": "On Track" }
}
```

### `data/Automation tracker.xlsx` — Raw Tracker

Multi-sheet file with one sheet per project domain. Each sheet has 4 labelled sections:
1. **Automation Status Summary** — totals row
2. **Non-Automatable Test Cases** — list of modules with counts & reasons
3. **Day-by-Day Automation Plan** — date-by-date rows
4. **Project Completion Plan** — one row per environment with dates and daily avg

---

## 3. Project IDs & Known Projects

| Sheet / Source | `id` | Name |
|---|---|---|
| Firmware → 1-Phase | `1p` | 1-Phase Meter Firmware |
| Firmware → 3-Phase WC | `3p_wc` | 3-Phase WC |
| Firmware → 3-Phase LTCT | `3p_ltct` | 3-Phase LTCT |
| HES sheet | `hes` | HES (Gomati / Sangai) |
| VEE sheet | `vee` | VEE (Gomati / Sangai) |
| Consumer_App sheet | `consumer_app` | Consumer App (Gomati Android) |
| Comms sheet | `comms` | Comms (4G / RF / IMG / DCU) |
| WFM sheet | `wfm` | WFM Portal – Stage (UP) |

New sheets not in the list above are **auto-registered** at parse time with a cycled color and `"Medium"` priority.

---

## 4. Data Flow — End to End

```
User uploads tracker.xlsx
         │
         ▼
process_uploaded_file()
  ├─ Detects tracker format (any core sheet present OR "Automation Status Summary" found)
  ├─ Saves raw bytes → data/Automation tracker.xlsx
  └─ Calls _parse_and_save_tracker()
              │
              ├─ Iterates all sheets (skips: Sheet1/2/3, Summary, Index, etc.)
              ├─ Locates 4 section-header rows via _find_row()
              ├─ For "Firmware" sheet → _parse_firmware_sheet()
              │     Splits day-plan rows by env_key ("1-Phase", "3-Phase WC", "3-Phase LTCT")
              │     Creates 3 project rows (one per firmware sub-project)
              └─ For all other sheets → _parse_single_sheet()
                    Reads summary row for totals
                    Reads completion plan for dates/status
                    Outputs project row + non-auto rows + day-plan rows
              │
              ▼
        Writes 4 sheets to data/automation_data.xlsx
              │
              ▼
app.py / pages call ensure_data_file()
  ├─ If tracker newer than internal store → re-parse (auto-sync on load)
  └─ If internal store missing → seed from hardcoded defaults
              │
              ▼
load_projects() → pd.DataFrame (reads Projects sheet)
              │
              ▼
enrich_projects()
  ├─ coverage_pct = automated / automatable × 100  (capped at 100%)
  └─ pending = automatable − automated
              │
              ▼
load_completion_plan(df_projects)
  ├─ Reads completion_settings.json for daily_avg, start_date, status
  ├─ Computes: pending = automatable − automated
  ├─ duration_days = ceil(pending / daily_avg)   (0 if daily_avg = 0)
  └─ expected_completion = start_date + duration_days
```

---

## 5. Key Functions — `utils/data_loader.py`

| Function | What it does |
|---|---|
| `ensure_data_file()` | Sync gate: re-parses tracker if newer, seeds defaults if store missing |
| `_parse_and_save_tracker(path)` | Iterates all tracker sheets, calls sheet-specific parsers, writes `automation_data.xlsx` |
| `_parse_firmware_sheet(...)` | Splits Firmware sheet into 3 sub-project rows (1p / 3p_wc / 3p_ltct) |
| `_parse_single_sheet(...)` | Parses any single-project sheet into project + non-auto + plan + completion rows |
| `load_projects()` | Reads Projects sheet, coerces dates, fills missing status |
| `save_projects(df)` | Overwrites Projects sheet in `automation_data.xlsx` |
| `load_non_automatable(pid?)` | Reads Non_Automatable sheet, optionally filtered by project |
| `save_non_automatable(pid, df)` | Merges new rows for `pid`, writes full Non_Automatable sheet |
| `load_day_plan(pid?)` | Reads Day_Plan sheet, parses dates |
| `save_day_plan(pid, df)` | Merges new rows for `pid`, writes full Day_Plan sheet |
| `load_completion_plan(df_projects?)` | Builds completion plan dynamically from live project data + JSON settings |
| `save_completion_plan(df)` | Persists only `daily_avg`, `start_date`, `status` to JSON (not Excel) |
| `process_uploaded_file(file)` | Handles tracker upload (auto-detect format) or internal-format xlsx/csv |
| `get_tracker_download()` | Returns original tracker bytes if stored, else reconstructs from internal data |
| `get_template_excel()` | Returns blank 4-sheet xlsx template |

### Parsing Helpers

| Helper | Purpose |
|---|---|
| `_parse_int(val)` | Safe int parse, returns 0 on failure |
| `_parse_float(val)` | Safe float parse |
| `_parse_date(val)` | Returns ISO date string or None |
| `_safe_str(val)` | Returns `""` for None/NaN |
| `_find_row(df, keyword)` | Finds first row in col-0 containing keyword (case-insensitive) |
| `_rows_between(df, start, end)` | Returns raw rows from start+2 to end, skipping all-NaN rows |
| `_count_from_name(name)` | Extracts count from `"TAP (54 Test Cases)"` style strings |

---

## 6. Key Functions — `utils/calculations.py`

| Function | Formula / Logic |
|---|---|
| `coverage_pct(row)` | `min(automated / automatable × 100, 100)`. If `automatable = 0`, returns 100. |
| `pending(row)` | `max(automatable − automated, 0)` |
| `enrich_projects(df)` | Applies `coverage_pct` and `pending` as new columns on the projects DataFrame |
| `portfolio_summary(df)` | Aggregates totals across all projects → dict with `total_cases, total_auto, coverage_pct, completed, in_progress, not_started, total_projects` |
| `plan_cumulative(df_plan)` | Adds `cumulative_actual` (cumsum of actual_cases) and `cumulative_planned` columns |
| `schedule_status_from_plan(row, df_plan)` | Returns "At Risk" if >30% of past plan rows have actual < planned, else "On Track" |

---

## 7. Authentication — `utils/auth.py`

- Credentials stored in `credentials.yaml` with bcrypt-hashed passwords
- Roles: `admin` (full edit access) vs `user` / viewer (read-only)
- `require_login()` — renders branded login form; sets session state on success; calls `st.stop()` if not authenticated
- `is_admin()` — checks `st.session_state["_role"] == "admin"`
- `current_user()` — returns display name from session state

**Session state keys set on login:**

| Key | Value |
|---|---|
| `authentication_status` | `True` |
| `username` | username string |
| `name` | display name |
| `_role` | `"admin"` or `"user"` |

---

## 8. Pages

### `app.py` — Executive Overview (Home)

**Render order:**
1. `inject_css` + `sidebar_logo`
2. `require_login()`
3. Sidebar: dark mode toggle + admin upload + template download
4. `get_data(data_version)` → cached; calls `ensure_data_file`, `enrich_projects`, `load_non_automatable`, `load_day_plan`, `load_completion_plan`, `portfolio_summary`
5. `portfolio_kpi_row(summary)` — top KPI strip
6. 3-column charts: `coverage_donut` | `progress_bar_chart` | `portfolio_stacked_bar`
7. `project_gantt` — full-width timeline
8. Completion Plan dataframe
9. Non-Automatable summary (by-project count + detail table)
10. Export buttons: Tracker download, Excel summary, HTML/PDF, CSV

**Cache:** `@st.cache_data(ttl=60)` keyed on `data_version` — incremented on upload or save.

---

### `pages/1_Portfolio.py` — Portfolio

**Render order:**
1. Project cards (one column per project) — shows coverage%, progress bar, status, target, notes, "View Detail" button
2. Two charts: `progress_bar_chart` + `portfolio_stacked_bar`
3. `project_gantt`
4. **Editable progress table** (admin only) — can edit `automated`, `in_progress`, `status` inline and Save

**"View Detail" button** sets `st.session_state["selected_project"] = row["id"]` then `st.switch_page`.

---

### `pages/2_Project_Detail.py` — Project Detail

**Project selector:** dropdown at top; synced with `selected_project` in session state.

**5 Tabs:**

| Tab | Content |
|---|---|
| **Summary** | Donut chart + editable project fields (admin: all fields; viewer: read-only) |
| **Non-Automatable** | Pie by module + detail table + editable records (admin) |
| **Day-by-Day Plan** | Sprint Gantt + Planned vs Actual bar chart + editable plan rows (admin) |
| **Completion Plan** | 9 live KPI metrics + progress bar + editable daily_avg/start_date/status form (admin) |
| **Export** | Per-project and full-portfolio Excel/HTML downloads |

**Save flow for Day Plan:**  
Edit rows → Save Plan → recalculates cumulative as `cumsum(actual_cases)` → calls `save_day_plan()` → if any actual_cases > 0, also updates `automated` in Projects sheet.

**Save flow for Completion Plan:**  
Form submit → calls `save_completion_plan(upd)` → writes only `daily_avg / start_date / status` to `completion_settings.json` → `load_completion_plan` recomputes `duration_days` and `expected_completion` dynamically on next load.

---

## 9. Charts — `components/charts.py`

All functions return `go.Figure`. Caller passes `dark: bool` for theme switching.

| Function | Chart type | Data needed |
|---|---|---|
| `coverage_donut(df, dark)` | Donut — Automated / Pending / Non-Auto | `df_projects` |
| `progress_bar_chart(df, dark)` | Horizontal bar — coverage% per project | `df_projects` |
| `portfolio_stacked_bar(df, dark)` | Stacked bar — Automated / Pending / Non-Auto per project | `df_projects` |
| `velocity_trend(df_daily, name, dark)` | Line — planned vs actual cumulative | `df_plan` |
| `forecast_chart(row, df_daily, plan_df, dark)` | Scatter+line — actual + forecast + target hline + target date vline | `row`, `df_plan` |
| `project_radar(df, dark)` | Radar — 5 dimensions: coverage, team size, velocity, progress, on-time risk | `df_projects` |
| `burndown_chart(row, df_daily, burn_df, dark)` | Scatter — ideal burndown vs actual remaining | `df_plan` |
| `velocity_histogram(df_daily, dark)` | Histogram — daily delta distribution | `df_plan` |
| `portfolio_timeline_lines(df, daily_all, dark)` | Multi-line — coverage% over time per project | `df_projects`, `df_plan` |

**Color thresholds for progress bar:**  
≥80% → teal | ≥50% → blue | <50% → warning (amber)

---

## 10. Export — `utils/exports.py`

### `export_excel(df_projects, df_non_auto, df_plan, df_completion) → bytes`
Uses `xlsxwriter`. 4 sheets: Projects Summary, Non-Automatable, Day-by-Day Plan, Completion Plan.  
Header style: white text on `#0a3690`. Alternating row background `#ebf4fb`.

### `export_pdf_html(df_projects, df_non_auto, df_plan) → str`
Returns self-contained HTML with inline CSS. Contains:
- Cover block (blue gradient)
- KPI row: Total Cases, Automatable, Automated, Projects count
- Project summary table with inline progress bars
- Non-automatable table
- Day-by-Day Plan table (first 20 rows)

Open in browser → Ctrl+P → Save as PDF.

---

## 11. Admin vs Viewer Permissions

| Action | Admin | Viewer |
|---|---|---|
| Upload tracker / data | ✅ | ❌ |
| Edit project fields (Summary tab) | ✅ | ❌ |
| Edit non-automatable records | ✅ | ❌ |
| Edit day-by-day plan | ✅ | ❌ |
| Edit completion plan settings | ✅ | ❌ |
| Edit portfolio progress table | ✅ | ❌ |
| View all data / charts | ✅ | ✅ |
| Download exports | ✅ | ✅ |
| Reset to defaults | ✅ | ❌ |

---

## 12. Data Version & Cache Invalidation

`st.session_state.data_version` is an integer counter.  
It is **incremented** any time data changes (upload, save, reset).  
`@st.cache_data(ttl=60)` functions are keyed on `data_version`, so a version bump forces a full reload.

---

## 13. Common Data Gotchas

- **Firmware sheet is special** — it maps to 3 project rows, not 1. Day-plan rows are split by `env_key` prefix match.
- **Completion Plan is always computed dynamically** — never read raw from Excel at runtime. `load_completion_plan()` builds it from live project data + JSON settings every time.
- **`completion_settings.json` is the source of truth for `daily_avg`, `start_date`, `status`** — not the Projects sheet. Tracker re-uploads do NOT overwrite this file.
- **`_rows_between`** skips the section-header row and the column-header row (offset `start + 2`), then reads until next section.
- **Auto-discovered sheets** (not in `_SHEET_PID`) get IDs from `re.sub(r"[^a-z0-9]", "_", sheet.lower())` and colors cycled from `_AUTO_COLORS`.
- **Date columns** use `_safe_date()` which returns `"TBD"` for any unparseable / NaT / empty value — never NaN.
- **`save_day_plan` / `save_non_automatable`** load the full sheet, replace rows for the given `project_id`, write back — so other projects' data is never lost.

---

## 14. Session State Keys Reference

| Key | Set by | Purpose |
|---|---|---|
| `authentication_status` | `require_login()` | `True` when logged in |
| `_role` | `require_login()` | `"admin"` or `"user"` |
| `_username` / `_name` | `require_login()` | Display name |
| `dark_mode` | dark mode toggle | `bool` — passed to all chart/CSS functions |
| `data_version` | any save / upload | Cache bust key |
| `uploader_key` | upload success | Forces file uploader widget reset |
| `selected_project` | Portfolio "View Detail" button | `project_id` string for detail page |
| `_upload_ok_msg` | upload success | Success toast shown once on rerun |
| `_login_error` | failed login | Shows error inside login card |
