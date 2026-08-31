(written by me, structured and formatted by AI)

# D7: AI usage log

## Tools used

- DeepSeek v4 Flash, driven through the OpenCode harness, for almost all of the work: the generator, the streamlit dashboard, and the analysis.
- Faker for synthetic data.
- pandas and numpy for analysis.
- nbformat and nbclient to build and execute the notebook headlessly.
- Streamlit and Altair for the dashboard.
- Plain search (manual) for the India scale figures only. No real NHA, AB PM-JAY, or ABDM data was fetched or used.

## Places the AI got it wrong, and how it was caught

1. Duplicate-row bug in the generator. The "duplicate claim" dirt rows were shallow copies, so a dirt edit applied to one row also showed up on its twin, inflating the detected counts (for example 31 impossible dates instead of 30). Caught because the planted counts and the detected counts did not line up when I checked the output. Fix: make the duplicate rows independent deep copies, then re-verify every count.

2. Zero-supply district moved. I altered the AI agent's original claim status split (55 approved-23 rejected-22 pending), the seeded random stream shifted and the district with no empanelled-active hospitals changed from districts 3/17 to district 11. The write-up in the seeded_flaws and the hypothesis doc still named the old districts. Caught by cross-checking the facility table against the docs.

3. Percentile bug in the notebook. A line meant to rank district 13 among peers instead ranked its three metrics against each other, because rank() was applied to a single row. Caught because the printed percentile was nonsensical. Fix: rank across the column, re-run, and confirm district 13 now sits mid-range.

4. Cwd-dependent paths. The notebook assumed it ran from the repo root, which breaks on another machine if the notebook is opened from a subfolder. Using the root in the notebook also caused an error because it's in a nested folder. Caught during a manual notebook run from inside analysis/. Fix: resolve the repo root by walking up to a marker file, and the agent verified that the notebook runs identically from the repo root and from a subfolder.
