"""Turn the template into your own project.

Usage:
    python scripts/rename_project.py my_project --author "Jane Doe" --email jane@example.org

Renames the package ``mypackage`` (folder, imports, configs, docs) and fills in the
author. Run it once, right after copying the template, then delete this script.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "mypackage"
SKIP_DIRS = {".git", ".venv", ".uv-cache", "node_modules", "site", "public", "__pycache__"}
TEXT_SUFFIXES = {".py", ".toml", ".md", ".yml", ".yaml", ".json", ".ini", ".cfg", ".txt", ".sh", ""}


def iter_text_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES and path.name != "uv.lock":
            files.append(path)
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="new package name, e.g. sar_flood or sar-flood")
    parser.add_argument("--author", help="author name for pyproject.toml and LICENSE")
    parser.add_argument("--email", help="author e-mail for pyproject.toml")
    args = parser.parse_args()

    dist_name = args.name.strip().lower().replace("_", "-")
    import_name = dist_name.replace("-", "_")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", import_name):
        parser.error("name must start with a letter and contain only letters, digits, '-' or '_'")

    for path in iter_text_files(ROOT):
        if path == Path(__file__).resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:  # binary file, e.g. .coverage
            continue
        new = text
        # distribution name in pyproject / mkdocs / devcontainer, then the import name everywhere else
        new = new.replace(f'name = "{OLD}"', f'name = "{dist_name}"')
        new = new.replace(f'"name": "{OLD}"', f'"name": "{dist_name}"')
        new = new.replace(f"site_name: {OLD}", f"site_name: {dist_name}")
        new = new.replace(f'version("{OLD}")', f'version("{dist_name}")')
        new = new.replace(OLD, import_name)
        if args.author:
            new = new.replace(
                '{ name = "Your Name", email = "you@example.com" }',
                f'{{ name = "{args.author}", email = "{args.email or "you@example.com"}" }}',
            )
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"updated  {path.relative_to(ROOT)}")

    old_pkg = ROOT / "src" / OLD
    if old_pkg.exists():
        old_pkg.rename(ROOT / "src" / import_name)
        print(f"renamed  src/{OLD} -> src/{import_name}")

    lock = ROOT / "uv.lock"
    if lock.exists():
        lock.unlink()
        print("removed  uv.lock (it is recreated by `uv sync`)")

    for cache in (".venv", ".mypy_cache", ".pytest_cache", ".ruff_cache"):
        shutil.rmtree(ROOT / cache, ignore_errors=True)

    print(f"\nDone. Package '{import_name}' (pip name '{dist_name}').")
    print("Next: review the README, rebuild the dev container, then `make check test`.")


if __name__ == "__main__":
    main()
