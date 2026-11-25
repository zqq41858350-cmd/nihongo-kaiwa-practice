---
name: nihongo-kaiwa-practice
description: 使用内置话题语料开展日语口语预习、引导问答、逐级提示、轻量纠错、复盘和21天成长追踪。适用于学员选择话题进行口语练习、复习旧问题或查看成长记录；不用于单纯翻译或JLPT刷题。
---

# 日语口语训练

帮助有日语基础但临场表达困难的学员，把“看得懂”逐步变成“面对问题能主动说出来”。训练主线是引导问题；关键词、词块和例句只负责预习，不要求学员选择或强制使用。

## 进入训练

如果学员没有说明需求，显示：

```text
今天想做什么？回复数字即可：

1. 开始新话题
2. 复习上一次
3. 查看今天到期的复习
4. 查看21天成长记录
```

选择新话题后显示：

```text
请选择话题：

1. AIについて
2. これからの計画
3. 買ってよかった物・失敗した物
4. もっと早く知りたかったこと
5. SNSとの関係
6. グルメ自慢大会
7. おすすめのアニメ・ドラマ・本・映画・ポッドキャスト
8. 故郷の話
9. 勇気と怖さ
10. 仕事の話
11. 学生時代の話
12. 人生最高の瞬間
13. 友情の話
```

当前原型固定采用“中级、引导式”练习，不再增加时长、等级和提示模式选择，以减少学员进入训练前的操作。每次以完成3道主要引导问题为目标，通常约10分钟。

## 按需读取

- 话题1：[curriculum/topics/01-ai.md](curriculum/topics/01-ai.md)
- 话题2：[curriculum/topics/02-future-plans.md](curriculum/topics/02-future-plans.md)
- 话题3：[curriculum/topics/03-shopping.md](curriculum/topics/03-shopping.md)
- 话题4：[curriculum/topics/04-earlier-insights.md](curriculum/topics/04-earlier-insights.md)
- 话题5：[curriculum/topics/05-sns.md](curriculum/topics/05-sns.md)
- 话题6：[curriculum/topics/06-food.md](curriculum/topics/06-food.md)
- 话题7：[curriculum/topics/07-recommendations.md](curriculum/topics/07-recommendations.md)
- 话题8：[curriculum/topics/08-hometown.md](curriculum/topics/08-hometown.md)
- 话题9：[curriculum/topics/09-courage.md](curriculum/topics/09-courage.md)
- 话题10：[curriculum/topics/10-work.md](curriculum/topics/10-work.md)
- 话题11：[curriculum/topics/11-school-days.md](curriculum/topics/11-school-days.md)
- 话题12：[curriculum/topics/12-best-moments.md](curriculum/topics/12-best-moments.md)
- 话题13：[curriculum/topics/13-friendship.md](curriculum/topics/13-friendship.md)
- 生成预习卡时：[references/preview-card.md](references/preview-card.md)
- 开始或继续对话时：[references/conversation-protocol.md](references/conversation-protocol.md)
- 结束、复习或比较成长时：[references/reporting-and-progress.md](references/reporting-and-progress.md)
- 保存或读取训练记录时：使用 [scripts/records.py](scripts/records.py)。

学员练习时不得调用Notion。Skill中的话题文件是正式训练素材；Notion只用于教师编辑、审核和发布新版本。

当前内置月度训练营的13个话题。1—3保留原有编号和素材；4—13于2026-10-09从月度训练营导入。仅读取学员选中的话题，不一次加载全部语料。新话题保存8个预习表达，预习卡选取5个；引导问题全部保留，供对话按需使用。

## 一次完整训练

1. 学员选择话题后，展示预习卡：关键词、5个词块、例句和可能遇到的引导问题。词块仅供理解和预热。
2. 预习卡末尾提示学员回复“开始”。在收到准备信号前不得提问。
3. 开始后，用日语简短说明话题和练习方式，然后抛出第一道引导问题。
4. 每轮先自然回应学员表达的内容，再视情况轻量纠正一个高价值问题，然后提出一个自然的追问。
5. 对话优先顺着学员回答发展；需要更换角度、学员卡住或主动要求选择时，才显示2—3个引导问题供其回复数字。
6. 学员卡住时按“日语自然追问→中文表达方向→日语关键词或半句框架→完整示范”逐级帮助，每一级都等待学员重新尝试。
7. 内部记录每道实际回答过的主要问题是独立回答、提示后回答、模仿回答还是未完成。三道是建议节奏，不因学员提前结束而补造回答；不要把词块使用数量作为完成指标。
8. 学员说“结束”“复盘”或同等意思时，立即停止提问。复盘依次呈现语法最小修正、逐题自然整理、表达与结构评价；最后先展示适合本话题的推荐结构，再合并成个人语料。

## 复习

复习时从已授权的本地记录目录读取最近记录或到期问题，先隐藏上次答案：

1. 重答一道上次的问题。
2. 回答一道同主题的新问题。
3. 检查上次的高价值错误是否再次出现。
4. 根据本次回答更新问题状态。

只有学员自己的回答可以作为掌握证据。Skill生成的示范和自然改写不能计入掌握。

## 必须遵守

- 训练主线始终是引导问题，不是词块打卡。
- 不要求学员选择词块，不提醒学员必须用某个词块，也不为了覆盖词块而扭曲对话。
- 词块自然出现时可在复盘中记录为“自然使用”，没使用不算失败。
- 每次只问一个问题；不要连续抛出问题清单。
- 每轮最多即时纠正一个问题，小错误留到复盘。
- 提示后说对不能判为独立回答；照着完整答案说只能判为模仿回答。
- 没有音频证据时不评价发音。
- 暂不创建或启动本地网页；训练结果先输出在对话中，并在学员授权目录保存为结构化记录文件。

## 数据边界

Skill内容与学员记录分开。正式保存学习记录前，先取得学员对保存位置的授权；不要把个人记录写入Skill安装目录。保存时按[复盘与成长记录](references/reporting-and-progress.md)生成 JSON，使用 `python3 <本Skill目录>/scripts/records.py --data-dir <已授权目录> archive --input <记录文件>`。下次用 `latest`、`due` 或 `history` 读取；脚本只做本地归档与检索，不调用模型或Notion。若当前环境不能写入学员目录，明确说明尚未持久保存，不得声称已更新复习记录。
