"""Independent synthetic CQ21/CQ23 receiving checks, deliberately not in pytest's suite.

Usage (on a checkout containing PR128 query files):
  python conductor/reviews/pr128-independent-costing-20261120/check_cq21_cq23.py \
      --query-root competency-questions --expect-original-head

With no --expect-original-head, rerun on the costing writer's corrected query bytes.
Exit 1 on any semantic counterexample. No external source data, edits or network.
"""
from __future__ import annotations

import argparse
import hashlib
from decimal import Decimal
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF
from rdflib.namespace import XSD

EX = Namespace("http://example.org/costing/newborn/")
COST = Namespace("https://w3id.org/uogto/packs/costing-valuation#")
EXPECTED_GIT_BLOBS = {
    21: "4fbdeb27546d3e78e384b85571b1962825f57574",
    23: "1028141d5c3677eaeb5a94fff7b21771b16630f2",
}
NAMES = {
    21: "cq21-costing-batch-conservation.rq",
    23: "cq23-costing-infant-attribution.rq",
}
FIXTURE = """@prefix ex: <http://example.org/costing/newborn/> .
@prefix cost: <https://w3id.org/uogto/packs/costing-valuation#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:infant-a a ex:Infant . ex:infant-b a ex:Infant .
ex:specimen-a cost:relatedCostObject ex:infant-a .
ex:specimen-b cost:relatedCostObject ex:infant-b .
ex:confirmation-b cost:relatedCostObject ex:infant-b .
ex:a-use cost:forCostObject ex:specimen-a .
ex:b-use cost:forCostObject ex:specimen-b .
ex:conf-use cost:forCostObject ex:confirmation-b .
ex:a-line a cost:ValuationLine ; cost:sourceResourceUse ex:a-use ; cost:lineAmount "10.00"^^xsd:decimal ; cost:scenarioKey "baseline" .
ex:b-line a cost:ValuationLine ; cost:sourceResourceUse ex:b-use ; cost:lineAmount "10.00"^^xsd:decimal ; cost:scenarioKey "baseline" .
ex:conf-line a cost:ValuationLine ; cost:sourceResourceUse ex:conf-use ; cost:lineAmount "30.00"^^xsd:decimal ; cost:scenarioKey "baseline" .
ex:batch-line a cost:ValuationLine ; cost:lineAmount "100.00"^^xsd:decimal ; cost:scenarioKey "baseline" .
ex:pool a cost:CostPool ; cost:poolAmount "100.00"^^xsd:decimal ; cost:unallocatedAmount "0.00"^^xsd:decimal ;
 cost:hasComponentLine ex:batch-line ; cost:hasAllocation ex:alloc-a, ex:alloc-b .
ex:alloc-a a cost:Allocation ; cost:fromPool ex:pool ; cost:allocatedTo ex:infant-a ; cost:allocatedAmount "50.00"^^xsd:decimal .
ex:alloc-b a cost:Allocation ; cost:fromPool ex:pool ; cost:allocatedTo ex:infant-b ; cost:allocatedAmount "50.00"^^xsd:decimal .
"""


def cash(value):
    return Decimal(str(value)) if value is not None else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-root", type=Path, required=True)
    parser.add_argument("--expect-original-head", action="store_true")
    args = parser.parse_args()
    queries = {}
    for n, name in NAMES.items():
        data = (args.query_root / name).read_bytes()
        git_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if args.expect_original_head and git_blob != EXPECTED_GIT_BLOBS[n]:
            raise ValueError(f"CQ{n} exact Git blob mismatch: {git_blob}")
        print(f"CQ{n} Git blob: {git_blob}")
        queries[n] = data.decode("utf-8")

    failures = []
    def check(label, actual, expected):
        ok = actual == expected
        print(f"{'PASS' if ok else 'FAIL'} {label}: actual={actual!r}; expected={expected!r}")
        if not ok:
            failures.append(label)

    g = Graph().parse(data=FIXTURE, format="turtle")
    rows = list(g.query(queries[21]))
    check("CQ21 baseline", [(cash(r.allocatedTotal), int(r.recipientCount)) for r in rows], [(Decimal(100), 2)])
    totals = {str(r.infant).rsplit('/', 1)[-1]: cash(r.attributedAmount) for r in g.query(queries[23])}
    check("CQ23 baseline", totals, {"infant-a": Decimal(60), "infant-b": Decimal(90)})

    g.remove((EX.pool, COST.hasAllocation, None))
    for n in ("alloc-a", "alloc-b"):
        g.remove((EX[n], None, None))
    g.set((EX.pool, COST.unallocatedAmount, Literal("100.00", datatype=XSD.decimal)))
    rows = list(g.query(queries[21]))
    check("CQ21 zero allocation", [(cash(r.allocatedTotal), None if r.recipientCount is None else int(r.recipientCount)) for r in rows], [(Decimal(0), 0)])

    g = Graph().parse(data=FIXTURE, format="turtle")
    g.add((EX["a-alt"], RDF.type, COST.ValuationLine))
    g.add((EX["a-alt"], COST.sourceResourceUse, EX["a-use"]))
    g.add((EX["a-alt"], COST.lineAmount, Literal("7.00", datatype=XSD.decimal)))
    g.add((EX["a-alt"], COST.scenarioKey, Literal("alternative")))
    direct = {str(r.infant).rsplit('/', 1)[-1]: cash(r.attributedAmount) for r in g.query(queries[23])}
    check("CQ23 direct scenario isolation", direct.get("infant-a"), Decimal(60))

    g = Graph().parse(data=FIXTURE, format="turtle")
    g.add((EX["pool-alt"], RDF.type, COST.CostPool))
    g.add((EX["pool-alt"], COST.hasComponentLine, EX["alt-line"]))
    g.add((EX["alt-line"], COST.scenarioKey, Literal("alternative")))
    for suffix, infant in (("a", "infant-a"), ("b", "infant-b")):
        allocation = EX["alt-allocation-" + suffix]
        g.add((allocation, RDF.type, COST.Allocation))
        g.add((allocation, COST.fromPool, EX["pool-alt"]))
        g.add((allocation, COST.allocatedTo, EX[infant]))
        g.add((allocation, COST.allocatedAmount, Literal("60.00", datatype=XSD.decimal)))
    pooled = {str(r.infant).rsplit('/', 1)[-1]: cash(r.attributedAmount) for r in g.query(queries[23])}
    check("CQ23 pooled scenario isolation", pooled, {"infant-a": Decimal(60), "infant-b": Decimal(90)})
    print(f"Summary: {5-len(failures)}/5 semantic checks passed; {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
