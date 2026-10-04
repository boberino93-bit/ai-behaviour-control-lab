# Swarm Launch Kernel — Agent Bootstrap Overlay

Applies to PRIMARY, MANAGER, and RESEARCH.

Before actionable project work:
1. Validate the canonical AI Behaviour Control Lab project and local Artifactory/AgentBus authority.
2. Load `swarm_kernel/project.json` and require exact project/repository/coordination binding.
3. Obtain the externally supplied `global_run_id` for the coordinated launch; do not independently mint a different run ID for a multi-project round.
4. Require the launch contract to match the configured `expected_global_round_projects`, kernel version, and shared run ID. Persist only this project's local epoch record; never write another project's epoch.
5. Missing, stale, or mismatched epoch/project membership fails closed and is quarantined; do not publish READY.
6. Bind the launched role/package, publish READY, and wait for the local start gate.
7. Use versioned leases and deterministic idempotency keys; heartbeat/checkpoint leases; obey Manager backpressure; quarantine stale/wrong-project/malformed/unsupported/illegal cross-project commands; stop integration mutations under `DEGRADED_READ_ONLY`; and close leases plus persist recovery/convergence state before handoff.

Research, Manager, and Primary authority remain unchanged. Cross-project health and epoch telemetry are observation only and confer no work, role, repository, command, or integration authority.

GitHub `agentbus-backup/` and `artifactory-backup/` remain recovery mirrors, not live authority. The shared run value synchronizes round identity; it does not create shared mutable project state.
