# 青岚余生（暂定名）· Unity 美术资源导入建议

本阶段只交付图片、切片、状态和说明。**尚未在 Unity 中导入或验证**，没有 C#、Prefab、场景或业务接入交付。本建议针对后续 uGUI/TMP 或等价 UI 技术，不把离线图片验收写作引擎验收。

## 交付边界和目录

下列资源路径以本项目根目录为基准。可直接查看[完整资源索引](../../art-delivery/records/complete-resource-manifest.json)、[完整导入表](../../art-delivery/records/unity-import-complete.csv)及[文件规格验收](../../art-delivery/records/complete-resource-validation.json)。

- 正式通用资源：`art-delivery/resources/ui/`。
- 正式类别图标和生存物品图标：`art-delivery/resources/icons/`。
- 中文字体及许可证：`art-delivery/resources/fonts/`。
- 逐件规范、来源、SHA-256 与 Unity 建议参数：`art-delivery/records/asset-manifest.json`。
- 24 个现代生存图标的源图切片映射：`art-delivery/records/survival-icon-slices.json`。
- 完整独立资源索引：`art-delivery/records/complete-resource-manifest.json`；完整导入表：`art-delivery/records/unity-import-complete.csv`。
- 完整索引包含原 108 件控件／图标、3 张背景和 1 张人物立绘，共 **112 件正式独立图片资源**。原 108 件索引保持不变。2 张图标／标题母图只列为 `sourceOnly`，不计入运行 Sprite；字体、许可证、整屏设计、预览和记录同样不计入该数字。
- 背景：`art-delivery/resources/backgrounds/`；人物：`art-delivery/resources/characters/`。不将带字整屏设计图用作可拉伸的运行窗口底图。

功能研究来源为 Cataclysm-DDA；F 盘道家 UI 仅提供画法与经核实的可复用图片。上游技能名称、相性、区服、奖励和数值未移入本游戏规则。图标中的道家物件可用作主题类别徽标；现代电池、枪械、工具等采用独立的新生存物品图标，不能互相冒充。

## 默认设计合同

采用 **1920×1080 横屏设计画布**，这是本次美术阶段的合理默认值，不代表上游游戏只支持该分辨率。后续可用 Canvas Scaler 的 Scale With Screen Size，Reference Resolution 为 1920×1080，Match 值先取 0.5，再结合目标设备复核。所有关键文字、按钮、弹窗和滚动区域应按实际屏幕安全区重排。

角色、图标、圆徽标、装饰整体等比显示；只有资源清单明确提供 Border 和允许伸缩方向的板件使用 Sliced。源图本身的像素数、切片尺寸与整屏合成尺寸分别记录，不把九宫格放大、裁切或母图切片称作新的原生模型细节。

## TextureImporter 建议

| 参数 | 建议 |
|---|---|
| Texture Type | Sprite (2D and UI) |
| Sprite Mode | Single；本包已逐件切出，优先使用独立 PNG |
| Mesh Type | Full Rect，避免 UI 边缘或九宫格被紧包网格截断 |
| Pivot | 默认 (0.5, 0.5)，特殊锚点由页面布局定义 |
| Pixels Per Unit | 100，作为 UI 默认约定 |
| sRGB | 开启 |
| Alpha Is Transparency | 有 Alpha 通道的皮肤开启；保持原透明边缘 |
| Mip Maps | 关闭 |
| Filter | Bilinear；原图不属于像素画 |
| Wrap | Clamp |
| Compression | 首次视觉验收先用 None；平台压缩质量留待实机确认 |
| Max Size | 保持原始像素，按资源最大边选择，避免导入时无意缩小 |
| Atlas | 按 UI 皮肤、类别图标、物品图标、背景分别组织；建议 padding 至少 4–8 px，实机检查边缘串色 |

每个 Sprite 的 Border 数值按 manifest 中 **Left、Bottom、Right、Top** 顺序填写，单位是交付 PNG 的原始像素，不能把 Left/Top/Right/Bottom 顺序直接抄入 Unity。坐标映射与顶左裁切框另保存在切片记录中。

## 背景与人物导入建议

以下 4 件使用原生文件，没有为适配设计画布重新采样。均建议 Sprite (2D and UI)、Single、Full Rect、Simple、PPU 100、Pivot (0.5, 0.5)、Border (0, 0, 0, 0)、Max Size 2048、Bilinear、Clamp、sRGB 开启、Mip Maps 关闭，首次验收用无压缩。这些参数**尚未在 Unity 中验证**。

| ID / 文件 | 原生像素与通道 | 具体建议与来源记录 |
|---|---|---|
| entry-keyart | 1672×941 RGB | 入口、加载或菜单插画。字节复用本项目已生成入口图；邻接 `.source.json` 指向原始 `.generation.json`。RGB 无透明背景，Alpha Is Transparency 不适用。 |
| expedition-playfield | 1672×941 RGB | 探索／战斗界面场景插画，独立地点和目标文字覆盖于图上；不提供可行走地图、碰撞或导航数据。邻接 `.generation.json`。 |
| regional-map | 1672×941 RGB | 区域地图美术示例；地名、地点状态、路径、坐标和标记由后续独立 UI 与数据绑定。邻接 `.generation.json`。 |
| hero-survivor | 1024×1536 RGBA | 静态全身立绘；真实 Alpha 为 0–254，保留半透明柔边，开启 Alpha Is Transparency。完整轮廓等比显示，脚部位置由布局底部锚点决定；不包含骨骼或逐帧动画。邻接 `.generation.json`。 |

三张背景按比例使用 Cover 裁边或 Contain 留边，由具体页面可用区域决定，不九宫格拉伸。1672×941 在 1920×1080 设计图中铺满时约放大至 1.148 倍，这是排版缩放，不是原生 1080p 新细节；后续如需更大原生图片应另行制作。人物保持等比缩放，不将透明立绘横向拉宽，也不自动裁去画布边距改变对齐。

完整索引记录这 4 件的当前文件哈希、实际尺寸／模式／Alpha、邻接来源或生成记录哈希、配置目标、实际提交参数和实际返回证据。宿主未披露实际模型／质量，因此相应字段仍为未确认，不用配置目标代替生成证明。`complete-resource-validation.json` 只证明 112 文件可解码、哈希与规格一致，不代表 Unity 导入或运行验收。

## 常用九宫格

| ID / 文件 | 原始像素 | L / B / R / T | 使用规则 |
|---|---|---|---|
| panel-main | 1440×840 | 148 / 125 / 148 / 112 | 双向拉伸，保留云角和细金边 |
| panel-content | 1080×620 | 145 / 122 / 145 / 108 | 双向拉伸，文字保持在推荐内容区内 |
| panel-tooltip | 448×930 | 48 / 80 / 48 / 160 | 双向拉伸；标题装饰占据固定上边区域 |
| title | 716×145 | 180 / 34 / 170 / 31 | 新无字原画等比派生，实际绘制 609×137；优先横向伸缩 |
| section | 433×72 | 145 / 16 / 145 / 16 | 同源等比派生，实际绘制 285×64；横向伸缩 |
| button-primary-* | 460×112 | 82 / 34 / 82 / 30 | 横向伸缩，状态固定符号不纵向拉长 |
| button-secondary-* | 271×82 | 30 / 27 / 30 / 27 | 横向伸缩，标签为独立文字 |
| tab-* | 360×114 | 82 / 34 / 82 / 30 | 横向伸缩，选中勾记及边缘饰纹保持比例 |
| row-* | 360×96 | 82 / 31 / 82 / 27 | 横向伸缩；文字另行排版 |
| slot-* | 160×160 | 11 / 11 / 11 / 11 | 可拉伸方槽；内部物品图标单独等比显示 |
| progress-track / progress-fill | 324×23 / 60×23 | 7 / 7 / 7 / 7 | 横向伸缩；数值与语义标签分离 |
| scrollbar-track | 23×324 | 7 / 7 / 7 / 7 | 纵向伸缩，来自已绘制滑杆旋转派生 |

普通九宫格目标宽高不得小于固定边框之和。若目标按钮高度明显小于源图，应先按整体比例缩放其边框与尺寸，再仅沿许可方向伸缩；不能把带符号的整图强制纵向拉长。主面板大跨度缩放后还须复核纸纹、角饰和文字净空。

标题牌与分栏牌在验收中发现旧扁平切片残留原组队文字／天空及矩形抹字区，已被同一新生成无字玉绿云纹原画替换，旧污染输出不保留回退像素。新原画 `art-delivery/resources/ui/clean-header-master.png` 为原生 2203×714，逐图记录同目录保存；title 与 section 依实际 Alpha 裁去透明边距后等比缩小，不能称作新的模型生成或原生 716／433 图。

流苏会把整张图片的几何中点拉低，独立标题文字应使用 `textCenterNormalized: [0.5, 0.41]`：title 在画布 y≈59 px，section 在 y≈30 px。原生分栏牌建议文字 18–20 px，长标题另行横向展开牌面或改写，不通过压扁图形容纳。具体内容净空以 manifest 的 `textInsetsLeftTopRightBottom` 为准。

## 状态和对齐

按钮、页签、行与物品槽均提供 normal、pressed、selected、disabled、locked，**同一 stateFamily 画布尺寸完全相同**，Pivot 均为 (0.5, 0.5)。状态以独立文件切换，不改变布局坐标。

pressed 是已绘制控件的确定性明度变化；selected 采用已绘制的勾记或选中皮肤；locked 使用现有手绘锁形。disabled 和 locked 仍须配合明确的不可用原因和文字说明，不能只靠颜色或图形表达。它们只是美术资源，后续业务层必须实施交互禁用规则。

checkbox 另提供 normal、selected、disabled。search 提供 normal、selected、disabled，实际输入、焦点和校验由后续 UI 控件处理。paper-tile 是有意不透明的纸纹素材；其余通用皮肤具有真实透明边缘，不能据有 Alpha 通道就推定纸纹也应透明。

## 24 个生存图标与切片

母图请求为 6×4，但实际物件越过名义单元边界，因此本次**没有等格机械裁切**。每个物件依实际 Alpha 连通轮廓和附近的细碎构件隔离，保留柔和边缘，再按非均匀原生 bbox 裁出。统一导出到 256×256 RGBA 画布，最大内容 224 px，实际四边透明留白至少 16 px。

只在需要时缩小，不放大原生物件。每个物件的原生 bbox、隔离方法、源图 SHA-256、缩放系数、画布定位、Alpha 边界和输出哈希均在 `survival-icon-slices.json`。物品边缘已通过联系表实看，未将参考图的透明像素下 RGB 背景当成实色底。

文件 ID：`survival-battery`、`flashlight`、`bandage`、`water`、`food`、`wrench`、`wheel`、`scrap`、`bottle`、`rifle`、`ammo`、`magnifier`、`map`、`compass`、`campfire`、`terminal`、`circuit`、`book`、`backpack`、`radio`、`helmet`、`seeds`、`meat`、`pot`，每项均有 `survival-` 前缀。它们是图片与排版示例，正式物品 ID、名称和数值由后续游戏数据绑定。

## 字体、文字和图层

包内 `NotoSansCJKsc-Regular.otf` 从官方 Noto CJK 仓库取得，`OFL.txt` 随包保留。实际文件与许可 URL、SHA-256 记录在 asset-manifest。当前 F 盘目录未发现独立 TTF/OTF，因此没有复制其他项目或系统专有字体。后续 TMP 字库构建、字符集裁剪和渲染清晰度尚待 Unity 验证。

建议原生正文 24–28 px，次要文字 20–22 px，按钮 26–30 px，页面标题 34–42 px；最终以每张设计图文字区域说明为准。深玉底采用象牙字，纸底采用深玉／深棕字；状态语义颜色在纸面保持足够对比，禁用标签不与皮肤一起降低至不可读。

推荐图层：背景 → 暗幕或纸面 → 面板和装饰 → 列表／槽位底板 → 图标 → 原生动态文字 → 选择／焦点提示 → 弹窗 → 通知。动态名称、数量、时间、属性和按钮标签均独立，资源中固定锁、勾、加减等手绘符号在 manifest 明确标记。

## 本阶段验收与下阶段事项

每张主图与状态板的图片使用位置、源尺寸、目标矩形、缩放方式和实际预览 Border 已另行导出：[234 份使用位置总索引](../../art-delivery/records/resource-placement-index.json)、[字段说明](RESOURCE_PLACEMENTS.md)。它们与 `records/layouts/` 的独立文字区域配套，直接对应最终 PNG 哈希；是静态设计坐标建议，尚未转换或验证 RectTransform。

已完成 PNG 解码、尺寸、哈希、Alpha 通道、状态画布一致、九宫格边距合法性和图标留白检查，并实际查看状态及图标联系表。报告为 `art-delivery/records/resource-validation.json`，不代表 Unity 运行通过。

下一阶段需验证：Sprite 导入颜色／Alpha、九宫格缩放、TMP 字形与中英混排、Canvas 安全区、状态交换不跳动、滚动裁切、焦点和输入提示、图集打包与实际分辨率清晰度。届时再实施 C#、Prefab、场景、业务状态、接口和游戏运行联调。
