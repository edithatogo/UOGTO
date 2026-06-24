"""Build ontology-quality benchmarking artifacts for the article-hardening track."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS
from pyshacl import validate as shacl_validate


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
DEFAULT_METRICS = DOCS / "quality-metrics.json"
DEFAULT_REPORT = DOCS / "reasoner-report.md"
UOGTO_CORE = "https://w3id.org/uogto/core#"
UOGTO_EXT = "https://w3id.org/uogto/extensions#"
SH = URIRef("http://www.w3.org/ns/shacl#")
SH_TARGET_CLASS = URIRef("http://www.w3.org/ns/shacl#targetClass")
SH_PATH = URIRef("http://www.w3.org/ns/shacl#path")
SH_NODE_SHAPE = URIRef("http://www.w3.org/ns/shacl#NodeShape")
SH_PROPERTY_SHAPE = URIRef("http://www.w3.org/ns/shacl#PropertyShape")
REGISTER_DATE = "2026-06-24"

CLASS_TYPES = {OWL.Class, RDFS.Class}
OBJECT_PROPERTY_TYPES = {OWL.ObjectProperty}
DATATYPE_PROPERTY_TYPES = {OWL.DatatypeProperty}
ANNOTATION_PROPERTY_TYPES = {OWL.AnnotationProperty}
PROPERTY_TYPES = {RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty}
DEFINITION_PREDICATES = {SKOS.definition, DCTERMS.description}
OWL_PROFILE_REVIEW_CONSTRUCTS = {
    OWL.unionOf,
    OWL.intersectionOf,
    OWL.complementOf,
    OWL.oneOf,
    OWL.hasKey,
    OWL.propertyChainAxiom,
    OWL.disjointUnionOf,
    OWL.cardinality,
    OWL.minCardinality,
    OWL.maxCardinality,
    OWL.qualifiedCardinality,
    OWL.minQualifiedCardinality,
    OWL.maxQualifiedCardinality,
}

REQUIRED_TOP_LEVEL = {
    "annotation_completeness",
    "orphan_classes",
    "relation_richness",
    "hierarchy_depth",
    "import_depth",
    "shacl_coverage",
    "examples_per_module",
    "competency_query_coverage",
    "owl_profile_reasoner_status",
    "pitfall_indicators",
}


def ttl_files() -> list[Path]:
    return sorted((ROOT / "ontologies").glob("**/*.ttl"))


def shape_files() -> list[Path]:
    return sorted((ROOT / "shapes").glob("*.ttl"))


def example_files() -> list[Path]:
    return sorted(path for path in (ROOT / "examples").glob("*") if path.suffix in {".ttl", ".jsonld"})


def query_files() -> list[Path]:
    return sorted((ROOT / "competency-questions").glob("*.rq"))


def parse_graph(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path, format="json-ld" if path.suffix == ".jsonld" else "turtle")
    return graph


def combined_graph(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        graph += parse_graph(path)
    return graph


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def module_id(path: Path) -> str:
    return path.relative_to(ROOT / "ontologies").with_suffix("").as_posix()


def is_named_uogto_term(term) -> bool:
    text = str(term)
    return isinstance(term, URIRef) and (text.startswith(UOGTO_CORE) or text.startswith(UOGTO_EXT))


def local_name(term: URIRef) -> str:
    text = str(term)
    if "#" in text:
        return text.rsplit("#", 1)[1]
    return text.rstrip("/").rsplit("/", 1)[-1]


def collect_defined_terms(module_graphs: dict[str, Graph]) -> tuple[dict[URIRef, set[str]], dict[str, dict[str, set[URIRef]]]]:
    term_modules: dict[URIRef, set[str]] = defaultdict(set)
    module_terms: dict[str, dict[str, set[URIRef]]] = {}
    for module, graph in module_graphs.items():
        classes = {
            subject
            for subject in graph.subjects(RDF.type, None)
            if is_named_uogto_term(subject) and any((subject, RDF.type, class_type) in graph for class_type in CLASS_TYPES)
        }
        object_properties = {
            subject
            for subject in graph.subjects(RDF.type, OWL.ObjectProperty)
            if is_named_uogto_term(subject)
        }
        datatype_properties = {
            subject
            for subject in graph.subjects(RDF.type, OWL.DatatypeProperty)
            if is_named_uogto_term(subject)
        }
        annotation_properties = {
            subject
            for subject in graph.subjects(RDF.type, OWL.AnnotationProperty)
            if is_named_uogto_term(subject)
        }
        rdf_properties = {
            subject for subject in graph.subjects(RDF.type, RDF.Property) if is_named_uogto_term(subject)
        }
        properties = object_properties | datatype_properties | annotation_properties | rdf_properties
        module_terms[module] = {
            "classes": classes,
            "object_properties": object_properties,
            "datatype_properties": datatype_properties,
            "annotation_properties": annotation_properties,
            "properties": properties,
        }
        for term in classes | properties:
            term_modules[term].add(module)
    return term_modules, module_terms


def has_definition(graph: Graph, term: URIRef) -> bool:
    return any((term, predicate, None) in graph for predicate in DEFINITION_PREDICATES)


def annotation_completeness(module_graphs: dict[str, Graph], module_terms: dict[str, dict[str, set[URIRef]]]) -> dict:
    modules = {}
    global_graph = Graph()
    global_classes = set()
    global_properties = set()
    for graph in module_graphs.values():
        global_graph += graph
    for module, terms in module_terms.items():
        graph = module_graphs[module]
        classes = terms["classes"]
        properties = terms["properties"]
        entities = classes | properties
        labelled = {term for term in entities if (term, RDFS.label, None) in graph}
        defined = {term for term in entities if has_definition(graph, term)}
        modules[module] = {
            "class_count": len(classes),
            "property_count": len(properties),
            "entity_count": len(entities),
            "labelled_count": len(labelled),
            "defined_count": len(defined),
            "label_completeness": round(len(labelled) / len(entities), 4) if entities else 1.0,
            "definition_completeness": round(len(defined) / len(entities), 4) if entities else 1.0,
            "missing_labels": sorted(str(term) for term in entities - labelled),
            "missing_definitions": sorted(str(term) for term in entities - defined),
        }
        global_classes |= classes
        global_properties |= properties
    global_entities = global_classes | global_properties
    global_labelled = {term for term in global_entities if (term, RDFS.label, None) in global_graph}
    global_defined = {term for term in global_entities if has_definition(global_graph, term)}
    return {
        "global": {
            "class_count": len(global_classes),
            "property_count": len(global_properties),
            "entity_count": len(global_entities),
            "labelled_count": len(global_labelled),
            "defined_count": len(global_defined),
            "label_completeness": round(len(global_labelled) / len(global_entities), 4) if global_entities else 1.0,
            "definition_completeness": round(len(global_defined) / len(global_entities), 4) if global_entities else 1.0,
        },
        "modules": modules,
    }


def subclass_edges(graph: Graph, classes: set[URIRef]) -> dict[URIRef, set[URIRef]]:
    edges: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent in graph.subject_objects(RDFS.subClassOf):
        if child in classes and isinstance(parent, URIRef) and parent in classes and child != parent:
            edges[child].add(parent)
    return edges


def orphan_classes(graph: Graph, classes: set[URIRef]) -> dict:
    edges = subclass_edges(graph, classes)
    parents = {parent for values in edges.values() for parent in values}
    children = set(edges)
    orphans = sorted(classes - parents - children, key=str)
    return {
        "count": len(orphans),
        "class_count": len(classes),
        "orphan_ratio": round(len(orphans) / len(classes), 4) if classes else 0.0,
        "classes": [str(term) for term in orphans],
    }


def hierarchy_depth(graph: Graph, classes: set[URIRef]) -> dict:
    parents = subclass_edges(graph, classes)
    children: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent_set in parents.items():
        for parent in parent_set:
            children[parent].add(child)
    roots = sorted((classes - set(parents)) | {parent for parent in children if parent not in parents}, key=str)
    depths = {root: 0 for root in roots}
    queue = deque(roots)
    while queue:
        node = queue.popleft()
        for child in children.get(node, set()):
            next_depth = depths[node] + 1
            if next_depth > depths.get(child, -1):
                depths[child] = next_depth
                queue.append(child)
    max_depth = max(depths.values(), default=0)
    depth_counts = Counter(depths.values())
    return {
        "max_depth": max_depth,
        "root_class_count": len(roots),
        "root_classes": [str(term) for term in roots[:50]],
        "depth_distribution": {str(depth): count for depth, count in sorted(depth_counts.items())},
    }


def relation_richness(graph: Graph, classes: set[URIRef], properties: set[URIRef]) -> dict:
    object_properties = {term for term in properties if (term, RDF.type, OWL.ObjectProperty) in graph}
    datatype_properties = {term for term in properties if (term, RDF.type, OWL.DatatypeProperty) in graph}
    annotation_properties = {term for term in properties if (term, RDF.type, OWL.AnnotationProperty) in graph}
    subclass_count = sum(1 for _ in graph.triples((None, RDFS.subClassOf, None)))
    domain_count = sum(1 for prop in properties if (prop, RDFS.domain, None) in graph)
    range_count = sum(1 for prop in properties if (prop, RDFS.range, None) in graph)
    non_annotation_property_count = len(object_properties | datatype_properties | (properties - annotation_properties))
    return {
        "class_count": len(classes),
        "property_count": len(properties),
        "object_property_count": len(object_properties),
        "datatype_property_count": len(datatype_properties),
        "annotation_property_count": len(annotation_properties),
        "subclass_axiom_count": subclass_count,
        "domain_coverage": round(domain_count / len(properties), 4) if properties else 0.0,
        "range_coverage": round(range_count / len(properties), 4) if properties else 0.0,
        "properties_per_class": round(non_annotation_property_count / len(classes), 4) if classes else 0.0,
        "subclass_axioms_per_class": round(subclass_count / len(classes), 4) if classes else 0.0,
    }


def ontology_imports(module_graphs: dict[str, Graph]) -> dict:
    ontology_to_module = {}
    imports_by_module = {}
    for module, graph in module_graphs.items():
        ontology_iris = [subject for subject in graph.subjects(RDF.type, OWL.Ontology) if isinstance(subject, URIRef)]
        ontology = ontology_iris[0] if ontology_iris else URIRef(f"https://w3id.org/uogto/module/{module}")
        ontology_to_module[str(ontology)] = module
        imports_by_module[module] = [str(obj) for obj in graph.objects(ontology, OWL.imports) if isinstance(obj, URIRef)]

    def depth(module: str, seen: set[str]) -> int:
        if module in seen:
            return 0
        local_import_modules = [ontology_to_module[iri] for iri in imports_by_module[module] if iri in ontology_to_module]
        if not local_import_modules:
            return 0
        return 1 + max(depth(imported, seen | {module}) for imported in local_import_modules)

    module_depths = {module: depth(module, set()) for module in imports_by_module}
    external_imports = sorted(
        {
            iri
            for imports in imports_by_module.values()
            for iri in imports
            if iri not in ontology_to_module
        }
    )
    return {
        "max_local_import_depth": max(module_depths.values(), default=0),
        "modules": {
            module: {"local_import_depth": module_depths[module], "imports": imports_by_module[module]}
            for module in sorted(imports_by_module)
        },
        "external_import_count": len(external_imports),
        "external_imports": external_imports,
    }


def shacl_coverage(all_graph: Graph, shacl_graph: Graph, classes: set[URIRef], properties: set[URIRef]) -> dict:
    target_classes = {obj for obj in shacl_graph.objects(None, SH_TARGET_CLASS) if isinstance(obj, URIRef)}
    paths = {obj for obj in shacl_graph.objects(None, SH_PATH) if isinstance(obj, URIRef)}
    node_shapes = set(shacl_graph.subjects(RDF.type, SH_NODE_SHAPE))
    property_shapes = set(shacl_graph.subjects(RDF.type, SH_PROPERTY_SHAPE))
    class_targets_in_ontology = target_classes & classes
    property_paths_in_ontology = paths & properties
    return {
        "shape_file_count": len(shape_files()),
        "node_shape_count": len(node_shapes),
        "property_shape_count": len(property_shapes),
        "target_class_count": len(target_classes),
        "target_class_coverage": round(len(class_targets_in_ontology) / len(classes), 4) if classes else 0.0,
        "target_classes_missing_from_ontology": sorted(str(term) for term in target_classes - classes),
        "property_path_count": len(paths),
        "property_path_coverage": round(len(property_paths_in_ontology) / len(properties), 4) if properties else 0.0,
        "property_paths_missing_from_ontology": sorted(str(term) for term in paths - properties),
    }


def load_examples() -> tuple[dict[str, Graph], Graph]:
    examples = {}
    combined = Graph()
    for path in example_files():
        graph = parse_graph(path)
        examples[rel(path)] = graph
        combined += graph
    return examples, combined


def examples_per_module(
    example_graphs: dict[str, Graph],
    term_modules: dict[URIRef, set[str]],
    module_terms: dict[str, dict[str, set[URIRef]]],
) -> dict:
    module_examples: dict[str, set[str]] = defaultdict(set)
    example_terms = {}
    for example, graph in example_graphs.items():
        terms = {term for term in graph.predicates() if is_named_uogto_term(term)}
        terms |= {term for term in graph.objects(None, RDF.type) if is_named_uogto_term(term)}
        example_terms[example] = sorted(str(term) for term in terms)
        for term in terms:
            for module in term_modules.get(term, set()):
                module_examples[module].add(example)
    modules = {}
    for module in sorted(module_terms):
        modules[module] = {
            "example_count": len(module_examples[module]),
            "examples": sorted(module_examples[module]),
        }
    return {
        "example_count": len(example_graphs),
        "modules_with_examples": sum(1 for examples in module_examples.values() if examples),
        "modules": modules,
        "example_terms": example_terms,
    }


def mentioned_query_terms(query_text: str) -> set[str]:
    terms = set()
    for prefix, base in [("uogto", UOGTO_CORE), ("uogtox", UOGTO_EXT)]:
        for match in re.finditer(rf"\b{prefix}:([A-Za-z_][A-Za-z0-9_\-]*)", query_text):
            terms.add(base + match.group(1))
    for match in re.finditer(r"<(https://w3id\.org/uogto/(?:core|extensions)#[^>]+)>", query_text):
        terms.add(match.group(1))
    return terms


def competency_query_coverage(
    ontology_graph: Graph,
    ontology_and_examples: Graph,
    term_modules: dict[URIRef, set[str]],
) -> dict:
    records = []
    module_hits: dict[str, set[str]] = defaultdict(set)
    executable = 0
    with_example_results = 0
    for path in query_files():
        query_text = path.read_text(encoding="utf-8")
        record = {"query": rel(path), "terms": sorted(mentioned_query_terms(query_text))}
        try:
            ontology_results = ontology_graph.query(query_text)
            example_results = ontology_and_examples.query(query_text)
            record["status"] = "executable"
            record["ontology_result_count"] = len(ontology_results)
            record["ontology_plus_examples_result_count"] = len(example_results)
            executable += 1
            if len(example_results):
                with_example_results += 1
        except Exception as exc:  # pragma: no cover - failure path is validated by repo tests.
            record["status"] = "failed"
            record["error"] = str(exc)
            record["ontology_result_count"] = None
            record["ontology_plus_examples_result_count"] = None
        modules = set()
        for iri in record["terms"]:
            for module in term_modules.get(URIRef(iri), set()):
                modules.add(module)
                module_hits[module].add(rel(path))
        record["modules"] = sorted(modules)
        records.append(record)
    return {
        "query_count": len(records),
        "executable_count": executable,
        "executable_ratio": round(executable / len(records), 4) if records else 1.0,
        "queries_with_example_results": with_example_results,
        "module_coverage_count": len(module_hits),
        "modules": {module: sorted(paths) for module, paths in sorted(module_hits.items())},
        "queries": records,
    }


def pitfall_indicators(metrics: dict) -> dict:
    annotation = metrics["annotation_completeness"]["global"]
    relation = metrics["relation_richness"]
    shacl = metrics["shacl_coverage"]
    imports = metrics["import_depth"]
    reasoner = metrics["owl_profile_reasoner_status"]
    indicators = {
        "missing_labels": annotation["entity_count"] - annotation["labelled_count"],
        "missing_definitions": annotation["entity_count"] - annotation["defined_count"],
        "orphan_classes": metrics["orphan_classes"]["count"],
        "properties_without_domain": round((1 - relation["domain_coverage"]) * relation["property_count"]),
        "properties_without_range": round((1 - relation["range_coverage"]) * relation["property_count"]),
        "shacl_uncovered_class_count": round((1 - shacl["target_class_coverage"]) * annotation["class_count"]),
        "external_import_count": imports["external_import_count"],
        "reasoner_not_passed": reasoner["reasoner"]["owlrl_status"] != "passed",
    }
    return {
        "method": "local OOPS-style proxy indicators; no external OOPS service was called",
        "indicators": indicators,
        "open_issue_count": sum(1 for value in indicators.values() if value),
    }


def owl_profile_reasoner_status(graph: Graph, shacl_graph: Graph, examples_graph: Graph) -> dict:
    constructs = {
        str(predicate): sum(1 for _ in graph.triples((None, predicate, None)))
        for predicate in OWL_PROFILE_REVIEW_CONSTRUCTS
    }
    constructs = {predicate: count for predicate, count in constructs.items() if count}
    profile_status = "owl2_rl_candidate_syntactic_subset" if not constructs else "requires_manual_profile_review"
    reasoner_status = {
        "owlrl_available": False,
        "owlrl_status": "skipped",
        "owlrl_triples_before": len(graph),
        "owlrl_triples_after": None,
        "owlrl_error": None,
    }
    try:
        from owlrl import DeductiveClosure, OWLRL_Semantics

        closure_graph = Graph()
        for triple in graph:
            closure_graph.add(triple)
        DeductiveClosure(OWLRL_Semantics).expand(closure_graph)
        reasoner_status.update(
            {
                "owlrl_available": True,
                "owlrl_status": "passed",
                "owlrl_triples_after": len(closure_graph),
            }
        )
    except Exception as exc:
        reasoner_status.update({"owlrl_error": str(exc)})

    conforms, _, results_text = shacl_validate(
        graph + examples_graph,
        shacl_graph=shacl_graph,
        ont_graph=graph,
        inference="rdfs",
    )
    return {
        "rdf_parse_status": "passed",
        "owl_profile_screen": {
            "method": "local syntactic screen for constructs that require manual OWL profile review",
            "status": profile_status,
            "review_construct_counts": constructs,
        },
        "reasoner": reasoner_status,
        "pyshacl_examples_rdfs_status": "passed" if conforms else "failed",
        "pyshacl_results_text": "" if conforms else results_text,
    }


def build_metrics() -> dict:
    module_paths = ttl_files()
    module_graphs = {module_id(path): parse_graph(path) for path in module_paths}
    ontology_graph = Graph()
    for graph in module_graphs.values():
        ontology_graph += graph
    shacl_graph = combined_graph(shape_files())
    example_graphs, examples_graph = load_examples()
    ontology_and_examples = ontology_graph + examples_graph
    term_modules, module_terms = collect_defined_terms(module_graphs)
    all_classes = {term for terms in module_terms.values() for term in terms["classes"]}
    all_properties = {term for terms in module_terms.values() for term in terms["properties"]}
    metrics = {
        "schema": "uogto.article-hardening.quality-metrics.v1",
        "created": REGISTER_DATE,
        "scope": {
            "ontology_file_count": len(module_paths),
            "shape_file_count": len(shape_files()),
            "example_file_count": len(example_files()),
            "competency_query_count": len(query_files()),
        },
        "annotation_completeness": annotation_completeness(module_graphs, module_terms),
        "orphan_classes": orphan_classes(ontology_graph, all_classes),
        "relation_richness": relation_richness(ontology_graph, all_classes, all_properties),
        "hierarchy_depth": hierarchy_depth(ontology_graph, all_classes),
        "import_depth": ontology_imports(module_graphs),
        "shacl_coverage": shacl_coverage(ontology_graph, shacl_graph, all_classes, all_properties),
        "examples_per_module": examples_per_module(example_graphs, term_modules, module_terms),
        "competency_query_coverage": competency_query_coverage(
            ontology_graph, ontology_and_examples, term_modules
        ),
        "owl_profile_reasoner_status": owl_profile_reasoner_status(
            ontology_graph, shacl_graph, examples_graph
        ),
    }
    metrics["pitfall_indicators"] = pitfall_indicators(metrics)
    return metrics


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(path: Path, metrics: dict) -> None:
    ann = metrics["annotation_completeness"]["global"]
    orphan = metrics["orphan_classes"]
    relation = metrics["relation_richness"]
    hierarchy = metrics["hierarchy_depth"]
    imports = metrics["import_depth"]
    shacl = metrics["shacl_coverage"]
    examples = metrics["examples_per_module"]
    queries = metrics["competency_query_coverage"]
    reasoner = metrics["owl_profile_reasoner_status"]
    lines = [
        "# UOGTO Ontology-Quality and Reasoner Benchmark",
        "",
        "This report is generated from `scripts/maintenance/build_article_hardening_quality.py`.",
        "",
        "## Scope",
        "",
        f"- Ontology files: {metrics['scope']['ontology_file_count']}",
        f"- SHACL files: {metrics['scope']['shape_file_count']}",
        f"- Example files: {metrics['scope']['example_file_count']}",
        f"- Competency queries: {metrics['scope']['competency_query_count']}",
        "",
        "## Annotation Completeness",
        "",
        f"- Classes: {ann['class_count']}",
        f"- Properties: {ann['property_count']}",
        f"- Label completeness: {ann['label_completeness']}",
        f"- Definition completeness: {ann['definition_completeness']}",
        "",
        "## Structural Metrics",
        "",
        f"- Orphan classes: {orphan['count']} of {orphan['class_count']} ({orphan['orphan_ratio']})",
        f"- Object properties: {relation['object_property_count']}",
        f"- Datatype properties: {relation['datatype_property_count']}",
        f"- Relation richness, properties per class: {relation['properties_per_class']}",
        f"- Domain coverage: {relation['domain_coverage']}",
        f"- Range coverage: {relation['range_coverage']}",
        f"- Maximum class hierarchy depth: {hierarchy['max_depth']}",
        f"- Root classes: {hierarchy['root_class_count']}",
        f"- Maximum local import depth: {imports['max_local_import_depth']}",
        f"- External import count: {imports['external_import_count']}",
        "",
        "## SHACL and Example Coverage",
        "",
        f"- SHACL target class coverage: {shacl['target_class_coverage']}",
        f"- SHACL property path coverage: {shacl['property_path_coverage']}",
        f"- Modules with examples: {examples['modules_with_examples']}",
        f"- Example files: {examples['example_count']}",
        "",
        "## Competency Query Coverage",
        "",
        f"- Executable queries: {queries['executable_count']} of {queries['query_count']}",
        f"- Queries returning results against ontology plus examples: {queries['queries_with_example_results']}",
        f"- Modules mentioned by competency queries: {queries['module_coverage_count']}",
        "",
        "## Pitfall Indicators",
        "",
        f"- Local OOPS-style open issue count: {metrics['pitfall_indicators']['open_issue_count']}",
        f"- Missing labels: {metrics['pitfall_indicators']['indicators']['missing_labels']}",
        f"- Missing definitions: {metrics['pitfall_indicators']['indicators']['missing_definitions']}",
        "",
        "## OWL Profile and Reasoner Status",
        "",
        f"- RDF parse status: {reasoner['rdf_parse_status']}",
        f"- OWL profile screen: {reasoner['owl_profile_screen']['status']}",
        f"- OWL profile screen method: {reasoner['owl_profile_screen']['method']}",
        f"- OWL RL reasoner status: {reasoner['reasoner']['owlrl_status']}",
        f"- OWL RL available: {reasoner['reasoner']['owlrl_available']}",
        f"- PySHACL RDFS example status: {reasoner['pyshacl_examples_rdfs_status']}",
        "",
        "## Limitations",
        "",
        "The OWL profile check is a deterministic local syntactic screen, not a formal certification by an external OWL profile reasoner. Metrics are intended for article reporting, regression checks, and prioritising ontology improvements.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_metrics(metrics: dict) -> dict:
    if metrics.get("schema") != "uogto.article-hardening.quality-metrics.v1":
        raise AssertionError("Unexpected quality metrics schema")
    missing = sorted(REQUIRED_TOP_LEVEL - set(metrics))
    if missing:
        raise AssertionError("Quality metrics missing sections: " + ", ".join(missing))
    ann = metrics["annotation_completeness"]["global"]
    if ann["class_count"] <= 0 or ann["property_count"] <= 0:
        raise AssertionError("Quality metrics must count classes and properties")
    for field in ["label_completeness", "definition_completeness"]:
        if not 0 <= ann[field] <= 1:
            raise AssertionError(f"Invalid annotation completeness ratio: {field}")
    if metrics["hierarchy_depth"]["max_depth"] < 1:
        raise AssertionError("Hierarchy depth should detect subclass structure")
    if metrics["competency_query_coverage"]["executable_count"] != metrics["scope"]["competency_query_count"]:
        raise AssertionError("All competency queries must execute")
    if metrics["owl_profile_reasoner_status"]["rdf_parse_status"] != "passed":
        raise AssertionError("RDF parse status must pass")
    return {
        "classes": ann["class_count"],
        "properties": ann["property_count"],
        "queries": metrics["competency_query_coverage"]["query_count"],
        "examples": metrics["examples_per_module"]["example_count"],
    }


def build_outputs(metrics_path: Path, report_path: Path) -> dict:
    metrics = build_metrics()
    write_json(metrics_path, metrics)
    write_report(report_path, metrics)
    return validate_metrics(metrics)


def check_outputs(metrics_path: Path, report_path: Path) -> dict:
    if not report_path.exists():
        raise AssertionError(f"Missing reasoner report: {report_path}")
    metrics = read_json(metrics_path)
    report = report_path.read_text(encoding="utf-8")
    for section in [
        "## Annotation Completeness",
        "## Structural Metrics",
        "## SHACL and Example Coverage",
        "## Competency Query Coverage",
        "## Pitfall Indicators",
        "## OWL Profile and Reasoner Status",
    ]:
        if section not in report:
            raise AssertionError(f"Reasoner report missing section: {section}")
    return validate_metrics(metrics)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or validate article-hardening ontology quality metrics.")
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    summary = check_outputs(args.metrics, args.report) if args.check_only else build_outputs(args.metrics, args.report)
    print(
        "Article-hardening quality metrics valid: "
        f"{summary['classes']} classes, {summary['properties']} properties, "
        f"{summary['examples']} examples, {summary['queries']} competency queries."
    )


if __name__ == "__main__":
    main()
