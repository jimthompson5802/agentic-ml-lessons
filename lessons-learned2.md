# Lessons Learned: #2 Agentic ML Development

Clear requirements, developer approval gates, and acceptance-based verification supported agentic development. Human review narrowed the MVP and simplified the design, replacing custom extraction abstractions with native pandas interfaces.

These lessons cover commits `4602fa6` through `8775327` in [agentic-ml](https://github.com/jimthompson5802/agentic-ml). The US-11 prompt/response table illustrates developer direction from planning through merge.

**Key takeaway:** Well-defined user stories, detailed design specifications, and regular review of the coding assistant’s work are critical to controlling project scope and preventing over-engineering.

## What Worked

**Clear requirements authority defined scope.** GitHub issues govern implementation, including acceptance criteria and comment decisions. Stories provide milestone context; design documents support implementation. Agents must read the complete issue and relevant design contracts before coding. ([Agent instructions](../agentic-ml/AGENTS.md), [User stories](../agentic-ml/docs/specs/user-stories.md), [Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

**Phase gates kept approval explicit.** Plans follow milestone → user story → implementation phases → tasks. Each phase requires developer approval; plan approval alone does not authorize implementation. Scope changes require a recorded impact assessment and decision. ([Agent instructions](../agentic-ml/AGENTS.md))

**Verification clarified completion.** TDD requires agreed public test boundaries, small red–green cycles, and preserved evidence. Phase, story, and milestone acceptance have distinct obligations; passing story checks does not complete milestone verification. ([Agent instructions](../agentic-ml/AGENTS.md), [Development checkpoints](../agentic-ml/CHECKPOINTS.md))

**Criterion-level scope made acceptance precise.** The scope revision synchronized GitHub issues and acceptance criteria. US-12 issue #15 covers quality checks and blocking; #19 retains assessment and partitions. Closing one issue does not complete the story, and approving scope does not deliver the MVP. ([Scope revision plan](../agentic-ml/docs/plans/mvp-scope-revision.md), [Development checkpoints](../agentic-ml/CHECKPOINTS.md))

**Example prompts for implementing a user story.** This table from the [US-11 chat extract](raw-data/us-11-chat.md#prompt-and-response-table) shows developer direction and approvals from planning through merge. Responses show the first 100 characters of the first assistant message before the next user prompt. Ellipses mark longer responses; matching-record sessions are incomplete.

| Workflow State | My prompt | Coding Assistant response |
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

**Ambiguity gave the coding assistant too much design freedom.** As development progressed, it became clear that gaps in the user stories and design left too much room for the assistant to invent detailed interfaces and code. The result was an over-engineered solution for this stage of development. More explicit scope, simpler interface expectations, and early design review were needed to keep implementation focused on the MVP.

Resolving this issue consumed additional development time and tokens to narrow the roadmap, simplify requirements and interfaces, clarify design claims and assistant evidence, and update project records.

The following items describe that rework.

- **The roadmap needed a tighter MVP.** M1–6 became two milestones: M1 completes one local classification experiment; M2 adds usability and committed-project reproduction. M0 foundation and M50 tooling retain their obligations; broader platform work is deferred. US-39 covers the basic experiment path; US-40 covers scientist-directed external assistant use. ([User stories](../agentic-ml/docs/specs/user-stories.md), [Scope revision plan](../agentic-ml/docs/plans/mvp-scope-revision.md))

- **The basic path needed simpler requirements.** Mandatory experiment approvals were removed from the basic path. Existing strict planning, validation, and approval APIs remain supported, with their integrity and validation contracts preserved. ([Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

- **Extraction needed fewer abstractions.** Native pandas DataFrames and project functions replaced proposed wrappers, query abstractions, and registration machinery. A small helper records provenance; native scikit-learn components support preprocessing and models. ([Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))

- **Design claims needed clearer boundaries.** The design separates implemented contracts, proposed interfaces, and deferred capabilities. OS isolation, hard quotas, managed agents, and durable recovery remain deferred. Historical designs serve as references rather than MVP requirements. ([Active design](../agentic-ml/docs/specs/agentic-ml-harness-design.md))


**Periodic clean up of CHECKPOINTS.md** Reduce the clutter in CHECKPOINTS.md. It now summarizes the current position and links to authoritative plans and evidence. ([Development checkpoints](../agentic-ml/CHECKPOINTS.md))
