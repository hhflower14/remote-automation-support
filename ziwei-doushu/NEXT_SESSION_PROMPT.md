# 新会话提示词 · 接手「见微 Ziwei Lab」

> 用法：在你 Mac 上的 `/Users/andyfang/jianwei-ziwei-lab` 目录开新会话（Claude 桌面应用，或终端里 `claude`），把下面分隔线以下的全部内容粘贴进去。
> 带 ⚠️ 的地方是你上次消息被截断、我不知道的内容，粘贴前请补上或删掉。

---

你正在接手「见微 Ziwei Lab」项目。这是一个紫微斗数教学、确定性排盘、今日节律、关系互动和证据约束解读网站，已经是可以部署的全栈 Demo。

- 项目路径：/Users/andyfang/jianwei-ziwei-lab
- 公开体验站：https://jianwei.andyterminal.com
- ChatGPT Site：https://jianwei-ziwei-lab.andyzjenergy.chatgpt.site
- 预期分支：sprint/plain-language-copy
- 预期提交：c99bca3 refactor(ui): replace methodology copy with user tasks

## 工作方式（全程遵守）

- 按下面的阶段顺序做，**每个阶段结束停下来向我汇报，等我确认再进入下一阶段**。
- 汇报只写核对过的事实。没跑的命令、读不到的文件，直接说没跑、读不到，不要推测结果。
- 阶段 0 和阶段 2、3 只读，不改代码。只有阶段 1 改文档。
- 不 push、不部署、不改 Cloudflare / D1 配置，除非我明确说可以。
- 不新增依赖，不升级 Iztro 或其他依赖。

## 硬性边界（来自交接说明，优先级高于一切优化建议）

- 当前版本：引擎 `iztro@2.5.8+jianwei-adapter@0.6.1`，规则 `JIANWEI-ZIWEI-RULES-0.5.1`，预设 `sanhe-iztro-default`、`zhongzhou-iztro-2.5.8`。
- AI 不参与历法、命宫身宫、宫干、五行局、安星、四化或任何排盘计算。
- 真实排盘只能走 `packages/ziwei-engine`，业务页面不得直接调用 Iztro。
- AI 只能把传入的匿名结构化 evidence 转成文字，不得补造 evidence 里没有的星曜、宫位、四化和时间。
- 不得把真实个人出生资料写进测试 fixtures、日志、analytics 或提交信息。需要样本时只用合成日期。
- 不新增八字、塔罗、星座等其他体系。
- 不用更好看的 mock 绕过算法或后端问题。首页示例盘和案例合成盘可以保留，但必须明确标识，并和真实排盘隔离。
- 核心排盘、历法、AI、安全、关系模块处于受控冻结。要改的话，先按 AGENTS.md 提供：真实复现样本、失败的回归测试、根因分析、最小改动、完整验收。
- 生产环境的 AI、D1 和加密密钥只能在服务端，不得出现在客户端 bundle。`.env.example` 只放占位符。禁止提交真实密钥，也不要复用历史聊天里出现过的 NVIDIA 或其他 API key。
- 关系邀请必须保持：双方分别授权；共享证据用 AES-GCM 加密存 D1；token 和撤回凭据只存哈希；24 小时过期；任一方可撤回；撤回或过期后清理加密负载和共享报告；负载不含原始出生信息；不输出缘分百分比或宿命化人格标签。
- 模型请求里不得出现姓名、完整出生日期、出生地点、手机号、用户 ID、IP。

## 架构速览（交接说明，待阶段 0 核实）

- React 19、TypeScript 5、Next.js App Router 兼容；用 vinext、Vite 和 Cloudflare Vite Plugin 构建，部署到 Cloudflare Workers；Node.js >= 22.13.0。
- `packages/ziwei-engine` 统一封装 Iztro 2.5.8；`packages/lunar-lite-exact` 和 `lunar-javascript` 负责历法和交节边界。
- Workers AI：服务端 Binding `AI`，模型 `@cf/qwen/qwen3-30b-a3b-fp8`。D1：Binding `DB`，用于匿名反馈、关系邀请、AI 解释缓存和限流。
- 页面：`/` `/today` `/chart` `/ask` `/relationship` `/learn` `/cases` `/knowledge` `/profile` `/invite/[token]`。
- API：`GET /api/health`、`POST /api/interpret`（主 AI 接口）、`POST /api/ask`、`POST /api/feedback`、`POST /api/relationships`、`GET/POST /api/invites/[token]`、`POST /api/invites/[token]/revoke`。
- 问盘链路：`components/AskExperience.tsx` → `/api/interpret` → `lib/ai/` → Workers AI。超时、模型繁忙、JSON 错误时降级为本地证据答案；页面要如实区分模型、缓存和本地答案；现在还不是真正逐 token 流式输出。
- 关键目录：`app/` `components/` `packages/ziwei-engine/` `packages/lunar-lite-exact/` `src/modules/{chart,almanac,ask,relationship,learning}/` `lib/ai/` `data/` `testing-fixtures/` `migrations/` `tests/`。

⚠️ 交接说明在「测试与部署命令」处被截断。目前已知的命令只有：`npm install`、`npm run dev`、`npm test`、`npm run lint`、`npm run typecheck`、`npm run test:dev-runtime`。部署命令和其余内容以 `package.json`、AGENTS.md 为准，不要猜。

---

## 阶段 0：只读核对（不改任何文件）

1. 依次阅读：
   - `AGENTS.md`
   - `docs/HANDOFF.md`（最后更新于 2026-09-24，分支、提交、测试计数和 Sites 版本已经过时）
   - `docs/ziwei-rule-spec.md`
   - 原始 PRD：`/Users/andyfang/Library/Containers/com.tencent.qq/Data/Downloads/Jianwei-Ziwei-Lab-PRD(1).md`。读不到就直接说读不到，不要猜它写了什么。
2. 运行并贴出原始输出：
   - `git status --short`
   - `git branch --show-current`
   - `git log -1 --oneline`
   - `node -v`
3. 如果没有 `node_modules`，先运行 `npm install`（不要改 lockfile；如果 lockfile 被改了，告诉我）。然后依次运行，记录每项的通过数、失败数和耗时：
   - `npm test`
   - `npm run lint`
   - `npm run typecheck`
   - `npm run test:dev-runtime`
4. 不跑网络请求的前提下，核对代码里的这些值和交接说明是否一致：引擎和规则版本号、两个预设名、Workers AI 模型名、D1 / AI Binding 名（看 wrangler 配置）、Node 版本要求。
5. 列出 `package.json` 里所有 scripts，特别标出部署相关的（只列，不执行）。

**阶段 0 汇报格式**：
- 一张表：交接说明写的 vs 实际看到的 vs 是否一致；
- 测试结果表；
- AGENTS.md 里规定的修改流程和冻结范围（摘要）；
- PRD 能否读到，能读到就给出它和当前实现的主要差异（最多 10 条）；
- 发现的异常或风险。

## 阶段 1：更新交接文档（等我确认后再做）

- 只改 `docs/HANDOFF.md`：把分支、提交、测试计数、版本号、页面和 API 列表更新成阶段 0 核实过的事实，并写上「最后核对日期」。
- Sites 版本、线上部署版本如果本地查不到，就写「未核实」，不要编。
- 在当前分支单独做一个文档提交，提交信息里不要出现任何出生资料。先给我看 diff，我同意后再提交；不要 push。

## 阶段 2：对照开源项目 ziwei-doushu 做差距评估（只读，产出报告）

参考项目：https://github.com/Renhuai123/ziwei-doushu（代码 MIT；数据集 CC BY 4.0，必须标注来源；`docs/tianji-ziwei/` 下的倪海厦原话是 CC BY-NC-SA 4.0，不能商用）。它和见微一样基于 iztro 2.5.x，已有一套回归测试可以拿来对照。

请 clone 到项目目录之外（例如 `~/tmp/ziwei-doushu`），不要把它的代码或数据复制进见微仓库，然后在见微里写报告 `docs/research/ziwei-doushu-gap.md`，包含：

1. **回归测试覆盖对照**。对方的测试主题有：紫微安星铁律（768 盘）、1986–1991 中国夏令时、钟表时间平移、晚子时 / 早子时换日、立春四柱边界、红鸾天喜、iztro 时辰序号 0–11 边界、不存在的公历日期（2 月 30 日等）、性别校验、同宫双四化、闰月口径、真太阳时和均时差、十二神煞。逐项写见微是否已有对应测试（给出测试文件路径），没有的写建议新增的测试，样本只用合成日期。
2. **口径差异**。重点看：星曜亮度（对方不用 iztro 自带的亮度，而是自建流派表）、闰月归属（对方默认「月中分界」split）、晚子时换日策略、真太阳时。逐项说明见微当前用的是哪种口径、写在哪里，以及差异会不会让同一个输入排出不同的盘。
3. **交叉校验建议**。设计一个只在本地跑的脚本方案：用合成日期批量对比两边的命宫、身宫、五行局、十四主星位置和生年四化，输出差异统计。这一阶段只写方案，不实现。
4. **可借鉴但受冻结约束的点**。例如对方 `patterns.ts` 的格局规则库能不能作为见微 evidence 的来源。每一条都要说明会碰到哪个冻结模块、需要走 AGENTS.md 的哪些步骤。
5. **不建议采用的点**，并写明原因。至少包括：
   - 对方的 v4.0 解读数据集不是见微引擎产生的 evidence，不能喂给 AI 当证据；
   - 数据集里每张盘平均有约 44 处倪海厦原话引用，不能商用；
   - 数据集里的健康、六亲类断语不适合直接展示。

## 阶段 3：上线与合规自查（只读，产出清单）

写 `docs/research/compliance-checklist.md`，逐条标注 ✅ / ❌ / 未确认，并给出代码位置：

- AI 生成内容是否有用户一眼能看到的显式标识（《人工智能生成合成内容标识办法》2025-09-01 起施行），包括分享内容；
- 是否有「文化学习 / 娱乐参考，不构成预测或建议」类声明，以及出现在哪些页面；
- 文案和 AI 输出里有没有：转运、改运、化解、招财、旺财、逢凶化吉、注定、必然，以及疾病、寿命、灾祸、离婚类结论；`lib/ai/` 的输出校验有没有拦截这些；
- 健康、父母、子女类内容的展示方式；
- 出生资料是否只存在本地；模型请求、日志和 analytics 里是否可能混入敏感字段（抽查代码路径，不要用真实数据测试）；
- 客户端 bundle 里有没有密钥或服务端 Binding 泄露（构建后搜索产物；只有当构建命令不会触发部署时才执行，拿不准就先问我）；
- 关系邀请的 9 条约束是否都有对应测试；
- 用到第三方开源代码或数据的地方，是否保留了许可声明和来源标注。

每个阶段完成后都停下来，等我回复。

⚠️ 这里补上本轮的具体目标（如果有）：例如「之后要做小红书引流的免费测试页」「准备上线收费」「只做稳定性」。没写就只做以上四个阶段。
