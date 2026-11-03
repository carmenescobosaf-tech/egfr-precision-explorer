import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------
# MAIN PAGE 
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
            "This mutation is a small section of the DNA"
            "strand being missing from exon 19 of the EGFR gene."
        ),
        "biology": (
            "This change can make EGFR signalling more active than "
            "normal. Because of this, cells may receive signals to keep "
            "growing and surviving when they shouldn't."
        ),
        "resistance": (
            "Over time, some cancers with this mutation can become "
            "less responsive to EGFR-targeted treatments. This can "
            "happen because cancer cells develop additional changes, "
            "although the reasons can be different in each tumour."
        )
    },

    "L858R": {
        "gene": "EGFR",
        "exon": "21",
        "type": "Substitution",
        "description": (
            "L858R is a change in exon 21 of the EGFR gene. It happens "
            "when one part of the EGFR protein, called leucine, is "
            "replaced by another, called arginine, at position 858."
        ),
        "biology": (
            "This change can switch on EGFR signalling too much, "
            "encouraging cancer cells to grow and survive."
        ),
        "resistance": (
            "Some tumours with L858R can eventually become resistant "
            "to targeted treatments. Other new genetic mutations can help "
            "cancer cells keep growing even when treatment is being used."
        )
    },

    "T790M": {
        "gene": "EGFR",
        "exon": "20",
        "type": "Substitution",
        "description": (
            "T790M is a change in exon 20 of the EGFR gene. It happens "
            "when threonine is replaced by methionine at position 790 "
            "in the EGFR protein."
        ),
        "biology": (
            "This mutation changes the EGFR protein and can affect "
            "how it works. It is important because it can "
            "help cancer cells avoid the effects of some treatments."
        ),
        "resistance": (
            "T790M is a well-known reason why some cancers become "
            "resistant to earlier EGFR inhibitors. In other words, "
            "a treatment that worked before may become less effective."
        )
    }
}

# -----------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------

st.sidebar.title("🧬 EGFR Explorer")
st.sidebar.caption("Precision Cancer Medicine")

page = st.sidebar.radio(
    "EXPLORE",
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
    "Learn how changes in the EGFR gene are connected "
    "to non-small cell lung cancer."
)

# -----------------------------------------
# OVERVIEW
# -----------------------------------------

if page == "Overview":

    st.title("EGFR Precision Explorer")

    st.markdown(
        "### How gene mutations can affect lung cancer "
        "and its treatment"
    )

    st.write(
        "The EGFR gene is really important in how cells grow. "
        "But what happens when this gene changes? This website "
        "shows how EGFR mutations can contribute to non-small "
        "cell lung cancer (NSCLC), and why some treatments may "
        "stop working over time."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Gene of interest", "EGFR")
    col2.metric("Cancer type", "NSCLC")
    col3.metric("Mutations", len(MUTATIONS))

    st.subheader("What can you learn about EGFR?")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**Mutation Explorer**\n\n"
            "Choose an EGFR mutation and find out what changes "
            "in the gene and how this can affect cells."
        )

        st.info(
            "**Genomic Data**\n\n"
            "Upload a research dataset and create charts to see "
            "which mutations appear in the samples."
        )

    with col2:
        st.info(
            "**Treatment Resistance**\n\n"
            "Find out why some cancer cells can become "
            "resistant to targeted treatments, making it harder to treat."
        )

        st.info(
            "**Research Sources**\n\n"
            "Check out scientific databases and websites where "
            "you can learn more about EGFR and cancer."
        )

    st.divider()

# -----------------------------------------
# MUTATION EXPLORER
# -----------------------------------------

elif page == "Mutation Explorer":

    st.title("Mutation Explorer")

    st.write(
        "Not all EGFR mutations are the same. Choose one below "
        "to learn what it changes and why it matters."
    )

    selected = st.selectbox(
        "Choose an EGFR mutation",
        list(MUTATIONS.keys())
    )

    mutation = MUTATIONS[selected]

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Gene", mutation["gene"])
    col2.metric("Exon", mutation["exon"])
    col3.metric("Mutation type", mutation["type"])

    st.subheader("What is this mutation?")

    st.write(mutation["description"])

    st.subheader("What happens inside the cell?")

    st.write(mutation["biology"])

    st.subheader("Can it affect treatment?")

    st.warning(mutation["resistance"])

    st.divider()

    st.caption(
        "These explanations simplify some complex scientific ideas. "
        "Treatment responses can vary between tumours and depend "
        "on several factors."
    )

# -----------------------------------------
# GENOMIC DATA
# -----------------------------------------

elif page == "Genomic Data":

    st.title("Genomic Data")

    st.write(
        "Here you can upload a CSV research dataset and look at "
        "the genetic information it contains. The charts will "
        "update based on the data you upload."
    )

    st.markdown("""
    **What should your CSV file include?**

    - `sample_id`: an ID for each sample
    - `mutation`: the genetic mutation found in that sample
    - `treatment_response`: an optional category showing the recorded treatment response
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
                    "Your file needs to include both sample_id "
                    "and mutation columns. Please check it and try again."
                )

            elif df.empty:
                st.warning(
                    "This dataset looks empty. Try uploading a file "
                    "that contains some data."
                )

            else:
                st.success("Your dataset has been uploaded!")

                st.subheader("Take a look at your data")

                st.dataframe(df.head(20), use_container_width=True)

                col1, col2 = st.columns(2)

                col1.metric("Total records", len(df))
                col2.metric(
                    "Different mutations",
                    df["mutation"].nunique()
                )

                st.subheader("Which mutations appear most often?")

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
                    title="Mutation frequency in your dataset"
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
                            title="Recorded treatment responses"
                        )

                        st.plotly_chart(
                            fig2,
                            use_container_width=True
                        )

                    else:
                        st.info(
                            "There aren't any complete treatment "
                            "response records in this dataset."
                        )

                st.caption(
                    "These charts only show what is in the uploaded "
                    "dataset. They cannot prove that a mutation causes "
                    "a certain response or predict how a patient will "
                    "respond to treatment."
                )

        except Exception as error:
            st.error(f"Could not read the CSV file: {error}")

    else:
        st.info(
            "Upload a research dataset to see the charts and explore "
            "its mutations. No patient data is included in this app."
        )

# -----------------------------------------
# TREATMENT RESISTANCE
# -----------------------------------------

elif page == "Treatment Resistance":

    st.title("Treatment Resistance")

    st.write(
        "Targeted treatments are designed to block specific changes "
        "in cancer cells. But sometimes, these cells find ways around "
        "the treatment. This is called treatment resistance."
    )

    selected = st.selectbox(
        "Choose a mutation to explore",
        list(MUTATIONS.keys())
    )

    mutation = MUTATIONS[selected]

    st.subheader(selected)

    st.write(mutation["resistance"])

    st.subheader("Why does treatment resistance happen?")

    st.markdown("""
    1. EGFR mutations can change how the EGFR protein works.
    2. Targeted treatments try to block the signals that tell cancer
       cells to grow.
    3. Sometimes, cancer cells develop extra genetic changes that
       help them keep growing despite the treatment.
    4. Researchers study these changes to understand why treatments
       stop working and how new treatment options might be developed.
    """)

    st.warning(
        "This section explains how treatment resistance can happen. "
        "It does not predict whether a specific tumour will respond "
        "to a treatment."
    )

# -----------------------------------------
# RESEARCH SOURCES
# -----------------------------------------

elif page == "Research Sources":

    st.title("Research Sources")

    st.write(
        "I used scientific resources to explore EGFR mutations "
        "and understand their connection to lung cancer. "
        "You can also visit these websites to find more information "
        "and check scientific data."
    )

    st.markdown("""
    ### Scientific databases

    - [NCBI Gene – EGFR](https://www.ncbi.nlm.nih.gov/gene/1956)
    - [ClinVar – Genetic variants](https://www.ncbi.nlm.nih.gov/clinvar/)
    - [cBioPortal – Cancer genomics](https://www.cbioportal.org/)
    - [COSMIC – Cancer mutation database](https://cancer.sanger.ac.uk/cosmic)

    ### Project inspiration

    - [SMART Precision Cancer Medicine](https://apps.smarthealthit.org/app/smart-precision-cancer-medicine)
    """)

    st.info(
        "Scientific information can be complex, so it is important "
        "to check reliable sources and compare information before "
        "making conclusions."
    )

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "EGFR Precision Explorer | Educational project"
)
