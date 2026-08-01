#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, sys
ROOT=Path(__file__).parents[1]
def files():return sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts)
def manifest(v):return {'package':'oc-character-designer','version':v,'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files()]}
def check():
 v=(ROOT/'VERSION').read_text().strip();errs=[]
 if f'v{v}' not in (ROOT/'README.md').read_text():errs.append('README version')
 if f'version: "{v}"' not in (ROOT/'SKILL.md').read_text():errs.append('SKILL version')
 if f'## {v} ' not in (ROOT/'CHANGELOG.md').read_text():errs.append('CHANGELOG version')
 if f'version: {v}' not in (ROOT/'governance/MODULE_REGISTRY.yaml').read_text():errs.append('registry version')
 m=json.loads((ROOT/'manifest.json').read_text()) if (ROOT/'manifest.json').exists() else {}
 if m.get('version')!=v:errs.append('manifest version')
 print(json.dumps({'ok':not errs,'version':v,'errors':errs},ensure_ascii=False,indent=2));return not errs
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write-manifest',action='store_true');ap.add_argument('--check',action='store_true');a=ap.parse_args();v=(ROOT/'VERSION').read_text().strip()
 if a.write_manifest:(ROOT/'manifest.json').write_text(json.dumps(manifest(v),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if a.check and not check():raise SystemExit(1)
if __name__=='__main__':main()
