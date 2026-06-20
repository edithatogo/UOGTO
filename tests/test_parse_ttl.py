import glob
from rdflib import Graph

def test_parse_all_ttl():
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True) + glob.glob("shapes/*.ttl")
    assert len(ttl_files) > 0, "No turtle files found to parse."
    for ttl in ttl_files:
        g = Graph()
        try:
            g.parse(ttl, format="turtle")
        except Exception as e:
            assert False, f"Failed to parse {ttl}: {e}"
