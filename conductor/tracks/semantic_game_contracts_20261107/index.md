# Versioned semantic contracts for Paignia

Status: in progress; SGC.07 reference-tool labels implemented; seven leaves pending.

- [Specification](./spec.md)
- [Implementation plan](./plan.md)
- [Metadata](./metadata.json)
- [Existing interoperability track](../uogto_interoperability_benchmarks_20260705/index.md)
- [Existing modelling decisions](../../../docs/modelling-decisions.md)
- [Paignia provider repository](https://github.com/edithatogo/paignia) (T17 transfer and qualification remain provider-owned)
- [Existing Paignia semantic handoff](https://github.com/edithatogo/UOGTO/issues/123)

This track supplies semantic contracts and conformance evidence. It does not
replace provider qualification, implement a simulation core, change published
IRIs, or promote historical completion into new runtime evidence.

Paignia is the chosen library name and its repository has been created. The
renamed `paignia-core`/`paignia-solve` seed is transferring there from the
reimbursement-game incubator; publication and provider qualification remain
pending. The eight SGC leaves
remain the implementation authority here, including separate static and dynamic
receipt scopes. UOGTO retains ontology, profile and conformance ownership.

## Strategic information integration — 8 November 2026

- [Owner-scoped roadmap and acceptance cases](strategic-information-integration.md).
  Planning only; existing implementation statuses, pins and release gates remain unchanged.

The November reconciliation implements SGC.07 with tested reference-origin labels.
The remaining seven leaves and both SGC.08 receipt scopes remain pending. Static
semantic acceptance denotes offline interchange, independently of whether the
model is a `StaticGame` or a `DynamicGame`.
