# UOGTO PR #128: independent costing receiving review and close-out

**Review date:** 20 November 2026 (Australia/Brisbane). **Disposition:** independent review evidence complete; **PR #128 blocked/returned to the existing costing writer**, not accepted or merged. **Receiving acknowledgement requested, not yet established.** This file is evidence in a *separate review lane*, not a change to the writer's costing ontology, queries, tests, source-import pipeline, track status or shared Conductor registry.

## Follow-through — 28 November 2026 (Australia/Brisbane)

**Current disposition:** the reviewer-owned qualification increment is verified
and ready for publication. The existing costing writer's CQ21/CQ23 fixes and
receiving acknowledgement remain pending. Combined CQ integration and admission
remain with the existing integrator. The recovery hold tracked in #134 remains
in force; this review lane is not archived. The earlier dated sections below are
preserved historical records, not the current main or current acceptance state.

### Complete fixtures qualify the historical counterexamples

The new [standalone diagnostic](check_shape_qualified_cq21_cq23.py) starts from
the writer's complete, synthetic newborn fixture at PR128
`7e9075b8fd77543fc8853fab20319415cb86597d`. It requires exact Git blobs for the
fixture, three costing/HTA ontologies, two costing/HTA shape files and CQ21/CQ23.
All eight identities are recorded in the [full execution receipt](shape-qualified-results-20261128.json).
Validation uses RDFS inference, no remote OWL imports and `inplace=False`;
queries then run against the asserted fixture, not an inference-expanded graph.
This matches the scope of the writer's costing/HTA test schema. It is not a
claim that every repository shape or the combined integration tree was tested.

| Case | Asserted triples | Costing/HTA SHACL result | Original query observation |
| --- | ---: | --- | --- |
| Unchanged baseline | 241 | Conforms | CQ21: allocated 100, residual 0, recipients 2; CQ23: A=60, B=90 |
| Fully unallocated pool | 229 | Conforms | CQ21: allocated total and recipient count unbound; expected 0 and 0, residual 100 |
| Alternative direct valuation | 249 | Conforms | CQ23: A=70, B=90; the alternative 10 is mixed into baseline A=60 |
| Alternative pooled valuation | 269 | Conforms | CQ23: A=110, B=140; alternative 50/50 is mixed into baseline 60/90 |
| Alternative pool line missing its scenario | 268 | Rejected as intended | Exact line/scenarioKey/MinCount violation confirmed; no query correctness claim |

The zero-allocation mutation updates both residual amount and fraction and
removes the allocation subjects and pool links. Alternative scenarios clone
complete existing lines, pools and allocations, retaining the original quote,
quantity and valuation amounts. Pool membership and reciprocal allocation links
are rewired consistently. Consequently the new results differ numerically from
the old sparse 7-unit/120-unit diagnostic; neither receipt is relabelled.

The fresh run has **5/5 shape expectations satisfied, 2 query checks passed and
3 query checks failed, exit 1**. Full IRIs, datatypes, unbound values and complete
result rows are retained without collapsing duplicate rows into dictionaries.
Baseline invariance under an alternative scenario is a diagnostic of the pinned
queries; the writer still owns the choice between selected-scenario and grouped
scenario output. Changed inputs are rejected before execution, so this helper
cannot qualify future corrected queries. The original sparse helper/log remain
unchanged. The [guard-check log](shape-qualified-checks-20261128.txt) records all
eight changed-input rejections and the absence of an optional pin bypass.

```shell
python conductor/reviews/pr128-independent-costing-20261120/check_shape_qualified_cq21_cq23.py \
  --source-root PATH_TO_ORIGINAL_PR128_CHECKOUT
# Exit 1: the historical query defects remain present.
# Exit 2: an input pin or the shape-qualification premise failed.
```

Ponytail's independent replay reproduced the complete JSON receipt exactly and
verified all eight source guards. No correctness blocker was found; complexity
verdict: **Lean already. Ship.** Local `make validate`, targeted Ruff and
`py_compile` passed. Local `make test` passed: **453 passed, 1 skipped, 24,707
warnings, 65.41 s** on receiving main plus these review files. The normal suite
does not collect this standalone historical diagnostic. Hosted results are
recorded with publication, without treating the historical failures as green.

### Actual receiving-main checks after the earlier merges

The prior review and bounded maintenance changes are now on main:
[PR138 / c00301f](https://github.com/edithatogo/UOGTO/commit/c00301ffd7ad3843fcd3bcf40eb93485ea602d48),
[PR110 / 1d672af](https://github.com/edithatogo/UOGTO/commit/1d672af8179428abb340db266d5cacf1d594f277), and
[PR114 / 82364d9](https://github.com/edithatogo/UOGTO/commit/82364d9fee2614ecac02d1ab8a945854c6116aa3).
All seven push workflows on actual receiving main `82364d9` succeeded.
[Validate UOGTO](https://github.com/edithatogo/UOGTO/actions/runs/46082992680)
ran `make all`: **453 passed, 1 skipped, 24,707 warnings, 83.35 s**.
[Required Gate](https://github.com/edithatogo/UOGTO/actions/runs/46082992804)
also ran validation/tests: **453 passed, 1 skipped, 24,707 warnings, 86.92 s**,
plus its native-profile and manuscript checks. These are receiving-main results,
not just historical pull-request checks.

The main manifest still executes 22 expectations: CQ01–20, CQ25 and CQ26.
CQ25 returns 4 expected rows; CQ26 returns 16. CQ21–24 remain in unmerged PR128.
The requested combined CQ01–25 acceptance must retain CQ26 and execute the actual
26-query integrated commit. That integration has not been performed by this lane.
[Privacy push run](https://github.com/edithatogo/UOGTO/actions/runs/46082992850)
passed for its changed-file scope (one file); it does not resolve the earlier
full-scope scheduled failure routed under #107.

### Receiving dependency and next owned work

The existing [PR128 handoff](https://github.com/edithatogo/UOGTO/pull/128#issuecomment-7229938074)
remains the concrete routing surface for the costing track owner and integrator
conversation `6af96da1-c088-83ec-85a8-ab19f5f4512c`. The PR128 and linked MCHS411
records identify the maintainer account but no distinct writer contact. There
is still no express writer or integrator acknowledgement. Publishing a request
or an independent review is not that acknowledgement.

The next writer-owned work is the CQ21/CQ23 correction with zero/partial/full,
scenario-isolation and malformed-provenance regressions; next integrator-owned
work is combined CQ01–26 verification. This increment advances the first research
recommendation with shape-qualified evidence. Native round trips and held-out
semantic-loss experiments remain proposals for the existing SGC/Paignia and
FRT/MAT owners, without an achieved frontier claim or a new shared track.

## Earlier review amendment — 28 November 2026 (Australia/Brisbane)

The sections below retain the 20 November evidence; this amendment records the
current review. Main has advanced to `b3f1de0119ee1c1e49913d9c1f9284e053e43433`.
PR128 remains at `7e9075b8fd77543fc8853fab20319415cb86597d`, conflicted, and the
writer/integrator acknowledgement is still absent. The [renewed receiving
request](https://github.com/edithatogo/UOGTO/pull/128#issuecomment-7229938074)
preserves the existing writer and integrator assignments. No costing fix,
combined-tree acceptance, source recovery or archive action is claimed.

### Ponytail and correctness review

The complexity review found no unnecessary abstraction or dependency in the
compact reproducer. A separate correctness review found that its infant-keyed
CQ23 dictionaries would overwrite separate scenario rows from a future corrected
query. That could give order-dependent false passes or failures. The smallest
sound correction is to remove the optional hash bypass and require the two
original Git blobs on every run. This is now a historical reproducer only.
Future acceptance belongs to the writer's chosen scenario contract and must
preserve scenario identity and row multiplicity. The original 20 November log
and its old command remain historical evidence, not instructions for the updated
script.

Fresh local checks on current main plus these review changes used CPython
3.15.2, RDFLib 7.6.0, PySHACL 0.40.2 and pytest 9.2.0:

| Executed check | Observed result | Scope |
| --- | --- | --- |
| `make all` (`build`, `validate`, `test`, `coverage`) | Pass; 453 passed, 1 skipped, 24,707 warnings, pytest 65.44 s | Current main plus review files; excludes unmerged CQ21–24 |
| `scripts/maintenance/audit_semantics.py` | Pass; 55 ontology files | Current review tree |
| Updated historical reproducer | 2 baseline passes, 3 failures, exit 1 | Unchanged original PR128 CQ21/CQ23 blobs |
| Changed-query rejection | Both CQ21 and CQ23 mutations rejected before semantic execution | Mandatory original-byte guard |
| `python -m py_compile` | Pass | Updated reproducer |
| `git diff --check` | Pass | Review changes |

The compact run and guard results are in `review-checks-20261128.txt`. The
intentional semantic failures remain writer-owned defects; they are not waived
by the passing main-based suite. No new SHACL claim is made for the compact
diagnostic fixture. Fresh hosted checks and any merge result are recorded in
PR138 against the resulting remote head; historical checks are not relabelled.

### Integration now also preserves CQ26

Current main has 22 expectations: CQ01–20, CQ25 and CQ26. PR128 has 24:
CQ01–24. The static union is **26 distinct queries**. Satisfying the requested
CQ01–25 combined verification must also retain and execute CQ26; a 25-entry
manifest would now drop current-main work. Main's manifest blob is
`7d4ebbfb2a37987cf430b00500c88a124d0d3e82`, CQ25 remains
`9b6ee8deed098919bcba437f097acb6cded059fb`, and CQ26 is
`58c6381e001200bf3cb14fc0897dc189156eada5`. This inventory is not a combined run.

### Other merge-review dependencies

A newer [scheduled privacy run](https://github.com/edithatogo/UOGTO/actions/runs/45811415789)
failed on current main after an earlier successful push run. A sanitized
[handoff under existing security issue #107](https://github.com/edithatogo/UOGTO/issues/107#issuecomment-7229938315)
routes diagnosis to the existing central privacy rollout and UOGTO security
owners. This lane does not waive the failure, change shared policy, or disclose
matched values. Current PR checks must be inspected separately.

The bounded maintenance review found #110 and #114 contain small dead-code
deletions, but their old August checks do not validate current-main integration.
PR109 must retain its deterministic sample ordering: an independently replayed
four-row, two-sample control selects `[a,b]` for both input orders on current
main, while PR109 `279bfef55954de17600100db317e15b0a10ae511` changes from `[a,b]`
to `[z,y]` when the same rows are reversed. No shared writer branch was changed.

### Next research steps within existing ownership

These are falsifiable proposals, not achieved frontier results or new tracks.

1. **Costing writer and integrator:** qualify zero/partial/full conservation,
   distinct recipient counts, direct and pooled scenario isolation, multi-line
   pools and malformed scenario provenance using shape-qualified fixtures and
   complete result rows; then execute CQ01–26 on the actual combined commit.
2. **Existing SGC/Paignia owners:** use the existing information-set and
   discounted-Markov profiles for a real version-matched read/write round trip.
   Preserve full identities, labelled axes, payoff ownership, timing,
   probabilities and provider revisions. A mutated payoff owner or information
   partition must fail beside a valid passing control. Reuse current native
   receipts and SGC.02–05/SGC.08; do not add another acceptance framework.
3. **Existing FRT.04/FRT.07 and MAT.04 owners:** test semantic-loss detection on
   independently specified held-out cases and seeded mutations, comparing direct
   conversion, identity-only checks and the semantic checker. Predeclare missed
   errors, false rejection, supported-case denominator, runtime and memory, then
   ablate individual checks. Implementation alone cannot establish superiority.

These follow the existing [frontier programme](../../../docs/roadmap/frontier-programme-20261108.md)
and [Markov contract](../../../docs/contracts/executable-discounted-markov-profile-v1.md).
Issue #134 remains held; none of these proposals recovers predecessor artifacts,
grants source rights or qualifies manuscript publication.

## Provenance and ownership

- Repository: [edithatogo/UOGTO](https://github.com/edithatogo/UOGTO).
- Current main as inspected: `147aee40fd682c0949244b5e34897ed952ed4b73`.
- Writer-owned [PR #128](https://github.com/edithatogo/UOGTO/pull/128): `7e9075b8fd77543fc8853fab20319415cb86597d` (`codex/costing-valuation-reporting-20261108`), three commits ahead and nine behind main; GitHub reports `mergeable=false`.
- Existing integration/admission owner: conversation `6af96da1-c088-83ec-85a8-ab19f5f4512c`. No integrator or writer authority is transferred by this review.
- PR128's branch-local Conductor metadata for `costing_valuation_reporting_20261108` says `status=in_progress`, `execution_status=semantic_implementation_verified_with_baseline_suite_limitations`. This is not completed/merged status on main.
- Previous full [independent receiving receipt](https://github.com/edithatogo/UOGTO/pull/128#issuecomment-7009348837) and [source inventory receipt](https://github.com/edithatogo/UOGTO/issues/134#issuecomment-7009365696) remain preserved.

## Exact source identities

| File | Git blob at pinned head |
| --- | --- |
| CQ21 conservation, PR128 | `4fbdeb27546d3e78e384b85571b1962825f57574` |
| CQ22 reporting, PR128 | `56cf264601c8ea7188a406318f3563d181c92bfe` |
| CQ23 infant attribution, PR128 | `1028141d5c3677eaeb5a94fff7b21771b16630f2` |
| CQ24 rate provenance, PR128 | `834110549313faffbc82c2816ef3453f967a3cb3` |
| CQ25 dynamic representation, main | `9b6ee8deed098919bcba437f097acb6cded059fb` |
| Main CQ expectation manifest | `4c36f87f68d07397eb02f7dc61a186ed6115c709` |
| PR128 CQ expectation manifest | `f26edca35b836cbe8fb1403a47b668a07cb84063` |
| Main CQ-ID reservation record | `c9ad1dd41ee76e641b18f963f84c075680d2077c` |

### Executed independent SPARQL verification

2026-11-19 pinned-query suite: Python 3.13.5, RDFLib 7.5.0, pytest 9.0.2, **8 passed / 3 failed (expected RED)**. Repeated on 2026-11-20: **8 passed / 3 failed**, 597 warnings, 0.45 s. The negative fixture outputs are unchanged:

1. CQ21 entirely unallocated 100-unit pool: pool row exists in RDFLib but `allocatedTotal` and `recipientCount` are **unbound**, rather than `0` / `0`. Other engines may omit the row; both outcomes violate the intended query contract.
2. CQ23 added alternative **direct** 7-unit valuation: infant A becomes **67**, incorrectly combining with baseline **60**.
3. CQ23 added alternative **pooled** 60+60 valuation: infants A/B become **120/150**, incorrectly combining with baseline **60/90**. The minimal alternative-pool RDF tests SPARQL aggregation only; complete SHACL conformance is not asserted.

CQ22 evidence and CQ24 rate-provenance baseline pass, as does a separate 4-row synthetic CQ25 main test. For an independently replayable *compact RED* reproduction, use adjacent `check_cq21_cq23.py` against an **actual checkout** of PR128 query files (not main). On the original head its three negative checks must fail:

```shell
python conductor/reviews/pr128-independent-costing-20261120/check_cq21_cq23.py \
  --query-root PATH_TO_PR128_CHECKOUT/competency-questions
# Exit 1: 2 baseline checks pass, 3 negative regression checks fail.
# Only the pinned historical bytes are accepted; changed queries are rejected.
```

The standalone script was executed locally on 2026-11-20 against the exact query bytes: 2 passes / 3 failures, expected exit 1; `python -m py_compile` passed. No real patients, funding figures or empirical observations are involved. Local PySHACL was not installed, so **no new local SHACL pass** is claimed. The optional diagnostic repair prototypes in the prior receiving artifact passed in isolation but are *not* a validated patch or instruction to replace owner code.

### Hosted baseline results — not combined-tree acceptance

PR128 unchanged-head GitHub Actions: [Validate UOGTO 42431227335](https://github.com/edithatogo/UOGTO/actions/runs/42431227335) and [Required Gate 42431227269](https://github.com/edithatogo/UOGTO/actions/runs/42431227269) both successful: **344 passed, 1 skipped**, semantic audit 56 ontology files, 31 SHACL-conforming examples, expected **CQ01–24** results. Those baseline cases did **not** detect the independent edge cases, and main-only CQ25 was not present in the PR128 validation tree.

## Writer: bounded requested fixes and regressions

1. CQ21: anchor all `CostPool` rows, optionally aggregate allocations, and use typed zero-safe totals/counts, including a completely unallocated pool. Prove 0%, partial and 100% allocations, amount/residual conservation, no duplicate recipients.
2. CQ23: separate alternative scenarios across **both direct valuation lines and allocations**. Either require a single selected scenario consistently or group by `scenarioKey` and infant. Define/enforce unambiguous pool/allocation scenario provenance; prevent join multiplication for multi-component pools. Prove alternate direct + pooled lines and failure on missing/mixed scenarios. Allocation is an attribution view, **not** a second source expense.
3. Submit exact-head RED→GREEN fixture receipts and full semantic/SHACL/CQ validation; leave source catalogue rights/editorial claims unchanged. Writer should acknowledge receipt and state intended correction head in [PR #128](https://github.com/edithatogo/UOGTO/pull/128).

## Integrator: CQ01–25 boundary

A *static comparison* of remote manifests finds **21** entries on current main (CQ01–20 and CQ25) and **24** on PR128 (CQ01–24); their unique union has exactly **25** distinct filenames/numbers. The CQ25 file on main retains original blob `9b6ee8...`. **This is not an executed combined-tree validation.**

After writer corrections, the existing integrator should non-forcibly reconcile both branches, preserving main's CQ25 query, reservation, temporality test and all PR128 CQ21–24 queries/fixtures/profiles, then run the **complete CQ01–25 manifest and SPARQL execution** together with all semantic/SHACL, security and protected CI checks on the exact integrated commit. Do not suppress checks or relabel historical results. Integrator should record receiving acknowledgement and actual combined-tree results before admission; no separate review lane may merge PR128.

## Source/recovery hold: issue #134

[Issue #134](https://github.com/edithatogo/UOGTO/issues/134) remains open. Main's independently accessible 60 source seeds, 74 bibliography entries, 64 attribution records, 4 checked-in RDF source artifacts plus 35 reference-only sources, and 24 current-manuscript CSL references are **not evidence of recovering** the predecessor's reported 114 references, 57 raw-byte receipts, 22 RDF parses or 26-page PDF. Preserve original worktree/archive, raw-byte SHA-256, copyright/licence disposition, original manuscript, graphs, figures, execution environment, logs and dirty/untracked inventory. No source promotion, rights inference, manuscript publication, artifact destruction or recovery closure.

## Close-out boundary

**Review evidence:** published for the independent reviewer lane. **Owner receipt:** pending express acknowledgement. **Costing acceptance, combined CQ integration, source recovery, scientific appraisal and release:** all remain with their existing owners and **not complete**. Under the user's 28 November review-and-merge instruction, this separate evidence PR may be merged after its current checks pass; that records the review without admitting costing or completing the handoff. Do not archive this lane. Shared `conductor/status.md`, `conductor/runlog.md`, track registry, root CI and owner-owned code are intentionally untouched.
