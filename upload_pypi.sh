#!/bin/bash

# PyPI Upload Script
# Usage: ./upload_pypi.sh --test  or  ./upload_pypi.sh --prod

set -e

REPOSITORY_URL=""
TOKEN_ENV=""

if [ "$1" = "--test" ]; then
    REPOSITORY_URL="https://test.pypi.org/legacy/"
    TOKEN_ENV="PYPI_TEST_TOKEN"
    echo "Uploading to PyPI Test..."
elif [ "$1" = "--prod" ]; then
    REPOSITORY_URL="https://upload.pypi.org/legacy/"
    TOKEN_ENV="PYPI_PUB_TOKEN"
    echo "Uploading to PyPI Production..."
else
    echo "Error: Invalid argument"
    echo "Usage: $0 --test | --prod"
    exit 1
fi

if [ -z "${!TOKEN_ENV}" ]; then
    echo "Error: $TOKEN_ENV environment variable is not set"
    exit 1
fi

PYTHON_CMD=""

if [ -d ".venv" ] && [ -x ".venv/bin/python3" ]; then
    PYTHON_CMD=".venv/bin/python3"
    echo "Using existing .venv environment"
else
    PYTHON_CMD="python3"
    echo "Using system Python"
fi

echo "Building package..."
rm -rf dist/ build/
$PYTHON_CMD -m build

if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "Error: Build failed - no files in dist/"
    exit 1
fi

UPLOAD_DIR="dist/"

if [ -d "wheelhouse" ] && [ -n "$(ls -A wheelhouse/*.whl 2>/dev/null)" ]; then
    UPLOAD_DIR="wheelhouse/"
    echo "Found manylinux wheels in wheelhouse/"
else
    echo "No manylinux wheels found, uploading sdist only"
    echo "To build wheels: ./build_manylinux.sh"
fi

echo "Files to upload:"
ls -lh "$UPLOAD_DIR"

echo "Uploading..."
TWINE_USERNAME="__token__" \
TWINE_PASSWORD="${!TOKEN_ENV}" \
twine upload \
    --repository-url "$REPOSITORY_URL" \
    --verbose \
    "$UPLOAD_DIR"*.{whl,tar.gz}

echo "Upload complete!"
