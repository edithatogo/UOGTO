"""Executable semantic boundaries; these tests do not qualify a costing engine."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD


ROOT = Path(__file__).resolve().parents[1]
COST = Namespace("https://w3id.org/uogto/packs/costing-valuation#")
BRIDGE = Namespace("https://w3id.org/uogto/bridges/costing-hta#")
CORE = Namespace("https://w3id.org/uogto/core#")
EX = Namespace("http://example.org/costing/newborn/")
FUND = Namespace("http://example.org/costing/activity-funding/")


@pytest.fixture(scope="module")
def schema() -> tuple[Graph, Graph]:
    ontology = Graph()
    for name in (
        "ontologies/applied/costing-valuation.ttl",
        "ontologies/applied/health-economics-hta.ttl",
        "ontologies/bridges/costing-hta.ttl",
    ):
        ontology.parse(ROOT / name, format="turtle")
    shapes = Graph()
    for name in ("costing-valuation.shacl.ttl", "costing-hta.shacl.ttl"):
        shapes.parse(ROOT / "shapes" / name, format="turtle")
    return ontology, shapes


@pytest.fixture
def data() -> Graph:
    return Graph().parse(ROOT / "examples/newborn-screening-costing.ttl", format="turtle")


@pytest.fixture
def funding_data() -> Graph:
    return Graph().parse(ROOT / "examples/activity-funding-valuation.ttl", format="turtle")


def check(data: Graph, schema: tuple[Graph, Graph]) -> tuple[bool, str]:
    ontology, shapes = schema
    conforms, _, report = validate(
        data, shacl_graph=shapes, ont_graph=ontology, inference="rdfs"
    )
    return bool(conforms), str(report)


def decimal(value: str) -> Literal:
    return Literal(value, datatype=XSD.decimal)


def clone_subject(data: Graph, source: URIRef, target: URIRef) -> None:
    for predicate, value in list(data.predicate_objects(source)):
        data.add((target, predicate, value))


def test_synthetic_newborn_example_conforms(data, schema) -> None:
    conforms, report = check(data, schema)
    assert conforms, report


def test_weighted_activity_funding_does_not_require_resource_classification(funding_data, schema) -> None:
    ontology, shapes = schema
    conforms, _, report = validate(
        funding_data, shacl_graph=shapes, ont_graph=ontology, inference="rdfs", inplace=True
    )
    assert conforms, report
    assert not list(funding_data.subjects(RDF.type, COST.Resource))
    assert not list(funding_data.subjects(RDF.type, COST.ResourceUse))
    assert funding_data.value(FUND["activity-quote"], COST.appliesToResource) is None
    assert funding_data.value(FUND["funding-policy"], COST.valuationBasis) == COST["funding-valuation"]
    amount = Decimal(funding_data.value(FUND["funding-line"], COST.lineAmount))
    quantity = Decimal(funding_data.value(FUND["weighted-output"], COST.quantity))
    rate = Decimal(funding_data.value(FUND["activity-quote"], COST.quoteAmount))
    assert amount == quantity * rate == Decimal("42.50")


def test_cross_kind_activity_quote_needs_an_explicit_recipe(funding_data, schema) -> None:
    funding_data.set((FUND["activity-quote"], COST.appliesToActivityKind, FUND["raw-episode-kind"]))
    conforms, report = check(funding_data, schema)
    assert not conforms
    assert "quoted activity kinds" in report


def test_cross_unit_activity_quote_needs_an_explicit_recipe(funding_data, schema) -> None:
    funding_data.set((FUND["activity-quote"], COST.perUnit, FUND["episode-unit"]))
    conforms, report = check(funding_data, schema)
    assert not conforms
    assert "quoted activity units" in report


def test_explicit_activity_conversion_recipe_is_representable(funding_data, schema) -> None:
    funding_data.set((FUND["activity-quote"], COST.appliesToActivityKind, FUND["raw-episode-kind"]))
    funding_data.set((FUND["activity-quote"], COST.perUnit, FUND["episode-unit"]))
    funding_data.add((FUND["funding-line"], COST.valuationRecipe, Literal(
        "For this synthetic fixture only, a model maps the 2.50 weighted units to 2.50 "
        "equivalent episodes before applying the invented episode rate. No general "
        "equivalence or actual conversion calculation is established by this assertion."
    )))
    conforms, report = check(funding_data, schema)
    assert conforms, report


def test_resource_consumption_cannot_be_directly_priced_by_an_activity_quote(data, schema) -> None:
    data.remove((EX["staff-quote"], COST.appliesToResource, None))
    data.add((EX["staff-quote"], COST.appliesToActivityKind, EX["specimen-count-kind"]))
    conforms, report = check(data, schema)
    assert not conforms
    assert "XoneConstraintComponent" in report


def test_activity_to_resource_recipe_preserves_resource_quote_support(data, schema) -> None:
    data.remove((EX["batch-line"], COST.sourceResourceUse, None))
    data.add((EX["batch-line"], COST.sourceActivityMeasure, EX["specimen-count"]))
    data.add((EX["batch-line"], COST.valuationRecipe, Literal(
        "Two synthetic specimens consume one shared batch kit; value that one kit "
        "at the declared resource quote. The specimen count is not itself resource consumption."
    )))
    conforms, report = check(data, schema)
    assert conforms, report


def test_quote_cannot_simultaneously_target_resource_and_activity(funding_data, schema) -> None:
    funding_data.add((FUND["invented-resource"], RDF.type, COST.Resource))
    funding_data.add((FUND["activity-quote"], COST.appliesToResource, FUND["invented-resource"]))
    conforms, report = check(funding_data, schema)
    assert not conforms
    assert "XoneConstraintComponent" in report


def test_allocations_are_attributions_not_duplicate_expenses(data) -> None:
    source_total = sum(
        (Decimal(data.value(line, COST.lineAmount)) for line in data.objects(EX.ledger, COST.hasLine)),
        Decimal(0),
    )
    allocation_total = sum(
        (Decimal(data.value(allocation, COST.allocatedAmount))
         for allocation in data.objects(EX["batch-pool"], COST.hasAllocation)),
        Decimal(0),
    )
    query = (ROOT / "competency-questions/cq23-costing-infant-attribution.rq").read_text()
    rows = data.query(query)
    totals = {str(row.infant): Decimal(row.attributedAmount) for row in rows}
    assert source_total == Decimal("150.00")
    assert allocation_total == Decimal("100.00")
    assert totals == {str(EX["infant-a"]): Decimal("60.00"), str(EX["infant-b"]): Decimal("90.00")}
    assert sum(totals.values()) == source_total
    assert set(data.objects(EX["batch-1"], COST.hasMember)) == {EX["specimen-a"], EX["specimen-b"]}
    assert data.value(EX["confirmation-use"], COST.forCostObject) == EX["confirmation-b"]
    assert not list(Graph().query(query)), "An empty graph must not invent a zero-cost infant"


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("overallocated-batch", "conserve one whole pool"),
        ("wrong-allocation-amount", "stated share of its source pool"),
        ("duplicate-resource-line", "only once per component and scenario"),
        ("duplicate-resource-identity", "only once per component and scenario"),
        ("duplicate-pool", "two pools of the same ledger"),
        ("duplicate-recipient", "one consolidated allocation per recipient"),
        ("pool-amount-disagrees", "equal its component ledger lines"),
        ("resource-is-activity", "NotConstraintComponent"),
        ("activity-without-recipe", "XoneConstraintComponent"),
        ("negative-resource-use", "nonnegative decimal or exact rational"),
        ("mixed-currency", "Currency or valuation-basis conversion"),
        ("tariff-is-not-opportunity-cost", "Currency or valuation-basis conversion"),
        ("mixed-ledger-policy", "ledger's declared valuation policy"),
        ("unexplained-unit-conversion", "unit-conversion recipe"),
        ("empty-effective-interval", "LessThanConstraintComponent"),
        ("quote-known-after-release", "cannot become known after the release"),
        ("reported-without-evidence", "requires an evidence reference"),
        ("not-applicable-without-rationale", "requires an explicit rationale"),
        ("uncertainty-is-heterogeneity", "NotConstraintComponent"),
        ("payoff-without-transformation", "MinCountConstraintComponent"),
    ],
)
def test_semantically_invalid_changes_are_rejected(data, schema, case, message) -> None:
    if case == "overallocated-batch":
        data.set((EX["batch-to-a"], COST.allocationFraction, decimal("1.0")))
        data.set((EX["batch-to-a"], COST.allocatedAmount, decimal("100.0")))
    elif case == "wrong-allocation-amount":
        data.set((EX["batch-to-a"], COST.allocatedAmount, decimal("49.0")))
    elif case in {"duplicate-resource-line", "duplicate-resource-identity"}:
        clone_subject(data, EX["batch-line"], EX["duplicate-line"])
        data.add((EX.ledger, COST.hasLine, EX["duplicate-line"]))
        if case == "duplicate-resource-identity":
            clone_subject(data, EX["batch-use"], EX["duplicate-use"])
            data.set((EX["duplicate-line"], COST.sourceResourceUse, EX["duplicate-use"]))
    elif case == "duplicate-pool":
        clone_subject(data, EX["batch-pool"], EX["duplicate-pool"])
        data.remove((EX["duplicate-pool"], COST.hasAllocation, None))
        data.set((EX["duplicate-pool"], COST.unallocatedFraction, decimal("1.0")))
        data.set((EX["duplicate-pool"], COST.unallocatedAmount, decimal("100.0")))
    elif case == "duplicate-recipient":
        data.set((EX["batch-to-b"], COST.allocatedTo, EX["infant-a"]))
    elif case == "pool-amount-disagrees":
        data.set((EX["batch-pool"], COST.poolAmount, decimal("200.0")))
    elif case == "resource-is-activity":
        data.add((EX["batch-use"], RDF.type, COST.ActivityMeasure))
    elif case == "activity-without-recipe":
        data.remove((EX["batch-line"], COST.sourceResourceUse, None))
        data.add((EX["batch-line"], COST.sourceActivityMeasure, EX["specimen-count"]))
    elif case == "negative-resource-use":
        data.set((EX["collection-a-use"], COST.quantity, decimal("-1.0")))
    elif case == "mixed-currency":
        data.set((EX["staff-quote"], COST.currency, Literal("USD")))
    elif case == "tariff-is-not-opportunity-cost":
        data.set((EX["staff-quote"], COST.valuationBasis, COST["tariff-valuation"]))
        data.set((EX.policy, COST.valuationBasis, COST["economic-opportunity"]))
    elif case == "mixed-ledger-policy":
        clone_subject(data, EX.policy, EX["another-policy"])
        data.set((EX["collection-a-line"], COST.valuationPolicy, EX["another-policy"]))
    elif case == "unexplained-unit-conversion":
        data.set((EX["collection-a-use"], COST.unit, URIRef("http://qudt.org/vocab/unit/HR")))
    elif case == "empty-effective-interval":
        data.set((EX["staff-quote"], COST.effectiveTo, Literal("2026-01-01", datatype=XSD.date)))
    elif case == "quote-known-after-release":
        data.set((EX["staff-quote"], COST.knownFrom, Literal("2026-03-01T00:00:00Z", datatype=XSD.dateTime)))
    elif case == "reported-without-evidence":
        data.remove((EX["perspective-assertion"], COST.evidenceReference, None))
    elif case == "not-applicable-without-rationale":
        data.set((EX["family-time-assertion"], COST.applicability, Literal("not-applicable")))
    elif case == "uncertainty-is-heterogeneity":
        data.add((EX["rate-uncertainty"], RDF.type, COST.HeterogeneityDimension))
    elif case == "payoff-without-transformation":
        data.remove((EX["budget-bridge"], BRIDGE.valueTransformation, None))
    else:
        raise AssertionError(case)
    conforms, report = check(data, schema)
    assert not conforms, case
    assert message in report, report


def test_an_explicit_unallocated_residual_is_valid(data, schema) -> None:
    data.remove((EX["batch-pool"], COST.hasAllocation, EX["batch-to-b"]))
    data.remove((EX["batch-to-b"], None, None))
    data.set((EX["batch-pool"], COST.unallocatedFraction, decimal("0.5")))
    data.set((EX["batch-pool"], COST.unallocatedAmount, decimal("50.0")))
    conforms, report = check(data, schema)
    assert conforms, report


def test_an_entirely_unallocated_pool_is_valid(data, schema) -> None:
    data.remove((EX["batch-pool"], COST.hasAllocation, None))
    for allocation in (EX["batch-to-a"], EX["batch-to-b"]):
        data.remove((allocation, None, None))
    data.set((EX["batch-pool"], COST.unallocatedFraction, decimal("1.0")))
    data.set((EX["batch-pool"], COST.unallocatedAmount, decimal("100.0")))
    conforms, report = check(data, schema)
    assert conforms, report


def test_separate_scenarios_do_not_trigger_duplicate_consumption(data, schema) -> None:
    clone_subject(data, EX["batch-line"], EX["alternative-batch-line"])
    data.set((EX["alternative-batch-line"], COST.scenarioKey, Literal("sensitivity-scenario")))
    data.add((EX.ledger, COST.hasLine, EX["alternative-batch-line"]))
    conforms, report = check(data, schema)
    assert conforms, report


def rational_inputs(data: Graph) -> None:
    data.add((EX["one-third"], RDF.type, COST.RationalValue))
    data.add((EX["one-third"], COST.exactNumerator, Literal(1, datatype=XSD.integer)))
    data.add((EX["one-third"], COST.exactDenominator, Literal(3, datatype=XSD.positiveInteger)))
    data.remove((EX["collection-a-use"], COST.quantity, None))
    data.add((EX["collection-a-use"], COST.quantityExact, EX["one-third"]))
    data.remove((EX["staff-quote"], COST.quoteAmount, None))
    data.add((EX["staff-quote"], COST.quoteAmountExact, EX["one-third"]))
    for line, amount in ((EX["collection-a-line"], "0.11"),
                         (EX["collection-b-line"], "1.67"),
                         (EX["confirmation-line"], "5.00")):
        data.set((line, COST.lineAmount, decimal(amount)))
        data.add((line, COST.valuationRecipe, Literal("Multiply exact rational inputs, then round each line half-even to two decimal places in AUD. The ontology records this policy; it does not execute it.")))


def test_nonterminating_rational_inputs_do_not_require_decimal_approximations(data, schema) -> None:
    rational_inputs(data)
    conforms, report = check(data, schema)
    assert conforms, report
    assert data.value(EX["collection-a-use"], COST.quantity) is None
    assert data.value(EX["staff-quote"], COST.quoteAmount) is None


def test_rational_zero_denominator_is_rejected(data, schema) -> None:
    rational_inputs(data)
    data.set((EX["one-third"], COST.exactDenominator, Literal(0, datatype=XSD.positiveInteger)))
    conforms, report = check(data, schema)
    assert not conforms
    assert "exactDenominator" in report


def test_rational_to_decimal_boundary_must_be_declared(data, schema) -> None:
    rational_inputs(data)
    data.remove((EX["collection-a-line"], COST.valuationRecipe, None))
    conforms, report = check(data, schema)
    assert not conforms
    assert "conversion and rounding recipe" in report


def test_decimal_and_rational_measurements_cannot_conflict(data, schema) -> None:
    rational_inputs(data)
    data.add((EX["collection-a-use"], COST.quantity, decimal("0.3333333")))
    conforms, report = check(data, schema)
    assert not conforms
    assert "XoneConstraintComponent" in report


def test_costing_terms_do_not_inherit_game_or_payoff_semantics(schema) -> None:
    ontology, _ = schema
    for term in ontology.subjects(RDF.type, OWL.Class):
        if str(term).startswith(str(COST)):
            ancestors = set(ontology.transitive_objects(term, RDFS.subClassOf))
            assert not ancestors & {CORE.GameEntity, CORE.GameSpecification, CORE.Payoff}
    assert not list(ontology.triples((None, OWL.equivalentClass, None)))
    assert not list(ontology.triples((None, OWL.equivalentProperty, None)))
    assert (COST.ReportingDomain, RDFS.subClassOf, SKOS.Concept) in ontology
    for assessment in (COST.ReportingAssertion, COST.MethodologicalAssessment,
                       COST.ComputationalVerification, COST.EmpiricalValidation):
        assert (assessment, RDFS.subClassOf, COST.Assessment) in ontology


def test_all_new_terms_have_labels_definitions_and_context_mappings(schema) -> None:
    ontology, _ = schema
    context = json.loads((ROOT / "jsonld/costing-valuation.context.jsonld").read_text())["@context"]
    for kind in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty):
        for term in ontology.subjects(RDF.type, kind):
            if not str(term).startswith((str(COST), str(BRIDGE))):
                continue
            assert ontology.value(term, RDFS.label), term
            assert ontology.value(term, SKOS.definition), term
            local_name = str(term).split("#")[-1]
            assert local_name in context, term


def test_jsonld_context_preserves_exact_decimal_and_iri_types() -> None:
    context = json.loads((ROOT / "jsonld/costing-valuation.context.jsonld").read_text())["@context"]
    document = {
        "@context": context, "id": str(EX["jsonld-observation"]), "type": "ResourceUse",
        "quantity": "0.100000000000000000000001", "usesResource": str(EX["staff-time"]),
    }
    graph = Graph().parse(data=json.dumps(document), format="json-ld")
    quantity = graph.value(EX["jsonld-observation"], COST.quantity)
    assert quantity.datatype == XSD.decimal
    assert quantity.toPython() == Decimal("0.100000000000000000000001")
    assert graph.value(EX["jsonld-observation"], COST.usesResource) == EX["staff-time"]
