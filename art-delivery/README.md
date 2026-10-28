# 全游戏 UI 美术包

临时名称：青岚余生（暂定名）。核实日期：2026-10-26（America/New_York）。正式位置：`E:\work\image\cataclysm-dao-ui\art-delivery`。本阶段交付图片与接入建议。

## 实际读取的依据

功能克隆为 `../reference/Cataclysm-DDA`，固定提交 `eb86dffd20072d6fde54af568cf229f3cd4d751f`。已读取 README、UI 可访问性和边栏说明、主菜单/世界生成/人物创建/物品/制作/设置源码，以及地图、战斗、任务、NPC、营地、载具、义体、变异、法术和终端实现。逐界面的文件、符号与行号在 [总清单](records/ui-master-manifest.json) source 字段。克隆无 AGENTS.md、无 LFS 过滤；所需 PNG 已解码，非指针。

美术来源为只读 `F:\work\image`，实际读取及影响：

| 文档/成图 | 本包采用的要求 |
|---|---|
| `AGENTS.md` | 指定两张成图优先、逐图证据、素材保留、禁止操作共享 Git；当前用户明确要求优先 |
| `README.md` 接手说明、`docs/WUXING_QITAN_HANDOFF.md` | 区分历史与当前采用版本；旧游戏名称、业务、数值和上传授权不移入本任务 |
| `docs/QDAO_ART_DIRECTION.md` | 玉绿、米白、暖金、圆润 Q 版、清楚轮廓与独立身份；地图图像不等同于导航 |
| `docs/IMAGE_MODEL_POLICY.md`、`config/image-generation.json` | 优先内置生图，配置目标、实际提交与返回分开记录，未披露的型号/质量标未确认 |
| `designs/README.md` | 定位确认成图与同功能资源，邮件/组队画法优先 |
| `qdao_ui_redesign_v5/UI_SPEC.md` 第 2 节 | 当前文件缺失，无法读取；未从旧 Git 恢复，执行本窗口明确视觉和资源要求 |
| 邮件、组队、属性、装备、技能、HUD、通用组件目录现存 README/manifest/采用记录 | 按真实图片和透明切片合同选择复用；精确路径、来源快照、哈希和处理见 asset-manifest |

两张主参考 `designs/mail-ui-v1/01-mail-event.png`、`designs/team-ui-v2/team-ui-v2.png` 已实际查看，本阶段 5 次新图调用均实际附入两张图片，并按需附人物参考。风格副本在 `../docs/reference-images/`；当前实际关联在 `../docs/image-reference-associations.md`。没有复制源游戏测试数据作为本游戏逻辑。

## 范围与排版

100 类源码研究的玩家界面加 1 类通用弹窗，共 101 类；每族含默认整屏、适用状态、流程与独立资源映射。法术、特定传送等条件能力单独标记。开发调试器、全部第三方模组和每个 JSON 物品的独立图鉴图不属于本包全量范围。

画布为 1920×1080 横屏；七组导航，玉绿主操作与选中项、纸底次级内容，危险状态明确取消，条件不足禁用原操作。`records/layouts/*.json` 保存实际文字与区域，左上原点，rect 为 `[x,y,width,height]`，含源图和输出 SHA、制作配方哈希。

| 项目 | 采用值 |
|---|---|
| 字体 | 随包 Noto Sans CJK SC Regular，SIL OFL 1.1；TMP 字库待下一阶段 |
| 主色 | 玉绿 `#214d41`、正文 `#243e36`、次要字 `#68776a` |
| 辅色 | 暖金 `#ad884b`、朱砂 `#a34f3f`、象牙 `#f7efdc` |
| 字号 | 页面标题约 34–43 px，正文 24–28，次要 20–23；长标题按净空调整，逐图记录实际字号 |
| 对齐 | 正文左、数值按列右、标题与按钮居中；以 layout JSON 为准 |
| 文案 | 中文独立排版，业务名、数量、时间、属性均为样例；正式游戏名待定 |
| 控件状态 | 按适用控件提供普通/按下/选中/禁用/锁定，状态画布一致；业务原因另见状态板 |

共 101 张主图、133 张状态板，表达源系统 604 项加通用 6 项、合计 610 个状态条目。每板最多六项，是文案与反馈合同，不执行游戏业务。地图、身体和载具平面示意仅表达 UI，不是可运行地图或模型。

## 资源与逐图记录

- `designs/screens/`、`designs/states/`：整屏及状态 PNG。
- `resources/ui/`：54 件皮肤，另有无字标题母图。
- `resources/icons/`：54 枚图标，另有现代生存图标母图。
- `resources/backgrounds/`：入口、探索和区域地图，原生 1672×941 RGB。
- `resources/characters/`：透明幸存者，原生 1024×1536 RGBA。
- `resources/fonts/`：字体和许可证。
- `previews/index.html`：图集；8 张流程 PNG/SVG 及联系表供审阅。
- [完整独立资源索引](records/complete-resource-manifest.json)、[完整导入参数](records/unity-import-complete.csv)：112 件正式独立资源，2 张母图另列；[文件规格验收](records/complete-resource-validation.json) 记录对应检查。

生存图标母图原生 1536×1024，按实际非均匀 Alpha 边界隔离、缩小并居中到 256×256，不放大物件，每边至少留白 16 px。标题母图原生 2203×714，title/section 保持比例派生。九宫格、裁切、缩放、调色和勾/锁合成如实记录，不称作新的模型生成。被重切脚本引用的母图是必要来源，予以保留。

每张新图旁 `.generation.json` 保存配置目标、实际参数、时间、参考来源、返回证据、正式路径及哈希。配置目标为 `gpt-image-2.5-sunburst / max`；内置入口没有 model/quality 参数或返回，实际型号和质量明确为未确认。提示词不充当锁定证明，未启用新增付费 API。

## 验收及下一阶段

[最终报告](records/FINAL_ACCEPTANCE.json) 汇总尺寸、Alpha、状态画布、Border、哈希、功能/状态覆盖、文字画布边界、流程、图集链接及独立视觉审查。独立复核在 `../docs/art-v2/REVIEW_CORE_ART.json`、`../docs/art-v2/REVIEW_ADVANCED.json`。总清单中的状态据此维护。

[Unity 导入说明](../docs/art-v2/UNITY_IMPORT.md) 和 CSV 均为建议，尚未在引擎验证。下一阶段实施 Sprite/TMP、九宫格、图集、安全区、多分辨率、Prefab、状态绑定及业务运行联调。

环境诊断 `records/scene-capability.json` 的 overall 为 WARN：多 Python PATH、SciPy/resvg/FFmpeg、外部 API 凭证和备用 Grok CLI 不齐，Codex CLI 生图路线未验证。本包实际使用 Python 3.14.3、Pillow 12.2.0 与宿主内置 image_gen；静态 PNG 不依赖上述备用路线和视频编码，未宣称诊断全通过。

成果远端待提供；本阶段未提交、推送或发布。F 盘按最新要求只读，关联与来源全部在本项目文档中维护。

## 重建与复核

在本项目根目录执行；只重新组合现有图片，不调用生图或游戏业务：

```powershell
Set-Location -LiteralPath 'E:\work\image\cataclysm-dao-ui'
python tools/art_screens.py
python tools/validate_art_delivery.py --check
python tools/finalize_art_delivery.py --accept
python tools/package_art_delivery.py
```

重建会将美术状态置回待独立复核。像素或文案改变后必须重新审图并更新审核哈希，再运行验收与打包；脚本不会自动把新图判为通过。运行组合需要 Pillow，使用资源本身不依赖 F 盘；重新核验来源时则需要原参考仓库和固定提交源码，或经核实的同哈希路径映射。交付 ZIP 排除功能参考克隆、旧启动器、官方游戏二进制与用户存档。
