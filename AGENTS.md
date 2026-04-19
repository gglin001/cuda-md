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

- Keep `.gitignore` narrow and targeted; do not switch to a deny-all whitelist pattern unless explicitly requested.
- `.gitignore` only affects Git tracking, so agents may still read ignored files, including relevant content under `docs/` and safe symlinked contents.
- When searching under `docs/`, prefer `rg -u`. Use `rg -uL` when symlinks may contain relevant files.
- Do not skip `docs/` subfolders such as `_images/`, `_static/`, `generated/`, or `latest/` when they are relevant to link resolution or context tracing.
- Put disposable scripts and outputs in `debug_agent/` instead of broadening ignore rules.

## Agent Scratch Workflow

- For debugging, repro, validation, or inspection, prefer saving helper scripts, fixtures, and outputs under `debug_agent/` and running them from there.
- Use descriptive names such as `debug_agent/repro_matmul_stride.py`, and keep useful scratch artifacts during the task so the workflow stays visible and reproducible.
- `python - <<'PY'` is a discouraged style example; reserve inline heredocs or one-liners for truly tiny throwaway commands, and otherwise default to saved files in `debug_agent/`.
