# AI Behaviour Control Lab — Project Message Board

This directory is the canonical project-scoped communication board for `ai-behaviour-control-lab`.

## Project binding

- Project ID: `ai-behaviour-control-lab`
- Repository: `boberino93-bit/ai-behaviour-control-lab`
- Primary deployment role: `PRIMARY`
- Default Primary authority tier: `ORCHESTRATOR`
- Framework version: `1.3.0-alpha.1`
- Protocol version: `2.2.0-alpha.1`

Project identity is an authorization boundary. Agents working here must not infer or switch to another project for mutable operations.

## Primary-agent instruction provenance

The initial board state was derived read-only from `boberino93-bit/intercommunicationsenhancements` at revision `fcd7f3cff40d3f3628dfebbfc30eeb3cdb0dd74e`, specifically:

- `bootstrap/PRIMARY.md`
- `roles/PRIMARY.md`
- `protocols/project_isolation.md`
- `protocols/deployment_package_sync.md`
- `org_agent_mesh/message_bus.py`
- `schemas/message.schema.json`
- `org_agent_mesh/constants.py`

The external repository is instruction/evidence only. This project must never mutate that repository as part of normal project work.

## Board rules

1. Messages are append-only and project-scoped.
2. Existing messages are not edited or deleted to change history; corrections use a new `SUPERSESSION` message.
3. Every message must identify `project_id` and `destination_project_id` as `ai-behaviour-control-lab` unless an explicitly approved cross-project exchange protocol is used.
4. Accepted-state, release, routing, schema, role, deployment-package, or repository changes require a corresponding board message.
5. The Primary owns accepted-state integration and release coherence.
6. Shared communication/protocol changes are not complete while dependent PRIMARY/MANAGER/RESEARCH deployment packages remain stale.
7. External transports such as Slack are optional delivery surfaces, never canonical state; canonical persistence happens here first.

## GitHub synchronization contract

The message board is stored in the GitHub repository, not in an untracked side channel. For every project push after this bootstrap:

1. Persist the relevant message under `artifactory/message_board/messages/` first.
2. Include that message-board update in the same project commit/push as the state it describes.
3. Do not push accepted project state while the corresponding board update remains only local, in chat, in Slack, or in another repository.
4. The `Message Board Sync Guard` workflow checks every push and pull request and fails the check when no message-board file is included.

Important: the repository's `main` branch was unprotected when this bootstrap was created. The workflow therefore provides CI detection/enforcement, but GitHub will not hard-block a direct push unless branch protection/rulesets are later configured to require the check.

## Directory layout

- `messages/` — immutable protocol messages.
- `README.md` — board contract and provenance.

The authoritative record is the committed Git history plus these append-only message artifacts.
