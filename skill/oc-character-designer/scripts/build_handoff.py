#!/usr/bin/env python3
from pathlib import Path
import argparse, datetime, hashlib, json

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--canon',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();c=load(a.canon)
 if c.get('schema_version')!='3.1':raise SystemExit('unsupported Canon schema')
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True);mapping={'root_canon':'root-canon.json','strong_reference':'strong-reference.json','approved_variants':'approved-variants.json','consistency_lock':'consistency-lock.json'}
 dump(out/mapping['root_canon'],c['root_canon']);dump(out/mapping['strong_reference'],c['strong_reference']);dump(out/mapping['approved_variants'],c['variants']);dump(out/mapping['consistency_lock'],{'rules':c['consistency_lock'],'risks':c['qa'].get('likely_failures',[])})
 dump(out/'reference-manifest.json',{'assets':[]});mapping['reference_manifest']='reference-manifest.json';files={k:{'path':v,'sha256':sha(out/v)} for k,v in mapping.items()}
 dump(out/'manifest.json',{'handoff_version':'1.0','character_id':c['meta']['id'],'character_name':c['meta']['name'],'source_schema_version':'3.1','source_revision':c['meta']['revision'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files})
if __name__=='__main__':main()
