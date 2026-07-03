from __future__ import annotations

import glob
import os
import tempfile


def main() -> None:
    import matplotlib.pyplot as plt
    import networkx as nx
    import rdflib
    import streamlit as st
    from pyshacl import validate as shacl_validate

    st.set_page_config(page_title="UOGTO Playground", layout="wide")
    st.title("Universal Open Game Theory Ontology (UOGTO) Playground")
    st.markdown(
        "Upload a game specification in Turtle (.ttl) format to validate SHACL "
        "constraints and inspect game graphs."
    )

    st.sidebar.header("SHACL Configuration")
    ontology_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    shape_files = glob.glob("shapes/*.ttl")

    st.sidebar.write(f"Loaded Ontologies: {len(ontology_files)}")
    st.sidebar.write(f"Loaded SHACL Shapes: {len(shape_files)}")

    uploaded_file = st.file_uploader("Upload Turtle (.ttl) Game Graph", type=["ttl"])
    if uploaded_file is None:
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttl") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        user_graph = rdflib.Graph()
        user_graph.parse(tmp_path, format="turtle")
        st.success(f"Successfully parsed graph with {len(user_graph)} triples.")

        st.header("SHACL Validation Result")
        ont_g = rdflib.Graph()
        for ont in ontology_files:
            ont_g.parse(ont, format="turtle")

        shacl_g = rdflib.Graph()
        for shape in shape_files:
            shacl_g.parse(shape, format="turtle")

        combined = ont_g + user_graph
        with st.spinner("Running PySHACL..."):
            conforms, _results_graph, results_text = shacl_validate(
                combined,
                shacl_graph=shacl_g,
                ont_graph=ont_g,
                inference="rdfs",
            )

        if conforms:
            st.success("Graph conforms to the configured SHACL shapes.")
        else:
            st.error("SHACL validation violations found.")
            st.text(results_text)

        st.header("Game Graph Topology")
        graph = nx.DiGraph()
        for subject, predicate, obj in user_graph:
            subject_name = _short_name(subject)
            obj_name = _short_name(obj)
            predicate_name = _short_name(predicate)
            if "type" in predicate_name:
                continue
            graph.add_edge(subject_name, obj_name, label=predicate_name)

        if graph:
            fig, ax = plt.subplots(figsize=(10, 6))
            pos = nx.spring_layout(graph, seed=42)
            nx.draw(
                graph,
                pos,
                with_labels=True,
                node_color="skyblue",
                node_size=1500,
                edge_color="gray",
                font_size=10,
                font_weight="bold",
                ax=ax,
                arrowsize=20,
            )
            nx.draw_networkx_edge_labels(
                graph,
                pos,
                edge_labels=nx.get_edge_attributes(graph, "label"),
                font_size=8,
                ax=ax,
            )
            st.pyplot(fig)
        else:
            st.info("No semantic edges found to display.")
    except Exception as exc:  # pragma: no cover - displayed in Streamlit UI
        st.error(f"Error parsing/validating graph: {exc}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def _short_name(value: object) -> str:
    name = str(value).split("/")[-1].split("#")[-1]
    if len(name) > 30:
        return name[-30:]
    return name


if __name__ == "__main__":
    main()
