"""Trace the frozen art recipe into placement metadata without changing PNGs."""
from pathlib import Path
import hashlib,json
from PIL import ImageOps
import art_screens as recipe
from art_screen_data import DATA

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art-delivery';RES=OUT/'resources'
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rel(path):return Path(path).relative_to(ROOT).as_posix()
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
recipe.ASSETS={item['id']:item for item in load(OUT/'records/asset-manifest.json')['assets']}
recipe.DATA=DATA
for name in ['copy-core.json','copy-advanced.json']:
    for key,value in load(ROOT/'docs/art-v2'/name).items():recipe.DATA[key].update(value)
INPUTS={name:sha(ROOT/name) for name in ['tools/art_screens.py','tools/art_screen_data.py','docs/art-v2/copy-core.json','docs/art-v2/copy-advanced.json']}
INDEX=[]

class DrawRecorder:
    def __init__(self,canvas):self.canvas=canvas
    def text(self,*args,**kwargs):pass # Actual text areas are in the existing layout JSON.
    def add(self,shape,*args,**kwargs):self.canvas.vectors.append(dict(shape=shape,args=args,properties=kwargs))
    def rounded_rectangle(self,*args,**kwargs):self.add('rounded_rectangle',*args,**kwargs)
    def ellipse(self,*args,**kwargs):self.add('ellipse',*args,**kwargs)
    def line(self,*args,**kwargs):self.add('line',*args,**kwargs)
    def rectangle(self,*args,**kwargs):self.add('rectangle',*args,**kwargs)

def initialize(self,feature,background='entry-keyart',framed=True):
    self.feature=feature;self.used=set();self.texts=[];self.rects=[];self.state_controls=[]
    self.placements=[];self.vectors=[];self.d=DrawRecorder(self)
    bg=RES/'backgrounds'/f'{background}.png'
    self.placements.append(dict(file=rel(bg),rect=[0,0,1920,1080],sourceSize=list(recipe.picture(bg).size),render='Pillow ImageOps.fit, Lanczos, centering=(0.5,0.5)',layer='background'))
    if framed:
        self.vectors.append(dict(shape='full-canvas-dim',colorRGBA=[23,49,39,55]))
        self.frame()

def art(self,path,box,contain=False):
    source=RES/path;x,y,w,h=map(int,box);image=recipe.picture(source)
    actual=[x,y,w,h]
    if contain:
        fitted=ImageOps.contain(image,(w,h),ImageOps.Image.Resampling.LANCZOS)
        actual=[x+(w-fitted.width)//2,y+(h-fitted.height)//2,fitted.width,fitted.height]
    self.placements.append(dict(file=rel(source),rect=list(box),resolvedRect=actual,sourceSize=list(image.size),render='contain-centered' if contain else 'cover-centered',layer='art'))

def skin(self,name,box):
    item=recipe.ASSETS[name];source=RES/'ui'/f'{name}.png';x,y,w,h=map(int,box)
    l,b,r,t=item['borderLeftBottomRightTop'];k=min(.78,w/(l+r+1),h/(t+b+1))
    target=[max(1,round(v*k)) for v in (l,b,r,t)] if any((l,b,r,t)) else [0,0,0,0]
    self.placements.append(dict(id=name,file=rel(source),rect=[x,y,w,h],sourceSize=item['size'],render='nine-slice' if any((l,b,r,t)) else 'contain-top-left',borderSourceLeftBottomRightTop=[l,b,r,t],borderRenderedLeftBottomRightTop=target,layer='skin'))

def save(self,path):
    layout_path=OUT/'records/layouts'/f'{Path(path).stem}.json';old=load(layout_path)
    if old['recipeInputs']!=INPUTS:raise RuntimeError(f'Recipe changed since image creation: {path}')
    if old['sha256']!=sha(path):raise RuntimeError(f'PNG changed since layout recording: {path}')
    target=OUT/'records/resource-placements'/f'{Path(path).stem}.json'
    for i,item in enumerate(self.placements):item['drawOrder']=i;item['sha256']=sha(ROOT/item['file'])
    dump(target,dict(file=rel(path),screenSha256=sha(path),canvas=[1920,1080],coordinateOrigin='top-left',rectOrder='x,y,width,height',operation='Geometry trace of the exact frozen composition recipe; no PNG pixels were regenerated or modified',recipeInputs=INPUTS,traceTool=dict(file='tools/export_resource_placements.py',sha256=sha(Path(__file__))),imageAreas=self.placements,vectorUI=self.vectors,textLayout=rel(layout_path),unityStatus='Placement advice, not imported or verified in Unity'))
    INDEX.append(dict(file=rel(path),placementFile=rel(target),sha256=sha(target),screenSha256=sha(path),imageAreaCount=len(self.placements)))
    return old

recipe.Canvas.__init__=initialize;recipe.Canvas.art=art;recipe.Canvas.skin=skin;recipe.Canvas.save=save
recipe.dump=lambda *args,**kwargs:None
master=load(OUT/'records/ui-master-manifest.json')
for feature in master['features']:
    canvas=recipe.render_feature(feature);canvas.save(ROOT/feature['designFile']);recipe.render_states(feature)
dump(OUT/'records/resource-placement-index.json',dict(schemaVersion=1,screenCount=len(master['features']),stateBoardCount=sum(len(f['statePreviewFiles']) for f in master['features']),recordCount=len(INDEX),sourceRecipe=INPUTS,records=INDEX))
print('Placement records:',len(INDEX),'PNG files unchanged')
