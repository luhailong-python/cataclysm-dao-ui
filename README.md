# 青岚余生（暂定名）· 全游戏道家 Q 版 UI 美术

本对话制作目录：**E:\work\image\cataclysm-dao-ui**。本次沿用已有独立目录，返修继续在这里进行。当前交付静态 UI、独立图片、状态及流程说明，Unity 接入留待下一阶段。

## 查看成果

- [完整图集：整屏、状态及排版记录](art-delivery/previews/index.html)
- [本次美术交付压缩包](exports/qinglan-ui-art-20261026.zip)
- [功能与资源总清单](art-delivery/previews/UI_COVERAGE.md)，[机器可读清单](art-delivery/records/ui-master-manifest.json)
- [正式资源目录](art-delivery/resources/)，[全部资源索引](art-delivery/records/complete-resource-manifest.json)
- [流程总览](art-delivery/previews/flow-overview.png)，[流程说明](docs/art-v2/FLOWS.md)
- [Unity 导入建议](docs/art-v2/UNITY_IMPORT.md)，[导入参数 CSV](art-delivery/records/unity-import-complete.csv)
- [最终验收记录](art-delivery/records/FINAL_ACCEPTANCE.json)
- [设计与制作说明](art-delivery/README.md)，[来源与项目关联](docs/image-reference-associations.md)

图集可直接用浏览器打开。整屏画布为 1920×1080，100 类源码研究的玩家界面，另有 1 类通用弹窗，共 101 张主设计图、133 张状态板。源系统 604 项状态加通用 6 项，共表达 610 个状态条目。状态板是文案与操作反馈合同，并非 610 张独立整屏。

独立资源 112 件：54 件 UI 皮肤、54 枚图标、3 张背景及 1 张透明人物。另有 2 张用于重切的母图，不计作独立控件。流程包括 1 张总览、7 张分组 PNG 及对应 SVG。逐项状态以总清单和最终验收为准。

## 来源分别管理

| 用途 | 已核实信息 |
|---|---|
| 功能参考 | [CleverRaven/Cataclysm-DDA](https://github.com/CleverRaven/Cataclysm-DDA)，固定提交 eb86dffd20072d6fde54af568cf229f3cd4d751f；本地 reference/Cataclysm-DDA |
| 美术参考 | F:\work\image，项目“五行奇谈”；origin 为 Azure DevOps https://luyuacpp.visualstudio.com/image/_git/image；其 GitHub 地址待确认 |
| 成果仓库 | 待用户后续提供；当前没有成果提交、推送或发布 |

最新消息中的游戏地址仍为占位文字，本次采用本对话此前实际提供的 Cataclysm-DDA 地址。已阅读源码与配置核实单人回合制生存、人物创建、探索、物品制作、NPC、营地、载具、义体和条件能力。联网账号、MMORPG 区服、世界聊天、充值、签到、抽卡没有作为本体功能添加。证据见 [核心研究](docs/art-v2/UI_REQUIREMENTS_CORE.md) 和 [高级系统](docs/art-v2/advanced-systems.md)。

F 盘按最新统一要求只读，来源和关联集中在本项目 docs/image-reference-associations.md。功能参考克隆仅用于研究，reference/ 已忽略，后续成果提交应排除它。

## 交付边界

整屏由已记录的手绘 PNG、独立中文和简单 UI 指示线合成。5 张本阶段新生成原画、既有入口插画、复用资源、裁切缩放与状态派生分别记录；101 张整屏不冒称 101 次模型生成。入口、场景和地图原画为原生 1672×941，人物为 1024×1536；1920 合成不代表原生细节升级。

画面采用玉绿、象牙纸绢、暖金云纹和道家 Q 版人物。动态文字独立，人物、地名及数值均为排版样例。图标用于类别与示例物品，未重画上游数千件物品或全部模组内容。

Unity 工程、C#、Prefab、业务交互、接口及引擎运行未实施或验收。下一阶段按布局、文字区、Sprite 参数和状态合同接入，复核目标设备、安全区、TMP 字库与实机效果。

此前 app/、assets/、qa/ 及启动脚本属于旧启动器阶段，保留已有成果；[历史说明](docs/legacy-launcher.md) 不作为当前美术或 Unity 验收。正式交付入口为 art-delivery/。

