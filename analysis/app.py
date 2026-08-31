from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data_generator" / "data"
OUT = ROOT / "analysis" / "output"

st.set_page_config(page_title="AB PM-JAY reach vs use", layout="wide")

st.markdown(
    "<style>div[data-testid='stMetric'] { background: rgba(0, 120, 212, 0.08); "
    "border-radius: 8px; padding: 12px; }</style>",
    unsafe_allow_html=True,
)

metrics = pd.read_csv(OUT / "district_metrics.csv")
claims = pd.read_csv(DATA / "claims.csv", usecols=["claim_status"])
status = claims.claim_status.value_counts()

NOTES = {
    7: "coverage >100% due to duplicate IDs; de-duplicated figure shown",
    11: "no empanelled-active hospitals; zero approved claims",
    13: "coverage >100% flagged; eligible-population figure looks understated",
}
metrics["note"] = metrics.district_id.map(NOTES).fillna("")

st.title("AB PM-JAY: where reach and use are out of step")
st.caption("District-level, synthetic data only. Metrics built in analysis/analysis.ipynb.")

with st.container(border=True):
    st.markdown("**Overview**")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Districts", metrics.shape[0])
    c2.metric("Approved claims at viable hospitals", int(metrics.approved_claims.sum()))
    c3.metric("Rejected claims", int(status.get("rejected", 0)))
    c4.metric("Pending claims", int(status.get("pending", 0)))
    c5.metric("Districts with no viable supply", int(metrics.supply_count.eq(0).sum()))
    st.caption("Approved figure counts only claims at empanelled-active hospitals; rejected and pending are totals as filed.")

with st.expander("District shortlist (largest reach-use gap first)", expanded=True):
    show = metrics[["district_id", "clean_coverage", "utilisation_per_card", "utilisation_per_eligible",
                    "gap", "supply_per_1000", "private_share", "note"]].sort_values("gap", ascending=False)
    st.dataframe(
        show.round(3),
        width="stretch",
        height=420,
        column_config={
            "district_id": st.column_config.NumberColumn("District", width=90),
            "clean_coverage": st.column_config.NumberColumn("Coverage", width=110),
            "utilisation_per_card": st.column_config.NumberColumn("Use per card", width=120),
            "utilisation_per_eligible": st.column_config.NumberColumn("Use per eligible", width=130),
            "gap": st.column_config.NumberColumn("Gap", width=110),
            "supply_per_1000": st.column_config.NumberColumn("Supply per 1000", width=130),
            "private_share": st.column_config.NumberColumn("Private share", width=120),
            "note": st.column_config.TextColumn("Note", width=340),
        },
    )

with st.expander("Reach vs use by district", expanded=True):
    st.markdown(
        "**Coverage** is the share of eligible people who hold a card, after duplicate records are removed. "
        "A value of 1.0 means every eligible person has a card. "
        "**Use per eligible** is the number of approved hospitalisations per eligible person. "
        "A district with tall coverage but short use is enrolling people without the care being used."
    )
    plot_data = metrics[["district_id", "clean_coverage", "utilisation_per_eligible"]].melt(
        id_vars="district_id", var_name="metric", value_name="value"
    )
    plot_data["metric"] = plot_data["metric"].replace({
        "clean_coverage": "Coverage",
        "utilisation_per_eligible": "Use per eligible",
    })
    bars = alt.Chart(plot_data).mark_bar().encode(
        x=alt.X("district_id:N", title="District"),
        xOffset="metric:N",
        y=alt.Y("value:Q", title="Share"),
        color=alt.Color("metric:N", legend=alt.Legend(title=None)),
    )
    st.altair_chart(bars, width="stretch", height=400)
    st.caption(
        "In nearly every district the coverage bar is taller than the use bar, which is the reach-use gap this dashboard ranks. "
        "District 11 has coverage but no usable hospitals, so use sits at zero. "
        "District 13's bars overshoot 1 because its eligible-population figure is understated."
    )

with st.expander("Reach-use gap vs hospital supply", expanded=True):
    scatter = metrics[["gap", "supply_per_1000", "district_id"]].fillna({"supply_per_1000": 0})
    pts = alt.Chart(scatter).mark_circle(size=70).encode(
        x=alt.X("supply_per_1000:Q", title="Supply per 1000 eligible"),
        y=alt.Y("gap:Q", title="Reach-use gap"),
        tooltip=[
            alt.Tooltip("district_id:N", title="District"),
            alt.Tooltip("supply_per_1000:Q", title="Supply per 1000"),
            alt.Tooltip("gap:Q", title="Gap"),
        ],
    )
    st.altair_chart(pts, width="stretch", height=400)
    st.caption(
        "Each dot is a district; hover to identify it. District 11 is shown at supply 0 (no empanelled-active hospitals). "
        "The gap is largest where supply collapses, but raw supply does not explain it: the notebook shows the private share of usable hospitals tracks utilisation per card instead."
    )

with st.expander("Hypothesis: private vs public hospital supply", expanded=True):
    st.markdown(
        "**The hypothesis (D3):** districts where the usable hospitals are mostly private use the scheme less than comparable public-dominated districts. "
        "Districts with no usable hospitals are excluded. Coverage is held constant below, so this is not just an enrolment effect."
    )
    m = metrics[metrics.private_share.notna()].copy()
    m["group"] = np.where(m.private_share > 0.5, "private_dominated", "public_dominated")
    m["coverage_band"] = pd.qcut(m.clean_coverage, 3, labels=["low", "mid", "high"])

    means = m.groupby("group").utilisation_per_card.mean()
    diff = means.get("private_dominated", np.nan) - means.get("public_dominated", np.nan)
    st.markdown(
        f"**Approved claims per card: {means.get('private_dominated', float('nan')):.2f} in private-dominated districts "
        f"vs {means.get('public_dominated', float('nan')):.2f} in public-dominated districts.** "
        f"The private-dominated average is {abs(diff):.2f} lower."
    )

    st.subheader("Private share vs use per card (each dot is a district)")
    pts = alt.Chart(m).mark_circle(size=70).encode(
        x=alt.X("private_share:Q", title="Private share of usable hospitals"),
        y=alt.Y("utilisation_per_card:Q", title="Approved claims per card"),
        color=alt.Color("group:N", title="Group"),
        tooltip=[
            alt.Tooltip("district_id:N", title="District"),
            alt.Tooltip("private_share:Q", title="Private share"),
            alt.Tooltip("utilisation_per_card:Q", title="Claims per card"),
        ],
    )
    st.altair_chart(pts, width="stretch", height=400)

    st.subheader("Use per card by coverage band (control for reach)")
    band_means = m.groupby(["coverage_band", "group"]).utilisation_per_card.mean().reset_index()
    bars = alt.Chart(band_means).mark_bar().encode(
        x=alt.X("coverage_band:N", title="Coverage band (low to high)"),
        xOffset="group:N",
        y=alt.Y("utilisation_per_card:Q", title="Mean approved claims per card"),
        color=alt.Color("group:N", title="Group"),
    )
    st.altair_chart(bars, width="stretch", height=400)
    st.caption(
        "Private-dominated districts sit below public-dominated districts in every coverage band, "
        "so the lower use is more likely tied to who owns the hospitals, and not to how many people hold cards."
    )

with st.expander("Column key"):
    st.markdown(
        "- **district_id**: district number.\n"
        "- **Coverage**: share of eligible people holding a card, duplicates removed.\n"
        "- **Use per card**: approved hospitalisations per card holder.\n"
        "- **Use per eligible**: approved hospitalisations per eligible person.\n"
        "- **Gap**: reach minus use. Bigger means many cards but few hospitalisations.\n"
        "- **Supply per 1000**: usable (empanelled and active) hospitals per 1000 eligible people.\n"
        "- **Private share**: share of usable hospitals that are private.\n"
        "- **Note**: flags on districts that need attention before the number is used."
    )
