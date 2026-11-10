# Base: b-data JupyterLab + CUDA + QGIS stack
#   - Ubuntu + NVIDIA CUDA runtime, GDAL/PROJ, QGIS, GRASS, SAGA, Orfeo Toolbox
#   - Xfce desktop served through noVNC (open it from JupyterLab)
#   - default user: jovyan
# Tags: https://gitlab.b-data.ch/jupyterlab/cuda/qgis/base/container_registry
# "ltr" follows the QGIS long-term release. For reproducible results pin a concrete version,
# e.g. `python3 scripts/rename_project.py my_project --base-tag 3.44.15`, or edit BASE_TAG
# in devcontainer.json. List the available tags: see "Troubleshooting" in the README.
ARG BASE_IMAGE=glcr.b-data.ch/jupyterlab/cuda/qgis/base
ARG BASE_TAG=ltr
FROM ${BASE_IMAGE}:${BASE_TAG}

USER root

# Extra system packages (keep this list short: Python packages belong in pyproject.toml)
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        htop \
        tmux \
        nvtop \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# uv: Python package and project manager (pin the tag for reproducibility)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy (not hard-link) from the uv cache, which may live on another filesystem
ENV UV_LINK_MODE=copy

# Back to the unprivileged user
USER ${NB_USER}
