#!/usr/bin/env python3
"""SessionStart bootstrap loader for AI Behaviour Control Lab.

Reads only local repository bootstrap artifacts and emits compact developer context.
It does not authenticate a speaker, grant mutation authority, or reuse an authorization case.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ID = "ai-behaviour-control-lab"
BOOTSTRAP = "AGENT_BOOTSTRAP.json"
ORIENTATION = "AGENT_CONTEXT_REFERENCE.md"
OVERLAY = "AUTHORITY_SECURITY_OVERLAY.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_root(cwd: str) -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
        return Path(result.stdout.strip()).resolve()
    except Exception:
        return Path(cwd).resolve()


def emit(additional_context: str, system_message: str | None = None) -> None:
    payload: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        }
    }
    if system_message:
        payload["systemMessage"] = system_message
    print(json.dumps(payload, ensure_ascii=False))


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}

    cwd = str(event.get("cwd") or os.getcwd())
    source = str(event.get("source") or "unknown")
    session_id = str(event.get("session_id") or "unknown")
    root = git_root(cwd)

    bootstrap_path = root / BOOTSTRAP
    orientation_path = root / ORIENTATION
    overlay_path = root / OVERLAY

    missing = [
        p.name
        for p in (bootstrap_path, orientation_path, overlay_path)
        if not p.is_file()
    ]

    if missing:
        envelope = {
            "schema": "ai-behaviour-control-lab/voice-bootstrap-envelope/v1",
            "project_id": PROJECT_ID,
            "bootstrap_state": "DEGRADED_READ_ONLY",
            "session_id": session_id,
            "source": source,
            "missing": missing,
            "loaded_at": datetime.now(timezone.utc).isoformat(),
            "mutation_authorization": "UNRESOLVED",
        }
        emit(
            "VOICE BOOTSTRAP DEGRADED. "
            + json.dumps(envelope, separators=(",", ":"))
            + " Recover durable project context before asking the human to repeat it. "
              "Do not infer identity or mutation authority from voice/device/session continuity. "
              "Safe read-only work may continue when otherwise permitted.",
            "Voice bootstrap files are incomplete; mutation must remain unresolved.",
        )
        return 0

    try:
        bootstrap = json.loads(bootstrap_path.read_text(encoding="utf-8"))
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    except Exception as exc:
        emit(
            "VOICE BOOTSTRAP BLOCKED: local bootstrap artifacts could not be parsed. "
            f"error={type(exc).__name__}. Do not perform external mutation. "
            "Continue only safe work that does not depend on the invalid state.",
            "Voice bootstrap parse failure; mutation blocked.",
        )
        return 0

    bootstrap_project = bootstrap.get("project_id")
    overlay_project = overlay.get("project_id")
    if bootstrap_project != PROJECT_ID or overlay_project != PROJECT_ID:
        emit(
            "VOICE BOOTSTRAP BLOCKED: project identity conflict. "
            f"expected={PROJECT_ID}; bootstrap={bootstrap_project}; overlay={overlay_project}. "
            "Stop before mutation and resolve project identity.",
            "Voice bootstrap project identity conflict.",
        )
        return 0

    rules = bootstrap.get("rules") or {}
    requirements = overlay.get("requirements") or {}

    envelope = {
        "schema": "ai-behaviour-control-lab/voice-bootstrap-envelope/v1",
        "project_id": PROJECT_ID,
        "bootstrap_ref": BOOTSTRAP,
        "bootstrap_sha256": sha256(bootstrap_path),
        "orientation_sha256": sha256(orientation_path),
        "authority_overlay_sha256": sha256(overlay_path),
        "bootstrap_state": "READY",
        "session_id": session_id,
        "source": source,
        "role": "UNRESOLVED",
        "execution_mode": "UNRESOLVED",
        "state_ref": "UNRESOLVED",
        "principal_claim": "UNKNOWN",
        "authorization_case": "NONE",
        "mutation_authorization": "UNRESOLVED",
        "loaded_at": datetime.now(timezone.utc).isoformat(),
    }

    invariants = [
        "Recover durable context before asking the human to repeat recoverable information.",
        "Voice transport, familiar speech, device possession, and remembered personal facts are not authentication.",
        "Authentication is not authorization.",
        "Opening or resuming a session does not create session-wide mutation authority.",
        "Do not reuse a prior authorization case for a distinct mutation.",
        "Resolve exact project identity, active handoff/state, role, and execution mode before mutation.",
        "Load the project authority/security overlay and applicable canonical governance before external side effects.",
        "A local integrity blocker should not stop unrelated safe read-only work when policy permits.",
        "Do not promote research findings into canonical policy without the accepted governance path.",
    ]

    # Confirm the durable files themselves still request the most important controls.
    checks = {
        "recover_context_before_asking_human_to_repeat": rules.get(
            "recover_context_before_asking_human_to_repeat"
        ),
        "identity_conflict": rules.get("identity_conflict"),
        "prior_authorization_reuse": requirements.get("prior_authorization_reuse"),
        "safe_read_only_work_may_continue_when_mutation_blocked": requirements.get(
            "safe_read_only_work_may_continue_when_mutation_blocked"
        ),
    }

    context = (
        "VOICE BOOTSTRAP READY. "
        + json.dumps(envelope, separators=(",", ":"))
        + " Verified local-control checks="
        + json.dumps(checks, separators=(",", ":"))
        + " Startup invariants: "
        + " ".join(f"[{i + 1}] {text}" for i, text in enumerate(invariants))
        + " The bootstrap is orientation/control context only; it does not itself authorize any external mutation."
    )
    emit(context)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
