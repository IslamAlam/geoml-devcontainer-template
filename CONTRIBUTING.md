# Contributing

1. Create a branch: `git checkout -b my-change`.
2. Work inside the dev container (see `README.md`).
3. Add tests for new code in `tests/`.
4. Run `make check` and `make test`.
5. Push and open a merge request. CI runs ruff, mypy and pytest in the same image.

Please keep `uv.lock` in sync (`uv lock`) whenever `pyproject.toml` changes.
