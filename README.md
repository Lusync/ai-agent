# Agentic Bug-Fixing Assistant (Toy Project)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-experimental-orange.svg)

> Warning: This project can be configured to access your filesystem, run shell commands, and execute Python code via tools you provide. Use only in a controlled environment with non-sensitive data. Do not run on machines with secrets or production credentials. You are responsible for what it accesses.

This repository contains a toy coding assistant built by following the Boot.dev course. It uses an LLM with callable tools to analyze, fix, and refactor code in a local repository. It is an educational prototype—not hardened or secure.

Repo: https://github.com/Lusync/ai-agent

## Features
- Proposes and applies code fixes
- Optional refactoring suggestions
- Extensible tool interface (add tools carefully)
- Works on a local codebase you point it at

## Quick Start
1. Clone and enter:
   ```bash
   git clone https://github.com/Lusync/ai-agent.git
   cd ai-agent

Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Set your model provider key(s):
export OPENAI_API_KEY=your_key_here
 or whichever provider the code is configured for
 (e.g., ANTHROPIC_API_KEY, GOOGLE_API_KEY)

Run the agent:
python main.py

## Configuration
Environment variables: API keys (see above).
You can adjust model/provider settings in-code where the client is initialized.
Tools: the baseline course setup may include read/write filesystem and Python execution—review the code before enabling them.

## Usage Tips
Commit your repo before running the agent so you can revert changes.
Start with read-only operations; enable write/exec tools only when needed.
Review diffs carefully before accepting modifications.

## Extending
Add tools for linting, testing, formatting, or shell tasks—but restrict paths and validate inputs.
Try alternative model providers by swapping the client initialization and API keys.

## Security Considerations
Principle of least privilege (limit file paths, commands, and network access).
Prefer running in a container or a throwaway VM.
Log tool calls/outputs for traceability.
Assume prompt injection is possible—never pass secrets or private code you don’t own/authorize.

## Limitations
May propose incorrect or incomplete fixes.
Not designed for large codebases without customization.
No guarantee of safety, reliability, or correctness.

## License
MIT — see [LICENSE](./LICENSE) for details.

## Acknowledgments
Built by following the Boot.dev course on agentic coding assistants. Inspired by tools like Cursor/Zed Agentic Mode and Claude Code.



