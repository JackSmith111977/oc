# Ask Interaction Adapter

Do not hard-code private widget syntax into portable prompts.

- If the runtime exposes a real interactive question tool, adapt the question batch to it.
- Otherwise render numbered options and `其他（自行填写）`.
- One batch stays inside one I-stage.
- Every question has 2–5 concrete options plus custom text when choices are not exhaustive.
- Typed text overrides a conflicting selected option.

Example fallback:

```text
I4 · 镜头与构图 · I4-B01

1. 景别？
   1) 环境全景：人物较小，世界信息优先
   2) 全身：动作和服装完整
   3) 半身：表情与手部互动平衡
   4) 近景：面部情绪优先
   5) 其他（自行填写）

2. 机位？
   1) 平视稳定
   2) 轻微仰视，增强存在感
   3) 轻微俯视，增强脆弱或亲近感
   4) 倾斜或特殊机位（自行填写）
```
