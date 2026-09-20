# FinZoom — Financial Analysis & Valuation Dashboard

## Disclaimer

This is a **fictional personal portfolio project** using **synthetic financial
data**. It is **not affiliated with KPMG** and does not reproduce
confidential methodologies, data or tools. The company analyzed
("NovaTech Solutions") does not exist; all figures are fabricated for
educational purposes.

## Project Overview

FinZoom is a Streamlit application that analyzes five years of historical
financials for a fictional B2B SaaS company, forecasts three additional
years under user-defined assumptions, and values the company with a simple
Discounted Cash Flow (DCF) model. It was built as a portfolio project to
demonstrate business analysis, financial modeling, and data visualization
skills for a Business Analyst alternance (apprenticeship) application.

## Business Context

NovaTech Solutions is a fictional B2B SaaS company with five years of
financial history (2021-2025) but no simple tool to understand its
performance trajectory or test how business assumptions affect its
valuation.

## Business Problem

> The management team needs a simple way to understand historical
> performance and evaluate how business assumptions affect a simulated
> valuation.

## Objectives

- Analyze historical financial performance (2021-2025).
- Calculate standard financial KPIs without hardcoding any result.
- Forecast three future years under adjustable assumptions.
- Value the company with a simple DCF.
- Show how sensitive that valuation is to key assumptions.
- Present the work the way a Business Analyst would: problem, stakeholders,
  requirements, and traceable acceptance criteria.

## Stakeholders

| Stakeholder | Need |
|---|---|
| Management | A synthetic view of historical performance |
| Finance Team | Reliable, traceable KPIs (no hardcoded figures) |
| Business Analyst | Translate business assumptions into financial impact |
| Strategy Team | Understand valuation sensitivity to key assumptions |

## Business Questions

1. How has revenue evolved?
2. How has profitability evolved?
3. What assumptions drive the forecast?
4. How sensitive is valuation to WACC?
5. How sensitive is valuation to terminal growth?
6. How does EBITDA margin affect valuation?

## User Stories

- As **management**, I want to see revenue and EBITDA evolution so I can
  understand the company's trajectory.
- As a **business analyst**, I want to adjust growth and margin
  assumptions so I can produce a 3-year forecast.
- As the **strategy team**, I want to visualize a WACC x Terminal Growth
  heatmap so I can understand valuation sensitivity.
- As a **user**, I want to export results to CSV so I can reuse them
  elsewhere.

## Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| REQ-001 | Display historical revenue | High |
| REQ-002 | Calculate EBITDA margin | High |
| REQ-003 | Let the user modify forecast revenue growth | High |
| REQ-004 | Calculate enterprise value using a DCF | High |
| REQ-005 | Display sensitivity analysis | Medium |
| REQ-006 | Flag data quality anomalies | Medium |
| REQ-007 | Export financial summaries to CSV | Low |
| REQ-008 | Reject a DCF calculation when WACC <= Terminal Growth | High |

## Financial KPIs

- **Revenue Growth** = (Revenue_t - Revenue_t-1) / Revenue_t-1
- **EBITDA Margin** = EBITDA / Revenue
- **Net Margin** = Net Income / Revenue
- **Free Cash Flow (FCF)** = EBIT x (1 - effective tax rate) + D&A - Capex - Working Capital Change
- **FCF Margin** = Free Cash Flow / Revenue
- **Revenue CAGR** = (Revenue_end / Revenue_start)^(1 / n years) - 1

The effective tax rate is derived per year from `Taxes / EBIT` in the
historical data rather than a hardcoded assumption.

## Forecast Methodology

The user controls only **Revenue Growth** and **EBITDA Margin** per
forecast year (2026-2028). Every other ratio (D&A, Capex, Working Capital,
effective tax rate) is held at its 2021-2025 historical average as a
percentage of revenue, so the forecast stays grounded in the company's own
historical data instead of requiring unrelated guesses.

The Forecast page also reports the gap between the forecast assumptions
and the historical average (e.g. "Forecast revenue growth is 4 percentage
points above the historical average") as a **neutral, descriptive
observation** — it does not judge whether the assumption is realistic.

## DCF Methodology

A DCF values the company as the present value of its future free cash
flows, plus a terminal value for everything beyond the explicit forecast
period.

- **Discount Factor** = 1 / (1 + WACC)^t
- **PV(FCF)** = FCF x Discount Factor
- **Terminal Value** = FCF_final x (1 + g) / (WACC - g)
- **Enterprise Value** = Sum of PV(FCF) + PV(Terminal Value)
- **Equity Value** = Enterprise Value + Cash - Debt

If **WACC <= Terminal Growth**, the app raises an explicit error and does
not compute a valuation, since the Gordon Growth formula is undefined (or
negative) in that case.

Default assumptions: WACC = 9%, Terminal Growth = 2.5% (both adjustable).

## Sensitivity Analysis

Two independent sensitivity views:

1. **WACC x Terminal Growth** — Enterprise Value for every combination of
   WACC (8-11%) and Terminal Growth (2-3%), shown as a heatmap.
2. **Revenue Growth x EBITDA Margin** — Enterprise Value for every
   combination of a flat Revenue Growth and EBITDA Margin applied across
   the forecast period, also shown as a heatmap.

**Scenarios** (Downside / Base / Upside) apply three pre-defined
Revenue Growth / EBITDA Margin pairs through the same forecast + DCF
engine and present the resulting Revenue, EBITDA, FCF and Enterprise
Value side by side, without labelling any scenario as "better".

## Data Model

`data/financials.csv` — one row per fiscal year (2021-2025):

| Column | Description |
|---|---|
| Year | Fiscal year |
| Revenue | Total revenue |
| COGS | Cost of goods/services sold |
| Operating_Expenses | Operating expenses (S&M, R&D, G&A) |
| EBITDA | Revenue - COGS - Operating Expenses |
| D_A | Depreciation & amortization |
| EBIT | EBITDA - D&A |
| Taxes | Income taxes |
| Net_Income | EBIT - Taxes |
| Capex | Capital expenditures |
| Working_Capital_Change | Change in working capital |

## Architecture

```
finzoom/
├── app.py                     # Home / Executive Dashboard
├── pages/
│   ├── 1_📊_Financials.py       # Detailed historical statements + KPIs
│   ├── 2_🔮_Forecast.py         # 3-year forecast, historical vs forecast
│   ├── 3_💰_Valuation.py        # Step-by-step DCF, Enterprise & Equity Value
│   ├── 4_🌡️_Sensitivity.py      # WACC x g and Growth x Margin heatmaps
│   ├── 5_🎭_Scenarios.py        # Downside / Base / Upside
│   └── 6_🧭_Business_Analysis.py # Problem, stakeholders, business questions
├── data/
│   └── financials.csv
├── src/
│   ├── data_loader.py         # CSV loading + column validation
│   ├── calculations.py        # KPI calculations (pure functions)
│   ├── ui.py                  # Shared theme + layout helpers
│   ├── forecast.py            # 3-year forecast engine
│   ├── valuation.py           # DCF + sensitivity helpers
│   ├── scenarios.py           # Downside / Base / Upside engine
│   └── data_quality.py        # Anomaly checks
├── tests/
│   └── test_*.py              # pytest unit tests
├── requirements.txt
└── README.md
```

Every calculation function is **pure**: it takes a DataFrame (or values)
and returns a new one, without mutating its input. Pages only call these
functions and render the results — no business logic lives in the UI
layer.

## Installation

```bash
git clone <repository-url>
cd finzoom
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (typically http://localhost:8501) and
navigate through the pages using the sidebar.

Run the test suite:

```bash
python -m pytest tests/ -v
```

## Limitations

- All financial data is **entirely fictional and synthetic**.
- Only 5 years of historical data are available.
- The forecast is simplified: only Revenue Growth and EBITDA Margin are
  user-adjustable; every other ratio is a historical average.
- The DCF is a **pedagogical, simplified model** — it does not reflect a
  real valuation methodology used by any firm.
- No real market data, comparables, or industry benchmarks are used.
- This project makes **no investment recommendation** and draws **no
  conclusion about the real value of any company**.

## Future Improvements

- Add a comparable companies (multiples) valuation alongside the DCF.
- Support uploading a custom CSV to analyze a different (still fictional)
  company.
- Add Monte Carlo simulation for the sensitivity analysis.
- Persist user assumptions across pages with session state.
