"""
Variant Calling Project - read-only results viewer.

This app does NOT run the R parser or the Random Forest model live.
Predictions must be precomputed offline (using your existing
generate_pred()-based pipeline) and placed under precomputed/ before
building the Docker image. See README notes at the bottom of this file.

Only the synthetic DREAM Challenge samples (syn1-syn5) are included.
real1/real2 are intentionally excluded: they derive from real patient
tumor-normal genomes released under the ICGC-TCGA DREAM Somatic
Mutation Calling Challenge, which restricts real patient data (and
data derived from it) to controlled access under ICGC DACO approval.
"""

import warnings
import pandas as pd
import streamlit as st
import numpy as np
import joblib

warnings.simplefilter(action='ignore')

st.title("Variant Calling Project")
st.caption(
    "Research/educational demo — not for clinical use. "
    "Predictions shown here are generated on synthetic tumour-normal "
    "datasets from the ICGC-TCGA DREAM Somatic Mutation Calling "
    "Challenge."
)
st.write("An optimisation of somatic Single Nucleotide Variant calling across 4 different algorithms using a machine learning approach")
st.write("Find source code and more details about the project at [GitHub](https://github.com/maryjess/variant-calling)")

# data_source = st.radio("Select data source", ("Upload your own test data", "Use example data"), key = "data_source")

# if data_source == "Upload your own test data":
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
#     if uploaded_file is not None:
#         input_df = pd.read_csv(uploaded_file)
#         st.write("Input data preview:")
#         st.dataframe(input_df.head())

data_source = st.selectbox("Choose a sample", ["syn1", "syn2", "syn3", "syn4", "syn5"], key="data_source")

# inform that syn are synthetic datasets obtained from a particular link
# we avoid real datasets due to privacy concerns and the need for consent when using real patient data.

# if data_source:
