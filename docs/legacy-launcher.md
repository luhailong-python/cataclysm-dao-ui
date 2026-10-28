> 历史阶段存档：以下为旧启动器说明，不是本次全游戏 UI 美术或 Unity 验收。F 盘关联已迁回本地 docs/image-reference-associations.md，当前 F 盘只读。

# Cataclysm: Dark Days Ahead · 道风主题启动器

本项目独立目录：**`E:\work\image\cataclysm-dao-ui`**。首批界面包括启动首页、继续游戏、世界存档、设置与帮助；以 Python/Tk 原生桌面窗口实现，实际扫描本地存档并启动官方游戏。没有与父目录的“道途幸存者”Unity 工程混用代码或素材输出。

上游游戏：[CleverRaven/Cataclysm-DDA](https://github.com/CleverRaven/Cataclysm-DDA)。这是游戏来源地址，本地主题交付的 Git 仓库与发布远端尚未指定。本次没有提交或推送。

## 直接运行

本机可双击 [start.cmd](../start.cmd)，或运行：

```powershell
Set-Location -LiteralPath 'E:\work\image\cataclysm-dao-ui'
python -m app
```

运行环境为 Python 3.11+、Tk 与 Pillow；本机已核实 Python 3.14、Tk 8.6、Pillow 12.2.0。其他电脑先执行 `python -m pip install -r requirements.txt`。快捷键：`N` 启动游戏、`C` 继续旅程、`W` 世界存档、`S` 设置、`F1` 帮助、`F5` 刷新、`F11` 启动器全屏、`Ctrl+S` 保存设置；按钮与输入字段支持 Tab／Shift+Tab，Enter 确认，Escape 返回首页。

本地已下载的官方游戏位于 `.local/runtime/0.I-1/cataclysm-tiles.exe`，启动器会自动发现。游戏版本、官方发行 URL、下载哈希和实际启动证据见 [运行来源](../docs/RUNTIME_SOURCE.json)。`.local` 为本机运行目录，不作为源码交付依赖；移机时可另行下载官方游戏，在“游戏设置”中选择它。

## 功能与数据

- “开始游戏”进入官方游戏主菜单，在那里创建世界、人物并开始生存。
- “继续旅程”读取所选用户目录的真实 `save/<world>/*.sav` 与 `*.sav.gz`，按世界名启动。官方 `--world` 加载该世界首个存档；其他人物在游戏内选择。
- “世界存档”展示真实目录、角色存档数量及最近时间，支持刷新、列表翻页和打开文件夹。没有删除或重写游戏存档的功能。
- “游戏设置”选择游戏程序与用户目录，并保存启动器文字大小和窗口模式；设置位于 `.local/user/settings.json`。
- 默认游戏用户目录为本项目 `.local/game-user`，首次使用会正确显示无世界／无存档状态。截图中的列表测试数据只存在于隔离验收目录，不预置到正式用户目录。

游戏通过 `--basepath`、`--userdir`、`--world` 参数数组启动，进程运行时阻止重复启动，找不到程序或启动失败时显示实际错误。本批完成的是主题启动入口；官方 C++ 游戏内部的背包、战斗 HUD、地图与规则仍由游戏提供，未宣称这些窗口已经换肤。

## 查看与验证

默认布局目标 1920×1080，并验证 1600×900 与 1280×720。实际 Tk 客户区截图和定向检查结果存放在 [qa](../qa/)；游戏实际窗口截图与启动器界面截图分开。运行测试：

```powershell
python -m unittest discover -s tests -v
```

布局、状态和控件规格见 [UI_SPEC.md](../docs/UI_SPEC.md)。最终验证结果以 [qa/validation.json](../qa/validation.json) 为准，不把静态插画当作运行验收。

## 美术来源和逐图记录

美术参考仓库为 `F:\work\image`，已核实远端为 [Azure DevOps image](https://luyuacpp.visualstudio.com/image/_git/image)；参考仓库 GitHub 地址仍待确认，与上游游戏 GitHub 分别记录。

已实际查看并作为生成输入的两张主参考保存于 [邮件风格图](../docs/reference-images/mail-style.png)和[组队风格图](../docs/reference-images/team-style.png)。同时查看源库 `qdao_ui_redesign_v5/01_login_2560x1080.png` 与 README 研究入口层级。源库指定 `qdao_ui_redesign_v5/UI_SPEC.md` 当前缺失，未从旧 Git 恢复；当前明确风格要求和实际成图仍适用。

| 素材 | 使用方式 | 可追溯记录 |
|---|---|---|
| [幸存者主视觉](../assets/art/survivor-keyart.png) | 内置 image_gen 新生成；原生 1672×941 RGB，无字无界面框 | [逐图模型与质量证据](../assets/art/survivor-keyart.png.generation.json)、[实际提示词](../docs/production/survivor-keyart.prompt.txt)、[返回记录](../docs/production/imagegen-receipt.json) |
| `assets/ui/*.png` | 源库组队界面透明控件逐字节复用，运行时九宫格显示；文字独立 | [来源、哈希、尺寸与边距](../docs/ASSET_SOURCES.json) |
| `docs/reference-images/*.png` | 两张指定风格参考的完整副本，不作为运行背景 | [来源清单](../docs/ASSET_SOURCES.json) |

插画当次配置目标为 GPT Image 2.5 Sunburst / max，已复核官方资料；本次内置入口未披露实际模型和质量，逐图记录明确标为未确认。原生图未放大保存；1920 布局中的显示缩放不代表原生 1920 或 4K 细节。

参考仓库项目关联记录位于 `designs/mail-ui-v1/README.md`、`designs/team-ui-v2/README.md` 和 `qdao_ui_redesign_v5/README.md`。F 盘仅追加必要关联，未操作其共享 Git HEAD、index、refs、提交或推送。
