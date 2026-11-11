# Choosing versions: QGIS, CUDA and PyTorch

The base image fixes three things at once: the **QGIS** version, the **CUDA** version and the
**Linux** release. PyTorch brings its own CUDA build. This page shows how to pick versions that work
together.

## 1. Use an LTR image

QGIS has two release lines: *latest* (newest features) and **LTR** (*long-term release*: fewer
changes, bug fixes for a long time). For research code, use **LTR**. The template does this by
default with `"BASE_TAG": "ltr"` in `.devcontainer/devcontainer.json`.

For a paper, pin the exact version instead of `ltr`, so the environment cannot change under you:

```bash
python3 scripts/rename_project.py my_project --base-tag 3.44.15
```

or set `"BASE_TAG": "3.44.15"` by hand and run *Dev Containers: Rebuild Container*.

## 2. Look up the CUDA version of the image

b-data publishes which CUDA version each image contains in its
**[CUDA version matrix](https://github.com/b-data/jupyterlab-qgis-docker-stack/blob/main/CUDA_VERSION_MATRIX.md#ltr)**.
Always check there for the latest releases. A snapshot of the newest LTR rows (November 2026):

| QGIS (LTR) | CUDA | Linux |
|---|---|---|
| 3.44.15 | 13.4.3 | Ubuntu 24.04 |
| 3.44.14 | 13.4.1 | Ubuntu 24.04 |
| 3.44.13 | 13.3.1 | Ubuntu 24.04 |
| 3.44.11 | 13.3.0 | Ubuntu 24.04 |
| 3.44.8 | 13.2.0 | Ubuntu 24.04 |
| 3.40.x | 12.8–12.9 | Ubuntu 22.04 |

*Snapshot only; the matrix linked above is the reference.*

## 3. Check the server’s NVIDIA driver

The driver on the **server** must be new enough for the CUDA version you use. Check it with:

```bash
nvidia-smi
```

The top line shows the driver version and the highest CUDA version it supports. The matrix lists
the recommended and supported drivers for each CUDA version. If the driver is too old, ask the
server’s admin, or choose an older image whose CUDA version the driver supports.

## 4. Pick the matching PyTorch build

PyTorch wheels come with their own CUDA libraries, built for one CUDA version (for example
`torch 2.x.y+cu130`). Choose the build on the
**[PyTorch “Get started” page](https://pytorch.org/get-started/locally/#supported-linux-distributions)**:

- Select a CUDA version that PyTorch offers and that the **server’s driver** supports.
- Prefer the same **major** version as the image’s CUDA (CUDA 13.x image → a `cu13x` PyTorch build),
  so PyTorch and the image’s CUDA tools agree.
- The image’s Linux release must be supported by PyTorch (Ubuntu 22.04 and 24.04 are).

`uv sync --extra ml` installs the default PyTorch build from PyPI. To choose a specific CUDA build,
point uv at PyTorch’s package index in `pyproject.toml` (replace `cuXXX`, for example `cu130`, with
the version from the PyTorch page):

```toml
[[tool.uv.index]]
name = "pytorch-cuXXX"
url = "https://download.pytorch.org/whl/cuXXX"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cuXXX" }
torchvision = { index = "pytorch-cuXXX" }
```

Then run `uv lock` and `uv sync --extra ml`.

## 5. Verify

```bash
make env
```

shows the installed PyTorch build (for example `2.15.0+cu132`), whether CUDA is available and the
GPU name. In our test, the LTR image 3.44.15 (CUDA 13.4.3) with PyTorch `2.15.0+cu132` ran on an
NVIDIA A100.
