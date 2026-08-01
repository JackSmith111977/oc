# 40-costume-color · 服装、道具与色材

> 服装构造、附件、配色和材质

- Canon revision: 65
- Updated: 2026-07-28T14:43:13+00:00

## Structured canon

### accessories and props

`visual_canon.accessories_and_props`

- {"name": "古董金色椭圆框眼镜", "attachment": "面部", "state_logic": "白天／宅家／程序员状态佩戴；正式直播／贵族状态摘下"}
- {"name": "黑色丝带颈饰", "attachment": "绕过颈部并在颈部中央形成稳定固定点"}
- {"name": "新月荆棘蝙蝠徽", "attachment": "固定在黑色丝带中央", "composition": ["旧金色新月外框", "黑紫色展开双翼蝙蝠", "翼根与躯干缠绕的荆棘", "暗红蔷薇", "暗红宝石"], "identity_rule": "五个组成部分必须作为一个不可拆散的整体，不能改成普通项链"}

### costume construction

`visual_canon.costume_construction`

```json
{
  "primary_outfit": "完整三层黑紫哥特萝莉正式长裙",
  "silhouette": "上窄下丰；长发与蓬松裙摆构成纵向主轮廓",
  "bodice": {
    "construction": "紧身胸衣、方领、少量露出锁骨、泡袖、蝴蝶结与层叠蕾丝",
    "front": "正面保持整洁，不显示背部闭合结构",
    "back_closure": {
      "type": "古典背部交叉系带",
      "must_show": [
        "系带穿孔",
        "左右交叉路径",
        "腰部收紧区域",
        "系带末端",
        "下方蝴蝶结"
      ],
      "forbidden_substitutes": [
        "前襟暗扣",
        "侧面拉链"
      ],
      "visibility": "背面视图与服装拆解图中必须清晰可读，不能被长发遮挡"
    }
  },
  "skirt_layers": {
    "count": 3,
    "inner": "支撑蓬松轮廓",
    "middle": "提供裙体体积",
    "outer": "以蕾丝与装饰边收束层次",
    "qa": "不得合并为单层，后侧三层高度与体积关系须可读"
  },
  "footwear_and_socks": "黑色玛丽珍鞋＋白色蕾丝长袜",
  "formal_outfit": "直播／贵族状态使用完整三层黑紫哥特萝莉正式长裙，摘下眼镜",
  "daytime_work_outfit": "仅在明确要求白天工作／宅家变体时使用：宽松衬衫＋针织外套＋简化长裙；不替代正式服 canon"
}
```

### materials

`visual_canon.materials`

蕾丝、黑色丝带、洋装面料、少量旧金属与暗红宝石；以清晰平涂和少量中性材质色块表达，不把磨损程度、污渍或特殊光泽锁成不可变设定。

### palette

`visual_canon.palette`

正式服主色比例固定为黑紫70％、暗红20％、旧金10％；黑紫覆盖主要裙装与胸衣结构，暗红集中于内衬、蔷薇与宝石，旧金仅用于家徽、扣饰和细边点缀。

## User notes

<!-- USER NOTES START -->

<!-- USER NOTES END -->
