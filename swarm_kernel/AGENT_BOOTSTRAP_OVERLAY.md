# Swarm Launch Kernel — Agent Bootstrap Overlay

Applies to PRIMARY, MANAGER, and RESEARCH. Validate the canonical project and local Artifactory/AgentBus first; require `swarm_kernel/project.json` to match; bind one `global_run_id`; publish READY; wait for local start gate; use versioned leases and idempotency keys; heartbeat/checkpoint leases; obey Manager backpressure; quarantine stale/wrong-project/malformed/unsupported/illegal cross-project commands; stop integration mutations under `DEGRADED_READ_ONLY`; and close leases plus persist recovery/convergence state before handoff.

Research, Manager, and Primary authority remain unchanged. Cross-project health telemetry is observation only. GitHub backup mirrors are not live authority.
