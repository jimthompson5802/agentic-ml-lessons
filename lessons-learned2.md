# Lessons Learned: #2 Agentic ML Development

These lessons cover commits `4602fa6` through `889c28e` in [agentic-ml](https://github.com/jimthompson5802/agentic-ml). 

Two dialogue tables at the end trace developer direction from planning through implementation, review, and merge. The US-11 table shows design correction and phased approvals for local data extraction. The US-12 issue #19 table shows how questions about requirements and proposed APIs led to scope alignment, simpler interfaces, and verification of assessment and partitioning behavior.

**Key takeaway:** Well-defined user stories, detailed design specifications, and regular review of the coding assistant’s work are critical to controlling project scope and preventing over-engineering. Reviewing proposed interfaces before coding helps uncover missing requirements and unnecessary abstractions.

## What Worked

**Phase gates kept approval explicit.** Plans follow milestone → user story → implementation phases → tasks. Each phase requires developer approval; plan approval alone does not authorize implementation. Scope changes require a recorded impact assessment and decision. ([Agent instructions](https://github.com/jimthompson5802/agentic-ml/blob/main/AGENTS.md))

**Verification clarified completion.** TDD requires agreed public test boundaries, small red–green cycles, and preserved evidence. Phase, story, and milestone acceptance have distinct obligations; passing story checks does not complete milestone verification. ([Agent instructions](https://github.com/jimthompson5802/agentic-ml/blob/main/AGENTS.md), [Development checkpoints](https://github.com/jimthompson5802/agentic-ml/blob/main/CHECKPOINTS.md))

**Criterion-level scope made acceptance precise.** The scope revision synchronized GitHub issues and acceptance criteria. US-12 issue #15 covers quality checks and blocking; #19 retains assessment and partitions. Closing one issue does not complete the story, and approving scope does not deliver the MVP. ([Scope revision plan](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/plans/mvp-scope-revision.md), [Development checkpoints](https://github.com/jimthompson5802/agentic-ml/blob/main/CHECKPOINTS.md))



## What Needed Improvement

**Ambiguity gave the coding assistant too much design freedom.** As development progressed, it became clear that gaps in the user stories and design left too much room for the assistant to invent detailed interfaces and code. The result was an over-engineered solution for this stage of development. More explicit scope, simpler interface expectations, and early design review were needed to keep implementation focused on the MVP.

Resolving this issue added development time and increased tokens costs.

The following items describe that rework.

- **The roadmap needed a tighter MVP.** M1–6 became two milestones: M1 completes one local classification experiment; M2 adds usability and committed-project reproduction. M0 foundation and M50 tooling retain their obligations; broader platform work is deferred. US-39 covers the basic experiment path; US-40 covers scientist-directed external assistant use. ([User stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md), [Scope revision plan](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/plans/mvp-scope-revision.md))

- **The basic path needed simpler requirements.** Mandatory experiment approvals were removed from the basic path. Existing strict planning, validation, and approval APIs remain supported, with their integrity and validation contracts preserved. ([Active design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md))

- **Extraction needed fewer abstractions.** Native pandas DataFrames and project functions replaced proposed wrappers, query abstractions, and registration machinery. A small helper records provenance; native scikit-learn components support preprocessing and models. ([Active design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md))

- **Design claims needed clearer boundaries.** The design separates implemented contracts, proposed interfaces, and deferred capabilities. OS isolation, hard quotas, managed agents, and durable recovery remain deferred. Historical designs serve as references rather than MVP requirements. ([Active design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md))

- **Refactor CI into two parallel jobs to solve time out error.** Default milestone tests and code checks now run alongside the remaining tests and distribution checks in two independent jobs. The split preserves complete test coverage without overlap and requires both jobs to pass. ([CI design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/development/ci.md))


**Periodic clean up of CHECKPOINTS.md** Reduce the clutter in CHECKPOINTS.md. It now summarizes the current position and links to authoritative plans and evidence. ([Development checkpoints](https://github.com/jimthompson5802/agentic-ml/blob/main/CHECKPOINTS.md))


## Example Dialog with the Coding Assistant

### User Story (US-11) Development Dialog

This table from the [US-11 chat extract](raw-data/us-11-chat.md#prompt-and-response-table) shows developer direction and approvals from planning through merge. Responses show the first 100 characters of the first assistant message before the next user prompt. Ellipses mark longer responses; matching-record sessions are incomplete.

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

### User Story (US-12) Issue #19 Development Dialog

This table from the [issue #19 chat extract](raw-data/issue-19-chat.md) follows developer direction, design decisions, and approvals through implementation and merge. Responses show the first 100 characters of the final assistant response, or the first reply when no final response was exported. Ellipses mark truncated responses.

| Workflow State | My Prompt | Coding Assistant Response |
| --- | --- | --- |
| Confirming ability to start development. | is there any blocker to implment gh issue #19 | No technical or dependency blocker was found for [issue #19](https://github.com/jimthompson5802/agen... |
| Initiated plan development. | define implementation plan for gh issue #19 | I’ll use the create-implementation-plan skill to draft issue #19’s owning plan, including public tes... |
| Continue plan development after switching model. | define implementation play for gh issue #19 | Created the [implementation plan for issue #19](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-... |
| Reviewing the generated plan. | what is the business objective of the assessment-split feature?  What capability does it deliver? | The business objective is to help data scientists judge whether their data is suitable for a classif... |
|  | is there any guidance on how to generate the reproducible partitions? | Yes. The design gives the requirements; the [implementation plan](/workspaces/agentic-ml/docs/plans/... |
|  | summarize the plan by calling out each phase and its tasks | The [plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-assessment-splits.md) has four implem... |
|  | does the design document provide any guidance on this part of the work? | Yes. The active [Data and Features design](/workspaces/agentic-ml/docs/specs/design/data-and-feature... |
|  | I'd like to refine the design documentation ot indicat that the toolkit should use scikit-learn capabilties.  we should not be building any custom where scikit-learn has the functionality.  If you believe we have to build some custom functionality support the assessment or partitioning, call that out and I want to discuss it. | Updated the [design guidance](/workspaces/agentic-ml/docs/specs/design/data-and-features.md:41) and ... |
| Identifying missing functional requirement. | sometimes, all I'll need is a two way split (train/test) and not the full three-way split (train/validate/test).  Is this option supported? | Scikit-learn supports both. Our draft plan currently requires three partitions, so **two-way splitti... |
|  | update the plan so that two-way and three-way splits are supported | Updated the [plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-assessment-splits.md) to supp... |
|  | does the design or any other document have to be updated re: support for two-way and three-way splitting? | Yes. The plan now supports both layouts, but the authoritative documentation still needs alignment:<br>... |
|  | what authorative document needs alignment | Two documents define the requirements and need alignment:<br><br>1. **[GitHub issue #19](https://github.co... |
|  | make the alignment | Aligned [issue #19](https://github.com/jimthompson5802/agentic-ml/issues/19), repository US-12-AC-03... |
|  | summarize plan callout each phases and its objective and the tasks w/in the phase. | The [plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-assessment-splits.md) contains four i... |
| Approve the implementation plan. | i approve the plan | Recorded your approval in the [plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-assessment-... |
|  | commit changes | Committed as `c0dcaa1` — `docs: plan US-12 assessment and split layouts`.<br><br>Working tree is clean. Ch... |
| Start Implementation Phase 1 | start ip1 | IP1 is underway. Issue #19 and supplier discussions are refreshed; the [contract proposal](/workspac... |
| Reviewing the artifacts generated during Implementation Phase 1. | summarize docs/plans/milestone-1-us-12-assessment-splits.md | The [plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-assessment-splits.md) delivers issue ... |
|  | summarize docs/data-assessment-and-splits.md | The [document](/workspaces/agentic-ml/docs/data-assessment-and-splits.md) proposes four toolkit help... |
| Soliciting more information on the proposed design. | explain more teh assess_data helper | `assess_data` is proposed as a small reporting helper: give it a pandas DataFrame and the classifica... |
|  | explain create_partitions | `create_partitions` is proposed as the helper that **prepares train/test or train/validation/test da... |
|  | does create_partition support stratification | Yes—the proposed `create_partitions` helper supports target stratification for seeded splits:<br><br>```py... |
|  | what is the purpose of the read/write partition records | The partition records let you **save a split once and later restore the exact same rows**, without g... |
|  | is use of the read/write partiton functions critical to just running an experiment | No. **They are not critical to simply running an experiment.**<br><br>A script can create partitions and p... |
|  | for the four functions which one are mandatory | For **simply running an experiment, none of the four toolkit helpers is inherently mandatory**—proje... |
|  | summarize docs/plans/sources/us-12-19-ip1-issues.md | The [file](/workspaces/agentic-ml/docs/plans/sources/us-12-19-ip1-issues.md) is a **source snapshot ... |
|  | summarize docs/verification/us-12-19-ip1.md | The [report](/workspaces/agentic-ml/docs/verification/us-12-19-ip1.md) records **partial IP1 contrac... |
|  | is there an estimate on the number of test cases that will be added | There is no recorded test-count estimate yet. For the current four-helper proposal, I’d estimate **r... |
|  | what is my pending action | Your pending action is to **decide which toolkit helpers to retain**:<br><br>1. `assess_data` — consistent... |
| Changing the design. | I only want to keep 1 and 2.  Confirm what this means? | You want to retain only:<br><br>1. **`assess_data`** — produces a consistent report using native pandas st... |
|  | summarize the plan | The revised direction is to deliver **two optional toolkit helpers** for issue #19:<br><br>- **`assess_dat... |
|  | does any other document have to be updated with this change | Yes. Alongside the implementation plan, these documents need updates:<br><br>&#124; Document &#124; Required change ... |
|  | make the update | Updated the [plan](/workspaces/agentic-ml/docs/plans/milestone-1-us-12-assessment-splits.md), [contr... |
|  | summarize docs/verification/us-12-19-ip1.md | The [report](/workspaces/agentic-ml/docs/verification/us-12-19-ip1.md) records **IP1’s contract revi... |
|  | summarize docs/data-assessment-and-splits.md | The [document](/workspaces/agentic-ml/docs/data-assessment-and-splits.md) defines the proposed contr... |
|  | is there support for both 2-way and 3-way splits | Yes. The proposal supports both:<br><br>- **Two-way:** train/test, with no validation partition.<br>- **Three... |
| Approval of Implementation Phase 1 Design artifacts. | i approve ip1; commit changes | Committed as `37ffe7d` — `docs: approve US-12 assessment and partition contracts`.<br><br>IP1 and Gate 1 a... |
|  | what is the next phase | The next phase is **IP2: implement data assessment** for US-12 issue #19, covering **AC-02**.<br><br>It wi... |
| Start Implementation Phase 2 | start ip2 | IP2 is complete: `assess_data` now provides descriptive summaries, missingness and target balance.<br><br>... |
| Reviewing the Implementation Phase 2 artifacts | summarize | IP2 implemented `assess_data` with numeric summaries, missingness, categorical frequencies and targe... |
|  | what skills are avaialble | Available skills:<br><br>&#124; Area &#124; Skills &#124;<br>&#124;---&#124;---&#124;<br>&#124; GitHub &#124; `retrieve-github-issue`, `create-github-is... |
|  | what is my pending action | Your pending action is to **approve Gate 2 for IP2**.<br><br>IP2 is complete and verified. You can say:<br><br>-... |
| After reviewing artifacts approve Implementation Phase 2 | i approve ip2; commit changes | IP2 approved and committed as `c092a33` — `feat(data-assessment): add descriptive assessment reports... |
| Adhoc addition of an agent skill to monitor running tests. | commit skill changes as well | Committed as `43cd770` — `docs(skills): add pytest progress reporting skill`.<br><br>Working tree is clean... |
| Approve start of Implementation Phase 3 | start ip3 | I’ll check the current checkpoint and plan to identify IP3 and its next authorized step. |
|  | report test progress | IP3 is complete: seeded and supplied partitions, membership validation, and source records are imple... |
| Manual verification of the generated code. | is there a short python program I can run that allows me to see the functionality implemented | Yes—added and verified [examples/assessment_and_splits.py](/workspaces/agentic-ml/examples/assessmen... |
|  | what is pending action | Your **Gate 3 approval** is pending. IP3 is complete and verified.<br><br>After approval, authorize **“sta... |
| After reviewing artifacts and running sample code, approve Implementation Phase 3. | i approve ip3; commit | Gate 3 approval recorded. Committed as `ffd5322` — `feat(splitting): add recorded and validated data... |
| Approve start of Implementation Phase 4 | start ip4 | I’ll check the checkpoint and implementation plans to identify IP4 and its next approved step. |
|  | report test progress | IP4 is technically complete.<br><br>- Both installed wheel paths pass.<br>- M1 and final M1–6 each passed **7... |
| After reviewing artifacts, approve Implementation 4. | i approve ip4; commit | Committed as `600f49e` — `test(data): verify assessment and splits in installed projects`.<br><br>Gate 4 a... |
| Accept the completion of Issue #19. | i accept issue #19 | Issue #19 acceptance is recorded and pushed as `6df5c1b`.<br><br>Created [PR #62](https://github.com/jimth... |
| Request for resolution of review comment. | resolve this review comment: https://github.com/jimthompson5802/agentic-ml/pull/62#discussion_r4504392360 | Updated both design pages in `23b260d`, pushed to PR #62, and [resolved the review thread](https://g... |
| Squash merge PR and update main branch. | squash merge; switch to main; pull changes; commit and push | Done.<br><br>- Squash-merged PR #62 as `980c97f`; issue #19 closed.<br>- Switched to `main` and pulled change... |
|  | what does context.md say | I couldn’t find `context.md` in this repository, including hidden and ignored files. Did you mean `C... |
|  | summarize checkpoints.md | `CHECKPOINTS.md` says:<br><br>- **Current state:** On `main`. Issue #19 is accepted and closed; PR #62 was... |
| Clean up feature branches. | delete local and remote branches the pr | Deleted local and remote `US-12-assessment-splits` branches for PR #62.<br><br>Cleanup records committed a... |
|  | what is current status | - On **`main` at `83c86a1`**, synchronized with `origin/main`; working tree is clean.<br>- **Issue #19 ... |
