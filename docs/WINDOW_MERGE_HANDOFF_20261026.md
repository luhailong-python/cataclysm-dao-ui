# 窗口归并交接 · 2026-10-26

## 停止范围与唯一主窗口

- 本窗口原目录：`E:\work\image\cataclysm-dao-ui`。本文件仅交接，不继续新增生成、重复制作、实现或发布。
- 协调通知指定的唯一继续窗口：`01a17800-a901-75a2-963c-09c4ca8cfc09`。
- 唯一主目录：`E:\work\image\CataclysmDDA_道家UI_20261026_073832`，本次已只读核实存在。没有向该目录写文件，也没有逐件合并或覆盖其成果。
- 本次仅新增本交接文件；不删除、不搬移、不改 F 盘、不操作 Git、不向其他 chat 发消息。等待协调者归档。

## 当前采用入口与完成状态

本窗口最新采用入口是 `art-delivery/`，不是此前的 `app/` 启动器。

| 内容 | 本目录内路径 |
|---|---|
| 离线完整图集 | `art-delivery/previews/index.html` |
| 六屏概览 | `art-delivery/previews/preview-overview.jpg` |
| 主设计图 / 状态板 | `art-delivery/designs/screens/` / `art-delivery/designs/states/` |
| 正式独立资源 | `art-delivery/resources/` |
| 功能及状态清单 | `art-delivery/records/ui-master-manifest.json`、`art-delivery/previews/UI_COVERAGE.md` |
| 全资源、尺寸、Alpha、源 Border | `art-delivery/records/complete-resource-manifest.json`、`unity-import-complete.csv` |
| 每图独立文字区域 | `art-delivery/records/layouts/` |
| 图片实际使用矩形及缩放 | `art-delivery/records/resource-placement-index.json`、`resource-placements/` |
| 人读 / 机器验收 | `art-delivery/ACCEPTANCE.md`、`art-delivery/records/FINAL_ACCEPTANCE.json` |
| Unity 建议 | `docs/art-v2/UNITY_IMPORT.md`、`RESOURCE_PLACEMENTS.md` |
| 交付 ZIP | `exports/qinglan-ui-art-20261026.zip` |
| ZIP 清单 / CRC 核验 | `exports/package-manifest.json`、`exports/package-validation.json` |

本窗口固定清单已完成：100 类源码研究界面加通用弹窗，共 101 张 1920×1080 主图、133 张状态板，604 条源码状态加 6 条通用状态，共 610 条；112 件正式独立资源，另有 2 张必要制作母图。流程为 8 张 PNG 及 8 份 SVG，位置映射 234 份。

当前 `FINAL_ACCEPTANCE.json` 为 passed：12,127 项通过，0 项失败；`ui-master-manifest.json` 的 artAcceptance 为 passed。该结论只对应本窗口现存文件和清单，不表示主目录已采用、归并已验收或 Unity 已接入。

ZIP 为 636,432,074 字节、977 个条目，SHA-256：

`86dd5df7aae2696753601c6d5b273cc84d2e4df70eddbf62c5a5872172104775`

ZIP 已通过 CRC 与必需条目核验；排除了参考游戏克隆、旧启动器、官方游戏二进制、用户存档和 `.local/` 临时资料。归并交接文件在打包之后新增，因此不在该既有 ZIP 内；不重新打包。

## 本窗口独立产出的采用候选

以下为本窗口实际新生成的 5 张原画及派生资源，不将重复的 F 盘素材算作新生成。未对唯一主目录进行全量哈希去重，故“独立产出”不等于已证明在主目录全局独有；协调者可据下列哈希对账。

| 原画路径（相对本目录） | 原生尺寸 | SHA-256 |
|---|---|---|
| `art-delivery/resources/backgrounds/expedition-playfield.png` | 1672×941 RGB | `514ec6c3e037d13ec5e4857cfa0ec9f8994a3cd9636205e239e435ca8a4e12ff` |
| `art-delivery/resources/backgrounds/regional-map.png` | 1672×941 RGB | `c2be49a7ec4c36936f156b6e6a28eb5925f0b4bb930031ec0dd9eb5b05674bef` |
| `art-delivery/resources/characters/hero-survivor.png` | 1024×1536 RGBA | `89402f654adbe05a1d1e93a1b0ec8c2f9bb2ca512a5d19d12d5ebd2cf526f471` |
| `art-delivery/resources/icons/survival-icons-master.png` | 1536×1024 RGBA | `00a632708b989c27b740243dcc349191fd5824c89befa6fa4d540686a5b43a53` |
| `art-delivery/resources/ui/clean-header-master.png` | 2203×714 RGBA | `22a9a26495a86065e1ed4f0c8642d07852f376cecef2c6a23ab928ce7c816564` |

- `resources/icons/survival-*.png` 的 24 枚生存物品图标：非均匀 Alpha 边界隔离、仅缩小、居中到 256×256。切片坐标和处理证据在 `records/survival-icon-slices.json`，不能按名义 6×4 等格重切母图。
- `resources/ui/title.png`、`section.png`：从上述无字新牌面等比派生，清除了曾发现的旧文字/天空污染，源 Border 和文字中心 y=0.41 在资源合同中。
- `resources/backgrounds/entry-keyart.png` 是本窗口此前已生成入口插画的字节复用，不列入本轮 5 张新图；邻接 `.source.json` 保留来源。
- 其余通用皮肤及类别图标包括 F 盘复用和确定性状态派生，精确关系在 `records/asset-manifest.json`、`complete-resource-manifest.json`，不能归并后重复计为原生新图。
- 可单独采用的研究文档：`docs/art-v2/research-core.json`（51 类）、`research-advanced.json`（49 类）、`copy-core.json`（308 条状态）、`copy-advanced.json`（296 条状态）、`UI_REQUIREMENTS_CORE.md`、`advanced-systems.md`、`FLOWS.md`。
- 全部整屏是原画/控件与独立中文的确定性合成，不是 101 次模型原生整屏生成。生产脚本在 `tools/art_screens.py`、`art_screen_data.py`；采用本批图片无需重新执行生成。

## 来源与证据

- 功能参考：`https://github.com/CleverRaven/Cataclysm-DDA`，固定提交 `eb86dffd20072d6fde54af568cf229f3cd4d751f`，只读克隆在 `reference/Cataclysm-DDA`。成果提交仓库待用户提供，不能混作上游。
- 美术参考：`F:\work\image`；已核实 origin 为 `https://luyuacpp.visualstudio.com/image/_git/image`（Azure DevOps），其 GitHub 地址待确认。当前 F 盘只读。
- 实际输入主参考为邮件 `designs/mail-ui-v1/01-mail-event.png` 和组队 `designs/team-ui-v2/team-ui-v2.png`；本地副本在 `docs/reference-images/`。
- 每张新图的 `.generation.json` 邻接原画，提示词在 `art-delivery/records/*.prompt.txt`。配置目标为 gpt-image-2.5-sunburst / max；内置入口实际型号和质量未披露，均为未确认，不得归并时补写为已确认。
- 项目关联已统一保存在 `docs/image-reference-associations.md`；迁移核验在 `docs/image-reference-association-migration-20261026.json`。不要恢复向 F 盘 README 写关联的旧入口。
- 最终独立视觉证据：`docs/art-v2/REVIEW_CORE_ART.json`、`REVIEW_CORE_STATES_A.json`、`REVIEW_CORE_STATES_B.json`、`REVIEW_ADVANCED.json`；资源、位置映射和文档核验在各自 validation / review JSON。
- 最后状态板脚注修复仅改变 `[93,923,207,935]` 区域；101 主图字节完全不变，状态卡正文/控件像素不变。报告明确区分旧完整实看、新版代表图实看和独立限定像素差复验，不能改写成全部新版均重新实看。

## 在途、子工及待接入

- 图像调用：无已发出未返回调用；5 张新原画已全部落盘并有逐图证据。
- 生成、合成、位置导出、验收和打包命令：均已结束，无本窗口在途素材写入；本文件保存完成后本窗口不再写制作文件。
- 本次只读进程核查未发现匹配本目录且使用 4377 端口的 Python 预览服务；不重新启动。预览以离线 HTML/PNG 路径为准。
- `/root/advanced_footer_recheck`：completed；已通知停止新增，无需再写报告。
- `/root/art_final_qa`：列表显示 pending_init；已发送停止新增/停止写入指令并调用 interrupt，返回此前状态 pending_init。没有活动图像调用；未将“已通知并中断”写作子工明确回执。
- 其余本窗口制作/研究/复核子工此前均已完成或不在活动列表；当前没有活动生成子工。没有向其他 chat 发送消息。
- Unity 工程、C#、Prefab、真实业务绑定与运行联调未开展，按用户阶段约定留待主窗口后续处理。
- 归并后的主项目采用、去重和整体验收尚未进行；本窗口不越权宣称已归并通过。
- 源库指定 `qdao_ui_redesign_v5/UI_SPEC.md` 当前缺失，未从旧 Git 恢复。本批按用户明确风格和真实参考图执行。
- 67 处小高度预览的目标九宫格中心带高为 0；源 Border 合法、没有负中心，已在 `records/placement-validation.json` 如实记录，Unity 接入需按真实 RectTransform 重算。
- `.local/state-review-baseline-20261026/` 留有 133 张临时修复对比图。此前清理被自动审批审查拒绝（blocked by policy），记录在 `art-delivery/records/cleanup-deferred.json`；未打入 ZIP。此次遵守保留要求，不再次清理。
- `app/`、`assets/`、`qa/`、旧启动脚本与 `.local/runtime/` 属于更早启动器阶段，保留但不计入当前 UI 美术包，不建议混入主项目美术采用入口。

## 交接边界

本窗口到此停止生产。所有有效成果保留原位，不移动、不删除、不提交、不推送。该文件为有界交接，等待协调者核对和归档；任何归并采用均由指定唯一主窗口执行。
