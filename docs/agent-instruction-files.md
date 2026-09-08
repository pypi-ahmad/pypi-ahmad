# Agent instruction files: official support matrix

Research date: 2026-08-29. This note uses first-party documentation or first-party source repositories only.

## Verdict

There is no single instruction filename or location shared by every installed coding agent. `AGENTS.md` is the strongest cross-tool **project** convention, but global/personal instructions remain tool-specific. Claude Code uses `CLAUDE.md` natively; Gemini CLI uses `GEMINI.md` by default; Copilot and VS Code add their own `.github`/`~/.copilot` formats. OpenCode, Copilot, VS Code, Grok Build, and Pi accept at least some compatibility aliases. No official MiMo Code source located in this research documents its discovery contract.

## Official mapping

| Tool | Native or supported files | Global/personal scope | Project discovery and precedence |
| --- | --- | --- | --- |
| **OpenAI Codex** | `AGENTS.md`; `AGENTS.override.md`; configurable fallback names | In `CODEX_HOME` (default `~/.codex`), `AGENTS.override.md` replaces `AGENTS.md` | From project root to current directory, at most one file per directory: override, then `AGENTS.md`, then configured fallbacks. Files nearer the current directory appear later and take precedence. [OpenAI docs](https://developers.openai.com/codex/agent-configuration/agents-md) |
| **Claude Code** | `CLAUDE.md`, `CLAUDE.local.md`; modular `.claude/rules/**/*.md`; auto-memory `MEMORY.md` | User: `~/.claude/CLAUDE.md`. Managed Windows policy: `C:\Program Files\ClaudeCode\CLAUDE.md` | Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`; local: `./CLAUDE.local.md`. Files above the working directory load at launch; child-directory files load when Claude works there. Rules may be path-scoped. [Anthropic docs](https://code.claude.com/docs/en/memory) |
| **OpenCode** | `AGENTS.md`; fallback `CLAUDE.md`; arbitrary files via `instructions` in `opencode.json` | `~/.config/opencode/AGENTS.md`; fallback `~/.claude/CLAUDE.md` | Traverses upward from the current directory. The first local match wins, with `AGENTS.md` preferred over `CLAUDE.md`; global OpenCode rules beat the Claude fallback. [OpenCode docs](https://opencode.ai/docs/rules/) |
| **GitHub Copilot CLI** | `.github/copilot-instructions.md`; `.github/instructions/**/*.instructions.md`; agent files `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, and `GEMINI.md` | `~/.copilot/copilot-instructions.md` and `~/.copilot/instructions/**/*.instructions.md` | Repository instructions plus matching path-specific files are supported. Agent-file discovery considers the Git root, current directory, intermediate directories, and directories in the path of a file being edited. [GitHub CLI instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) and [support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) |
| **GitHub Copilot in VS Code / Insiders** | `.github/copilot-instructions.md`; `.github/instructions/**/*.instructions.md`; `AGENTS.md`; `CLAUDE.md`; `.claude/rules/**/*.md` | User rules: `~/.copilot/instructions/**/*.instructions.md` or `~/.claude/rules/**/*.md`; `CLAUDE.md` may also live in the user home | Workspace-wide files are always on; `*.instructions.md` files apply by glob or semantic match. Nested `AGENTS.md` support is experimental, and parent-repository discovery is controlled by settings. Insiders exposes the same feature family, often earlier. [VS Code docs](https://code.visualstudio.com/docs/agent-customization/custom-instructions) and [GitHub support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) |
| **Gemini CLI** | `GEMINI.md` by default; filename(s) configurable through `context.fileName`, so `AGENTS.md` can be selected | `~/.gemini/GEMINI.md` by default | Loads global and hierarchical workspace context; scans relevant ancestors and can discover context just in time as files/directories are accessed. The exact filename is configuration-dependent. [Gemini CLI docs](https://geminicli.com/docs/cli/gemini-md/) and [configuration reference](https://geminicli.com/docs/reference/configuration/) |
| **Grok Build** | `Agents.md`, `Claude.md`, `CLAUDE.md`, `CLAUDE.local.md`, `AGENT.md`, `AGENTS.md`; `.grok/rules/*.md` | `$GROK_HOME` (default `~/.grok`) and `$GROK_HOME/rules/*.md` | In a repository, reads rules from root through current directory; deeper rules come later. Outside Git, it checks the current directory. [xAI docs](https://docs.x.ai/build/features/project-rules) and [official source guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/12-project-rules.md) |
| **Pi coding agent** | `AGENTS.md` or `CLAUDE.md`; `AGENTS.override.md`; system-prompt files `SYSTEM.md` and `APPEND_SYSTEM.md` | `~/.pi/agent/AGENTS.md`; global system files under `~/.pi/agent/` | Walks parent directories and the current directory and concatenates matches. A same-directory `AGENTS.override.md` replaces that directory's `AGENTS.md`/`CLAUDE.md`. Project system-prompt files may live in `.pi/`. [Pi official README](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md#context-files) |
| **Xiaomi MiMo Code** | **Not established by a first-party source found in this research** | **Unknown** | Xiaomi's official model/service material does not document a MiMo Code instruction-file discovery contract. Treat observed local behavior or Claude/OpenCode compatibility as implementation evidence, not an official guarantee, until Xiaomi publishes it. |

## Practical shared setup

- Put repository-wide cross-agent guidance in a root `AGENTS.md`.
- Keep `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`, `~/.pi/agent/AGENTS.md`, and Grok's global rule location for personal defaults where native global discovery matters.
- Keep `~/.claude/CLAUDE.md` for Claude Code. It also serves as OpenCode's documented fallback and is supported by current VS Code customization.
- Keep `~/.gemini/GEMINI.md` unless Gemini CLI's `context.fileName` is explicitly configured to include `AGENTS.md`.
- Keep `~/.copilot/copilot-instructions.md` (and optionally `~/.copilot/instructions/`) for Copilot CLI personal rules; use `.github/copilot-instructions.md` and `.github/instructions/` for repository/path-specific Copilot rules.

## Limits

- Support varies by product surface: Copilot CLI, VS Code Chat, cloud agent, and code review do not all accept the same files. The GitHub support matrix is authoritative for that distinction.
- VS Code Insiders can expose preview behavior before stable VS Code; settings and experimental nested-file behavior may differ by installed version.
- This matrix describes documented instruction discovery, not Agent Skills directories, agent definitions, prompts, hooks, or MCP configuration.
