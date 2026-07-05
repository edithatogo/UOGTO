# PRISMA-style systematic search and ontology enrichment flow

Broad source discovery, source-family screening, feature extraction, candidate mapping review, and conservative alignment outcomes for UOGTO.

```mermaid
flowchart TD
    N0["Search records/routes<br/>6 inclusion + 1 negative<br/>n=7"]
    N1["Article-hardening records<br/>identified and normalized<br/>n=39"]
    N2["Evidence sources retained<br/>for synthesis<br/>n=39"]
    N3["Comparative source<br/>families reviewed<br/>n=21 sources / 17 families"]
    N4["Terms normalized<br/>from UOGTO + sources<br/>n=4,046"]
    N5["Mapping candidates<br/>reviewed<br/>n=460"]
    N6["Accepted conservative<br/>alignments<br/>n=12"]
    N7["Rejected / non-asserted<br/>negative evidence<br/>n=448"]
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N5 -.-> N7
```
