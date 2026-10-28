"""Verify a bounded shared-template repair against temporary PNG baselines."""
from pathlib import Path
from PIL import Image,ImageChops
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art-delivery'
record=OUT/'records/state-ghost-repair.json';data=json.loads(record.read_text(encoding='utf-8'))
baseline=Path(data['baselineDirectory']);allowed=[86,235,328,938]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
main=[dict(file=f'art-delivery/designs/screens/{name}',before=value,after=sha(OUT/'designs/screens'/name)) for name,value in data['beforeMainHashes'].items()]
states=[]
for name,value in data['beforeStateHashes'].items():
    before=baseline/name;after=OUT/'designs/states'/name
    assert sha(before)==value
    with Image.open(before) as a,Image.open(after) as b:
        box=ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox()
    bounded=box is None or (box[0]>=allowed[0] and box[1]>=allowed[1] and box[2]<=allowed[2] and box[3]<=allowed[3])
    states.append(dict(file=f'art-delivery/designs/states/{name}',before=value,after=sha(after),changedPixelBoundingBox=box,withinAllowedHiddenLayerRegion=bounded))
data.update(afterFreeze=True,allowedChangedRegion=allowed,mainScreensByteIdentical=all(x['before']==x['after'] for x in main),mainScreens=main,stateBoards=states,allStateDifferencesBounded=all(x['withinAllowedHiddenLayerRegion'] for x in states),method='Pillow RGB pixel difference and SHA256; only hidden navigation/sample-footnote region may change. Content, labels and action coordinates were not edited.',baselineRetainedTemporarily=True)
data['overallStatus']='passed' if data['mainScreensByteIdentical'] and data['allStateDifferencesBounded'] else 'needs-revision'
record.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=data['overallStatus'],mainScreens=len(main),mainByteIdentical=data['mainScreensByteIdentical'],stateBoards=len(states),uniqueDeltaBounds=sorted({tuple(x['changedPixelBoundingBox'] or []) for x in states})),ensure_ascii=False))
if data['overallStatus']!='passed':raise SystemExit(1)
