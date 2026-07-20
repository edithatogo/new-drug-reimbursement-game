# ADR 0004: Hugging Face scope is edithatogo-only

**Status:** accepted

All Hub repository IDs in executable manifests must begin `edithatogo/`.
Third-party models and datasets are not runtime or research-data dependencies
for this project. General open-source Python tooling can still be used locally
under the dependency policy.
