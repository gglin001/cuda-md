#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

args=(
  # CUDA Toolkit Documentation
  cuda-toolkit-release-notes.sh

  # Installation Guides
  cuda-quick-start-guide.sh
  cuda-installation-guide-linux.sh
  # cuda-installation-guide-microsoft-windows.sh

  # Programming Guides
  cuda-programming-guide.sh
  cuda-c-best-practices-guide.sh
  cutile-python.sh
  parallel-thread-execution.sh
  tile-ir.sh

  # Architecture Guides
  ada-compatibility-guide.sh
  ada-tuning-guide.sh
  ampere-compatibility-guide.sh
  ampere-tuning-guide.sh
  blackwell-compatibility-guide.sh
  blackwell-tuning-guide.sh
  hopper-compatibility-guide.sh
  hopper-tuning-guide.sh
  inline-ptx-assembly.sh
  ptx-writers-guide-to-interoperability.sh
  # turing-compatibility-guide.sh
  # turing-tuning-guide.sh
  # video-decoder.sh

  # CUDA API References
  # cublas.sh
  # cudla-api.sh
  # cufft.sh
  # curand.sh
  # cufile-api-reference-guide.sh
  # cusolver.sh
  # cusparse.sh
  cuda-driver-api.sh
  cuda-math-api.sh
  cuda-runtime-api.sh
  # npp.sh
  # nvblas.sh
  nvfatbin.sh
  nvjitlink.sh
  # nvjpeg.sh
  nvrtc.sh
  # cccl contains `cub`, `thrust`, `libcudacxx`, and others
  cccl.sh
  # cub.sh
  # cuda-cpp-standard-library.sh
  # thrust.sh

  # PTX Compiler API References
  ptx-compiler-api.sh

  # Miscellaneous
  cupti.sh
  cuda-compatibility.sh
  demo-suite.sh
  debugger-api.sh
  # eflow-users-guide.sh
  gpudirect-rdma.sh
  gpudirect-storage.sh
  # mig-user-guide.sh
  # vGPU.sh
  # wsl-user-guide.sh

  # Tools
  # compute-sanitizer.sh
  # cuda-binary-utilities.sh
  # cuda-compile-time-advisor.sh
  # cuda-gdb.sh
  cuda-compiler-driver-nvcc.sh
  nsight-compute.sh
  # nsight-eclipse-plugins-guide.sh
  # nsightee-plugins-install-guide.sh
  nsight-systems.sh
  # nsight-visual-studio-edition.sh

  # White Papers
  # floating-point.sh
  # incomplete-lu-cholesky.sh

  # Application Notes
  # cuda-for-tegra-appnote.sh

  # Compiler SDK
  libnvvm-api.sh
  libdevice-users-guide.sh
  nvvm-ir-spec.sh

  # CUDA Archives
  # cuda-c-programming-guide.sh
  # cuda-features-archive.sh

  # Legal Notices
  # eula.sh
)

for script in "${args[@]}"; do
  echo "==> ${script}"
  "${SCRIPT_DIR}/${script}" "$@"
done
