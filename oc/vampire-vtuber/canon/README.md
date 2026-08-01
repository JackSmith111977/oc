# Canon Layer

`canon.json` is the only machine source of stable character facts. `manifest.json` maps those facts to human-readable chapters; `field_registry.json` prevents unregistered or wrongly typed updates.

修改 canon 必须经过同阶段批次：`questions.json → answers.json → dry-run → commit`。页面和提示词只能消费 canon，不能反向偷偷修改 canon。
