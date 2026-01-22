# circuit-io C++ Components

This directory contains C++ components extracted from [DREAMPlace](https://github.com/limbo018/DREAMPlace).

## Components

### place_io

Python bindings for placement database (PlaceDB) using pybind11.

**Features:**
- LEF/DEF file parsing and writing
- Verilog file parsing
- Bookshelf format support
- Python bindings for PlaceDB and PyPlaceDB classes

**Source:** https://github.com/limbo018/DREAMPlace/tree/master/dreamplace/ops/place_io

**Build:**
```bash
cd place_io
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=$(pwd)/install
cmake --build build
cmake --install build
```

### utility

Utility library providing common functions and data structures.

**Features:**
- Timer utilities
- Logging functions
- Math utilities
- Memory management helpers

**Source:** https://github.com/limbo018/DREAMPlace/tree/master/dreamplace/ops/utility

**Build:**
```bash
cd utility
cmake -B build -S .
cmake --build build
```

### Limbo

Library for circuit design automation file parsing.

**Source:** https://github.com/limbo018/Limbo

**Components:**
- LEF parser
- DEF parser
- Verilog parser
- GDSII parser
- Bookshelf parser

**Build:**
```bash
cd Limbo
cmake -B build -S .
cmake --build build
```

## Dependencies

### Required
- CMake >= 3.15
- C++17 compiler
- Boost (graph, regex)
- ZLIB
- Python 3.x
- pybind11

### Optional
- Cairo (for drawing support)

## Project Structure

```
cpp/
├── place_io/        # Python bindings for PlaceDB
├── utility/          # Utility library
└── Limbo/            # File parsing libraries (git submodule)
```

## License

See component-specific license files.
