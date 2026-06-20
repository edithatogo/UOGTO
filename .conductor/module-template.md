# Module Template

Use this template to add a new ontology module.

## 1. Ontology File (`ontologies/extensions/<name>.ttl`)
```turtle
@prefix uogtox: <https://w3id.org/uogto/extensions#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .

uogtox:MyClass a owl:Class ;
    rdfs:label "My Class"@en ;
    skos:definition "A template class description."@en .
```

## 2. SHACL Shape (`shapes/<name>.shacl.ttl`)
```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix uogtox: <https://w3id.org/uogto/extensions#> .

uogtox:MyClassShape a sh:NodeShape ;
    sh:targetClass uogtox:MyClass .
```

## 3. Example (`examples/<name>.ttl` or `.jsonld`)
Implement a minimal working example referencing `MyClass`.
