"""Produce static UI flow diagrams; no game or Unity implementation."""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache
from datetime import datetime, timezone, timedelta
from xml.sax.saxutils import escape
import hashlib
import json
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art-delivery'
PRE = OUT / 'previews'
REC = OUT / 'records'
FONT = OUT / 'resources/fonts/NotoSansCJKsc-Regular.otf'
PAPER_FILE = OUT / 'resources/ui/paper-tile.png'
W, H = 1920, 1080
INK, JADE, GOLD, MUTED, CREAM = '#29463c', '#235347', '#b38e4c', '#69776a', '#f8f1df'
NOW = datetime.now(timezone(timedelta(hours=-4))).isoformat()
CORE = json.loads((ROOT/'docs/art-v2/research-core.json').read_text(encoding='utf-8'))
ADV = json.loads((ROOT/'docs/art-v2/research-advanced.json').read_text(encoding='utf-8'))
FEATURES = CORE['features'] + ADV['features']
BYID = {f['id']: f for f in FEATURES}
COMMIT = CORE['commit']

GROUPS = [
    dict(id='01', title='启程、世界与人物创建', short='启程与创建',
         featureIDs='main-menu motd credits world-list world-create world-mods world-options load-character creation-mode creation-scenario creation-profession creation-background creation-stats creation-traits creation-skills creation-summary character-templates loading'.split(),
         overview=['首页 → 世界 → 创建 / 读取', '模组与世界规则独立确认', '人物创建保留七个步骤'],
         lanes=[
             ('创建世界', ['首页世界入口','世界列表','模组与规则','名称确认','创建世界','人物创建']),
             ('自定义人物 · 七步', ['开局情景','职业','人生背景','初始属性','天赋特征','初始技能','身份总览']),
             ('出发与读取', ['新建 / 读取','人物列表','身份与存档','出发确认','加载步骤','生存主界面'])],
         notes=['情景、职业的解锁条件与特征冲突必须说明原因。', '无世界 / 无人物 / 无模板 / 非法名称 / 读取失败各自有返回出口。'],
         optional='人物总览内可调整开局日期与起点；不是游戏中任意传送。'),
    dict(id='02', title='物品、容器与周边转移', short='行囊与容器',
         featureIDs='inventory item-detail item-compare item-containers advanced-inventory worn-layers wield pickup multidrop consume read reload item-unload liquid-transfer item-use electronic-files'.split(),
         overview=['分类列表 → 物品详情 → 操作', '容器容量与兼容条件可见', '周边物品采用左右来源转移'],
         lanes=[
             ('物品操作', ['随身行囊','分类与搜索','物品详情','操作确认','消耗与反馈','返回行囊']),
             ('容器与口袋', ['背包或容器','口袋列表','容量与规则','选择去向','移动结果','返回容器']),
             ('周边转移', ['高级物品管理','左右来源','多选物品','数量确认','耗时转移','刷新来源'])],
         notes=['饮食、阅读、装填、卸载、液体、电子资料共享选择 / 详情 / 结果结构。', '容量不足、重量过高、弹药不兼容、容器不防水等限制不混成同一错误。'],
         optional='仓储来源是邻近地面、角色容器或载具货物，不新增远程公共仓库。'),
    dict(id='03', title='人物成长、制作与维护', short='成长与制作',
         featureIDs='character-sheet character-encumbrance character-skills character-proficiencies repair gunmods craft-recipes craft-batch disassemble construction construction-place activity-progress butcher-harvest zone-activities'.split(),
         overview=['配方 → 条件 → 批量 → 活动', '理论 / 实作 / 熟练技艺分开', '制作、建造与修理保留耗时'],
         lanes=[
             ('制作与拆解', ['制作入口','配方与目标','材料工具条件','批量确认','活动与中断','结果 / 返回']),
             ('技能成长', ['人物总览','技能与技艺','理论实作详情','训练开关','成长反馈','返回人物']),
             ('维护与施工', ['装备 / 建造','目标与部位','材料技能时间','操作确认','成功或失败','返回列表'])],
         notes=['收藏材料、替代材料、缺工具、知识不足、位置非法各自提示。', '阅读、屠宰、农耕与区域批量工作接入同一长时活动 / 中断视觉合同。'],
         optional='技能不是MMORPG通用角色等级；区域工作不扩张成独立经营游戏。'),
    dict(id='04', title='生存回合、战斗与伤势', short='生存与战斗',
         featureIDs='game-hud aim-ranged throw-target look-examine nearby-creatures message-log body-health medical-treatment status-effects morale wait-sleep memorial'.split(),
         overview=['选择行动 → 目标 → 回合推进', '伤势、饥渴、疲劳与士气可见', '终局记录与返回入口分开'],
         lanes=[
             ('回合行动', ['生存主界面','选择行动','目标与轨迹','行动确认','回合结果','返回主界面']),
             ('伤势处理', ['身体状态','受伤部位','治疗与风险','消耗确认','处理结果','返回状态']),
             ('休息与终局', ['等待 / 睡眠','时间与闹钟','风险或中断','继续 / 结束','状态 / 纪念','主界面 / 首页'])],
         notes=['弹药不足、超出范围、目标丢失与友方弹道需明确反馈。', '等待和长时活动可因危险中断；人物死亡后的纪念不作为可领取奖励。'],
         optional='自动时间推进与回合耗时按实际规则表达，不套动作闯关技能轮盘。'),
    dict(id='05', title='地图、探索、任务与终端', short='探索与目标',
         featureIDs='overmap map-notes route-travel zone-manager missions creature-codex diary terminal translocator'.split(),
         overview=['地图地点 → 路线 → 到达 / 中断', '任务含进行中 / 完成 / 失败', '交互终端保留权限与警报'],
         lanes=[
             ('探索与旅行', ['区域地图','地点与筛选','地点路线详情','旅行确认','到达或中断','返回地图']),
             ('任务闭环', ['任务入口','任务列表','目标与条件','交付对话','完成或失败','任务 / 地图']),
             ('终端与装置', ['接近并交互','可用操作','权限与风险','操作确认','成功或警报','返回观察'])],
         notes=['任务追踪、地图标记、兴趣点、日记与生物见闻保持各自列表和详情。', '旅行是路径规划后的行进，不增加无条件快速传送。'],
         optional='传送只适用于已发现并激活的对应装置；缺目的地时提供空态。'),
    dict(id='06', title='NPC、交易、营地与载具', short='社交与载具',
         featureIDs='npc-talk npc-trade factions followers camp-overview companion-assignment camp-upgrade vehicle-dashboard vehicle-parts vehicle-refill atm-bank vending-machine npc-orders animal-care'.split(),
         overview=['人物对话连接任务与交易', '营地派遣检查同伴和资源', '载具按部件进行维护补给'],
         lanes=[
             ('人物交谈', ['接近 / 联系','对话与命令','要求与信息','选择回应','关系任务变化','返回世界']),
             ('交易与交换', ['交易入口','双方物品','数量与价值','成交确认','余额库存变化','返回对话']),
             ('营地派遣', ['营地负责人','任务与工人','技能资源时间','派遣确认','工作 / 回收','返回营地']),
             ('载具维护', ['检查车辆','结构部件','材料工具条件','安装修理确认','耗时与结果','返回载具'])],
         notes=['钱卡终端与自动售货机按实际金额 / 库存表达；不是充值商城。', '同伴命令、驯养与骑乘依赖可用对象和条件，不能混成玩家好友系统。'],
         optional='营地扩建、同伴工作和载具维修为实际生存系统，不加入无依据公会或坐骑养成。'),
    dict(id='07', title='辅助、能力与可选内容', short='辅助与能力',
         featureIDs='bionics bionic-surgery mutations martial-arts spellbook spell-target achievements safemode-rules autopickup-rules settings-general settings-interface settings-graphics settings-audio keybindings help colors-theme tutorial'.split(),
         overview=['设置保留应用 / 放弃 / 重启', '规则可编辑、测试与保存', '法术仅在适用内容启用时出现'],
         lanes=[
             ('设置与规则', ['设置入口','分类与规则','选项说明','保存或放弃','生效 / 重启','返回设置']),
             ('义体与特征', ['能力入口','已知能力','消耗与条件','启停 / 手术','结果与状态','返回人物']),
             ('法术 · 可选', ['内容已启用','已知法术','范围与消耗','合法目标确认','施展结果','返回主界面'])],
         notes=['成就、准则、分数与击杀是记录；不机械添加签到、抽卡或奖励领取。', '帮助、教学与按键映射有返回路径；规则设置的冲突和非法输入必须解释。'],
         optional='魔法能力依赖对应内容；义体手术与主动特征按条件启用，不默认全解锁。')
]

assert len(BYID) == 100
flat = [id for g in GROUPS for id in g['featureIDs']]
assert len(flat) == 100 and len(set(flat)) == 100
assert set(flat) == set(BYID), (set(BYID)-set(flat), set(flat)-set(BYID))

@lru_cache(maxsize=64)
def font(size): return ImageFont.truetype(str(FONT),size)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def wrap(value, size, width):
    result=[]
    for paragraph in str(value).split('\n'):
        line=''
        for char in paragraph:
            if line and font(size).getlength(line+char)>width:
                result.append(line); line=char
            else: line+=char
        result.append(line)
    return result

class Diagram:
    def __init__(self,title,subtitle):
        self.image=Image.new('RGB',(W,H),CREAM)
        paper=Image.open(PAPER_FILE).convert('RGB')
        for y in range(0,H,paper.height):
            for x in range(0,W,paper.width): self.image.paste(paper,(x,y))
        self.image=Image.blend(self.image,Image.new('RGB',(W,H),CREAM),.65)
        self.draw=ImageDraw.Draw(self.image)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920" height="1080" viewBox="0 0 1920 1080">',
                  '<style>@font-face{font-family:NotoCJK;src:url(../resources/fonts/NotoSansCJKsc-Regular.otf)}text{font-family:NotoCJK,\"Noto Sans CJK SC\",sans-serif}</style>',
                  f'<rect width="1920" height="1080" fill="{CREAM}"/>',
                  '<defs><pattern id="paper" x="0" y="0" width="375" height="57" patternUnits="userSpaceOnUse"><image href="../resources/ui/paper-tile.png" width="375" height="57" opacity="0.35"/></pattern></defs>',
                  '<rect width="1920" height="1080" fill="url(#paper)"/>']
        self.texts=[]
        self.rect((54,38,1812,118),JADE,JADE,24)
        self.text(92,60,title,44,'#fff2d0',1740)
        self.text(92,170,subtitle,24,MUTED,1740)
        self.line((80,216,1840,216),GOLD,2)

    def rect(self,box,fill,stroke=GOLD,radius=14,width=2):
        x,y,w,h=box
        self.draw.rounded_rectangle((x,y,x+w,y+h),radius=radius,fill=fill,outline=stroke,width=width)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def text(self,x,y,value,size=24,color=INK,width=1700,center=False):
        lines=wrap(value,size,width)
        for i,line in enumerate(lines):
            dx=x+(width-font(size).getlength(line))/2 if center else x
            py=y+i*round(size*1.5)
            self.draw.text((round(dx),round(py)),line,font=font(size),fill=color)
            self.svg.append(f'<text x="{dx:.1f}" y="{py+size:.1f}" font-size="{size}" fill="{color}">{escape(line)}</text>')
        self.texts.append(dict(text=value,rect=[x,y,width,len(lines)*round(size*1.5)],fontSize=size))

    def line(self,coords,color=JADE,width=3):
        self.draw.line(coords,fill=color,width=width)
        x1,y1,x2,y2=coords
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')

    def arrow(self,x1,y1,x2,y2):
        self.line((x1,y1,x2,y2),JADE,3)
        self.draw.polygon([(x2,y2),(x2-9,y2-6),(x2-9,y2+6)],fill=JADE)
        self.svg.append(f'<path d="M{x2},{y2} L{x2-9},{y2-6} L{x2-9},{y2+6} Z" fill="{JADE}"/>')

    def lane(self,y,label,nodes):
        self.text(88,y,label,27,JADE,1744)
        n=len(nodes);gap=26 if n==7 else 38;bw=(1744-gap*(n-1))/n;by=y+47;bh=75
        for i,node in enumerate(nodes):
            x=88+i*(bw+gap);endpoint=i in (0,n-1)
            self.rect((x,by,bw,bh),JADE if endpoint else '#fcf7e9',JADE if endpoint else GOLD,12)
            lines=wrap(node,24,bw-22)
            ty=by+(bh-len(lines)*36)/2-4
            self.text(x+11,ty,node,24,'#fff5d9' if endpoint else INK,bw-22,True)
            if i<n-1: self.arrow(x+bw+5,by+bh/2,x+bw+gap-7,by+bh/2)

    def save(self,stem):
        PRE.mkdir(parents=True,exist_ok=True)
        png=PRE/f'{stem}.png';svg=PRE/f'{stem}.svg'
        self.image.save(png)
        svg.write_text('\n'.join(self.svg+['</svg>'])+'\n',encoding='utf-8')
        return dict(png=str(png.relative_to(ROOT)).replace('\\','/'),svg=str(svg.relative_to(ROOT)).replace('\\','/'),
                    pngSha256=sha(png),svgSha256=sha(svg),width=W,height=H,textMinSize=min(t['fontSize'] for t in self.texts),texts=self.texts)

def group_diagram(g):
    d=Diagram(f'流程 {g["id"]}  ·  {g["title"]}','青岚余生（暂定名） · 功能关系美术说明 · 入口、条件、确认、反馈与返回')
    spacing=153 if len(g['lanes'])==4 else 173
    for i,(label,nodes) in enumerate(g['lanes']): d.lane(242+i*spacing,label,nodes)
    note_y=885 if len(g['lanes'])==4 else 810
    d.rect((70,note_y,1780,167 if len(g['lanes'])==4 else 220),'#eee7d4','#d0b578',12)
    for i,note in enumerate(g['notes']): d.text(96,note_y+14+i*40,note,24,INK,1720)
    d.text(96,note_y+96,g['optional'],22,MUTED,1720)
    return d.save(f'flow-{g["id"]}')

def overview():
    d=Diagram('青岚余生（暂定名） · 全游戏 UI 流程总览','固定参考提交 '+COMMIT[:8]+' · 100 个玩家界面族 + 1 组通用弹窗 · 本阶段仅美术')
    for i,g in enumerate(GROUPS):
        row,col=divmod(i,3)
        if i==6: col=1
        x,y=80+col*600,247+row*247
        d.rect((x,y,560,217),'#fcf7e9',GOLD,18)
        d.rect((x+14,y+13,532,51),JADE,JADE,12)
        d.text(x+32,y+19,g['id']+'  '+g['short'],30,'#fff4d8',496)
        for j,line in enumerate(g['overview']): d.text(x+27,y+81+j*37,line,23,INK,508)
    d.text(80,1003,'可选内容须满足启用条件；未确认的运营 / 联网系统不纳入本体已有功能。',22,MUTED,1760,True)
    return d.save('flow-overview')

def flow_json(outputs):
    all_groups=[]
    for g,output in zip(GROUPS,outputs):
        entry={k:v for k,v in g.items()}
        entry['output']={k:v for k,v in output.items() if k!='texts'}
        entry['features']=[dict(id=id,title=BYID[id]['title'],source=BYID[id]['source'],flow=BYID[id]['flow'],
                                states=BYID[id]['states'],availability=BYID[id].get('availability','base-or-context-dependent')) for id in g['featureIDs']]
        all_groups.append(entry)
    payload=dict(schemaVersion=1,generatedAt=NOW,referenceCommit=COMMIT,referenceRepository='https://github.com/CleverRaven/Cataclysm-DDA',
        scope='Design-only static flow diagrams; no runtime or Unity execution evidence',
        operation='Deterministic diagram composition from native text, vector boxes/arrows, and existing paper texture. No new image-generation call.',
        font='art-delivery/resources/fonts/NotoSansCJKsc-Regular.otf',fontLicense='art-delivery/resources/fonts/OFL.txt',
        derivedFrom=[dict(file='art-delivery/resources/ui/paper-tile.png',sha256=sha(PAPER_FILE),sourceRecord='art-delivery/records/asset-manifest.json')],
        overview={k:v for k,v in OVERVIEW.items() if k!='texts'},groups=all_groups,
        commonStates=dict(featureID='common-dialogs',description='通用确认、取消、数量、通知与错误图形由各系统引用；实际语义仍来自各自状态。'),
        review=dict(featureIDs=len(flat),uniqueFeatureIDs=len(set(flat)),allResearchFeaturesCovered=set(flat)==set(BYID),
                    minDiagramTextSize=min([OVERVIEW['textMinSize']]+[o['textMinSize'] for o in outputs]),
                    typography='1920x1080; body text >=22px; diagram text is editable, not baked into a new AI illustration'))
    REC.mkdir(parents=True,exist_ok=True)
    (REC/'flow-manifest.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return payload

def write_docs(payload):
    lines=['# 全游戏 UI 流程关系', '',
        '制作名：**青岚余生（暂定名）**。功能参考固定为 Cataclysm-DDA 提交 `'+COMMIT+'`。流程图用于表达 UI 美术关系，不代表 Unity、C#、Prefab、业务接口或运行联调已经完成。', '',
        '总览：[PNG](../../'+OVERVIEW['png']+') · [可编辑 SVG](../../'+OVERVIEW['svg']+')。每张 1920×1080，正文至少 22px；字体与 OFL 许可随资源包交付。PNG 是既有纸面纹理、原生文字与矢量框线的确定性组合，没有调用新的生成模型。', '',
        '玉绿节点表示流程入口或返回点，米白节点表示列表、详情、条件、确认或反馈。并不是每个只读信息页都存在“领取”或“成交”；具体确认语义以各条源码流程为准。', '']
    for g in payload['groups']:
        lines += ['## '+g['id']+' · '+g['title'], '',
                  '[PNG](../../'+g['output']['png']+') · [可编辑 SVG](../../'+g['output']['svg']+')', '']
        for label,nodes in g['lanes']: lines.append('- **'+label+'**：'+' → '.join(nodes)+'。')
        lines += ['', g['optional'], '', '覆盖的实际功能：', '']
        for f in g['features']:
            s=f['source'][0]
            url=s.get('url') or f'https://github.com/CleverRaven/Cataclysm-DDA/blob/{COMMIT}/{s["file"]}#L{s.get("line",1)}'
            lines.append('- `'+f['id']+'` **'+f['title']+'**：'+' → '.join(f['flow'])+'。 [源码依据]('+url+')')
        lines += ['', '条件与异常：'+'；'.join(g['notes']), '']
    lines += ['## 共用状态与验收边界', '',
        '- 通用确认、数量、错误、空态、锁定与结果皮肤在 `common-dialogs` 引用。它们用于统一美术，不取代弹药不兼容、口袋容量不足、材料不足、未解锁、无目的地等具体说明。',
        '- 法术等可选内容仅在对应内容启用且人物已掌握时显示；传送必须有实际装置及目的地；职业/情景解锁遵守源条件。',
        '- 无依据的网络账号、MMORPG区服、充值、世界聊天、邮件、签到、抽卡和远程公共仓库没有机械加入。',
        '- 流程图覆盖100个研究到的玩家界面族。图中所有人物名和数值均属样例，功能研究不证明图像视觉验收通过；独立美术验收与下一阶段Unity验证须分别记录。',
        '- 完整结构、各功能状态、固定源码引用及图像哈希见 [`flow-manifest.json`](../../art-delivery/records/flow-manifest.json)。']
    (ROOT/'docs/art-v2/FLOWS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def coverage_review():
    master_path=REC/'ui-master-manifest.json'
    master=json.loads(master_path.read_text(encoding='utf-8'))
    mids=[f['id'] for f in master['features']]
    mmap={f['id']:f for f in master['features']}
    copy_path=ROOT/'docs/art-v2/copy-core.json'
    player_copy=json.loads(copy_path.read_text(encoding='utf-8')) if copy_path.is_file() else {}
    rows=[]
    for f in CORE['features']:
        m=mmap.get(f['id'])
        sources=[]
        for s in f['source']:
            source_file=ROOT/'reference/Cataclysm-DDA'/s['file']
            count=len(source_file.read_text(encoding='utf-8').splitlines()) if source_file.is_file() else 0
            sources.append(dict(file=s['file'],symbol=s['symbol'],line=s.get('line'),fileExists=source_file.is_file(),
                                lineInBounds=1<=s.get('line',1)<=count))
        declared=[]
        if m:
            for kind,paths in [('design',[m['designFile']]),('state-preview',m['statePreviewFiles']),('layout',[m['layoutFile']]),('resource',m['resourceFiles'])]:
                for file in paths:
                    p=ROOT/file
                    declared.append(dict(kind=kind,file=file,exists=p.is_file(),sha256=sha(p) if p.is_file() else None))
        row=dict(id=f['id'],title=f['title'],system=f['system'],sourceChecks=sources,
            presentInMaster=m is not None,sourceMappingPreserved=m is not None and m.get('source')==f['source'],
            flowPreserved=m is not None and m.get('flow')==f['flow'],statesPreserved=m is not None and m.get('states')==f['states'],
            assumptionsPreserved=m is not None and m.get('assumptions')==f['assumptions'],
            declaredArtifacts=declared,declaredArtifactsAllPresent=bool(declared) and all(a['exists'] for a in declared),
            productionStatus=m.get('productionStatus') if m else 'missing',
            recordedIndependentAcceptance=m.get('acceptanceStatus') if m else 'missing',
            playerCopyPresent=f['id'] in player_copy,
            explicitPlayerStateFeedback=len(player_copy.get(f['id'],{}).get('stateFeedback',{})),
            playerCopyMessageNamesValid=all(name in f['states'] for name in player_copy.get(f['id'],{}).get('stateFeedback',{})),
            reviewStatus='source-and-scope-mapping-reviewed; independent visual acceptance remains separate',
            unity='not-implemented; next-stage integration only')
        rows.append(row)
    passing=all(r['presentInMaster'] and r['sourceMappingPreserved'] and r['flowPreserved'] and r['statesPreserved'] and r['assumptionsPreserved'] and all(s['fileExists'] and s['lineInBounds'] for s in r['sourceChecks']) for r in rows)
    report=dict(schemaVersion=1,reviewedAt=NOW,referenceCommit=COMMIT,scope='Core 51 feature source/scope/flow/state mapping review, plus declared artifact existence snapshot. Not independent pixel-art acceptance.',
        functionalReference='https://github.com/CleverRaven/Cataclysm-DDA',coreFeatureCount=len(rows),masterFeatureCount=len(mids),
        duplicateMasterIDs=sorted({id for id in mids if mids.count(id)>1}),missingCoreIDs=[f['id'] for f in CORE['features'] if f['id'] not in mmap],
        mappingPassed=passing,coreArtifactsPresentCount=sum(r['declaredArtifactsAllPresent'] for r in rows),
        playerFacingCopy=dict(file='docs/art-v2/copy-core.json',coreFeatures=len(player_copy),
                              explicitStateMessages=sum(len(v.get('stateFeedback',{})) for v in player_copy.values()),
                              semantics='blocked=true forbids the original operation; action is a safe alternate or return destination. danger=true is a risk confirmation with cancel. No blocked condition is accepted merely because an image exists.'),
        independentArtAcceptance='Do not infer passed from rendered or file existence. Refer to independent art validation and per-feature acceptance status.',
        notApplicableReviewed=CORE['notApplicable'],features=rows,
        flowCoverage=dict(groups=7,sourceFeaturesCovered=100,commonDialogs='shared supplemental visual contract'),
        finalRule='No unverified or missing screen/resource may be called complete; Unity import values are recommendations until actually tested.')
    (ROOT/'docs/art-v2/REVIEW_COVERAGE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    outputs=[group_diagram(g) for g in GROUPS]
    OVERVIEW=overview()
    payload=flow_json(outputs)
    write_docs(payload)
    reviewed=coverage_review()
    print(json.dumps(dict(flowPNGs=8,editableSVGs=8,sourceFeatures=100,minTextSize=payload['review']['minDiagramTextSize'],
                          coreMappingPassed=reviewed['mappingPassed'],coreArtifactsPresent=reviewed['coreArtifactsPresentCount']),ensure_ascii=False))
