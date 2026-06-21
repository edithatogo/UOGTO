import streamlit as st
import rdflib
import networkx as nx
import matplotlib.pyplot as plt
import os
import tempfile
from pyshacl import validate as shacl_validate
import glob

# Set page config
st.set_page_config(page_title="UOGTO Playground", layout="wide")

st.title("🎮 Universal Open Game Theory Ontology (UOGTO) Playground")
st.markdown("Upload a game specification in Turtle (.ttl) format to validate SHACL constraints and inspect game graphs.")

# Sidebar for SHACL validation config
st.sidebar.header("SHACL Configuration")
ontology_files = glob.glob("ontologies/**/*.ttl", recursive=True)
shape_files = glob.glob("shapes/*.ttl")

st.sidebar.write(f"Loaded Ontologies: {len(ontology_files)}")
st.sidebar.write(f"Loaded SHACL Shapes: {len(shape_files)}")

# Main File Upload
uploaded_file = st.file_uploader("Upload Turtle (.ttl) Game Graph", type=["ttl"])

if uploaded_file is not None:
    # Save uploaded file to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttl") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        # Load user graph
        user_graph = rdflib.Graph()
        user_graph.parse(tmp_path, format="turtle")
        st.success(f"Successfully parsed graph with {len(user_graph)} triples!")

        # Perform SHACL Validation
        st.header("🔍 SHACL Validation Result")
        
        ont_g = rdflib.Graph()
        for ont in ontology_files:
            ont_g.parse(ont, format="turtle")
            
        shacl_g = rdflib.Graph()
        for shape in shape_files:
            shacl_g.parse(shape, format="turtle")
            
        combined = ont_g + user_graph
        
        with st.spinner("Running PySHACL..."):
            conforms, results_graph, results_text = shacl_validate(
                combined,
                shacl_graph=shacl_g,
                ont_graph=ont_g,
                inference='rdfs'
            )
            
        if conforms:
            st.success("✅ Graph conforms perfectly to all SHACL shapes!")
        else:
            st.error("❌ SHACL validation violations found!")
            st.text(results_text)

        # Graph Topology Visualization
        st.header("🕸️ Game Graph Topology")
        
        # Build NetworkX representation for visualization
        G = nx.DiGraph()
        for s, p, o in user_graph:
            s_name = str(s).split('/')[-1].split('#')[-1]
            o_name = str(o).split('/')[-1].split('#')[-1]
            p_name = str(p).split('/')[-1].split('#')[-1]
            
            # Simple shortening for presentation
            if len(s_name) > 30: s_name = s_name[-30:]
            if len(o_name) > 30: o_name = o_name[-30:]
            
            # Filter standard type declarations for layout cleanliness
            if "type" in p_name:
                continue
                
            G.add_edge(s_name, o_name, label=p_name)
            
        if len(G) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', font_size=10, font_weight='bold', ax=ax, arrowsize=20)
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)
            st.pyplot(fig)
        else:
            st.info("No semantic edges found to display.")

    except Exception as e:
        st.error(f"Error parsing/validating graph: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
