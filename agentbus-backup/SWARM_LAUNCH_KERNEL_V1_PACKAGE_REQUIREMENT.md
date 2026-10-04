# AI Behaviour Control Lab — Swarm Launch Kernel V1 Deployment Requirement

Status: ACTIVE FOR FUTURE DEPLOYMENTS
Kernel version: `1.0.0`
Project: `ai-behaviour-control-lab`
Repository: `boberino93-bit/ai-behaviour-control-lab`

## Authority boundary

The lab's local `AI-Behaviour-Control-Lab-AgentBus` / Artifactory remains canonical. GitHub `agentbus-backup/` and `artifactory-backup/` remain recovery mirrors only. This record does not promote either backup tree into live coordination authority.

## Package requirement

Every new or regenerated PRIMARY, MANAGER, and RESEARCH deployment used for a new full-system/global research run must include or load:

- `SWARM_LAUNCH_KERNEL_V1.md`
- `swarm_kernel/project.json`
- `swarm_kernel/AGENT_BOOTSTRAP_OVERLAY.md`
- `swarm_kernel/kernel.py`

The package must bind `project_id=ai-behaviour-control-lab`, repository `boberino93-bit/ai-behaviour-control-lab`, and the active global run ID before actionable work. READY barrier, versioned leases, deterministic idempotency, heartbeat/expiry, Manager backpressure, quarantine, project-local circuit breaker, and convergence gate are mandatory for the round.

Cross-project telemetry is read-only and grants no work, role, repository, command, or integration authority.

## Existing recovery packages

Existing GitHub recovery snapshots remain immutable evidence. They are not automatically kernel-compliant. Before the next simultaneous research round, deployment packages must be regenerated or wrapped with the current kernel overlay from the canonical local Artifactory/AgentBus and verified against its live state.
