# CI Supply Chain Pinning Policy

Mutable CI inputs must be pinned to immutable versions whenever the provider supports it.

- GitHub Actions may use major-version tags only when the repository is already covered by GitHub's verified action provenance and the update is reviewed in a pull request.
- External source installs must use immutable commit pins. SourceRight is installed with `cargo install --git ... --rev f0c2c7c5dc9c2a25724e11985eb2b906d34c7c17`.
- Downloaded binary release artifacts must be pinned by URL and SHA-256. WIDOCO v1.4.25 uses the JDK 17 dependency JAR with SHA-256 `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`.
- Updating action tags, source pins, or artifact checksums requires a pull request that records the upstream release or commit, the reason for the update, and the local validation evidence.
