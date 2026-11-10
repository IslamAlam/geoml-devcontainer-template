# Getting started

From an empty folder to a GPU-ready package with JupyterLab and QGIS.
You need VS Code with the *Remote - SSH* and *Dev Containers* extensions, and a Linux server
with Docker, the NVIDIA driver and the NVIDIA Container Toolkit.

## 1. Connect to the GPU server

In VS Code, open the **Remote Explorer**, expand **SSH** and click the arrow next to your server
(here `pontus`) to connect. If the server is not listed, add it with
*Remote-SSH: Open SSH Configuration File…*.

![Remote Explorer with the SSH hosts](img/01-remote-ssh.png)

When connected, the status bar in the bottom-left shows `SSH: <server>`.

## 2. Make it your project

Open a terminal on the server (*Terminal → New Terminal*) and run:

```bash
git clone https://github.com/IslamAlam/geoml-devcontainer-template.git my_project
cd my_project
rm -rf .git
git init -b main
python3 scripts/rename_project.py my_project --author "Jane Doe" --email jane@example.org
rm scripts/rename_project.py
```

From the UniBw GitLab, clone with
`git clone ssh://git@git.unibw.de:2222/l91bisma/geoml-devcontainer-template.git my_project` instead.

`rename_project.py` renames the package `mypackage` everywhere (folder, imports, configs, docs)
and fills in the author. Run `git init` **before** opening the container: the container setup
installs the git hooks into this repository.

![Cloning the template and renaming the package](img/02-clone-and-rename.png)

## 3. Open the project folder

*File → Open Folder…* and select the new `my_project` folder on the server.

![Open Folder dialog on the server](img/03-open-folder.png)

## 4. Reopen it in the container

VS Code detects `.devcontainer/` and offers **Reopen in Container**:

![Reopen in Container notification](img/04-reopen-notification.png)

If you missed the notification, use the command palette (<kbd>F1</kbd> or
<kbd>Ctrl/Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) → **Dev Containers: Reopen in Container**.
After changing the `Dockerfile` or `devcontainer.json`, run **Dev Containers: Rebuild Container**
(from inside the container) or **Rebuild and Reopen in Container** (from the server).

![Dev Containers: Rebuild Container](img/05b-rebuild-command.png)

![Dev Containers commands in the command palette](img/05-reopen-command.png)

## 5. Wait for the first build

Click **show log** to follow progress. The first start pulls a large image and takes a few
minutes; later starts take seconds. Lines with `Exit code 1` in the log are normal checks, not errors.

![Connecting to the dev container, with the build log](img/06-connecting.png)

The container is ready when the status bar shows `Dev Container: my-project @ <server>` and the
setup terminal ends with `Dev container ready. Try: make help`.

## 6. Check that everything works

`make help` lists the available commands:

![make help](img/07-make-help.png)

Install the ML extra (PyTorch) and check Python, GDAL and the GPU:

```bash
uv sync --extra ml
make env
```

![make env showing CUDA and the GPU](img/08-make-env-gpu.png)

Run the tests and the code-quality checks:

```bash
make test
make check
```

![make test with coverage](img/09-make-test.png)

## JupyterLab and QGIS

The container keeps the image's own start command (`"overrideCommand": false`), so JupyterLab
runs on port 8888 next to your editor.

1. **Open JupyterLab.** In the **Ports** tab, VS Code has already forwarded port 8888.
   Click `localhost:8888` (or the globe icon) to open it in your browser.

    ![Ports tab with JupyterLab forwarded](img/10-ports.png)

2. **Log in with the token.** JupyterLab asks for a token:

    ![JupyterLab token page](img/11-jupyter-token-page.png)

    In a terminal in the container, run `jupyter server list` and open the printed URL, or paste
    the part after `token=` into the page:

    ![jupyter server list output, token blurred](img/12-jupyter-server-list.png)

3. **Start the desktop.** In the JupyterLab launcher, click **QGIS Desktop**. It opens an Xfce
   desktop (noVNC) in a new browser tab.

    ![JupyterLab launcher with QGIS Desktop](img/13-jupyterlab-launcher.png)

4. **Use QGIS, GRASS or SAGA.** They are under *Applications → Education*. Your project is at
   `/workspaces/my_project`, so QGIS sees exactly the files your code writes.

    ![QGIS on the Xfce desktop](img/14-qgis-desktop.png)

Without VS Code, forward the port yourself: `ssh -L 8888:localhost:8888 <server>`.

**PyQGIS:** QGIS's Python bindings live in the image's system Python, not in `.venv`. To use
`import qgis` from your project, create the venv with access to system packages:
`uv venv --system-site-packages && uv sync`.
