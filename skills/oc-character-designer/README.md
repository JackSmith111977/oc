# OC Character Designer Skill Package v3.1.2

将模糊 OC 概念转化为可持续维护的角色根本、强参考、批准变体和横向设定集。

## 当前合同

- Package: `3.1.2`
- Canon schema: `3.1`
- Workspace format: `1.1`
- Question/answer batch: `1.0`
- Character-bible template: `1.1.0`
- Downstream: `oc-illustration-director >=2.0.0,<3.0.0`

## 核心命令

```bash
python scripts/oc_workspace.py init ./characters/my-oc --name "My OC"
python scripts/oc_workspace.py queue-batch ./characters/my-oc --file S2-B01.questions.json
python scripts/oc_workspace.py commit-batch ./characters/my-oc --file S2-B01.answers.json --dry-run
python scripts/oc_workspace.py commit-batch ./characters/my-oc --file S2-B01.answers.json
python scripts/oc_workspace.py validate ./characters/my-oc
```

`canon/canon.json` 是唯一角色事实源。`INDEX.md`、章节和 `ACTIVE_CONTEXT.md` 都可由脚本重建。
