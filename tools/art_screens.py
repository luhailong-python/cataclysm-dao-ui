"""Compose review-only full-screen artwork from real painted assets and native text.

No gameplay, Unity project, business API, or image-generation call lives here.
"""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from datetime import datetime, timezone, timedelta
import json, hashlib, html, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'art-delivery'; RES=OUT/'resources'
W,H=1920,1080
JADE='#214d41'; INK='#243e36'; MUTED='#68776a'; GOLD='#ad884b'; RED='#a34f3f'; PAPER='#f7efdc'
FONT=RES/'fonts/NotoSansCJKsc-Regular.otf'
SYSTEMS=['启程与世界','人物与成长','物品与制作','探索与战斗','地图与营地','社交与载具','设置与辅助']
@lru_cache(maxsize=80)
def font(n): return ImageFont.truetype(str(FONT),n)
@lru_cache(maxsize=256)
def picture(path):
    with Image.open(path) as im:return im.convert('RGBA')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def wrap(text,size,width):
    lines=[]
    for paragraph in str(text).split('\n'):
        line=''
        for char in paragraph:
            if line and font(size).getlength(line+char)>width:lines.append(line);line=char
            else:line+=char
        lines.append(line)
    return lines

class Canvas:
    def __init__(self,feature,background='entry-keyart',framed=True):
        self.feature=feature;self.used=set();self.texts=[];self.rects=[];self.state_controls=[]
        bg=RES/'backgrounds'/f'{background}.png'
        self.im=ImageOps.fit(picture(bg),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');self.used.add(str(bg.relative_to(ROOT)).replace('\\','/'))
        if framed:
            self.im.alpha_composite(Image.new('RGBA',(W,H),(23,49,39,55)))
        self.d=ImageDraw.Draw(self.im)
        if framed:self.frame()
    def tx(self,x,y,text,size=27,color=INK,width=1000,align='left',lines=None,key=None):
        strings=wrap(text,size,width)
        if lines and len(strings)>lines:
            strings=strings[:lines]
            while font(size).getlength(strings[-1]+'…')>width:strings[-1]=strings[-1][:-1]
            strings[-1]+='…'
        lh=round(size*1.48)
        for i,line in enumerate(strings):
            dx=x if align=='left' else x+(width-font(size).getlength(line))/2 if align=='center' else x+width-font(size).getlength(line)
            self.d.text((int(dx),int(y+i*lh)),line,font=font(size),fill=color)
        self.texts.append(dict(id=key or f'text-{len(self.texts)}',text=str(text),displayText='\n'.join(strings),rect=[x,y,width,max(lh,lh*len(strings))],fontSize=size,color=color,align=align,exampleData=True))
    def art(self,path,box,contain=False):
        full=RES/path;im=picture(full);self.used.add(str(full.relative_to(ROOT)).replace('\\','/'))
        x,y,w,h=map(int,box)
        if contain:
            im=ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS);x+=(w-im.width)//2;y+=(h-im.height)//2
        else:im=ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS)
        self.im.alpha_composite(im,(x,y));self.d=ImageDraw.Draw(self.im)
    def skin(self,name,box):
        file=RES/'ui'/f'{name}.png';entry=ASSETS.get(name)
        if entry is None:raise KeyError(name)
        im=picture(file);self.used.add(str(file.relative_to(ROOT)).replace('\\','/'))
        x,y,w,h=map(int,box);l,b,r,t=entry['borderLeftBottomRightTop'];sw,sh=im.size
        if not any((l,b,r,t)):dst=ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS)
        else:
            k=min(.78,w/(l+r+1),h/(t+b+1));dl,dr,dt,db=[max(1,round(v*k)) for v in (l,r,t,b)]
            sx=[0,l,sw-r,sw];sy=[0,t,sh-b,sh];dx=[0,dl,w-dr,w];dy=[0,dt,h-db,h]
            dst=Image.new('RGBA',(w,h))
            for a in range(3):
                for z in range(3):
                    ww,hh=dx[a+1]-dx[a],dy[z+1]-dy[z]
                    if ww>0 and hh>0:dst.alpha_composite(im.crop((sx[a],sy[z],sx[a+1],sy[z+1])).resize((ww,hh),Image.Resampling.LANCZOS),(dx[a],dy[z]))
        self.im.alpha_composite(dst,(x,y));self.d=ImageDraw.Draw(self.im)
    def button(self,label,box,primary=False,state='normal'):
        x,y,w,h=box;self.skin(f'button-{"primary" if primary else "secondary"}-{state}',box)
        size=27
        while size>19 and font(size).getlength(label)>w-30:size-=1
        self.tx(x+12,y+(h-size*1.48)/2-3,label,size,'#fff4d7' if primary and state not in ('disabled','locked') else MUTED if state in ('disabled','locked') else JADE,w-24,'center',1)
    def plaque_text(self,label,box,size):
        x,y,w,h=box;available=max(90,w-320)
        while size>18 and font(size).getlength(label)>available:size-=1
        bb=font(size).getbbox(label)
        self.tx(x+(w-available)/2,y+h*.41-(bb[1]+bb[3])/2,label,size,'#fff5d5',available,'center',1)
    def bar(self,box,fraction,color=JADE):
        x,y,w,h=map(int,box);self.skin('progress-track',box)
        self.d.rounded_rectangle((x+4,y+4,x+4+max(2,int((w-8)*fraction)),y+h-4),radius=max(2,h//3),fill=color)
    def icon(self,name,box):
        candidate=RES/'icons'/f'{name}.png'
        if not candidate.exists():candidate=RES/'icons'/f'icon-{name}.png'
        if not candidate.exists():raise FileNotFoundError(candidate)
        self.art(candidate.relative_to(RES),box,True)
    def frame(self):
        pw=max(630,min(1020,round(font(35).getlength(self.feature['title'])+330)))
        pb=((W-pw)//2,24,pw,131)
        self.skin('panel-main',(38,62,1844,972));self.skin('title',pb)
        self.plaque_text(self.feature['title'],pb,35)
        self.tx(92,154,'青岚余生  ·  暂定名',25,JADE,270)
        self.tx(365,163,self.feature.get('subtitle','生存回合制 · 道家 Q 版 UI 美术方案'),25,MUTED,1390)
        if not self.feature.get('stateBoard'):
            for i,label in enumerate(SYSTEMS):
                chosen=label==self.feature.get('section')
                self.skin('tab-selected' if chosen else 'tab-normal',(86,235+i*89,242,72))
                self.tx(101,251+i*89,label,25,'#fff2d5' if chosen else JADE,212,'center',1)
            self.tx(93,882,'样例数据\n仅为美术排版',19,MUTED,220)
        self.tx(365,974,self.feature['id']+'  ·  设计预览 / 非游戏运行截图',18,MUTED,750)
        self.button('返回',(95,956,220,62))
    def panel(self,box):self.skin('panel-content',box)
    def title(self,text,x,y,w):
        self.skin('section',(x,y,w,76));self.plaque_text(text,(x,y,w,76),24)
    def row(self,x,y,w,title,value='',selected=False,icon=None,h=82):
        self.skin('row-selected' if selected else 'row-normal',(x,y,w,h))
        if icon:self.icon(icon,(x+17,y+11,58,58))
        self.tx(x+(88 if icon else 60),y+15,title,26,'#fff4d7' if selected else JADE,w-(260 if value else 102)-(30 if icon else 0),lines=1)
        if value:self.tx(x+w-235,y+20,value,22,'#e9e6d2' if selected else MUTED,195,'right',1)
    def save(self,path):
        path.parent.mkdir(parents=True,exist_ok=True);self.im.convert('RGB').save(path,optimize=True)
        derived=[]
        for name in sorted(self.used):
            fp=ROOT/name;gen=Path(str(fp)+'.generation.json');der=Path(str(fp)+'.source.json')
            derived.append(dict(file=name,sha256=sha(fp),record=str((gen if gen.exists() else der).relative_to(ROOT)).replace('\\','/') if gen.exists() or der.exists() else 'art-delivery/records/asset-manifest.json'))
        recipes=['tools/art_screens.py','tools/art_screen_data.py','docs/art-v2/copy-core.json','docs/art-v2/copy-advanced.json']
        layout=dict(id=self.feature['id'],file=str(path.relative_to(ROOT)).replace('\\','/'),sha256=sha(path),canvas=[W,H],coordinateOrigin='top-left',fontFile='art-delivery/resources/fonts/NotoSansCJKsc-Regular.otf',phase='art-only, not Unity verified',operation='Deterministic composition of recorded painted PNGs, vector UI indicators, and independent text. No model generation for this full-screen composite.',recipeInputs={name:sha(ROOT/name) for name in recipes},derivedFrom=derived,assets=sorted(self.used),textAreas=self.texts,stateControls=self.state_controls,allBusinessData='illustrative layout examples',source=self.feature.get('source',[]))
        return layout

def samples(f):
    return DATA[f['id']]

def render_feature(f):
    p=f.get('layoutPattern','list-detail');p={'loading':'progress','tutorial-overlay':'reader'}.get(p,p);v=samples(f);c=Canvas(f,'expedition-playfield' if p in ('hud','targeting','progress') else 'entry-keyart',p not in ('hud','targeting','hero-menu'))
    rows=v.get('rows',[]);heading=v.get('heading',rows[0][0] if rows else f['title']);detail=v.get('detail','所选内容的详情、条件、消耗与可执行操作。示例数值用于展示信息层级。')
    if p=='hero-menu':
        c.skin('panel-content',(1020,185,790,760));c.skin('title',(1080,130,670,130))
        c.plaque_text('青岚余生',(1080,130,670,130),43);c.tx(1120,300,'暂定名 · 生存回合制',24,MUTED,590,'center')
        for i,label in enumerate(['新的旅程','继续旅程','世界管理','设置与帮助']):c.button(label,(1150,390+i*112,530,83),i==0)
        c.tx(1080,850,'道家 Q 版 · 整款游戏 UI 美术方案',24,MUTED,650,'center')
    elif p in ('hud','targeting'):
        c.skin('panel-tooltip',(40,35,590,174))
        label='青岚 · 幸存者（样例）';bb=font(28).getbbox(label)
        c.tx(105,84-(bb[1]+bb[3])/2,label,28,'#fff5d5',460,'center',1)
        c.tx(85,118,'体力  82 / 100',23,INK,260);c.bar((90,163,460,20),.82)
        c.skin('panel-tooltip',(1370,37,510,854))
        label='驾驶与车辆' if f['id']=='vehicle-dashboard' else '瞄准与目标' if p=='targeting' else '生存手记';bb=font(29).getbbox(label)
        c.tx(1420,85-(bb[1]+bb[3])/2,label,29,'#fff5d5',410,'center',1)
        statuses=[('速度','0 km/h'),('引擎','已熄火'),('燃料','62%'),('蓄电量','74%'),('车灯','关闭'),('储物','可查看')] if f['id']=='vehicle-dashboard' else [('时间','春 · 第 3 日 08:40'),('天气','晴朗 · 微风'),('行动','步行 / 安全模式'),('口渴','轻度口渴'),('饥饿','尚可'),('疲劳','精神良好')]
        for i,(a,b) in enumerate(statuses):c.tx(1420,154+i*74,a,22,MUTED,100);c.tx(1530,154+i*74,b,23,INK,295,lines=1)
        c.tx(1420,650,detail,23,INK,405,lines=4)
        if f['id']!='vehicle-dashboard':c.art(Path('characters/hero-survivor.png'),(785,407,176,264),True)
        if p=='targeting':
            c.d.ellipse((1020,410,1150,540),outline=RED,width=4);c.d.line((875,567,1085,475),fill=RED,width=4)
            summary='范围与消耗按模组法术规则显示' if f['id']=='spell-target' else '投掷物  空瓶     距离  4 格     确认落点后投掷' if f['id']=='throw-target' else '命中预测  72%     距离  6 格     预计消耗  100 行动'
            c.skin('panel-tooltip',(430,765,825,114));c.tx(473,816,summary,25,JADE,750,'center',1)
        actions=['加速','减速','停车','喇叭','车灯','部件','地图','离车'] if f['id']=='vehicle-dashboard' else ['移动','等待','观察','物品','制作','攻击','地图','更多']
        if p=='targeting':actions[5]={'aim-ranged':'射击','throw-target':'确认投掷','spell-target':'释放法术'}.get(f['id'],'确认');actions[7]='取消'
        for i,label in enumerate(actions):c.button(label,(60+i*158,941,146,75),i==5)
        c.skin('row-normal',(700,24,600,67));c.tx(720,37,f['title']+' · UI 美术示意',25,JADE,560,'center',1)
    elif p=='vehicle-plan':
        c.panel((359,230,1050,692));c.panel((1422,230,410,692));c.tx(410,266,'部件位置示意 · 旧旅行车',30,JADE,930)
        parts=[(0,0,'左前车架','survival-scrap'),(1,0,'引擎','survival-wrench'),(0,1,'左前轮','survival-wheel'),(1,1,'蓄电池','survival-battery'),(2,1,'右前轮','survival-wheel'),(1,2,'驾驶座','survival-helmet'),(0,3,'左后轮','survival-wheel'),(1,3,'储物箱','survival-backpack'),(2,3,'右后轮','survival-wheel'),(1,4,'车架','survival-scrap')]
        for col,row,label,icon in parts:
            x,y=550+col*210,340+row*105;c.skin('slot-selected' if label=='左前车架' else 'slot-normal',(x,y,182,95));c.icon(icon,(x+10,y+9,69,69));c.tx(x+81,y+25,label,21,JADE,93,lines=2)
        c.tx(1460,270,'左前车架 · 受损',29,JADE,330)
        for i,(a,b) in enumerate([('耐久','60 / 100'),('所需材料','钢片 ×2'),('维修工具','焊接工具'),('预计耗时','约 25 分钟'),('状态','可检查维修条件')]):c.tx(1460,355+i*80,a,22,MUTED,330);c.tx(1460,385+i*80,b,25,INK,330)
        c.button(v.get('action','选择部件操作'),(1130,932,398,70),True)
    elif p.startswith('map'):
        local=f['id']=='construction-place';c.panel((359,230,1050,692));c.art(Path('backgrounds/expedition-playfield.png' if local else 'backgrounds/regional-map.png'),(388,260,988,620))
        c.panel((1422,230,410,692));c.tx(1462,270,heading,29,JADE,325,lines=2)
        for i,(a,b) in enumerate(rows[:6]):c.tx(1462,350+i*60,a,20,MUTED,325,lines=1);c.tx(1462,374+i*60,b,23,INK,325,lines=1)
        c.tx(1462,735,detail,20,INK,325,lines=3)
        if local:
            for i in range(3):
                for j in range(3):c.d.rectangle((810+i*75,445+j*75,880+i*75,515+j*75),outline=RED if (i,j)==(2,0) else JADE,width=4)
            c.tx(790,710,'绿色：可施工    朱砂：受阻',24,JADE,500)
        else:
            points=[(650,410,'已激活装置 A'),(977,630,'已激活装置 B')] if f['id']=='translocator' else [(650,410,'避难点'),(977,390,'废弃工坊'),(865,670,'河湾农场')]
            for x,y,label in points:
                c.d.ellipse((x-13,y-13,x+13,y+13),fill=JADE,outline='#f5e7bf',width=4);c.tx(x-95,y+22,label,22,JADE,190,'center')
        if p=='map-confirm' and f['id']!='translocator':
            c.d.line([(650,410),(740,465),(820,535),(865,670)],fill='#b65f44',width=6)
        c.button(v.get('action','查看选中地点'),(1130,932,398,70),True)
    elif p in ('character-sheet','character-summary','stat-editor','equipment','body','body-detail','confirm-risk'):
        c.panel((359,225,560,698))
        if f['id']=='gunmods':
            c.tx(420,284,'狩猎步枪 · 枪械示意',26,JADE,440,'center');c.icon('survival-rifle',(420,370,430,320));c.tx(445,743,'查看枪口、瞄具、枪托与弹仓。',22,MUTED,395,lines=2)
        else:c.art(Path('characters/hero-survivor.png'),(400,340,465,530) if p in ('body','body-detail') else (392,265,485,605),True)
        c.panel((935,225,897,698));c.tx(985,265,heading,33,JADE,790)
        for i,(name,value) in enumerate(rows[:6]):c.row(981,325+i*70,802,name,value,('左臂' in name if p in ('body','body-detail') else i==0),h=66)
        if p in ('body','body-detail'):
            c.d.ellipse((730,585,770,625),fill=RED,outline='#faedce',width=4);c.tx(453,275,'当前：左臂 · 浅表伤口',23,RED,410,'center')
        c.tx(1005,760,detail,21,MUTED,750,lines=2);c.button(v.get('action','确认'),(1170,930,345,73),True)
    elif p in ('item-grid-detail','item-detail','container','selection'):
        c.panel((359,225,910,698));c.panel((1282,225,550,698))
        names=['survival-water','survival-bandage','survival-food','survival-flashlight','survival-wrench','survival-battery','survival-backpack','survival-book','survival-ammo','survival-radio','survival-seeds','survival-meat','survival-pot','survival-circuit','survival-compass','survival-map','icon-sword','icon-boots','icon-herbs','icon-blade']
        if v.get('icon') not in names:names[0]=v.get('icon','survival-water')
        selected_index=names.index(v.get('icon','survival-water'))
        c.tx(405,260,v.get('leftTitle','随身物品   /   分类与筛选'),26,JADE,800)
        for i,name in enumerate(names):
            count={'pickup':3,'multidrop':8,'reload':8}.get(f['id'],[1,3,2,1,1][i%5]) if i==selected_index else [1,3,2,1,1][i%5]
            x,y=410+(i%5)*164,325+(i//5)*120;c.skin('slot-selected' if i==selected_index else 'slot-normal',(x,y,130,108));c.icon(name,(x+18,y+7,94,82));c.tx(x+83,y+79,str(count),18,JADE,28,'right')
        c.tx(450,803,'负重  18.6 / 32 kg       容量  12.4 / 18 L',21,MUTED,730)
        c.icon(v.get('icon','survival-water'),(1438,270,240,240));c.tx(1330,527,heading,31,JADE,450)
        c.tx(1330,589,detail,23,INK,440,lines=4)
        for i,(a,b) in enumerate(rows[:2]):c.tx(1350,745+i*46,a+'   '+b,21,MUTED,400,lines=1)
        c.button(v.get('action','使用'),(1360,931,335,73),True)
    elif f['id']=='item-compare':
        for col,(label,icon,values) in enumerate([
            ('当前 · 软布帽','survival-helmet',[('防护','2'),('重量','0.2 kg'),('头部阻碍','2'),('覆盖部位','头部'),('状态','完好')]),
            ('候选 · 防护头盔','survival-helmet',[('防护','5  ↑ 更高'),('重量','0.9 kg  ↑ 更重'),('头部阻碍','8  ↑ 更高'),('覆盖部位','头部'),('状态','完好')])]):
            x=359+col*747;c.panel((x,225,726,698));c.title(label,x+35,259,656)
            c.tx(x+64,348,'同部位防具 · 排版样例',22,MUTED,595)
            for i,(a,b) in enumerate(values):
                y=410+i*70;c.row(x+45,y,636,a,'',h=64);c.tx(x+340,y+17,b,22,JADE if col==1 and i==0 else RED if col==1 and i in (1,2) else MUTED,300,'right',1)
            c.tx(x+70,803,'绿色：防护提升；朱砂：负担增加。',21,MUTED,590,lines=1)
        c.button('返回物品',(1150,934,370,72),True)
    elif p in ('dual-list','dual-inventory','compare'):
        for col,label in enumerate(v.get('columns',['可用内容','已选择内容'])):
            x=359+col*747;c.panel((x,225,726,698));c.title(label,x+35,259,656)
            side_rows=[('绷带 ×1','价值 6'),('食品 ×2','价值 16'),('干净布料 ×4','价值 4'),('手电 ×1','价值 12')] if f['id']=='npc-trade' and col==1 else rows[:5]
            if col==1 and f['id']=='advanced-inventory':side_rows=[('净水 ×1','0.3 kg'),('绷带 ×3','0.1 kg'),('食品 ×2','0.8 kg'),('帆布背包','容量 18 L')]
            if col==1 and f['id']=='creation-traits':side_rows=[('夜间视觉','情景固定'),('怕冷','已选择')]
            if col==1 and f['id']=='world-mods':side_rows=[('基础生存内容','已启用'),('所需依赖','依赖已满足')]
            if col==1 and f['id']=='electronic-files':side_rows=[('当前目标设备','手持终端'),('可用空间','128 MB'),('已有资料','工坊检修记录')]
            for i,(a,b) in enumerate(side_rows):
                item_icon=v.get('icon')
                if f['id'] in ('npc-trade','advanced-inventory'):
                    item_icon=next((ic for term,ic in [('背包','survival-backpack'),('水','survival-water'),('绷带','survival-bandage'),('布','survival-bandage'),('钢','survival-scrap'),('食品','survival-food'),('手电','survival-flashlight'),('工具','survival-wrench')] if term in a),None)
                c.row(x+35,353+i*91,656,a,b,i==0,item_icon)
            c.tx(x+80,810,('给出估值 8' if col==0 else '获得估值 6 · 新增信用 2') if f['id']=='npc-trade' else '筛选 · 搜索 · 数量与选择',21,MUTED,570)
        c.button(v.get('action','确认调整'),(1150,934,370,72),True)
    elif p in ('settings','table'):
        c.panel((359,225,1473,698));c.tx(410,264,heading,32,JADE,1330)
        for i,(a,b) in enumerate(rows[:6]):
            y=345+i*70;c.skin('row-normal',(405,y,1370,62));c.tx(445,y+12,a,24,JADE,710)
            c.skin('tab-normal',(1270,y+5,452,49));c.tx(1288,y+9,b,22,JADE,415,'center',1)
        c.tx(465,770,detail,21,MUTED,1260,lines=2);c.button(v.get('action','保存设置'),(1150,934,370,72),True)
    elif f['id']=='craft-batch':
        c.panel((359,225,850,698));c.panel((1222,225,610,698));c.tx(420,275,'简易绷带 · 材料与工具',29,JADE,730)
        for i,(a,b) in enumerate(rows[:4]):c.row(410,365+i*96,745,a,b,i==0,h=80)
        c.icon('survival-bandage',(1430,275,180,155));c.tx(1280,445,'制作数量',27,JADE,475)
        c.button('−',(1280,510,100,70));c.skin('row-normal',(1400,503,240,86));c.tx(1415,519,'3',34,JADE,210,'center');c.button('+',(1660,510,100,70))
        c.tx(1295,615,'数量范围 1–3（本样例）\n总耗时 18 分钟（游戏时间）',23,INK,455,lines=2)
        c.tx(1295,741,'材料与工具已备齐。\n调整数量后重新核对总消耗。',22,MUTED,445,lines=2)
        c.button('确认批量',(1360,934,370,72),True)
    elif f['id']=='atm-bank':
        c.panel((359,225,1473,698));c.title('现金卡 · 存款确认',925,255,650)
        for i,label in enumerate(['存入银行','从银行取出','纸币兑换','查看余额']):c.button(label,(430,350+i*112,360,80),i==0)
        c.tx(900,376,'存款金额',29,JADE,700);c.skin('row-normal',(900,431,775,86));c.tx(1050,448,'100',34,JADE,470,'center');c.button('−',(920,439,110,65));c.button('+',(1535,439,110,65))
        for i,(a,b) in enumerate([('银行账户','500 → 600'),('现金卡余额','340 → 240'),('本次存款','100'),('纸币兑换','另行操作 · 1% 费用')]):c.tx(920,560+i*67,a,25,MUTED,320);c.tx(1240,560+i*67,b,27,INK,400,'right')
        c.button('确认存款',(1150,934,370,72),True)
    elif f['id']=='common-dialogs':
        cases=[('离开当前页面？','未保存的调整将被放弃。\n已保存的内容不受影响。','离开','继续编辑',True),('删除世界？','将删除“河湾”世界及其中人物。\n此操作不能撤销。','删除世界','取消',True),('选择数量','当前 3 份 · 范围 1–3','确认数量','取消',True),('发现新地点','河湾农场已记录到地图。\n可查看地点或继续探索。','查看地点','关闭',True),('制作完成','简易绷带 ×3 已放入行囊。\n材料消耗已结算。','查看物品','返回',True),('制作未开始','还缺少 1 份清洁材料。\n补齐后可重新确认。','条件不足','查看材料',False)]
        for i,(title,message,primary,secondary,enabled) in enumerate(cases):
            x,y=380+(i%3)*474,250+(i//3)*322;c.panel((x,y,452,298));c.tx(x+52,y+24,title,28,RED if i in (1,5) else JADE,348,'center',1)
            c.tx(x+48,y+93,message,23,INK,356,lines=2)
            if i==2:
                c.button('−',(x+55,y+147,80,54));c.tx(x+145,y+152,'3',27,JADE,160,'center',1);c.button('+',(x+320,y+147,80,54))
            c.button(primary,(x+24,y+221,240,58),enabled,'normal' if enabled else 'disabled');c.button(secondary,(x+283,y+221,145,58))
        c.tx(420,896,'跨系统共用皮肤与独立文字 · 各状态按实际业务绑定',21,MUTED,1310,lines=1)
    elif p in ('cards','choice','choice-detail','action-menu'):
        for i,(a,b) in enumerate(rows[:6]):
            x,y=380+(i%3)*474,250+(i//3)*322;c.panel((x,y,452,298));c.icon(v.get('icon','icon-notes'),(x+32,y+30,85,85))
            c.tx(x+145,y+40,a,29,JADE,270,lines=2);c.tx(x+40,y+145,b,25,MUTED,370,lines=3)
        c.tx(450,884,detail,20,MUTED,680,lines=1);c.button(v.get('action','确认选择'),(1150,934,370,72),True)
    elif p in ('reader','notice','terminal','summary','progress'):
        c.panel((359,225,1473,698));c.icon(v.get('icon','survival-book'),(420,275,170,170));c.tx(640,280,heading,34,JADE,1080)
        c.tx(640,355,detail,27,INK,1065,lines=5)
        for i,(a,b) in enumerate(rows[:4]):c.row(435,572+i*68,1320,a,b,i==0,h=66)
        if p=='progress':c.bar((640,480,1035,35),.62);c.tx(640,525,'正在读取世界资料 · 阶段示意，不假定参考代码提供精确百分比' if f['id']=='loading' else '进度 62%  ·  预计剩余 18 分钟（游戏时间示例）',25,JADE,1050)
        c.button(v.get('action','确认'),(1150,934,370,72),True)
    else:
        c.panel((359,225,652,698));c.panel((1024,225,808,698));c.tx(410,266,v.get('leftTitle','分类与列表'),28,JADE,550)
        for i,(a,b) in enumerate(rows[:6]):c.row(400,335+i*84,572,a,b,i==0,v.get('icon'))
        c.icon(v.get('icon','icon-notes'),(1240,270,225,205));c.tx(1080,498,heading,34,JADE,685,lines=2)
        c.tx(1080,586,detail,27,INK,685,lines=5)
        if v.get('condition'):c.tx(1080,790,v['condition'],22,MUTED,685,lines=1)
        c.button(v.get('action','确认选择'),(1150,934,370,72),True)
    return c

def normalized_states(f):
    raw=f.get('states',[])
    if not raw:raw=['默认','选中','确认','取消与返回']
    states=[]
    for s in raw:
        if isinstance(s,dict):label=s.get('name') or s.get('title') or s.get('id') or str(s);body=s.get('description',s.get('behavior',''))
        else:label=str(s);body=''
        states.append((label,body))
    return states

def render_states(f):
    states=normalized_states(f);paths=[]
    for page in range(math.ceil(len(states)/6)):
        c=Canvas(dict(f,title=f['title']+' · 状态',stateBoard=True))
        # Reuse outer title only; cover left navigation with deliberate state board.
        c.panel((76,210,1758,730))
        for j,(label,body) in enumerate(states[page*6:page*6+6]):
            x,y=103+(j%3)*572,238+(j//3)*340
            c.panel((x,y,548,319));c.tx(x+62,y+29,label,28,JADE,424,lines=1)
            error=any(k in label for k in ['失败','不足','错误','无效','中断','危险','不可','禁用'])
            locked=any(k in label for k in ['未解锁','锁定','未满足'])
            feedback=state_feedback(f,label,body)
            c.state_controls.append(dict(label=label,**feedback))
            c.tx(x+31,y+105,feedback['message'],23,RED if feedback.get('tone') in ('warning','danger') else MUTED,482,lines=3)
            c.button(feedback['primaryLabel'],(x+31,y+231,238,61),feedback['primaryEnabled'],'normal' if feedback['primaryEnabled'] else 'disabled')
            c.button(feedback.get('secondaryLabel','返回'),(x+286,y+231,231,61))
        c.tx(365,935,'状态与反馈合同 · 不执行游戏业务'+(' · 第 '+str(page+1)+' 页' if len(states)>6 else ''),20,MUTED,1050)
        path=OUT/'designs/states'/f'{f["id"]}--states-{page+1}.png';layout=c.save(path)
        dump(OUT/'records/layouts'/f'{f["id"]}--states-{page+1}.json',layout);paths.append(str(path.relative_to(ROOT)).replace('\\','/'))
    return paths

def state_description(label,title):
    if any(k in label for k in ['空','没有','无内容','无存档','无任务','无目标']):return '当前没有可显示的'+title+'内容。保留分类和返回入口，并说明如何获得内容。'
    if any(k in label for k in ['未解锁','锁定']):return '尚未解锁。显示前置条件与当前进度，主要操作禁用，保留查看与返回。'
    if any(k in label for k in ['不足','未满足']):return '条件不足。逐项标出缺少的工具、材料、能力或空间，调整前不执行操作。'
    if any(k in label for k in ['确认','警告','风险']):return '确认前展示对象、数量、成本与后果。取消保留原选择，确认后进入结果反馈。'
    if any(k in label for k in ['失败','错误','无效','不可']):return '显示具体失败原因；不虚构成功结果。保留当前选择并提供返回或重新选择。'
    if any(k in label for k in ['完成','成功','已领取']):return '展示实际结果和发生的变化。已完成操作不可重复触发，返回列表保留上下文。'
    if any(k in label for k in ['按下','悬停','选中','选择']):return '使用统一高亮、边框与文字反馈表达当前焦点，保持控件画布与锚点一致。'
    if any(k in label for k in ['进行','等待','加载']):return '显示当前阶段、时间或进度；可中断活动明确中断后果，不可中断时说明原因。'
    if any(k in label for k in ['取消','返回']):return '返回来源界面，保留滚动、筛选与已选对象；未提交内容按确认规则处理。'
    return '以“'+label+'”为此系统的专属状态。文案、可操作范围与反馈保持一致；界面数值均为示例。'

def state_feedback(f,label,body=''):
    v=samples(f);over=v.get('stateFeedback',{}).get(label,{})
    if over:
        enabled=over.get('primaryEnabled',not over.get('blocked',False))
        return dict(message=over.get('message',body),primaryLabel=over.get('primaryLabel','条件未满足' if over.get('blocked') else over.get('action',v.get('action','确认'))),primaryEnabled=enabled,secondaryLabel=over.get('secondaryLabel',over.get('action') if over.get('blocked') else over.get('secondary','返回')) or '返回',tone=over.get('tone','warning' if not enabled else 'danger' if over.get('danger') else 'normal'))
    blocked=any(s in label for s in ['无世界','无存档','无内容','无物','无可','无兼容','无弹药','无路径','无合法','无目标','无能力','无目的地','未启用','未解锁','未满足','不足','缺','冲突','不可','无效','错误','故障','超范围','超重','已满','过重','楼层不一致','污染','已装','丢失','禁止','不兼容','被阻','不能'])
    danger=any(s in label for s in ['友方','危险','风险','删除','重置','永久','误伤'])
    finished=any(s in label for s in ['成功','已完成','已领取','已达成','结束','死亡'])
    message=body or (f'当前状态：{label}。暂时不能执行“{v.get("action","此操作")}”，请先调整相关条件。' if blocked else f'{label}。请检查当前对象和所选内容，再决定下一步。')
    if danger and not blocked:message='此操作可能造成不可逆后果。请核对对象与条件，或取消返回。'
    return dict(message=message,primaryLabel='条件未满足' if blocked else '查看结果' if finished else '仍然继续' if danger else v.get('action','查看详情'),primaryEnabled=not blocked,secondaryLabel='返回调整' if blocked else '取消' if danger else '返回',tone='warning' if blocked else 'danger' if danger else 'normal')

def section_for(system,id):
    if id.startswith(('main','motd','world','load','creation','character-templates','loading')):return SYSTEMS[0]
    if id.startswith(('character','bionic','mutation','martial','spell')):return SYSTEMS[1]
    if id.startswith(('inventory','item','advanced-inventory','worn','wield','pickup','multidrop','consume','read','reload','repair','gunmods','craft','disassemble','liquid','electronic')):return SYSTEMS[2]
    if id.startswith(('game-hud','aim','throw','look','nearby','message','body','medical','status','morale','wait','activity','butcher','terminal')):return SYSTEMS[3]
    if id.startswith(('overmap','map','route','zone','camp','construction','translocator')):return SYSTEMS[4]
    if id.startswith(('npc','mission','faction','follower','companion','vehicle','atm','vending','creature-codex','animal-care')):return SYSTEMS[5]
    return SYSTEMS[6]

def build():
    all_features=[];excluded=[]
    for name in ['research-core.json','research-advanced.json']:
        data=json.loads((ROOT/'docs/art-v2'/name).read_text(encoding='utf-8-sig'))
        all_features+=data['features'];excluded+=data.get('notApplicable',[])
    ids=[f['id'] for f in all_features];assert len(ids)==len(set(ids)), 'duplicate feature IDs'
    extra=[dict(id='loading',system='启程',title='加载与进入世界',layoutPattern='progress',source=[dict(file='src/loading_ui.cpp',symbol='loading_ui')],flow=['选择世界','载入数据','进入主界面'],states=['加载中','准备完成','资源读取错误','返回'],assumptions=['按参考加载进度重排为图形进度面板。']),dict(id='common-dialogs',system='通用',title='通用弹窗与通知',layoutPattern='cards',source=[dict(file='src/popup.cpp',symbol='popup'),dict(file='src/uilist.cpp',symbol='uilist')],flow=['触发操作','确认或取消','结果反馈'],states=['确认取消','危险确认','数量选择','提示通知','操作成功','操作失败'],assumptions=['跨系统共用的视觉组件与状态合同。'])]
    all_features+=[f for f in extra if f['id'] not in ids]
    preliminary=dict(schemaVersion=2,title='青岚余生（暂定名）',referenceCommit='eb86dffd20072d6fde54af568cf229f3cd4d751f',features=[dict(f,productionStatus='planned',designFile=f'art-delivery/designs/screens/{f["id"]}.png') for f in all_features],notApplicable=excluded,phase='master inventory established before full-screen production')
    dump(OUT/'records/ui-master-manifest.json',preliminary)
    master=[]
    for index,f in enumerate(all_features):
        f['section']=section_for(f.get('system',''),f['id']);c=render_feature(f)
        path=OUT/'designs/screens'/f'{f["id"]}.png';layout=c.save(path)
        dump(OUT/'records/layouts'/f'{f["id"]}.json',layout)
        states=render_states(f)
        master.append(dict(f,designFile=str(path.relative_to(ROOT)).replace('\\','/'),statePreviewFiles=states,layoutFile=f'art-delivery/records/layouts/{f["id"]}.json',resourceFiles=layout['assets'],productionStatus='rendered',acceptanceStatus='pending-independent-art-review',unityStatus='待下一阶段接入验证',sampleCopy=samples(f)))
        if (index+1)%10==0:print('composed',index+1,'/',len(all_features),flush=True)
    data=dict(schemaVersion=2,title='青岚余生（暂定名）',scope='Entire regular-player feature UI art based on fixed reference commit; no Unity implementation',functionalReference='https://github.com/CleverRaven/Cataclysm-DDA',referenceCommit='eb86dffd20072d6fde54af568cf229f3cd4d751f',resultRemote='待补充',artReference=r'F:\work\image',designResolution=[W,H],features=master,notApplicable=excluded,generatedAt=datetime.now(timezone(timedelta(hours=-4))).isoformat())
    dump(OUT/'records/ui-master-manifest.json',data)
    make_gallery(data);make_index(data);return data

def make_gallery(data):
    cards=[]
    for f in data['features']:
        rel='../designs/screens/'+f['id']+'.png';states=' '.join(f'<a href="../designs/states/{Path(s).name}">状态 {i+1}</a>' for i,s in enumerate(f['statePreviewFiles']))
        cards.append(f'<article data-group="{html.escape(f["section"])}" data-search="{html.escape(f["title"]+f["id"])}"><a href="{rel}" target="_blank"><img loading="lazy" src="{rel}" alt="{html.escape(f["title"])}"></a><h2>{html.escape(f["title"])}</h2><p>{html.escape(f["id"])} · {html.escape(f["section"])}</p><nav>{states} <a href="../../records/layouts/{f["id"]}.json">排版记录</a></nav></article>')
    # Plain local art catalogue. No game logic or hosting/publishing integration.
    document='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>青岚余生 · 全游戏UI美术图集</title><style>body{margin:0;background:#e8e5d3;color:#214d41;font:16px system-ui}header{padding:30px 4%;background:#204f43;color:#fff4d8}h1{font-size:30px;margin:0 0 12px}main{padding:24px 4%;display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:24px}article{background:#fbf3df;border:1px solid #b6955f;border-radius:16px;overflow:hidden;box-shadow:0 3px 14px #293d2b12}img{display:block;width:100%;aspect-ratio:16/9}h2,p,nav{margin:14px 20px}h2{font-size:21px}a{color:#26694e}nav{display:flex;gap:18px;flex-wrap:wrap;padding-bottom:8px}input,select{font:inherit;padding:10px 14px;margin:14px 12px 0 0;border-radius:7px;border:1px solid #c4b17a}small{color:#e4dec8}article[hidden]{display:none}footer{padding:24px 4%}button{font:inherit}</style><header><h1>青岚余生（暂定名） · 全游戏 UI 美术图集</h1><p style="margin:0">功能参考 Cataclysm-DDA · 仅图片与资源设计 · Unity 接入待下一阶段</p><input id="search" placeholder="按界面名称或ID搜索"><select id="group"><option value="">全部系统</option>GROUPS</select><small id="count"></small></header><main>CARDS</main><footer>整屏为原画资源与独立文字的确定性组合，不是 Unity 或游戏运行截图。数值、名称与局部地理仅为排版样例。<a href="flow-overview.png">查看流程总览</a> · <a href="../records/ui-master-manifest.json">功能与资源总清单</a></footer><script>function filter(){let n=0;for(const a of document.querySelectorAll('article')){let ok=(!group.value||a.dataset.group===group.value)&&a.dataset.search.toLowerCase().includes(search.value.toLowerCase());a.hidden=!ok;if(ok)n++}count.textContent=n+' 个界面'}search.oninput=group.onchange=filter;filter()</script></html>'''
    document=document.replace('GROUPS',''.join('<option>'+s+'</option>' for s in SYSTEMS)).replace('CARDS','\n'.join(cards)).replace('../../records/layouts/','../records/layouts/')
    (OUT/'previews/index.html').write_text(document,encoding='utf-8')

def make_index(data):
    lines=['# UI 功能与资源总清单','','功能参考固定提交 `'+data['referenceCommit']+'`。所有示例文案为暂定名与排版样例。','', '| 系统 | 界面 | 整屏图 | 状态预览 | 布局与资源映射 | 状态 |','|---|---|---|---|---|---|']
    for f in data['features']:lines.append('| '+f['section']+' | '+f['title']+' | [整屏](../designs/screens/'+f['id']+'.png) | '+ ' '.join(f'[状态{i+1}](../designs/states/{Path(s).name})' for i,s in enumerate(f['statePreviewFiles']))+' | [文字/资源](../records/layouts/'+f['id']+'.json) | 已制作，待独立复核 |')
    lines+=['','## 不适用、可选及建议','','详情和源码证据见 `ui-master-manifest.json` 的 notApplicable、features.source 与 assumptions。没有把登录、区服、全服榜、运营邮件、充值等机械加到单人生存游戏。可选法术仅在相应模组启用时适用。','']
    (OUT/'previews/UI_COVERAGE.md').write_text('\n'.join(lines),encoding='utf-8')

ASSETS={}
DATA={}
if __name__=='__main__':
    ASSETS={a['id']:a for a in json.loads((OUT/'records/asset-manifest.json').read_text(encoding='utf-8-sig'))['assets']}
    from art_screen_data import DATA
    for name in ['copy-core.json','copy-advanced.json']:
        file=ROOT/'docs/art-v2'/name
        if file.exists():
            for key,values in json.loads(file.read_text(encoding='utf-8-sig')).items():
                if key in DATA:DATA[key].update(values)
    import sys
    if '--only' in sys.argv:
        names=sys.argv[sys.argv.index('--only')+1:]
        record=OUT/'records/ui-master-manifest.json';result=json.loads(record.read_text(encoding='utf-8'))
        for f in result['features']:
            if f['id'] not in names:continue
            c=render_feature(f);path=ROOT/f['designFile'];layout=c.save(path)
            dump(ROOT/f['layoutFile'],layout);f['resourceFiles']=layout['assets'];f['sampleCopy']=samples(f)
            f['statePreviewFiles']=render_states(f)
        dump(record,result);make_gallery(result);make_index(result)
        print('REFRESHED',names)
    else:
        result=build();print('DONE',len(result['features']),'full screens')
