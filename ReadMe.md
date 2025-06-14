Given a list of cybersecurity controls (from multiple frameworks), build a system that:

Groups similar controls by semantic meaning

Merges them into a unified version (with new description + implementation steps)

Outputs a structured, machine-usable list

[Raw JSON Input]
        ->
 [Semantic Vectorizer]
        ->
 [Clustering Engine]
        ->
 [LLM Unifier Engine]
        ->
[Unified Controls JSON Output]
