# GitHub backup policy

GitHub is a downstream recovery copy of local Artifactory state. It is not an active coordination plane.

## Required order for any backup push
1. Complete the project mutation in the correct project workspace.
2. Persist the corresponding durable message(s) in local Artifactory `/messages/`.
3. Read back the newly persisted local records and verify project identity and message IDs.
4. Build a backup snapshot/commit containing the project change plus all local Artifactory message-board updates through a declared cutoff.
5. Push the backup to `boberino93-bit/ai-behaviour-control-lab`.
6. Record a local `BackupReceipt` containing Git commit SHA, local message cutoff, included message IDs or manifest/hash, timestamp, and result.

## Fail-closed rules
- Never use a GitHub commit as a substitute for local Artifactory persistence.
- Never write a message to GitHub first and later "sync it back" as authoritative state.
- If local persistence/readback fails, do not claim backup completion.
- If GitHub backup fails after local persistence succeeds, local project work remains valid; record backup status as FAILED/PENDING and retry idempotently.
- A push that omits local message-board changes after the last recorded cutoff is an incomplete backup and must not receive a successful BackupReceipt.
