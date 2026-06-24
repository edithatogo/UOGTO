# Article Hardening Case Studies

This register captures the case studies that should be used to stress-test UOGTO before expanding the ontology further.

| Case | Focus | Why it matters | Primary analysis lens | Expected artifacts |
| --- | --- | --- | --- | --- |
| Auction and mechanism design | Allocation rules, incentive compatibility, auction formats, and mechanism properties. | Tests strategic allocation, payments, and mechanism-level execution semantics. | ontology coverage, mapping completeness, competency-query support, executable trace linkage | candidate term mapping, module gap assessment, example instance, competency query |
| Voting and social choice | Preference aggregation, voting rules, collective choice, and social welfare criteria. | Checks collective decision rules versus individual strategy. | relation richness, hierarchy placement, external alignment only, disposition triage | cross-ontology alignment, review note, benchmark case, documentation example |
| Security and Stackelberg games | Leader-follower commitment, defender-attacker roles, and adversarial timing. | Tests asymmetry, commitment, and sequential best response. | role semantics, timing semantics, module overlap, domain review | module recommendation, alignment record, triage disposition, case-study note |
| Multi-agent reinforcement learning and Markov games | State transitions, policy learning, joint action spaces, and stochastic dynamics. | Validates learning agents, environment state, and repeated interaction with traceable execution. | state transition coverage, traceability, import depth, reasoner profile | state/action model, example trace, benchmark metric, mapping summary |
| Agent-based policy simulation | Population heterogeneity, adaptive behavior, rule-driven interaction, and policy outcome analysis. | Separates ABM semantics from game-theoretic commitments while showing where overlap is legitimate. | scope separation, defer vs reject triage, network analysis, descriptive analysis | scope decision, ontology boundary note, case comparison, review commentary |
| System-dynamics feedback game | Feedback loops, endogenous state evolution, policy levers, and long-run behavior. | Exercises the boundary between game-theoretic interaction and dynamic systems models. | causal loop coverage, hierarchy depth, out-of-scope triage, external alignment | boundary rationale, mapping note, candidate disposition, synthesis paragraph |
| LLM-agent and tool-use game | Agent tool selection, planner-executor feedback, prompt-mediated strategies, and observed action traces. | Captures strategic interaction in agentic systems and distinguishes it from general workflows. | executability, trace provenance, domain review, living evidence register | executive trace case, provenance model, review disposition, article example |
| Executable trace and provenance | Run logs, decision traces, provenance capture, and reproducible execution evidence. | Bridges formal ontology modelling and the paper's evidence model. | provenance linkage, evidence auditability, benchmark coverage, publication readiness | trace example, evidence register, quality benchmark, documentation cross-reference |

## Notes

- Use these cases as a fixed review spine for the article-hardening track.
- Each case should be paired with at least one example instance, one mapping decision, and one evidence note.
- The set is intentionally broader than the current UOGTO core so that missing or adjacent concepts can be triaged before expansion.

