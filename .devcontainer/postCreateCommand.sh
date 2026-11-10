#!/usr/bin/env bash
set -euo pipefail

# Create .venv from uv.lock (or resolve it the first time) and install the package in editable mode
if [ -f uv.lock ]; then
  uv sync --all-groups --locked
else
  uv sync --all-groups
fi

# The workspace is owned by your host user; let git trust it inside the container
git config --global --add safe.directory "$(pwd)"

# Install the git hooks (needs a git repository)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  uv run pre-commit install
  # Pre-build the hook environments; if that fails (e.g. no network), it is retried on the first commit
  uv run pre-commit install-hooks || echo "Warning: pre-commit hook environments not built yet; they are retried on the first commit."
else
  echo "Note: $(pwd) is not a git repository yet, so the pre-commit hooks were not installed."
  echo "      Run 'git init -b main' and then 'make install'."
fi

# Auto-activate the project venv in new terminals
for rc in "${HOME}/.bashrc" "${HOME}/.zshrc"; do
  [ -f "$rc" ] || continue
  if ! grep -q "AUTO_ACTIVATE_VENV" "$rc"; then
    cat <<'RC' >> "$rc"

# AUTO_ACTIVATE_VENV
if [ -z "${VIRTUAL_ENV:-}" ] && [ -n "${UV_PROJECT_ENVIRONMENT:-}" ] && [ -f "${UV_PROJECT_ENVIRONMENT}/bin/activate" ]; then
  . "${UV_PROJECT_ENVIRONMENT}/bin/activate"
fi
RC
  fi
done

echo "Dev container ready. Try: make help"
