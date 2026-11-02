import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="EGFR Precision Explorer",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------------------
# DESIGN
# -----------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FB;
}
h1, h2, h3 {
    color: #17365D;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E1E7F0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# MUTATION DATABASE
# -----------------------------------------

MUTATIONS = {
    "Exon 19 deletion": {
        "gene": "EGFR",
        "exon": "19",
        "type": "Deletion",
        "description": (
            "A group of mutations involving the deletion of genetic "
            "material in exon 19 of the EGFR gene."
        ),
        "biology": (
            "These alterations can activate EGFR signalling, which "
            "can promote cell growth and survival."
        ),
        "resistance": (
            "Some cancers with this mutation can develop resistance "
            "to EGFR-targeted treatments over time. The mechanisms "
            "of resistance can differ between tumours."
        )
    },

    "L858R": {
        "gene": "EGFR",
        "exon": "21",
        "type": "Substitution",
        "description": (
            "A specific change in exon 21 of EGFR, where leucine "
            "is replaced by arginine at position 858."
        ),
        "biology": (
            "This alteration can activate EGFR signalling and "
            "encourage cancer cell growth."
        ),
        "resistance": (
            "Tumours with L858R can develop acquired resistance "
            "to targeted therapies. Additional genetic alterations "
            "may contribute to this process."
        )
    },

    "T790M": {
        "gene": "EGFR",
        "exon": "20",
        "type": "Substitution",
        "description": (
            "A change in exon 20 of EGFR, where threonine is "
            "replaced by methionine at position 790."
        ),
        "biology": (
            "This alteration changes the structure and activity "
            "of the EGFR protein."
        ),
        "resistance": (
            "T790M is a recognised mechanism of acquired resistance "
            "to some earlier EGFR inhibitors."
        )
    }
}

# -----------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------

st.sidebar.title("🧬 EGFR Explorer")
st.sidebar.caption("Precision Cancer Medicine")

page = st.sidebar.radio(
    "INDEX",
    [
        "Overview",
        "Mutation Explorer",
        "Genomic Data",
        "Treatment Resistance",
        "Research Sources"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    "A website focused on EGFR mutations "
    "in non-small cell lung cancer."
)

# -----------------------------------------
# OVERVIEW
# -----------------------------------------

if page == "Overview":

    st.title("EGFR Precision Explorer")

    st.markdown(
        "### Understanding genetic mutations and treatment "
        "resistance in lung cancer"
    )

    st.write(
        "This shows how changes "
        "in the EGFR gene can influence the biology of non-small "
        "cell lung cancer (NSCLC) and its response to targeted treatments."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Gene of interest", "EGFR")
    col2.metric("Cancer type", "NSCLC")
    col3.metric("Mutations included", len(MUTATIONS))

    st.subheader("Explore the platform")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**Mutation Explorer**\n\n"
            "Investigate selected EGFR mutations and their "
            "biological effects."
        )

        st.info(
            "**Genomic Data**\n\n"
            "Upload a research dataset and visualise its "
            "genetic information."
        )

    with col2:
        st.info(
            "**Treatment Resistance**\n\n"
            "Explore how genetic alterations can be associated "
            "with changes in treatment response."
        )

        st.info(
            "**Research Sources**\n\n"
            "Access scientific databases and further reading."
        )

    st.divider()

# -----------------------------------------
# MUTATION EXPLORER
# -----------------------------------------

elif page == "Mutation Explorer":

    st.title("Mutation Explorer")

    st.write(
        "Select a genetic alteration to explore its "
        "characteristics and possible relevance to treatment."
    )

    selected = st.selectbox(
        "Select an EGFR mutation",
        list(MUTATIONS.keys())
    )

    mutation = MUTATIONS[selected]

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Gene", mutation["gene"])
    col2.metric("Exon", mutation["exon"])
    col3.metric("Mutation type", mutation["type"])

    st.subheader("Mutation description")
    st.write(mutation["description"])

    st.subheader("Biological effect")
    st.write(mutation["biology"])

    st.subheader("Treatment resistance")
    st.warning(mutation["resistance"])

    st.divider()

    st.caption(
        "These are simplified scientific summaries. "
        "Individual treatment responses depend on multiple factors."
    )

# -----------------------------------------
# GENOMIC DATA
# -----------------------------------------

elif page == "Genomic Data":

    st.title("Genomic Data Analysis")

    st.write(
        "Upload a CSV research dataset to explore mutation "
        "patterns in a group of samples."
    )

    st.markdown("""
    **Expected CSV columns:**

    - `sample_id`: unique sample identifier
    - `mutation`: genetic alteration
    - `treatment_response`: optional response category
    """)

    uploaded_file = st.file_uploader(
        "Upload your genomic CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            required_columns = {"sample_id", "mutation"}

            if not required_columns.issubset(df.columns):
                st.error(
                    "Your file must contain sample_id and mutation columns."
                )

            elif df.empty:
                st.warning("The uploaded dataset is empty.")

            else:
                st.success("Dataset uploaded successfully!")

                st.subheader("Dataset preview")
                st.dataframe(df.head(20), use_container_width=True)

                col1, col2 = st.columns(2)

                col1.metric("Rows", len(df))
                col2.metric(
                    "Unique mutations",
                    df["mutation"].nunique()
                )

                st.subheader("Mutation distribution")

                counts = (
                    df["mutation"]
                    .fillna("Unknown")
                    .value_counts()
                    .reset_index()
                )

                counts.columns = ["Mutation", "Number of records"]

                fig = px.bar(
                    counts,
                    x="Mutation",
                    y="Number of records",
                    color="Mutation",
                    title="Mutation frequency in uploaded dataset"
                )

                st.plotly_chart(fig, use_container_width=True)

                if "treatment_response" in df.columns:

                    st.subheader("Treatment response by mutation")

                    response_data = df.dropna(
                        subset=["mutation", "treatment_response"]
                    )

                    if not response_data.empty:

                        response_counts = (
                            response_data.groupby(
                                ["mutation", "treatment_response"]
                            )
                            .size()
                            .reset_index(name="Number of records")
                        )

                        fig2 = px.bar(
                            response_counts,
                            x="mutation",
                            y="Number of records",
                            color="treatment_response",
                            barmode="group",
                            title="Recorded responses by mutation"
                        )

                        st.plotly_chart(
                            fig2,
                            use_container_width=True
                        )

                    else:
                        st.info("No complete treatment response records.")

                st.caption(
                    "Charts describe the uploaded dataset only. "
                    "They do not establish causation or predict "
                    "an individual patient's response."
                )

        except Exception as error:
            st.error(f"Could not read the CSV file: {error}")

    else:
        st.info(
            "Upload a research dataset to activate the genomic "
            "visualisations. No patient data is included by default."
        )

# -----------------------------------------
# TREATMENT RESISTANCE
# -----------------------------------------

elif page == "Treatment Resistance":

    st.title("Treatment Resistance")

    st.write(
        "Explore the relationship between EGFR mutations "
        "and resistance to targeted treatments."
    )

    selected = st.selectbox(
        "Choose a mutation",
        list(MUTATIONS.keys())
    )

    mutation = MUTATIONS[selected]

    st.subheader(selected)

    st.write(mutation["resistance"])

    st.subheader("Why is this important?")

    st.markdown("""
    1. EGFR mutations can change how the EGFR protein functions.
    2. Targeted treatments are designed to block specific
       signalling pathways.
    3. Additional genetic changes can sometimes allow cancer
       cells to continue growing despite treatment.
    4. Understanding these changes is important for research
       into treatment resistance.
    """)

    st.warning(
        "This section explains established biological concepts. "
        "It does not predict whether a particular tumour will "
        "respond to treatment."
    )

# -----------------------------------------
# RESEARCH SOURCES
# -----------------------------------------

elif page == "Research Sources":

    st.title("Research Sources")

    st.write(
        "These scientific resources can help verify mutation "
        "information and find real genomic datasets."
    )

    st.markdown("""
    ### Scientific databases

    - [NCBI Gene – EGFR](https://www.ncbi.nlm.nih.gov/gene/1956)
    - [ClinVar – Genetic variants](https://www.ncbi.nlm.nih.gov/clinvar/)
    - [cBioPortal – Cancer genomics](https://www.cbioportal.org/)
    - [COSMIC – Cancer mutation database](https://cancer.sanger.ac.uk/cosmic)

    ### Research inspiration

    - [SMART Precision Cancer Medicine](https://apps.smarthealthit.org/app/smart-precision-cancer-medicine)
    """)

    st.info(
        "Use scientific publications and database records to "
        "verify the information before drawing conclusions."
    )

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "EGFR Precision Explorer | Educational prototype"
)
