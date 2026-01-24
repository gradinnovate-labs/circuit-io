# circuit_io

Circuit I/O library with multi-format support (Bookshelf, LEF/DEF, Verilog).

## Features

- **Multi-format support**: Read IC design files in Bookshelf, LEF+DEF, Verilog, and mixed formats
- **Elegant Python API**: Intuitive function-based interface instead of command-line arguments
- **Cross-platform**: Wheels built for Linux x86_64 (manylinux2014, manylinux2_17)
- **Multi-Python**: Support for Python 3.8, 3.9, 3.10, 3.11, 3.12
- **ABI compatibility**: Both old ABI (CXX11_ABI=0) and new ABI (CXX11_ABI=1) supported
- **Backward compatible**: Legacy `forward()` function still works

## Installation


### From Source

```bash
git clone https://github.com/gradinnovate-labs/circuit-io.git
cd circuit-io

# Option 1: Recommended - use uv (faster)
uv pip install .

# Option 2: Use pip
pip install .
```

**Note**: The build process is handled automatically by `scikit-build-core`. You don't need to run CMake manually.

### SKILL Installation

#### Option A: For Claude Code users

Copy the skills to your project's `.claude/skills/` directory:

```bash
# Copy all skills
cp -r /path/to/EDA-Skills/.claude/skills/* .claude/skills/
```

#### Option B: For OpenCode users

Copy the skills to your project's `.opencode/skills/` directory:

```bash
# Copy all skills
cp -r /path/to/EDA-Skills/.claude/skills/* .opencode/skills/
```
