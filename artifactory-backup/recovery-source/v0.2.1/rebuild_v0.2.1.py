#!/usr/bin/env python3
from pathlib import Path
import zipfile,json,hashlib,re,sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/"snapshots"/"ai-behaviour-control-lab-v0.2.0"
P=json.loads((HERE/"v0.2.1-patches.json").read_text(encoding="utf-8"))["patches"]
HASHES={'primary': 'cb2342dacc2d91ef41d164bfe3128ce8a148861b373e696bb730969a4d7e5284', 'manager': '9de95f75d824c4024135d7f9b8e31381641dc5d1d0764ff0019cd107ebcc8046', 'research': 'e9f0dc8330492a6acd83459f2d2139b78fd6e0b7d01bd6cf1915c7ede76cdfda'}
STAMP=(2026,10,3,23,28,0)

def apply_unified(old,diff):
    old_lines=old.splitlines(keepends=True)
    out=[]; old_i=0; lines=diff.splitlines(keepends=True); i=0
    while i<len(lines):
        if lines[i].startswith(("--- ","+++ ")): i+=1; continue
        if not lines[i].startswith("@@ "): i+=1; continue
        m=re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@",lines[i])
        start=int(m.group(1))-1
        out.extend(old_lines[old_i:start]); old_i=start; i+=1
        while i<len(lines) and not lines[i].startswith("@@ "):
            s=lines[i]
            if s.startswith(" "): out.append(s[1:]); old_i+=1
            elif s.startswith("-"): old_i+=1
            elif s.startswith("+"): out.append(s[1:])
            elif s.startswith("\\"): pass
            else: break
            i+=1
    out.extend(old_lines[old_i:])
    return "".join(out)

for role,expected in HASHES.items():
    base=BASE/f"ai-behaviour-control-lab-{role}-agent-v0.2.0.zip"
    with zipfile.ZipFile(base) as z:
        names=[i.filename for i in z.infolist()]
        entries={n:z.read(n) for n in names}
    for key,spec in P.items():
        if key.startswith("roles/"):
            prefix=f"roles/{role}/"
            if not key.startswith(prefix): continue
            name=key[len(prefix):]
        else:
            name=key
        if spec["mode"]=="replace":
            entries[name]=spec["content"].encode()
            if name not in names: names.append(name)
        else:
            entries[name]=apply_unified(entries[name].decode(),spec["diff"]).encode()
    target=HERE/f"ai-behaviour-control-lab-{role}-agent-v0.2.1.zip"
    with zipfile.ZipFile(target,"w") as z:
        for name in names:
            info=zipfile.ZipInfo(name,STAMP); info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=2175008768; info.create_system=3; info.flag_bits=0
            z.writestr(info,entries[name])
    sha=hashlib.sha256(target.read_bytes()).hexdigest()
    if sha!=expected: raise SystemExit(f"FAIL {role}: {sha} != {expected}")
    print("PASS",role,sha)
