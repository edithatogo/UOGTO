# Repository-only ontology snapshot supplement

Date: 2026-07-02

This supplement identifies the exact ontology copy and modular ontology source files that correspond to the manuscript and raw-search evidence package. It is a repository evidence artefact only. It does not need to be submitted with the arXiv preprint or a journal manuscript unless a reviewer asks for a raw ontology snapshot ledger.

## Snapshot Summary

- Modular ontology source files: 49
- Merged ontology copy: `dist/uogto.ttl` (2327 triples)
- Merged SHACL copy: `dist/uogto-shapes.ttl` (100 triples)
- Citation register entries: 19
- Machine-readable manifest: `docs/article-hardening/ontology-snapshot-manifest.json`
- Citation register: `docs/article-hardening/ontology-citation-register.md` and `.json`

## Ontology Copy Assets

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `dist/context.jsonld` | 93 | `406414d54e1001a23b326bc71731d66f7e5700275ddf4364d80309c5600172c6` |
| `dist/core.context.jsonld` | 4177 | `83bec14743fa4e1cfb131d807c8d888ec8e423e679b65985f908c24b1d994c9a` |
| `dist/extensions.context.jsonld` | 22548 | `4a7b2b4d3a985f2dd96e42656c9d7379a8b89690e750a1415acd1e41ecdc08b7` |
| `dist/uogto-shapes.ttl` | 3823 | `9c797fef91a25d41db065c7823647e05322288476b44c25d2c3568ff43b7acd2` |
| `dist/uogto.ttl` | 112639 | `d1535e606ca39293f08a4ca012933a28702b82966cbda6afce977c89c760ceb8` |

## Modular Ontology Source Files

These are the version-controlled Turtle files merged into the release ontology copy.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `ontologies/alignments/mcp-a2a.ttl` | 574 | `2698d2d685f2c6c91c3aef4bdaad97a857c584c0d97424336b711ff6caf8b2c2` |
| `ontologies/alignments/open-games.ttl` | 609 | `f26d3877038d44ac7e1d46cb0385379b1060070fa21b0013378373b25c6e1ec4` |
| `ontologies/alignments/prov-o.ttl` | 630 | `2144e6b5224f1ae5df8aea8aade7fe6e3afb7a8f6f57a387441dc4b33df0c98b` |
| `ontologies/alignments/schema-org.ttl` | 589 | `714b11a0d62c77a508ac1e5bd3e89b19f54ee242c2e8b5139c64f4ac7c965ee4` |
| `ontologies/alignments/wot-thing-description.ttl` | 716 | `8916578529ade900c242e280a29fd6f721dd702fdacf0725f8cb1cec18a3c805` |
| `ontologies/core/actions.ttl` | 828 | `5f8070ed12573f5fcd3e380445984d5934807cad6ea133703fc47f951749bd8c` |
| `ontologies/core/agents.ttl` | 779 | `69cd19bbc5252e53b43fe63b0c949134e8e3579c2d96965cd9d1574e79a93cf3` |
| `ontologies/core/dynamics.ttl` | 851 | `f9c80b1f6505321cd9953fa6631e25ecabdfa49e9fccd77267ed902135ea45a4` |
| `ontologies/core/equilibria.ttl` | 889 | `641bebcf7d653663cc9ea5abbd11b4e795ad7437c5d0c88c4d37afde16002510` |
| `ontologies/core/games.ttl` | 830 | `13fbd77e66308c667a287dc812f3b5ba83cc4916f0e17ed15678c0eb62076dcb` |
| `ontologies/core/information.ttl` | 874 | `322246623ecb8c78e22c3a7c7f99333557d75d899617f4d353444079aa35d399` |
| `ontologies/core/outcomes.ttl` | 828 | `455d2de5dbfcb989ce55ab792d4ac446dd3b670f85b4a19ac3317ad77e8aea53` |
| `ontologies/core/payoffs.ttl` | 815 | `eb5122d7552acfb053e8f92b357cb77903ddfd255e4c0cc208bcd3ce40a2b66f` |
| `ontologies/core/rules.ttl` | 797 | `6391e55074fcc6f7ecd0f1aecf71a315bacfdcce930477a413e678dc2244ca1c` |
| `ontologies/core/strategies.ttl` | 825 | `7eec8a9dedfea1bb22a2b724ee78cdb0a5cf76248062de6225fe12118713d269` |
| `ontologies/core/uogto-core.ttl` | 15354 | `7e14bdd6d9ad04ddc67cb99220c5b98d3482e8c6e7cb097652aea5d3aa56fce8` |
| `ontologies/core/uogto-governance.ttl` | 3993 | `911095f5217920d10a5ad7e4126860d827422e9810616f8b6bb7bdbbf529f4e3` |
| `ontologies/extensions/algorithmic-game-theory.ttl` | 3167 | `3640162cef14e13421026d93acca3da5ca65950cd3697775b2cfb22b4d26d83e` |
| `ontologies/extensions/algorithmic-solvers-patch.ttl` | 466 | `a8dc9eee6c7516061859d5838f59861c578b1473d5073999c926b84ca0798178` |
| `ontologies/extensions/auctions.ttl` | 2807 | `ea95b19a0cd5b1961ad2188ac9ccb036452aad074e7f7c2fdbb1e433147d79ad` |
| `ontologies/extensions/bargaining.ttl` | 2917 | `f0922aec55c333a4440894eef8d80e3aea6c6e7a2ef9783ba94c736228103aa2` |
| `ontologies/extensions/behavioural-games.ttl` | 3247 | `decaf45b1aadebd4c16575d74be7168f256d6dbddba7c8d882b58d5f6c7190b5` |
| `ontologies/extensions/causal-games.ttl` | 3151 | `b1ac7fe6b4895514039a0526b5d71a0683d3475efdde2bf8da56ad738bb85bd2` |
| `ontologies/extensions/compositional-open-games.ttl` | 3318 | `644f118690308a71407e4ab58cbac5e853301970f630574085fc23a6532d3880` |
| `ontologies/extensions/computational-social-choice.ttl` | 3365 | `3189fb82b9851b821e3bf848b4f913dfc399cd6556d07e85ec5345761afa0861` |
| `ontologies/extensions/congestion-routing-games.ttl` | 3305 | `5ad6fc6569909fd42e00b66251f173762a10b750c64ffe28208125df94be9ce9` |
| `ontologies/extensions/contract-theory.ttl` | 3618 | `2e4a8df44384bc352d88551a1e3486ffd0608d2e0f01a5c12c2d454f7577818d` |
| `ontologies/extensions/cooperative.ttl` | 3464 | `9b30eac977a4345a14acc7dee98937b0627e1abb6777ae2010f79584272793c6` |
| `ontologies/extensions/deontic-logic.ttl` | 3350 | `ff1ef0c8a0744dac3598e9c40ed6b8072526f52b999cb3111b0e332d01d852d2` |
| `ontologies/extensions/differential-hybrid-games.ttl` | 3392 | `6c6aeccbbd96fc9b0283117e3a360a944d9d468903e07d3f843a3b1044660a54` |
| `ontologies/extensions/digital-twin-games.ttl` | 3520 | `c409ff4fb0518822d1a509a632f74021cf9cba979a19cabcae3f8e8ed016baf9` |
| `ontologies/extensions/epistemic-games.ttl` | 2988 | `e627403e061e04136fa0bb9b75962030f296289c5a731e7c418f3432b07a6429` |
| `ontologies/extensions/evolutionary-games.ttl` | 3041 | `350faa79e01dd2608cbaa5f074d3ed3813a17135edf907080bc0241ff0d3de1b` |
| `ontologies/extensions/game-description-languages.ttl` | 3552 | `62836169b63b6dc5068d7d54082f4abcdd17cff5bb1ba758811c5257d29890d4` |
| `ontologies/extensions/information-design.ttl` | 3154 | `759d8d72cfbc24d4eddf363ba3edbb2cc9f1ae4d1a83941cfd4e6a647abe7557` |
| `ontologies/extensions/institutional-economics.ttl` | 3331 | `b437a03c570b4955bf01ed49ac94392a4beadec0498dd94b62faff459c144fe4` |
| `ontologies/extensions/kg-execution-bindings.ttl` | 3409 | `a643f0b3642da25d14b7ea860d9f3e41b364f2acbdd070ca64e6695265af25eb` |
| `ontologies/extensions/learning-in-games.ttl` | 2796 | `1647c22edf9f138dd118731e82705fddd3e2a609275382f2922022b6407afe25` |
| `ontologies/extensions/llm-agent-games.ttl` | 3594 | `1b33388798047e1a14a1980195bc05bffd73704809174207356b77bff1f9e9a9` |
| `ontologies/extensions/marl.ttl` | 3967 | `d23d69abeed01467f6e0dc461f74688ed998af3ad757a76848f22f5bfe77a5e2` |
| `ontologies/extensions/matching-allocation.ttl` | 3275 | `bd010b340ed92b4c4cfa6edf0d09de23eb5b51b6905078a571a72c4378ea1746` |
| `ontologies/extensions/mean-field-games.ttl` | 3022 | `51b195ca990e31ae2fd15152342fd02cc802540d982315323bb46be06e9a62fc` |
| `ontologies/extensions/mechanism-design.ttl` | 3152 | `ea893c159bf2d339fd77fd72816caf8766f1ae2f2d266328fb5cf27e1901cfdc` |
| `ontologies/extensions/network-games.ttl` | 3058 | `6096da2e9115cc56c1d5891bd2f0b52f03f0b3c98df0f9c2c6fc87a66138c604` |
| `ontologies/extensions/petri-net-devs-hla.ttl` | 3507 | `abed94362da36e4a931d91abec44e9f3b5bae2bdbc2f30bbb8932d401bcb1a14` |
| `ontologies/extensions/privacy-disclosure.ttl` | 2941 | `475094e7221bc14afae49913291937d21e5883571d589e1ede0a76126fa1c2f9` |
| `ontologies/extensions/security-games.ttl` | 3337 | `ccc8f9ba849d7d7be5ecdc80738beea52188825872f2b0b47cd09e8ff8b8ea77` |
| `ontologies/extensions/trust-reputation-provenance.ttl` | 3042 | `40534b9646ecba09903519a7e6892c4bfd4ad388f14b58ad00c7a017e5192036` |
| `ontologies/extensions/verification-games.ttl` | 3521 | `2a883382d9a04fd3f2e9ed577a69e11fd885841d5f6a600b81700859432e6e77` |

## Use In The Evidence Trail

- Cite `dist/uogto.ttl` as the compact ontology copy for repository review.
- Cite `ontologies/` when reviewers need module-level provenance.
- Cite `docs/article-hardening/ontology-citation-register.md` for the corresponding final reference list.
- Keep this supplement repository-facing unless a submission venue requests raw ontology assets.
