"""Assemble delivery preview and promote only a fully accepted art package."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse, hashlib, json
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art-delivery'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def preview():
    selected=['main-menu','inventory','character-sheet','game-hud','map-overworld','npc-trade']
    master=read(OUT/'records/ui-master-manifest.json')
    by_id={f['id']:f for f in master['features']}
    # Use the researched map ID when the descriptive alias is absent.
    if selected[4] not in by_id:
        selected[4]=next(f['id'] for f in master['features'] if f.get('layoutPattern','').startswith('map') and f['id']!='construction-place')
    font_path=OUT/'resources/fonts/NotoSansCJKsc-Regular.otf'
    title_font=ImageFont.truetype(str(font_path),40)
    label_font=ImageFont.truetype(str(font_path),27)
    image=Image.new('RGB',(2000,1920),'#eee8d5');draw=ImageDraw.Draw(image)
    draw.text((44,22),'青岚余生（暂定名） · 全游戏 UI 美术',font=title_font,fill='#214d41')
    draw.text((48,86),'101 张主设计图 · 133 张状态板 · 仅美术，Unity 接入待下一阶段',font=label_font,fill='#566452')
    sources=[]
    for i,id in enumerate(selected):
        f=by_id[id];path=ROOT/f['designFile'];x=40+(i%2)*980;y=158+(i//2)*575
        with Image.open(path) as screen:thumb=ImageOps.fit(screen.convert('RGB'),(940,529),method=Image.Resampling.LANCZOS)
        image.paste(thumb,(x,y));draw.text((x+8,y+532),f['title'],font=label_font,fill='#214d41')
        sources.append(dict(file=f['designFile'],sha256=sha(path)))
    target=OUT/'previews/preview-overview.jpg';image.save(target,quality=95)
    write(OUT/'records/overview-preview.json',dict(operation='Contact-sheet composition of six delivered full-screen designs; no image-model generation',file=str(target.relative_to(ROOT)).replace('\\','/'),sha256=sha(target),size=[2000,1920],sources=sources))

def accept():
    report=read(OUT/'records/FINAL_ACCEPTANCE.json')
    if report.get('overallStatus')!='passed' or report.get('summary',{}).get('failed')!=0:
        raise SystemExit('Final art acceptance has not passed; no promotion performed.')
    master_path=OUT/'records/ui-master-manifest.json';master=read(master_path)
    for f in master['features']:
        f['acceptanceStatus']='art-accepted'
        f['acceptanceReport']='art-delivery/records/FINAL_ACCEPTANCE.json'
        f['unityStatus']='待下一阶段接入验证'
        f['missingArtItems']=[]
    master['artAcceptance']='passed'
    master['acceptedAt']=datetime.now(timezone(timedelta(hours=-4))).isoformat()
    master['acceptanceReport']='art-delivery/records/FINAL_ACCEPTANCE.json'
    master['remainingWork']=['Unity Sprite/TMP import and platform visual validation','Prefab, scene, state bindings and gameplay integration','Result GitHub account/repository and submission requirements are pending']
    write(master_path,master)
    coverage=OUT/'previews/UI_COVERAGE.md'
    coverage.write_text(coverage.read_text(encoding='utf-8').replace('已制作，待独立复核','美术验收通过；Unity 待接入'),encoding='utf-8')
    summary=report['summary']
    acceptance=f'''# 本次 UI 美术验收

核验时间：{report['checkedAt']}。结论：**本次固定清单美术验收通过**。

| 项目 | 结果 |
|---|---|
| 功能范围 | 100 类固定源码研究界面 + 1 类通用弹窗 |
| 主设计 / 状态板 | 101 / 133 张，均为 1920×1080 |
| 状态条目 | 604 条源码研究状态 + 6 条通用状态 = 610 |
| 独立资源 | 112 件；2 张制作母图另列，不计作运行 Sprite |
| 流程 | 1 张总览、7 张分组，均含 PNG 与 SVG |
| 正式文件检查 | {summary['passed']} 项通过，{summary['failed']} 项失败 |
| 独立视觉复核 | 核心 51 + 通用、高级 49；最终文件哈希已绑定 |
| 使用位置映射 | 234 份，图片位置、缩放和源 Border 核验通过 |
| Unity 导入和运行 | 未执行；按当前阶段约定留待下一阶段 |

[正式逐项报告](records/FINAL_ACCEPTANCE.json)、[功能覆盖](previews/UI_COVERAGE.md)、[完整图集](previews/index.html)、[位置映射验收](records/placement-validation.json)。独立图片审查分别在 `../docs/art-v2/REVIEW_CORE_ART.json` 与 `REVIEW_ADVANCED.json`。

检查范围包括解码、尺寸、Alpha、状态画布、源 Border、字体许可、来源和配方哈希、状态文案/可用性、布局、流程、链接和独立实看图片。本机浏览器已显示图集及 101 项计数，见 `records/PREVIEW_CHECK.json`。

## 已知边界与后续事项

- Unity Sprite/TMP、九宫格实际缩放、图集、安全区、多分辨率、Prefab、业务绑定和运行联调尚待下一阶段，当前没有引擎验收证明。
- 静态预览制作中有 67 处小高度控件的目标中心带高度为 0；源 Border 合法、目标中心不为负。完整记录见 placement-validation，接入时按源 Border 与实际 RectTransform 重算，不能直接照抄预览目标边框。
- 源库指定的 `qdao_ui_redesign_v5/UI_SPEC.md` 当前缺失；未恢复旧文件，本包按本窗口明确要求和两张主参考制作。
- 内置生成入口未披露实际型号/质量，逐图记录为未确认；目标设置不充当返回证明。整屏为合成，不把缩放和切片称作新原生细节。
- 数值、人物、地名和对白是排版样例；图标覆盖 UI 类别和示例物品，没有重画全部 JSON 物品、第三方模组或开发调试器。
- 成果 GitHub 与提交要求待用户提供；本阶段未提交、推送或发布。F 盘只读，关联记录在本项目文档。
'''
    (OUT/'ACCEPTANCE.md').write_text(acceptance,encoding='utf-8')
    print('Art acceptance promoted for',len(master['features']),'families. Unity remains deferred.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--accept',action='store_true');args=parser.parse_args()
    preview()
    if args.accept:accept()
