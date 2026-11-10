# geoml-devcontainer-template

A ready-to-use template for **Python package development in a dev container**, aimed at
geospatial, SAR and machine-learning work.

One `git clone` and "Reopen in Container" gives you:

- **GPU-ready image**: NVIDIA CUDA, GDAL/PROJ, QGIS, GRASS, SAGA and Orfeo Toolbox
  (b-data JupyterLab CUDA + QGIS stack), with JupyterLab and a QGIS desktop in the browser (noVNC)
- **uv** for fast, locked Python dependencies (`pyproject.toml` + `uv.lock`)
- **Quality gates**: ruff (lint + format), mypy, pytest with coverage, pre-commit hooks
- **Docs** with mkdocs-material + mkdocstrings, and a **GitLab CI** pipeline that runs in the same image

Author: Islam Mansour.

---

## Quick start (10 minutes)

### 0. Requirements

| Where the container runs | You need |
|---|---|
| Linux GPU server / workstation | Docker, NVIDIA driver, [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/) |
| Your laptop | VS Code with the *Dev Containers* extension (and *Remote - SSH* to use a server) |

No CUDA toolkit is needed on the host, only the driver. On a machine without an NVIDIA GPU
(e.g. an Apple Silicon Mac), remove `"--gpus", "all"` from `runArgs` in `.devcontainer/devcontainer.json`.

### 1. Make it your project

The template lives in two places (same content):

- GitHub: <https://github.com/IslamAlam/geoml-devcontainer-template>
- UniBw GitLab: <https://git.unibw.de/l91bisma/geoml-devcontainer-template>

```bash
# from GitHub
git clone https://github.com/IslamAlam/geoml-devcontainer-template.git my_project
# or from the UniBw GitLab (SSH)
git clone ssh://git@git.unibw.de:2222/l91bisma/geoml-devcontainer-template.git my_project

cd my_project
rm -rf .git && git init                      # start your own history
python3 scripts/rename_project.py my_project --author "Jane Doe" --email jane@example.org
rm scripts/rename_project.py
```

This renames the package `mypackage` everywhere (folder, imports, configs, docs).

### 2. Open it in the container

1. (GPU server) VS Code → *Remote-SSH: Connect to Host…* → open the project folder.
2. Command palette → **Dev Containers: Reopen in Container**.
3. Wait for the first build. `postCreateCommand.sh` runs `uv sync` and installs the pre-commit hooks.

### 3. Check that everything works

```bash
make env     # Python, GDAL, PyTorch, CUDA, GPU name
make test    # tests + coverage
make check   # lock file, ruff, mypy
```

`make env` reports PyTorch only after `uv sync --extra ml` (see below).

---

## Daily workflow

```bash
uv add rioxarray                 # add a runtime dependency (updates uv.lock)
uv add --dev pytest-xdist        # add a dev-only tool
uv sync --extra geo --extra ml   # install the optional geo / ML stacks
uv run python examples/check_environment.py
make help                        # list all make targets
```

Rule of thumb: **never `pip install` by hand**. Use `uv add`, so the change is in `pyproject.toml`
and `uv.lock` and everyone, including CI, gets the same environment.

## Project layout

```
.devcontainer/
  Dockerfile               # image: CUDA + GDAL + QGIS + uv
  devcontainer.json        # editor, GPUs, ports, post-create
  postCreateCommand.sh     # uv sync + pre-commit install
  devcontainer-local/      # your personal overrides (git-ignored)
src/mypackage/             # the package (installed in editable mode)
tests/                     # pytest
examples/                  # runnable scripts
docs/                      # mkdocs site
scripts/rename_project.py  # one-off: rename the template
pyproject.toml  uv.lock  Makefile  tox.ini
.pre-commit-config.yaml  .gitlab-ci.yml  mkdocs.yml
```

## QGIS and JupyterLab

The container keeps the image's own start command (`"overrideCommand": false`), so JupyterLab runs
on port 8888 and VS Code forwards it automatically. Open it in your browser, then open the
**Desktop** (Xfce via noVNC) to run QGIS on the same files your code writes.

Get the JupyterLab URL with its token from a terminal in the container:

```bash
jupyter server list
```

Without VS Code, forward the port yourself: `ssh -L 8888:localhost:8888 gpu-server`.

**PyQGIS:** QGIS's Python bindings live in the image's system Python, not in `.venv`. To use
`import qgis` from your project, create the venv with access to system packages:
`uv venv --system-site-packages && uv sync`.

## Personal settings and data

Do not edit the shared `devcontainer.json` for things that only apply to you (dataset mounts,
extra ports). Copy it to `.devcontainer/devcontainer-local/devcontainer.json` (git-ignored), change
`"dockerfile": "Dockerfile"` to `"dockerfile": "../Dockerfile"`, add your mounts, and pick that
configuration when VS Code asks which one to use for "Reopen in Container":

```jsonc
"mounts": [
  { "source": "/data/sentinel1", "target": "/data/sentinel1", "type": "bind", "readonly": true }
]
```

Never put data into the image or the repository.

## Reproducibility

- `uv.lock` pins every Python package. Commit it.
- Pin the base image tag (`BASE_TAG` in `devcontainer.json`, e.g. a concrete QGIS version instead
  of `ltr`) and the uv image tag in the Dockerfile when you publish results.
- CI runs in a small uv image by default. To run it in the dev-container image instead, build and
  push `.devcontainer/Dockerfile` and set `CI_IMAGE` in GitLab (Settings → CI/CD → Variables).

## Documentation site

On every push to `main`, the `pages` CI job builds the mkdocs site and publishes it with GitLab
Pages (Deploy → Pages shows the URL). No extra setup is needed.

**Cloudflare (Workers & Pages) instead:** connect the repository and keep the deploy command
`npx wrangler deploy`. `wrangler.jsonc` builds the site with mkdocs into `site/` and serves it
as static assets. Rename `"name"` in `wrangler.jsonc` to your project.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `torch.cuda.is_available()` is `False` | Host lacks the NVIDIA Container Toolkit, or `--gpus all` is missing from `runArgs` |
| DataLoader crashes with shared-memory errors | Increase `--shm-size` in `runArgs` |
| Files created in the container are owned by root | Keep `"remoteUser": "jovyan"` and `"updateRemoteUserUID": true` |
| First build is slow | The CUDA + QGIS image is many GB; pull it once per server: `docker pull glcr.b-data.ch/jupyterlab/cuda/qgis/base:ltr` |
| pre-commit changed files and the commit stopped | That is expected: `git add` the fixes and commit again |

## Credits

Template by Islam Mansour. Project tooling inspired by
[fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv); base images by
[b-data](https://gitlab.b-data.ch/jupyterlab).
