# Project coordination protocol

## State authority
Local Artifactory/Library is canonical. GitHub is backup-only.

## Project isolation
All messages, tasks, artifacts, locks, leases, package records, and backup receipts are scoped to `ai-behaviour-control-lab`. Missing or conflicting project identity fails closed. Ordinary project channels never cross project boundaries.

## Message lifecycle
Messages are append-only. Corrections are new superseding messages; historical messages are not silently edited. Material messages retain project, sender, sender instance, recipient/role, timestamp, message ID, task/correlation context, status, evidence/artifact references, and backup state.

## Routing and validation
Before accepting a message or mutation, validate project identity, sender/instance identity where available, destination, ownership, type/schema, timestamp/expiry when applicable, capability, and referenced artifact ownership. Ambiguous routing is rejected or quarantined, never guessed.

## Work coordination
Tasks belong to exactly one project. Claims/leases are project-namespaced, recoverable after stale agents, and designed for idempotent retry. Duplicate commands should be safe no-ops or return the prior result.

## Primary authority
Primary owns architectural integration, accepted state, package/release coherence, project-boundary enforcement, and authorization of backup snapshots. Subordinate outputs are proposals/evidence until integrated by Primary.

## Package coherence
Changes affecting project identity, communication, schemas, bootstrap, role responsibilities, routing, Artifactory, repository resolution, or safety require impact analysis across PRIMARY/MANAGER/RESEARCH packages. Do not claim a coordinated release complete while affected packages are stale.

## Evidence and audit
Meaningful mutations must be reconstructable: what changed, who requested it, which project/agent/task/message caused it, when it occurred, what resource/version was involved, and the result.
