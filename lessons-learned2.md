# Development workflow, user-story scope, and design changes

Comparison: commit `4602fa6` through `8775327` in `agentic-ml`.

The main shift is toward a smaller MVP with clearer scope authority and more explicit development controls.

## Development workflow

- GitHub issues now govern implementation scope, including acceptance criteria and decisions recorded in comments. Repository stories provide milestone context; design documents support implementation.
- Before implementation, agents must retrieve the complete issue and follow the design reading map and related contracts.
- Plans follow **milestone → user story → implementation phases → granular tasks**, with explicit developer approval at each phase boundary. Plan approval does not authorize every implementation phase.
- Scope changes require a recorded impact assessment and scope-change history.
- TDD expectations are explicit: agree on public test boundaries, work in small red–green slices, and preserve evidence.
- Verification distinguishes phase gates, story acceptance and milestone acceptance. Passing story checks does not close broader milestone obligations.
- `CHECKPOINTS.md` was condensed into a current handoff with links to authoritative plans and evidence.

## User-story scope

- The former M1–6 roadmap became a **two-milestone MVP**:
  - **M1:** Complete one local classification experiment.
  - **M2:** Improve usability and reproduce a committed experiment project.
- M0 foundation and M50 contributor tooling retain their obligations; broader platform work moves to deferred scope.
- Added **US-39** for a simpler basic experiment path and **US-40** for scientist-directed external assistant use.
- Existing strict planning, validation and approval APIs remain supported, but mandatory experiment approvals are no longer a requirement for the basic path.
- Scope is more carefully divided between issues. For example, completed US-12 issue #15 covers quality checks and blocking; assessment and partitions remain with #19. Closing one issue does not complete every aspect of the story.
- The scope revision was synchronized with GitHub issues and documented criterion by criterion. Approval of those documents does not mean the MVP is implemented.

## Design

- The active design now distinguishes **implemented contracts, proposed interfaces and deferred capabilities**.
- It favors native library interfaces: pandas DataFrames and ordinary project functions for extraction, plus native scikit-learn components for learned preprocessing and models.
- Proposed extraction wrappers, query abstractions and registration machinery were withdrawn in favor of a small provenance helper around pandas.
- The basic path and existing strict APIs have separate responsibilities; simpler usage must preserve existing integrity and validation contracts.
- External assistants remain scientist-directed. The toolkit must demonstrate their use through recorded actions and independently verified outputs, without claiming control over assistant sessions.
- OS isolation, hard quotas, managed agents, durable recovery and other platform guarantees are explicitly deferred.
- Historical designs remain archived as reference material rather than active MVP requirements.

## Source documents

Paths are relative to this file and refer to the sibling `agentic-ml` repository.

- [User stories](../agentic-ml/docs/specs/user-stories.md)
- [Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md)
- [Scope revision plan](../agentic-ml/docs/plans/mvp-scope-revision.md)
- [Agent instructions](../agentic-ml/AGENTS.md)
- [Development checkpoints](../agentic-ml/CHECKPOINTS.md)
