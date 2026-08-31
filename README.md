# AB PM-JAY reach vs use (take-home simulation)

District-level analysis of where scheme reach (card holders) is out of step with scheme use (hospitalisation claims), using fully synthetic data.

## Structure

```
data_generator/
  generate_data.py     builds the synthetic files and seeds the flaws
  seeded_flaws.md      what was planted and measured counts
  data/                the four generated CSVs
analysis/
  analysis.ipynb       load, clean, metrics, sensitivity, hypothesis test
  app.py               Streamlit dashboard (D5)
  output/              district_metrics.csv produced by the notebook
D1_Problem_Breakdown.md
D3_Hypothesis.md
D6_Leadership_Note.md  
D7_AI_LOG.md           AI usage log
SUBMISSION.md          cover sheet
run_all.sh             regenerates data and opens the dashboard
```

## Run it

(I'd recommend using a virtual env you can simply remove after to avoid cluttering your system)

From the repo root (paths are relative, any subfolder also works):

```
pip install -r requirements.txt
./run_all.sh
```

`./run_all.sh` regenerates the synthetic data and opens the dashboard in the browser. The dashboard reads the precomputed `analysis/output/district_metrics.csv`, which ships in the repo. To reproduce that file from scratch, run `analysis/analysis.ipynb` once; the committed copy is already in the zip.

Note: if the Faker seed (42) is changed, the data that is generated will also change, and the hard-coded findings in the notebook and streamlit will be obsolete.

## Privacy posture

- Outputs are district-level only; no individual record is ever released.
- People are identified only by surrogate IDs (beneficiary_id, family_id); no names or contact details exist in the data.
- No real NHA, AB PM-JAY, or ABDM data is used; everything is synthetic and fictional.
- On real data, the same pipeline would require pseudonymized identifiers, minimum-cell-size suppression for small counts, and a DPDP Act / SAHI compliance gate before any run.

## What the analysis shows

Private-dominated districts show lower approved claims per card than comparable public-dominated districts, and the gap holds when coverage is controlled for. District 11 has no empanelled-active hospitals and tops the reach-use gap ranking. Districts 7 and 13 show coverage above 100% for different reasons (duplicate records versus an understated eligible-population figure) and are flagged rather than quoted.
