#!/usr/bin/env python3
from pathlib import Path
import tempfile, subprocess, json, sys
ROOT=Path(__file__).resolve().parents[1]
UP=Path('/mnt/data/oc-character-designer-skill/examples/v3.1/harbor-courier-canon.json')
if not UP.exists():
    UP=ROOT/'examples/harbor-courier-canon.json'
with tempfile.TemporaryDirectory() as td:
    td=Path(td); h=td/'handoff'; ws=td/'project'
    subprocess.run([sys.executable,str(ROOT/'scripts/build_handoff.py'),'--canon',str(UP),'--output',str(h)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/illustration_workspace.py'),'init',str(ws),'--handoff',str(h),'--title','self test'],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/illustration_workspace.py'),'queue-batch',str(ws),'--file',str(ROOT/'examples/I1-B01.questions.json')],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/illustration_workspace.py'),'commit-batch',str(ws),'--file',str(ROOT/'examples/I1-B01.answers.json')],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/illustration_workspace.py'),'compile',str(ws)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/illustration_workspace.py'),'validate',str(ws)],check=True)
    p=json.load(open(ws/'state/project.json',encoding='utf-8'))
    assert p['meta']['revision']==1 and p['direction']['deliverable']=='角色主视觉'
print('ok')
