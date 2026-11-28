"""Historical PR128 counterexamples using the writer's complete synthetic fixture.

Run with --source-root pointing to an original PR128 checkout. Eight mandatory
Git blob pins reject changed inputs; this is not a corrected-query acceptance
suite. SHACL scope is the writer's costing/HTA test schema with RDFS inference.
Exit 1 reports semantic failures; exit 2 means the qualification premise failed.
No network, source edits, empirical data or shared Conductor changes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from decimal import Decimal
from importlib.metadata import version
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SH

EX = Namespace("http://example.org/costing/newborn/")
COST = Namespace("https://w3id.org/uogto/packs/costing-valuation#")
SOURCE_COMMIT = "7e9075b8fd77543fc8853fab20319415cb86597d"
FIXTURE = "examples/newborn-screening-costing.ttl"
ONTOLOGIES = (
    "ontologies/applied/costing-valuation.ttl",
    "ontologies/applied/health-economics-hta.ttl",
    "ontologies/bridges/costing-hta.ttl",
)
SHAPES = ("shapes/costing-valuation.shacl.ttl", "shapes/costing-hta.shacl.ttl")
QUERIES = {
    21: "competency-questions/cq21-costing-batch-conservation.rq",
    23: "competency-questions/cq23-costing-infant-attribution.rq",
}
PINNED_BLOBS = {
    FIXTURE: "0875177ba4886fa5daee057c1eef64e2ccdeaa85",
    ONTOLOGIES[0]: "1bd22cf55c3c6b80816e8b3b2994f7dcd06da566",
    ONTOLOGIES[1]: "7924c94933a6e11623d760098ec976649964f48f",
    ONTOLOGIES[2]: "0989ec950df4d9b2474947a82d61a225a072e5d7",
    SHAPES[0]: "c3a4d2e8e3f10534e1221a4d9c9a9b6c1d2b13cc",
    SHAPES[1]: "5eab82997b64547b7b143e2bb11cb9aa99dd7441",
    QUERIES[21]: "4fbdeb27546d3e78e384b85571b1962825f57574",
    QUERIES[23]: "1028141d5c3677eaeb5a94fff7b21771b16630f2",
}


def clone_subject(data, source, target):
    for predicate, value in list(data.predicate_objects(source)):
        data.add((target, predicate, value))


def query_check(data, query, number, expected):
    result = data.query(query)
    rows = list(result)
    values = [tuple(term.toPython() if term is not None else None for term in row)
              for row in rows]
    return {
        "query": f"CQ{number}",
        "variables": [str(variable) for variable in result.vars],
        # Lists preserve row multiplicity; N3 preserves full IRIs and datatypes.
        "actual_rows_n3": sorted(
            [[term.n3() if term is not None else None for term in row] for row in rows],
            key=repr,
        ),
        "expected_values": sorted(expected, key=repr),
        "passed": sorted(values, key=repr) == sorted(expected, key=repr),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    sources = {}
    for path, expected_blob in PINNED_BLOBS.items():
        try:
            raw = (args.source_root / path).read_bytes()
        except OSError as error:
            parser.error(str(error))
        actual_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if actual_blob != expected_blob:
            parser.error(f"{path}: Git blob mismatch: {actual_blob}")
        sources[path] = raw.decode("utf-8")

    ontology, shapes = Graph(), Graph()
    for path in ONTOLOGIES:
        ontology.parse(data=sources[path], format="turtle")
    for path in SHAPES:
        shapes.parse(data=sources[path], format="turtle")

    baseline_attribution = [(str(EX["infant-a"]), Decimal(60)),
                            (str(EX["infant-b"]), Decimal(90))]
    cases = []
    for name in ("baseline", "zero-allocation", "alternative-direct",
                 "alternative-pool", "missing-scenario-control"):
        data = Graph().parse(data=sources[FIXTURE], format="turtle")
        if name == "zero-allocation":
            data.remove((EX["batch-pool"], COST.hasAllocation, None))
            for allocation in ("batch-to-a", "batch-to-b"):
                data.remove((EX[allocation], None, None))
            data.set((EX["batch-pool"], COST.unallocatedFraction, Literal(Decimal(1))))
            data.set((EX["batch-pool"], COST.unallocatedAmount, Literal(Decimal(100))))
        elif name == "alternative-direct":
            clone_subject(data, EX["collection-a-line"], EX["alternative-direct-line"])
            data.set((EX["alternative-direct-line"], COST.scenarioKey, Literal("alternative")))
            data.add((EX.ledger, COST.hasLine, EX["alternative-direct-line"]))
        elif name in ("alternative-pool", "missing-scenario-control"):
            line, pool = EX["alternative-batch-line"], EX["alternative-pool"]
            clone_subject(data, EX["batch-line"], line)
            data.set((line, COST.scenarioKey, Literal("alternative")))
            data.add((EX.ledger, COST.hasLine, line))
            clone_subject(data, EX["batch-pool"], pool)
            data.set((pool, COST.hasComponentLine, line))
            data.remove((pool, COST.hasAllocation, None))
            for suffix in ("a", "b"):
                allocation = EX[f"alternative-to-{suffix}"]
                clone_subject(data, EX[f"batch-to-{suffix}"], allocation)
                data.set((allocation, COST.fromPool, pool))
                data.add((pool, COST.hasAllocation, allocation))
            if name == "missing-scenario-control":
                data.remove((line, COST.scenarioKey, None))

        conforms, report_graph, _ = validate(
            data, shacl_graph=shapes, ont_graph=ontology, inference="rdfs",
            inplace=False, do_owl_imports=False,
        )
        violations = [tuple(report_graph.value(result, field) for field in
                            (SH.focusNode, SH.resultPath, SH.sourceConstraintComponent))
                      for result in report_graph.subjects(RDF.type, SH.ValidationResult)]
        control = name == "missing-scenario-control"
        shape_passed = (not conforms and
                        (EX["alternative-batch-line"], COST.scenarioKey,
                         SH.MinCountConstraintComponent) in violations) if control else bool(conforms)
        checks = []
        # A failed shape premise never gets presented as a qualified query check.
        if shape_passed and not control:
            if name in ("baseline", "zero-allocation"):
                zero = name == "zero-allocation"
                expected = [(str(EX["batch-pool"]), Decimal(100),
                             Decimal(0 if zero else 100), Decimal(100 if zero else 0),
                             0 if zero else 2)]
                checks.append(query_check(data, sources[QUERIES[21]], 21, expected))
            if name != "zero-allocation":
                checks.append(query_check(data, sources[QUERIES[23]], 23, baseline_attribution))
        cases.append({
            "case": name,
            "triples": len(data),
            "shacl_conforms": bool(conforms),
            "shacl_check_passed": shape_passed,
            "shacl_results_n3": sorted(
                [[term.n3() if term is not None else None for term in row] for row in violations],
                key=repr,
            ),
            "query_checks": checks,
        })

    checks = [check for case in cases for check in case["query_checks"]]
    shape_failures = sum(not case["shacl_check_passed"] for case in cases)
    query_failures = sum(not check["passed"] for check in checks)
    report = {
        "source_commit": SOURCE_COMMIT,
        "source_blobs": PINNED_BLOBS,
        "runtime": {"python": platform.python_version(), "rdflib": version("rdflib"),
                    "pyshacl": version("pyshacl")},
        "scope": "Historical costing/HTA SHACL qualification and pinned-query diagnostics only",
        "scenario_check": "Baseline invariance under alternative-scenario additions; not a future query interface",
        "cases": cases,
        "summary": {"shape_checks": len(cases), "shape_failures": shape_failures,
                    "query_checks": len(checks), "query_failures": query_failures},
    }
    print(json.dumps(report, indent=2, default=str))
    return 2 if shape_failures else 1 if query_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
