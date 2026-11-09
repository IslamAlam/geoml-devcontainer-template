# Development

The full guide is in the repository's `README.md`. In short:

1. Open the project in VS Code and run **Dev Containers: Reopen in Container**.
2. `make env` to check Python, GDAL and the GPU.
3. Add dependencies with `uv add <package>`; never `pip install` by hand.
4. `make check` and `make test` before pushing; pre-commit runs on every commit.
5. `make docs` serves this documentation locally.

## Writing documentation

Docstrings use the Google style and are rendered by mkdocstrings on the
[API reference](api.md) page. Add a page under `docs/` and list it in `mkdocs.yml` under `nav`.
