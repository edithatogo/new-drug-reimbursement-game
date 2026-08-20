# Hugging Face policy

This project only references Hugging Face repositories under the username
`edithatogo`.

Current integration target:

- dataset: `edithatogo/reimbursement-atlas`
- Space: `edithatogo/reimbursement-atlas`

The repository does not depend on third-party Hub models or datasets. Any
machine-learning extraction experiments should be developed in, or published
to, an `edithatogo/*` repository with a dataset/model card, licence decision,
revision pin, evaluation protocol, and human-review boundary.

The Atlas dataset card and Hub metadata agree on `license: other` at immutable
Hub revision `a2b3682b1fd4dc5910a154c15abdc6e9c4199442`. This is not a
permissive licence grant: `RIGHTS.md` retains an unresolved registry status and
the publication manifest limits reuse to reviewed, derived metadata with
source-specific terms. The consumer must therefore continue to fail closed on
record-level rights, provenance, and approval even though the repository-level
metadata is internally consistent.

The corresponding static Space was observed at revision
`2a82c05f8e38a0ae8ab681d3d4cbda1b43c46d01`. Neither Hub surface contains a
TA1121-specific approved parameter packet. Exact revisions in
`ecosystem.lock.toml` remain authoritative until a deliberate compatibility,
rights, packet, and approval requalification is completed.
