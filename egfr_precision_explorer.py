
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
            "This mutation happens when a small part of the DNA "
            "in exon 19 of the EGFR gene is missing."
        ),
        "biology": (
            "This change can make EGFR send too many growth signals. "
            "Because of this, cells may keep growing and surviving "
            "when they normally shouldn't."
        ),
        "resistance": (
            "Some cancers with this mutation can become less sensitive "
            "to EGFR-targeted treatments over time. This can happen when "
            "cancer cells develop other changes."
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
            "This change can make EGFR send too many signals, "
            "which can help cancer cells grow and survive."
        ),
        "resistance": (
            "Some cancers with L858R can become resistant to targeted "
            "treatments over time. Other genetic changes can help "
            "cancer cells keep growing even while treatment is being used."
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
            "This change affects the EGFR protein and how it works. "
            "It is important because it can help cancer cells avoid "
            "the effects of some treatments."
        ),
        "resistance": (
            "T790M is a well-known reason why some cancers stop "
            "responding to earlier EGFR inhibitors. This means that "
            "a treatment that worked before may stop working as well."
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
    "Find out how changes in the EGFR gene are linked "
    "to non-small cell lung cancer."
)

# -----------------------------------------
# OVERVIEW
# -----------------------------------------

if page == "Overview":

    st.title("EGFR Precision Explorer")

    st.markdown(
        "### How changes in a gene can affect lung cancer and its treatment"
    )

    st.write(
        "The EGFR gene plays an important part in how cells grow. "
        "But what happens when this gene changes? This website looks "
        "at how EGFR mutations are linked to non-small cell lung cancer "
        "(NSCLC), and why some treatments can stop working over time."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Gene of interest", "EGFR")
    col2.metric("Cancer type", "NSCLC")
    col3.metric("Mutations", len(MUTATIONS))

    st.subheader("What is on this website?")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**Mutation Explorer**\n\n"
            "Pick an EGFR mutation and see what changes in the gene "
            "and how it can affect cells."
        )

        st.info(
            "**Genomic Data**\n\n"
            "Upload a research dataset and use charts to see which "
            "mutations are found in the samples."
        )

    with col2:
        st.info(
            "**Treatment Resistance**\n\n"
            "Find out why some cancer cells can stop responding "
            "to certain treatments."
        )

        st.info(
            "**Research Sources**\n\n"
            "Find the scientific websites and databases used "
            "for this project."
        )

    st.divider()

# -----------------------------------------
# MUTATION EXPLORER
# -----------------------------------------

elif page == "Mutation Explorer":

    st.title("Mutation Explorer")

    st.write(
        "EGFR mutations are not all the same. Pick one below "
        "to see what changes and why it matters."
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
        "These explanations are simplified to make the science easier "
        "to understand. The way a tumour responds to treatment can vary."
    )

# -----------------------------------------
# GENOMIC DATA
# -----------------------------------------

elif page == "Genomic Data":

    st.title("Genomic Data")

    st.write(
        "Upload a CSV file to see the data in it. You can look at "
        "the mutations in the samples and compare their treatment responses."
    )

    st.write(
        "The example CSV for this project has information about six "
        "research samples. It is not the full genetic sequencing data."
    )

    st.markdown("### What does the CSV need?")

    st.write(
        "- `sample_id`: the ID of each sample"
        "\n- `mutation`: the EGFR mutation found in the sample"
        "\n- `treatment_response`: for example, Sensitive or Resistant"
        "\n- Extra columns like `cell_line` and `treatment` give more information."
    )

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)
            df.columns = df.columns.str.strip()

            required_columns = {"sample_id", "mutation"}

            if not required_columns.issubset(df.columns):
                st.error(
                    "The file needs both sample_id and mutation columns. "
                    "Check the column names and try again."
                )

            elif df.empty:
                st.warning(
                    "This file is empty. Try uploading a CSV with some data."
                )

            else:
                st.success("CSV uploaded successfully!")

                # Clean the main columns so the results are easier to read.
                df["mutation"] = (
                    df["mutation"]
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                )

                if "treatment_response" in df.columns:
                    df["treatment_response"] = (
                        df["treatment_response"]
                        .fillna("Not recorded")
                        .astype(str)
                        .str.strip()
                    )

                # 1. Quick look at the data

                st.markdown("### 1. A quick look at the data")

                col1, col2, col3 = st.columns(3)

                col1.metric("Number of samples", len(df))

                col2.metric(
                    "Different mutations",
                    df["mutation"].nunique()
                )

                if "treatment_response" in df.columns:
                    col3.metric(
                        "Response types",
                        df["treatment_response"].nunique()
                    )
                else:
                    col3.metric("Treatment response", "Not included")

                st.write(
                    "Each row is one sample. The columns show details "
                    "about its mutation and treatment response."
                )

                # 2. Sample information

                st.markdown("### 2. Look at the samples")

                display_columns = [
                    col for col in
                    [
                        "sample_id",
                        "cell_line",
                        "mutation",
                        "treatment_response",
                        "treatment"
                    ]
                    if col in df.columns
                ]

                if display_columns:
                    st.code(
                        df[display_columns].head(20).to_string(index=False),
                        language="text"
                    )

                # 3. Mutation chart

                st.markdown("### 3. Which mutations are in the data?")

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
                        f"**What the chart shows:** {common_mutations[0]} "
                        f"appears the most in this file, with "
                        f"{most_common} sample(s)."
                    )
                else:
                    st.write(
                        f"**What the chart shows:** {', '.join(common_mutations)} "
                        f"appear the most, with {most_common} sample(s) each."
                    )

                st.caption(
                    "This only shows the samples in this file. It does not "
                    "tell us how common these mutations are in all people "
                    "with lung cancer."
                )

                # 4. Treatment response

                if "treatment_response" in df.columns:

                    st.markdown("### 4. How did the cells respond to treatment?")

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
                            "This chart shows how many samples in each "
                            "mutation group were marked as Sensitive "
                            "or Resistant."
                        )

                        response_totals = (
                            response_data["treatment_response"]
                            .value_counts()
                        )

                        st.write("**Treatment responses in this file:**")

                        for label, number in response_totals.items():
                            st.write(f"- {label}: {number} sample(s)")

                    else:
                        st.info(
                            "There are no treatment response results "
                            "in this file."
                        )

                else:
                    st.info(
                        "This CSV does not have a treatment_response column, "
                        "so treatment responses cannot be compared."
                    )

                # 5. Compare cell lines

                if "cell_line" in df.columns:

                    st.markdown("### 5. Compare cell lines")

                    cell_lines = sorted(
                        df["cell_line"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    if cell_lines:

                        chosen_line = st.selectbox(
                            "Choose a cell line",
                            cell_lines
                        )

                        related = df[
                            df["cell_line"].astype(str).str.contains(
                                chosen_line,
                                case=False,
                                na=False
                            )
                        ]

                        st.write(
                            f"Here are the samples linked to **{chosen_line}**:"
                        )

                        comparison_columns = [
                            col for col in
                            [
                                "sample_id",
                                "cell_line",
                                "mutation",
                                "treatment_response",
                                "treatment"
                            ]
                            if col in related.columns
                        ]

                        st.code(
                            related[comparison_columns].to_string(index=False),
                            language="text"
                        )

                        st.write(
                            "Some research studies compare an original cell "
                            "line with another version that has become resistant "
                            "to treatment. This helps researchers study why "
                            "treatments sometimes stop working."
                        )

                # 6. Main findings

                st.markdown("### 6. What does the data show?")

                st.write(
                    "This file has samples with different EGFR mutations. "
                    "Some cells were sensitive to treatment, while others "
                    "were resistant. The charts make it easier to compare "
                    "the samples."
                )

                st.write(
                    "However, this small dataset cannot prove which genetic "
                    "change caused resistance. It also cannot predict how "
                    "a patient would respond to a treatment."
                )

                st.caption(
                    "This is a student science project, not a medical tool. "
                    "The results depend on the CSV file that is uploaded."
                )

        except Exception as error:
            st.error(f"Could not read the CSV file: {error}")

    else:
        st.info(
            "Upload a CSV file to see the samples, mutations and treatment "
            "responses. This project uses research cell samples, not patient data."
        )

# -----------------------------------------
# TREATMENT RESISTANCE
# -----------------------------------------

elif page == "Treatment Resistance":

    st.title("Treatment Resistance")

    st.write(
        "Some cancer treatments are made to block changes in cancer cells. "
        "But sometimes, the cells find ways around the treatment. "
        "This is called treatment resistance."
    )

    selected = st.selectbox(
        "Choose a mutation to learn more",
        list(MUTATIONS.keys())
    )

    mutation = MUTATIONS[selected]

    st.subheader(selected)

    st.write(mutation["resistance"])

    st.subheader("Why can this happen?")

    st.markdown("""
    1. EGFR mutations can change how the EGFR protein works.
    2. Targeted treatments try to block signals that tell cancer cells to grow.
    3. Sometimes, cancer cells develop other genetic changes that help
       them keep growing even when treatment is being used.
    4. Researchers study these changes to understand why treatments stop
       working and how new treatments could be developed.
    """)

    st.warning(
        "This section explains how treatment resistance can happen. "
        "It cannot predict if a specific tumour will respond to treatment."
    )

# -----------------------------------------
# RESEARCH SOURCES
# -----------------------------------------

elif page == "Research Sources":

    st.title("Research Sources")

    st.write(
        "These are some of the scientific websites and databases used "
        "to learn about EGFR mutations and lung cancer. They are also "
        "useful if you want to find out more about the topic."
    )

    st.markdown("""
    ### Scientific websites and databases

    - [NCBI Gene – EGFR](https://www.ncbi.nlm.nih.gov/gene/1956)
    - [ClinVar – Genetic variants](https://www.ncbi.nlm.nih.gov/clinvar/)
    - [cBioPortal – Cancer genomics](https://www.cbioportal.org/)
    - [COSMIC – Cancer mutation database](https://cancer.sanger.ac.uk/cosmic)

    ### Project inspiration

    - [SMART Precision Cancer Medicine](https://apps.smarthealthit.org/app/smart-precision-cancer-medicine)
    """)

    st.info(
        "It is always important to check where scientific information "
        "comes from and use reliable sources."
    )

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "EGFR Precision Explorer"
)
