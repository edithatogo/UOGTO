# Systematic Scoping Review Protocol: UOGTO Validation and Coverage

## 1. Title
Systematic Scoping Review of Game Theory Formulations, Definitions, and Payoff Representations for the Universal Open Game Theory Ontology (UOGTO).

## 2. Objectives
This protocol describes the methodology for a systematic scoping review of game-theoretic academic literature to validate the comprehensiveness of UOGTO classes, properties, and mathematical alignments. The objectives are to:
1. Identify all historically documented game types, payoff structures, and strategy types.
2. Triangulate mathematical formulas, parameter bindings, and payoffs from literature.
3. Map coverage and detect gaps in the UOGTO ontology representation.

## 3. PRISMA-P Protocol Specifications

### 3.1 Eligibility Criteria
*   **Inclusion Criteria**: 
    *   Peer-reviewed articles, conference proceedings, preprints, and books describing game-theoretic architectures, classes of games, payoff matrices, transition systems, or equilibrium definitions.
    *   No restriction on publication year (going back to the founding publications of modern game theory up to the present day).
    *   No domain restrictions (covering mathematics, economics, computer science, biology, sociology, and political science).
*   **Exclusion Criteria**:
    *   Articles using game-theoretic terms purely as metaphors without mathematical or structural game descriptions.
    *   Duplicates, review outlines, or abstracts lacking structural specifications.

### 3.2 Information Sources
To ensure comprehensive scoping, the search queries the following indices and registries:
1.  **OpenAlex**: Open metadata catalog representing 250M+ scientific records (indexing Scopus, Web of Science, etc.).
2.  **PubMed / PMC**: Biomedical and life sciences index (capturing evolutionary and biological game theory).
3.  **Europe PMC**: Comprehensive life sciences partner.
4.  **arXiv**: Preprints in mathematics, physics, computer science, and quantitative biology.
5.  **Crossref**: DOI registry for academic papers, books, and conference proceedings.

---

## 4. PRISMA-S Search Strategy

### 4.1 Search Terms & Logic
Search strings utilize boolean operators targeting title, abstract, and keyword fields:

```text
("game theory" OR "game-theoretic" OR "normal-form game" OR "extensive-form game" OR "Markov game" OR "evolutionary game" OR "coalitional game" OR "mechanism design") AND ("payoff" OR "utility" OR "matrix" OR "action" OR "strategy" OR "regret" OR "equilibria")
```

### 4.2 Database Specific Formulations
*   **OpenAlex API**:
    ```text
    https://api.openalex.org/works?search=(title.search:"game theory" OR abstract.search:"game theory") AND (title.search:"payoff" OR title.search:"utility" OR title.search:"strategy")
    ```
*   **PubMed/NCBI Entrez**:
    ```text
    ("game theory"[Title/Abstract] OR "game-theoretic"[Title/Abstract] OR "Markov game"[Title/Abstract] OR "evolutionary game"[Title/Abstract]) AND ("payoff"[Title/Abstract] OR "utility"[Title/Abstract] OR "strategy"[Title/Abstract])
    ```
*   **arXiv API**:
    ```text
    http://export.arxiv.org/api/query?search_query=ti:%22game+theory%22+OR+abs:%22game+theory%22&max_results=1000
    ```

---

## 5. Screening & Selection Workflow
1.  **Deduplication**: Match and clean duplicate entries across databases based on DOIs, normalized titles, and author listings.
2.  **Active Learning Screening**:
    *   Train a text classification loop on a seed dataset (100 screened papers).
    *   Iteratively predict and prioritize the remaining records to isolate high-relevance papers.
3.  **NLP Extraction & Parsing**:
    *   Extract game definitions, payoffs, and structural variables from abstracts/texts.
    *   Parse mathematical equations formatted in LaTeX, MathML, Quarto, and Typst syntaxes.
4.  **Ontology Mapping (L2O Graph)**:
    *   Create a local temporary graph representing extracted literature nodes.
    *   Align L2O nodes with UOGTO classes using SPARQL mapping queries.
