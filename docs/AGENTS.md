# Docs Agent Guide

## Goal

Use local `docs/` as the primary source when understanding CUDA behavior and assisting development tasks. Prefer grounded answers from local files over memory.

## What To Read First

- Prefer `*.html.md` files, because they are text-friendly and searchable.
- Use sibling `.html` files only when structure or embedded links matter.
- Treat `Title`, `URL Source`, and `Published Time` as metadata. Focus on `Markdown Content` for technical details.

## Directory Map By Intent

- Core CUDA model: `docs/cuda-programming-guide/`
- API details: `docs/cuda-runtime-api/`, `docs/cuda-driver-api/`, `docs/cuda-math-api/`
- Performance: `docs/cuda-c-best-practices-guide/`, `docs/*-tuning-guide/`
- Architecture compatibility: `docs/*-compatibility-guide/`, `docs/cuda-compatibility/`
- Compiler and IR: `docs/cuda-compiler-driver-nvcc/`, `docs/parallel-thread-execution/`, `docs/ptx-compiler-api/`, `docs/nvvm-ir-spec/`, `docs/libnvvm-api/`
- Tooling and profiling: `docs/nsight-compute/`, `docs/nsight-systems/`, `docs/cupti/`, `docs/debugger-api/`

## Recommended Workflow

1. Classify the request, for example correctness, API usage, compile issue, or performance tuning.
2. Pick one anchor doc directory, then expand to 1-2 related directories.
3. Search with `rg` and read the most relevant `index.html.md` plus linked chapter files.
4. Cross-check version-sensitive claims in `docs/cuda-toolkit-release-notes/`.
5. Return actionable guidance with file-path evidence.

```bash
rg -n "stream|event|synchron" docs/cuda-runtime-api
rg -n "occupancy|warp|shared memory" docs/cuda-c-best-practices-guide docs/*-tuning-guide
rg -n "ptx|sm_[0-9]+" docs/parallel-thread-execution docs/nvvm-ir-spec
```

## Output Rules For Agents

- Cite concrete local paths in every non-trivial answer, for example `docs/cuda-runtime-api/index.html.md`.
- Separate confirmed facts from inference.
- If docs do not contain the needed detail, say so clearly and suggest the next best doc path to inspect.
- For code help, end with practical steps, for example API choice, kernel changes, compiler flags, and validation checks.
