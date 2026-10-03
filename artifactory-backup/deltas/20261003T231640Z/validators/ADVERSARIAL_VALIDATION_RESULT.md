# Adversarial coordination-state validation

Project: `ai-behaviour-control-lab`  
Baseline package set: `0.1.0` / protocol `1.0.0`  
Validation scope: coordination integrity only

| Test | Result | Observation |
|---|---|---|
| canonical authority boundary | PASS | local Artifactory canonical / GitHub backup-only |
| real message uniqueness/project binding | PASS | 5 messages |
| real package coherence | PASS | registry + 3 manifests aligned |
| missing project identity | PASS | rejected |
| foreign project identity | PASS | rejected |
| duplicate message ID | PASS | rejected |
| stale active lease | PASS | rejected |
| package protocol drift | PASS | rejected |
| role identity mismatch | PASS | rejected |
| foreign-project package | PASS | rejected |

**Result: 10/10 PASS.**

The tests intentionally confirm fail-closed behavior for missing/foreign identity, duplicate IDs, stale active leases, package protocol drift, role identity drift, and foreign-project packages. The live baseline also passed message uniqueness/project binding, package coherence, and the local-Artifactory/GitHub-backup authority boundary.

This does not validate any external research hypothesis or scientific claim.
