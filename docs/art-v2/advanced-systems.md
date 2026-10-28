# 高级与类型专属系统研究

核实：2026-10-26。功能参考：Cataclysm: Dark Days Ahead，固定提交 eb86dffd20072d6fde54af568cf229f3cd4d751f；实际克隆目录 reference/Cataclysm-DDA。美术任务暂名“青岚余生（暂定名）”。

本文件覆盖 49 个高级／类型专属 UI 场景和 9 项范围排除，供总清单合并。主菜单、人物创建、基础属性、背包、物品、制作拆解与基础设置由核心研究分工另行记录。本研究不是整套图片制作完成或 Unity 接入完成的声明。

## 研究方式与边界

已实际读取克隆中的主地图路线、远程目标事件循环、身体部位与医疗回调、交易确认、任务标签和详情、阵营与同伴、营地工作与扩建、载具部件和控制、义体开关与手术条件、变异、武术、法术选择、战绩、日记、电子终端、ATM／售货机、区域、安全与拾取规则等实现与相关 JSON。每条记录附固定提交下的文件、符号和行号。

基础玩法是时间推进的生存探索，并非 MMORPG。道家 Q 版应改变皮肤、图标、角色绘制和层级，不应把饥渴、伤势、kJ 义体能量、载具燃料、NPC 信用等逻辑改成网游等级门槛、元宝、离线收益或统一领奖。

地图示意、载具部件图和身体示意属于美术设计，不代表真实世界坐标、碰撞、导航或 Unity 模型已完成。所有演示人物名、地名、数字与对白须标注“样例”。

## 需要保留的特殊关系

- 区域地图主要做步行／驾驶路线；特定世界传送装置另有条件入口。不得将两者合并为任意点付费传送。
- 任务日志有进行中、已完成、已失败和兴趣点；任务交付和奖励应接 NPC 或具体任务条件，不统一添加“领取附件”。
- 阵营、同伴和营地是世界内 NPC 关系与工作；不是玩家帮会、五人匹配组队或世界聊天。
- 阵营 UI 的生物标签是目击／拍照见闻图鉴，不是宠物抽取。
- 成就、行为准则、分数和击杀记录是本地战绩；部分调试人物不能获取成就，没有证据支持全服排行榜和日签礼包。
- 完整仙术设计作为 Magiclysm 等配置的可选扩展。底层 spell 引擎亦用于部分基础义体和特殊能力，因此不声称“全部 spell 代码只存在于 mod”；也不把法术栏视为所有基础人物固有界面。
- 世界内电子终端的“登录”是设备安全认证，不是游戏账号登录。ATM 与售货机是世界内现金卡／银行交互，不是现实充值。

## 生存与战斗

### game-hud · 生存主界面

入口与返回：进入世界 → 观察生命/体力/需求/环境 → 选择行动 → 回合推进。

适用状态：常态、受伤、饥渴、疲劳、负重、警戒、乘车、活动中。

布局模式：hud；内容可用性：base。

按源sidebar信息组重排；场景和数值是设计样例。

依据：[data/json/ui/sidebar.json:3](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/data/json/ui/sidebar.json#L3)。

### aim-ranged · 瞄准与射击

入口与返回：远程武器 → 选目标 → 选瞄准精度/射击模式 → 确认射击 → 主界面。

适用状态：瞄准中、无弹药、超范围、目标丢失、友方弹道确认、取消。

布局模式：targeting；内容可用性：base。

显示命中Great/Normal/Graze概率层级；不加入无依据技能轮盘。

依据：[src/ranged.cpp:2847](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ranged.cpp#L2847)。

### throw-target · 投掷目标

入口与返回：选投掷物 → 选生物/地面 → 看距离轨迹 → 确认或取消。

适用状态：物品选中、合法轨迹、超范围、盲投、取消。

布局模式：targeting；内容可用性：base。

与射击共用目标框与轨迹资源。

依据：[src/ranged.cpp:504](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ranged.cpp#L504)。

## 探索

### look-examine · 观察与环境详情

入口与返回：观察 → 移动光标 → 读取地形/生物/物品 → 返回。

适用状态：可见、视线受阻、黑暗、无物、切换楼层。

布局模式：detail；内容可用性：base。

美术地图为功能示意，不等于游戏真实世界或Unity导航。

依据：[src/game.cpp:5977](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game.cpp#L5977)。

### nearby-creatures · 附近物品与目标

入口与返回：附近列表 → 物品/生物/地形家具 → 筛选 → 详情 → 返回。

适用状态：有目标、无目标、无搜索结果、选中、危险。

布局模式：list-detail；内容可用性：base。

源菜单实际三类对象；不是敌人掉落领取界面。

依据：[src/surroundings_menu.cpp:73](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/surroundings_menu.cpp#L73)。

## 记录

### message-log · 消息日志

入口与返回：日志 → 历史消息 → 滚动查看 → 返回。

适用状态：有记录、无记录、长文、错误提示。

布局模式：list；内容可用性：base。

游戏事件日志，不是玩家聊天频道。

依据：[src/messages.cpp:924](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/messages.cpp#L924)。

## 身体与状态

### body-health · 身体状态总览

入口与返回：身体状态 → 选择部位 → 子部位/伤势/穿戴 → 返回。

适用状态：完整、受伤、部位缺失、选中、治疗后。

布局模式：body；内容可用性：base。

保留身体/子身体部位结构，不以全局血条替代。

依据：[src/body_status_ui.cpp:200](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/body_status_ui.cpp#L200)；[src/body_status_ui.h:28](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/body_status_ui.h#L28)。

### medical-treatment · 处理伤势

入口与返回：医疗标签 → 受伤部位 → 可用治疗 → 确认 → 活动进度。

适用状态：待处理、无伤势、无药物工具、选中治疗、完成、中断。

布局模式：body-detail；内容可用性：base。

实际调用pick_wound_fix；不设计通用一键满血。

依据：[src/body_status_ui.cpp:601](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/body_status_ui.cpp#L601)；[src/medical_ui.cpp:496](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/medical_ui.cpp#L496)。

### status-effects · 状态效果

入口与返回：角色信息 → 效果标签 → 选择效果 → 说明 → 返回。

适用状态：正面、负面、无效果、长说明。

布局模式：list-detail；内容可用性：base。

强度持续时间仅样例；环境伤害药物等来源保留。

依据：[src/player_display.cpp:742](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L742)。

### morale · 士气与专注

入口与返回：士气 → 正负来源 → 合计/专注影响 → 返回。

适用状态：正士气、负士气、无来源、惩罚叠加。

布局模式：list-detail；内容可用性：base。

不是社交好感度或运营活跃度。

依据：[src/morale.cpp:530](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/morale.cpp#L530)。

## 地图与旅行

### overmap · 区域地图

入口与返回：大地图 → 平移缩放楼层 → 选地点 → 地点任务详情。

适用状态：探索过、未知、地点选中、天气图层、任务目标、楼层。

布局模式：map；内容可用性：base。

地名与坐标样例，图层和文字分离。

依据：[src/overmap_ui.cpp:194](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L194)。

### map-notes · 地图标记与搜索

入口与返回：地图 → 搜索/标记列表 → 新增编辑 → 保存/删除确认 → 地图。

适用状态：有标记、无标记、无结果、编辑、删除确认。

布局模式：map-detail；内容可用性：base。

标记图标和原生文字独立，不能烘焙所有地点。

依据：[src/overmap_ui.cpp:279](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L279)。

### route-travel · 路线与自动旅行

入口与返回：选目的地 → 规划 → 步行/驾驶确认 → 自动行进 → 到达/中断。

适用状态：可达、无路径、楼层不一致、负重警告、车内非驾驶、行进、取消。

布局模式：map-confirm；内容可用性：base。

不是任意点付费传送，保留同Z层和驾驶状态限制。

依据：[src/overmap_ui.cpp:2000](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L2000)。

## 营地与区域

### zone-manager · 区域管理

入口与返回：区域 → 地图选区 → 类型/启停 → 排序 → 保存。

适用状态：选中、无区域、启用、禁用、个人区域、车辆区域。

布局模式：map-list；内容可用性：base。

分类存放、农田、施工、车辆工作区域；不是PvP领土。

依据：[src/zone_manager_ui.cpp:159](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/zone_manager_ui.cpp#L159)。

## 人物与关系

### npc-talk · 人物交谈

入口与返回：接近/无线电联系NPC → 历史 → 回答/说服/交易/任务 → 返回。

适用状态：常态、多段历史、不可选、说服成功、说服失败、结束。

布局模式：dialogue；内容可用性：base。

人物名与对白样例；头像和原生文字分离。

依据：[src/dialogue_imgui.cpp:410](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/dialogue_imgui.cpp#L410)。

### npc-trade · 交易与交换

入口与返回：NPC交谈 → 双方物品 → 数量 → 价值余额 → 成交确认。

适用状态：可成交、拒收、价值不足、容量不足、信用上限、确认、取消。

布局模式：dual-inventory；内容可用性：base。

真实以物易物/信用/部分银行余额，不是元宝商城。

依据：[src/trade_ui.cpp:301](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/trade_ui.cpp#L301)。

## 任务

### missions · 任务与兴趣点

入口与返回：任务 → 进行中/完成/失败/兴趣点 → 详情 → 设目标/地图定位。

适用状态：进行中、已完成、已失败、无任务、限时、目标选中。

布局模式：list-detail；内容可用性：base。

奖励交付按NPC或任务脚本，不添加全任务一键领奖。

依据：[src/mission_ui.cpp:378](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/mission_ui.cpp#L378)；[src/mission_ui.cpp:39](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/mission_ui.cpp#L39)。

## 人物与关系

### factions · 阵营资料

入口与返回：阵营 → 自己/其他 → 选择 → 关系描述 → 返回。

适用状态：已知、无记录、友好、敌对、中立。

布局模式：list-detail；内容可用性：base。

世界内阵营，不是玩家公会。

依据：[src/faction_ui.cpp:650](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L650)。

### followers · 同伴与随行状态

入口与返回：同伴 → 列表 → 位置状态工作 → 命令/营地详情 → 返回。

适用状态：随行、驻营、工作中、未响应、无同伴、受伤。

布局模式：list-detail；内容可用性：base。

NPC关系，不包含网络组队/副本匹配。

依据：[src/faction_ui.cpp:455](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L455)。

### creature-codex · 生物见闻

入口与返回：生物见闻 → 已记录生物 → 危险/体型/物种/感官/说明。

适用状态：已记录、无目击照片、高危、长文。

布局模式：list-detail；内容可用性：base。

依据目击拍照记录，非宠物抽取养成。

依据：[src/faction_ui.cpp:847](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L847)。

## 营地与区域

### camp-overview · 营地总览

入口与返回：联系营地负责人 → 任务 → 管理生产扩建 → 确认 → 返回。

适用状态：可管理、无权限、无人、食物不足、任务可用、任务中。

布局模式：management；内容可用性：base。

食物热量、工人和设施；不伪造放置离线收益。

依据：[src/faction_camp.cpp:777](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L777)。

### companion-assignment · 同伴工作与派遣

入口与返回：营地 → 选工作/任务 → 同伴 → 条件时间 → 派遣 → 回收。

适用状态：无人、可指派、技能不符、工作中、未到时间、可回收、召回。

布局模式：roster；内容可用性：base。

实际任务时间危险成果以定义为准，画面均样例。

依据：[src/faction_camp.cpp:2096](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L2096)。

### camp-upgrade · 营地扩建与生产

入口与返回：营地 → 扩建方向方案 → 材料技能食物时间 → 工人 → 确认 → 施工。

适用状态：可建、缺材料、缺食物、前置不足、施工、完工、撤销。

布局模式：requirements；内容可用性：base。

农耕采伐采集共用任务详情，不画无依据科技树。

依据：[src/faction_camp.cpp:1926](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L1926)。

## 载具

### vehicle-dashboard · 驾驶与载具控制

入口与返回：驾驶位 → 引擎速度能源电子控制 → 行驶/制动 → 停车。

适用状态：关闭、启动、无燃料、移动、停车、自动驾驶、故障。

布局模式：hud；内容可用性：base。

保留速度燃料电池现实单位，不改坐骑战力。

依据：[src/vehicle_use.cpp:405](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/vehicle_use.cpp#L405)；[src/vehicle_use.cpp:310](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/vehicle_use.cpp#L310)；[src/smart_controller_ui.cpp:41](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/smart_controller_ui.cpp#L41)。

### vehicle-parts · 车辆部件与改装

入口与返回：检查车辆 → 选结构部位 → 安装维修拆卸 → 工具材料 → 确认活动。

适用状态：正常、损坏、不可修、材料技能不足、驾驶中禁止、部件选中、完成。

布局模式：vehicle-plan；内容可用性：base。

结构配置示意，非Unity车辆模型完成。

依据：[src/veh_interact.cpp:518](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/veh_interact.cpp#L518)。

### vehicle-refill · 车辆补给

入口与返回：车辆 → 选可补给部件 → 兼容燃料液体 → 确认 → 返回。

适用状态：可补给、无兼容物、已满、移动中禁止、目标选中、完成。

布局模式：requirements；内容可用性：base。

按部件类型处理，非万能货币能源。

依据：[src/veh_interact.cpp:1289](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/veh_interact.cpp#L1289)。

## 身体与成长

### bionics · 义体管理

入口与返回：义体 → 主动/被动 → 说明耗能燃料 → 开关 → 返回。

适用状态：无义体、启动、关闭、能量不足、无燃料、节能阈值、故障。

布局模式：list-detail；内容可用性：base。

保留kJ能量语义，道家装饰不改变消耗逻辑。

依据：[src/bionics_ui.cpp:586](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/bionics_ui.cpp#L586)。

### bionic-surgery · 义体手术与风险

入口与返回：安装者/手术台 → CBM → 麻醉无菌槽位成功率 → 确认 → 手术 → 结果。

适用状态：可装、已装、槽位不足、污染、缺麻醉、确认、成功、失败。

布局模式：confirm-risk；内容可用性：base。

手术世界交互，不是拖入装备格即安装。

依据：[src/bionics.cpp:2468](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/bionics.cpp#L2468)。

### mutations · 变异与主动特征

入口与返回：变异 → 主动/被动 → 描述 → 激活停用/快捷键 → 返回。

适用状态：无变异、被动不可激活、关闭、生效、资源不足、永久特征。

布局模式：list-detail；内容可用性：base。

非标准等级天赋树，不额外设计升星突破。

依据：[src/mutation_ui.cpp:103](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/mutation_ui.cpp#L103)。

### martial-arts · 武术与招式

入口与返回：武术 → 已知流派 → 招式与兼容武器 → 选用/空手 → 返回。

适用状态：已学、未选择、当前选用、武器兼容说明、义体提供。

布局模式：list-detail；内容可用性：base。

列表来自所学或激活义体提供，不默认固定门派。

依据：[src/character.cpp:8442](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/character.cpp#L8442)。

## 可选超自然内容

### spellbook · 法术与超自然能力（可选）

入口与返回：相关内容启用并掌握能力 → 列表 → 详情收藏快捷键 → 施展。

适用状态：未启用、无能力、已学、能量不足、失败率、收藏。

布局模式：list-detail；内容可用性：mod-only。

完整仙术示例仅针对Magiclysm等配置；底层spell引擎还用于部分基础义体/特殊内容，不算所有基础人物固有能力。

依据：[src/magic.cpp:3373](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/magic.cpp#L3373)；[data/mods/Magiclysm/modinfo.json:4](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/data/mods/Magiclysm/modinfo.json#L4)。

### spell-target · 法术目标与施展（可选）

入口与返回：选能力 → 合法生物/地面/车辆目标 → 范围 → 确认 → 结果。

适用状态：可施展、无合法目标、能量不足、超范围、范围预览、取消。

布局模式：targeting；内容可用性：mod-only。

同spellbook为相关可选内容扩展，不默认基础人物都有法术栏。

依据：[src/ranged.cpp:586](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ranged.cpp#L586)。

## 记录

### achievements · 成就、准则与战绩

入口与返回：战绩 → 成就/准则/分数/击杀 → 进度记录 → 返回。

适用状态：未完成、已完成、违背准则、空记录、调试人物禁用。

布局模式：list-detail；内容可用性：base。

本地记录，无全服排行、货币领奖或每日签到。

依据：[src/scores_ui.cpp:36](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/scores_ui.cpp#L36)。

### memorial · 旅程终局与纪念

入口与返回：人物死亡 → 临终观察/终局 → 日记成绩 → NPC阵营后记 → 主菜单。

适用状态：死亡、临终观察、成绩、无击杀、后记、纪念。

布局模式：summary；内容可用性：base。

基础死亡终局，无通用付费复活；特殊防死内容例外需另标。

依据：[src/game.cpp:2939](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game.cpp#L2939)；[src/game.cpp:2859](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game.cpp#L2859)。

### diary · 生存日记

入口与返回：日记 → 页面列表 → 变化正文 → 编辑页 → 返回。

适用状态：无日记、已记录、长文、编辑、保存、取消。

布局模式：list-detail；内容可用性：base。

本地日记，不是邮件收件箱，正文样例。

依据：[src/diary_ui.cpp:175](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/diary_ui.cpp#L175)。

## 世界交互

### terminal · 电子终端

入口与返回：交互终端 → 权限 → 绕过安全确认 → 功能 → 结果/警报。

适用状态：接入、锁定、破解确认、破解失败、无权限、成功、关闭。

布局模式：terminal；内容可用性：base。

终端登录是世界内计算机认证，不是游戏账号登录。

依据：[src/computer_session.cpp:153](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/computer_session.cpp#L153)。

### atm-bank · 现金卡与银行终端

入口与返回：ATM → 余额 → 购卡/存取/兑换/转卡 → 输入数额 → 结果。

适用状态：正常、无卡、余额不足、数量输入、手续费确认、成功。

布局模式：choice-detail；内容可用性：base。

世界内现金卡银行，不是现实支付或充值。

依据：[src/iexamine.cpp:861](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/iexamine.cpp#L861)。

### vending-machine · 自动售货机

入口与返回：售货机 → 商品列表详情 → 可用金额 → 购买 → 库存变化。

适用状态：有货、售罄、无卡、余额不足、商品选中、购买结果。

布局模式：list-detail；内容可用性：base。

库存来自场景设备，价格和商品为样例。

依据：[src/iexamine.cpp:1046](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/iexamine.cpp#L1046)。

### translocator · 已激活传送装置

入口与返回：发现装置 → 激活/停用 → 高级装置传送 → 已知目的地。

适用状态：未激活、已激活、无目的地、停用确认、目的地选择。

布局模式：map-confirm；内容可用性：conditional-world-device。

特定世界装置条件入口，非任意地图点付费传送。

依据：[src/iexamine.cpp:799](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/iexamine.cpp#L799)。

## 辅助规则

### safemode-rules · 安全模式规则

入口与返回：规则管理 → 全局/人物 → 编辑启停排序 → 测试 → 保存。

适用状态：无规则、启用、禁用、距离态度类别、匹配、无匹配、未保存。

布局模式：table；内容可用性：base。

危险行动保护，不是自动战斗。

依据：[src/safemode_ui.cpp:56](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/safemode_ui.cpp#L56)。

### autopickup-rules · 自动拾取规则

入口与返回：自动拾取 → 全局/人物 → 包含排除通配 → 测试 → 保存。

适用状态：无规则、启用、禁用、包含、排除、匹配、无匹配、未保存。

布局模式：table；内容可用性：base。

顺序容器和材质规则影响结果，不是挂机收益。

依据：[src/auto_pickup.cpp:308](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/auto_pickup.cpp#L308)。

## 建造与活动

### construction · 建造计划

入口与返回：建造 → 分类可建筛选 → 阶段详情 → 材料工具技能 → 位置。

适用状态：全部、材料就绪但地点缺失、此处可建、缺材料、缺技能、太暗。

布局模式：requirements；内容可用性：base。

源码明确all/ready missing location/buildable here三种筛选。

依据：[src/construction.cpp:522](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/construction.cpp#L522)。

### construction-place · 施工位置预览

入口与返回：选方案 → 附近合法格预览 → 位置 → 确认 → 进度。

适用状态：有效、无效、占用、多阶段、确认、返回。

布局模式：map-target；内容可用性：base。

位置状态图，不宣称Unity碰撞导航实现。

依据：[src/construction.cpp:465](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/construction.cpp#L465)。

### wait-sleep · 等待、休息与闹钟

入口与返回：休息 → 等待/睡眠/闹钟 → 时长自然时间 → 确认 → 推进。

适用状态：定时、等天亮天气、恢复体力、等同伴、无表近似、驾驶禁止、取消。

布局模式：choice；内容可用性：base。

有无表影响时间选项，非离线奖励或免费恢复。

依据：[src/handle_action.cpp:1237](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/handle_action.cpp#L1237)。

### activity-progress · 长时活动与中断

入口与返回：阅读制作修车休息等 → 进度 → 危险/取消 → 中断继续 → 完成。

适用状态：进行中、可中断、危险打断、可恢复、不可恢复、完成、取消。

布局模式：progress；内容可用性：base。

真实活动信息视觉封装，不是实时挂机任务。

依据：[src/player_activity.cpp:134](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_activity.cpp#L134)。

### butcher-harvest · 处理遗骸与收获

入口与返回：选目标 → 处理方式 → 工具时间 → 确认 → 进度产物。

适用状态：无目标、缺工具、快速、完整处理、解剖、知识要求、完成失败。

布局模式：choice-detail；内容可用性：base。

中性图标和文字避免血腥，不改成战斗宝箱。

依据：[src/butchery.cpp:1184](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/butchery.cpp#L1184)。

### zone-activities · 区域工作与批量活动

入口与返回：定义区域 → 工作入口 → 分类/农耕/采伐/修车/施工 → 条件 → 活动。

适用状态：无兼容区域、就绪、缺工具、工作中、完成、中断。

布局模式：choice-detail；内容可用性：base。

保留源区域活动入口，子活动共用选择和进度资源。

依据：[src/handle_action.cpp:1496](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/handle_action.cpp#L1496)。

## 不适用或未确认的通用模板项

- **在线账号登录与区服列表**（not-applicable-to-reviewed-base-flow）：主菜单为本地新游戏、存档、世界和设置；共享地图参数不等于网游认证或分服。 依据：[src/main_menu.cpp:462](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L462)。
- **充值与付费货币商城**（not-applicable-to-reviewed-base-flow）：源NPC交易、ATM现金卡和售货机是世界内买卖，不是现实支付或元宝充值。 依据：[src/trade_ui.cpp:301](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/trade_ui.cpp#L301)。
- **运营活动、每日签到、限时礼包**（not-confirmed-as-base-flow）：本次已读玩家菜单、任务与战绩未确认运营式日签礼包；MOTD是本地信息而非运营活动中心。 依据：[src/main_menu.cpp:435](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L435)。
- **玩家好友、世界聊天、邮件、网络组队**（not-applicable-to-reviewed-base-flow）：实际为NPC交谈、同伴、阵营和无线电联系，不能叠加玩家社交系统。 依据：[src/faction_ui.cpp:991](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_ui.cpp#L991)。
- **帮会、副本匹配、网络团队邀请**（not-applicable-to-reviewed-base-flow）：阵营/营地/同伴是世界内NPC与工作流程，不是玩家帮会和匹配副本。 依据：[src/faction_camp.cpp:777](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/faction_camp.cpp#L777)。
- **全服排行榜与排名奖励**（not-applicable-to-reviewed-base-flow）：scores为本地成就、准则、分数、击杀，不推导全服排名与领奖。 依据：[src/scores_ui.cpp:36](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/scores_ui.cpp#L36)。
- **大地图任意点付费传送**（not-applicable-to-reviewed-base-flow）：大地图规划步行驾驶路线；特定装置另有条件入口，不推广为任意点传送。 依据：[src/overmap_ui.cpp:2000](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/overmap_ui.cpp#L2000)。
- **死亡付费复活**（not-applicable-to-reviewed-base-flow）：基础死亡流程进入终局/成绩/后记，特殊防死内容不能证明通用付费复活。 依据：[src/game.cpp:2859](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game.cpp#L2859)。
- **开发调试和ImGui Demo**（excluded-player-scope）：调试地图实体编辑/开发调试控制台不是常规玩家UI；源scores明确调试人物成就禁用。 依据：[src/scores_ui.cpp:197](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/scores_ui.cpp#L197)。

## 制作采用建议

每个场景至少有一张整屏设计图；选中、确认、失败和结果可结合共享状态资源与相应状态预览表达。不得用同一张通用空态图宣称所有界面的具体条件均已设计。标记 mod-only 的两张图应在总预览中单列可选扩展，并在未启用时隐藏或展示明确未启用说明。

机器可读记录：[research-advanced.json](research-advanced.json)。整套覆盖、资源路径及实际验收状态由协调者维护的总清单决定。

## 补充核实的玩家交互

### npc-orders · 同伴命令与行为规则

入口与返回：同伴交谈/喊话入口 → 选择一位或多位同伴 → 临时命令与行为规则 → 切换近随/交战/枪械/睡眠策略 → 确认并返回。

适用状态：无同伴、一人/多人选中、默认行为、临时覆盖、已启用、恢复默认。

与followers资料页分别表达操作和信息；多人命令可能覆盖不同原规则，不添加网络团队权限。

依据：[src/npctalk.cpp:884](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/npctalk.cpp#L884)。

### animal-care · 驯养动物与骑乘交互

入口与返回：接近已友善/驯养动物 → 查看可用交互 → 改名/牵引/背包/护具/治疗/骑乘 → 选择物品或确认 → 返回世界。

适用状态：友善、已牵引/已拴住、可骑乘、不可骑乘、负载过重、缺绳索/器具、受伤。

这是世界动物的条件性交互，非抽宠、升星或玩家坐骑战力；物种与装备条件必须明确。

依据：[src/monexamine.cpp:649](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/monexamine.cpp#L649)；[src/monexamine.cpp:636](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/monexamine.cpp#L636)。
