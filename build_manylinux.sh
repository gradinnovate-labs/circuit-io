#!/bin/bash
set -e

echo "Installing cibuildwheel..."
pipx install cibuildwheel || pip install --user cibuildwheel

echo "Building manylinux wheels (10-20 minutes)..."
cibuildwheel --platform linux --output-dir wheelhouse

echo "Wheels in wheelhouse/:"
ls -lh wheelhouse/

echo "Upload with: ./upload_pypi.sh --test or --prod"
