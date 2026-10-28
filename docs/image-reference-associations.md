# 美术参考素材关联记录

2026-10-26，按用户要求将误写在 `F:\work\image` 素材 README 中的本项目关联记录迁回本项目。素材来源、实际使用位置、哈希及生成证据按原记录保留。

每节注明迁移前的 README 位置；原文中的“本目录”“本参考仓库”按该来源路径理解，本项目资源与证据的相对路径以本项目根目录为准。核实日期与阶段描述为原记录的时间状态。

---

原记录位置：[designs/mail-ui-v1/README.md](F:/work/image/designs/mail-ui-v1/README.md)

### Cataclysm-DDA · 道风主题启动器（2026-10-26）

- 新项目名称：Cataclysm: Dark Days Ahead · 道风主题启动器；独立位置 `E:\work\image\cataclysm-dao-ui`。用户纠正为每个新项目单独目录后采用此路径，与父目录现存 Unity 工程分开。
- 游戏上游 GitHub：<https://github.com/CleverRaven/Cataclysm-DDA>；本地主题交付的仓库／发布远端尚未指定，未向上游提交或推送。
- 本参考仓库远端：<https://luyuacpp.visualstudio.com/image/_git/image>（Azure DevOps）；参考仓库 GitHub 地址待确认。
- 参考仓库素材目录：`designs/mail-ui-v1`；实际查看并使用 `01-mail-event.png`，PNG 真字节与 SHA 已核实。
- 关联类型：风格参考。完整参考副本保存于新项目 `docs/reference-images/mail-style.png`，在内置生图调用中作为真实图片输入，生成新项目 `assets/art/survivor-keyart.png`；未将邮件整屏用作运行背景或复制业务文案。
- 新项目实际使用位置：`app/gui.py` 使用新插画；输入、模型／质量证据及哈希分别见 `docs/ASSET_SOURCES.json` 与 `assets/art/survivor-keyart.png.generation.json`。
- 核实日期：2026-10-26。该关联只属于本地主题启动器，不代表官方上游已采用本素材，不替换现有五行奇谈客户端关联。

---

原记录位置：[designs/team-ui-v2/README.md](F:/work/image/designs/team-ui-v2/README.md)

### Cataclysm-DDA · 道风主题启动器（2026-10-26）

- 新项目名称：Cataclysm: Dark Days Ahead · 道风主题启动器；独立位置 `E:\work\image\cataclysm-dao-ui`。与父目录现存 Unity 工程分别管理。
- 游戏上游 GitHub：<https://github.com/CleverRaven/Cataclysm-DDA>；本地主题交付的仓库／发布远端尚未指定，未向上游提交或推送。
- 本参考仓库远端：<https://luyuacpp.visualstudio.com/image/_git/image>（Azure DevOps）；参考仓库 GitHub 地址待确认。
- 参考仓库素材目录：`designs/team-ui-v2` 与 `designs/team-ui-v2/unity-slices`。
- 关联类型：风格参考与直接复用。`team-ui-v2.png` 的完整参考副本保存于新项目 `docs/reference-images/team-style.png`，已作为新主视觉的真实生成输入。五张无字透明皮肤 `member_row`、`title_plate`、`section_plate`、`button_primary`、`button_secondary` 从 `unity-slices/png` 逐字节复制；尺寸、RGBA、哈希和九宫格边距均保留来源记录。
- 新项目实际使用位置：`assets/ui/*.png`、`assets/art/survivor-keyart.png`、`app/gui.py`。没有复制组队业务文案；新项目的世界列表、设置与按钮为原生控件和真实本地数据。
- 核实日期：2026-10-26。来源清单为新项目 `docs/ASSET_SOURCES.json`，逐图记录为 `assets/art/survivor-keyart.png.generation.json`。本关联不代表官方游戏内部 C++ UI 已换肤，不替换现有五行奇谈客户端关联。

---

原记录位置：[qdao_ui_redesign_v5/README.md](F:/work/image/qdao_ui_redesign_v5/README.md)

### Cataclysm-DDA · 道风主题启动器（2026-10-26）

- 新项目：Cataclysm: Dark Days Ahead · 道风主题启动器，独立目录 `E:\work\image\cataclysm-dao-ui`；游戏上游为 <https://github.com/CleverRaven/Cataclysm-DDA>，本地交付仓库／发布远端尚未指定。
- 本参考仓库远端：<https://luyuacpp.visualstudio.com/image/_git/image>（Azure DevOps），其 GitHub 地址待确认。
- 参考仓库相对目录：`qdao_ui_redesign_v5`。已实际查看 `01_login_2560x1080.png` 并读取本 README；指定 `UI_SPEC.md` 当前缺失，未从旧 Git 恢复。
- 关联类型：风格参考及入口控件层级研究；未复制本目录图片作为新项目运行素材，未在本次生图中附入该登录图，未采用五行奇谈的标题、区服或账号流程。
- 新项目对应位置：`app/gui.py` 的启动首页层级、`docs/UI_SPEC.md`、`docs/ASSET_SOURCES.json`。实际新插画输入为邮件和组队两张主风格图，另在各自 README 记录。
- 核实日期：2026-10-26。仅为本地启动器设计关联，不代表官方上游采用，不覆盖原客户端关联。


---

<!-- local-association: qinglan-cataclysm-ui-art-20261026 -->
## 当前全游戏 UI 美术阶段：青岚余生（暂定名）

按最新通知，`F:\work\image` 此后仅作只读美术参考。所有后续关联维护集中在本文件；本节迁回本制作子任务刚追加的来源记录，不再向 F 盘新增关联。 清理已核验：7 个原有 README 的原正文按字节保留，2 个仅由本子任务新建且没有其他文字的关联 README 已删除；本节中的 F 盘 README 路径为迁移前位置，不表示关联仍留在 F 盘或文件仍存在。逐项前后哈希、移除内容及工具写入入口核查见 `docs/image-reference-association-migration-20261026.json`。
### 青岚余生（暂定名）全游戏道家Q版UI美术（2026-10-26）

- 功能参考 GitHub：<https://github.com/CleverRaven/Cataclysm-DDA>；固定研究提交 `eb86dffd20072d6fde54af568cf229f3cd4d751f`，仅用于研究功能、系统与流程，不是成果保存仓库，也不向其提交或推送。
- 成果 GitHub：**待用户后续提供**。本阶段未执行成果 Git 提交、推送或发布。
- 本对话制作目录：`E:\work\image\cataclysm-dao-ui`；本阶段正式美术位于 `art-delivery/`，后续资源使用目标为 Unity。
- 美术参考仓库：`F:\work\image`；已核实 origin 为 `https://luyuacpp.visualstudio.com/image/_git/image`（Azure DevOps），美术仓库自身的 GitHub 地址待确认，与功能参考及成果地址分别管理。
- 核实日期：2026-10-26。精确来源、原图/导出尺寸、SHA-256、处理步骤、Alpha、状态与九宫格边距见新项目 `art-delivery/records/asset-manifest.json`；现代生存图标切片另见 `art-delivery/records/survival-icon-slices.json`。
- 本条只记录当前整款游戏 UI 美术阶段的实际来源；旧 `app/` 启动器、其运行截图及历史测试不计作本次美术完成或 Unity 接入验收。当前不制作 Unity 工程、C#、Prefab 或业务接入，不代表官方上游采用本素材，不改写其他项目及历史阶段的关联。

### 来源：`qdao_ui_redesign_v5/components`

原关联 README：`F:\work\image\qdao_ui_redesign_v5\components\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用与派生使用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `qdao_ui_redesign_v5/components/png/check.png` | `art-delivery/resources/ui/button-secondary-selected.png`、`art-delivery/resources/ui/check.png`、`art-delivery/resources/ui/slot-selected.png` |
| `qdao_ui_redesign_v5/components/png/cloud_corner.png` | `art-delivery/resources/ui/cloud-corner.png` |
| `qdao_ui_redesign_v5/components/png/content_panel.png` | `art-delivery/resources/ui/panel-content.png` |
| `qdao_ui_redesign_v5/components/png/gold_flower.png` | `art-delivery/resources/ui/gold-flower.png` |
| `qdao_ui_redesign_v5/components/png/list_row_disabled.png` | `art-delivery/resources/ui/row-disabled.png` |
| `qdao_ui_redesign_v5/components/png/list_row_normal.png` | `art-delivery/resources/ui/row-locked.png`、`art-delivery/resources/ui/row-normal.png`、`art-delivery/resources/ui/row-pressed.png` |
| `qdao_ui_redesign_v5/components/png/list_row_selected.png` | `art-delivery/resources/ui/row-selected.png` |
| `qdao_ui_redesign_v5/components/png/lock.png` | `art-delivery/resources/ui/button-primary-locked.png`、`art-delivery/resources/ui/button-secondary-locked.png`、`art-delivery/resources/ui/lock.png`、`art-delivery/resources/ui/row-locked.png`、`art-delivery/resources/ui/slot-locked.png`、`art-delivery/resources/ui/tab-locked.png` |
| `qdao_ui_redesign_v5/components/png/main_frame.png` | `art-delivery/resources/ui/panel-main.png` |
| `qdao_ui_redesign_v5/components/png/primary_button_disabled.png` | `art-delivery/resources/ui/button-primary-disabled.png` |
| `qdao_ui_redesign_v5/components/png/primary_button_normal.png` | `art-delivery/resources/ui/button-primary-locked.png`、`art-delivery/resources/ui/button-primary-normal.png`、`art-delivery/resources/ui/button-primary-pressed.png` |
| `qdao_ui_redesign_v5/components/png/primary_button_selected.png` | `art-delivery/resources/ui/button-primary-selected.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_compass.png` | `art-delivery/resources/icons/icon-compass.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_flame.png` | `art-delivery/resources/icons/icon-fire.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_furnace.png` | `art-delivery/resources/icons/icon-crafting.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_lotus.png` | `art-delivery/resources/icons/icon-morale.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_mountain.png` | `art-delivery/resources/icons/icon-map.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_pagoda.png` | `art-delivery/resources/icons/icon-settlement.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_peach_spirit.png` | `art-delivery/resources/icons/icon-herbs.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_sword.png` | `art-delivery/resources/icons/icon-sword.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_taiji.png` | `art-delivery/resources/icons/icon-martial.png` |
| `qdao_ui_redesign_v5/components/png/round_badge_water.png` | `art-delivery/resources/icons/icon-water.png` |
| `qdao_ui_redesign_v5/components/png/search_disabled.png` | `art-delivery/resources/ui/search-disabled.png` |
| `qdao_ui_redesign_v5/components/png/search_normal.png` | `art-delivery/resources/ui/search-normal.png` |
| `qdao_ui_redesign_v5/components/png/search_selected.png` | `art-delivery/resources/ui/search-selected.png` |
| `qdao_ui_redesign_v5/components/png/status_dot_gray.png` | `art-delivery/resources/ui/status-gray.png` |
| `qdao_ui_redesign_v5/components/png/status_dot_green.png` | `art-delivery/resources/ui/status-green.png` |
| `qdao_ui_redesign_v5/components/png/status_dot_orange.png` | `art-delivery/resources/ui/status-orange.png` |
| `qdao_ui_redesign_v5/components/png/tab_disabled.png` | `art-delivery/resources/ui/tab-disabled.png` |
| `qdao_ui_redesign_v5/components/png/tab_normal.png` | `art-delivery/resources/ui/tab-locked.png`、`art-delivery/resources/ui/tab-normal.png`、`art-delivery/resources/ui/tab-pressed.png` |
| `qdao_ui_redesign_v5/components/png/tab_selected.png` | `art-delivery/resources/ui/tab-selected.png` |

- 通用控件保持各状态画布一致、真实透明外缘和记录中的许可伸缩方向；本项目当前标题牌来自新增无字原画，未将原扁平组队标题当成通用牌。圆徽标只作类别美术示意，不作为上游世界/角色的业务真值。

### 来源：`designs/attribute-panels/v2-painted/unity-slices`

原关联 README：`F:\work\image\designs\attribute-panels\v2-painted\unity-slices\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用与派生使用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/attribute-panels/v2-painted/unity-slices/png/button_secondary.png` | `art-delivery/resources/ui/button-secondary-disabled.png`、`art-delivery/resources/ui/button-secondary-locked.png`、`art-delivery/resources/ui/button-secondary-normal.png`、`art-delivery/resources/ui/button-secondary-pressed.png`、`art-delivery/resources/ui/button-secondary-selected.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/dropdown_arrow.png` | `art-delivery/resources/ui/dropdown.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/paper_tile.png` | `art-delivery/resources/ui/paper-tile.png`、`art-delivery/resources/ui/slot-disabled.png`、`art-delivery/resources/ui/slot-locked.png`、`art-delivery/resources/ui/slot-normal.png`、`art-delivery/resources/ui/slot-pressed.png`、`art-delivery/resources/ui/slot-selected.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/portrait_frame.png` | `art-delivery/resources/ui/slot-disabled.png`、`art-delivery/resources/ui/slot-locked.png`、`art-delivery/resources/ui/slot-normal.png`、`art-delivery/resources/ui/slot-pressed.png`、`art-delivery/resources/ui/slot-selected.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/slider_fill.png` | `art-delivery/resources/ui/progress-fill.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/slider_thumb.png` | `art-delivery/resources/ui/scrollbar-thumb.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/slider_track.png` | `art-delivery/resources/ui/progress-track.png`、`art-delivery/resources/ui/scrollbar-track.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/stat_field.png` | `art-delivery/resources/ui/stat-field.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/step_minus.png` | `art-delivery/resources/ui/step-minus.png` |
| `designs/attribute-panels/v2-painted/unity-slices/png/step_plus.png` | `art-delivery/resources/ui/step-plus.png` |

- 固定符号与干净纸面分离；五态次按钮、滚动条旋转派生和物品槽九宫格组合保持来源。未复制原人物/宝宝等级、相性或旧业务状态；本次 Unity 导入参数仅为建议，不借用原项目 Unity 报告宣称新包验证通过。

### 来源：`designs/team-ui-v2/unity-slices`

原关联 README：`F:\work\image\designs\team-ui-v2\unity-slices\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/team-ui-v2/unity-slices/png/close.png` | `art-delivery/resources/ui/close.png` |

- 本阶段本目录只直接使用 `png/close.png`。`title_plate.png`、`section_plate.png` 已因原文字/天空/抹字污染被拒用于正式新美术包；现行 title/section 来自本项目新生成干净原画。原组队人数、申请状态和玩家示例数据未移入。

### 来源：`designs/team-ui-v2`

原关联 README：`F:\work\image\designs\team-ui-v2\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**风格参考**。已实际查看 `designs/team-ui-v2/team-ui-v2.png`，并以真实图片输入传入内置 `image_gen`；参考副本为新项目 `docs/reference-images/team-style.png`，SHA-256 为 `5fab5229de7030ac48172cfa39bb45f612a545cee0dba6303ae6f2dcfdf38750`。
- 本次实际风格输入对应的新原画包括 `art-delivery/resources/backgrounds/expedition-playfield.png`、`backgrounds/regional-map.png`、`characters/hero-survivor.png`、`icons/survival-icons-master.png` 和 `ui/clean-header-master.png`（后四项同属 `art-delivery/resources/`）。每张新原画的同名 `.generation.json` 分别保存该次实际输入、配置目标与未确认的实际型号/质量；并非只写了参考文件名。
- 新无字玉绿标题原画 `art-delivery/resources/ui/clean-header-master.png` 是本项目新生成结果，随后按真实 Alpha 轮廓等比派生 `ui/title.png`、`ui/section.png`；它不是原组队扁平标题/分栏切片的直接复用。旧污染切片已被新派生图替换，拒用原因与旧来源文字记录见新项目 `art-delivery/records/header-repair-history.json`，未保留污染图片回退副本。

### 来源：`designs/equipment-ui-20261009`

原关联 README：`F:\work\image\designs\equipment-ui-20261009\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/equipment-ui-20261009/sprites/tooltip_panel.png` | `art-delivery/resources/ui/panel-tooltip.png` |

### 来源：`designs/equipment-ui-20261008`

原关联 README：`F:\work\image\designs\equipment-ui-20261008\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用与派生使用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/equipment-ui-20261008/sprites/checkbox_off.png` | `art-delivery/resources/ui/checkbox-disabled.png`、`art-delivery/resources/ui/checkbox-normal.png` |
| `designs/equipment-ui-20261008/sprites/checkbox_on.png` | `art-delivery/resources/ui/checkbox-selected.png` |
| `designs/equipment-ui-20261008/sprites/icon_boots.png` | `art-delivery/resources/icons/icon-boots.png` |
| `designs/equipment-ui-20261008/sprites/icon_sword.png` | `art-delivery/resources/icons/icon-blade.png` |

### 来源：`designs/mail-ui-v1`

原关联 README：`F:\work\image\designs\mail-ui-v1\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**风格参考**。已实际查看 `designs/mail-ui-v1/01-mail-event.png`，并以真实图片输入传入内置 `image_gen`；参考副本为新项目 `docs/reference-images/mail-style.png`，SHA-256 为 `3cf0b7d7b3bae337d51e947719588419a01ae21bdce9bccedd6258ce1feef0a2`。
- 本次实际风格输入对应的新原画包括 `art-delivery/resources/backgrounds/expedition-playfield.png`、`backgrounds/regional-map.png`、`characters/hero-survivor.png`、`icons/survival-icons-master.png` 和 `ui/clean-header-master.png`（后四项同属 `art-delivery/resources/`）。每张新原画的同名 `.generation.json` 分别保存该次实际输入、配置目标与未确认的实际型号/质量；并非只写了参考文件名。
- 新无字玉绿标题原画 `art-delivery/resources/ui/clean-header-master.png` 是本项目新生成结果，随后按真实 Alpha 轮廓等比派生 `ui/title.png`、`ui/section.png`；它不是原组队扁平标题/分栏切片的直接复用。旧污染切片已被新派生图替换，拒用原因与旧来源文字记录见新项目 `art-delivery/records/header-repair-history.json`，未保留污染图片回退副本。
- 关联类型：**直接复用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/mail-ui-v1/assets/icon-chest.png` | `art-delivery/resources/icons/icon-cache-building.png` |
| `designs/mail-ui-v1/assets/icon-pill.png` | `art-delivery/resources/icons/icon-medication.png` |
| `designs/mail-ui-v1/assets/icon-scroll.png` | `art-delivery/resources/icons/icon-notes.png` |
| `designs/mail-ui-v1/assets/icon-talisman.png` | `art-delivery/resources/icons/icon-talisman-optional.png` |
| `designs/mail-ui-v1/assets/lantern.png` | `art-delivery/resources/ui/lantern.png` |

- 原 `assets/icon-chest.png` 实物为阁楼/建筑徽标，按实际外观导出 `icon-cache-building`，不冒充物理箱子；药葫芦图标仅为主题类别标。原邮件业务、活动、数值和奖励未作为参考游戏业务移入。

### 来源：`designs/main-hud-20261021`

原关联 README：`F:\work\image\designs\main-hud-20261021\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/main-hud-20261021/sprites/bag.png` | `art-delivery/resources/icons/icon-bag.png` |
| `designs/main-hud-20261021/sprites/channel.png` | `art-delivery/resources/icons/icon-chat.png` |
| `designs/main-hud-20261021/sprites/pet.png` | `art-delivery/resources/icons/icon-companion.png` |
| `designs/main-hud-20261021/sprites/rank.png` | `art-delivery/resources/icons/icon-achievement.png` |
| `designs/main-hud-20261021/sprites/social.png` | `art-delivery/resources/icons/icon-dialogue.png` |
| `designs/main-hud-20261021/sprites/spectate.png` | `art-delivery/resources/icons/icon-observe.png` |
| `designs/main-hud-20261021/sprites/team.png` | `art-delivery/resources/icons/icon-party-command.png` |
| `designs/main-hud-20261021/sprites/trade.png` | `art-delivery/resources/icons/icon-trade.png` |

- 徽标只作为背包、观察、NPC 交互、物资交换等美术类别示意，不据 `pet`、`team`、`rank` 等旧文件名叠加 MMO 宠物养成、多人组队或排行榜系统。源图实际生成和切片证据以本目录 `sprite-manifest.json` 及 Sprite 同名记录为准。

### 来源：`designs/class-skills-20260928`

原关联 README：`F:\work\image\designs\class-skills-20260928\README.md`。下列源路径相对 F 盘参考仓库，目标路径相对本项目根。

- 关联类型：**直接复用与派生使用**。下表源路径相对 F 盘美术仓库根；目标路径相对本对话制作目录。字节复制与裁切、缩放、调色/固定符号合成分别记录，均未冒称为新模型生成。

| 参考仓库内实际素材路径 | 新项目实际资源路径 |
|---|---|
| `designs/class-skills-20260928/icons/1101.png` | `art-delivery/resources/icons/art-martial-1101.png` |
| `designs/class-skills-20260928/icons/1103.png` | `art-delivery/resources/icons/art-martial-1103.png` |
| `designs/class-skills-20260928/icons/1106.png` | `art-delivery/resources/icons/art-martial-1106.png` |
| `designs/class-skills-20260928/icons/1107.png` | `art-delivery/resources/icons/art-martial-1107.png` |
| `designs/class-skills-20260928/icons/1301.png` | `art-delivery/resources/icons/art-martial-1301.png` |
| `designs/class-skills-20260928/icons/1303.png` | `art-delivery/resources/icons/art-martial-1303.png` |

- 采用 1101、1103、1106、1107、1301、1303 六张现存技能卡作为主题/可选系统美术示意，原职业技能名、伤害、相性和规则未成为参考游戏功能依据。每张从原生 1254 方图缩小导出 256 方图，不声称新生成或新增原生细节。现存最新采用说明为 `icons-style-20261021/README.md`；此前根 README 不存在，本文件仅为本次必要来源关联新建，不恢复旧文档。

<!-- /local-association: qinglan-cataclysm-ui-art-20261026 -->
