# Ecosystem discovery report

This report contains no absolute local paths. The ignored machine-readable manifest is
`.local/ecosystem-paths.json`.

| Component | Repository | Selection | Source | HEAD | Pin | Pin available | Clean | Branch |
|---|---|---|---|---|---|---:|---:|---|
| UOGTO | `https://github.com/edithatogo/uogto` | resolved-at-pin | bootstrap-cache | `ac5b8e86c4a3` | `ac5b8e86c4a3` | yes | no | `main` |
| Kairos | `https://github.com/edithatogo/kairos` | resolved-at-pin | bootstrap-cache | `fae901558f07` | `fae901558f07` | yes | yes | `main` |
| Voiage | `https://github.com/edithatogo/voiage` | resolved-at-pin | bootstrap-cache | `4b93ee04231b` | `4b93ee04231b` | yes | yes | `main` |
| Reimbursement Atlas | `https://github.com/edithatogo/reimbursement-atlas` | resolved | bootstrap-cache | `5b0c2fe3e1b7` | `c73d34dacae2` | yes | yes | `main` |

The selected working tree does not need to be checked out at the pin. Integrations must
read or test the pinned commit explicitly and must not mutate sibling working trees.
