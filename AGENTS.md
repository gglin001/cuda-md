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
