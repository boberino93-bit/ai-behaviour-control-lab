# `.swarm/` Project-Local Runtime Namespace

Reserved for Swarm Launch Kernel records. Use sharded immutable/per-task records instead of one mutable hotspot. Records are scoped to this project and `global_run_id`. Foreign projects may only read health telemetry where permitted. GitHub create-if-absent + blob-SHA/expected-version semantics apply; stale writers reconcile/back off and never force-push.
