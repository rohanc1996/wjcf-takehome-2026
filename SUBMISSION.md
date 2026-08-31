(AI mostly wrote right at the end, and then I manually adjusted it.)

## How to reproduce from a fresh clone

1. `pip install -r requirements.txt`
2. `./run_all.sh` (regenerates the synthetic data and opens the dashboard)
3. `analysis/analysis.ipynb` can be run separately to reproduce the analysis and rewrite `district_metrics.csv`

Paths are relative to the repository, so the steps work from the repo root or any subfolder.

## Self-scored checklist (against Section 4 of the brief)

| Check | Score | Notes |
| --- | --- | --- |
| Thread runs from a fresh clone with one documented command | Yes | `./run_all.sh` generates data (or regenerates the same data since we use a fixed seed) and opens the dashboard; the notebook is run separately to reproduce the analysis. |
| Analysis detects the problems seeded in the data | Yes | Every planted flaw is detected with counts; the two >100% coverage districts are resolved to different causes. |
| Hypothesis is falsifiable, and I say plainly whether data confirmed or refuted it | Yes | Confirm/refute in D3; the notebook states the finding and its limits. |
| One-screen visual communicates without me in the room | Yes | Streamlit dashboard with shortlist, charts, and plain-language interpretation lines. |
| Leadership note reads like someone who sat across from a senior official and is honest about limits | Yes | In my opinion... |

## Assumptions I made

- The synthetic districts are small reference units, not real districts; the eligible-population range was chosen so a few thousand beneficiaries and claims stay coherent (see D1 and seeded_flaws.md).
- Only approved claims at empanelled-and-active hospitals count as use.
- A coverage ratio above 100% is investigated, not discarded: duplicates for district 7, denominator for district 13.
- The dashboard reads the precomputed `district_metrics.csv`, which ships in the repo; `analysis/analysis.ipynb` regenerates it if run from scratch. If the faker seed is changed, new data is created and then the analysis and metrics csv will both change. I didn't factor this in for now, but if this were to happen, the hard-coded lines under the plots in the dashboard will be obsolete.

## What I cut and why

- No real-data lookups and no external eligibility sources, per the brief.
- No statistical significance testing; with 20 synthetic districts the honest output is a ranking and a group comparison, not a p-value.
- No per-claim, package, or provider drill-down; the question is district-level only.

## Approx. hours spent

3-4 in total during an 8 hour stretch...I was pulled away for other tasks a few times in between and couldn't lock in for extended stretches of time sadly. 