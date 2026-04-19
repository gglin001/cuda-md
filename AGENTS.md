# Repository Guidelines

## Project Structure & Module Organization

This repository mirrors NVIDIA CUDA documentation into local Markdown and HTML sidecars. Keep source logic in `scripts/` and treat `docs/` as generated output.

- `scripts/crawl.py`: Threaded crawler that downloads pages, linked assets, and `.html.md` sidecars.
- `scripts/*.sh`: One wrapper per CUDA document. Each script defines `--base-url` and writes to `docs/<slug>/`.
- `scripts/_run.sh`: Batch runner for a curated set of wrappers.
- `docs/<slug>/`: Downloaded artifacts grouped by document slug.
- `debug_agent/`: untracked scratch workspace for temp files and local experiments (use this instead of `/tmp`).

## Build, Test, and Development Commands

- `bash scripts/cuda-programming-guide.sh --max-files 20`: Smoke test one guide without a full crawl.
- `bash scripts/_run.sh`: Run the default multi-guide crawl set.

## Workspace Hygiene and `.gitignore` Policy

The repository uses a narrow `.gitignore` strategy (targeted ignores), not a global deny-all pattern like `*` + whitelist.

- Do not switch to a deny-all ignore pattern unless explicitly requested.
- Assume `.gitignore` controls Git tracking only; it does not define what agents may read.
- For content lookup in `docs/`, prefer `rg -u` so ignored files are not skipped by default search behavior.
- Do not skip `docs/` subfolders such as `_images/`, `_static/`, `generated/`, or `latest/` when they are relevant to link resolution or context tracing.
- Prefer putting disposable outputs in `debug_agent/` instead of expanding broad ignore rules.
