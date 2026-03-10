# macOS fixes for HW2 (`hw2_robot_control_mdps`)

This document lists the macOS-specific issues we hit and the fixes that work.

## 1) Use Python 3.12 venv

From project root:

```bash
python3.12 -m venv mujoco
source mujoco/bin/activate
python --version
```

Expected: `Python 3.12.x`

## 2) `pip` SSL certificate errors on PyPI

If you see errors like:

- `SSLCertVerificationError`
- `Could not fetch URL https://pypi.org/simple/...`

Install with trusted hosts:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .
```

## 3) `launch_passive` on macOS requires `mjpython`

If you see:

- ``RuntimeError: `launch_passive` requires that the Python script be run under `mjpython` on macOS``

Run scripts with:

```bash
mjpython scripts/inverse_kinematics.py
```

## 4) `mjpython` fails: missing `libpython3.12.dylib`

If you see:

- `Library not loaded: @rpath/libpython3.12.dylib`
- `Reason: tried ... mujoco/libpython3.12.dylib (no such file)`

Create the expected symlink in the venv root:

```bash
ln -sf /Users/platztreapn/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/libpython3.12.dylib \
  mujoco/libpython3.12.dylib
```

Then retry:

```bash
source mujoco/bin/activate
mjpython scripts/inverse_kinematics.py
```
