#!/usr/bin/env python3
from pathlib import Path
import json,zipfile,hashlib
HERE=Path(__file__).resolve().parent
S=json.loads((HERE/"v0.3.0-source.json").read_text())
stamp=tuple(S["zip_timestamp"])
for role,rec in S["roles"].items():
    target=HERE/f"ai-behaviour-control-lab-{role}-agent-v0.3.0.zip"
    with zipfile.ZipFile(target,"w") as z:
        for name,data in [("PACKAGE_MANIFEST.json",rec["PACKAGE_MANIFEST.json"]),("ROLE.md",rec["ROLE.md"]),*S["shared"].items()]:
            info=zipfile.ZipInfo(name,stamp); info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=25165824; info.create_system=3; info.flag_bits=0
            z.writestr(info,data.encode())
    sha=hashlib.sha256(target.read_bytes()).hexdigest()
    if sha!=rec["sha256"]: raise SystemExit(f"FAIL {role}: {sha} != {rec['sha256']}")
    print("PASS",role,sha)
