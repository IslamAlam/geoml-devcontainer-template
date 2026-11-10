# geoml-devcontainer-template

A ready-to-use template for **Python package development in a dev container**, aimed at
geospatial, SAR and machine-learning work. It is maintained by Islam Mansour.

Source code: [GitHub](https://github.com/IslamAlam/geoml-devcontainer-template) ·
[UniBw GitLab](https://git.unibw.de/l91bisma/geoml-devcontainer-template)

## What you get

- **GPU-ready image**: NVIDIA CUDA, GDAL/PROJ, QGIS, GRASS, SAGA and Orfeo Toolbox, with
  JupyterLab and a QGIS desktop in the browser.
- **uv** for fast, locked Python dependencies (`pyproject.toml` + `uv.lock`).
- **Quality gates**: ruff, mypy, pytest with coverage and pre-commit hooks, set up automatically.
- **Docs and CI**: this mkdocs site and a GitLab CI pipeline that use the same setup.

## What to expect

| | |
|---|---|
| **You need** | VS Code with *Remote - SSH* and *Dev Containers*; a Linux server with Docker, the NVIDIA driver and the NVIDIA Container Toolkit |
| **First setup** | About 15 minutes. Most of it is the one-time download of the container image (several GB) |
| **Later starts** | A few seconds |
| **At the end** | Your own package with passing tests, a working GPU, JupyterLab and QGIS on the same files |

**Start here: [Getting started](getting-started.md)**, a step-by-step guide with screenshots.
For the background (why dev containers, how the template is built), see the
[tutorial slides](https://tutorial.geoml-template.imansour.net/).
Then see [Development](dev.md) for the daily workflow and the [API reference](api.md).

## Example

The template ships two small example functions that you replace with your own code:

```python
from mypackage import linear_to_db, normalize

db = linear_to_db(sigma0)
x = normalize(db)
```
