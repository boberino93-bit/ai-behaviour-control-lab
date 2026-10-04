# Swarm Launch Kernel V1

Kernel version: `1.0.0`.

This project uses the common Swarm Launch Kernel for concurrent multi-agent rounds. Runtime records are project-local under `.swarm/` and bound to both `project_id` and `global_run_id`. Cross-project telemetry is read-only and never grants command/integration authority. No force pushes or blind coordination overwrites are permitted. Stale run epochs, project mismatch, malformed/unsupported messages, and illegal cross-project commands are quarantined. Repeated invariant failures can place only this project into `DEGRADED_READ_ONLY`.

Launch: `BOOT -> IDENTITY -> PACKAGE -> GLOBAL RUN -> ROLE -> READY -> LOCAL START GATE -> WORK`.
Work: `IDENTIFY -> VALIDATE RUN -> ACQUIRE/VERIFY LEASE -> READ -> WORK -> IDEMPOTENT PERSIST -> VERIFY -> CHECKPOINT -> HANDOFF`.

Claims are versioned leases. Create new GitHub lease paths only if absent. Renew/reassign using the current blob SHA plus expected lease version. Stale writers reread/reconcile/use bounded deterministic backoff. Never force-push.

State is sharded under `.swarm/{epochs,ready,leases,idempotency,quarantine,health,checkpoints,convergence}/<run>/...`. Managers publish queue depth for backpressure. Completion requires research accounted for, Manager dispositions complete, Primary/local decisions persisted, package parity restored, no unresolved leases, and a valid recovery checkpoint.

Every PRIMARY, MANAGER, and RESEARCH package must include/load this protocol, `swarm_kernel/project.json`, `swarm_kernel/AGENT_BOOTSTRAP_OVERLAY.md`, and compatible `swarm_kernel/kernel.py`.

The lab's local Artifactory/AgentBus remains canonical. GitHub `artifactory-backup/` and `agentbus-backup/` remain recovery mirrors; this kernel does not promote them to live authority.
