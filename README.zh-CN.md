# agent-thinking

[English](README.md) | 中文

一个 Agent Skill，兼容 Claude Code、Codex、pi 等支持 `SKILL.md` 的 Agent。它从 27 条思维方法里给当前任务挑出合适的几条并照着做，也能生成发给其他 Agent 的提示词。

方法包括第一性原理、苏格拉底提问法、事前验尸、切斯特顿的篱笆、科学方法调试、对抗式审查、验证链、消融实验等，另有按任务类型整理的提示词技巧，覆盖解释讲解、写代码、画架构图、长任务、调研和输出格式。

## 安装

用 [skills CLI](https://github.com/vercel-labs/skills) 安装。`-g` 装到用户目录，所有项目都能用；去掉 `-g` 只装到当前项目。`-a` 后面写你用的 Agent，可以写多个。

```bash
npx skills add zengyuzhi/agent-thinking -g -a claude-code codex pi
```

Claude Code 的 skill 装进 `.claude/skills/`，Codex 和 pi 共用 `.agents/skills/`。也可以手动 clone 到对应目录。

```bash
git clone https://github.com/zengyuzhi/agent-thinking.git ~/.claude/skills/agent-thinking   # Claude Code
git clone https://github.com/zengyuzhi/agent-thinking.git ~/.agents/skills/agent-thinking   # Codex、pi
```

装完重开会话才生效。仓库设为私有时，安装用的是你本机已有的 git 凭据，需要有这个仓库的访问权限。

## 用法

这个 skill 只能手动调用，模型不会自己加载它，平时不占上下文。

| Agent | 调用方式 | 怎样关掉自动调用 |
|---|---|---|
| Claude Code | `/agent-thinking 任务` | `SKILL.md` 里的 `disable-model-invocation: true` |
| pi | `/skill:agent-thinking 任务` | 同上，pi 也认这个字段 |
| Codex | `$agent-thinking 任务` | `agents/openai.yaml` 里的 `allow_implicit_invocation: false` |

其他 Agent 如果不认这两个字段，skill 仍然能用，只是可能会被模型自动加载。

```
/agent-thinking 修复登录超时后无法重新登录的 bug
/agent-thinking 写提示词：让子 Agent 审查这次的支付改动
/agent-thinking 事前验尸
```

| 模式 | 触发方式 | 做什么 |
|---|---|---|
| 套用 | 参数描述一件要做的事，或者留空 | 按任务阶段挑最多五条方法，自己完成任务，每条方法在对话里留下证据 |
| 写提示词 | 参数要求写提示词、交给某个 Agent、写进 CLAUDE.md 或 AGENTS.md | 只产出一段自包含的提示词，不执行任务 |
| 点名 | 参数里点了某条方法的名字 | 只用被点名的方法 |

## 文件

| 文件 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 操作步骤，以及任务阶段和方法的对照表 |
| [references/methods.md](references/methods.md) | 27 条思维方法，每条附可复制的提示词 |
| [references/techniques.md](references/techniques.md) | 按任务类型的提示词技巧，以及一份可放进 CLAUDE.md 或 AGENTS.md 的合并版提示词 |
| [agents/openai.yaml](agents/openai.yaml) | Codex 的界面信息和调用策略 |

两个 reference 文件也可以脱离 skill 单独阅读，各自文末列了来源。skill 和 reference 文件都是英文写的，调用时 Agent 会用你提问的语言回复。
