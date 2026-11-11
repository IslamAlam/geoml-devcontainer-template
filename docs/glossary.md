# Glossary

Plain-language explanations of the words used in this guide and in the tutorial. No computer
science background needed.

## Containers

**Image**
:   A frozen, read-only copy of a complete software setup: operating system, libraries (CUDA, GDAL,
    QGIS) and tools. Think of it as the **master copy** of a computer’s software. An image never
    changes once it is built, and the same image gives everyone exactly the same setup.

**Container**
:   A **running copy** of an image, the place where you actually work. You can start many containers
    from one image. If you break a container, throw it away and start a fresh one: the image is
    untouched.

**Dockerfile**
:   The **recipe** that builds an image: “start from this image, install these tools”. Our template
    has one in `.devcontainer/Dockerfile`.

**Registry**
:   An online **shelf of images**, for example `glcr.b-data.ch` or `quay.io`. *Pulling* an image
    means downloading it from a registry.

**Tag**
:   The version label after the colon in an image name, for example `:ltr` or `:3.44.15` in
    `glcr.b-data.ch/jupyterlab/cuda/qgis/base:ltr`.

**Docker**
:   The program on the server that downloads images and runs containers.

**Dev container**
:   A container set up for writing code, which VS Code opens and works inside. Its settings live in
    the project’s `.devcontainer/` folder.

**Rebuild**
:   Make a new container (and, if the Dockerfile changed, a new image) from the recipe. Needed after
    you change `.devcontainer/`. Your project files are not affected.

**Mount**
:   Making a folder from the server visible inside the container. Your project folder is mounted at
    `/workspaces/<project>`, so it **lives on the server** and survives every rebuild.

!!! tip "Image vs container in one sentence"
    The **Dockerfile** is the recipe, the **image** is the frozen result everyone shares, and the
    **container** is your running copy of it. Your **project files** are not inside any of them:
    they stay on the server and are mounted in.

## Computers and connections

**Local machine**
:   Your laptop. With VS Code, only the window runs here.

**Server / host**
:   The (GPU) computer where Docker runs and your code actually runs. *Host* means the machine a
    container runs on.

**SSH**
:   The secure connection from your laptop to the server, used by the terminal and by VS Code’s
    *Remote - SSH* extension.

**SSH key pair**
:   Two files that replace typing a password. The **private key** (`id_ed25519`) stays on your
    laptop and is never shared. The **public key** (`id_ed25519.pub`) is copied to the server, to
    GitLab or to GitHub.

**SSH config**
:   A small file on your laptop (`~/.ssh/config`) that gives a server a short name, for example
    `gpu-server`, together with your user name and key.

**Port forwarding**
:   Making a web page that runs on the server (JupyterLab on port 8888) open on your laptop as
    `localhost:8888`. VS Code does this automatically.

**GPU, driver, CUDA**
:   The graphics card that speeds up training, the program that lets the system talk to it, and
    NVIDIA’s toolkit that libraries like PyTorch use. Inside the container you only need CUDA;
    the driver is on the server.

**Terminal, shell**
:   The window where you type commands. The *shell* is the program that reads them: `zsh` or
    `bash` on Linux and macOS, PowerShell on Windows.

## Code and versions

**git**
:   A tool that saves every version of your project and shows what changed.

**Repository (repo)**
:   A project folder whose history git tracks.

**Commit**
:   A saved snapshot of the whole project, with a short message.

**Branch**
:   A separate line of work, for trying an idea without touching the main version.

**Remote, clone, push, pull**
:   A *remote* is a copy of the repo on GitHub or GitLab. *Clone* downloads it, *push* uploads your
    commits, *pull* downloads other people’s.

**pre-commit hook**
:   Checks that run automatically on every `git commit` and fix small issues such as formatting.

**CI (continuous integration)**
:   The same checks and tests, run automatically on GitLab or GitHub after every push.

## Python

**Package**
:   Someone else’s code that you install and import: NumPy, PyTorch, rasterio.

**Environment (`.venv`)**
:   The folder with the packages, and their versions, that one project uses.

**`pyproject.toml`**
:   The project’s description: its name and which packages it needs.

**Lockfile (`uv.lock`)**
:   The exact version of every package, so the same environment can be rebuilt anywhere.

**uv**
:   The tool that installs packages and keeps `pyproject.toml`, `uv.lock` and `.venv` in sync.

**Extra**
:   An optional group of packages, for example `geo` or `ml`, installed with
    `uv sync --extra ml`.

## Editor and apps

**Extension**
:   An add-on for VS Code, for example *Python*, *Remote - SSH* or *Dev Containers*.

**Profile**
:   A saved set of VS Code extensions and settings that you can import in one step.

**JupyterLab**
:   Notebooks, terminals and files in the browser. It runs inside the container.

**noVNC desktop**
:   A full Linux desktop in a browser tab, used here to run QGIS inside the container.
