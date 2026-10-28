"""Aggregate completed independent review observations and bounded repair evidence."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art-delivery'
def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
target=ROOT/'docs/art-v2/REVIEW_CORE_ART.json'
if target.exists():raise SystemExit('Existing core report preserved; inspect it before replacing.')
master=load('art-delivery/records/ui-master-manifest.json');core=load('docs/art-v2/research-core.json')
proof=load('art-delivery/records/state-ghost-repair.json')
assert proof['overallStatus']=='passed' and proof['mainScreensByteIdentical'] and proof['allChangesBelowStateCards']
a=load('docs/art-v2/REVIEW_CORE_STATES_A.json');b=load('docs/art-v2/REVIEW_CORE_STATES_B.json')
assert a.get('status')=='passed' and b.get('overallStatus')=='passed'
ids={f['id'] for f in core['features']}|{'common-dialogs'}
features=[f for f in master['features'] if f['id'] in ids]
contacts=load('art-delivery/records/CORE_CONTACT_SHEETS.json')
for sheet in contacts['sheets']:
    assert sha(sheet['file'])==sheet['sha256']
    for item in sheet['sourceImages']:assert sha(item['file'])==item['sha256']
files=[]
for f in features:
    path=f['designFile'];assert sha(path)==proof['beforeMainHashes'][Path(path).name]
    files.append(dict(file=path,sha256=sha(path),actualView=True,actualViewBy='/root/art_final_qa',reviewBasis='Actual final main contact-sheet review by art_final_qa; common-dialogs original also reviewed; global repair proof confirms these PNG bytes did not change'))
    for path in f['statePreviewFiles']:
        transition=next(x for x in proof['stateBoards'] if x['file']==path)
        assert sha(path)==transition['after'] and transition['changedPixelBoundingBox']==[93,923,207,935]
        files.append(dict(file=path,sha256=sha(path),actualView=Path(path).stem in ['main-menu--states-1','world-options--states-1','craft-recipes--states-1','common-dialogs--states-1'],previousCompleteContentReviewActuallyViewed=True,previouslyActuallyViewedSha256=transition['before'],independentPixelDifferenceBoundingBox=[93,923,207,935],stateCardContentPixelsUnchanged=True,reviewBasis='Complete prior image/content review by independent core_states_a/b, then independent before/after pixel comparison and representative repaired-original views; no claim all repaired originals were reopened'))
report=dict(schemaVersion=2,assembledAt=datetime.now(timezone(timedelta(hours=-4))).isoformat(),assembledBy='/root',overallStatus='passed',scope='Core 51 families plus shared-dialogue family: UI art only',method='Coordinated aggregation of actual independent main-picture inspection, independent state-picture reports and exact bounded-repair checks. This aggregate is not a claim that the coordinator personally reopened every image.',mainReviewEvidence=dict(reviewer='/root/art_final_qa',trustedTeamMessage='最终主图9/9联系表已全实看（51），加之前20 pattern 原图+common6格、8流程原图；此前底部说明/对象/数量/导航修复均通过。核心主图无新增阻塞。',mainContactManifest='art-delivery/records/CORE_CONTACT_SHEETS.json',mainContactManifestSha256=sha('art-delivery/records/CORE_CONTACT_SHEETS.json'),mainPixelsUnchangedAfterReview=True),stateReviewEvidence=[dict(file=p,sha256=sha(p)) for p in ['docs/art-v2/REVIEW_CORE_STATES_A.json','docs/art-v2/REVIEW_CORE_STATES_B.json']],boundedRepair=dict(file='art-delivery/records/state-ghost-repair.json',sha256=sha('art-delivery/records/state-ghost-repair.json'),observedDelta=[93,923,207,935],allStateCardContentAndControlsUnchanged=True),summary=dict(coreFamilies=51,sharedFamilies=1,mainScreens=52,stateBoards=sum(len(f['statePreviewFiles']) for f in features),coreStateEntries=308,sharedStateEntries=6,independentStateContactSheets=17,afterRepairStateOriginalsActuallyViewed=4,openBlockingFindings=0,openMinorFindings=0),resolvedFindings=['Bottom descriptions intruding into panel decoration','Selected object, profession, location and detail mismatches','Unclear item comparison and repair object','Row icons and gun-modification subject mismatches','Missing visible quantity controls','Incorrect navigation fallback','Shared state-board underlying sample-footnote remnant'],reviewedFiles=files,unityValidation='Not performed; next phase',limitations=['Only four repaired core/shared state originals were reopened; the other repaired card contents were accepted through independently proven bit-identical pixels and the prior complete visual inspection.','Independent main-review observations above are retained from trusted team messages; the coordinator aggregated their evidence rather than claiming a new full manual view.'])
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Core aggregate passed:',len(files),'PNG bindings')
