**Building an Agentic ML Toolkit — and Learning About Agentic Coding Along the Way**

I've been working on an open-source project called **Agentic ML**, an agent-agnostic toolkit for machine learning experimentation.

The long-term goal is to support iterative ML development, including feature engineering, model training, hyperparameter tuning, evaluation, and data improvement, with reproducibility and human approval built into the workflow.

But there's a second, equally important goal: **using the project as a hands-on experiment to explore and refine agentic coding practices.**

I'm using coding assistants for planning, implementation, testing, and GitHub interactions, while retaining human oversight at key decision points.

**A few lessons learned so far:**

- **Structured workflows make a difference.** GitHub issues define requirements and acceptance criteria. Implementation plans break work into phases, with verification evidence and approval gates.
- **Reusable agent skills improve consistency.** Skills for planning, implementation, scope management, and pull requests help standardize recurring development activities.
- **Human judgment remains essential.** The assistant can implement, investigate, and verify changes, but decisions about scope, priorities, and difficult tradeoffs still benefit from developer direction.
- **Fast test feedback is critical.** Long-running tests significantly slowed the development loop and consumed substantial time and tokens. Test stratification and a Linux devcontainer helped address the problem.
- **The development process has its own costs.** Testing the workflow itself introduced additional complexity and overhead, raising questions about how much process verification is worthwhile.

**My biggest takeaway so far:** Human judgment remains essential to effective agentic coding. While coding assistants can handle much of the implementation and verification, developers must still set priorities, evaluate results, and make difficult tradeoffs. Structured workflows, fast feedback, and persistent evidence make that judgment more effective while allowing assistants to operate with greater autonomy.

This is very much a **work in progress**. The ML toolkit is still in its early stages, and I'm continuing to experiment with the development practices as the project evolves.

Project: https://github.com/jimthompson5802/agentic-ml

Lessons learned: https://github.com/jimthompson5802/agentic-ml/blob/main/lessons-learned1.md

I'd be interested in hearing how others are approaching agentic coding workflows, particularly around testing, approval gates, and balancing autonomy with developer oversight.

#AgenticAI #CodingAgents #SoftwareEngineering #MachineLearning #OpenSource