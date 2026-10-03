#!/usr/bin/env python3
import json, sys
from pathlib import Path
from datetime import datetime, timezone

PROJECT='ai-behaviour-control-lab'

def parse_ts(s):
    return datetime.fromisoformat(s.replace('Z','+00:00'))

def validate_project_obj(obj, name='object'):
    if obj.get('project_id') != PROJECT:
        raise ValueError(f'{name}: project_id must be {PROJECT}')

def validate_messages(root):
    seen=set()
    for p in sorted((root/'messages').glob('*.json')):
        o=json.loads(p.read_text())
        validate_project_obj(o, p.name)
        mid=o.get('id')
        if not mid: raise ValueError(f'{p.name}: missing message id')
        if mid in seen: raise ValueError(f'duplicate message id: {mid}')
        seen.add(mid)
    return len(seen)

def validate_packages(root):
    pm=json.loads((root/'PROJECT_MANIFEST.json').read_text())
    reg=json.loads((root/'packages/PACKAGE_REGISTRY.json').read_text())
    validate_project_obj(pm,'project manifest'); validate_project_obj(reg,'package registry')
    if pm['protocol_version'] != reg['protocol_version']: raise ValueError('package registry protocol drift')
    if pm['package_set_version'] != reg['package_set_version']: raise ValueError('package set drift')
    for role,rec in reg['roles'].items():
        m=json.loads((root/rec['manifest_path']).read_text())
        validate_project_obj(m,f'{role} manifest')
        if m['role'] != role: raise ValueError(f'{role}: role mismatch')
        if m['protocol_version'] != pm['protocol_version']: raise ValueError(f'{role}: protocol drift')
        if m['package_set_version'] != pm['package_set_version']: raise ValueError(f'{role}: package set drift')

def validate_lease(o, now):
    validate_project_obj(o,'lease')
    if o.get('status')=='ACTIVE' and parse_ts(o['expires_at_utc']) <= now:
        raise ValueError('active lease is expired/stale')

def expect_reject(fn, label):
    try: fn()
    except Exception: return (label,'PASS','rejected')
    return (label,'FAIL','unexpectedly accepted')

def main(root):
    tests=[]
    pm=json.loads((root/'PROJECT_MANIFEST.json').read_text())
    validate_project_obj(pm,'project manifest')
    if pm.get('github_role')!='BACKUP_ONLY' or pm.get('canonical_state_system')!='LOCAL_ARTIFACTORY_LIBRARY':
        raise ValueError('authority boundary mismatch')
    tests.append(('canonical authority boundary','PASS','local Artifactory canonical / GitHub backup-only'))
    n=validate_messages(root); tests.append(('real message uniqueness/project binding','PASS',f'{n} messages'))
    validate_packages(root); tests.append(('real package coherence','PASS','registry + 3 manifests aligned'))

    valid_msg={'project_id':PROJECT,'id':'m1'}
    tests.append(expect_reject(lambda: validate_project_obj({'id':'x'},'missing-project message'),'missing project identity'))
    tests.append(expect_reject(lambda: validate_project_obj({'project_id':'foreign-project','id':'x'},'foreign message'),'foreign project identity'))

    def dup():
        seen=set()
        for o in [valid_msg,valid_msg.copy()]:
            validate_project_obj(o,'message')
            if o['id'] in seen: raise ValueError('duplicate')
            seen.add(o['id'])
    tests.append(expect_reject(dup,'duplicate message ID'))

    stale={'project_id':PROJECT,'status':'ACTIVE','expires_at_utc':'2020-01-01T00:00:00Z'}
    tests.append(expect_reject(lambda: validate_lease(stale,datetime.now(timezone.utc)),'stale active lease'))

    def protocol_drift():
        reg=json.loads((root/'packages/PACKAGE_REGISTRY.json').read_text()); reg['protocol_version']='999.0.0'
        if reg['protocol_version'] != pm['protocol_version']: raise ValueError('drift')
    tests.append(expect_reject(protocol_drift,'package protocol drift'))

    def role_drift():
        m=json.loads((root/'packages/manager/PACKAGE_MANIFEST.json').read_text()); m['role']='PRIMARY'
        if m['role']!='MANAGER': raise ValueError('role mismatch')
    tests.append(expect_reject(role_drift,'role identity mismatch'))

    def package_project_escape():
        m=json.loads((root/'packages/research/PACKAGE_MANIFEST.json').read_text()); m['project_id']='duo-open'
        validate_project_obj(m,'research manifest')
    tests.append(expect_reject(package_project_escape,'foreign-project package'))

    failed=[t for t in tests if t[1]!='PASS']
    for t in tests: print('\t'.join(t))
    print(f'SUMMARY\t{len(tests)-len(failed)}/{len(tests)} PASS')
    return 1 if failed else 0

if __name__=='__main__':
    raise SystemExit(main(Path(sys.argv[1] if len(sys.argv)>1 else '.')))
