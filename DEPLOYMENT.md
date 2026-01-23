# PyPI Deployment Guide

This guide explains how to set up and use the PyPI deployment workflows.

## GitHub Repository Secrets

Before using the deployment workflows, you need to add the following secrets to your GitHub repository:

### Required Secrets

| Secret Name | Purpose | Where to get it |
|--------------|---------|------------------|
| `PYPI_PUB_TOKEN` | Publish to Production PyPI | Create at https://pypi.org/manage/account/token/ |
| `PYPI_TEST_TOKEN` | Publish to TestPyPI | Create at https://test.pypi.org/manage/account/token/ |

### How to Add Secrets

1. Go to your GitHub repository: `https://github.com/your-org/circuit-io/settings/secrets/actions`
2. Click "New repository secret"
3. Add each secret:

#### For Production PyPI Token:
```
Name: PYPI_PUB_TOKEN
Value: pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### For TestPyPI Token:
```
Name: PYPI_TEST_TOKEN
Value: pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Important**: Keep these tokens secret! Never commit them to your repository.

## GitHub Actions Workflows

### 1. Build Wheels Workflow (`.github/workflows/build-wheels.yml`)

**Triggers:**
- Push to `main` branch
- Push to version tags (e.g., `v0.1.0`)
- Pull requests to `main`
- Manual trigger (workflow_dispatch)

**What it does:**
- Builds wheels for multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Builds both ABI variants (0 and 1)
- Runs on Ubuntu (Linux x86_64)
- Uploads wheels as GitHub artifacts

**How to trigger manually:**
```bash
gh workflow run build-wheels.yml -r main
```

**Matrix Build:**
- Python: 3.8, 3.9, 3.10, 3.11, 3.12
- ABI: 0, 1
- Excludes invalid combinations (e.g., Python <3.10 with ABI=1)

### 2. Publish Workflow (`.github/workflows/publish.yml`)

**Triggers:**
- Push to version tags starting with `v` (auto-publish to production)
- Manual trigger (workflow_dispatch for testing)

**What it does:**
- Downloads all built wheels
- Publishes to Production PyPI (using `PYPI_PUB_TOKEN`)
- Has manual trigger to test with TestPyPI (using `PYPI_TEST_TOKEN`)

**How to trigger test publish:**
```bash
# Publish to TestPyPI (testing environment)
gh workflow run publish.yml -f publish_test -r main
```

## Release Process

### Step 1: Create Version Tag

```bash
# Update version in pyproject.toml
# Then tag and push
git tag v0.1.0
git push origin v0.1.0
```

### Step 2: Build Wheels (Automatic or Manual)

```bash
# Automatic: On tag push, build-wheels.yml runs automatically

# Manual: Trigger via GitHub CLI
gh workflow run build-wheels.yml -r main
```

### Step 3: Test Locally (Optional but Recommended)

```bash
# Download wheels from GitHub Actions
gh run-id <run-id> download

# Install and test
pip install place_io-0.1.0-*.whl
python3 test_new_api.py
```

### Step 4: Publish to PyPI

```bash
# Automatic: On tag push, publish.yml runs automatically
# This publishes to Production PyPI using PYPI_PUB_TOKEN

# Or manual test publish (to TestPyPI):
gh workflow run publish.yml -f publish_test -r main
```

## Wheel Naming Convention

The workflows generate wheels with the following naming convention:

```
place_io-<python_version>-<platform>-<abi>.whl
```

Examples:
```
place_io-0.1.0-cp38-cp38-manylinux2014_x86_64.whl  (ABI=0)
place_io-0.1.0-cp39-cp39-manylinux2014_x86_64.whl     (ABI=0)
place_io-0.1.0-cp310-cp310-manylinux2014_x86_64.whl   (ABI=0)
place_io-0.1.0-cp311-cp311-manylinux2014_x86_64.whl   (ABI=0)
place_io-0.1.0-cp311-cp311-manylinux2_17_x86_64.whl (ABI=1)
```

## PyPI Packages

Two packages will be published to PyPI:

1. **place_io** (default, ABI=0)
   - For Python 3.8, 3.9, 3.10
   - Maximum compatibility with older NumPy
   - Default when installing: `pip install place_io`

2. **place_io_cxx11** (new ABI)
   - For Python 3.11, 3.12
   - Required for NumPy >= 2.0
   - Must install explicitly: `pip install place_io_cxx11`

## Users

Users should choose the appropriate package based on their Python and NumPy versions:

```bash
# For Python 3.8-3.10 with any NumPy
pip install place_io

# For Python 3.11+ with NumPy 2.0+
pip install place_io_cxx11
```

## Troubleshooting

### Build fails
- Check GitHub Actions logs: `.github/workflows/build-wheels.yml`
- Common issues: Missing dependencies, CMake errors, pybind11 errors

### Publish fails
- Verify secrets are set correctly
- Check if PyPI token is expired
- Test with TestPyPI first before Production PyPI

### ImportError after install
- Check Python version: `python3 --version`
- Check NumPy version: `python3 -c "import numpy; print(numpy.__version__)"`
- Try the other package: `pip install place_io_cxx11`

## References

- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [TestPyPI](https://test.pypi.org/)
- [scikit-build Documentation](https://scikit-build.readthedocs.io/)
