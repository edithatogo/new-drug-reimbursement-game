# Ecosystem-first engineering policy

1. Search `edithatogo` GitHub and Hugging Face namespaces before selecting a
   dependency or creating a capability.
2. Classify the work as application-specific, shared capability, adapter, or
   evidence asset.
3. If an owned shared capability exists, depend on its public contract and add
   upstream proposals there.
4. If the capability is missing, incubate it behind a port and design it for
   extraction; do not bury it in the application package.
5. Third-party generic libraries require an ADR and migration decision.
6. Third-party capability frameworks are validation-only and isolated unless
   the owner explicitly approves them.
7. Pin repository revisions in `ecosystem.lock.toml` and update deliberately.
8. Treat Hugging Face metadata, licences, and revisions as governed supply-chain
   inputs. This project permits `edithatogo/*` IDs only.
