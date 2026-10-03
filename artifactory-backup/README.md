# AI Behaviour Control Lab — Artifactory recovery backups

`/AI-Behaviour-Control-Lab-AgentBus` is the canonical project state. This GitHub directory is recovery storage only and must never be treated as the live message board, task registry, lock authority, or accepted-state authority.

Backups are versioned and append to repository history. `LATEST.json` identifies the newest complete recovery generation. Older full snapshots and deltas remain preserved as historical recovery evidence.

For v0.2.0, restore `state.tar.xz` into the canonical Artifactory root, then restore the three role ZIPs from the same versioned snapshot directory to their package paths. Verify the SHA-256 values in `SNAPSHOT_MANIFEST.json` before accepting the restored state.

The v0.2.0 snapshot was generated from locally persisted and read-back Artifactory state through its declared message cutoff. A concurrent older-protocol recovery delta already present on GitHub is preserved in history but was not treated as authoritative input to local state.
