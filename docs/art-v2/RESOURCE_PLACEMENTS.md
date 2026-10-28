# 独立图片使用位置映射

[总索引](../../art-delivery/records/resource-placement-index.json) 对应 101 张主设计图和 133 张状态板，共 234 份布局记录。每份在 `art-delivery/records/resource-placements/`，与同名的 PNG、`records/layouts/` 文字说明配套。

这些 JSON 通过对最终冻结的制作脚本作几何追踪取得，没有重新生成或改写 PNG。导出时核对原图 SHA 和四项制作输入哈希；每份映射还绑定导出工具哈希。不能把几何追踪称作 Unity 接入。

- `imageAreas`：逐次使用的图片路径、源尺寸、目标 rect 与处理方式。`drawOrder` 是图片之间的绘制顺序，文字和原生 UI 指示另列。
- `rect`：左上原点的 `[x,y,width,height]`，基准画布 1920×1080。
- `resolvedRect`：等比 Contain 后的实际定位；Cover 则按中心裁边。
- `borderSourceLeftBottomRightTop`：原图 Border，按 Unity L/B/R/T 顺序。
- `borderRenderedLeftBottomRightTop`：静态制作器为该预览目标尺寸采用的边框缩放值；后续 Unity 可以按组件整体缩放实现，不能直接当作原图 Border 覆盖导入设置。
- `vectorUI`：进度填充、轨迹、目标圈、施工网格等简单原生 UI 指示，不是新增绘画资源。
- `textLayout`：对应的独立中文、字号、颜色、对齐和文字区域说明。

在 Unity 中转换坐标、Anchor、安全区、遮罩和层级时，以原 PNG 对照验证。绘制顺序建议见 UNITY_IMPORT；当前没有建立 RectTransform、Prefab 或实际 Canvas。
