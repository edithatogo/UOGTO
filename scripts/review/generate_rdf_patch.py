import rdflib
import sys

UOGTO = rdflib.Namespace("https://w3id.org/uogto/core#")
UOGTOX = rdflib.Namespace("https://w3id.org/uogto/extensions#")

def build_patches():
    print("Generating RDF Turtle semantic patches for identified gaps...")
    
    # Create patch graph containing classes discovered missing
    g = rdflib.Graph()
    g.bind("uogto", UOGTO)
    g.bind("uogtox", UOGTOX)
    
    solver = UOGTOX.AlgorithmicSolver
    g.add((solver, rdflib.RDF.type, rdflib.OWL.Class))
    g.add((solver, rdflib.RDFS.subClassOf, UOGTO.Solver))
    g.add((solver, rdflib.RDFS.label, rdflib.Literal("Algorithmic Solver", lang="en")))
    g.add((solver, rdflib.Namespace("http://www.w3.org/2004/02/skos/core#").definition, rdflib.Literal("An algorithmic solver resolving game theoretic equilibrium.", lang="en")))
    
    # Save target patch
    patch_path = "ontologies/extensions/algorithmic-solvers-patch.ttl"
    g.serialize(destination=patch_path, format="turtle")
    print(f"Semantic patch saved to: {patch_path}")

if __name__ == "__main__":
    build_patches()
