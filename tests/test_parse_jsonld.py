import glob
from rdflib import Graph

def test_parse_all_jsonld():
    jsonld_files = glob.glob("examples/*.jsonld") + glob.glob("jsonld/*.jsonld")
    assert len(jsonld_files) > 0, "No JSON-LD files found to parse."
    for jsonld in jsonld_files:
        g = Graph()
        try:
            g.parse(jsonld, format="json-ld")
        except Exception as e:
            assert False, f"Failed to parse {jsonld}: {e}"
