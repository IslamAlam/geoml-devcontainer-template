"""Print what the container provides: Python, GDAL, GPU.

Run with: uv run python examples/check_environment.py
"""

import importlib
import platform
import shutil
import subprocess


def main() -> None:
    print(f"Python      {platform.python_version()}")

    gdal = shutil.which("gdalinfo")
    if gdal:
        out = subprocess.run([gdal, "--version"], capture_output=True, text=True, check=False)  # noqa: S603
        print(f"GDAL (sys)  {out.stdout.strip()}")
    else:
        print("GDAL (sys)  not found")

    for name in ("rasterio", "torch"):
        try:
            module = importlib.import_module(name)
        except ImportError:
            print(f"{name:<11} not installed (uv sync --extra {'geo' if name == 'rasterio' else 'ml'})")
            continue
        print(f"{name:<11} {module.__version__}")
        if name == "rasterio":
            print(f"  GDAL      {module.__gdal_version__} (bundled with the wheel)")
        if name == "torch":
            available = module.cuda.is_available()
            print(f"  CUDA      {'available' if available else 'NOT available'}")
            if available:
                print(f"  GPU       {module.cuda.get_device_name(0)}")

    if shutil.which("nvidia-smi") is None:
        print("nvidia-smi  not found (no GPU passed to the container?)")


if __name__ == "__main__":
    main()
