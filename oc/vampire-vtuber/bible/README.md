# Character Bible Publication Layer

每个 `bible/sheets/<sheet-id>/` 目录是一个单一生产目的页面，包含：

- `sheet.json`：页面规格与 canon revision
- `prompt.md`：精确生成 prompt
- `annotations.json`：可编辑的后期标注文案
- `assets/`：页面源资产
- `output/`：clean 与 annotated 导出

先生成无段落文字的视觉版，再用 `annotations.json` 做确定性覆盖层；未生成或未验收的页面不能写成 approved。
