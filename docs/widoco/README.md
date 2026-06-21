# WIDOCO Documentation

UOGTO publishes human-readable ontology documentation with WIDOCO after the ontology build and validation gates pass.

## Canonical Input
Documentation is generated from `dist/uogto.ttl`, the merged ontology artifact produced by:

```bash
make build
```

Using the merged artifact keeps WIDOCO output aligned with the release artifact that is cited, archived, and submitted to registries. Individual module files remain the authoritative source files under `ontologies/`.

## Local Build
1. Install Java 17 or later.
2. Build the merged ontology:
   ```bash
   make build
   ```
3. Download a WIDOCO release JAR from <https://github.com/dgarijo/Widoco/releases>.
4. Generate documentation:
   ```bash
   java -jar widoco.jar -ontFile dist/uogto.ttl -outFolder site -rewriteAll -getOntologyMetadata -webVowl -uniteSections
   ```

The generated HTML should be written to `site/`.

## CI/CD
`.github/workflows/widoco-pages.yml` builds `dist/uogto.ttl`, downloads the latest WIDOCO JAR from GitHub releases, generates `site/`, and deploys the result to GitHub Pages.
