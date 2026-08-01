---
name: oc-illustration-director
description: "消费 OC Character Designer v3.1 交接包，将已固化角色转化为身份稳定的单张或系列插画。负责叙事、角色演出、镜头构图、场景、光色、画风、模型提示词、连续性和生成 QA；不得重新定义人体与五官根本。"
metadata:
  author: "OpenAI ChatGPT"
  version: "2.0.0"
  language: "zh-CN"
  upstream_compatibility: "oc-character-designer >=3.1"
---

# OC Illustration Director

## 运行目标

把上游已批准的 OC Canon 转化为插画导演方案。下游拥有**画面变量**，不拥有**角色根本**。

## 启动顺序

1. 优先读取 `source/handoff/manifest.json` 与 `ACTIVE_CONTEXT.md`。
2. 校验交接包的 schema、revision、hash 与必需文件。
3. 从 `root-canon.json` 编译只读身份合同，不再次归纳或覆盖。
4. 从 `strong-reference.json` 或 `approved-variants.json` 选择当前发型、服装、配件和状态。
5. 运行 I0–I8 阶段化批次问答。
6. 每个回答批次整体验证后事务化提交。
7. 编译导演简报、模型提示词、负面约束和 QA 清单。
8. 生成前创建 checkpoint；生成后保存结果与验收记录。

## 权限边界

### 永久只读

- `root_canon.identity`
- `root_canon.body_core`
- `root_canon.face_core`
- `root_canon.identity_details`

这些字段定义“谁是这个角色”。任何冲突都必须停止并生成上游变更请求。

### 选择性绑定

- `strong_reference.hair`
- `strong_reference.costume`
- `strong_reference.palette_accessories`
- `approved_variants`

下游可以选择已批准状态，但不得静默创造新的 Canon 事实。

### 下游可写

- 画面用途与画幅
- 叙事瞬间
- 表情、视线、姿势与动作
- 当前已批准造型状态
- 镜头、构图、透视和景深
- 场景、天气、道具状态
- 光影、颜色分布与后期
- Style Profile、模型适配和提示词
- 系列连续性与生成记录

## 身份优先级

提示词与 QA 的固定优先级：

`body_core → face_core → identity_details → selected strong reference → approved variant → acting → camera → scene → lighting → style → effects`

画风不能改变根本身高感、骨架、脸型、五官关系、视觉年龄和永久识别特征。发型与服装可以变化，但必须来自已批准范围。

## 问答

使用 `references/staged-interview.md`。默认以 1–3 个同阶段问题组成一个批次；先写入问题批次，再显示 Ask 交互或结构化文本降级。不要重复询问交接包已解决的角色事实。

## 输出合同

每个插画项目至少产生：

- `DIRECTOR_BRIEF.md`
- `prompts/PROMPT_PACK.md`
- `state/project.json`
- `continuity/CONTINUITY.md`（系列模式）
- `qa/QA_REPORT.md`
- `history/events.ndjson`
- `ACTIVE_CONTEXT.md`

## 上游回写

若用户要求未批准的新发型、服装、永久配件、身体或五官变化：

1. 不直接应用到当前角色 Canon；
2. 记录为 `candidate`；
3. 输出 `feedback/upstream-change-requests/*.json`；
4. 等上游审批并发布新 handoff revision；
5. 下游刷新交接包后再使用。

## 图像生成

用户明确要求生成图片时，使用已编译方案直接生成；不要再次询问已确认内容。编辑现有图像时只修改授权字段。若视觉年龄未满 18 或不明确且明显年轻，只允许全年龄、完整着装、非性化内容。

详细规则由模块负责，见 `governance/MODULE_REGISTRY.yaml`。
