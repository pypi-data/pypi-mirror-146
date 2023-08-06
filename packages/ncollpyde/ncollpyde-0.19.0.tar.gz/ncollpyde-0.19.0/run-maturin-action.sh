#!/bin/bash
set -e
echo "::group::Install Rust"
which rustup > /dev/null || curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable
export PATH="$HOME/.cargo/bin:$PATH"
rustup override set stable
echo "::endgroup::"
export PATH="$PATH:/opt/python/cp36-cp36m/bin:/opt/python/cp37-cp37m/bin:/opt/python/cp38-cp38/bin:/opt/python/cp39-cp39/bin"
echo "::group::Install maturin"
curl -L https://github.com/PyO3/maturin/releases/latest/download/maturin-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin
maturin --version || true
which patchelf > /dev/null || python3 -m pip install patchelf
echo "::endgroup::"
maturin publish -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGFjMTI0ZDlmLTFlNmUtNDAzOC05YjJiLTk3MmM4MzRlZTkzNwACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgz4ebNID3sj0Nbm7umV-2lE3ZjpfWFQBY8lXiuuSphfY --skip-existing --universal2