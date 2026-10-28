# 新项目与美术参考核查

> 本文是初期核查的历史记录。用户随后纠正为“每个都新建一个本地目录，Git 仓库不确定，先做完”。本次最终独立交付路径为 `E:\work\image\cataclysm-dao-ui`，项目为 Cataclysm: Dark Days Ahead 道风主题启动器；现有父目录 Unity 工程另属其他任务。本报告已移入正确项目，当前状态以本项目 README、UI_SPEC、ASSET_SOURCES 与验收记录为准。此前误建的父目录空 Git 元数据清理被自动审批阻止（仅返回 blocked by policy），因此保留，未宣称已移除，也未提交或绑定远端。

核实日期：2026-10-26（America/New_York）。用户后续要求“先本地仓库”，已为本地目录建立独立 Git 仓库。远端及首个 UI 模块待确认；本窗口尚未开始正式美术生成或实现。

## 两个独立目录

| 项目 | 实际路径 | 已核实状态 |
|---|---|---|
| 新项目开发目录 | `E:\work\image` | 普通目录，非目录链接；本窗口按用户后续要求初始化独立 Git 仓库，当前无远端。原有在制文件保留。 |
| 美术参考仓库 | `F:\work\image` | 普通目录，Git 根为 `F:/work/image`；README 名称为“五行奇谈 · Q 版游戏美术”。 |

参考仓库 origin 的 fetch/push 均为 <https://luyuacpp.visualstudio.com/image/_git/image>。这是 Azure DevOps 地址；参考仓库 GitHub 地址待确认。

消息内的实际链接 <https://github.com/CleverRaven/Cataclysm-DDA> 已可访问，仓库名称为 **Cataclysm: Dark Days Ahead**，官方 README 将其描述为末日背景的回合制生存游戏。这只证明链接所指仓库身份，不能证明其就是本地目录对应项目。

初次读取时，新项目只有文件 `docs/production/lobby-v1.prompt.txt`，描述“中国道家 Q 版生存游戏大厅插画”，要求 16:9、人物位于左侧、右侧保留 UI 空间、无文字及无界面框。该文件不是已确认的完整需求合同，其项目名、技术栈、UI 模块、目标平台和正式分辨率均未核实。文件 SHA-256：`66eb99fb6c9a655613de4da662dc159f9f1eae4116cb12cbda8b9ee9a960189e`。

本次开始核查时，`E:\AGENTS.md`、`E:\work\AGENTS.md`、`E:\work\image\AGENTS.md`、`E:\work\image\README.md` 均不存在；没有发现新项目代码、资源合同、交接或验收文件。没有覆盖已有目录、初始化 Git 或进行克隆。该目录已有在制文件，不能按“路径不存在”处理。

### 核查期间出现其他写入

2026-10-26 05:33（America/New_York，UTC-04:00）复查时，目录中出现本窗口及本窗口子任务均未创建的 `assets/DaoSurvivor` 代码和资源、`docs/ASSET_SOURCES.json`、`Packages/manifest.json`、`ProjectSettings/ProjectVersion.txt`、`.gitignore`，以及正在写入的 `.local/tools` 安装文件。它们属于并行在制内容，本窗口未修改、移动、清理或运行。

已实际读取的 `docs/ASSET_SOURCES.json` 自称暂定名“道途幸存者”、Unity 平台，并记录另一来源 URL `https://github.com/Roo-Roo-Roo/survivors-roguelike-kit`，同时明确 `gitRemoteBindingConfirmed: false`。这与本窗口提供的 Cataclysm-DDA 链接不同；该清单是其他写入方的声明，不是本窗口用户对目标项目的确认。清单列出 18 张参考仓库图片复用及两张风格参考，但本窗口没有逐项验收这些外部新增资源，不能将其算作本窗口交付。

该次复查时 `AGENTS.md`、`README.md` 仍未出现，Git 根检查仍失败。原始提示词与两张参考原图哈希复查未变。后续工作需要明确首个 UI 模块及并行在制范围，避免覆盖正在写入的 Unity 工程。

## 按后续要求建立本地仓库

用户回复“先本地仓库”后，本窗口执行 `git init --initial-branch=codex/local-ui`，已核实 Git 根为 `E:/work/image`，元数据位于本项目 `.git`。分支为 `codex/local-ui`，没有配置远端，没有创建提交或上传；工作区在制文件仍未暂存。此操作只针对 E 盘独立新仓库，未操作 F 盘 Git 状态。

已验证现存 `.gitignore` 将 `.local/tools` 安装文件、Unity `Library`、`Temp`、`Logs`、`UserSettings` 与 `Builds` 排除；`RunModel.cs`、`Packages/manifest.json`、`ProjectSettings/ProjectVersion.txt` 与本核查文档均未被忽略。没有替换并行写入方的 `.gitignore`。本次只初始化本地仓库，未把仍在变更的工程宣称为已验收提交。

## 实际读取及影响

已读取参考仓库以下现存文件：

- `AGENTS.md`、`README.md`（含“给接手的 Codex”）。
- `docs/WUXING_QITAN_HANDOFF.md`、`docs/QDAO_ART_DIRECTION.md`。
- `docs/IMAGE_MODEL_POLICY.md`、`config/image-generation.json`。
- `designs/README.md`。
- `designs/mail-ui-v1/README.md`、`UI_SPEC.md`、`source/generation.json`。
- `designs/team-ui-v2/README.md`、`source/generation.json`。
- `docs/AI_DESIGN_TOOLS_SETUP.md` 的内置入口、模型设置、移机及凭据相关说明。

`qdao_ui_redesign_v5/UI_SPEC.md` 当前缺失，未能读取其第 2 节；README 指向的 `docs/COMPUTER_HANDOFF_20261011.md` 也缺失。未从历史 Git 恢复。`designs/README.md` 中“邮件 PNG 缺失”与旧 D 盘替代路径的说明已过时，以当前根规则和真实文件为准。历史文档中的 E 盘路径、旧发布授权、游戏名称及 Unity 验收不作为本次新项目的实现或发布授权。

后续采用玉绿／青绿、象牙暖米纸绢、细暖金边、圆润云纹及适量道家元素。正文、状态和操作原生实现；参考中的邮件、奖励、等级、人物名称不作为新项目业务数据。旧参考的 2560×1080 布局目标不自动成为新项目尺寸合同。

图像配置当次读取值为 `gpt-image-2.5-sunburst`、`max`、`ChatGPT Images 2.5`，配置核对日为 2026-10-22；这些是配置目标，本次没有执行生成，也没有证明实际返回型号或质量。正式生成前须重新核对官方能力并重读适用规则，使用真实图片输入；内置入口优先，无选择器或返回证据的字段记录为未确认，每张图记录配置快照、提交参数、返回信息、时间、来源和正式路径。

## 已实际查看的风格来源

| 参考仓库相对路径 | 实际文件 | SHA-256 | 使用方式与新项目位置 |
|---|---|---|---|
| `designs/mail-ui-v1/01-mail-event.png` | PNG，1931×814，2,576,312 字节 | `3cf0b7d7b3bae337d51e947719588419a01ae21bdce9bccedd6258ce1feef0a2` | 已查看并核查风格；正式采用和资源位置待确认。 |
| `designs/team-ui-v2/team-ui-v2.png` | PNG，1931×814，2,356,938 字节 | `5fab5229de7030ac48172cfa39bb45f612a545cee0dba6303ae6f2dcfdf38750` | 已查看并核查风格；正式采用和资源位置待确认。 |

已检查 PNG 文件签名及哈希，两图均为真实图片字节，不是 LFS 指针。参考仓库使用 Git LFS，本次需要查看的两图已取得；没有宣称全库 LFS 下载完成。本窗口未把任何参考素材复制到新项目；其他写入方新增的资源情况见上节。

初期对应来源目录的项目关联入口为 `F:\work\image\designs\mail-ui-v1\README.md` 和 `F:\work\image\designs\team-ui-v2\README.md`，当时仅作核查，正式使用关系待确认。2026-10-26 按用户要求，后续确认的3段关联已从F盘迁回[本项目素材关联记录](image-reference-associations.md)，现以该文档及本项目来源清单为准。

## 本次输出和继续条件

本次新增输出为本核查文档、E 盘独立 Git 元数据及两处必要的待确认关联记录。没有本窗口制作的 UI 成品、切片、运行预览或游戏运行验收；不能把本核查当作设计交付。

已只读检查候选 Cataclysm-DDA 的官方 README、贡献规范、主菜单及 UI 源码、Windows 构建说明：其为 C++ 原生游戏，使用 catacurses/ui_manager 及 ImGui 适配，不能直接把 Unity 或网页预览当成该游戏实现。上游贡献规范有 LLM 来源投稿限制，见 <https://github.com/CleverRaven/Cataclysm-DDA/blob/master/CONTRIBUTING.md#licensing-and-authorship>；该要求只作为候选项目后续投稿约束记录，不扩大为禁止用户本地改造。候选核查未克隆或修改该仓库。

初期已向用户请求确认实际目标与首个 UI 模块，用户后续选择先处理本地仓库，已完成本地初始化。当时后续工作为核实具体 UI 范围、资源合同与运行入口，远端绑定待确认；代码、正式素材、制作记录与验证输出保存在 E 盘，F 盘仅曾补充来源关联，未操作其 Git HEAD、index、refs、提交或推送。当前独立交付目录与验收状态以本文开头说明及本项目文档为准，素材关联已迁回上述本项目文档。
