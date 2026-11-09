#!/usr/bin/env bash
set -euo pipefail

# Create .venv from uv.lock (or resolve it the first time) and install the package in editable mode
if [ -f uv.lock ]; then
  uv sync --all-groups --locked
else
  uv sync --all-groups
fi

# Install the git hooks
uv run pre-commit install --install-hooks

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
