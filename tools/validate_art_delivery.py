"""Validate art contracts and provenance without claiming Unity/runtime acceptance.

Optional contact sheets are review aids, not automated visual approval.
"""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse, csv, hashlib, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art-delivery'
REF=ROOT/'reference/Cataclysm-DDA'
FONT=OUT/'resources/fonts/NotoSansCJKsc-Regular.otf'
COMMIT='eb86dffd20072d6fde54af568cf229f3cd4d751f'

def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rel(path):return str(Path(path).relative_to(ROOT)).replace('\\','/')
def write(path,data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def labels(feature):
    result=[]
    for value in feature.get('states',[]):
        result.append(value.get('name') or value.get('title') or value.get('id') if isinstance(value,dict) else str(value))
    return result

class Links(HTMLParser):
    def __init__(self):super().__init__();self.values=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('src','href') and value:self.values.append(value)

class Audit:
    def __init__(self):self.checks=[];self.images={};self.hashes={};self.fonts={}
    def check(self,name,passed,evidence=None):
        self.checks.append(dict(id=name,passed=bool(passed),evidence=evidence))
    def hash(self,path):
        path=Path(path)
        if not path.is_file():return None
        key=(str(path),path.stat().st_mtime_ns,path.stat().st_size)
        if key not in self.hashes:self.hashes[key]=digest(path)
        return self.hashes[key]
    def image(self,path):
        path=Path(path)
        try:
            with Image.open(path) as image:
                image.load()
                info=dict(size=list(image.size),mode=image.mode,format=image.format)
                if 'A' in image.getbands():info['alphaExtrema']=list(image.getchannel('A').getextrema())
            self.images[rel(path)]=info;return info
        except Exception as error:
            self.check('image-decode:'+str(path),False,str(error));return None
    def layout(self,path,expected=None):
        if not Path(path).is_file():self.check('layout-exists:'+str(path),False);return None
        item=load(path);output=ROOT/item['file'];info=self.image(output)
        self.check('layout-output-sha:'+item['file'],self.hash(output)==item['sha256'])
        self.check('layout-canvas:'+item['file'],item.get('canvas')==[1920,1080] and info and info['size']==[1920,1080])
        self.check('layout-phase:'+item['file'],'not Unity' in item.get('phase',''))
        for name,value in item.get('recipeInputs',{}).items():self.check('recipe-sha:'+item['file']+':'+name,self.hash(ROOT/name)==value)
        self.check('recipe-inputs-complete:'+item['file'],set(item.get('recipeInputs',{}))=={'tools/art_screens.py','tools/art_screen_data.py','docs/art-v2/copy-core.json','docs/art-v2/copy-advanced.json'})
        for source in item.get('derivedFrom',[]):
            self.check('source-sha:'+item['file']+':'+source['file'],self.hash(ROOT/source['file'])==source['sha256'])
            self.check('source-record:'+item['file']+':'+source['file'],(ROOT/source.get('record','')).is_file())
        self.check('font-available:'+item['file'],(ROOT/item.get('fontFile','')).is_file())
        extent_errors=[]
        for text in item.get('textAreas',[]):
            x,y,width,height=text['rect']
            if not(0<=x<1920 and 0<=y<1080 and x+width<=1920.1 and y+height<=1080.1):extent_errors.append(dict(id=text['id'],rect=text['rect'],text=text['displayText']))
        self.check('text-canvas-bounds:'+item['file'],not extent_errors,extent_errors)
        if expected is not None:self.check('layout-feature-id:'+item['file'],item['id']==expected)
        return item

def contact_sheets(master,selection='core'):
    source=load(ROOT/f'docs/art-v2/research-{selection}.json')
    selected={item['id'] for item in source['features']}
    features=[item for item in master['features'] if item['id'] in selected]
    contact_dir=OUT/'previews/review-core';contact_dir.mkdir(parents=True,exist_ok=True)
    thumb_w,thumb_h=920,518;gap=28;top=78;label_h=54
    sheets=[];face=ImageFont.truetype(str(FONT),23);heading=ImageFont.truetype(str(FONT),31)
    for page in range((len(features)+5)//6):
        batch=features[page*6:page*6+6]
        image=Image.new('RGB',(1920,1840),'#e9e3d0');draw=ImageDraw.Draw(image)
        draw.text((30,20),f'核心界面视觉复核 · {page+1} / {(len(features)+5)//6}',font=heading,fill='#214d41')
        entries=[]
        for i,item in enumerate(batch):
            x=28+(i%2)*(thumb_w+gap);y=top+(i//2)*(thumb_h+label_h+18)
            path=ROOT/item['designFile']
            with Image.open(path) as screen:thumb=ImageOps.fit(screen.convert('RGB'),(thumb_w,thumb_h),method=Image.Resampling.LANCZOS)
            image.paste(thumb,(x,y));draw.text((x,y+thumb_h+8),item['id']+' · '+item['title'],font=face,fill='#214d41')
            entries.append(dict(id=item['id'],file=item['designFile'],sha256=digest(path)))
        path=contact_dir/f'core-{page+1:02d}.jpg';image.save(path,quality=94)
        sheets.append(dict(file=rel(path),sha256=digest(path),sourceImages=entries))
    write(OUT/'records/CORE_CONTACT_SHEETS.json',dict(method='Six actual screen thumbnails per sheet; review aid only, not automatic approval',sheets=sheets))
    print('Contact sheets:',len(sheets),'core screens:',len(features))
    return sheets

def state_contact_sheets(master):
    """Make legible, hash-bound review sheets; viewing them is still required."""
    selected={f['id'] for f in load(ROOT/'docs/art-v2/research-core.json')['features']}|{'common-dialogs'}
    boards=[(f,file) for f in master['features'] if f['id'] in selected for file in f['statePreviewFiles']]
    directory=OUT/'previews/review-core';directory.mkdir(parents=True,exist_ok=True)
    face=ImageFont.truetype(str(FONT),23);sheets=[]
    # Four large thumbnails per sheet retain 23px board copy at approximately 11px.
    for page in range((len(boards)+3)//4):
        sheet=Image.new('RGB',(1920,1250),'#e9e3d0');draw=ImageDraw.Draw(sheet);entries=[]
        draw.text((28,14),f'核心状态视觉复核 · {page+1}',font=face,fill='#214d41')
        for i,(feature,file) in enumerate(boards[page*4:page*4+4]):
            x=28+(i%2)*948;y=60+(i//2)*590;path=ROOT/file
            with Image.open(path) as image:thumb=image.convert('RGB').resize((920,518),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(x,y));draw.text((x,y+525),Path(file).stem,font=face,fill='#214d41')
            entries.append(dict(id=feature['id'],file=file,sha256=digest(path)))
        file=directory/f'core-states-{page+1:02d}.jpg';sheet.save(file,quality=95)
        sheets.append(dict(file=rel(file),sha256=digest(file),sourceImages=entries))
    write(OUT/'records/CORE_STATE_CONTACT_SHEETS.json',dict(method='Actual state-board thumbnails; all contact sheets must be visually viewed before acceptance',sheets=sheets))
    print('Core state contact sheets:',len(sheets),'boards:',len(boards))
    return sheets

def run():
    audit=Audit();master=load(OUT/'records/ui-master-manifest.json')
    core=load(ROOT/'docs/art-v2/research-core.json');advanced=load(ROOT/'docs/art-v2/research-advanced.json')
    expected={item['id']:item for item in core['features']+advanced['features']};actual={item['id']:item for item in master['features']}
    audit.check('reference-commit',master.get('referenceCommit')==COMMIT)
    reference_head=subprocess.run(['git','-C',str(REF),'rev-parse','HEAD'],capture_output=True,text=True,check=False)
    audit.check('actual-reference-checkout-commit',reference_head.returncode==0 and reference_head.stdout.strip()==COMMIT,reference_head.stdout.strip())
    audit.check('reference-association-record',(ROOT/'docs/image-reference-associations.md').is_file())
    audit.check('reference-feature-coverage',set(expected)<=set(actual),dict(missing=sorted(set(expected)-set(actual)),referenceCount=len(expected),deliveredFamilies=len(actual)))
    audit.check('common-dialogue-family','common-dialogs' in actual)
    audit.check('unique-feature-ids',len(actual)==len(master['features']))
    state_count=0;boards=0
    copies={}
    for name in ['copy-core.json','copy-advanced.json']:copies.update(load(ROOT/'docs/art-v2'/name))
    for item in master['features']:
        id=item['id'];normal=audit.layout(ROOT/item['layoutFile'],id)
        audit.check('screen-path:'+id,normal and normal.get('file')==item['designFile'])
        for source in item.get('source',[]):
            file=REF/source['file'];exists=file.is_file()
            audit.check('functional-source:'+id+':'+source['file'],exists)
            if exists and source.get('line'):
                count=len(file.read_text(encoding='utf-8',errors='replace').splitlines())
                audit.check('source-line:'+id+':'+source['file'],1<=source['line']<=count)
        controls=[]
        for board in item['statePreviewFiles']:
            path=OUT/'records/layouts'/(Path(board).stem+'.json');data=audit.layout(path,id)
            boards+=1
            if data:controls+=data.get('stateControls',[])
        expected_labels=labels(expected.get(id,item))
        audit.check('state-label-coverage:'+id,[state['label'] for state in controls]==expected_labels,dict(expected=expected_labels,delivered=[state['label'] for state in controls]))
        feedback=copies.get(id,{}).get('stateFeedback',{})
        if id in expected:audit.check('explicit-state-feedback:'+id,set(expected_labels)<=set(feedback),sorted(set(expected_labels)-set(feedback)))
        for state in controls:
            state_count+=1;key=id+':'+state['label'];source=feedback.get(state['label'])
            audit.check('state-control-booleans:'+key,isinstance(state.get('primaryEnabled'),bool))
            audit.check('state-feedback-specific:'+key,bool(state.get('message')) and '为此系统的专属状态' not in state['message'])
            if source:
                wanted=source.get('primaryEnabled',not source.get('blocked',False))
                audit.check('state-control-semantics:'+key,state['primaryEnabled']==wanted)
                audit.check('state-feedback-copy:'+key,state['message']==source.get('message'))
            if not state['primaryEnabled']:audit.check('blocked-state-safe-exit:'+key,bool(state.get('secondaryLabel')))
    assets=load(OUT/'records/asset-manifest.json');families=defaultdict(list)
    for item in assets['assets']:
        file=ROOT/item['file'];image=audit.image(file);id=item['id']
        audit.check('asset-sha:'+id,audit.hash(file)==item['sha256'])
        audit.check('asset-size:'+id,image and image['size']==item['size'])
        audit.check('asset-alpha-record:'+id,image and image.get('alphaExtrema')==item.get('alphaExtrema'))
        l,b,r,t=item['borderLeftBottomRightTop'];w,h=item['size']
        audit.check('asset-border:'+id,min(l,b,r,t)>=0 and l+r<w and t+b<h)
        audit.check('asset-pivot:'+id,len(item['pivot'])==2 and all(0<=v<=1 for v in item['pivot']))
        audit.check('no-dynamic-baked-text:'+id,item.get('dynamicTextBaked') is False)
        if item.get('stateFamily'):families[item['stateFamily']].append(item)
        for origin in item.get('derivedFrom',[]):
            if origin.get('file'):path=ROOT/origin['file']
            elif origin.get('repositoryRelativePath'):path=Path(r'F:\work\image')/origin['repositoryRelativePath']
            else:continue
            audit.check('asset-native-source:'+id+':'+str(path),audit.hash(path)==origin.get('sha256'))
    for name,items in families.items():
        audit.check('state-family-size:'+name,len({tuple(item['size']) for item in items})==1)
        audit.check('state-family-alpha:'+name,all(item.get('mode')=='RGBA' and item['alphaExtrema'][0]==0 for item in items))
    font=assets['font'];audit.check('font-sha',audit.hash(ROOT/font['file'])==font['sha256']);audit.check('font-license-sha',audit.hash(ROOT/font['license'])==font['licenseSha256'])
    license_text=(ROOT/font['license']).read_text(encoding='utf-8-sig');audit.check('font-ofl','SIL OPEN FONT LICENSE' in license_text.upper())
    complete_file=OUT/'records/complete-resource-manifest.json';complete=load(complete_file)
    complete_assets=complete.get('assets',[]);complete_ids={item['id'] for item in complete_assets}
    audit.check('complete-index-count',len(complete_assets)==complete.get('formalIndependentSpriteCount')==112)
    audit.check('complete-index-base-manifest-current',complete['baseKitManifest']['sha256']==audit.hash(OUT/'records/asset-manifest.json'))
    audit.check('complete-index-kit-subset',{item['id'] for item in assets['assets']}<=complete_ids)
    audit.check('complete-index-unique',len(complete_ids)==len(complete_assets))
    for item in complete_assets:
        file=ROOT/item['file'];info=audit.image(file)
        audit.check('complete-asset-sha:'+item['id'],audit.hash(file)==item['sha256'])
        audit.check('complete-asset-size:'+item['id'],info and info['size']==item['size'])
        audit.check('complete-asset-alpha:'+item['id'],info and info.get('alphaExtrema')==item.get('alphaExtrema'))
        record=item.get('sourceRecord')
        if record:audit.check('complete-asset-source-record:'+item['id'],audit.hash(ROOT/record)==item.get('sourceRecordSha256'))
    csv_file=OUT/'records/unity-import-complete.csv'
    with csv_file.open(encoding='utf-8-sig',newline='') as source:csv_rows=list(csv.DictReader(source))
    audit.check('complete-import-csv-coverage',{item['id'] for item in csv_rows}==complete_ids and len(csv_rows)==112)
    indexed={item['id']:item for item in complete_assets}
    for row in csv_rows:
        item=indexed.get(row['id'],{})
        audit.check('complete-import-csv-values:'+row['id'],row.get('file')==item.get('file') and row.get('sha256')==item.get('sha256') and [int(row['width']),int(row['height'])]==item.get('size'))
        # Two source exporters explicitly label the same deferred engine stage.
        claim=row.get('unityValidation','').lower()
        audit.check('complete-import-not-unity-claim:'+row['id'],'not imported into unity' in claim or 'pending next unity stage' in claim)
    audit.check('complete-index-masters-excluded',len(complete.get('sourceOnly',[]))==2 and not ({x['file'] for x in complete.get('sourceOnly',[])} & {x['file'] for x in complete_assets}))
    for item in complete.get('sourceOnly',[]):
        audit.check('source-master-sha:'+item['file'],audit.hash(ROOT/item['file'])==item['sha256'])
        audit.check('source-master-generation:'+item['file'],audit.hash(ROOT/item['generationRecord'])==item['generationRecordSha256'])
    generations=list((OUT/'resources').rglob('*.generation.json'))
    for file in generations:
        data=load(file);image_path=ROOT/data['file'];info=audit.image(image_path)
        audit.check('generation-sha:'+rel(file),audit.hash(image_path)==data['sha256'])
        audit.check('generation-native-size:'+rel(file),info and info['size']==[data['width'],data['height']])
        audit.check('generation-actual-unknown-honest:'+rel(file),data.get('actualModel') is None and data.get('actualQuality') is None and bool(data.get('unverifiedReason')))
        parameters=data.get('submittedParameters',{});audit.check('generation-submitted-unknown:'+rel(file),parameters.get('model') is None and parameters.get('quality') is None)
        audit.check('generation-prompt:'+rel(file),(ROOT/data['prompt']).is_file())
        for reference in data.get('references',[]):
            origin=Path(reference['file']);origin=origin if origin.is_absolute() else ROOT/origin
            audit.check('generation-input-sha:'+rel(file)+':'+str(origin),audit.hash(origin)==reference['sha256'])
    gallery=OUT/'previews/index.html';links=Links();links.feed(gallery.read_text(encoding='utf-8'))
    for value in sorted(set(links.values)):
        parsed=urlsplit(value)
        if parsed.scheme or parsed.netloc or not parsed.path:continue
        path=(gallery.parent/unquote(parsed.path)).resolve()
        audit.check('gallery-link:'+value,path.is_file())
    flow=load(OUT/'records/flow-manifest.json');flow_ids=set()
    for key in ['png','svg']:
        output=flow['overview'];target=ROOT/output[key]
        audit.check('flow-overview-sha:'+key,audit.hash(target)==output.get(key+'Sha256'))
        if key=='png':
            info=audit.image(target);audit.check('flow-overview-canvas',info and info['size']==[1920,1080])
    for origin in flow.get('derivedFrom',[]):audit.check('flow-source:'+origin['file'],audit.hash(ROOT/origin['file'])==origin['sha256'])
    for group in flow['groups']:
        flow_ids.update(group.get('featureIDs',[]))
        for key in ['png','svg']:
            target=group.get('output',{}).get(key)
            if target:
                audit.check('flow-file:'+target,(ROOT/target).is_file())
                audit.check('flow-sha:'+target,audit.hash(ROOT/target)==group['output'].get(key+'Sha256'))
                if key=='png':
                    info=audit.image(ROOT/target);audit.check('flow-canvas:'+target,info and info['size']==[1920,1080])
    audit.check('flow-reference-coverage',set(expected)<=flow_ids,sorted(set(expected)-flow_ids))
    core_review_file=ROOT/'docs/art-v2/REVIEW_CORE_ART.json';advanced_file=ROOT/'docs/art-v2/REVIEW_ADVANCED.json'
    repair_path=OUT/'records/state-ghost-repair.json';repair=load(repair_path)
    transitions={item['file']:item for item in repair['stateBoards']}
    reviews={}
    for key,path in [('core',core_review_file),('advanced',advanced_file)]:
        reviews[key]=load(path) if path.exists() else dict(overallStatus='pending')
        audit.check('independent-visual-review:'+key,reviews[key].get('overallStatus') in ('passed','accepted','passed-after-revision','art-accepted'),reviews[key].get('overallStatus'))
        source_features=core['features'] if key=='core' else advanced['features']
        if key=='core':source_features=source_features+[actual['common-dialogs']]
        required_screens={actual[f['id']]['designFile'] for f in source_features}
        required_states={file for f in source_features for file in actual[f['id']]['statePreviewFiles']}
        reviewed=set()
        binding=reviews[key].get('boundedRepair',{}) if key=='core' else reviews[key].get('boundedRepairVerification',{})
        proof_sha=binding.get('sha256') if key=='core' else binding.get('proofFileSha256')
        for item in reviews[key].get('reviewedFiles',[]):
            if item.get('actualView'):reviewed.add(item['file']);continue
            transition=transitions.get(item['file'],{})
            # Reuse is allowed only for actually reviewed prior pixels, with an
            # independently verified footer-only change and current hash binding.
            bounded=(item.get('previousCompleteContentReviewActuallyViewed') is True
                and item.get('stateCardContentPixelsUnchanged') is True
                and item.get('previouslyActuallyViewedSha256')==transition.get('before')
                and item.get('sha256')==transition.get('after')==audit.hash(ROOT/item['file'])
                and transition.get('changedPixelBoundingBox')==[93,923,207,935]
                and item.get('independentPixelDifferenceBoundingBox')==[93,923,207,935]
                and proof_sha==audit.hash(repair_path)
                and repair.get('overallStatus')=='passed'
                and repair.get('allChangesBelowStateCards') is True)
            audit.check('bounded-prior-visual-review:'+key+':'+item['file'],bounded)
            if bounded:reviewed.add(item['file'])
        audit.check('visual-screen-coverage:'+key,required_screens<=reviewed,sorted(required_screens-reviewed))
        audit.check('visual-state-coverage:'+key,required_states<=reviewed,sorted(required_states-reviewed))
        for item in reviews[key].get('reviewedFiles',[]):
            audit.check('visual-review-current:'+key+':'+item['file'],audit.hash(ROOT/item['file'])==item['sha256'])
    failed=[item for item in audit.checks if not item['passed']]
    report=dict(schemaVersion=1,checkedAt=datetime.now(timezone(timedelta(hours=-4))).isoformat(),scope='UI art, source coverage, PNG contracts, state feedback, layout/provenance and independent picture review only',unityValidation='Not performed; deferred to next phase',gameRuntimeValidation='Not claimed for this art package',referenceCommit=COMMIT,summary=dict(referenceFeatures=len(expected),fullScreenFamilies=len(master['features']),coreSourceStates=sum(len(labels(f)) for f in core['features']),advancedSourceStates=sum(len(labels(f)) for f in advanced['features']),stateBoards=boards,statePreviews=state_count,kitAssets=len(assets['assets']),formalIndependentSprites=len(complete_assets),sourceOnlyMasters=len(complete.get('sourceOnly',[])),newGenerationRecords=len(generations),checks=len(audit.checks),passed=len(audit.checks)-len(failed),failed=len(failed)),overallStatus='passed' if not failed else 'needs-revision',checks=audit.checks,failures=failed,images=audit.images,independentReviews={key:dict(status=value.get('overallStatus'),method=value.get('method')) for key,value in reviews.items()},limitations=['Unity import, Sprite rendering, Prefab assembly, game logic and runtime integration are outside this phase.','Full-screen PNGs are compositions using native-size painted resources and separate text; not new native image-model renders for every screen.','Model and quality are host-managed and unconfirmed where no return metadata was disclosed.'])
    write(OUT/'records/FINAL_ACCEPTANCE.json',report)
    print(json.dumps(dict(summary=report['summary'],overallStatus=report['overallStatus'],firstFailures=failed[:15]),ensure_ascii=False,indent=2))
    return 1 if failed else 0

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contacts',action='store_true');parser.add_argument('--state-contacts',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.contacts:contact_sheets(load(OUT/'records/ui-master-manifest.json'))
    if args.state_contacts:state_contact_sheets(load(OUT/'records/ui-master-manifest.json'))
    if args.check:raise SystemExit(run())
