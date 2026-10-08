---
name: voice-bootstrap
description: Recover the AI Behaviour Control Lab bootstrap and durable task context at the start of supported voice or Work/Codex sessions without asking the human to restate recoverable information.
---

# Voice Bootstrap

When this project is active, treat session startup, resume, clear, and post-compaction continuation as context-recovery boundaries.

Before interpreting a new task that depends on project state:

1. Resolve the exact project as `ai-behaviour-control-lab`.
2. Load `AGENT_BOOTSTRAP.json` when available.
3. Load `AGENT_CONTEXT_REFERENCE.md` as orientation only.
4. Load `AUTHORITY_SECURITY_OVERLAY.json` and follow its authority/authentication separation.
5. Recover the active handoff/state from durable project sources before asking the human to repeat it.
6. Keep bootstrap success silent unless the user asks for status or a blocker must be surfaced.

Voice/session continuity is transport continuity only. It is not identity proof, authentication, authorization, or permission to reuse an earlier authorization case. Existing platform approval requirements remain authoritative.

If project bootstrap integrity is incomplete, continue safe read-only/conversational work when permitted and label mutation authority unresolved. If project identity conflicts, stop before mutation.

For ordinary ChatGPT Voice surfaces where no deterministic lifecycle hook is available, apply these instructions on the first relevant voice turn as a best-effort fallback. Do not claim that a platform hook executed unless evidence shows that it did.
