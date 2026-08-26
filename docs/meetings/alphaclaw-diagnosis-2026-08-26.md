# AlphaClaw（Aliceclaw）全面诊断与对标

> 会议简报 · 2026-08-26  
> 用途：与对方开会前的系统诊断材料  
> 口径：公开可核验信息；营销话术与事实分开写  
> 数据截止：2026-08-26

---

## 0. 先对齐名字

用户口中的 **Aliceclaw / 桌面那个**，公开市场上对应的是 **AlphaClaw Apex**（Mac 桌面舰队控制台），不是一个叫 Aliceclaw 的独立 AI 产品。

| 名字 | 是什么 | 是否值得当会诊对象 |
|---|---|---|
| **AlphaClaw** | OpenClaw 的运维套件（harness / fleet manager） | **是，主对象** |
| **AlphaClaw Apex** | 官方 Mac 桌面端，管多台 OpenClaw 节点 | **是，桌面那一层** |
| **OpenClaw** | 真正干活的 AI 助手运行时 | **必须一起看**，问题大半出在这里 |
| Alice-Claw（GitHub `jammyrob28-create/Alice-Claw`） | 0 star、无 README、2026-02 后停更的个人 UI | 否，可忽略 |
| ClawX / 虾池子 / Kimi Claw | 同类桌面或托管方案 | 对标对象，不是同一家产品 |

开会时建议直接说：**我们诊断的是 AlphaClaw（含 Apex 桌面端），它不是 Agent 本体，是套在 OpenClaw 外面的运维层。**

---

## 1. 一句话总判断

**AlphaClaw 解决的是「OpenClaw 装得上但跑不稳、看不住、回不去」的运维痛，不是把 Agent 做得更聪明。**  
产品方向是对的，但当前位置是：**OpenClaw 热潮上的便利层，还不是企业级 Agent 操作系统。** 对方如果把它讲成「AI 员工 / 数字人 / 生产系统」，宣传和真实交付差了一层。

更直白一点：

- OpenClaw 负责「会干活」
- AlphaClaw 负责「别死、能看、能回滚、少 SSH」
- Apex 负责「多台机器不要开一堆浏览器标签」

用户觉得「问题很多」，公开证据也支持这个体感。问题分三层，不要混着吵：

1. **OpenClaw 本体问题**（安全、技能供应链、暴露面、5700+ issue）
2. **AlphaClaw 套件问题**（便利换安全、Docker 假设、装不上已有实例、渠道向导锁死）
3. **Apex 桌面问题**（Mac 控制台 vs Linux 运行时分裂、复制粘贴、更新失败、本地 Mac 开发还不支持）

---

## 2. 它是谁

| 项 | 可核验事实 |
|---|---|
| 官网 | https://alphaclaw.md |
| 开源仓库 | https://github.com/chrysb/alphaclaw |
| npm | `@chrysb/alphaclaw`，当前 **0.9.34**（2026-07-31） |
| 许可 | MIT |
| 创始人 | Chrys Bader（YC S08，Secret / Treehouse 联合创始人，现 Rosebud） |
| 核心贡献者 | 几乎是单人项目：chrysb 约 582 commits，其余贡献者个位数 |
| 创建时间 | 2026-02-25 |
| GitHub | **1,463 stars / 222 forks / 33 open issues** |
| npm 下载 | 2026-02 至今累计约 **3.15 万**；近 30 天约 **2,563** |
| 赞助 | Render 官方模板 + `$50` 优惠码 `RENDER-ALPHACLAW` |
| 商业化 | 开源套件免费；Apex 托管节点标价 **$99/月** |
| 运行时依赖 | 必须跑 [OpenClaw](https://github.com/openclaw/openclaw)（约 **38.8 万 stars**） |

官网 testimonials 出现了 Garry Tan、YC / SPC 圈的人。把它当**品牌背书**，不要当客户成功案例；公开仓库里看不到对应的企业落地报告。

---

## 3. 它到底卖什么（定位拆穿）

### 3.1 产品分层

```
用户 Mac 上的 Apex 桌面
        │
        │  管舰队、跳进每台节点的 Setup UI
        ▼
AlphaClaw 套件（Express + Setup UI + Watchdog）
        │
        │  spawn / proxy / 重启 / 备份
        ▼
OpenClaw Gateway  :18789
        │
        ▼
模型 + 通道（Telegram/Discord/Slack/Gmail...）+ Skills + 工作区
```

### 3.2 它宣称 vs 它实际交付

| 对方可能怎么讲 | 实际交付 |
|---|---|
| 部署一次，永远跑 | Docker/Linux 上的 watchdog + `openclaw doctor --fix`，不是 SLA |
| 零 SSH、浏览器搞定 | 对 **新部署** 大致成立；接管已有 OpenClaw 还没做完（issue #54 仍开着） |
| 多 Agent 管理 | 同一实例里的多 agent，**隔离是实例级不是 Agent 级**；密钥在同一份 `.env` |
| 自愈 | 进程挂了能拉起来；技能写坏、prompt 漂移、token 被偷，它治不了 |
| 无锁定 | 技术上成立：拆掉 AlphaClaw，OpenClaw 还能跑 |
| Mac 原生 App | Apex 是控制台；README 明确写 **macOS 本地开发还不支持**，运行时目标是 Docker/Linux |

### 3.3 目标用户

真正匹配的人：

- 已经决定用 OpenClaw
- 要在 VPS / Render / Railway 上 24/7 跑
- 不想 SSH 改 json、不想自己写 systemd
- 一个人或小团队管 3–10 个节点

不匹配的人：

- 想要「开箱即用的数字员工 / 销售 Agent」
- 中国本地通道（飞书、企微、微信、钉钉）是刚需
- 要企业级租户隔离、审计、合规
- 只想在自己 Mac 上当 ChatGPT 桌面客户端

---

## 4. 技术栈诊断

### 4.1 AlphaClaw 自身

| 层 | 技术 | 含义 |
|---|---|---|
| 语言 | JavaScript（约 3.2 MB），几乎无 TypeScript | 迭代快，类型约束弱，长期维护风险高 |
| 服务 | Node.js ≥ 22.22.3，Express | 把 OpenClaw gateway 当子进程管 |
| UI | Preact + htm + Wouter + Tailwind | 轻量 Setup UI，不是完整产品控制台 |
| 数据 | SQLite 事件日志 + `/data` 工作区 | Docker 默认根目录是 `/data`，本地 `npx` 会踩坑 |
| 备份 | 每小时 git commit 到 GitHub | 依赖 `GITHUB_TOKEN`；Docker 里曾经静默失败（#105 已修） |
| 部署 | Render / Railway 一键模板 + Docker | 云端 24/7 才是主路径 |
| 测试 | 自称 440 tests | 有测试意识，但产品仍停在 0.9.x |
| 桌面 | Apex（Mac native） | 仓库主体不含完整桌面源码；桌面是商业控制面 |

架构本质：**进程管家 + 反向代理 + 向导 UI**。没有自己的 Agent 运行时、没有自己的模型、没有自己的记忆系统。

### 4.2 它继承的 OpenClaw 技术债

OpenClaw 是 TypeScript 单体，Gateway + Control UI + Skills + 多通道。公开安全态势（2026 上半年）：

- 60+ CVE / GHSA，含 CVSS 9.9 提权（CVE-2026-32922）
- ClawHub 技能供应链：早期审计约 17% 恶意；Koi 报过 341 / 后续 800+ 恶意技能
- 一度有 10 万级实例公网暴露；3 月 Censys 仍扫到约 6.3 万
- 信息窃取木马已经开始扫 `~/.openclaw` 里的 token / 设备私钥
- 官方已接 VirusTotal / ClawScan，但 prompt injection 和动态加载仍能绕过静态扫描

**结论：给 AlphaClaw 做安全评估，等于同时评估 OpenClaw。** 套件自己的密码门、一键配对、query-string token，是在 OpenClaw 已经偏宽的权限模型上再放松一档。官方 README 自己写了这句：要完整安全姿态，请直接用 OpenClaw，不要用 AlphaClaw。

### 4.3 技术栈评分（开会用）

| 维度 | 分数 | 说明 |
|---|---|---|
| 解决真实痛点 | 8/10 | 「Agent 运维」确实是缺口 |
| 架构清晰度 | 7/10 | 包装层边界清楚，可卸载 |
| 工程成熟度 | 4/10 | 0.9.x、单人、JS 无 TS、桌面/运行时分裂 |
| 安全默认值 | 3/10 | 主动用便利换安全 |
| 可观测性 | 6/10 | watchdog、usage、cron、terminal 有，但 doctor UI 能把终端打坏 |
| 中国场景适配 | 2/10 | 通道向导锁 Telegram/Discord/Slack；飞书/微信不是一等公民 |
| 可维护性 / 总线因子 | 3/10 | 几乎绑在 chrysb 一个人身上 |

---

## 5. 商业与市场

### 5.1 商业模式

现在能看清的只有两层：

1. **开源获客**：MIT + Render/Railway 模板 + npm  
2. **托管变现**：Apex 节点 **$99/月**

没有公开的席位费、企业合同页、SOC2、SLA、多租户报价。这更像 **独立开发者 / 工作室产品**，不是已经完成 PMF 的 SaaS。

成本对照（对方很难回避）：

| 方案 | 大致月费 | 你买到什么 |
|---|---|---|
| 自建 OpenClaw（Hetzner / 闲置机器） | $2–20 + 模型费 | 运行时，自己运维 |
| Railway/Render 上的 AlphaClaw | PaaS $5–30 + 模型费 | 少 SSH，仍要自己盯 |
| **AlphaClaw Apex 托管节点** | **$99** + 模型费 | 少运维，实例仍是 OpenClaw |
| Kimi Claw（云托管 OpenClaw） | 会员 **$39** 起（Allegretto），另扣云主机额度 | 一键云端 + 40GB + ClawHub |
| 自己 Mac 上官方 OpenClaw App | 0 + 模型费 | 本机助手，不是 24/7 舰队 |

$99 要成立，必须证明：比 Kimi 更稳、比自建更省人、比 ClawX 更适合「多机舰队」。目前公开材料只证明了「比手搓 OpenClaw 省事」。

### 5.2 市场位置

OpenClaw 是 2025 年底到 2026 年增长最快的开源 Agent 之一（约 38.8 万 star）。周围已经长出三类生意：

1. **运行时替代**：NanoClaw、nanobot、TrustClaw、NemoClaw —— 主打更小、更隔离、更安全  
2. **桌面壳**：ClawX、虾池子、官方 macOS/Windows Hub —— 主打「别用终端」  
3. **运维/舰队层**：AlphaClaw、部分 Manager —— 主打「别 SSH、别死」  
4. **托管**：Kimi Claw —— 主打「别自己买机器」

AlphaClaw 卡在第 3 类。这一类市场真实存在，但：

- 用户量远小于「我想要一个桌面 Claw」
- 一旦 OpenClaw 官方把 watchdog / 备份 / 向导做完整，便利层会被压薄
- 中国客户更可能先碰到 ClawX / 虾池子，而不是 alphaclaw.md

### 5.3 增长信号（偏冷）

npm 月下载：

| 月份 | 下载量 | 解读 |
|---|---|---|
| 2026-02 | 2,854 | 发布首周 |
| 2026-03 | 11,076 | 高峰，吃 OpenClaw 流量 |
| 2026-04 | 7,201 | 回落 |
| 2026-05 | 3,105 | 继续掉 |
| 2026-06 | 1,705 | 低点 |
| 2026-07 | 3,311 | 小反弹（0.9.2x–0.9.34） |
| 2026-08（至 26 日） | 2,258 | 未回到 3 月水平 |

近 7 天仅约 385 次下载。结合「最新正式版停在 7 月 31 日、产品仍 0.9」，更像 **热潮后的长尾工具**，不是在加速的平台。

---

## 6. 用户与体验：问题清单（开会可逐条问）

### 6.1 产品体验分裂

1. **桌面是 Mac，运行时是 Linux。** Apex 宣传「Download for Mac」；README 写 macOS local development is not yet supported。用户在自己电脑上 `npx alphaclaw start`，会按 Docker 习惯去找 `/data`（issue #121，仍 open）。
2. **不能接管已有 OpenClaw。** issue #54 还开着。已经跑着的人无法「一键纳入舰队」，只能新装一套。
3. **Onboarding 通道锁死。** 即使 Signal 已经配好，向导仍强制 Telegram / Discord / Slack（#113）。中国客户常用的飞书/企微不在这条主路上。
4. **Doctor 修不好。** 浏览器里跑 `openclaw doctor --fix`，终端字符挤成一团，修故障的关键路径不可用（#76）。
5. **桌面基础交互。** Apex/Nexus 复制粘贴失效（#50）、应用更新失败（#55），都还开着。

### 6.2 运维可靠性

6. Git 整点备份曾在 Docker 里**静默失败**（#105，7 月才修）。宣传「hourly git backup / 可审计」在那之前是空的。
7. Railway 官方自己警告：Trial 内存不够会 OOM，必须升到 Hobby **8GB RAM**。这不是轻量玩具的资源画像。
8. 版本管理多次翻车：模板钉死的 AlphaClaw 和 npm 最新 OpenClaw 对不上（#67）、Railway 更新检测失败（#58）、部署缺 pin 版本（#65）。包装层最怕的就是「两套版本漂了」。
9. Watchdog 在 Tailscale serve 模式下健康检查会坏（#21，已关）。说明「自愈」依赖特定网络拓扑。

### 6.3 安全与多租户

10. 单密码进门、首次 CLI 自动批准、Webhook 支持 `?token=`。官方承认这是安全降级。
11. 多 Agent 共享实例 `.env`。做「给客户每人一个员工」会串密钥。
12. `/v1` OpenAI 兼容代理一旦打开，持有 gateway token 的调用方等于拥有该 Agent 的全部工具权限。
13. 把节点放到 Render/Railway 公网，等于把 Setup UI 暴露出去；密码强度和 lockout 成了唯一大门。这和 2026 年 OpenClaw 大规模暴露事件是同一类风险。

### 6.4 体验总评

对「会 Docker 的个人开发者」：能明显少痛苦。  
对「业务负责人 / 非技术运营」：向导前 5 分钟好看，后面仍会撞上 OpenClaw 的通道、OAuth、技能、权限。  
对「要卖给中国团队的人」：缺中文、缺本地 IM、缺国内模型一等接入（Z.AI provider 还是开着的 feature request #57）。

---

## 7. GitHub 对标：该看哪些方案

按「你开会时可能要选的路」分组，不按 star 崇拜排序。

### A. 官方原厂（先问：为什么不直接用这个）

| 项目 | Star | 定位 | 和 AlphaClaw 的关系 |
|---|---|---|---|
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | 387,682 | Agent 运行时 + Control UI + CLI | AlphaClaw 包的就是它 |
| 官方 macOS menu bar / Windows Hub ([openclaw-windows-node](https://github.com/openclaw/openclaw-windows-node) 2,070) | — | 本机伴侣：托盘、聊天、node | 本机体验应走官方，不走 Apex |
| [clawhub.ai](https://clawhub.ai) | 生态市场 | Skills / plugins | 能力来源，也是供应链风险来源 |

**建议：** 单机个人助手，优先官方 App + Gateway Dashboard（`127.0.0.1:18789`）。不要为了「有个桌面」去买 Apex。

### B. 桌面壳：ClawX 是当前最强对标

| 项目 | Star | 技术 | 适合谁 | 对 AlphaClaw 的杀伤 |
|---|---|---|---|---|
| **[ValueCell-ai/ClawX](https://github.com/ValueCell-ai/ClawX)** | **7,595** | Electron + React + 内嵌 OpenClaw | 要「装完就能聊」的中英用户 | **桌面体验明显更完整**：聊天、技能、通道、代理、国内站 clawx.com.cn / claw-x.com |
| **[miaoxworld/openclaw-manager](https://github.com/miaoxworld/openclaw-manager)**（虾池子） | **1,703** | Tauri 2 + React + Rust | 中国用户、要飞书/微信/钉钉、要安全扫描 | 星数已超过/持平 AlphaClaw，且自带一键安全修复 |
| [MrFadiAi/openclaw-manager](https://github.com/MrFadiAi/openclaw-manager) | 216 | 桌面一键安装器 | 小白安装 | 只解决安装，不解运维 |
| [wzdavid/openclaw-desktop](https://github.com/wzdavid/openclaw-desktop) | 43 | 桌面工作区 | 轻度替代 | 体量小 |
| [rshodoskar-star/openclaw-desktop](https://github.com/rshodoskar-star/openclaw-desktop)（AEGIS） | ~119 | Electron | Windows 向 | 非主流 |
| [xiaoaoke/openclaw-win](https://github.com/xiaoaoke/openclaw-win) | 27 | Electron | Windows GUI | 早期尝试 |
| [touwaeriol/claw-tool](https://github.com/touwaeriol/claw-tool) | 0 | NW.js + Vue3 | 远程 SSH 管实例 | 几乎无社区 |

**开会句：** 如果痛点是「桌面不好用」，答案更可能是 **ClawX 或虾池子**，不是 AlphaClaw Apex。Apex 赢面只在「多台云上节点的舰队控制台」。

### C. 运行时替代：如果问题其实是 OpenClaw 太大、太危险

| 项目 | Star | 一句话 |
|---|---|---|
| **[nanocoai/nanoclaw](https://github.com/nanocoai/nanoclaw)** | **30,623** | 容器级隔离，代码量可审计，针对 OpenClaw 安全模型的直接反对票 |
| **[HKUDS/nanobot](https://github.com/HKUDS/nanobot)** | **47,418** | Python 轻量自托管 Agent，带 WebUI |
| [ComposioHQ/trustclaw](https://github.com/ComposioHQ/trustclaw) | 882 | OAuth 工具 + 沙箱，偏「能连真实 App 但不把整台机器交出去」 |
| NVIDIA NemoClaw | 生态方案 | 硬件侧 guardrail / 本地模型，偏企业硬件路线 |

### D. 多 Agent 协同（和「舰队」不是一回事）

| 项目 | Star | 一句话 |
|---|---|---|
| [HKUDS/ClawTeam](https://github.com/HKUDS/ClawTeam) | 5,519 | 把多个 CLI Agent（含 OpenClaw）编成带 leader 的开发集群，worktree 隔离 |

AlphaClaw 的「多 Agent」是同一 Gateway 里的角色卡；ClawTeam 的「多 Agent」是并行干活的工程团队。对方如果把这两个词混用，要当场拆开。

### E. 托管商业化

| 产品 | 价格带 | 对比 AlphaClaw $99 |
|---|---|---|
| **Kimi Claw** | 会员 $39+ ，云主机另扣约 0.6% 额度/天 | 更便宜的「别自己运维」；绑定月之暗面生态 |
| AlphaClaw Apex node | $99/月 | 更贵，卖点是「你的节点、可自托管、可退出」 |
| 自建 + AlphaClaw 开源套件 | PaaS 小几十刀 | 多数团队的理性选择 |

---

## 8. 对照表（会议投影用）

| | OpenClaw 官方 | AlphaClaw / Apex | ClawX | 虾池子 | NanoClaw | Kimi Claw |
|---|---|---|---|---|---|---|
| 本质 | 运行时 | 运维套件 + Mac 控制台 | 桌面产品壳 | 桌面管理器 | 安全向运行时 | 托管 OpenClaw |
| 主场景 | 本机助手 | 云上 24/7 舰队 | 日常桌面使用 | 中国本地安装/运维 | 不信任宿主机权限 | 不想碰服务器 |
| 平台 | 全平台 | 运行时 Linux/Docker；Apex 仅 Mac | Win/Mac/Linux | Win/Mac/Linux | 容器 | 云 + 端 |
| 中文/飞书 | 弱 | 弱 | 强 | 强 | 一般 | 强 |
| 安全默认 | 已比早期硬，仍宽 | **再放松一档** | 钥匙串存密钥，仍吃 OpenClaw | 自带安全扫描修复 | 容器隔离 | 云厂商责任 |
| 成熟度 | 社区巨大、issue 巨大 | 0.9、单人 | 桌面最完整之一 | 与 AlphaClaw 同量级 | 社区比 AlphaClaw 大一个数量级 | 商业产品 |
| 锁定 | 无 | 宣称无锁定 | 内嵌 runtime | 管本地 OpenClaw | 自己的 runtime | 会员 + 云主机 |
| 该不该选 | 默认底座 | 只在「多云节点运维」时选 | 桌面入口优先 | 国内团队安装器优先 | 安全红线优先 | 愿付费省运维时选 |

---

## 9. 给对方会的提问清单（建议按这个顺序）

把问题丢给对方，比直接下结论更有用。每题后面是「什么答案算合格」。

1. **你们卖的是 OpenClaw、AlphaClaw 套件，还是 Apex 托管？**  
   合格：三层拆开报价。不合格：一律叫「AI 员工」。

2. **生产节点跑在哪？本机 Mac 还是 Linux/Docker？**  
   合格：Linux 云节点 + Apex 只做控制台。不合格：说在 Mac 上 24/7 跑生产。

3. **能不能接管我们现在已经在跑的 OpenClaw？**  
   合格：给时间表。现状：#54 还开着，默认不能。

4. **多客户 / 多员工如何隔离密钥和数据？**  
   合格：一人一实例，或容器级隔离。不合格：一个实例里建多个 agent。

5. **Watchdog 的恢复 SLA 是什么？doctor --fix 在 UI 里能不能用？**  
   合格：承认 #76，给出终端外的修复路径。不合格：用官网「self-healing」挡回去。

6. **安全基线：配对码、公网绑定、ClawHub 技能白名单、gateway token 保管，谁负责？**  
   合格：默认关公网、技能审核、token 当 root 密码。不合格：只靠 `SETUP_PASSWORD`。

7. **中国通道和模型：飞书 / 企微 / 微信 / GLM / Moonshot 是否一等公民？**  
   合格：给清单和演示。现状：向导仍锁海外 IM，Z.AI 还是 feature request。

8. **$99 托管和 Kimi $39、自建 $20 比，多出来的 60–80 刀买的是什么？**  
   合格：值班、备份验证、版本钉扎、恢复演练。不合格：重复讲 setup wizard。

9. **和 OpenClaw 官方版本怎么钉死？谁测过 Render/Railway 升级？**  
   合格：给出当前 pin 的 OpenClaw 版本和回滚办法。历史：#58/#65/#67 都翻过车。

10. **总线因子：chrysb 不在的时候谁修生产？**  
    合格：有第二人、有支持合同。现状：公开贡献几乎是单人。

---

## 10. 我们自己可以怎么用这轮会诊

按对方角色给三条路，避免会开成「好不好用」的空讨论。

### 路径 A：对方是 AlphaClaw 团队 / 代理商

- 承认运维层价值，但要求按第 9 节逐条书面回答
- 试点范围：**1 个非生产节点，Linux，不开公网 `/v1`，技能白名单，不用来跑真实客户数据**
- 桌面只拿 Apex 当跳板，不把 Mac App 当运行时
- 价格锚在 Kimi $39 和自建，不接受「因为是 AI」就 $99

### 路径 B：对方是想用 Claw 做业务的客户（我们去帮他们诊断）

优先推荐组合，而不是单点工具：

1. **个人/老板本机**：官方 OpenClaw 或 **ClawX**
2. **国内团队落地**：虾池子（安装 + 通道 + 安全扫描）
3. **要 24/7 且能接受海外栈**：开源 AlphaClaw 自托管，不上 $99，除非他们真的有多节点
4. **安全红线（邮箱、网银、客户数据）**：**不要**把生产放在默认 OpenClaw/AlphaClaw 上，改看 NanoClaw / 沙箱方案
5. **要多人并行干活**：ClawTeam，不是 AlphaClaw 里建几个 agent

### 路径 C：我们自己要做同类产品

可抄的：向导、watchdog、git 备份、usage/cron 可视化、可卸载包装层。  
不要抄：单密码安全模型、Docker `/data` 写死、通道锁死、把桌面和运行时做成两个故事。  
差异化机会（国内）：飞书/企微一等接入、中文技能审核、实例级隔离、把 OpenClaw 版本钉死并提供一键回滚。

---

## 11. 会后 30 秒结论稿（可直接念）

> AlphaClaw 不是 Agent，是 OpenClaw 的运维壳。桌面 Apex 只是舰队遥控器，真正跑任务的还是 OpenClaw。  
> 它把「部署和保活」做明白了，但安全默认值更松、Mac/Linux 故事是分裂的、不能接管已有实例、国内通道弱、产品还在 0.9、维护几乎绑在一个人。  
> GitHub 上桌面体验更好的是 ClawX，国内安装器更完整的是虾池子，安全方向该看 NanoClaw，省事托管该对比 Kimi Claw。  
> 除非你们的真实痛点就是「多台 Linux 节点别 SSH、别半夜挂掉」，否则不该把它当成业务主系统。

---

## 12. 关键链接

- 官网：https://alphaclaw.md
- 源码：https://github.com/chrysb/alphaclaw
- 已知问题：https://github.com/chrysb/alphaclaw/issues
- Product Hunt：https://www.producthunt.com/products/alphaclaw-apex
- OpenClaw：https://github.com/openclaw/openclaw
- ClawX：https://github.com/ValueCell-ai/ClawX
- 虾池子：https://github.com/miaoxworld/openclaw-manager
- NanoClaw：https://github.com/nanocoai/nanoclaw
- Kimi Claw：https://www.kimi.com/resources/kimi-claw-introduction
- 安全背景：Unit 42 ClawHub 供应链、CVE-2026-32922、OpenClaw 公网暴露事件

---

*材料性质：基于公开仓库、npm、issue、官网和第三方安全报告的会前诊断，不是对方系统的登录后渗透测试。会上若对方给演示环境，优先核验第 6 节和第 9 节，而不是再听一遍功能清单。*
