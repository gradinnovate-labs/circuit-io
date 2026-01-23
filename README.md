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

### From PyPI (Recommended)

```bash
# Install from PyPI
pip install circuit_io

# Note: By default installs ABI=0 (old C++ ABI) for maximum compatibility
# For new ABI, install: circuit_io_cxx11
```

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

## Usage

### New API (Recommended)

```python
import circuit_io

# 1. Read Bookshelf format (ISPD benchmarks)
db = circuit_io.read_bookshelf('path/to/design.aux')

# 2. Read LEF + DEF format (Industrial designs)
db = circuit_io.read_lef_def(['tech.lef', 'cells.lef'], 'design.def')

# 3. Read Verilog format (Netlist analysis)
db = circuit_io.read_verilog('path/to/design.v')

# 4. Read mixed format (LEF + DEF + Verilog for complex designs)
db = circuit_io.read_mixed(
    ['tech.lef', 'cells.lef'],  # LEF files
    'floorplan.def',                # DEF file
    'design.v'                     # Verilog file
)

# Access database properties
print(f"Design name: {db.designName()}")
print(f"Number of nodes: {len(db.nodes())}")
print(f"Number of nets: {len(db.nets())}")
print(f"Die area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")
```

### Legacy API (Backward Compatible)

```python
import circuit_io

# Old command-line style (still works for compatibility)
args = ['DREAMPlace', '--bookshelf_aux_input', 'adaptec1.aux']
db = circuit_io.forward(args)
```

## API Comparison

| API | Pros | Cons | Recommended For |
|-----|-------|-------|---------------|
| `read_bookshelf(aux)` | Simple, single param | Bookshelf only | ISPD benchmarks |
| `read_lef_def(lef, def)` | Explicit, clear | LEF+DEF only | Industrial LEF/DEF designs |
| `read_verilog(v)` | Simple, single param | Verilog only | Netlist analysis |
| `read_mixed(lef, def, v)` | Most flexible | More params | **mgc_des_perf_1** type designs |
| `forward(args)` | Compatible with old code | Complex CLI | Existing DREAMPlace code |

## Platform and ABI Support

### Available Wheels

| Platform | Python 3.8 | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----------|-------------|-------------|----------------|----------------|----------------|
| Linux x86_64 (manylinux2014) | ✅ cp38 | ✅ cp39 | ✅ cp310 | ✅ cp311 | ✅ cp312 |
| Linux x86_64 (manylinux2_17) | ✅ cp38 | ✅ cp39 | ✅ cp310 | ✅ cp311 | ✅ cp312 |
| macOS x86_64 | ✅ cp38 | ✅ cp39 | ✅ cp310 | ✅ cp311 | ✅ cp312 |

### ABI Notes

- **ABI=0 (default)**: Compatible with older NumPy (<2.0), C++11 ABI=0
- **ABI=1** (`circuit_io_cxx11` package): Required for newer NumPy (>=2.0), C++11 ABI=1

## Development

### Building Wheels Locally

```bash
# Option 1: Recommended - use uv
uv pip install .

# Option 2: Use pip
pip install .

# Option 3: For GitHub Actions CI
pip install scikit-build-core pybind11 cibuildwheel
python -m pip wheel . --no-build-isolation -w wheelhouse
```

### Running Tests

```bash
# Run test script (requires built module)
python3 test_circuit_io.py
```

## Benchmark Support

Successfully tested on:

| Benchmark | Format | Nodes | Nets | Status |
|-----------|---------|--------|-------|--------|
| adaptec1 | Bookshelf | 211K | 221K | ✅ Passed |
| mgc_des_perf_1 | LEF+DEF+Verilog | 113K | 113K | ✅ Passed |
| ispd19_test2 | LEF+DEF | 73K | 72K | ✅ Passed |

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Acknowledgment

This library uses parts of the source code from [DREAMPlace](https://github.com/limbo018/DREAMPlace).


