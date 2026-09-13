# Agent roles

This rule defines exactly four roles for Phase 2 and later work. It assigns responsibilities only; it does not configure Hermes chat profiles or handle credentials.

## PM

- **Responsibility:** Act as the dispatcher: read a goal, break it into Kanban tasks, and assign those tasks.
- **Claude Code subagent file (Task 2.2):** `.claude/agents/pm-dispatcher.md`
- **Hermes chat-profile setup:** Actual Hermes chat-profile setup, including bot tokens and gateway configuration, is a manual step Sugam performs outside this session via `hermes profile` commands. The PM does not configure profiles or handle credentials.

## tool-builder

- **Responsibility:** Implement a tool against the `@repo/tool-sdk` contract, including the manifest, entry point, quota-hook call, and applicable platform naming and layout conventions.
- **Claude Code subagent file (Task 2.2):** `.claude/agents/tool-builder.md`
- **Hermes chat-profile setup:** Actual Hermes chat-profile setup, including bot tokens and gateway configuration, is a manual step Sugam performs outside this session via `hermes profile` commands. The tool-builder does not configure profiles or handle credentials.

## reviewer

- **Responsibility:** Review the assigned work for specification compliance and code quality, including correctness, readability, architecture, security, and verification.
- **Claude Code subagent file (Task 2.2):** `.claude/agents/reviewer.md`
- **Hermes chat-profile setup:** Actual Hermes chat-profile setup, including bot tokens and gateway configuration, is a manual step Sugam performs outside this session via `hermes profile` commands. The reviewer does not configure profiles or handle credentials.

## tester

- **Responsibility:** Write and run focused smoke tests for the assigned work, then report the commands and results.
- **Claude Code subagent file (Task 2.2):** `.claude/agents/tester.md`
- **Hermes chat-profile setup:** Actual Hermes chat-profile setup, including bot tokens and gateway configuration, is a manual step Sugam performs outside this session via `hermes profile` commands. The tester does not configure profiles or handle credentials.
