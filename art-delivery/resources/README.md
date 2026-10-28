# 正式独立 UI 美术资源

本目录用于下一阶段 Unity 接入，当前仅交付美术。

- `ui/`：面板、标题、按钮、页签、列表、槽位、输入、进度条、滚动条、复选框和装饰；动态文字分离。
- `icons/`：道家风格类别徽标、示意卡片及 24 个现代生存物品透明图标。
- `fonts/`：官方 Noto Sans CJK SC Regular 与 SIL OFL 许可证。
- `backgrounds/`、`characters/`：由对应主视觉制作记录索引。

逐件规范及来源见 `../records/asset-manifest.json`，现代生存图标切片映射见 `../records/survival-icon-slices.json`。九宫格顺序为 Left、Bottom、Right、Top；所有大小是交付图片真实像素，不是模型原生细节的增幅证明。

源库 `icon-chest.png` 实物为阁楼建筑，已按实际外观命名为 `icon-cache-building`，不冒充箱子；`icon-medication` 是药葫芦类别标，真正的绷带、瓶装药剂等采用 `survival-*`。现有法器式技能卡仅是主题/可选系统美术示意，不把原 MMO 技能规则改称参考游戏原有功能。

`ui/title.png` 与 `ui/section.png` 已换成新生成干净无字原画的等比派生，避免扁平组队切片中的文字、天空和抹字区污染。`ui/clean-header-master.png` 是保留用于重建的源原画，不作为独立运行时控件计数；其逐图记录及派生裁切、缩放记录分别保留。正文标签仍由后续原生文字层绘制。

本阶段没有生成 Unity `.meta`、Prefab 或 C#。导入建议见 `../../docs/art-v2/UNITY_IMPORT.md`，引擎验证明确留待下一阶段。
