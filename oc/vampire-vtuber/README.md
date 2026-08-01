# 没落吸血鬼贵族 VTuber OC 工作区

这是按 `oc-character-designer` v2.2 持久化协议维护的角色工作区。聊天记录不是事实源；机器可读 canon 以 [`canon/canon.json`](canon/canon.json) 为准，人的总入口是 [`INDEX.md`](INDEX.md)。

## 阅读入口

1. 先读 [`ACTIVE_CONTEXT.md`](ACTIVE_CONTEXT.md)，确认当前 revision、阶段和未决项。
2. 再按需要读 [`canon/chapters/`](canon/chapters/) 中一个相关章节。
3. 生成设定集页面前读 [`bible/INDEX.md`](bible/INDEX.md)，再进入对应 `bible/sheets/<sheet-id>/`。
4. 需要修改设定时，先检查 [`interview/field_evidence.json`](interview/field_evidence.json) 和 [`decisions/DECISIONS.md`](decisions/DECISIONS.md)，通过批次提交，不直接改提示词制造分叉。

## 四层结构

| 层 | 文件 | 作用 |
|---|---|---|
| Canon | [`canon/canon.json`](canon/canon.json)、[`canon/chapters/`](canon/chapters/) | 稳定角色事实与一致性锁 |
| Interview | [`interview/`](interview/) | S0–S7 阶段、批次、证据和未决字段 |
| Publication | [`bible/`](bible/) | 设定集页面、页面规格、可编辑标注、资产和导出 |
| Working context | [`ACTIVE_CONTEXT.md`](ACTIVE_CONTEXT.md) | 可恢复的当前工作记忆 |

## 技能状态文件

- `canon/canon.json`：唯一 canonical 角色事实
- `interview/session.json`：会话与阶段状态
- `interview/pending.json`：当前批次状态
- `interview/field_evidence.json`：字段证据与迁移来源
- `bible/manifest.json`：有序设定集页面清单
- `bible/sheets/<sheet-id>/annotations.json`：可编辑标注副本
- `history/events.ndjson`：追加式审计记录
- `decisions/DECISIONS.md`：可持续设计决策
- `snapshots/`：重大修改和生成前检查点

## 兼容入口

旧版 [`state/`](state/)、[`chapters/`](chapters/)、[`CHARACTER_BIBLE.md`](CHARACTER_BIBLE.md)、[`SETTING_SET_INDEX.md`](SETTING_SET_INDEX.md) 和 `prompts/` 保留用于历史兼容；它们不是新的机器事实源。新内容应写入 v2.2 目录，并在必要时更新兼容入口。

## 修改规则

- 先通过已校验批次更新 `canon/`，再派生章节、页面规格和提示词。
- 不静默覆盖冲突；需要改变既有 canon 时，使用显式 revision 并记录 decision。
- 正式服是默认主视觉；白天程序员工作装只在明确请求白天／宅家变体时使用。
- 设定图保持全年龄、端庄、完全着装、非性化；不添加第二人物、文字或水印。
