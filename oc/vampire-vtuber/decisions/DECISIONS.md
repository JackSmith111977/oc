# Design Decisions

## 2026-07-26T15:39:44+00:00 — 固定角色的三面性结构

- Decision: 白天程序员的低能量宅家状态、宅家时佩戴古董金色椭圆框眼镜、直播／贵族状态摘下眼镜并呈现优雅自信，直播内容涉及游戏、杂谈、动画与电台。
- Reason: 这是目前最强的角色反差和可视化行为锚点，能直接指导表情、姿态、眼镜状态对照与VTuber场景。
- Scope: character-core

## 2026-07-26T15:39:44+00:00 — 固定新月荆棘蝙蝠徽

- Decision: 黑色丝带中央佩戴由旧金色新月、黑紫色展开双翼蝙蝠、荆棘蔷薇与暗红宝石组成的家徽。
- Reason: 三种元素组合是用户明确确认的家族象征，应作为跨服装和跨画面的不变识别符号。
- Scope: visual-canon

## 2026-07-26T15:51:32+00:00 — 核心动机：寻找陪伴

- Decision: 她最想在漫长岁月中找到真正的陪伴。
- Reason: 她独自居住在逐渐衰败的古老宅邸，家族只剩象征性的贵族名号；白天作为程序员、夜晚作为 VTuber 与观众交流，表面上维持现代生活，内心却渴望建立能跨越漫长寿命的真实关系。
- Scope: oc_profile.motivation_conflict

## 2026-07-26T15:59:21+00:00 — 血液操控与美食偏好

- Decision: 她的标志性吸血鬼能力是血液操控，使用代价是饥饿与失血；她非常喜欢美食，并将其作为现代生活中的日常享受与寻找陪伴的具体行为。
- Reason: 能力提供明确的吸血鬼辨识度与叙事代价；美食偏好连接程序员日常、VTuber杂谈和核心动机“在漫长岁月中找到陪伴”。
- Scope: character core and acting cues

## 2026-07-26T16:05:03+00:00 — 鞋袜组合

- Decision: 正式哥特萝莉服装固定采用黑色玛丽珍鞋＋白色蕾丝长袜。
- Reason: 该组合保留少女感、古典哥特萝莉轮廓与黑白对比；与黑紫、暗红、旧金主配色及长裙结构协调，并补足全身视觉锚点中的鞋袜识别。
- Scope: visual canon / costume construction

## 2026-07-26T16:10:54+00:00 — 胸衣采用背部交叉系带

- Decision: 背部交叉系带，系带结构可见于背面视图
- Reason: 强化古典吸血鬼贵族与束腰结构的时代感，并为背面三视图提供明确的服装工程细节。
- Scope: visual_canon.costume_construction.bodice_closure

## 2026-07-26T16:15:55+00:00 — 裙摆采用三层结构

- Decision: 裙摆采用三层结构：内层支撑蓬松轮廓，中层提供裙体体积，外层以蕾丝与装饰边收束层次。
- Reason: 三层结构在哥特萝莉蓬松度、蕾丝可读性与少女角色的行动便利性之间取得平衡，适合后续全身锚点、线稿和三视图稳定呈现。
- Scope: visual-canon / costume construction

## 2026-07-26T16:23:07+00:00 — 正式服与日常工作装分层

- Decision: 正式服保留完整三层哥特长裙；日常服改为宽松衬衫、针织外套与简化长裙。
- Reason: 明确直播／贵族状态与白天程序员身份的视觉区分，同时保留正式服作为角色主视觉锚点，避免现代工作装覆盖哥特贵族核心识别。
- Scope: visual-canon / costume construction

## 2026-07-26T16:28:21+00:00 — 正式服主色比例

- Decision: 正式服采用黑紫70％、暗红20％、旧金10％；黑紫覆盖主要裙装与胸衣结构，暗红集中于内衬、蔷薇与宝石，旧金仅用于家徽、扣饰和细边点缀。整体视觉沉静克制。
- Reason: 用户选择选项3。该比例强化黑紫主导的没落吸血鬼贵族气质，使暗红成为集中而明确的血族视觉符号，旧金作为少量家徽与金属点缀，避免正式服过度鲜艳。
- Scope: visual-canon / palette

## 2026-07-26T16:36:28+00:00 — 设定图采用3:4纵向画幅

- Decision: 设定图默认采用3:4纵向画幅，突出单角色全身比例；三视图与拆解信息需在纵向画布内分区排布，避免裁切。
- Reason: 用户选择选项2。纵向画幅更适合当前角色的长发、长裙和全身比例，也能保持主视觉锚点的垂直轮廓。
- Scope: production-spec / layout

## 2026-07-26T16:41:13+00:00 — neutral-full-body-anchor-v1

- Decision: 以正式服建立中立全身视觉锚点，作为后续线稿、三视图、彩色设定表和插画提示词的唯一视觉基线。
- Reason: S0–S7 已完成；技能要求先锁定中立全身视觉锚点，再派生其他交付物。当前已确认的服装、家徽、眼镜逻辑、鞋袜、三层裙摆、配色和3:4纵向画幅均纳入基线。
- Scope: production_sequence

## 2026-07-26T16:49:57+00:00 — 选择先制作线稿与三视图提示词

- Decision: 保留外表约14–16岁、实际年龄未知的当前设定；暂不生成中立全身图，先制作单色线稿、严格正侧背三视图与彩色模型表提示词。
- Reason: 全身图生成触发了安全误判；结构型设定图能够在不改变角色年龄与视觉 canon 的前提下，先验证发型、服装层次、背部系带和家徽结构。
- Scope: production_workflow

## 2026-07-28T14:47:02+00:00 — 按最新技能重构为索引—章节档案

- Decision: 以 state/oc.json 作为唯一 canonical source of truth，新增 CHARACTER_BIBLE.md、SETTING_SET_INDEX.md 与 chapters/01–04 作为人类可读索引和章节；保留现有 prompts/ 阶段包，并将动作与姿态对照纳入生产顺序。
- Reason: 用户要求按最新版 oc-character-designer 重构文件结构并支持后续补充；索引—章节形式符合既有偏好，同时满足 Character Core、Visual Canon、Production Pack 三层分离和技能持久化协议。
- Scope: workspace-structure

## 2026-07-29T00:00:00+00:00 — 迁移为 oc-character-designer v2.2 四层工作区

- Decision: 将机器 canon 迁移至 `canon/canon.json`；将阶段问答与证据迁移至 `interview/`；将设定集页面、页面规格、可编辑标注与资产目录迁移至 `bible/`；保留旧 `state/`、`chapters/` 和提示词作为兼容入口与历史来源。
- Reason: 新技能把角色事实、采访、出版物和工作记忆分层，能在不依赖完整聊天记录的情况下继续补充，并支持单页面 QA 与两遍标注流程。
- Scope: workspace-structure; no canon facts changed

## 2026-07-29T00:00:00+00:00 — 采用 standard-plus 设定集页面集合

- Decision: 规划 S00、S10、S15、S20、S30、S32、S36、S40、S44、S50、S70、S80、S90、S99 共14页；优先横向16:9／3:2，保留旧3:4提示词作为生成兼容输入。
- Reason: 角色用于持续 VTuber 插画和设定生产，需要将主视觉、比例、脸部、手势、服装、材质、头发、演出、变体和一致性 QA 拆成单一目的页面。
- Scope: character-bible / production-spec

## 2026-07-29T00:00:00+00:00 — 插画路由与批次问答分离

- Decision: 以 `interview/ROUTING.md` 保存 portrait、poster、narrative_scene、action_keyframe、daily_interaction、environment、material_showcase、character_sheet、series 九类路由；B0–B5 保持一批一答一记录，按类型动态替换 B2/B3 问题。
- Reason: 用户需要精准澄清不同场景与风格，同时保留创作自由；锁定层、引导层和创作槽位分离可以避免风格或构图误写入角色 canon。
- Scope: interview / illustration-director
