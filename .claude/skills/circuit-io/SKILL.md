---
name: circuit-io
description: Parse IC design files in Bookshelf, LEF/DEF, and Verilog formats. Extract circuit database with nodes, nets, placements, and floorplan information for VLSI placement and routing workflows.
license: MIT
metadata:
    skill-author: GradInnovate Labs
---

# Circuit I/O: IC Design File Parser

## Overview

Circuit I/O is a lightweight Python library for reading IC design files in multiple formats. Parse Bookshelf benchmarks, LEF/DEF industrial designs, Verilog netlists, and mixed-format designs. Extract circuit topology, placement information, and floorplan data with C++ backend performance and Python ease of use.

## When to Use This Skill

This skill should be used when:

- IC design files requiring parsing (Bookshelf, LEF/DEF, Verilog)
- Circuit topology extraction (nodes, nets, connections)
- Placement data reading from DEF files
- Floorplan and die area information needed
- ISPD benchmarks processing for placement research
- Industrial LEF/DEF file analysis
- Netlist analysis and validation
- Pre-processing for placement and routing tools

**Related Tools:** For advanced placement optimization and detailed routing analysis, consider using tools like DREAMPlace, OpenROAD, or commercial EDA tools as companions to Circuit I/O.

## Installation

```bash
pip install circuit_io
```

Requires Python 3.8 or later.

## Quick Start

### Reading Bookshelf Format

```python
import circuit_io

# Read ISPD benchmark (Bookshelf format)
db = circuit_io.read_bookshelf('adaptec1.aux')

# Access basic information
print(f"Design name: {db.designName()}")
print(f"Nodes: {len(db.nodes())}")
print(f"Nets: {len(db.nets())}")
print(f"Die area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")
```

### Reading LEF + DEF Format

```python
import circuit_io

# Read industrial design (LEF + DEF)
db = circuit_io.read_lef_def(['tech.lef', 'cells.lef'], 'design.def')

# Extract design statistics
print(f"Movable nodes: {db.numMovable()}")
print(f"Fixed nodes: {db.numFixed()}")
print(f"IO pins: {db.numIOPin()}")
print(f"Macros: {db.numMacro()}")
```

### Reading Verilog Format

```python
import circuit_io

# Read netlist (Verilog format)
db = circuit_io.read_verilog('design.v')

# Analyze netlist
print(f"Total nodes: {len(db.nodes())}")
print(f"Total nets: {len(db.nets())}")
```

## Core Workflows

### Reading Bookshelf Benchmarks

Bookshelf format is standard for ISPD placement contests.

**Basic Reading:**

```python
import circuit_io

# Single .aux file contains paths to all related files
db = circuit_io.read_bookshelf('design.aux')

# Design information
name = db.designName()
node_count = len(db.nodes())
net_count = len(db.nets())

# Die area
xl, yl = db.xl(), db.yl()
xh, yh = db.xh(), db.yh()
die_width = db.width()
die_height = db.height()

# Node statistics
movable = db.numMovable()
fixed = db.numFixed()
io_pins = db.numIOPin()
macros = db.numMacro()

# Site/row information
rows = db.rows()
utilization = db.computeMovableUtil()
```

**Accessing Node Information:**

```python
# Iterate through all nodes
for i in range(len(db.nodes())):
    node = db.node(i)
    prop = db.nodeProperty(node)

    name = prop.name()
    width = prop.width()
    height = prop.height()

    # Check node type
    if prop.isMovable():
        print(f"Movable: {name} ({width}x{height})")
    elif prop.isFixed():
        print(f"Fixed: {name} ({width}x{height})")
    elif prop.isIOPin():
        print(f"I/O: {name}")
    elif prop.isMacro():
        print(f"Macro: {name}")
```

**Accessing Net Information:**

```python
# Iterate through nets
for i in range(len(db.nets())):
    net = db.net(i)
    prop = db.netProperty(net)

    name = prop.name()
    node_count = len(prop.nodes())

    # Get connected nodes
    for j in range(node_count):
        node = prop.nodes()[j]
        node_prop = db.nodeProperty(node)
        print(f"  {node_prop.name()}")
```

### Reading LEF + DEF Designs

LEF/DEF is the standard industrial format for IC designs.

**Basic Reading:**

```python
import circuit_io

# LEF files: technology and cell library
lef_files = ['tech.lef', 'cells.lef']

# DEF file: design placement, routing, and connectivity
def_file = 'design.def'

# Read design
db = circuit_io.read_lef_def(lef_files, def_file)

# Design summary
print(f"Design: {db.designName()}")
print(f"Nodes: {len(db.nodes())}")
print(f"Nets: {len(db.nets())}")
print(f"Die area: ({db.xl()}, {db.yl()}) - ({db.xh()}, {db.yh()})")

# Placement information
print(f"Utilization: {db.computeMovableUtil():.2%}")
print(f"Movable: {db.numMovable()}, Fixed: {db.numFixed()}")
```

**Macro and Fixed Block Information:**

```python
# Access fixed blocks and macros
for i in range(len(db.nodes())):
    node = db.node(i)
    prop = db.nodeProperty(node)

    if prop.isFixed() or prop.isMacro():
        name = prop.name()
        x, y = prop.x(), prop.y()
        w, h = prop.width(), prop.height()
        orientation = prop.orientation()

        print(f"{name}: ({x}, {y}), {w}x{h}, {orientation}")
```

### Reading Verilog Netlists

Verilog files contain connectivity information without placement data.

**Basic Reading:**

```python
import circuit_io

# Read netlist
db = circuit_io.read_verilog('design.v')

# Extract netlist information
print(f"Module: {db.designName()}")
print(f"Instances: {len(db.nodes())}")
print(f"Nets: {len(db.nets())}")

# Analyze connectivity
for i in range(len(db.nets())):
    net = db.net(i)
    prop = db.netProperty(net)

    # Get fanout (number of connected nodes)
    fanout = len(prop.nodes())
    print(f"Net {i} ({prop.name()}): {fanout} pins")
```

### Reading Mixed Format Designs

Complex designs often require LEF + DEF + Verilog.

**Complete Design Reading:**

```python
import circuit_io

# All three formats for complete design information
lef_files = ['tech.lef', 'cells.lef']
def_file = 'floorplan.def'
verilog_file = 'design.v'

# Read mixed format
db = circuit_io.read_mixed(lef_files, def_file, verilog_file)

# Now you have complete design:
# - Physical placement from DEF
# - Cell library from LEF
# - Full connectivity from Verilog
```

**Benefits of Mixed Format:**

- **LEF**: Cell dimensions, pin definitions, technology rules
- **DEF**: Component placement, routing information
- **Verilog**: Complete netlist, hierarchical information

### Accessing Floorplan Information

Floorplan defines placement regions and rows.

**Row Information:**

```python
rows = db.rows()

for i in range(len(rows)):
    row = rows[i]
    print(f"Row {i}:")
    print(f"  Origin: ({row.x()}, {row.y()})")
    print(f"  Size: {row.width()} x {row.height()}")
    print(f"  Site: {row.site()}")
```

**Site Information:**

```python
# Access site definitions (placement grid)
# Sites define where cells can be placed
for row in db.rows():
    site_name = row.site()
    print(f"Site: {site_name}")
```

### Extracting Placement Data

When DEF files contain placement information.

**Reading Node Positions:**

```python
# For nodes with placement information
for i in range(len(db.nodes())):
    node = db.node(i)
    prop = db.nodeProperty(node)

    if prop.isMovable() or prop.isFixed():
        x = prop.x()
        y = prop.y()
        width = prop.width()
        height = prop.height()

        # Get orientation (N, S, W, E, FN, FS, FW, FE)
        orientation = prop.orientation()

        print(f"{prop.name()}: ({x}, {y}), {width}x{height}, {orientation}")
```

### Legacy API (DREAMPlace Compatible)

For backward compatibility with existing DREAMPlace code.

**Command-Line Style Arguments:**

```python
import circuit_io

# Legacy API using argument list
args = ['DREAMPlace',
        '--bookshelf_aux_input', 'adaptec1.aux',
        '--lef_input', 'tech.lef cells.lef',
        '--def_input', 'design.def']

db = circuit_io.forward(args)

# Access database as usual
print(f"Design: {db.designName()}")
```

**Migration to New API:**

```python
# Old way (legacy)
args = ['DREAMPlace', '--bookshelf_aux_input', 'design.aux']
db = circuit_io.forward(args)

# New way (recommended)
db = circuit_io.read_bookshelf('design.aux')
```

## Error Handling

Handle common Circuit I/O exceptions appropriately.

```python
import circuit_io

try:
    # Try reading Bookshelf
    db = circuit_io.read_bookshelf('design.aux')

except Exception as e:
    print(f"Error reading file: {e}")
    # Check if file exists
    import os
    if not os.path.exists('design.aux'):
        print("AUX file not found")
    else:
        print("Check file format and contents")
```

## Common Use Cases

### Analyzing Benchmark Characteristics

Quick analysis of design benchmarks:

```python
import circuit_io

# Read benchmark
db = circuit_io.read_bookshelf('benchmark.aux')

# Print comprehensive statistics
print("=" * 60)
print(f"Design: {db.designName()}")
print("=" * 60)
print(f"Die Area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")
print(f"Die Size: {db.width()} x {db.height()}")
print()
print(f"Nodes: {len(db.nodes())}")
print(f"  - Movable: {db.numMovable()}")
print(f"  - Fixed: {db.numFixed()}")
print(f"  - I/O Pins: {db.numIOPin()}")
print(f"  - Macros: {db.numMacro()}")
print()
print(f"Nets: {len(db.nets())}")
print(f"Rows: {len(db.rows())}")
print(f"Utilization: {db.computeMovableUtil():.2%}")
```

### Comparing Multiple Designs

Batch analysis of multiple benchmarks:

```python
import circuit_io
from pathlib import Path
import pandas as pd

benchmarks = [
    'adaptec1.aux',
    'adaptec2.aux',
    'adaptec3.aux',
    'adaptec4.aux'
]

results = []
for aux_file in benchmarks:
    db = circuit_io.read_bookshelf(aux_file)

    results.append({
        'Design': db.designName(),
        'Nodes': len(db.nodes()),
        'Nets': len(db.nets()),
        'Die': f"{db.width()}x{db.height()}",
        'Util': f"{db.computeMovableUtil():.1%}"
    })

df = pd.DataFrame(results)
print(df)
```

### Extracting Netlist for Analysis

Export connectivity information:

```python
import circuit_io

db = circuit_io.read_bookshelf('design.aux')

# Build netlist dictionary
netlist = {}

for i in range(len(db.nets())):
    net = db.net(i)
    prop = db.netProperty(net)

    # Get all connected nodes
    nodes = []
    for j in range(len(prop.nodes())):
        node = prop.nodes()[j]
        node_prop = db.nodeProperty(node)
        nodes.append(node_prop.name())

    netlist[prop.name()] = nodes

# Print high-fanout nets
for net_name, connected_nodes in sorted(netlist.items(),
                                        key=lambda x: len(x[1]),
                                        reverse=True)[:10]:
    print(f"{net_name}: {len(connected_nodes)} pins")
```

### Analyzing Placement Quality

When reading DEF with placement data:

```python
import circuit_io

db = circuit_io.read_lef_def(['tech.lef', 'cells.lef'], 'design.def')

# Check placement coverage
placed_count = 0
for i in range(len(db.nodes())):
    node = db.node(i)
    prop = db.nodeProperty(node)

    if prop.isMovable():
        x, y = prop.x(), prop.y()
        # Verify position is within die area
        if db.xl() <= x < db.xh() and db.yl() <= y < db.yh():
            placed_count += 1

coverage = placed_count / db.numMovable() * 100
print(f"Placement coverage: {coverage:.1f}%")
```

### Converting Data for Processing

Extract NumPy arrays for machine learning:

```python
import circuit_io
import numpy as np

db = circuit_io.read_bookshelf('design.aux')

# Extract node features
node_features = []
for i in range(len(db.nodes())):
    node = db.node(i)
    prop = db.nodeProperty(node)

    features = [
        prop.width(),
        prop.height(),
        prop.isMovable(),
        prop.isFixed(),
        prop.isMacro()
    ]
    node_features.append(features)

node_array = np.array(node_features)
print(f"Node features shape: {node_array.shape}")
```

## Best Practices

1. **File path handling**: Always use absolute paths when reading designs
2. **Memory efficiency**: Large designs (>1M nodes) may require significant memory
3. **Format selection**: Use the most appropriate API for your format:
   - Bookshelf benchmarks: `read_bookshelf()`
   - Industrial designs: `read_lef_def()`
   - Netlist only: `read_verilog()`
   - Complete designs: `read_mixed()`
4. **Error checking**: Validate file existence before reading
5. **Data validation**: Verify node/net counts after reading
6. **Legacy migration**: Convert legacy `forward()` calls to new APIs

## Advanced Topics

### Understanding Design Databases

Circuit I/O provides a unified database interface across all formats.

**Database Attributes:**
- `designName()`: Design identifier
- `nodes()`: List of all nodes
- `nets()`: List of all nets
- `rows()`: List of placement rows
- Die area: `xl()`, `yl()`, `xh()`, `yh()`, `width()`, `height()`

**Node Properties:**
- `name()`: Node name
- `width()`, `height()`: Cell dimensions
- `x()`, `y()`: Placement position (if available)
- `orientation()`: Cell rotation (N, S, E, W, FN, FS, FE, FW)
- Type checks: `isMovable()`, `isFixed()`, `isIOPin()`, `isMacro()`

**Net Properties:**
- `name()`: Net name
- `nodes()`: List of connected nodes

**Row Properties:**
- `x()`, `y()`: Row origin
- `width()`, `height()`: Row dimensions
- `site()`: Site name

### Format Comparison

| Format | Typical Use | Strengths | Limitations |
|--------|-------------|-----------|-------------|
| **Bookshelf** | ISPD benchmarks | Simple, standardized | Limited to placement |
| **LEF/DEF** | Industrial designs | Complete physical data | Complex format |
| **Verilog** | Netlist analysis | Pure connectivity | No placement info |
| **Mixed** | Complete designs | All information available | Multiple files required |

### Detailed API Reference

For comprehensive API documentation including all parameters, methods, and data structures, consult the detailed reference file:

**Read:** `references/api_reference.md`

The reference includes:
- Complete Database class documentation
- All read functions (read_bookshelf, read_lef_def, read_verilog, read_mixed)
- Node and Net property classes
- Row and Site information
- Extended example workflows

## Integration Notes

**NumPy Arrays**: Extract data for numerical analysis using NumPy
```python
import numpy as np
# Convert node properties to arrays
node_sizes = np.array([db.nodeProperty(node).width() * db.nodeProperty(node).height()
                       for node in db.nodes()])
```

**Pandas DataFrames**: Convert design statistics for reporting:
```python
import pandas as pd
df = pd.DataFrame({
    'name': [db.nodeProperty(node).name() for node in db.nodes()],
    'width': [db.nodeProperty(node).width() for node in db.nodes()],
    'height': [db.nodeProperty(node).height() for node in db.nodes()]
})
```

**DREAMPlace Integration**: Legacy `forward()` API ensures compatibility with DREAMPlace-based research code

**File Formats**:
- Bookshelf: ISPD placement contest standard
- LEF: Library Exchange Format (cell definitions)
- DEF: Design Exchange Format (placement, routing)
- Verilog: Hardware description language (netlists)

## Troubleshooting

**Problem:** "File not found error"
**Solution:** Use absolute paths and verify file existence with `os.path.exists()`

**Problem:** "Mismatch between LEF and DEF"
**Solution:** Ensure LEF files contain all cell definitions referenced in DEF

**Problem:** "Empty database after reading"
**Solution:** Check if file format matches the API used (e.g., using read_lef_def on Verilog file)

**Problem:** "Out of memory with large designs"
**Solution:** Process designs in smaller chunks or use machines with more RAM

**Problem:** "Missing node positions"
**Solution:** Verilog files don't contain placement; use LEF+DEF or DEF files

## Summary

Circuit I/O provides essential IC design file parsing capabilities for VLSI research and EDA workflows. Use it for reading Bookshelf benchmarks, industrial LEF/DEF designs, Verilog netlists, and mixed-format designs. The library combines C++ performance with Python ease of use, making it ideal for placement research, design analysis, and pre-processing for advanced EDA tools.

