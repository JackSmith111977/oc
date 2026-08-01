#!/usr/bin/env python3
"""Transactional file-backed workspace for OC Canon 3.1."""
from pathlib import Path
import argparse, copy, datetime as dt, hashlib, json, os, shutil, sys, tempfile, uuid

SCHEMA='3.1'; WORKSPACE='1.1'; ALLOWED=('root_canon.','strong_reference.','variants.','presentation.','production_spec.','consistency_lock','qa.','extensions.')
CHAPTERS=[('00-overview','Overview',['meta','root_canon.identity']),('20-body-core','Body Core',['root_canon.body_core']),('30-face-core','Face Core',['root_canon.face_core']),('35-identity-details','Identity Details',['root_canon.identity_details']),('40-hair-strong-reference','Hair Strong Reference',['strong_reference.hair']),('50-costume-strong-reference','Costume Strong Reference',['strong_reference.costume','strong_reference.palette_accessories']),('70-approved-variants','Approved Variants',['variants']),('80-production-spec','Production',['production_spec','presentation']),('90-consistency-lock','Consistency',['consistency_lock','qa'])]

def now(): return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def atomic(p,text):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix='.'+p.name,dir=p.parent)
 try:
  with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as f:f.write(text);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
def dump(p,o): atomic(p,json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def get(o,path):
 cur=o
 for k in path.split('.'):
  if isinstance(cur,dict) and k in cur:cur=cur[k]
  else:return None
 return cur
def setv(o,path,v):
 cur=o;ps=path.split('.')
 for k in ps[:-1]:cur=cur.setdefault(k,{})
 cur[ps[-1]]=v
def event(ws,t,payload):
 f=ws/'history/events.ndjson';f.parent.mkdir(parents=True,exist_ok=True)
 with f.open('a',encoding='utf-8') as h:h.write(json.dumps({'timestamp':now(),'type':t,'payload':payload},ensure_ascii=False)+'\n')
def validate_canon(c):
 e=[]
 if c.get('schema_version')!=SCHEMA:e.append('schema_version must be 3.1')
 for p in ['meta','root_canon.identity','root_canon.body_core','root_canon.face_core','root_canon.identity_details','strong_reference.hair','strong_reference.costume','strong_reference.palette_accessories','variants','production_spec','consistency_lock','qa']:
  if get(c,p) is None:e.append('missing '+p)
 return e
def project(ws):
 c=load(ws/'canon/canon.json');chap=ws/'canon/chapters';chap.mkdir(parents=True,exist_ok=True)
 links=[]
 for slug,title,paths in CHAPTERS:
  body=['# '+title,'']
  for p in paths:body+=['## `'+p+'`','```json',json.dumps(get(c,p),ensure_ascii=False,indent=2),'```','']
  atomic(chap/(slug+'.md'),'\n'.join(body));links.append(f'- [{title}](canon/chapters/{slug}.md)')
 atomic(ws/'INDEX.md','# '+c['meta']['name']+'\n\n'+'\n'.join(links)+'\n')
 compact={'name':c['meta']['name'],'revision':c['meta']['revision'],'root_canon':c['root_canon'],'strong_reference':c['strong_reference'],'consistency_lock':c['consistency_lock'],'open_issues':c['qa'].get('unresolved',[]),'next':'Continue active batch or review readiness.'}
 atomic(ws/'ACTIVE_CONTEXT.md','# ACTIVE OC CONTEXT\n\n```json\n'+json.dumps(compact,ensure_ascii=False,indent=2)+'\n```\n')
def init(ws,name,template):
 ws=Path(ws)
 if (ws/'canon/canon.json').exists():raise ValueError('workspace exists')
 c=load(template);c['meta'].update({'id':str(uuid.uuid4()),'name':name,'created_at':now(),'updated_at':now(),'revision':0})
 for d in ['canon/chapters','interview/batches','history/commits','snapshots','handoff']: (ws/d).mkdir(parents=True,exist_ok=True)
 dump(ws/'canon/canon.json',c);atomic(ws/'history/events.ndjson','');event(ws,'initialized',{'name':name});project(ws)
def queue(ws,file):
 ws=Path(ws);b=load(file);c=load(ws/'canon/canon.json')
 if b['base_revision']!=c['meta']['revision']:raise ValueError('stale base_revision')
 dst=ws/'interview/batches'/f"{b['batch_id']}.questions.json"
 if dst.exists() and sha(dst)!=sha(file):raise ValueError('batch id collision')
 shutil.copyfile(file,dst);dump(ws/'interview/pending.json',b);event(ws,'question_batch_queued',{'batch_id':b['batch_id']})
def apply(c,u):
 p=u['path'];op=u.get('op','set');v=u.get('value')
 if not p.startswith(ALLOWED):raise ValueError('unregistered path: '+p)
 old=get(c,p);policy=u.get('revision_policy','create_or_confirm')
 if old not in (None,[],{},'') and old!=v and policy!='revise':raise ValueError('explicit revision required: '+p)
 if policy=='revise':
  if 'expected_old' not in u or old!=u['expected_old']:raise ValueError('expected_old mismatch: '+p)
  if not u.get('reason'):raise ValueError('revision reason required: '+p)
 if op=='set':setv(c,p,v)
 elif op=='append':
  a=get(c,p)
  if a is None:a=[];setv(c,p,a)
  if not isinstance(a,list):raise ValueError('append target is not list: '+p)
  if v not in a:a.append(v)
 elif op=='merge':
  d=get(c,p)
  if d is None:d={};setv(c,p,d)
  if not isinstance(d,dict) or not isinstance(v,dict):raise ValueError('merge requires objects: '+p)
  d.update(v)
 elif op=='remove':setv(c,p,None)
 else:raise ValueError('unsupported op: '+op)
def commit(ws,file,dry=False):
 ws=Path(ws);b=load(file);c=load(ws/'canon/canon.json');cp=ws/'history/commits'/f"{b['batch_id']}.json";digest=sha(file)
 if cp.exists():
  r=load(cp)
  if r['answer_sha256']==digest:print(json.dumps(r,ensure_ascii=False,indent=2));return
  raise ValueError('batch id already committed')
 if b['base_revision']!=c['meta']['revision']:raise ValueError('stale base_revision')
 n=copy.deepcopy(c)
 for u in b.get('updates',[]):apply(n,u)
 errs=validate_canon(n)
 if errs:raise ValueError('; '.join(errs))
 n['meta']['revision']+=1;n['meta']['updated_at']=now();rec={'batch_id':b['batch_id'],'answer_sha256':digest,'from_revision':c['meta']['revision'],'to_revision':n['meta']['revision'],'committed_at':now()}
 if dry:print(json.dumps({'ok':True,'record':rec,'canon':n},ensure_ascii=False,indent=2));return
 dump(ws/'canon/canon.json',n);dump(cp,rec);shutil.copyfile(file,ws/'interview/batches'/f"{b['batch_id']}.answers.json")
 p=ws/'interview/pending.json'
 if p.exists():p.unlink()
 event(ws,'answer_batch_committed',rec);project(ws);print(json.dumps(rec,ensure_ascii=False,indent=2))
def checkpoint(ws,label):
 ws=Path(ws);c=load(ws/'canon/canon.json');dst=ws/'snapshots'/f"r{c['meta']['revision']:04d}-{label}";dst.mkdir(parents=True,exist_ok=False);shutil.copy2(ws/'canon/canon.json',dst/'canon.json');event(ws,'checkpoint',{'path':str(dst)})
def status(ws):
 c=load(Path(ws)/'canon/canon.json');print(json.dumps({'name':c['meta']['name'],'revision':c['meta']['revision'],'schema':c['schema_version'],'errors':validate_canon(c)},ensure_ascii=False,indent=2))
def validate(ws):
 ws=Path(ws);c=load(ws/'canon/canon.json');e=validate_canon(c)
 print(json.dumps({'ok':not e,'errors':e,'revision':c['meta']['revision']},ensure_ascii=False,indent=2));raise SystemExit(1 if e else 0)
def main():
 ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
 x=sp.add_parser('init');x.add_argument('workspace');x.add_argument('--name',required=True);x.add_argument('--template',default=str(Path(__file__).parents[1]/'templates/oc-workspace/canon.template.json'))
 for cmd in ['queue-batch','commit-batch']:
  x=sp.add_parser(cmd);x.add_argument('workspace');x.add_argument('--file',required=True);x.add_argument('--dry-run',action='store_true') if cmd=='commit-batch' else None
 x=sp.add_parser('render');x.add_argument('workspace');x=sp.add_parser('checkpoint');x.add_argument('workspace');x.add_argument('--label',default='checkpoint')
 x=sp.add_parser('status');x.add_argument('workspace');x=sp.add_parser('validate');x.add_argument('workspace')
 a=ap.parse_args()
 try:
  {'init':lambda:init(a.workspace,a.name,a.template),'queue-batch':lambda:queue(a.workspace,a.file),'commit-batch':lambda:commit(a.workspace,a.file,a.dry_run),'render':lambda:project(Path(a.workspace)),'checkpoint':lambda:checkpoint(a.workspace,a.label),'status':lambda:status(a.workspace),'validate':lambda:validate(a.workspace)}[a.cmd]()
 except Exception as e:print('ERROR:',e,file=sys.stderr);raise SystemExit(2)
if __name__=='__main__':main()
