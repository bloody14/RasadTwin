# Bootstrap Prompt — RasadTwin Antigravity Workspace

Paste this once at the beginning of a new Antigravity workspace after copying the governance pack into the repository.

```text
You are now operating inside the RasadTwin (SIH26251) repository.

FIRST: DO NOT CODE.

Read these files in this exact order:
1. AGENTS.md
2. SECURITY.md
3. docs/SECURITY_POLICY.md
4. docs/DECISION_POLICY.md
5. docs/CHANGE_CONTROL.md
6. docs/THREAT_MODEL.md
7. docs/ASSUMPTIONS.md (if present)
8. docs/PREREG.md (if present)
9. docs/STATE.md
10. the current phase prompt, when supplied

After reading them, create `docs/AGENT_BOOTSTRAP_ACK.md` containing:
- the official PS in one paragraph;
- the project goal in one paragraph;
- the security boundary;
- what you are allowed to decide autonomously;
- what requires human approval;
- the current phase/state;
- the files you consider protected;
- a statement that you will not invent results.

Then STOP and wait for the phase prompt.

IMPORTANT:
- Do not reinterpret the PS.
- Do not create new architecture without authorization.
- Do not add external network services by default.
- Do not use real or classified military data.
- Do not create offensive or autonomous military capabilities.
- Do not modify protected research/security files unless the phase explicitly authorizes the exact change.
- Do not claim that security is complete merely because tests pass.
- When uncertain, report the question; never guess.
```
