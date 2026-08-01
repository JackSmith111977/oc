#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, shutil, datetime

def dump(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--canon',required=True); ap.add_argument('--output',required=True); ap.add_argument('--references')
    a=ap.parse_args(); canon=json.load(open(a.canon,encoding='utf-8'))
    if str(canon.get('schema_version')) not in {'3.1','3.1.0'}: raise SystemExit('unsupported canon schema')
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    root=canon.get('root_canon',{}); strong=canon.get('strong_reference',{}); variants=canon.get('variants',{})
    dump(out/'root-canon.json',root); dump(out/'strong-reference.json',strong)
    dump(out/'approved-variants.json',variants)
    dump(out/'consistency-lock.json',{'rules':canon.get('consistency_lock',[]),'forbidden_drift':canon.get('qa',{}).get('likely_failures',[])})
    refs={'assets':[]}
    if a.references:
        rp=Path(a.references)
        if rp.exists(): refs=json.load(open(rp,encoding='utf-8'))
    dump(out/'reference-manifest.json',refs)
    meta=canon.get('meta',{}); cid=meta.get('id') or ''.join(ch.lower() if ch.isalnum() else '-' for ch in meta.get('name','character')).strip('-') or 'character'
    files={}
    for key,fn in [('root_canon','root-canon.json'),('strong_reference','strong-reference.json'),('approved_variants','approved-variants.json'),('consistency_lock','consistency-lock.json'),('reference_manifest','reference-manifest.json')]:
        files[key]={'path':fn,'sha256':sha(out/fn)}
    manifest={'handoff_version':'1.0','character_id':cid,'character_name':meta.get('name',''),'source_schema_version':str(canon.get('schema_version')),'source_revision':int(meta.get('revision',0)),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files}
    dump(out/'manifest.json',manifest)
    print(out)
if __name__=='__main__': main()
