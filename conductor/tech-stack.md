# Technology Stack: UOGTO

- **Language**: Python 3.10+
- **Package & Environment Manager**: Pixi
- **Graph Framework**: rdflib
- **Validation**: pyshacl
- **Tests**: pytest
- **Linter/Formatter**: ruff
- **Automation & CI**: GitHub Actions and Custom Agent Skills
- **Scoping Review Libraries**: Python standard library (urllib, xml.etree)
- **Playground & Visualization**: Streamlit, NetworkX, Matplotlib

## Boundaries and optional integrations

- The default semantic package retains Python 3.10+ compatibility. External adapters
  may need newer interpreters; test their supported versions in separate optional
  jobs and pin the actual library revisions used.
- Paignia is the Rust provider for representations, strategic algorithms and solver
  diagnostics. Its versioned interchange must preserve full UOGTO IRIs and fixture
  identity. No Paignia package qualification is implied by the bootstrap README.
- Gambit, OpenSpiel, PettingZoo, PyCID and Open Game Engine are semantic comparators
  and planned optional integrations. They are not default runtime dependencies or
  certified adapters in this change.
- Kairos supplies optional simulation execution. Offline analysis and static
  semantic acceptance must not require it; dynamic strategic games can be analysed
  offline as well.
- SVG is the canonical comparison visual. Inkscape/ImageMagick provide optional
  derivative rendering; missing derivatives must remain visible in build outcomes.
- Current quality reports and historical publication snapshots have distinct paths
  and scopes. Record input hashes for new evidence and retain existing CI gates.
