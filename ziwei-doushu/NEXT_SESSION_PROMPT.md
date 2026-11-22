# 见微 Ziwei Lab · 结合 ziwei-doushu 开源经验的完整工作规划（本机会话提示词）

> 用法：在 Mac 上进入 `/Users/andyfang/jianwei-ziwei-lab` 开新会话。**先粘贴你的《Claude Code 项目接手提示词：见微 Ziwei Lab》全文，再粘贴本文件分隔线以下的全部内容。**
> 交接提示词描述本机项目现状和硬性边界；本文件给出这一轮要做的事。两者冲突时，以交接提示词和 `AGENTS.md` 为准。

---

# 本轮工作规划

上面的交接提示词说「先确认我接下来给出的具体目标」——**具体目标就是本文件**。读完必读文档、核对完 Git 状态后，直接从 Sprint 0 开始做，不需要再问我要不要开始。

## 一、为什么做这一轮

GitHub 上有一个和见微同类的开源项目 **ziwei-doushu**（https://github.com/Renhuai123/ziwei-doushu），同样基于 iztro 2.5.x，并且已经做成了线上商业站。它在下面几件事上积累了可以直接借鉴的经验：

1. 把排盘引擎「边界不出错」做成成套的回归测试；
2. 把格局识别做成有出处、有可达性统计的规则库；
3. 整理了公有领域的古籍原文；
4. 把专业断语写成大众看得懂的白话结构。

这一轮的目标是：在**不破坏见微现有边界**的前提下，把这些经验落到见微里，让见微的排盘更可信、解读证据更丰富、内容更易懂，同时把合规补齐。

## 二、已核实的 ziwei-doushu 事实（2026-11-21 clone 并实测，可直接引用；用到细节时请再次以仓库为准）

**许可**（README §九、`LICENSE`、`DATASET-LICENSE`）：

| 内容 | 协议 | 对见微的含义 |
|---|---|---|
| 代码 `lib/` `app/` `components/` | MIT | 可以借鉴或移植，但移植的文件要保留原版权声明，并登记到 `THIRD_PARTY_NOTICES`（没有就新建） |
| 古籍原文 `lib/classics/`（《骨髓赋》`gusuifu.ts`、《紫微斗数全集》`quanji.ts`、《紫微斗数全书》`quanshu.ts`） | 公有领域 | 可以用，建议仍注明来源 |
| v3.0 / v4.0 解读数据集（Releases） | CC BY 4.0 | **见微不用**：它不是见微引擎产生的 evidence，违反「AI 只解释 evidence」 |
| `docs/tianji-ziwei/`、`research/` 及数据集里引用的倪海厦原话 | CC BY-NC-SA 4.0 / 不在授权内 | **禁止进入见微**（v4 数据集平均每张盘约 44 处引用） |

**引擎文件**（`lib/ziwei/`，共约 6,800 行）：
- `algorithm.ts`：`generateChart()`，676 行。对非法时辰、非法性别、不存在的公历日期都直接抛 `RangeError`。
- `patterns.ts`：1,192 行格局库，`detectPatterns(chart)` 返回识别出的格局；另有 `patterns-dingfu/dinggui/dingpin/dingza.ts` 四个分卷。
- 时间处理：`true-solar-time.ts`（经度差 + 均时差）、`dst-cn.ts`（1986–1991 夏令时只判定、不自动扣）、`clock-adjust.ts`。
- 盘面细节：`school-data.ts` 和 `school-tables.generated.ts`（星曜亮度 7 档，按流派查表，**不用 iztro 自带亮度**）、`shier-shen.ts`（十二神煞，本命按生年支，流年按流年支）、`yunxian-context.ts`（含童限）。
- 历法：`lunar-solar.ts`，闰月有 4 种口径，默认「月中分界 split」。

**回归测试**（`scripts/regression/*.test.ts`，`npm test` 全部通过）：
- 排盘与输入：紫微安星铁律（768 盘）、`dst-cn`、`clock-adjust`、`chart-entry`；
- 历法与时间边界：`sizhu-lichun-boundary`（立春四柱）、`iztro-time-index-boundary`（时辰序号 0–11）、`solar-date-exists`（不存在的日期）、`leap-policy-validation`、`form-true-solar-day`、`form-equation-of-time`；
- 星曜与四化：`hongluan-tianxi`、`natal-dual-sihua-same-palace`（同宫双四化）、`shier-shen`、`palace-minor-stars`；
- 格局：`patterns-sihua-bonus`、`patterns-dinggui/dingfu/dingpin/dingza`，会统计每条格局「可实现 / 存疑 / 无解」以及实测出现率；
- 其他：`gender-validation`、`famous-hour-consistency`、`neutral-naming`。

**实测**：
- 单盘约 70 ms。
- 在 tsx 下直接 import `patterns.ts` 会因为 `import 'server-only'` 报错，需要在你的临时目录里给 `server-only` 写个空模块。
- 用 v4 数据集的 1995 年分卷抽 600 张盘，引擎重排后命宫主星 600/600 一致。

**它踩过的坑（见微要防）**：
- v3 数据集每个月都生成了 1–30 日，iztro 遇到 2 月 30 日不报错，而是顺延排盘，结果出了 2,520 张重复的错误盘；
- 时辰序号（0–11）经常被误当成钟点（0–23）；
- 晚子时 23:00–23:59 要按次日排；
- 数据集按固定东经 120° 生成，没做真太阳时校正。

**它的白话写法（只借鉴结构，不复制文字）**：每个主题都是 `白话总览 → 一句话定调 → 核心论断 → 命盘依据（本宫 + 三方四正） → 可执行的小建议`。例如结尾会给「每周挑一件小事，故意按别人的办法做一次」这种具体动作，而不是空泛的吉凶。

## 三、执行规则（在交接提示词的规则之上补充）

- **自主推进**：按 Sprint 顺序连续做，每个 Sprint 结束写一段简短汇报（改了什么、测试实际结果、截图位置、遗留问题），然后**直接进入下一个**。
- **只在这些情况停下来等我回复**：
  1. 需要改冻结模块（排盘、历法、AI、安全、关系）。先按 `AGENTS.md` 五项门禁准备好「复现样本 + 失败测试 + 根因 + 拟改 diff」，再停下来问我；
  2. 需要 push、部署或发布 Sites；
  3. 需要我做业务决定（文中标了 🟡 的地方）；
  4. 发现工作区有不属于本轮的修改，或者 Git 状态与交接说明不一致。
- **分支**：每个 Sprint 一个分支，从上一个 Sprint 的分支切出；在本 Sprint 分支上提交，不合并到别的分支、不 push。
- **ziwei-doushu 只用作参考**：clone 到项目外的 `~/tmp/ziwei-doushu`（`git clone --depth 1`），只在那里跑它的代码。见微仓库里不出现它的数据集、倪海厦原话，也不出现未登记许可的整段代码。
- 测试样本一律用合成日期，不出现真实的人。

---

## Sprint 0 · 接手核对与交接刷新（分支 `sprint/handoff-refresh`）

1. 运行 `git status --short --branch`、`git branch --show-current`、`git log -1 --oneline`、`node -v`。和交接说明（`sprint/plain-language-copy` / `c99bca3` / 工作区干净）不一致就停下来。
2. 运行 `npm test`、`npm run lint`、`npm run typecheck`、`npm run test:dev-runtime`，记录通过数、失败数、耗时，和 2026-09-27 的历史结果（194 / 41 / 1）对比；同时记录 `IMPORT_IS_UNDEFINED` 提示还在不在。**基线有失败就先停下来汇报**，不要在红的基线上继续开发。
3. 只读检查线上：`curl -sS https://jianwei.andyterminal.com/api/health`，判断线上版本是否落后于本地。
4. 对照代码核实：版本号、preset、模型和生成参数（temperature 0.3、700 tokens、约 6 秒超时、重试 1 次、缓存 24 小时）、Binding、迁移文件、scripts。
5. 更新 `docs/HANDOFF.md`：写入核实过的事实和「最后核对日期」，查不到的写「未核实」，然后提交。

**验收**：HANDOFF 里没有过期的分支、提交或测试数字；汇报里附上对照表。

## Sprint 1 · 引擎边界回归加固（分支 `sprint/engine-regression`）

**只新增测试，不改引擎。** 测试放在 `tests/` 里，复用现有的组织方式。

先把 ziwei-doushu 的测试主题逐条映射到见微现有测试，写进 `docs/research/engine-regression-coverage.md`，列出「已有（给路径）/ 缺失」。然后为缺失项补测试，至少覆盖：

| 测试 | 断言 |
|---|---|
| 不变量（≥ 300 张合成盘，覆盖两个 preset） | 14 主星各出现且只出现一次；紫微、天府位置满足固定对称关系；12 宫地支各不相同；命宫、身宫唯一；生年四化 4 颗且属于本年干对应的星；同一输入两次排盘的 `chartFingerprint` 相同 |
| 不存在的日期 | 2 月 30 日、非闰年 2 月 29 日、4 月 31 日都必须被拒绝，不能顺延成别的日期 |
| 时辰边界 | 钟点和时辰序号的换算；22:59、23:00、23:59、00:00、00:59、01:00 各自归到哪个时辰、排哪一天 |
| 晚子时 / 早子时 | 23:30 和次日 00:30 的盘符合 `docs/ziwei-rule-spec.md` 的口径 |
| 中国夏令时 1986–1991 | 区间内的输入是否被识别和提示；不允许被悄悄扣掉 1 小时（按见微的规格断言） |
| 立春交节 | 立春时刻前后 1 分钟的年干、生年四化 |
| 闰月 | 每种已支持的口径各有一个闰月样本，口径要和 preset 声明一致 |
| 同宫双四化 | 同一宫出现两个四化时，结构化输出不丢失、不重复 |
| 性别 / 非法输入 | 非法值被拒绝，不允许默认按某一性别排盘 |
| 真太阳时 | 东西两端城市各一例，跨日的情况单独一例 |

- **全部通过**：提交，汇报覆盖率的提升。
- **有测试失败**：说明发现了真实缺陷。不要改引擎，也不要改测试去迁就。把失败测试标成预期失败（按仓库现有写法，比如 `todo` 或 `skip` 加原因），写出复现样本和根因分析，然后**停下来，按门禁请我批准修复**。

## Sprint 2 · 跨引擎交叉校验工具（分支 `sprint/cross-check`）

目的是用第二个独立实现给见微做对照，把差异找出来并归类。不是让两边结果必须一样。

1. 在 `~/tmp/ziwei-doushu` 里运行 `npm install`，再给 `server-only` 写个空模块。先确认它的 lockfile 锁定的 iztro 版本；如果不是 2.5.8，在报告里写明，差异归因时要考虑进去。
2. 在见微里新增 `scripts/cross-check/`，只用于开发，不进生产 bundle，也不进 `npm test`。脚本做这几件事：
   - 生成确定性的合成输入，覆盖 1950–2030 年、12 个时辰、男女，并刻意加入闰月、立春前后、晚子时样本，至少 2,000 例；
   - 用见微 `packages/ziwei-engine` 的两个 preset 分别排盘；
   - 通过子进程调用 `~/tmp/ziwei-doushu` 的 `generateChart`（只在本地执行，不把它的代码复制进见微）；
   - 对比命宫地支、身宫地支、五行局、14 主星所在地支、生年四化、各宫干，输出 `artifacts/cross-check/report.json` 和 `summary.md`（只含合成输入）。
3. 把差异归类：亮度口径、闰月口径、晚子时口径、其他。「其他」类必须逐条给出样本，判断是不是见微的缺陷。
4. 写 `docs/research/ziwei-doushu-cross-check.md`：方法、差异统计、每类差异的结论，以及哪些差异需要在 UI 的「流派对照」里展示给用户。

**验收**：脚本能一条命令重跑；不属于已知口径差异的不一致为 0，或者已经逐条列出并转成 Sprint 1 风格的失败测试（转成测试就意味着进入门禁，要停下来问我）。

## Sprint 3 · 格局识别作为新的 evidence 类型（分支 `sprint/patterns-evidence`）🔒 涉及冻结模块

见微现在的 evidence 是否包含「格局」，先在汇报里说明。ziwei-doushu 的经验是：格局是用户最容易感知的「命盘特点」，适合放进解读。

**3a. 先做方案，不改冻结模块，写进 `docs/research/patterns-proposal.md`：**
- 选出**第一批 15–25 个经典格局**。要求出处在《紫微斗数全书》《骨髓赋》等公有领域古籍里能找到原句；在 Sprint 2 的样本里实测出现率不为 0；判定条件不依赖存在争议的口径。
- 每个格局写清：判定条件（宫位、星曜、四化、三方四正、亮度要求）、古籍出处原句、ziwei-doushu 对应的规则（如果参考了），以及在两个 preset 下的结果是否一致。
- 架构：新建一个**只读消费引擎输出**的模块（例如 `src/modules/chart/patterns/`），不改 `packages/ziwei-engine` 的排盘逻辑。规则独立版本号，例如 `JIANWEI-PATTERNS-0.1.0`，并写入 `ruleSnapshot`。
- 接入点：命盘页展示格局卡片（含出处和判定依据），问盘 evidence 增加 `patterns[]`。后者会改 `lib/ai/` 的 evidence 结构和输出校验，**属于冻结模块**。
- 许可：如果移植了 ziwei-doushu 的判定代码，文件头保留 MIT 声明，并登记到 `THIRD_PARTY_NOTICES`。

**3b. 停下来**，把方案、预计 diff 范围和测试计划发给我，等我批准。

**3c. 批准后按 TDD 实现**：
- 先写测试：每个格局至少 1 个正例和 1 个反例（合成盘）；
- 再实现识别模块和 UI；
- 最后接入 evidence。AI 输出校验要保证：AI 提到的格局必须在 `patterns[]` 里，否则拦截；
- 跑全量验收，并提供 390px 和 1440px 截图。

## Sprint 4 · 公版古籍与白话学习内容（分支 `sprint/classics-content`）

这里的改动都在 `data/` 和展示组件，不涉及冻结模块。

1. 从 `~/tmp/ziwei-doushu/lib/classics/` 取《骨髓赋》全文，以及《全书》中与 14 主星和 Sprint 3 格局相关的段落，放进 `data/classics/`。
   - 每段标注出处（书名、卷、篇），注明「公有领域」，并加一份来源说明；
   - 入库前用脚本断言：不得含「倪海厦」「天纪」「倪师」以及任何视频时间码；
   - 逐段核对文字，有明显错字的标注出来，不要擅自改。
2. 在 `/knowledge` 的词条和 `/learn` 的课程里，按需展开显示「古籍原文」和人工撰写的「白话说明」。白话说明必须自己写，不得从 ziwei-doushu 的数据集或线上站复制。
3. 学习 ziwei-doushu 的白话结构，给 14 主星词条统一成：`一句话定调 → 白话说明 → 盘面依据看什么 → 生活里可以怎么做（具体动作）→ 古籍原文（折叠）`。先做 14 主星，其余词条在汇报里列为后续任务。
4. 保持「近期文案方向」：首屏不放方法论，技术依据放进折叠说明。

**验收**：内容测试（出处字段齐全、禁词断言通过）、页面结构测试、390px 和 1440px 截图。

## Sprint 5 · 合规与安全表达（分支 `sprint/compliance`）

1. 写 `docs/research/compliance-checklist.md`，每条标 ✅ / ❌，附代码位置：
   - **AI 内容标识**：《人工智能生成合成内容标识办法》2025-09-01 起施行，要求用户能直接看到的显式标识。检查 AI、缓存、本地降级三种状态在答案区、导出、分享、关系报告里是否都标示清楚；
   - **免责声明**：「文化学习 / 仅供参考，不构成预测或建议」覆盖了哪些页面；
   - **禁用表达**：`data/` 文案和 AI 输出校验能否拦截：转运、改运、化解、招财、旺财、逢凶化吉、注定、必然，以及疾病诊断、寿命、灾祸、离婚类结论；
   - **健康和六亲**：疾厄、父母、子女、兄弟相关内容怎么展示。ziwei-doushu 作者自己也承认六亲判断局限大，所以见微应该有降级提示或不展开；
   - **隐私**：模型请求、服务端日志、analytics、D1 的字段审查（只审代码路径，不用真实数据）；
   - **密钥**：检查 `npm test` 已经产生的构建产物里有没有密钥或 Binding 泄露；
   - **关系邀请**：每条约束都有对应测试；
   - **第三方许可**：iztro、lunar-javascript 以及本轮新增引用的许可是否都已登记；
   - **截图**：`artifacts/screenshots/` 和 `public/screenshots/` 里哪些明显旧于当前 UI。
2. 修复：
   - 只涉及 `data/`、`components/`、文案和截图的 ❌，直接按 TDD 修；
   - 涉及 `lib/ai/` 输出校验或其他冻结模块的 ❌，准备门禁材料后停下来问我。
3. 更新过期截图（390px 和 1440px）。

## Sprint 6 · 引流与分享（分支 `sprint/share-card`）🟡 需要我先做业务决定

ziwei-doushu 有分享卡片（`ShareCardCanvas.tsx`）；之前的规划里也提过「免费关键词卡片 → 小红书引流」。见微没有支付和账户系统，交接规则也不允许用 mock 冒充。所以：

- 先写 `docs/research/share-card-proposal.md`：竖版 3:4 分享卡片。内容只用确定性 evidence，比如命宫主星、格局、本年流年重点关键词。
  - 不含任何出生资料、不含缘分百分比和宿命标签；
  - 如果文字由 AI 生成，要带 AI 标识和免责声明；
  - 卡片上的二维码或链接不携带可还原生辰的参数。
- **停下来问我**：要不要做、放在哪个页面、是否面向小红书、文案语气。我确认后再按 TDD 实现。
- **不做**支付、订单、会员这类假功能。

---

## 收尾（所有 Sprint 完成或停在门禁时）

1. 更新 `docs/HANDOFF.md`：写清本轮新增的分支、测试数、规则或版本变化、新增文档和已知限制。
2. 输出最终汇报：
   - 每个 Sprint 的状态（完成 / 停在门禁 / 未开始）；
   - 测试实际结果；
   - 截图位置；
   - 交叉校验结论；
   - 等我决定的事项清单；
   - 「下一轮候选任务」：按 P0 / P1 / P2 排序，标明是否触发冻结门禁。
3. 提醒我哪些分支需要 push 或合并、是否需要部署。不要自己执行。
