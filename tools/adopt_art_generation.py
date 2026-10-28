"""Adopt actual built-in outputs and preserve unknown model/quality faithfully."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib, json, shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
GEN=Path(r'C:\Users\luyua\.codex\generated_images\01a17787-b8fd-7f30-a97f-1c03f4aa7770')
STYLE=[Path(r'F:\work\image\designs\mail-ui-v1\01-mail-event.png'),Path(r'F:\work\image\designs\team-ui-v2\team-ui-v2.png')]
CONFIG=json.loads(Path(r'F:\work\image\config\image-generation.json').read_text(encoding='utf-8-sig'))
JOBS=[
 ('exec-e0a4a52e-ca69-4566-af52-e8c9ac88d18c.png','backgrounds/expedition-playfield.png','expedition-playfield',False,STYLE+[ROOT/'assets/art/survivor-keyart.png']),
 ('exec-4ebfef17-cd63-4c1d-b734-cf5c172a07f2.png','characters/hero-survivor.png','hero-survivor',True,[ROOT/'assets/art/survivor-keyart.png']+STYLE),
 ('exec-a206da0a-57ae-43a7-be67-72d36a156294.png','icons/survival-icons-master.png','survival-icons',True,STYLE),
 ('exec-bea38321-7725-4c8a-8992-a8e2d0a9bc37.png','backgrounds/regional-map.png','regional-map',False,STYLE),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for native,name,prompt,transparent,refs in JOBS:
    src=GEN/native; dst=ROOT/'art-delivery/resources'/name
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copyfile(src,dst)
    assert sha(src)==sha(dst),str(dst)
    with Image.open(dst) as im:
        alpha=im.getchannel('A').getextrema() if 'A' in im.getbands() else None
        if transparent: assert alpha and alpha[0]==0 and alpha[1]>240,(name,alpha)
        record=dict(file=str(dst.relative_to(ROOT)).replace('\\','/'),sha256=sha(dst),
          generatedAt=datetime.fromtimestamp(src.stat().st_mtime,timezone(timedelta(hours=-4))).isoformat(),
          width=im.width,height=im.height,format=im.format,mode=im.mode,alphaExtrema=alpha,
          tool='image_gen.imagegen',route='builtin',art_source='host_image',configSnapshot=CONFIG,
          submittedParameters=dict(model=None,quality=None,transparent_background=transparent,referenced_image_paths=[str(r) for r in refs]),
          actualModel=None,actualQuality=None,unverifiedReason='宿主管理；工具只返回 image_url/output_hint，未披露实际型号或质量。配置目标不是返回证明。',
          prompt=f'art-delivery/records/{prompt}.prompt.txt',
          references=[dict(file=str(r),sha256=sha(r),usage='identity reference' if 'survivor-keyart' in str(r) else 'actual style image input') for r in refs],
          evidence=dict(sourceOutput=str(src),returnedFields=['image_url','output_hint'],pngMetadataKeys=list(im.info)),
          operation='Byte-for-byte adoption of native model output; no resize/crop/edit',nativeOutputPreserved=True)
    dst.with_name(dst.name+'.generation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(name,record['width'],record['height'],record['mode'],alpha)
# Existing confirmed art is reused with its own old record; never relabel its model.
src=ROOT/'assets/art/survivor-keyart.png'; dst=ROOT/'art-delivery/resources/backgrounds/entry-keyart.png'
if not dst.exists():shutil.copyfile(src,dst)
dst.with_name(dst.name+'.source.json').write_text(json.dumps(dict(file=str(dst.relative_to(ROOT)).replace('\\','/'),sha256=sha(dst),derivedFrom=dict(file='assets/art/survivor-keyart.png',sha256=sha(src),generationRecord='assets/art/survivor-keyart.png.generation.json'),operation='Byte-for-byte reuse of approved entry illustration'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
