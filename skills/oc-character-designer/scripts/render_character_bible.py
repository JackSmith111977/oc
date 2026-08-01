#!/usr/bin/env python3
"""Render a lightweight landscape character-bible PDF from JSON page data."""
from pathlib import Path
import argparse, json
try:
 from reportlab.pdfgen import canvas
 from reportlab.lib.pagesizes import A4, landscape
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
except ImportError as e: raise SystemExit('reportlab is required') from e

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def font():
 for p in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
  if Path(p).exists():pdfmetrics.registerFont(TTFont('Body',p));return 'Body'
 return 'Helvetica'
def wrap(c,text,x,y,w,size,leading):
 words=list(str(text));line='';yy=y
 for ch in words:
  if c.stringWidth(line+ch,'Body',size)>w:
   c.drawString(x,yy,line);yy-=leading;line=ch
  else:line+=ch
 if line:c.drawString(x,yy,line)
 return yy
def render(project,pages,out,preset):
 pr=load(project);pd=load(pages);f=font();size=(960,540) if preset=='digital-16x9' else landscape(A4);c=canvas.Canvas(str(out),pagesize=size)
 for n,page in enumerate(pd['pages'],1):
  W,H=size;c.setFont(f,20);c.drawString(36,H-42,f"{page['code']}  {page['title']}");c.setFont(f,8);c.drawRightString(W-36,H-38,f"{pr.get('character_name','')} · REV {pr.get('canon_revision',0)}")
  x,y,w,h=36,52,W-72,H-112;c.rect(x,y,w,h);c.setFont(f,11);c.drawCentredString(W/2,y+h/2+12,'视觉资产区域 / VISUAL ASSET ZONE');c.setFont(f,8);c.drawCentredString(W/2,y+h/2-8,'由图像生成或批准资产填充；正式说明通过矢量文字覆盖')
  c.setFont(f,7);c.drawString(36,24,f"模板 {pr.get('template_version','1.1.0')} · 技能 {pr.get('skill_version','3.1.2')}");c.drawRightString(W-36,24,str(n));c.showPage()
 c.save()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--pages',required=True);ap.add_argument('--output',required=True);ap.add_argument('--preset',choices=['digital-16x9','a4-landscape'],default='digital-16x9');a=ap.parse_args();render(a.project,a.pages,a.output,a.preset)
if __name__=='__main__':main()
