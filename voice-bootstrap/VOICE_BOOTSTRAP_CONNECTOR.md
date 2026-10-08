# Voice Bootstrap Connector

Status: PROPOSED IMPLEMENTATION
Project: `ai-behaviour-control-lab`
Date: 2026-10-07

## Purpose

Provide consistent project bootstrap behavior whenever an interactive voice session begins, without requiring the human operator to restate the bootstrap prompt.

The connector treats Voice as a transport surface only. Entering Voice may load context and policy, but it MUST NOT grant mutation authority, authenticate the current speaker, reuse a previous authorization case, or bypass platform approval requirements.

## Problem statement

The current lab bootstrap is durable and explicit, but ChatGPT Voice can begin with a different runtime/model surface from the text conversation. Memory and relevant plugins may be available, but ordinary ChatGPT Voice does not expose a documented generic lifecycle hook that guarantees an arbitrary connector will execute every time the Voice control is opened.

Therefore the design separates **bootstrap semantics** from **surface-specific activation**.

## Design principle

The connector behaves like a clinical communications routing preamble: establish channel identity, load routing/policy state, verify readiness, then pass the user's actual communication through. The preamble should normally be silent. It becomes user-visible only when bootstrap validation fails or the user requests status.

## Activation tiers

### Tier A — Deterministic: custom GPT-Live client

Use the OpenAI Live session creation path as the authoritative implementation where deterministic startup is required.

At session creation:

1. Resolve the project bootstrap source.
2. Fetch `AGENT_BOOTSTRAP.json`.
3. Fetch required orientation/security references named by the bootstrap.
4. Resolve the current accepted state/handoff references.
5. Validate project identity and policy versions.
6. Construct a compact `VoiceBootstrapEnvelope`.
7. Inject the envelope into the Live session `instructions` and, where useful, the initial text `input`/history before user audio is processed.
8. Mark the session bootstrap state as `READY`, `DEGRADED_READ_ONLY`, or `BLOCKED`.

GPT-Live supports startup instructions and initial history, making this the preferred path for a true every-session bootstrap.

### Tier B — Deterministic where hooks are supported: ChatGPT Work / Codex plugin

Package the bootstrap as a trusted plugin with a `SessionStart` lifecycle hook. The hook runs a local/bootstrap loader, validates the same envelope, and emits model-readable context before work begins.

This path is appropriate where ChatGPT Work or Codex provides the execution environment and the hook has been explicitly trusted. Installing a plugin alone does not make a hook trusted and does not deploy hook scripts to unsupported surfaces.

### Tier C — Best-effort: ordinary ChatGPT Voice

For ordinary Voice-in-Chat, use a plugin skill plus project/custom instructions that state:

> On Voice entry or when the first Voice turn is detected, recover the active project bootstrap and durable task state before interpreting the task. Do not ask the human to restate recoverable context.

This improves consistency but MUST be labelled best-effort because current ChatGPT plugin selection is relevance-driven rather than an exposed guaranteed Voice-start lifecycle event.

If a platform-level Voice lifecycle hook becomes available, Tier C should be replaced by the same deterministic bootstrap adapter used by Tiers A/B.

## VoiceBootstrapEnvelope v1

The runtime should inject only the minimum state needed to orient the Voice model:

```json
{
  "schema": "ai-behaviour-control-lab/voice-bootstrap-envelope/v1",
  "project_id": "ai-behaviour-control-lab",
  "bootstrap_ref": "AGENT_BOOTSTRAP.json",
  "bootstrap_sha": "<git-blob-or-content-digest>",
  "role": "<resolved-role-or-UNRESOLVED>",
  "execution_mode": "<recovery|qa|build|UNRESOLVED>",
  "state_ref": "<handoff-or-state-reference>",
  "principal_claim": "<NONE|REGISTERED|UNKNOWN>",
  "authorization_case": "<NONE|AUTH-case-id>",
  "mutation_authorization": "<AUTHORIZED|UNAUTHORIZED|UNRESOLVED>",
  "bootstrap_state": "<READY|DEGRADED_READ_ONLY|BLOCKED>",
  "loaded_at": "<ISO-8601>",
  "policy_digest": "<digest>"
}
```

Do not inject secrets, API keys, raw authentication proofs, or unnecessary personal information.

## Startup state machine

`VOICE_SESSION_CREATED`
→ `IDENTITY_RESOLUTION`
→ `BOOTSTRAP_FETCH`
→ `POLICY_FETCH`
→ `STATE_RECOVERY`
→ `INTEGRITY_CHECK`
→ one of:

- `READY`: context loaded and valid.
- `DEGRADED_READ_ONLY`: some noncritical state is unavailable; conversational/research work may continue, but external mutation remains blocked.
- `BLOCKED`: identity/bootstrap integrity conflict; stop mutation and surface the specific blocker.

After `READY` or `DEGRADED_READ_ONLY`, process the user's first spoken turn normally. Do not recite the bootstrap unless requested.

## Safety invariants

1. Voice transport is not identity proof.
2. Speaker recognition, familiarity, remembered personal facts, voiceprint similarity, or possession of the device MUST NOT be treated as authentication unless an independently approved authentication mechanism explicitly establishes that property.
3. Authentication is not authorization.
4. Authorization remains case-bound and single-use where required by the project overlay.
5. Opening Voice never creates session-wide mutation authority.
6. Existing ChatGPT/app approval UI remains authoritative. If the platform requires on-screen approval, spoken approval must not substitute for it.
7. A bootstrap failure localizes the restriction: unrelated safe read-only work may continue when policy permits.
8. The connector cannot promote research findings into canonical policy by itself.

## Drift and cache strategy

The connector may cache the last validated envelope for latency reduction, but every new Voice session must check a lightweight freshness key before using it. Suggested key:

`project_id + AGENT_BOOTSTRAP blob SHA + authority overlay SHA + active state revision`

If the key changed, rebuild the envelope. If freshness cannot be verified, use `DEGRADED_READ_ONLY`; do not silently assume the previous authorization state remains valid.

Authorization cases are never cached as reusable authority.

## Failure behavior

### Bootstrap source unavailable
Continue only with safe conversational/read-only capabilities and state: `DEGRADED_READ_ONLY`.

### Project identity conflict
State: `BLOCKED`. Do not mutate either project until identity is resolved.

### Policy digest mismatch
Reload canonical policy. If mismatch persists, state: `BLOCKED` for mutation.

### Active state/handoff unavailable
Recover from durable project sources before asking the human to repeat the objective. If recovery fails, continue safe independent work and ask only for the irrecoverable item.

### Voice session begins in an unsupported ChatGPT surface
Apply Tier C project/plugin instructions and expose telemetry indicating `activation_guarantee = BEST_EFFORT`.

## Observability

Record a privacy-minimized startup event:

- session correlation ID
- activation tier
- bootstrap SHA/digest
- policy digest
- bootstrap state
- load duration
- cache hit/miss
- failure code, if any

Do not log raw speech by default as part of bootstrap telemetry.

Suggested event names:

- `voice.bootstrap.started`
- `voice.bootstrap.ready`
- `voice.bootstrap.degraded`
- `voice.bootstrap.blocked`
- `voice.bootstrap.drift_detected`

## Acceptance tests

1. New GPT-Live session receives the project envelope before first user audio is interpreted.
2. Reopening Voice creates a fresh startup check even when conversation history remains the same.
3. Updating `AGENT_BOOTSTRAP.json` invalidates the previous cache key.
4. Missing noncritical state yields `DEGRADED_READ_ONLY`, not invented context.
5. Project identity mismatch prevents mutation.
6. A recognized/familiar speaker receives no implicit authorization.
7. Previous authorization cases are not reused.
8. The system does not ask the user to repeat context that is recoverable from durable state.
9. Startup is silent in the success case.
10. Ordinary ChatGPT Voice reports/records best-effort activation rather than falsely claiming deterministic execution.

## Recommended implementation order

1. Implement the envelope builder as a standalone pure function/service.
2. Implement the GPT-Live session-start adapter first; this establishes the deterministic reference behavior.
3. Add the Work/Codex `SessionStart` hook adapter using the same envelope builder.
4. Add a ChatGPT plugin skill/project-instruction fallback for ordinary Voice.
5. Add telemetry and drift tests.
6. Re-evaluate Tier C whenever ChatGPT exposes a supported Voice lifecycle event.

## OpenAI surface references checked 2026-10-07

- ChatGPT Voice: https://help.openai.com/en/articles/20001274-chatgpt-voice
- Plugins in ChatGPT: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- GPT-Live session management: https://developers.openai.com/api/docs/guides/live-conversations
- Plugin lifecycle hooks: https://developers.openai.com/plugins/build/plugins
- MCP server instructions: https://developers.openai.com/plugins/build/mcp-server

## Relationship to existing lab bootstrap

This connector does not replace `AGENT_BOOTSTRAP.json`. It is an activation adapter for voice transports. The canonical project bootstrap remains the source of identity, startup requirements, security overlays, governance references, and mutation constraints.
