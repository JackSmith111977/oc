#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, shutil, datetime, uuid, copy, sys

ALLOWED_PREFIXES=('selection.','direction.','production.','qa.','continuity.')
ROOT_READONLY=('source.','identity_contract.')

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p): return json.load(open(p,encoding='utf-8'))
def atomic_json(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding='utf-8'); t.replace(p)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def get(obj,path):
    cur=obj
    for k in path.split('.'):
        if not isinstance(cur,dict) or k not in cur: return None
        cur=cur[k]
    return cur
def setv(obj,path,val):
    cur=obj; parts=path.split('.')
    for k in parts[:-1]: cur=cur.setdefault(k,{})
    cur[parts[-1]]=val
def append_event(ws,typ,payload):
    p=ws/'history/events.ndjson'; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a',encoding='utf-8') as f: f.write(json.dumps({'timestamp':now(),'type':typ,'payload':payload},ensure_ascii=False)+'\n')
def verify_handoff(h):
    m=load(h/'manifest.json')
    for key,v in m['files'].items():
        p=h/v['path']
        if not p.exists() or sha(p)!=v['sha256']: raise ValueError(f'handoff hash mismatch: {key}')
    return m

def render(ws):
    p=load(ws/'state/project.json'); ic=load(ws/'state/identity-contract.json')
    lines=[f"# {p['meta']['title']}","",f"- Project revision: {p['meta']['revision']}",f"- Character: {p['source']['character_name']}",f"- Source revision: {p['source']['source_revision']}","",'## Root identity (read-only)',json.dumps(ic.get('root_canon',{}),ensure_ascii=False,indent=2),"",'## Selected appearance',json.dumps(p.get('selection',{}),ensure_ascii=False,indent=2),"",'## Direction',json.dumps(p.get('direction',{}),ensure_ascii=False,indent=2),"",'## Next',p.get('meta',{}).get('next_action','Continue staged interview or compile when ready.')]
    (ws/'ACTIVE_CONTEXT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (ws/'INDEX.md').write_text(f"# {p['meta']['title']}\n\n- [Active context](ACTIVE_CONTEXT.md)\n- [Director brief](DIRECTOR_BRIEF.md)\n- [Prompt pack](prompts/PROMPT_PACK.md)\n- [QA report](qa/QA_REPORT.md)\n",encoding='utf-8')

def init(ws,handoff,title):
    m=verify_handoff(handoff); ws.mkdir(parents=True,exist_ok=True)
    for d in ['source/handoff','state','interview/batches','prompts','continuity','feedback/upstream-change-requests','history/commits','snapshots','qa','outputs']:(ws/d).mkdir(parents=True,exist_ok=True)
    if (ws/'state/project.json').exists(): raise ValueError('workspace exists')
    shutil.copytree(handoff,ws/'source/handoff',dirs_exist_ok=True)
    root=load(handoff/'root-canon.json'); strong=load(handoff/'strong-reference.json'); variants=load(handoff/'approved-variants.json'); lock=load(handoff/'consistency-lock.json')
    manifest_hash=sha(handoff/'manifest.json')
    ic={'source_revision':m['source_revision'],'manifest_sha256':manifest_hash,'root_canon':root,'strong_reference':strong,'approved_variants':variants,'consistency_lock':lock}
    atomic_json(ws/'state/identity-contract.json',ic)
    project={'schema_version':'2.0','meta':{'project_id':str(uuid.uuid4()),'title':title,'revision':0,'created_at':now(),'updated_at':now(),'next_action':'Select deliverable and approved appearance state.'},'source':{'character_id':m['character_id'],'character_name':m['character_name'],'source_revision':m['source_revision'],'manifest_sha256':manifest_hash},'selection':{'hair_state':'default','outfit_state':'default','accessory_state':'default','character_state':None},'direction':{'deliverable':None,'narrative':{},'acting':{},'camera':{},'scene':{},'lighting':{},'style':{}},'production':{'target_model':None,'aspect_ratio':None,'series_mode':False,'prompt_status':'draft'},'qa':{'blocking':[],'warnings':[],'last_review':None},'continuity':{}}
    atomic_json(ws/'state/project.json',project); render(ws); append_event(ws,'workspace_initialized',{'source_revision':m['source_revision']})

def queue(ws,file):
    b=load(file); p=load(ws/'state/project.json')
    if b['base_revision']!=p['meta']['revision']: raise ValueError('stale base_revision')
    dst=ws/'interview/batches'/f"{b['batch_id']}.questions.json"
    if dst.exists() and sha(dst)!=sha(file): raise ValueError('batch id collision')
    shutil.copyfile(file,dst); atomic_json(ws/'interview/pending.json',b); append_event(ws,'question_batch_queued',{'batch_id':b['batch_id']})

def apply_update(obj,u):
    path=u['path']
    if not path.startswith(ALLOWED_PREFIXES) or path.startswith(ROOT_READONLY): raise ValueError(f'forbidden path: {path}')
    old=get(obj,path); policy=u.get('revision_policy','create_or_confirm')
    if old is not None and old!=u.get('value') and policy!='revise': raise ValueError(f'explicit revision required: {path}')
    if policy=='revise' and 'expected_old' in u and old!=u['expected_old']: raise ValueError(f'expected_old mismatch: {path}')
    op=u['op']; val=u.get('value')
    if op=='set': setv(obj,path,val)
    elif op=='append':
        arr=get(obj,path)
        if arr is None: arr=[]; setv(obj,path,arr)
        if not isinstance(arr,list): raise ValueError(f'not list: {path}')
        arr.append(val)
    elif op=='merge':
        cur=get(obj,path)
        if cur is None: cur={}; setv(obj,path,cur)
        if not isinstance(cur,dict) or not isinstance(val,dict): raise ValueError(f'not object: {path}')
        cur.update(val)
    elif op=='remove':
        setv(obj,path,None)
    else: raise ValueError(f'unsupported op: {op}')

def commit(ws,file,dry):
    b=load(file); p=load(ws/'state/project.json')
    commit_path=ws/'history/commits'/f"{b['batch_id']}.json"
    digest=sha(file)
    if commit_path.exists():
        old=load(commit_path)
        if old['answer_sha256']==digest: print(json.dumps(old,ensure_ascii=False,indent=2)); return
        raise ValueError('batch id already committed with different content')
    if b['base_revision']!=p['meta']['revision']: raise ValueError('stale base_revision')
    new=copy.deepcopy(p)
    for u in b.get('updates',[]): apply_update(new,u)
    new['meta']['revision']+=1; new['meta']['updated_at']=now(); new['meta']['next_action']='Continue staged interview or compile when ready.'
    record={'batch_id':b['batch_id'],'answer_sha256':digest,'from_revision':p['meta']['revision'],'to_revision':new['meta']['revision'],'committed_at':now()}
    if dry: print(json.dumps({'ok':True,'dry_run':True,'record':record,'project':new},ensure_ascii=False,indent=2)); return
    atomic_json(ws/'state/project.json',new); atomic_json(commit_path,record)
    shutil.copyfile(file,ws/'interview/batches'/f"{b['batch_id']}.answers.json")
    pending=ws/'interview/pending.json'
    if pending.exists(): pending.unlink()
    append_event(ws,'answer_batch_committed',record); render(ws); print(json.dumps(record,ensure_ascii=False,indent=2))

def compile_prompt(ws):
    p=load(ws/'state/project.json'); ic=load(ws/'state/identity-contract.json')
    root=ic['root_canon']; strong=ic['strong_reference']; variants=ic['approved_variants']
    text=f"""# Prompt Pack\n\n## Identity contract\n\nROOT BODY: {json.dumps(root.get('body_core',{}),ensure_ascii=False)}\n\nROOT FACE: {json.dumps(root.get('face_core',{}),ensure_ascii=False)}\n\nPERMANENT DETAILS: {json.dumps(root.get('identity_details',{}),ensure_ascii=False)}\n\nSELECTED APPEARANCE: {json.dumps(p.get('selection',{}),ensure_ascii=False)}\n\nSTRONG REFERENCE: {json.dumps(strong,ensure_ascii=False)}\n\nAPPROVED VARIANTS: {json.dumps(variants,ensure_ascii=False)}\n\n## Direction\n\n{json.dumps(p.get('direction',{}),ensure_ascii=False,indent=2)}\n\n## Production\n\n{json.dumps(p.get('production',{}),ensure_ascii=False,indent=2)}\n\n## Compiled semantic prompt\n\nCreate the requested illustration of the exact character defined above. Preserve root body proportions, root facial construction, apparent age and permanent identity details. Use only the selected approved hair, outfit, accessory and character state. Apply the confirmed acting, camera, scene, lighting, color and style direction. Do not introduce unapproved permanent design changes.\n\n## Negative constraints\n\nwrong body proportions, changed face shape or eye/nose/mouth relationship, wrong apparent age, missing permanent identity details, unapproved hairstyle or outfit, anatomy errors, hand errors, unauthorized extra characters, text, watermark, signature\n"""
    (ws/'prompts/PROMPT_PACK.md').write_text(text,encoding='utf-8')
    brief=f"# Director Brief\n\nCharacter: {p['source']['character_name']}\n\nSource revision: {p['source']['source_revision']}\n\n## Selected appearance\n{json.dumps(p['selection'],ensure_ascii=False,indent=2)}\n\n## Direction\n{json.dumps(p['direction'],ensure_ascii=False,indent=2)}\n\n## Production\n{json.dumps(p['production'],ensure_ascii=False,indent=2)}\n"
    (ws/'DIRECTOR_BRIEF.md').write_text(brief,encoding='utf-8')
    (ws/'qa/QA_REPORT.md').write_text('# QA Report\n\n- [ ] Root body preserved\n- [ ] Root face preserved\n- [ ] Permanent identity details preserved\n- [ ] Appearance state approved\n- [ ] Narrative/camera/scene/light coherent\n- [ ] Safety and age presentation pass\n',encoding='utf-8')
    append_event(ws,'prompt_compiled',{'revision':p['meta']['revision']}); render(ws)

def change_request(ws,file):
    req=load(file); p=load(ws/'state/project.json')
    if req['character_id']!=p['source']['character_id'] or req['source_revision']!=p['source']['source_revision']: raise ValueError('source mismatch')
    out=ws/'feedback/upstream-change-requests'/f"{req['request_id']}.json"; atomic_json(out,req); append_event(ws,'upstream_change_requested',{'request_id':req['request_id']}); print(out)

def validate(ws):
    p=load(ws/'state/project.json'); ic=load(ws/'state/identity-contract.json'); h=ws/'source/handoff'
    m=verify_handoff(h)
    errs=[]
    if p['source']['source_revision']!=m['source_revision']: errs.append('source revision mismatch')
    if p['source']['manifest_sha256']!=sha(h/'manifest.json'): errs.append('manifest hash mismatch')
    for key in ['body_core','face_core','identity_details']:
        if key not in ic.get('root_canon',{}): errs.append(f'missing root_canon.{key}')
    print(json.dumps({'ok':not errs,'errors':errs,'revision':p['meta']['revision']},ensure_ascii=False,indent=2))
    if errs: raise SystemExit(1)

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    x=sp.add_parser('init'); x.add_argument('workspace'); x.add_argument('--handoff',required=True); x.add_argument('--title',required=True)
    x=sp.add_parser('queue-batch'); x.add_argument('workspace'); x.add_argument('--file',required=True)
    x=sp.add_parser('commit-batch'); x.add_argument('workspace'); x.add_argument('--file',required=True); x.add_argument('--dry-run',action='store_true')
    x=sp.add_parser('compile'); x.add_argument('workspace')
    x=sp.add_parser('status'); x.add_argument('workspace')
    x=sp.add_parser('validate'); x.add_argument('workspace')
    x=sp.add_parser('propose-upstream-change'); x.add_argument('workspace'); x.add_argument('--file',required=True)
    a=ap.parse_args(); ws=Path(getattr(a,'workspace',''))
    try:
        if a.cmd=='init': init(ws,Path(a.handoff),a.title)
        elif a.cmd=='queue-batch': queue(ws,Path(a.file))
        elif a.cmd=='commit-batch': commit(ws,Path(a.file),a.dry_run)
        elif a.cmd=='compile': compile_prompt(ws)
        elif a.cmd=='status': print((ws/'ACTIVE_CONTEXT.md').read_text(encoding='utf-8'))
        elif a.cmd=='validate': validate(ws)
        elif a.cmd=='propose-upstream-change': change_request(ws,Path(a.file))
    except Exception as e:
        print(f'ERROR: {e}',file=sys.stderr); raise SystemExit(2)
if __name__=='__main__': main()
