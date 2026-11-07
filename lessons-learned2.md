# Lessons Learned: #2 Agentic ML Development

Agentic development benefited from clear requirements, phased implementation with developer approval, and verification tied to acceptance criteria. Human review also helped narrow the MVP and simplify the design, including replacing proposed custom extraction abstractions with native pandas interfaces. The lessons highlight the value of explicit scope decisions, familiar library interfaces, and evidence that distinguishes completed work from future capabilities.

These observations cover commits `4602fa6` through `8775327` in the [agentic-ml project](https://github.com/jimthompson5802/agentic-ml). They examine what worked in the development workflow and what needed improvement in user-story scope, design, and project records. A table of prompts and assistant response excerpts from US-11 provides a concrete example of developer direction through planning, design revision, phase approvals, testing, acceptance, and merge.

## What Worked

**Explicit requirements authority clarified implementation scope.** GitHub issues govern implementation scope, including acceptance criteria and decisions recorded in comments. Repository stories provide milestone context; design documents support implementation. Before implementation, agents must retrieve the complete issue and follow the design reading map and related contracts. ([Agent instructions](../agentic-ml/AGENTS.md), [User stories](../agentic-ml/docs/specs/user-stories.md), [Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

**Implementation phases kept developer approval and scope decisions explicit.** Plans follow milestone → user story → implementation phases → granular tasks, with explicit developer approval at each phase boundary. Plan approval does not authorize every implementation phase. Scope changes require a recorded impact assessment and scope-change history. ([Agent instructions](../agentic-ml/AGENTS.md))

**TDD and verification guidance clarified the evidence required for completion.** TDD expectations are explicit: agree on public test boundaries, work in small red–green slices, and preserve evidence. Verification distinguishes phase gates, story acceptance, and milestone acceptance. Passing story checks does not close broader milestone obligations. ([Agent instructions](../agentic-ml/AGENTS.md), [Development checkpoints](../agentic-ml/CHECKPOINTS.md))

**Scope synchronization made acceptance more precise.** The scope revision was synchronized with GitHub issues and documented criterion by criterion. Scope is more carefully divided between issues: completed US-12 issue #15 covers quality checks and blocking; assessment and partitions remain with #19. Closing one issue does not complete every aspect of the story. Approval of scope documents does not mean the MVP is implemented. ([Scope revision plan](../agentic-ml/docs/plans/mvp-scope-revision.md), [Development checkpoints](../agentic-ml/CHECKPOINTS.md))


**Example Prompts to implement a user story**:
The following table, copied from the [US-11 chat extract](raw-data/us-11-chat.md#prompt-and-response-table), illustrates the developer–assistant workflow from planning and design review through phase approvals, testing, story acceptance, and merge. It shows where the developer directed changes and authorized progress. Assistant responses contain only the first 100 characters of the first subsequent message before another user message; ellipses indicate longer responses, and matching-record sessions are incomplete.

| State of the Workflow | User prompt | Assistant response |
| --- | --- | --- |
|Selected US-11 for implementation, requesting agent to develop implementation plan. Coding Assistant creates feature branch.  | develop implementation plan for us-11 | I’ll use the create-implementation-plan and retrieve-github-issue skills to identify US-11’s scope a... |
| Coding assistant setting up access to Github | you can continue | I’ll retry GitHub access, then read US-11’s full discussion and the relevant design contracts before... |
|  | run gh auth login | I’ll start GitHub’s browser login flow in the container. |
|  | I want to run gh auth login and use paste a code | Run this in the container terminal:<br><br>```bash<br>gh auth login<br>```<br><br>Choose **GitHub.com → HTTPS → Paste ... |
|  | continue | I’ll check GitHub access and resume the US-11 plan if authentication is ready. |
| Implementation plan generated and I'm reviewing the proposed plan.  | what apis will be implemented | The plan proposes a new `agentic_ml.extraction` module with three public APIs:<br><br>&#124; API &#124; Purpose &#124;<br>&#124;-... |
|  | where is the design doc for the apis | The proposed APIs are in the [implementation plan’s “Proposed public contract for IP1 review” sectio... |
|  | are the proposed api consistent with the broader design? | I’ll compare the proposed API contract with the active design and separate clear alignment from deci... |
|  | do I have to decide now | No. Those decisions belong to Implementation Phase 1, which produces a concrete API contract for you... |
|  | what is my current action | Review the [US-11 plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-11.md). If you agree with i... |
| Approve proposed implementation plan and kick off the first phase.  | I approve plan; commit changes; and authorize ip1 | I’ll record your plan approval, commit the planning documents, and start IP1. I’ll use the execute-p... |
| Implementation Phase 1 completed and reviewing design artifacts.  Requested revision to one aspect of the design. | Instead of creating our own proprietary classes, I'd like to use pandas for all data extraction and the basis for feature engineering.  Rework the design of data extraction to use pandas. | I’ll rework extraction around native pandas DataFrames and project-owned pandas functions, removing ... |
|  | what is my action | Review the [revised pandas design](/workspaces/agentic-ml/docs/extraction.md) and [test boundaries](... |
| After ensuring requested change was made, approve the design from Implementation Phase 1 and start Implementation Phase 2 to generate code.  | i approve ip1; commit the changes; i authorize ip2 | I’ll record your approval, commit the revised design, then execute IP2 using TDD. I’ll stop after it... |
| Requesting coding assistant to provide periodic progress report. | every minute report number of remaining tests until complete | M1: **217 tests remaining of 432 selected**—214 passed, 1 skipped so far. I’ll report the remaining ... |
| Implementation Phase 2 complete and review the test artifacts.  | i approve ip2; commit changes; do not start ip3 | I’ll record IP2 approval, commit its changes, and leave IP3 unstarted. |
| Stopped work for the night and now restarting in the morning. | what is current status | US-11 is on branch `US-11-local-data-extraction`.<br><br>- **IP1:** Approved and committed—pandas API desi... |
| Initiate Implementation Phase 3 | start us-11 ip3 | I’ll check the US-11 plan and checkpoint, retrieve the issue discussion, and confirm IP3’s scope and... |
| Requesting coding assistant to provide periodic progress report. | how many remainng tests | About **282 of 433 tests remain** in the current M1 run, with no failures reported so far. After it ... |
|  | report the number of remainng tests every minute until all tests are complete | **281 tests remain** in the final M1–6 run. No failures reported. I’ll update the count every minute... |
|  | report count of remaining tests out of totl test count every minute until tests are complete | **251 remaining out of 433 total tests** in the final run; 182 completed. No failures reported. I’ll... |
| Implementation Phase 3 completed and reviewed the test artifacts. | i approve ip3 | I’ll record your IP3 approval in the plan, evidence, and checkpoint. Whole-story acceptance remains ... |
| Accept that US-11 acceptance criteria met based on coding assistant provided artifacts.  Coding assistant creates Pull Request and initiates a review.| i accept us-11 | I’ll record US-11 acceptance, commit the story changes, and follow the execute-plan workflow to push... |
| Coding Assistant flagged on issue, requesting coding assistant to resolve the issue. | resolve this comment https://github.com/jimthompson5802/agentic-ml/pull/60#discussion_r4501540084 | I’ll update the design status identified in the comment, verify the documentation change, push the f... |
|  | what is next step | Review PR #60’s CI results, then merge it when checks pass. US-11 is accepted and its review finding... |
| Issue resolved, direct coding assistant to merge feature branch to main. | squash merge PR #60 | I’ll check PR #60’s CI and merge status, squash-merge it, and verify the result. |
| Update local repo with changes from the Pull Reqests | switch to main; pull from origin; commit changes; | I’ll switch to `main`, pull from `origin` with fast-forward only, and commit the remaining checkpoin... |
|  | push | I’ll push the checkpoint commit on `main` to `origin`. |
| Clean up feature branches | delete local and remote branches for the pr just merged | I’ll verify that `US-11-local-data-extraction` is the merged PR branch, then delete it locally and f... |

## What Needed Improvement

**The roadmap needed a tighter MVP focus.** The former M1–6 roadmap became a two-milestone MVP: M1 completes one local classification experiment; M2 improves usability and reproduces a committed experiment project. M0 foundation and M50 contributor tooling retain their obligations; broader platform work moves to deferred scope. Added US-39 covers a simpler basic experiment path, and US-40 covers scientist-directed external assistant use. ([User stories](../agentic-ml/docs/specs/user-stories.md), [Scope revision plan](../agentic-ml/docs/plans/mvp-scope-revision.md))

**The basic experiment path needed simpler requirements.** Existing strict planning, validation, and approval APIs remain supported, but mandatory experiment approvals are no longer a requirement for the basic path. The basic path and existing strict APIs have separate responsibilities; simpler usage must preserve existing integrity and validation contracts. ([Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

**The extraction design needed fewer custom abstractions.** The design favors native library interfaces: pandas DataFrames and ordinary project functions for extraction, plus native scikit-learn components for learned preprocessing and models. Proposed extraction wrappers, query abstractions, and registration machinery were withdrawn in favor of a small provenance helper around pandas. ([Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

**Design documents needed clearer boundaries around delivery claims.** The active design now distinguishes implemented contracts, proposed interfaces, and deferred capabilities. OS isolation, hard quotas, managed agents, durable recovery, and other platform guarantees are explicitly deferred. Historical designs remain archived as reference material rather than active MVP requirements. ([Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

**Assistant support needed explicit evidence requirements and limits.** External assistants remain scientist-directed. The toolkit must demonstrate their use through recorded actions and independently verified outputs, without claiming control over assistant sessions. ([User stories](../agentic-ml/docs/specs/user-stories.md), [Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

**Checkpoints needed a more concise handoff.** CHECKPOINTS.md was condensed into a current handoff with links to authoritative plans and evidence. ([Development checkpoints](../agentic-ml/CHECKPOINTS.md))
