# Mapping robustness experiments

This experiment evaluates the mapping review set with a simple feature-ablation scaffold.
The goal is to measure how much each signal contributes to reviewed mapping decisions.

- Review rows: 2
- Scored rows: 2
- Positive rows: 1
- Negative rows: 1
- Embedding method: character-trigram-cosine-proxy

## Feature families

- exact_label
- normalized_label
- definition_similarity
- hierarchy_context
- property_signature
- embedding_similarity

## Ablations

| ablation | precision | recall | f1 | accuracy | active features |
| --- | ---: | ---: | ---: | ---: | --- |
| all_features | 1.000 | 1.000 | 1.000 | 1.000 | exact_label, normalized_label, definition_similarity, hierarchy_context, property_signature, embedding_similarity |
| minus_exact_label | 1.000 | 1.000 | 1.000 | 1.000 | normalized_label, definition_similarity, hierarchy_context, property_signature, embedding_similarity |
| only_exact_label | 1.000 | 1.000 | 1.000 | 1.000 | exact_label |
| minus_normalized_label | 1.000 | 1.000 | 1.000 | 1.000 | exact_label, definition_similarity, hierarchy_context, property_signature, embedding_similarity |
| only_normalized_label | 1.000 | 1.000 | 1.000 | 1.000 | normalized_label |
| minus_definition_similarity | 1.000 | 1.000 | 1.000 | 1.000 | exact_label, normalized_label, hierarchy_context, property_signature, embedding_similarity |
| only_definition_similarity | 1.000 | 1.000 | 1.000 | 1.000 | definition_similarity |
| minus_hierarchy_context | 1.000 | 1.000 | 1.000 | 1.000 | exact_label, normalized_label, definition_similarity, property_signature, embedding_similarity |
| only_hierarchy_context | 0.500 | 1.000 | 0.667 | 0.500 | hierarchy_context |
| minus_property_signature | 1.000 | 1.000 | 1.000 | 1.000 | exact_label, normalized_label, definition_similarity, hierarchy_context, embedding_similarity |
| only_property_signature | 0.500 | 1.000 | 0.667 | 0.500 | property_signature |
| minus_embedding_similarity | 1.000 | 1.000 | 1.000 | 1.000 | exact_label, normalized_label, definition_similarity, hierarchy_context, property_signature |
| only_embedding_similarity | 1.000 | 1.000 | 1.000 | 1.000 | embedding_similarity |
