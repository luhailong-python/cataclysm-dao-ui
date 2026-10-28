"""Package only accepted current art, supporting records and reproduction tools."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/'art-delivery/records/FINAL_ACCEPTANCE.json').read_text(encoding='utf-8'))
master=json.loads((ROOT/'art-delivery/records/ui-master-manifest.json').read_text(encoding='utf-8'))
if report.get('overallStatus')!='passed' or master.get('artAcceptance')!='passed':
    raise SystemExit('Refusing to package an art delivery before acceptance.')
files=set()
for dirname in ['art-delivery','docs/art-v2','docs/reference-images']:
    files.update(p for p in (ROOT/dirname).rglob('*') if p.is_file())
for name in ['docs/ASSET_SOURCES.json','docs/image-reference-associations.md','docs/image-reference-association-migration-20261026.json','tools/art_screens.py','tools/art_screen_data.py','tools/art_resources.py','tools/slice_survival_icons.py','tools/complete_resource_index.py','tools/validate_art_delivery.py','tools/finalize_art_delivery.py','tools/export_resource_placements.py','tools/check_state_ghost_repair.py','tools/assemble_core_review.py','tools/package_art_delivery.py']:
    path=ROOT/name
    if path.is_file():files.add(path)
export=ROOT/'exports';export.mkdir(exist_ok=True)
target=export/'qinglan-ui-art-20261026.zip'
readme='''# 青岚余生（暂定名）· UI 美术交付

打开 art-delivery/previews/index.html 查看整套图集。
功能清单：art-delivery/previews/UI_COVERAGE.md。
正式资源：art-delivery/resources/。
Unity 导入建议：docs/art-v2/UNITY_IMPORT.md。
最终验收：art-delivery/records/FINAL_ACCEPTANCE.json。
来源与关联：docs/image-reference-associations.md。

101 张主图、133 张状态板（604源状态+6通用）、112件独立资源；2张重切母图另列。
仅 UI 美术，未实施或验收 Unity/C#/Prefab/业务接入。游戏及数据名称为样例。
参考游戏 Cataclysm-DDA：eb86dffd20072d6fde54af568cf229f3cd4d751f。
功能克隆 reference/、旧启动器、官方游戏二进制和本地存档均未打包。
成果 GitHub 待提供；本阶段无成果提交/推送/发布。
'''
entries=[]
with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=1) as archive:
    archive.writestr('README.md',readme)
    for path in sorted(files):
        name=path.relative_to(ROOT).as_posix();archive.write(path,name)
        entries.append(dict(file=name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
manifest=dict(createdAt=datetime.now(timezone(timedelta(hours=-4))).isoformat(),file=str(target),bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),fileCount=len(entries)+1,excludes=['reference/','app/','assets/','qa/','.local/','exports/'],entries=entries)
(export/'package-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:manifest[key] for key in ['file','bytes','sha256','fileCount']},ensure_ascii=False,indent=2))
