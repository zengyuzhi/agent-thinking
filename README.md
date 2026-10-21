# agent-thinking

一个 Claude Code skill。它从 27 条思维方法里给当前任务挑出合适的几条并照着做，也能生成发给其他 Agent 的提示词。

方法包括第一性原理、苏格拉底提问法、事前验尸、切斯特顿的篱笆、科学方法调试、对抗式审查、验证链、消融实验等，另有按任务类型整理的提示词技巧，覆盖解释讲解、写代码、画架构图、长任务、调研和输出格式。

## 安装

用 [skills CLI](https://github.com/vercel-labs/skills) 安装，`-g` 装到用户目录，所有项目都能用；去掉 `-g` 只装到当前项目。

```bash
npx skills add zengyuzhi/agent-thinking -g -a claude-code
```

也可以直接 clone 到 Claude Code 的 skill 目录。

```bash
git clone https://github.com/zengyuzhi/agent-thinking.git ~/.claude/skills/agent-thinking
```

两种方式都要重开 Claude Code 会话才生效。仓库设为私有时，安装用的是你本机已有的 git 凭据，需要有这个仓库的访问权限。

## 用法

这个 skill 只能手动调用，平时不占上下文。

```
/agent-thinking 修复登录超时后无法重新登录的 bug
/agent-thinking 写提示词：让子 Agent 审查这次的支付改动
/agent-thinking 事前验尸
```

| 模式 | 触发方式 | 做什么 |
|---|---|---|
| 套用 | 参数描述一件要做的事，或者留空 | 按任务阶段挑最多五条方法，自己完成任务，每条方法在对话里留下证据 |
| 写提示词 | 参数要求写提示词、交给某个 Agent、写进 CLAUDE.md | 只产出一段自包含的提示词，不执行任务 |
| 点名 | 参数里点了某条方法的名字 | 只用被点名的方法 |

## 文件

| 文件 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 操作步骤，以及任务阶段和方法的对照表 |
| [references/methods.md](references/methods.md) | 27 条思维方法，每条附可复制的提示词 |
| [references/techniques.md](references/techniques.md) | 按任务类型的提示词技巧，以及一份可放进 CLAUDE.md 的合并版提示词 |

两个 reference 文件也可以脱离 skill 单独阅读，各自文末列了来源。
