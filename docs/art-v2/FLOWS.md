# 全游戏 UI 流程关系

制作名：**青岚余生（暂定名）**。功能参考固定为 Cataclysm-DDA 提交 `eb86dffd20072d6fde54af568cf229f3cd4d751f`。流程图用于表达 UI 美术关系，不代表 Unity、C#、Prefab、业务接口或运行联调已经完成。

总览：[PNG](../../art-delivery/previews/flow-overview.png) · [可编辑 SVG](../../art-delivery/previews/flow-overview.svg)。每张 1920×1080，正文至少 22px；字体与 OFL 许可随资源包交付。PNG 是既有纸面纹理、原生文字与矢量框线的确定性组合，没有调用新的生成模型。

玉绿节点表示流程入口或返回点，米白节点表示列表、详情、条件、确认或反馈。并不是每个只读信息页都存在“领取”或“成交”；具体确认语义以各条源码流程为准。

## 01 · 启程、世界与人物创建

[PNG](../../art-delivery/previews/flow-01.png) · [可编辑 SVG](../../art-delivery/previews/flow-01.svg)

- **创建世界**：首页世界入口 → 世界列表 → 模组与规则 → 名称确认 → 创建世界 → 人物创建。
- **自定义人物 · 七步**：开局情景 → 职业 → 人生背景 → 初始属性 → 天赋特征 → 初始技能 → 身份总览。
- **出发与读取**：新建 / 读取 → 人物列表 → 身份与存档 → 出发确认 → 加载步骤 → 生存主界面。

人物总览内可调整开局日期与起点；不是游戏中任意传送。

覆盖的实际功能：

- `main-menu` **启程首页**：首页 → 新游戏或读取世界 → 创建或读取人物 → 进入游戏。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L430)
- `motd` **今日告示**：首页 → 今日告示 → 滚动阅读 → 返回首页。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L434)
- `credits` **制作与致谢**：首页 → 制作名单 → 阅读来源与署名 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L444)
- `world-list` **世界管理**：首页 → 世界列表 → 选中世界 → 查看模组或复制规则或管理 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L1169)
- `world-create` **创建世界**：世界列表 → 新建世界 → 名称与规则 → 完成确认 → 进入人物创建。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/worldfactory.cpp#L1501)
- `world-mods` **世界模组**：创建世界 → 可用模组 → 启用与排序 → 检查依赖冲突 → 返回规则。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/worldfactory.cpp#L985)
- `world-options` **世界规则**：创建或复制世界 → 调整规则 → 查看选项解释 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/worldfactory.cpp#L746)
- `load-character` **选择幸存者**：读取游戏 → 选择世界 → 选择人物存档 → 确认读取 → 进入游戏。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L1122)
- `creation-mode` **创建方式**：首页新游戏 → 自定义或模板或随机 → 预览 → 创建人物。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L476)
- `creation-scenario` **开局情景**：人物创建 → 情景 → 查看故事与要求 → 选择 → 职业。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2793)
- `creation-profession` **职业**：情景 → 可选职业 → 查看初始装备技能特征 → 选择 → 背景。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L1465)
- `creation-background` **人生背景**：职业 → 背景列表 → 查看技能特征 → 选择背景 → 属性。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L1736)
- `creation-stats` **初始属性**：背景 → 力量敏捷智力感知 → 调整与查看影响 → 特征。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2812)
- `creation-traits` **天赋特征**：属性 → 特征分类与搜索 → 查看利弊冲突 → 选择 → 技能。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2818)
- `creation-skills` **初始技能**：特征 → 选择技能 → 查看等级描述 → 调整 → 总览。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2824)
- `creation-summary` **身份与出发**：人物创建各页 → 总览 → 名称外观起点与日期 → 最终确认 → 进入世界。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L1973)
- `character-templates` **人物模板**：新游戏 → 预设人物 → 模板列表 → 预览 → 总览调整 → 出发。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L568)
- `loading` **加载与生存提示**：新游戏或读取 → 当前加载上下文与步骤 → 完成 → 进入游戏。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/loading_ui.cpp#L258)

条件与异常：情景、职业的解锁条件与特征冲突必须说明原因。；无世界 / 无人物 / 无模板 / 非法名称 / 读取失败各自有返回出口。

## 02 · 物品、容器与周边转移

[PNG](../../art-delivery/previews/flow-02.png) · [可编辑 SVG](../../art-delivery/previews/flow-02.svg)

- **物品操作**：随身行囊 → 分类与搜索 → 物品详情 → 操作确认 → 消耗与反馈 → 返回行囊。
- **容器与口袋**：背包或容器 → 口袋列表 → 容量与规则 → 选择去向 → 移动结果 → 返回容器。
- **周边转移**：高级物品管理 → 左右来源 → 多选物品 → 数量确认 → 耗时转移 → 刷新来源。

仓储来源是邻近地面、角色容器或载具货物，不新增远程公共仓库。

覆盖的实际功能：

- `inventory` **随身行囊**：主界面行囊 → 分类搜索排序 → 选中物品 → 详情或操作 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L264)
- `item-detail` **物品详情**：物品列表 → 详情 → 查看描述与数值 → 可用操作 → 返回列表。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ui_iteminfo.cpp#L47)
- `item-compare` **物品比较**：物品列表 → 比较 → 选择两件物品 → 差异对照 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2746)
- `item-containers` **容器与口袋**：物品详情 → 容器口袋 → 选择口袋 → 移动物品或调整规则 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/item_contents.cpp#L2982)
- `advanced-inventory` **周边与仓储转移**：主界面高级物品管理 → 选择左右来源 → 筛选或排序 → 单件或批量转移 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/advanced_inv.cpp#L271)
- `worn-layers` **穿戴与衣层**：人物装备 → 穿戴列表 → 选择部位与衣层 → 重排或脱下 → 查看阻碍 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/armor_layers.cpp#L594)
- `wield` **选择手持物**：主界面持用 → 选择物品 → 查看持用要求 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2054)
- `pickup` **拾取物品**：地面互动 → 拾取列表 → 勾选物品及数量 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2558)
- `multidrop` **丢弃与数量**：行囊 → 多选丢弃 → 输入数量 → 确认落点与操作 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2512)
- `consume` **饮食与药品**：主界面食用 → 食物饮水药品 → 查看营养与风险 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1076)
- `read` **阅读与学习**：主界面阅读 → 选择书籍或电子书 → 查看知识门槛与时间 → 开始阅读 → 进度或中断。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1631)
- `reload` **装填与弹药**：手持武器或工具 → 装填 → 选择弹药与目标 → 数量 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L3288)
- `item-unload` **卸下内容物**：物品操作 → 卸载 → 选择容器或弹仓 → 选择目标 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L3139)
- `liquid-transfer` **液体与容器**：液体交互 → 选择目的容器 → 查看容量与兼容性 → 确认灌装 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L546)
- `item-use` **物品操作**：物品详情或操作入口 → 使用功能列表 → 查看消耗要求 → 选择 → 结果反馈。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/item_action.cpp#L272)
- `electronic-files` **电子设备与资料**：电子设备使用 → 选择设备与资料 → 阅读复制或移动 → 选择目标 → 完成反馈。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1885)

条件与异常：饮食、阅读、装填、卸载、液体、电子资料共享选择 / 详情 / 结果结构。；容量不足、重量过高、弹药不兼容、容器不防水等限制不混成同一错误。

## 03 · 人物成长、制作与维护

[PNG](../../art-delivery/previews/flow-03.png) · [可编辑 SVG](../../art-delivery/previews/flow-03.svg)

- **制作与拆解**：制作入口 → 配方与目标 → 材料工具条件 → 批量确认 → 活动与中断 → 结果 / 返回。
- **技能成长**：人物总览 → 技能与技艺 → 理论实作详情 → 训练开关 → 成长反馈 → 返回人物。
- **维护与施工**：装备 / 建造 → 目标与部位 → 材料技能时间 → 操作确认 → 成功或失败 → 返回列表。

技能不是MMORPG通用角色等级；区域工作不扩张成独立经营游戏。

覆盖的实际功能：

- `character-sheet` **人物总览**：主界面人物 → 属性概览 → 选中属性说明 → 切换标签 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L1526)
- `character-encumbrance` **负重与部位阻碍**：人物总览 → 阻碍与速度 → 选中部位 → 查看穿戴影响 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L289)
- `character-skills` **技能成长**：人物总览 → 技能 → 选择技能 → 理论与实作进度 → 切换训练状态 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L790)
- `character-proficiencies` **熟练技艺**：人物总览 → 熟练技艺 → 选择技艺 → 查看学习与制作影响 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L318)
- `repair` **修理与材料**：修理工具使用 → 选择损坏物品 → 查看材料工具条件 → 修理方式 → 结果。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2395)
- `gunmods` **枪械配件**：配件使用或枪械操作 → 选择武器或配件 → 查看槽位与条件 → 确认安装或拆下 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1309)
- `craft-recipes` **制作配方**：主界面制作 → 分类搜索 → 选择配方 → 材料工具熟练要求 → 制作或批量 → 活动进度。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/crafting_gui.cpp#L859)
- `craft-batch` **批量制作**：制作配方 → 批量 → 调整数量 → 重新计算时间与需求 → 确认 → 制作活动。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/crafting_gui.cpp#L764)
- `disassemble` **拆解回收**：主界面拆解 → 选择可拆物 → 查看产出工具耗时 → 确认 → 活动进度与结果。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L634)
- `construction` **建造计划**：建造 → 分类可建筛选 → 阶段详情 → 材料工具技能 → 位置。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/construction.cpp#L522)
- `construction-place` **施工位置预览**：选方案 → 附近合法格预览 → 位置 → 确认 → 进度。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/construction.cpp#L465)
- `activity-progress` **长时活动与中断**：阅读制作修车休息等 → 进度 → 危险/取消 → 中断继续 → 完成。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_activity.cpp#L134)
- `butcher-harvest` **处理遗骸与收获**：选目标 → 处理方式 → 工具时间 → 确认 → 进度产物。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/butchery.cpp#L1184)
- `zone-activities` **区域工作与批量活动**：定义区域 → 工作入口 → 分类/农耕/采伐/修车/施工 → 条件 → 活动。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/handle_action.cpp#L1496)

条件与异常：收藏材料、替代材料、缺工具、知识不足、位置非法各自提示。；阅读、屠宰、农耕与区域批量工作接入同一长时活动 / 中断视觉合同。

## 04 · 生存回合、战斗与伤势

[PNG](../../art-delivery/previews/flow-04.png) · [可编辑 SVG](../../art-delivery/previews/flow-04.svg)

- **回合行动**：生存主界面 → 选择行动 → 目标与轨迹 → 行动确认 → 回合结果 → 返回主界面。
- **伤势处理**：身体状态 → 受伤部位 → 治疗与风险 → 消耗确认 → 处理结果 → 返回状态。
- **休息与终局**：等待 / 睡眠 → 时间与闹钟 → 风险或中断 → 继续 / 结束 → 状态 / 纪念 → 主界面 / 首页。

自动时间推进与回合耗时按实际规则表达，不套动作闯关技能轮盘。

覆盖的实际功能：

- `game-hud` **生存主界面**：进入世界 → 观察生命/体力/需求/环境 → 选择行动 → 回合推进。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/data/json/ui/sidebar.json#L3)
- `aim-ranged` **瞄准与射击**：远程武器 → 选目标 → 选瞄准精度/射击模式 → 确认射击 → 主界面。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ranged.cpp#L2847)
- `throw-target` **投掷目标**：选投掷物 → 选生物/地面 → 看距离轨迹 → 确认或取消。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ranged.cpp#L504)
- `look-examine` **观察与环境详情**：观察 → 移动光标 → 读取地形/生物/物品 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game.cpp#L5977)
- `nearby-creatures` **附近物品与目标**：附近列表 → 物品/生物/地形家具 → 筛选 → 详情 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/surroundings_menu.cpp#L73)
- `message-log` **消息日志**：日志 → 历史消息 → 滚动查看 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/messages.cpp#L924)
- `body-health` **身体状态总览**：身体状态 → 选择部位 → 子部位/伤势/穿戴 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/body_status_ui.cpp#L200)
- `medical-treatment` **处理伤势**：医疗标签 → 受伤部位 → 可用治疗 → 确认 → 活动进度。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/body_status_ui.cpp#L601)
- `status-effects` **状态效果**：角色信息 → 效果标签 → 选择效果 → 说明 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L742)
- `morale` **士气与专注**：士气 → 正负来源 → 合计/专注影响 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/morale.cpp#L530)
- `wait-sleep` **等待、休息与闹钟**：休息 → 等待/睡眠/闹钟 → 时长自然时间 → 确认 → 推进。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/handle_action.cpp#L1237)
- `memorial` **旅程终局与纪念**：人物死亡 → 临终观察/终局 → 日记成绩 → NPC阵营后记 → 主菜单。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game.cpp#L2939)

条件与异常：弹药不足、超出范围、目标丢失与友方弹道需明确反馈。；等待和长时活动可因危险中断；人物死亡后的纪念不作为可领取奖励。

## 05 · 地图、探索、任务与终端

[PNG](../../art-delivery/previews/flow-05.png) · [可编辑 SVG](../../art-delivery/previews/flow-05.svg)

- **探索与旅行**：区域地图 → 地点与筛选 → 地点路线详情 → 旅行确认 → 到达或中断 → 返回地图。
- **任务闭环**：任务入口 → 任务列表 → 目标与条件 → 交付对话 → 完成或失败 → 任务 / 地图。
- **终端与装置**：接近并交互 → 可用操作 → 权限与风险 → 操作确认 → 成功或警报 → 返回观察。

传送只适用于已发现并激活的对应装置；缺目的地时提供空态。

覆盖的实际功能：

- `overmap` **区域地图**：大地图 → 平移缩放楼层 → 选地点 → 地点任务详情。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L194)
- `map-notes` **地图标记与搜索**：地图 → 搜索/标记列表 → 新增编辑 → 保存/删除确认 → 地图。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L279)
- `route-travel` **路线与自动旅行**：选目的地 → 规划 → 步行/驾驶确认 → 自动行进 → 到达/中断。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L2000)
- `zone-manager` **区域管理**：区域 → 地图选区 → 类型/启停 → 排序 → 保存。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/zone_manager_ui.cpp#L159)
- `missions` **任务与兴趣点**：任务 → 进行中/完成/失败/兴趣点 → 详情 → 设目标/地图定位。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/mission_ui.cpp#L378)
- `creature-codex` **生物见闻**：生物见闻 → 已记录生物 → 危险/体型/物种/感官/说明。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L847)
- `diary` **生存日记**：日记 → 页面列表 → 变化正文 → 编辑页 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/diary_ui.cpp#L175)
- `terminal` **电子终端**：交互终端 → 权限 → 绕过安全确认 → 功能 → 结果/警报。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/computer_session.cpp#L153)
- `translocator` **已激活传送装置**：发现装置 → 激活/停用 → 高级装置传送 → 已知目的地。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/iexamine.cpp#L799)

条件与异常：任务追踪、地图标记、兴趣点、日记与生物见闻保持各自列表和详情。；旅行是路径规划后的行进，不增加无条件快速传送。

## 06 · NPC、交易、营地与载具

[PNG](../../art-delivery/previews/flow-06.png) · [可编辑 SVG](../../art-delivery/previews/flow-06.svg)

- **人物交谈**：接近 / 联系 → 对话与命令 → 要求与信息 → 选择回应 → 关系任务变化 → 返回世界。
- **交易与交换**：交易入口 → 双方物品 → 数量与价值 → 成交确认 → 余额库存变化 → 返回对话。
- **营地派遣**：营地负责人 → 任务与工人 → 技能资源时间 → 派遣确认 → 工作 / 回收 → 返回营地。
- **载具维护**：检查车辆 → 结构部件 → 材料工具条件 → 安装修理确认 → 耗时与结果 → 返回载具。

营地扩建、同伴工作和载具维修为实际生存系统，不加入无依据公会或坐骑养成。

覆盖的实际功能：

- `npc-talk` **人物交谈**：接近/无线电联系NPC → 历史 → 回答/说服/交易/任务 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/dialogue_imgui.cpp#L410)
- `npc-trade` **交易与交换**：NPC交谈 → 双方物品 → 数量 → 价值余额 → 成交确认。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/trade_ui.cpp#L301)
- `factions` **阵营资料**：阵营 → 自己/其他 → 选择 → 关系描述 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L650)
- `followers` **同伴与随行状态**：同伴 → 列表 → 位置状态工作 → 命令/营地详情 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L455)
- `camp-overview` **营地总览**：联系营地负责人 → 任务 → 管理生产扩建 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L777)
- `companion-assignment` **同伴工作与派遣**：营地 → 选工作/任务 → 同伴 → 条件时间 → 派遣 → 回收。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L2096)
- `camp-upgrade` **营地扩建与生产**：营地 → 扩建方向方案 → 材料技能食物时间 → 工人 → 确认 → 施工。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L1926)
- `vehicle-dashboard` **驾驶与载具控制**：驾驶位 → 引擎速度能源电子控制 → 行驶/制动 → 停车。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/vehicle_use.cpp#L405)
- `vehicle-parts` **车辆部件与改装**：检查车辆 → 选结构部位 → 安装维修拆卸 → 工具材料 → 确认活动。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/veh_interact.cpp#L518)
- `vehicle-refill` **车辆补给**：车辆 → 选可补给部件 → 兼容燃料液体 → 确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/veh_interact.cpp#L1289)
- `atm-bank` **现金卡与银行终端**：ATM → 余额 → 购卡/存取/兑换/转卡 → 输入数额 → 结果。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/iexamine.cpp#L861)
- `vending-machine` **自动售货机**：售货机 → 商品列表详情 → 可用金额 → 购买 → 库存变化。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/iexamine.cpp#L1046)
- `npc-orders` **同伴命令与行为规则**：同伴交谈/喊话入口 → 选择一位或多位同伴 → 临时命令与行为规则 → 切换近随/交战/枪械/睡眠策略 → 确认并返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/npctalk.cpp#L884)
- `animal-care` **驯养动物与骑乘交互**：接近已友善/驯养动物 → 查看可用交互 → 改名/牵引/背包/护具/治疗/骑乘 → 选择物品或确认 → 返回世界。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/monexamine.cpp#L649)

条件与异常：钱卡终端与自动售货机按实际金额 / 库存表达；不是充值商城。；同伴命令、驯养与骑乘依赖可用对象和条件，不能混成玩家好友系统。

## 07 · 辅助、能力与可选内容

[PNG](../../art-delivery/previews/flow-07.png) · [可编辑 SVG](../../art-delivery/previews/flow-07.svg)

- **设置与规则**：设置入口 → 分类与规则 → 选项说明 → 保存或放弃 → 生效 / 重启 → 返回设置。
- **义体与特征**：能力入口 → 已知能力 → 消耗与条件 → 启停 / 手术 → 结果与状态 → 返回人物。
- **法术 · 可选**：内容已启用 → 已知法术 → 范围与消耗 → 合法目标确认 → 施展结果 → 返回主界面。

魔法能力依赖对应内容；义体手术与主动特征按条件启用，不默认全解锁。

覆盖的实际功能：

- `bionics` **义体管理**：义体 → 主动/被动 → 说明耗能燃料 → 开关 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/bionics_ui.cpp#L586)
- `bionic-surgery` **义体手术与风险**：安装者/手术台 → CBM → 麻醉无菌槽位成功率 → 确认 → 手术 → 结果。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/bionics.cpp#L2468)
- `mutations` **变异与主动特征**：变异 → 主动/被动 → 描述 → 激活停用/快捷键 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/mutation_ui.cpp#L103)
- `martial-arts` **武术与招式**：武术 → 已知流派 → 招式与兼容武器 → 选用/空手 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/character.cpp#L8442)
- `spellbook` **法术与超自然能力（可选）**：相关内容启用并掌握能力 → 列表 → 详情收藏快捷键 → 施展。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/magic.cpp#L3373)
- `spell-target` **法术目标与施展（可选）**：选能力 → 合法生物/地面/车辆目标 → 范围 → 确认 → 结果。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ranged.cpp#L586)
- `achievements` **成就、准则与战绩**：战绩 → 成就/准则/分数/击杀 → 进度记录 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/scores_ui.cpp#L36)
- `safemode-rules` **安全模式规则**：规则管理 → 全局/人物 → 编辑启停排序 → 测试 → 保存。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/safemode_ui.cpp#L56)
- `autopickup-rules` **自动拾取规则**：自动拾取 → 全局/人物 → 包含排除通配 → 测试 → 保存。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/auto_pickup.cpp#L308)
- `settings-general` **通用设置**：设置 → 通用 → 编辑选项 → 查看解释 → 保存或放弃 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L1571)
- `settings-interface` **界面与辅助**：设置 → 界面 → 语言单位与辅助 → 编辑 → 保存 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L1885)
- `settings-graphics` **画面与字体**：设置 → 画面 → 字体图块动画与小地图 → 编辑 → 预览与确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L2399)
- `settings-audio` **声音与音量**：设置 → 声音组 → 开启声音并选择音效包 → 音量 → 保存 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L1831)
- `keybindings` **按键映射**：设置或当前界面帮助 → 按键映射 → 搜索动作 → 添加删除或重置 → 冲突确认 → 返回。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/input_context.cpp#L1000)
- `help` **帮助与引导**：主菜单或游戏中帮助 → 主题分类 → 阅读条目 → 翻页 → 返回分类。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/help.cpp#L166)
- `colors-theme` **颜色与主题**：设置 → 颜色管理或ImGui样式 → 选择颜色与预设 → 预览 → 保存或还原。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/color.cpp#L836)
- `tutorial` **生存教学**：主菜单教学 → 教学世界 → 按区域触发说明 → 完成操作 → 下一提示。 [源码依据](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/data/mods/dda_tutorial/traps.json#L19)

条件与异常：成就、准则、分数与击杀是记录；不机械添加签到、抽卡或奖励领取。；帮助、教学与按键映射有返回路径；规则设置的冲突和非法输入必须解释。

## 共用状态与验收边界

- 通用确认、数量、错误、空态、锁定与结果皮肤在 `common-dialogs` 引用。它们用于统一美术，不取代弹药不兼容、口袋容量不足、材料不足、未解锁、无目的地等具体说明。
- 法术等可选内容仅在对应内容启用且人物已掌握时显示；传送必须有实际装置及目的地；职业/情景解锁遵守源条件。
- 无依据的网络账号、MMORPG区服、充值、世界聊天、邮件、签到、抽卡和远程公共仓库没有机械加入。
- 流程图覆盖100个研究到的玩家界面族。图中所有人物名和数值均属样例，功能研究不证明图像视觉验收通过；独立美术验收与下一阶段Unity验证须分别记录。
- 完整结构、各功能状态、固定源码引用及图像哈希见 [`flow-manifest.json`](../../art-delivery/records/flow-manifest.json)。
