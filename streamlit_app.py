"""
Variant Calling Project - read-only results viewer.

This app only reads and
displays the prediction and metrics CSVs already produced by the
project's original pipeline/submission — nothing is recomputed here,
so what's shown always matches exactly what was submitted.

Only the synthetic DREAM Challenge samples (syn1-syn5) are included.
real1/real2 are intentionally excluded: they derive from real patient
tumor-normal genomes released under the ICGC-TCGA DREAM Somatic
Mutation Calling Challenge, which restricts real patient data (and
data derived from it) to controlled access under ICGC DACO approval.

Required files (see README notes at the bottom of this file):
  precomputed/{sample}_pred.csv - predicted SNVs, one file per sample
                                   (Chr, START_POS_REF, END_POS_REF)
  precomputed/metrics.csv       - TP/FP/FN/Precision/Recall/F1 per
                                   sample (syn1-syn5 rows only)
"""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Variant Calling Project",
    page_icon="🧬",
)

st.title("Variant Calling Project")
st.caption(
    "Showcase of results from the original project submission — "
    "predictions and metrics shown here are precomputed, not "
    "recalculated live. Synthetic tumour-normal datasets from the "
    "[ICGC-TCGA DREAM Somatic Mutation Calling Challenge.](https://www.synapse.org/Synapse:syn312572/wiki/62018)"
)
st.write("An optimisation of somatic Single Nucleotide Variant calling across 4 different algorithms using a machine learning approach")
st.write("Find source code and more details about the project at [GitHub](https://github.com/maryjess/variant-calling)")

PRECOMPUTED_DIR = Path("precomputed")
SAMPLES = ["syn1", "syn2", "syn3", "syn4", "syn5"]

sample = st.selectbox("Choose a sample", SAMPLES, key="sample")
pred_path = PRECOMPUTED_DIR / f"{sample}_pred.csv"

if not pred_path.exists():
    st.error(f"No precomputed predictions found for {sample}. "
            f"Expected file at {pred_path}.")

else:
    results = pd.read_csv(pred_path)

    st.subheader(f"Predicted SNVs for {sample}")
    st.dataframe(results, use_container_width=True)

    st.download_button(
        "Download CSV",
        results.to_csv(index=False),
        file_name=f"{sample}_predictions.csv",
        mime="text/csv",
    )

    metrics_path = PRECOMPUTED_DIR / "metrics.csv"
    if metrics_path.exists():
        metrics = pd.read_csv(metrics_path)
        row = metrics[metrics["Dataset"] == sample]
        if not row.empty:
            st.subheader("Evaluation metrics")
            st.dataframe(row, use_container_width=True)

st.divider()
st.caption("Pipeline (run offline, not by this app):")
st.caption(
    "VCF -> R (VariantAnnotation, multi-caller parsing) -> feature engineering + Random Forest (Python) "
    "-> predicted SNVs -> evaluated against ground truth."
)

# ---------------------------------------------------------------------------
# README (setup notes, not executed):
#
# Just two things to place under precomputed/ before building:
#
# 1. precomputed/{sample}_pred.csv for sample in syn1..syn5 — the
#    exact pred_df output your generate_pred() already writes to
#    res/{output_name}_pred.csv. Copy/rename those five files over.
#
# 2. precomputed/metrics.csv — the syn-only slice of your metrics
#    output (Dataset, TP, FP, FN, Precision, Recall, F1). Use the
#    numbers from your original submission, not a fresh recompute,
#    so the app matches what was actually graded/submitted.
#
# Do not include real1/real2 files in precomputed/.
# ---------------------------------------------------------------------------