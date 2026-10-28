# 五行奇谈 · 通用 UI 控件 v10

当前 39 套 PNG／SVG 依据[指定风格与提示词](../UI_SPEC.md#2-统一视觉与控件层级)从 v10 内置生成原画重切，采用深玉绿、象牙米白、暖金与轻巧云纹，保留道家 Q 版及适量节庆。其他游戏图仅参考功能。[v10 来源与复现](../../qdao_ui_style_recut_v10/README.md)、[逐件映射](../../qdao_ui_style_recut_v10/source-map.common.json)记录实际原生尺寸和裁切，SVG 内嵌新 PNG。

查看 [可视总览](overview.html)、[总览 PNG](overview.png)、[十枚徽标与小尺寸总览](badges_overview.png) 和 [资源清单](manifest.json)。总览中的中文只是检查用的独立文字，**39 个 SVG 和 39 个 PNG 控件均未烘焙动态文字**。

## 资源范围

| 类别 | 每张尺寸 | 状态 / 数量 |
|---|---|---|
| `primary_button` | 460 × 112 | normal / selected / disabled，共 3 张 |
| `tab` | 360 × 114 | 三态，共 3 张 |
| `list_row` | 360 × 96 | 三态，共 3 张 |
| `server_card_wide` | 640 × 141 | 三态，共 3 张 |
| `server_card_medium` | 520 × 126 | 三态，共 3 张 |
| `search` | 420 × 84 | 三态，共 3 张 |
| `summary_bar` | 1280 × 79 | 1 张 |
| `main_frame` | 1440 × 840 | 1 张 |
| `content_panel` | 1080 × 620 | 1 张 |
| `round_badge` | 120 × 120 | 太极、楼阁、莲花、山、炼丹炉、剑、水纹、罗盘、桃灵、火焰，共 10 张 |
| `status_dot` | 32 × 32 | 绿勾、橙感叹号、灰横线，共 3 张 |
| `recommend_badge` | 96 × 40 | 1 张，无文字；客户端叠加“推荐” |
| `check` / `lock` | 48 × 48 | 各 1 张 |
| `gold_flower` | 120 × 120 | 1 张 |
| `cloud_corner` | 160 × 160 | 1 张；可镜像至其余三角 |

`svg/` 是保持原 viewport 和布局契约的便携包装文件（内嵌 AI 位图，并非无限细节矢量），`png/` 是与清单尺寸一致的透明 RGBA 导出。边缘透明区域包含阴影留白，不是额外可点击区域。圆徽标中的楼阁、莲花、山等是功能图形，不代表生产职业或服务器类型。

## 九宫格与原生文字

`manifest.json` 为可伸缩板件记录 `nine_slice.left/top/right/bottom`，单位是**原始 PNG 像素**；这四个值是保持不变的边框厚度，`center` 同时给出可拉伸矩形。边框值已经包含阴影和透明留白。圆徽标、状态点与装饰不做九宫格，等比缩放。

`minimum_size` 防止两侧固定区域碰撞；`content_insets` 是推荐文字和内容边距；`text_color` 是对应底色的文本颜色。服务器卡片右侧预留独立圆徽标区域，不会把圆徽标一起拉伸。实际触控尺寸、排版、锚点和像素密度由客户端确定。

**带勾记、锁形或放大镜的六类三态控件及摘要栏只按原高度做横向九宫格**，清单中为 `resize_axes: horizontal` 与 `fixed_height`；否则标识处于左/右边条中段，纵向拉伸会改变其形状。主框架和内容面板标记为 `resize_axes: both`，允许双向九宫格。若确需改变按钮高度，可整体等比缩放，或将标识分离后用原生图标叠加；不要直接纵向拉伸成品 PNG。

保持正方形徽标比例。背景纹理与渐变也会随九宫格中间区域伸缩，适用于有限范围的宽高变化；跨度很大时优先按目标尺寸从母图重新适配或调整原生布局，不把细长摘要栏拉成整页面板。

动态游戏名、服名、角色名、状态、搜索输入和按钮字由客户端文字层绘制。建议原尺寸按钮 / 页签 28–32 px，列表 / 卡片 / 搜索 24–28 px；缩小整个总览不是运行时文字尺寸规范。深绿底使用米白字，浅底使用深色字；禁用态仍保留可读文字，不用透明度把标签一起淡化。

## 状态与交互边界

- `selected` 同时使用勾记、边缘标识和底部小三角，不能仅靠颜色判断。选中不是推荐，也不等于 hover 或键盘焦点。
- `disabled` 包含锁形。客户端还应显示明确原因，并禁止相应动作；返回、清空或改选等恢复入口按业务保持可用。
- 状态点用颜色加形状区分；绿 / 橙 / 灰分别用于可用 / 繁忙 / 不可用的设计示意。服务端实际枚举由客户端映射，橙色不自动意味着禁入。
- 推荐徽标与勾选图标分别使用；“推荐”文字通过客户端叠加。
- 搜索框三态是视觉资源，不实现输入、焦点或验证。焦点与悬停需要原生控件在当前资源上额外提供可辨认的轮廓；此包不提供程序逻辑。

本套件只覆盖上述控件，未实现引擎导入、运行时九宫格、鼠标/键盘交互或页面事件绑定。

## 本地重建与验收

统一按 [v10 重建步骤](../../qdao_ui_style_recut_v10/README.md#确定性重建)执行。先提取保存的原画，再运行 `python qdao_ui_style_recut_v10/tools/build_common_legacy.py` 生成暂存控件；通过全量核验和视觉检查后，由 v10 发布器写入本目录。旧 `build.mjs` 已阻止生成历史 v7 皮肤，避免覆盖当前素材。

当前逐件信息以 `manifest.json`、v10 来源映射和 [全量验证](../../qdao_ui_style_recut_v10/validation.json)为准。旧 `validation.json`、`badge_validation.json` 和部分 SVG／HTML 总览可能是历史报告／预览，不能代替 v10 的哈希、透明边缘与九宫格检查。当前资源验收图统一从 v10 入口查看。

十枚徽标名称和语义保持原合同：太极、楼阁、莲花、山、炼丹炉、剑、水纹、罗盘、桃灵、火焰。v6 原生矢量补齐过程在 `badge_design_brief.md` 留档；当前徽标是 v10 新绘位图。圆形纹样保持比例，较小尺寸应配原生可读标签。未执行引擎导入或运行时交互验收。

2026-09-12：通用组件总览和十徽标总览的 PNG／SVG 已重新合成为当前 v10 皮肤，仍保留原尺寸、布局、标签和小尺寸检查位置。[本轮来源与验收](../../qdao_festival_refinement_20260910/component-overviews/publication.json)；39个正式控件像素未改。


## 项目关联

<!-- project-association-dao-survivors-20261026 -->
### 道途幸存者（暂定名）· 全游戏 UI 美术阶段

- 核实日期：2026-10-26。本对话制作目录：`E:\work\image\DaoSurvivors`；暂定项目名“道途幸存者”。[Roo-Roo-Roo/survivors-roguelike-kit](https://github.com/Roo-Roo-Roo/survivors-roguelike-kit) 仅为功能与流程参考，副本位于新项目 `.reference/survivors-roguelike-kit/`；**成果GitHub待用户补充**，不把参考仓库当作成果远端。
- 美术参考仓库为 `F:\work\image`，当前核实远端为 `https://luyuacpp.visualstudio.com/image/_git/image`，GitHub地址待确认；对应素材目录 `qdao_ui_redesign_v5/components/`。
- **直接复用**：`png/round_badge_taiji.png` 位于新项目 `art/icons/icon-taiji.png`。本目录 `png/` 中 primary_button、tab、list_row 各normal/selected/disabled三态，以及 `check.png`、`lock.png`，共11件原字节复制至 `art/common/states/`。每组状态保持同一画布；selected带勾，disabled带锁；没有冒称已有pressed或独立整幅locked图。
- 当前范围为**全游戏图片与UI美术交付**；资源使用新项目 `art/common/`、`art/characters/`、`art/icons/`、`art/illustrations/`、`art/fonts/`。早期 `Assets/` 初稿冻结保留，不属于本阶段验收；本条不表示Unity导入、Prefab、C#、场景实现或运行联调已经完成。
- 逐资源使用与尺寸/Alpha/边距/旧源更换记录见新项目 `docs/art-reference-extension.md`、`docs/art-extension-sources.json`；新生成图按各自来源记录追溯。保留其他项目关联，本次未操作F仓库Git HEAD、index或refs，未提交、推送或发布。
<!-- /project-association-dao-survivors-20261026 -->

<!-- project-association-directory: E:\work\image\Veloren_QDao_UI_20261026_060716 -->
### Veloren 功能参考 · 道家 Q 版 UI 美术包（2026-10-26）

- 本次项目：Veloren 功能参考 · 道家 Q 版 UI 美术包（游戏正式名待定，Veloren仅为功能参考标识）。功能参考 GitHub：<https://github.com/veloren/veloren.git>；成果保存 GitHub：待用户提供，未提交、推送或发布。
- 美术参考仓库：`F:\work\image`；本对话制作目录：`E:\work\image\Veloren_QDao_UI_20261026_060716`。未把功能参考仓库当作成果远端。
- 核实日期：2026-10-26。关联确认的是本地美术来源和实际文件使用，不代表Unity导入、Prefab、C#、场景组装、业务接入或在线运行已验收。来源文字按原证据保留；不以当前图像配置回填旧图实际型号/质量。
- 参考素材相对目录：`qdao_ui_redesign_v5/components/png/`；关联类型：**直接复用**。39张正式无字控件已按原字节复制至新项目 `assets/common/`，用于全套页面共享的面板、按钮三态、页签、列表、搜索、圆徽、锁/勾及状态提示。九宫格、横向伸缩限制、尺寸、Alpha与文字边距沿源manifest核实。
- 本项目另派生按钮按下态，属于本地亮度处理，未再次调用生成模型、不增加原生细节；实际命名和逐件映射见新项目 `records/reused-assets.json`。源目录图片未修改。
<!-- /project-association-directory: Veloren_QDao_UI_20261026_060716 -->




<!-- project-association-directory: E:\work\image\OpenSC2K_20261026_061035 -->
### OpenSC2K 道家Q版城市经营UI（云岫城记，暂定）（2026-10-26）

- 项目／任务：**OpenSC2K 道家Q版城市经营UI（云岫城记，暂定）**。功能参考 GitHub：[OpenSC2K/OpenSC2K](https://github.com/OpenSC2K/OpenSC2K.git)；该地址只用于研究城市经营功能与流程。成果 GitHub：**待用户补充**，当前没有提交、推送或发布本次成果。
- 美术参考仓库：`F:\work\image`；本对话正式制作目录：`E:\work\image\OpenSC2K_20261026_061035`。功能参考代码独立克隆于该目录 `reference/OpenSC2K/`，不与美术成果远端混用。
- 核实日期：2026-10-26。本记录只确认真实图片／资源关联；本阶段是本地图片与UI美术，未开展Unity工程、Prefab、C#、场景组装、接口或运行联调。旧项目的Unity验收记录不等于本项目验证。
- 关联类型：**直接复用**。以下25件现存PNG已核对Alpha／尺寸并按原字节复制；源路径以美术仓库根为基准，目标路径以本对话制作目录为基准。逐件哈希、原尺寸、Border L/B/R/T及历史来源文字见本项目 `assets/common-manifest.json` 与 `records/reuse-provenance.json`。

| 参考素材仓库相对路径 | 本项目实际资源路径 |
|---|---|
| `qdao_ui_redesign_v5/components/png/primary_button_normal.png` | `assets/common/button_large_normal.png` |
| `qdao_ui_redesign_v5/components/png/primary_button_selected.png` | `assets/common/button_large_selected.png` |
| `qdao_ui_redesign_v5/components/png/primary_button_disabled.png` | `assets/common/button_large_disabled.png` |
| `qdao_ui_redesign_v5/components/png/tab_normal.png` | `assets/common/tab_normal.png` |
| `qdao_ui_redesign_v5/components/png/tab_selected.png` | `assets/common/tab_selected.png` |
| `qdao_ui_redesign_v5/components/png/tab_disabled.png` | `assets/common/tab_disabled.png` |
| `qdao_ui_redesign_v5/components/png/list_row_normal.png` | `assets/common/list_row_normal.png` |
| `qdao_ui_redesign_v5/components/png/list_row_selected.png` | `assets/common/list_row_selected.png` |
| `qdao_ui_redesign_v5/components/png/list_row_disabled.png` | `assets/common/list_row_disabled.png` |
| `qdao_ui_redesign_v5/components/png/search_normal.png` | `assets/common/search_normal.png` |
| `qdao_ui_redesign_v5/components/png/search_selected.png` | `assets/common/search_selected.png` |
| `qdao_ui_redesign_v5/components/png/search_disabled.png` | `assets/common/search_disabled.png` |
| `qdao_ui_redesign_v5/components/png/status_dot_green.png` | `assets/common/status_good.png` |
| `qdao_ui_redesign_v5/components/png/status_dot_orange.png` | `assets/common/status_warning.png` |
| `qdao_ui_redesign_v5/components/png/status_dot_gray.png` | `assets/common/status_inactive.png` |
| `qdao_ui_redesign_v5/components/png/check.png` | `assets/common/check.png` |
| `qdao_ui_redesign_v5/components/png/lock.png` | `assets/common/lock.png` |
| `qdao_ui_redesign_v5/components/png/content_panel.png` | `assets/common/panel_content.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_taiji.png` | `assets/icons-reused/icon_taiji.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_pagoda.png` | `assets/icons-reused/icon_pagoda.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_mountain.png` | `assets/icons-reused/icon_mountain.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_water.png` | `assets/icons-reused/icon_water.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_compass.png` | `assets/icons-reused/icon_compass.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_flame.png` | `assets/icons-reused/icon_flame.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_lotus.png` | `assets/icons-reused/icon_lotus.png` |

- 实际使用位置：本项目 `designs/` 城市经营界面的通用窗口、分栏纸面、标题、操作按钮、卡片／列表／页签、数值与滑杆、设置选择、锁定与提示，以及 `previews/` 状态预览。已渲染页面的逐资源使用位置以 `records/composition-manifest.json` 为准；其余状态件作为正式公共资源库交付，不能据此声称每件已在Unity运行。
- 所有动态标题、资金、人口、日期、数量、操作文案独立排版；没有将本目录原属性／服务器／装备业务转入城市经营系统。九宫格与Pivot在本项目中仍为Unity导入建议，待下一阶段实测。
<!-- /project-association-directory: OpenSC2K_20261026_061035 -->
