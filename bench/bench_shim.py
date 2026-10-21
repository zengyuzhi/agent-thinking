"""Run the BenchFlow CLI with a newer claude-agent-acp.

BenchFlow 0.7.11 pins claude-agent-acp 0.73.0, which bundles Claude Code
2.1.257; claude-opus-5-5 needs 2.1.280 or newer. Swap the npm package at
runtime instead of editing the installed BenchFlow.
Run with BenchFlow's own interpreter: <benchflow venv>/bin/python bench_shim.py eval run ...
"""

import dataclasses
import os
import sys

from benchflow.agents import registry

OLD = "@agentclientprotocol/claude-agent-acp@0.73.0"
NEW = os.environ.get("BENCH_CLAUDE_AGENT_ACP", "@agentclientprotocol/claude-agent-acp@0.94.0")

cfg = registry.AGENTS["claude-agent-acp"]
assert OLD in cfg.install_cmd, "BenchFlow's pin changed; update bench_shim.py"
new_cmd = cfg.install_cmd.replace(OLD, NEW)
registry.AGENTS["claude-agent-acp"] = dataclasses.replace(cfg, install_cmd=new_cmd)
registry.AGENT_INSTALLERS["claude-agent-acp"] = new_cmd  # copy built at import; install reads this one

from benchflow.cli.main import app  # noqa: E402

sys.argv[0] = "bench"
sys.exit(app())
