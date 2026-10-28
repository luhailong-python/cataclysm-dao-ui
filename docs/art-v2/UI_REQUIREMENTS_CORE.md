# 全游戏 UI 核心功能研究

本次功能参考是 [Cataclysm: Dark Days Ahead](https://github.com/CleverRaven/Cataclysm-DDA)，不是此前其他窗口的 Unity 生存游戏。制作暂定名为 **青岚余生（暂定名）**。本阶段仅输出 UI 美术及 Unity 接入建议，不编写 Unity 业务实现。

参考源码已实际克隆到 `reference/Cataclysm-DDA`，固定提交 `eb86dffd20072d6fde54af568cf229f3cd4d751f`。源码未发现 AGENTS.md；上级目录规则由本对话目录规则及用户最新指令控制。README、主菜单/世界生成/人物创建/物品/制作/设置/帮助源码、UI 可访问性与边栏文档均已实际阅读。

本仓库是末日背景的回合制单人生存角色扮演游戏：创建本地世界，选择情景、职业与人物配置，在持续存在的世界探索、搜集物资、学习技能并制作维护装备。它的详细UI含列表/详情/快捷键与条件限制，不能机械套MMORPG登录、区服、商城及邮件。见 [官方README](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/README.md)。

`.gitattributes` 对 PNG/TTF 等使用 binary 属性，没有LFS过滤规则，`git lfs ls-files`为空；源码截图 PNG 已实际解码，非LFS指针。`reference/` 是只读功能研究来源，未来成果提交须排除该整个克隆。

## 已核实核心界面

| ID | 系统与界面 | 功能流程 | 必要状态 | 主来源 |
|---|---|---|---|---|
| main-menu | 启动与世界 / 启程首页 | 首页 → 新游戏或读取世界 → 创建或读取人物 → 进入游戏 | 有可读取存档、无世界、无存档、加载数据失败、退出确认 | [src/main_menu.cpp:430](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L430) |
| motd | 启动与世界 / 今日告示 | 首页 → 今日告示 → 滚动阅读 → 返回首页 | 有告示、无消息、长文滚动、文件缺失回退 | [src/main_menu.cpp:434](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L434) |
| credits | 启动与世界 / 制作与致谢 | 首页 → 制作名单 → 阅读来源与署名 → 返回 | 名单可用、无名单信息、长文滚动 | [src/main_menu.cpp:444](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L444) |
| world-list | 启动与世界 / 世界管理 | 首页 → 世界列表 → 选中世界 → 查看模组或复制规则或管理 → 返回 | 空列表、世界选中、无人物、复制规则、压缩切换、删除确认、重置确认、保存失败 | [src/main_menu.cpp:1169](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L1169) |
| world-create | 启动与世界 / 创建世界 | 世界列表 → 新建世界 → 名称与规则 → 完成确认 → 进入人物创建 | 默认规则、编辑后未保存、空名称随机确认、非法字符、同名世界、取消创建、创建失败 | [src/worldfactory.cpp:1501](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/worldfactory.cpp#L1501) |
| world-mods | 启动与世界 / 世界模组 | 创建世界 → 可用模组 → 启用与排序 → 检查依赖冲突 → 返回规则 | 可用、已启用、依赖缺失、模组冲突、过时模组、搜索无结果、不可调整顺序 | [src/worldfactory.cpp:985](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/worldfactory.cpp#L985) |
| world-options | 启动与世界 / 世界规则 | 创建或复制世界 → 调整规则 → 查看选项解释 → 确认 → 返回 | 默认、已修改、重置确认、数值边界、模组隐藏项、保存异常 | [src/worldfactory.cpp:746](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/worldfactory.cpp#L746) |
| load-character | 启动与世界 / 选择幸存者 | 读取游戏 → 选择世界 → 选择人物存档 → 确认读取 → 进入游戏 | 有存档、无人物可读、存档选中、读取中、存档读取失败、取消 | [src/main_menu.cpp:1122](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L1122) |
| creation-mode | 人物创建 / 创建方式 | 首页新游戏 → 自定义或模板或随机 → 预览 → 创建人物 | 自定义、预设模板、随机预览、保留情景重新随机、立即游玩、无模板 | [src/main_menu.cpp:476](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L476) |
| creation-scenario | 人物创建 / 开局情景 | 人物创建 → 情景 → 查看故事与要求 → 选择 → 职业 | 可选择、已选、成就条件未满足、起点限制、搜索无结果、取消 | [src/newcharacter.cpp:2793](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2793) |
| creation-profession | 人物创建 / 职业 | 情景 → 可选职业 → 查看初始装备技能特征 → 选择 → 背景 | 可选择、已选、成就条件未满足、情景限制、筛选无结果 | [src/newcharacter.cpp:1465](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L1465) |
| creation-background | 人物创建 / 人生背景 | 职业 → 背景列表 → 查看技能特征 → 选择背景 → 属性 | 未选择、已选择多项、背景条件不满足、冲突说明、搜索无结果 | [src/newcharacter.cpp:1736](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L1736) |
| creation-stats | 人物创建 / 初始属性 | 背景 → 力量敏捷智力感知 → 调整与查看影响 → 特征 | 默认、已调整、数值下限、数值上限、恢复调整 | [src/newcharacter.cpp:2812](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2812) |
| creation-traits | 人物创建 / 天赋特征 | 属性 → 特征分类与搜索 → 查看利弊冲突 → 选择 → 技能 | 未选择、已选择、情景锁定、职业锁定、互斥冲突、不可切换、搜索无结果 | [src/newcharacter.cpp:2818](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2818) |
| creation-skills | 人物创建 / 初始技能 | 特征 → 选择技能 → 查看等级描述 → 调整 → 总览 | 基础值、已调整、等级上下限、职业背景加成、搜索无结果 | [src/newcharacter.cpp:2824](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L2824) |
| creation-summary | 人物创建 / 身份与出发 | 人物创建各页 → 总览 → 名称外观起点与日期 → 最终确认 → 进入世界 | 信息完整、名字待填、随机描述、起点未选、开局日期选择、创建确认、返回修改、保存模板 | [src/newcharacter.cpp:1973](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/newcharacter.cpp#L1973) |
| character-templates | 人物创建 / 人物模板 | 新游戏 → 预设人物 → 模板列表 → 预览 → 总览调整 → 出发 | 有模板、空列表、模板选中、模板不可读、取消、新模板保存 | [src/main_menu.cpp:568](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/main_menu.cpp#L568) |
| character-sheet | 人物与成长 / 人物总览 | 主界面人物 → 属性概览 → 选中属性说明 → 切换标签 → 返回 | 正常、属性受影响、说明选中、长文滚动、外观自定义 | [src/player_display.cpp:1526](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L1526) |
| character-encumbrance | 人物与成长 / 负重与部位阻碍 | 人物总览 → 阻碍与速度 → 选中部位 → 查看穿戴影响 → 返回 | 正常、轻度阻碍、严重阻碍、速度修正、部位详情选中 | [src/player_display.cpp:289](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L289) |
| character-skills | 人物与成长 / 技能成长 | 人物总览 → 技能 → 选择技能 → 理论与实作进度 → 切换训练状态 → 返回 | 未习得、训练中、暂停训练、实作与理论不同、可继续提升、列表滚动 | [src/player_display.cpp:790](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L790) |
| character-proficiencies | 人物与成长 / 熟练技艺 | 人物总览 → 熟练技艺 → 选择技艺 → 查看学习与制作影响 → 返回 | 尚未掌握、学习中、已掌握、进度条、空列表 | [src/player_display.cpp:318](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/player_display.cpp#L318) |
| inventory | 行囊与装备 / 随身行囊 | 主界面行囊 → 分类搜索排序 → 选中物品 → 详情或操作 → 返回 | 有物品、空行囊、筛选无结果、超出负重、容量不足、物品选中、收藏标记 | [src/game_inventory.cpp:264](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L264) |
| item-detail | 行囊与装备 / 物品详情 | 物品列表 → 详情 → 查看描述与数值 → 可用操作 → 返回列表 | 正常、损坏、耐久不足、腐败或污染、未知信息、详细说明滚动 | [src/ui_iteminfo.cpp:47](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/ui_iteminfo.cpp#L47) |
| item-compare | 行囊与装备 / 物品比较 | 物品列表 → 比较 → 选择两件物品 → 差异对照 → 返回 | 仅选一件、两件已选、指标更优、指标更差、无法比较的项目 | [src/game_inventory.cpp:2746](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2746) |
| item-containers | 行囊与装备 / 容器与口袋 | 物品详情 → 容器口袋 → 选择口袋 → 移动物品或调整规则 → 返回 | 空口袋、已装物品、容量不足、物品不兼容、白名单黑名单、优先级、自动插入限制 | [src/item_contents.cpp:2982](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/item_contents.cpp#L2982) |
| advanced-inventory | 行囊与装备 / 周边与仓储转移 | 主界面高级物品管理 → 选择左右来源 → 筛选或排序 → 单件或批量转移 → 返回 | 两侧有物品、空来源、空目标、数量选择、超重、容器容量不足、位置不可达、过滤无结果 | [src/advanced_inv.cpp:271](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/advanced_inv.cpp#L271) |
| worn-layers | 行囊与装备 / 穿戴与衣层 | 人物装备 → 穿戴列表 → 选择部位与衣层 → 重排或脱下 → 查看阻碍 → 返回 | 衣层正常、衣层冲突、部位未覆盖、阻碍过高、无法脱下、选中移动 | [src/armor_layers.cpp:594](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/armor_layers.cpp#L594) |
| wield | 行囊与装备 / 选择手持物 | 主界面持用 → 选择物品 → 查看持用要求 → 确认 → 返回 | 可持用、已持用、双手需求、无法持用、无可选物品 | [src/game_inventory.cpp:2054](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2054) |
| pickup | 行囊与装备 / 拾取物品 | 地面互动 → 拾取列表 → 勾选物品及数量 → 确认 → 返回 | 有可拾取物、空地面、选中多件、数量输入、重量体积不足、容器选择 | [src/game_inventory.cpp:2558](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2558) |
| multidrop | 行囊与装备 / 丢弃与数量 | 行囊 → 多选丢弃 → 输入数量 → 确认落点与操作 → 返回 | 未选择、选中一件、选中多件、数量边界、收藏物提醒、取消 | [src/game_inventory.cpp:2512](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2512) |
| consume | 生存与物品 / 饮食与药品 | 主界面食用 → 食物饮水药品 → 查看营养与风险 → 确认 → 返回 | 可食用、缺少开罐或食用工具、腐败警告、无法食用、无可用物品、确认消耗 | [src/game_inventory.cpp:1076](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1076) |
| read | 生存与物品 / 阅读与学习 | 主界面阅读 → 选择书籍或电子书 → 查看知识门槛与时间 → 开始阅读 → 进度或中断 | 可阅读、尚未辨识、无法阅读、知识条件不足、黑暗或其他条件限制、已无可学内容、无书籍 | [src/game_inventory.cpp:1631](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1631) |
| reload | 行囊与装备 / 装填与弹药 | 手持武器或工具 → 装填 → 选择弹药与目标 → 数量 → 确认 → 返回 | 弹药兼容、没有兼容弹药、已满、多目标弹仓、数量不足、取消 | [src/game_inventory.cpp:3288](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L3288) |
| item-unload | 行囊与装备 / 卸下内容物 | 物品操作 → 卸载 → 选择容器或弹仓 → 选择目标 → 确认 → 返回 | 有可卸内容物、空容器、内容物锁定、选择多个容器、液体需兼容容器 | [src/game_inventory.cpp:3139](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L3139) |
| liquid-transfer | 行囊与装备 / 液体与容器 | 液体交互 → 选择目的容器 → 查看容量与兼容性 → 确认灌装 → 返回 | 可盛装、容量不足、容器不防水、内容物不兼容、无可用容器、取消 | [src/game_inventory.cpp:546](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L546) |
| item-use | 生存与物品 / 物品操作 | 物品详情或操作入口 → 使用功能列表 → 查看消耗要求 → 选择 → 结果反馈 | 功能可用、缺少消耗品、工具电量不足、没有注册用途、操作失败、操作完成 | [src/item_action.cpp:272](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/item_action.cpp#L272) |
| electronic-files | 生存与物品 / 电子设备与资料 | 电子设备使用 → 选择设备与资料 → 阅读复制或移动 → 选择目标 → 完成反馈 | 设备可用、无资料、空存储、容量不足、电量不足、选中多个文件、传输耗时 | [src/game_inventory.cpp:1885](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1885) |
| repair | 制作与维护 / 修理与材料 | 修理工具使用 → 选择损坏物品 → 查看材料工具条件 → 修理方式 → 结果 | 可修理、材料不足、电量不足、技能不满足、无可修物、修理成功、修理失败 | [src/game_inventory.cpp:2395](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L2395) |
| gunmods | 制作与维护 / 枪械配件 | 配件使用或枪械操作 → 选择武器或配件 → 查看槽位与条件 → 确认安装或拆下 → 返回 | 兼容、配件槽满、不兼容、技能不足、安装风险提示、已安装、拆下确认 | [src/game_inventory.cpp:1309](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L1309) |
| craft-recipes | 制作与维护 / 制作配方 | 主界面制作 → 分类搜索 → 选择配方 → 材料工具熟练要求 → 制作或批量 → 活动进度 | 可制作、缺少材料、缺少工具、理论知识不足、熟练技艺不足导致时间惩罚、配方隐藏、收藏、搜索无结果 | [src/crafting_gui.cpp:859](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/crafting_gui.cpp#L859) |
| craft-batch | 制作与维护 / 批量制作 | 制作配方 → 批量 → 调整数量 → 重新计算时间与需求 → 确认 → 制作活动 | 数量1、数量已调整、材料不足、最大可制数量、批量节时、收藏材料警告、取消 | [src/crafting_gui.cpp:764](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/crafting_gui.cpp#L764) |
| disassemble | 制作与维护 / 拆解回收 | 主界面拆解 → 选择可拆物 → 查看产出工具耗时 → 确认 → 活动进度与结果 | 可拆解、没有可拆物、工具不足、其他条件不足、预计产出、操作中断、完成 | [src/game_inventory.cpp:634](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/game_inventory.cpp#L634) |
| settings-general | 设置与辅助 / 通用设置 | 设置 → 通用 → 编辑选项 → 查看解释 → 保存或放弃 → 返回 | 默认、已修改、保存确认、放弃确认、无效值、重启后生效 | [src/options.cpp:1571](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L1571) |
| settings-interface | 设置与辅助 / 界面与辅助 | 设置 → 界面 → 语言单位与辅助 → 编辑 → 保存 → 返回 | 默认、已修改、依赖选项禁用、需重启、读屏辅助、保存确认 | [src/options.cpp:1885](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L1885) |
| settings-graphics | 设置与辅助 / 画面与字体 | 设置 → 画面 → 字体图块动画与小地图 → 编辑 → 预览与确认 → 返回 | 默认、已修改、字体不可用、图块集不可用、需重启、窗口尺寸变化 | [src/options.cpp:2399](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L2399) |
| settings-audio | 设置与辅助 / 声音与音量 | 设置 → 声音组 → 开启声音并选择音效包 → 音量 → 保存 → 返回 | 声音开启、声音关闭子项禁用、无音效构建、音效包缺失、更换需重启、已修改 | [src/options.cpp:1831](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/options.cpp#L1831) |
| keybindings | 设置与辅助 / 按键映射 | 设置或当前界面帮助 → 按键映射 → 搜索动作 → 添加删除或重置 → 冲突确认 → 返回 | 全局映射、当前界面映射、未绑定、冲突、等待输入、恢复默认确认、搜索无结果 | [src/input_context.cpp:1000](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/input_context.cpp#L1000) |
| help | 设置与辅助 / 帮助与引导 | 主菜单或游戏中帮助 → 主题分类 → 阅读条目 → 翻页 → 返回分类 | 主题列表、内容已打开、长文滚动、按键帮助、返回分类、教学入口 | [src/help.cpp:166](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/help.cpp#L166) |
| colors-theme | 设置与辅助 / 颜色与主题 | 设置 → 颜色管理或ImGui样式 → 选择颜色与预设 → 预览 → 保存或还原 | 默认配色、自定义配色、正常与高亮预览、修改未保存、还原确认、保存失败 | [src/color.cpp:836](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/color.cpp#L836) |
| loading | 启动与世界 / 加载与生存提示 | 新游戏或读取 → 当前加载上下文与步骤 → 完成 → 进入游戏 | 正在加载、模块步骤切换、生存提示、加载完成、加载失败说明 | [src/loading_ui.cpp:258](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/src/loading_ui.cpp#L258) |
| tutorial | 设置与辅助 / 生存教学 | 主菜单教学 → 教学世界 → 按区域触发说明 → 完成操作 → 下一提示 | 教学提示、操作已完成、下一步骤、退出确认、共享地图不适用 | [data/mods/dda_tutorial/traps.json:19](https://github.com/CleverRaven/Cataclysm-DDA/blob/eb86dffd20072d6fde54af568cf229f3cd4d751f/data/mods/dda_tutorial/traps.json#L19) |

## 适用边界与布局调整

- 人物创建源码标签为情景、职业、背景、属性、特征、技能、总览；锁定或条件不足来自成就、情景/职业限定或特征冲突等，不创设充值解锁。人物总览包含基础属性、阻碍、速度、技能、特征、义体、效果和熟练技艺；本文件只负责core部分，相关高级系统另列。
- 穿戴包括衣层顺序、部位覆盖、保暖与阻碍；技能包含实作/理论和训练状态；不添加MMORPG式总战力与通用角色等级。
- 行囊的重量、体积、容器和口袋限制必须可见。所谓仓储页使用高级物品管理的本地来源双栏转移，保持空间限制。
- 制作包括分类/搜索/收藏/隐藏配方、材料替代、工具品质、理论/熟练门槛、批量数量和时间修正。各类可用/不足/中断/完成状态可共用状态预览，但不能省略其文案与资源映射。
- 声音设置在源码属于General中的soundpack组，单列声音页是本次导航重组，不声称原本独立存在。无声音构建应隐藏/禁用相应项。
- 图形预览的所有人物名、数量、日期和数值是明确标注的示例。正式名未给定，使用青岚余生（暂定名）。

## 不适用或未确认

- **联网账号登录与注册**（not-applicable）：该源码的主菜单直接创建/读取本地世界与人物，没有MMORPG账户登录流程；可选map sharing不等于账户大厅。
- **MMORPG服务器选择**（not-applicable）：世界列表是本地世界管理，不是网络区服列表。
- **充值与付费货币商城**（not-applicable）：未在研究到的玩家核心功能中发现充值或付费货币；NPC交易由advanced清单覆盖，不换成充值商店。
- **玩家邮箱、好友与世界聊天**（not-applicable）：NPC对话/阵营/任务适用，但不据此创造MMORPG玩家社交系统。
- **签到、抽卡与限时运营领取**（not-applicable）：成就/统计适用，但没有将运营签到或抽卡作为本体功能的源码依据。
- **内置热更新下载器**（not-confirmed）：官方源码主菜单未提供客户端更新器；外置发行/启动器的下载不属于已核实本体UI，可作为建议扩充分列，不能标已有。
- **跨地区远程公共仓库**（not-applicable）：高级物品界面在周边地面/载具/角色容器之间转移，不能替换成不受空间约束的公共仓库。

## 研究范围与未完成证明

本文件核实 51 个core界面族；源码引用已绑定提交。高级玩法的功能清单由并行研究补充。这里只证明功能研究，不证明美术图、独立资源、状态预览或Unity导入已经完成；必须由总清单逐项链接实际文件并验收。

本次未向功能参考仓库提交或推送。成果提交账户、仓库与要求待用户后续提供。
