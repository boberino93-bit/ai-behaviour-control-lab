# AI Behaviour Control Lab — Primary bootstrap

This project operates from the local Artifactory/Library namespace at `/AI-Behaviour-Control-Lab-AgentBus`.

## Mandatory startup order
1. Read `PROJECT_MANIFEST.json` and bind to `project_id=ai-behaviour-control-lab` before mutable work.
2. Read `AGENT_DISCOVERY.json`, `PROTOCOL.md`, `REGISTRY.json`, and `BACKUP_POLICY.md`.
3. Inspect `/messages/` for durable project messages addressed to the agent, its role, or `all`.
4. Treat project identity as an authorization boundary. Do not infer another project from task wording.
5. Child agents inherit this project binding. Cross-project traffic is denied unless an explicit sanitized exchange is approved.
6. Primary owns accepted-state integration and release coherence. Manager reviews. Research supplies bounded evidence.
7. Before ending a material work unit, persist a durable message for findings, blockers, decisions, reviews, or handoffs.
8. Persist and read back local Artifactory state before any GitHub backup.

## GitHub rule
GitHub is a recovery mirror only. It is never the message board, task registry, decision authority, lock authority, or canonical project state. A GitHub commit must be traceable to already-persisted local Artifactory state and its backup receipt must identify the local message cutoff included.
