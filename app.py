import streamlit as st
import rdflib
import json
import os
import datetime
import time


#### Page configuration
st.set_page_config(
    page_title="Semantic-Beacons demo",
    layout="centered",
    initial_sidebar_state="collapsed",
)

test_query = """
    SELECT * WHERE {
        ?subject ?predicate ?object.
    } LIMIT 10
"""

st.info(
    "Check the [reference article]() and the [documentation](https://github.com/SemanticBeacon/SemanticBeacon) of the project"
)

st.title(
    "Semantic Beacons: a framework to support federated querying over genomic variants and public Knowledge Graphs"
)

st.markdown(
    "Comprehensive genomic data exchange is challenging but critical for future research. Beacon API networks, promoted by initiatives like \gls{ga4gh}, facilitate genomic variation data discovery while preserving privacy and data ownership. However, their use is often limited by the need for costly storage, compute intensive data pre-processing, and periodic updates as genomic knowledge constantly progresses. This work proposes an on-the-fly approach for enriching genomic variants with biological annotations provided by established knowledge bases. It thus reduces the computational load and processing time. We explore integrating open and interoperable life sciences knowledge graphs with sensitive health genomic data discoverable through Beacon APIs. We propose this federated framework as a step towards increasing FAIRness of genomic data."
)

st.subheader("Summary")
st.markdown(
    """
    1. Knowledge graph structure
    2. Execute prewritten queries
    3. Perform custom queries
"""
)

st.subheader("Exploration request")

st.markdown(f"Count the number of nodes in the local knowledge graph")

st.button(
    "Execute query",
    on_click=test_query,
    key=0,
    type="primary",
    disabled=False,
    use_container_width=False,
)

qryTab1, qryTab2 = st.tabs(["Sparql query", "Result table"])

# with qryTab1:
#     customquery = st.text_area("Edit you SPARQL query", value="", height=400)

# with qryTab2:
#     st.markdown("Preview of your custom SPARQL query")
#     st.code(customquery, language="sparql", line_numbers=False)

with qryTab1:
    st.markdown(
        f"This SPARQL query allows to get the number of nodes present in the graph"
    )
    st.code(test_query, language="sparql", line_numbers=True)

with qryTab2:
    if st.session_state.is_exec_countqry:
        with st.spinner("Wait for it..."):
            time.sleep(2)
        st.success("Query performed correctly !")
        print(st.session_state.df_res_countqry)
        st.table(st.session_state.df_res_countqry)
    else:
        st.markdown("Execute the request to see the results !")
