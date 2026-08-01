# 设定集索引 v2.3

所有页面都基于同一份 canonical 角色锁定生成。当前状态为 **prompt draft／未完成图片验收**。

## 生产顺序

| 阶段 | 页面用途 | 提示词 |
|---|---|---|
| 01 | 中立全身视觉锚点：唯一主参考 | [`PROMPT_PACK.md`](prompts/PROMPT_PACK.md) |
| 02 | 单色线稿：验证脸、发型、服装和鞋袜轮廓 | [`LINEART_TURNAROUND_PACK.md`](prompts/LINEART_TURNAROUND_PACK.md) |
| 03 | 正面／严格侧面／背面三视图：验证比例、裙摆和背部系带 | [`LINEART_TURNAROUND_PACK.md`](prompts/LINEART_TURNAROUND_PACK.md) |
| 04 | 彩色角色模型表：验证正式服、状态配件和色材 | [`PROMPT_PACK.md`](prompts/PROMPT_PACK.md) |
| 05 | 表情与状态对照：验证眼镜和三种状态反差 | [`EXPRESSION_STATE_PACK.md`](prompts/EXPRESSION_STATE_PACK.md) |
| 06 | 动作与姿态对照：白天编程、贵族直播、宅化反应 | [`POSE_ACTION_PACK.md`](prompts/POSE_ACTION_PACK.md) |
| 07 | 服装／家徽／材质拆解：胸衣、系带、三层裙摆、家徽、鞋袜和眼镜 | [`COSTUME_HERALDRY_CALLOUT_PACK.md`](prompts/COSTUME_HERALDRY_CALLOUT_PACK.md) |
| 08 | 最终插画：单人夜晚古老宅邸贵族直播 | [`FINAL_ILLUSTRATION_PACK.md`](prompts/FINAL_ILLUSTRATION_PACK.md) |

## 版式选择

- 单角色全身、线稿、模型表、表情表和动作表：默认3:4纵向白底。
- 三视图与高密度拆解表：优先横向宽画布；无法容纳时分图生成后合成。
- 图像阶段不生成文字、标签、水印或 UI；标注在后期处理。

## 角色圣经

- [`CHARACTER_BIBLE.md`](CHARACTER_BIBLE.md)
- [`chapters/01-CHARACTER_CORE.md`](chapters/01-CHARACTER_CORE.md)
- [`chapters/02-VISUAL_CANON.md`](chapters/02-VISUAL_CANON.md)
- [`chapters/03-PRODUCTION_SPEC.md`](chapters/03-PRODUCTION_SPEC.md)
- [`chapters/04-QA_AND_WORKFLOW.md`](chapters/04-QA_AND_WORKFLOW.md)

## QA 结论

- 角色连续性：以 `state/oc.json` 的 `consistency_lock` 为唯一基线。
- 正式服：三层裙摆、方领、泡袖、蕾丝、背部交叉系带、鞋袜和家徽均为固定结构。
- 状态逻辑：眼镜只属于白天／宅家／程序员状态；正式直播／贵族状态摘下。
- 最终插画：只允许单人夜晚古老宅邸贵族直播，不加入第二人物、字幕或直播 UI。
