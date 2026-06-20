import os
import glob
from rdflib import Graph

def build():
    print("Building UOGTO Ontologies...")
    os.makedirs("dist", exist_ok=True)
    
    # 1. Merge Ontologies
    merged_ontology = Graph()
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    for ttl in ttl_files:
        print(f"Parsing and merging {ttl}...")
        merged_ontology.parse(ttl, format="turtle")
        
    merged_ontology.serialize(destination="dist/uogto.ttl", format="turtle")
    print(f"Merged ontology saved to dist/uogto.ttl. Total triples: {len(merged_ontology)}")
    
    # Class / Property Counts
    from rdflib.namespace import RDF, OWL
    classes = list(merged_ontology.subjects(RDF.type, OWL.Class))
    obj_properties = list(merged_ontology.subjects(RDF.type, OWL.ObjectProperty))
    dt_properties = list(merged_ontology.subjects(RDF.type, OWL.DatatypeProperty))
    print(f"Total defined Classes: {len(classes)}")
    print(f"Total defined ObjectProperties: {len(obj_properties)}")
    print(f"Total defined DatatypeProperties: {len(dt_properties)}")


    # 2. Merge SHACL shapes
    merged_shapes = Graph()
    shacl_files = glob.glob("shapes/*.ttl")
    for shacl in shacl_files:
         print(f"Parsing and merging SHACL shape {shacl}...")
         merged_shapes.parse(shacl, format="turtle")
    merged_shapes.serialize(destination="dist/uogto-shapes.ttl", format="turtle")
    print(f"Merged SHACL shapes saved to dist/uogto-shapes.ttl. Total triples: {len(merged_shapes)}")

    # 3. Copy JSON-LD Contexts
    contexts = glob.glob("jsonld/*.jsonld")
    for ctx in contexts:
        dest = os.path.join("dist", os.path.basename(ctx))
        with open(ctx, "r", encoding="utf-8") as src_f:
            content = src_f.read()
        with open(dest, "w", encoding="utf-8") as dest_f:
            dest_f.write(content)
        print(f"Copied {ctx} to {dest}")

if __name__ == "__main__":
    build()
