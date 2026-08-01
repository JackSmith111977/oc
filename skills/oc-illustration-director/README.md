# OC Illustration Director 2.0

下游插画导演技能，兼容 `oc-character-designer` v3.1 的角色根本分层和文件持久化协议。

## 核心职责

- 读取上游 `ILLUSTRATION_HANDOFF`，而不是重新定义角色事实。
- 将 `root_canon` 作为只读根本；从 `strong_reference` 与 `approved_variants` 选择当前造型状态。
- 用阶段化批次问答确定叙事、表演、镜头、场景、光色、风格与模型。
- 事务化固化插画简报、提示词、连续性和生成记录。
- 若创意需要修改角色本体或新增强参考，输出上游变更请求，不直接篡改 Canon。

## 快速开始

```bash
python scripts/build_handoff.py \
  --canon ../oc-character-designer/characters/my-oc/canon/canon.json \
  --output ./ILLUSTRATION_HANDOFF

python scripts/illustration_workspace.py init \
  ./illustrations/my-scene \
  --handoff ./ILLUSTRATION_HANDOFF \
  --title "夜间电台主视觉"

python scripts/illustration_workspace.py status ./illustrations/my-scene
```

问答与写入使用批次文件，避免复杂 JSON 命令行参数：

```bash
python scripts/illustration_workspace.py queue-batch ./illustrations/my-scene \
  --file I2-B01.questions.json

python scripts/illustration_workspace.py commit-batch ./illustrations/my-scene \
  --file I2-B01.answers.json --dry-run

python scripts/illustration_workspace.py commit-batch ./illustrations/my-scene \
  --file I2-B01.answers.json
```

编译提示词：

```bash
python scripts/illustration_workspace.py compile ./illustrations/my-scene
```
