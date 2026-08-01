# Architecture

## 数据流

```text
oc-character-designer canon v3.1
        ↓ build_handoff
ILLUSTRATION_HANDOFF (signed snapshot)
        ↓ ingest / validate
illustration workspace
        ↓ staged interview batches
project state + director brief
        ↓ prompt compiler
generation prompt + QA + continuity
        ↓ optional feedback
upstream change request
```

## 单一事实源

- 角色事实：上游 handoff 快照。
- 当前插画事实：`state/project.json`。
- 系列连续性：`state/continuity.json`。
- 提示词：由上述数据派生，不是 Canon。

## 反重复原则

下游不得复制并维护另一份可编辑的角色 Canon。`identity-contract.json` 可以缓存，但必须包含 `source_revision` 与 `source_hash`，并能从 handoff 重建。

## 事务边界

每个问题批次对应一次插画项目 revision。批次内任一字段、类型、旧值或权限校验失败时，整批不写入。
