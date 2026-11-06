# Architecture Decision Records

Each ADR captures one significant, hard-to-reverse decision. Statuses:
`Proposed`, `Approved`, `Superseded`, `Rejected`.

Do not edit an approved ADR to change its decision. Write a new ADR that
supersedes it and update the index.

| ID | Title | Status |
| --- | --- | --- |
| [0001](0001-modular-monolith.md) | Modular monolith over microservices | Proposed |
| [0002](0002-technology-stack.md) | Initial technology stack and versions | Proposed |
| [0003](0003-rest-api.md) | REST API with Django REST Framework | Proposed |
| [0004](0004-authentication.md) | Session authentication through a same-origin proxy | Proposed |
| [0005](0005-ai-provider-abstraction.md) | Provider-independent AI adapter and RAG | Proposed |
| [0006](0006-file-uploads.md) | Presigned direct-to-object-storage uploads | Proposed |

## Creating an ADR

1. Copy `docs/templates/adr.md`.
2. Number it sequentially.
3. State the context, the decision, alternatives, and consequences.
4. Open a PR; a human approves and changes the status to `Approved`.
5. Add it to the table above.
