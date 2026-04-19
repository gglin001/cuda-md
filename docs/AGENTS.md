# Docs Agent Guide

## Goal

Use this docs tree as a local CUDA knowledge base for kernel and runtime development. Prefer evidence from local files over memory.

## What To Read First

- Prefer `*.html.md`, because they are text-friendly and fast to grep.
- Use sibling `.html` only when DOM structure or embedded navigation matters.
- Treat `Title`, `URL Source`, and `Published Time` as metadata, and use `Markdown Content` for technical claims.

## Directory Map By Intent

The categories below are a practical starting map, not an exhaustive list. If a topic is missing here, continue searching in other folders under `docs/`.

- Core model: `cuda-programming-guide/`
- API behavior: `cuda-runtime-api/`, `cuda-driver-api/`, `cuda-math-api/`
- Performance: `cuda-c-best-practices-guide/`, `*-tuning-guide/`
- Compatibility: `*-compatibility-guide/`, `cuda-compatibility/`
- Compiler and IR: `cuda-compiler-driver-nvcc/`, `parallel-thread-execution/`, `ptx-compiler-api/`, `nvvm-ir-spec/`
- Tooling: `nsight-compute/`, `nsight-systems/`, `cupti/`, `debugger-api/`

## Recommended Workflow

1. Classify the task, for example API usage, correctness, compile failure, or performance tuning.
2. Pick one anchor directory and 1-2 related directories.
3. Search via `rg -u`. Use `rg -uL` when symlinked docs may be relevant.
4. Check `cuda-toolkit-release-notes/` for version-sensitive behavior.
5. Return guidance with concrete evidence paths.

```bash
# CWD is docs
rg -n -u "stream|event|synchron" cuda-runtime-api
rg -n -u "occupancy|warp|shared memory" cuda-c-best-practices-guide *-tuning-guide
rg -n -uL "ptx|sm_[0-9]+" parallel-thread-execution nvvm-ir-spec
```

## Workspace Hygiene and `.gitignore` Policy

Use `.gitignore` as a Git tracking rule, not as a content relevance rule.

- Use `rg -u` for docs searches, so ignored files are not silently skipped.
- Use `rg -uL` when relevant docs may be reached through symlinks.
- Do not skip folders such as `_images/`, `_static/`, `generated/`, or `latest/` when tracing links, symbols, or anchor behavior.
- Narrow search scope with explicit paths and patterns, instead of dropping `-u`.

## Output Rules For Agents

- Quote evidence with concrete relative paths, for example `cuda-runtime-api/index.html.md`.
- Separate confirmed facts from inference.
- If evidence is missing, state that clearly, then suggest the next doc path to inspect.
- For code advice, end with concrete implementation and validation steps.
