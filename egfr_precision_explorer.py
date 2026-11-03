import streamlit as st
import pandas as pd

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
        "Explore a small research dataset and find out what it can tell us "
        "about EGFR mutations and treatment resistance."
    )

    with st.expander("Where does this example dataset come from?"):
        st.write(
            "The example CSV is based on study GSE156054, shared on NCBI GEO. "
            "The study looked at EGFR-mutated lung cancer cells and compared "
            "original cell lines with versions selected for treatment resistance."
        )
        st.markdown(
            "[View the original study on NCBI GEO]"
            "(https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE156054)"
        )
        st.write(
            "The CSV used here is a short summary of six samples. It is not "
            "the full genetic sequencing data."
        )

    st.info(
        "**Before you start:** This example uses cancer cells grown in a lab, "
        "not samples from patients. You can upload another CSV using the "
        "same column names."
    )

    st.markdown("### What should your CSV include?")
    st.write(
        "- `sample_id`: the sample's ID"
        "\n- `mutation`: the EGFR mutation"
        "\n- `treatment_response`: for example, Sensitive or Resistant"
        "\n- Extra columns, such as `cell_line` and `treatment`, can add more detail."
    )

    uploaded_file = st.file_uploader(
        "Upload your genomic CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)
            df.columns = df.columns.str.strip()

            required_columns = {"sample_id", "mutation"}

            if not required_columns.issubset(df.columns):
                st.error(
                    "Your file needs both sample_id and mutation columns. "
                    "Please check the column names and upload it again."
                )

            elif df.empty:
                st.warning("This dataset is empty. Please upload a file with data.")

            else:
                st.success("Your dataset has been uploaded!")

                # Clean the main columns so the summaries are easier to read.
                df["mutation"] = df["mutation"].fillna("Unknown").astype(str).str.strip()
                if "treatment_response" in df.columns:
                    df["treatment_response"] = (
                        df["treatment_response"]
                        .fillna("Not recorded")
                        .astype(str)
                        .str.strip()
                    )

                st.markdown("### 1. Dataset at a glance")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total samples", len(df))
                col2.metric("Different mutation labels", df["mutation"].nunique())
                if "treatment_response" in df.columns:
                    col3.metric(
                        "Response groups",
                        df["treatment_response"].nunique()
                    )
                else:
                    col3.metric("Response information", "Not included")

                st.write(
                    "Each row represents one sample. The mutation and response "
                    "columns help us compare the samples."
                )

                st.markdown("### 2. Explore the samples")
                display_columns = [
                    col for col in
                    ["sample_id", "cell_line", "mutation", "treatment_response", "treatment"]
                    if col in df.columns
                ]
                if display_columns:
                    # A plain text preview avoids relying on the interactive
                    # dataframe viewer for this small educational dataset.
                    st.code(
                        df[display_columns].head(20).to_string(index=False),
                        language="text"
                    )

                st.markdown("### 3. Which mutations appear in the dataset?")
                mutation_counts = (
                    df["mutation"]
                    .value_counts()
                    .rename_axis("Mutation")
                    .to_frame("Number of samples")
                )
                st.bar_chart(mutation_counts)

                most_common = mutation_counts["Number of samples"].max()
                common_mutations = mutation_counts[
                    mutation_counts["Number of samples"] == most_common
                ].index.tolist()

                if len(common_mutations) == 1:
                    st.write(
                        f"**What this means:** {common_mutations[0]} is the "
                        f"most common mutation label in this uploaded dataset, "
                        f"appearing in {most_common} sample(s)."
                    )
                else:
                    st.write(
                        f"**What this means:** {', '.join(common_mutations)} "
                        f"are tied as the most common mutation labels, with "
                        f"{most_common} sample(s) each."
                    )

                st.caption(
                    "This only describes the samples in your file. It does not "
                    "show how common these mutations are in all people with lung cancer."
                )

                if "treatment_response" in df.columns:
                    st.markdown("### 4. Treatment response")
                    response_data = df[
                        df["treatment_response"].ne("Not recorded")
                    ]

                    if not response_data.empty:
                        response_table = pd.crosstab(
                            response_data["mutation"],
                            response_data["treatment_response"]
                        )
                        st.bar_chart(response_table)

                        st.write(
                            "The chart counts how many samples in each mutation "
                            "group have each response label."
                        )

                        response_totals = (
                            response_data["treatment_response"]
                            .value_counts()
                        )
                        st.write("**Response labels in this file:**")
                        for label, number in response_totals.items():
                            st.write(f"- {label}: {number} sample(s)")
                    else:
                        st.info(
                            "There are no recorded treatment responses to compare "
                            "in this dataset."
                        )
                else:
                    st.info(
                        "Your CSV does not have a treatment_response column, "
                        "so this section cannot compare treatment responses."
                    )

                if "cell_line" in df.columns:
                    st.markdown("### 5. Compare related cell lines")
                    cell_lines = sorted(
                        df["cell_line"].dropna().astype(str).unique().tolist()
                    )
                    if cell_lines:
                        chosen_line = st.selectbox(
                            "Choose a cell line",
                            cell_lines
                        )
                        related = df[
                            df["cell_line"].astype(str).str.contains(
                                chosen_line, case=False, na=False
                            )
                        ]
                        st.write(
                            f"These row(s) are linked to **{chosen_line}** "
                            "in the cell_line column:"
                        )
                        comparison_columns = [
                            col for col in
                            ["sample_id", "cell_line", "mutation",
                             "treatment_response", "treatment"]
                            if col in related.columns
                        ]
                        st.code(
                            related[comparison_columns].to_string(index=False),
                            language="text"
                        )
                        st.write(
                            "**How to read this:** Some studies compare an original "
                            "cell line with a version selected to resist a treatment. "
                            "That comparison can help researchers study resistance."
                        )

                st.markdown("### 6. What can we learn from this dataset?")
                st.write(
                    "This small dataset is useful for seeing that the study includes "
                    "different EGFR mutation labels and both treatment-sensitive and "
                    "treatment-resistant cell samples. It gives an example of how "
                    "researchers can compare cell lines."
                )
                st.write(
                    "However, the dataset alone does not prove which genetic change "
                    "caused resistance. It also cannot predict how a patient would "
                    "respond to a treatment."
                )

                st.caption(
                    "This is an educational exploration of research data, not a "
                    "medical tool. Results depend on the file that is uploaded."
                )

        except Exception as error:
            st.error(f"Could not read the CSV file: {error}")

    else:
        st.info(
            "Upload a CSV file to explore its samples, mutations and treatment "
            "response information. No patient data is included in this app."
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
    "EGFR Precision Explorer"
)
