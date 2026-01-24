# Circuit I/O API Reference

## Overview

Circuit I/O is a Python library for reading IC design files in multiple formats: Bookshelf, LEF/DEF, and Verilog. It provides a C++ backend with Python bindings for high-performance parsing of VLSI design data.

## Installation

```bash
pip install circuit_io
```

Supports Python 3.8 and later.

## Module-Level Functions

### read_bookshelf()

```python
read_bookshelf(aux_file)
```

Read an ISPD benchmark in Bookshelf format from an .aux file.

**Parameters:**
- `aux_file` (str): Path to the Bookshelf .aux file

**Returns:**
- `PlaceDB`: A placement database object containing the design

**Example:**
```python
import circuit_io

# Read ISPD benchmark
db = circuit_io.read_bookshelf('adaptec1.aux')

# Access design information
print(f"Design: {db.designName()}")
print(f"Nodes: {len(db.nodes())}")
```

### read_lef_def()

```python
read_lef_def(lef_files, def_file)
```

Read an industrial design in LEF + DEF format.

**Parameters:**
- `lef_files` (list): List of LEF file paths (e.g., ['tech.lef', 'cells.lef'])
- `def_file` (str): Path to the DEF file

**Returns:**
- `PlaceDB`: A placement database object containing the design

**Example:**
```python
import circuit_io

# Read LEF and DEF files
db = circuit_io.read_lef_def(['tech.lef', 'cells.lef'], 'design.def')

# Access placement information
print(f"Movable nodes: {db.numMovable()}")
print(f"Fixed nodes: {db.numFixed()}")
```

### read_verilog()

```python
read_verilog(verilog_file)
```

Read a netlist in Verilog format.

**Parameters:**
- `verilog_file` (str): Path to the Verilog file

**Returns:**
- `PlaceDB`: A placement database object containing the netlist

**Example:**
```python
import circuit_io

# Read Verilog netlist
db = circuit_io.read_verilog('design.v')

# Analyze connectivity
print(f"Nets: {len(db.nets())}")
```

### read_mixed()

```python
read_mixed(lef_files, def_file, verilog_file)
```

Read a complete design in mixed format (LEF + DEF + Verilog).

**Parameters:**
- `lef_files` (list): List of LEF file paths
- `def_file` (str): Path to the DEF file
- `verilog_file` (str): Path to the Verilog file

**Returns:**
- `PlaceDB`: A placement database object containing the complete design

**Example:**
```python
import circuit_io

# Read complete design
db = circuit_io.read_mixed(
    ['tech.lef', 'cells.lef'],
    'floorplan.def',
    'design.v'
)

# Access all design information
print(f"Design: {db.designName()}")
print(f"Nodes: {len(db.nodes())}")
print(f"Nets: {len(db.nets())}")
```

### forward()

```python
forward(args)
```

Legacy function for reading designs using command-line arguments (DREAMPlace compatibility).

**Parameters:**
- `args` (list): List of command-line arguments

**Returns:**
- `PlaceDB`: A placement database object

**Example:**
```python
import circuit_io

# Legacy API
args = ['DREAMPlace', '--bookshelf_aux_input', 'adaptec1.aux']
db = circuit_io.forward(args)
```

### write()

```python
write(db, filename, format, x, y)
```

Write a placement solution to a file.

**Parameters:**
- `db` (PlaceDB): The placement database
- `filename` (str): Output file path
- `format` (SolutionFileFormat): Output format (DEF, DEFSIMPLE, BOOKSHELF, BOOKSHELFALL)
- `x` (numpy.ndarray): X-coordinates for movable nodes
- `y` (numpy.ndarray): Y-coordinates for movable nodes

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
import circuit_io
import numpy as np

# Read design
db = circuit_io.read_bookshelf('design.aux')

# Generate placement solution
x = np.random.rand(db.numMovable()) * db.width()
y = np.random.rand(db.numMovable()) * db.height()

# Write to DEF file
circuit_io.write(db, 'output.def',
                 circuit_io.DEF,
                 x, y)
```

### apply()

```python
apply(db, x, y)
```

Apply a placement solution to the database in-place.

**Parameters:**
- `db` (PlaceDB): The placement database (modified in-place)
- `x` (numpy.ndarray): X-coordinates for movable nodes
- `y` (numpy.ndarray): Y-coordinates for movable nodes

**Example:**
```python
import circuit_io
import numpy as np

# Read design
db = circuit_io.read_bookshelf('design.aux')

# Apply new placement
x = np.random.rand(db.numMovable()) * db.width()
y = np.random.rand(db.numMovable()) * db.height()
circuit_io.apply(db, x, y)

# Nodes are now updated with new positions
```

### pydb()

```python
pydb(db)
```

Convert a PlaceDB object to PyPlaceDB format (for advanced usage).

**Parameters:**
- `db` (PlaceDB): The placement database

**Returns:**
- `PyPlaceDB`: PyPlaceDB object with additional NumPy array views

**Example:**
```python
import circuit_io

# Read design
db = circuit_io.read_bookshelf('design.aux')

# Convert to PyPlaceDB for NumPy array access
pydb = circuit_io.pydb(db)
```

## PlaceDB Class

The `PlaceDB` class is the primary container for design data.

### Design Information Methods

#### designName()

```python
designName()
```

Returns the design name.

**Returns:**
- `str`: Design name

### Die Area Methods

#### xl(), yl(), xh(), yh()

```python
xl()
yl()
xh()
yh()
```

Return the die area boundaries.

**Returns:**
- `int`: Lower-left or upper-right coordinate

**Example:**
```python
print(f"Die area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")
```

#### width(), height()

```python
width()
height()
```

Return die dimensions.

**Returns:**
- `int`: Width or height

### Node Access Methods

#### nodes()

```python
nodes()
```

Return list of all nodes.

**Returns:**
- `list[Node]`: List of Node objects

#### node()

```python
node(index)
```

Get a specific node by index.

**Parameters:**
- `index` (int): Node index

**Returns:**
- `Node`: Node object

#### nodeProperty()

```python
nodeProperty(index)
nodeProperty(node)
```

Get node properties.

**Parameters:**
- `index` (int) or `node` (Node): Node identifier

**Returns:**
- `NodeProperty`: Node property object

**Example:**
```python
node = db.node(0)
prop = db.nodeProperty(node)
print(f"Node name: {prop.name()}")
print(f"Width: {prop.width()}, Height: {prop.height()}")
```

#### nodeName()

```python
nodeName(index)
nodeName(node)
```

Get node name.

**Returns:**
- `str`: Node name

#### numMovable()

```python
numMovable()
```

Return number of movable nodes.

**Returns:**
- `int`: Count of movable nodes

#### numFixed()

```python
numFixed()
```

Return number of fixed nodes.

**Returns:**
- `int`: Count of fixed nodes

#### numMacro()

```python
numMacro()
```

Return number of macro cells.

**Returns:**
- `int`: Count of macros

#### numIOPin()

```python
numIOPin()
```

Return number of I/O pins.

**Returns:**
- `int`: Count of I/O pins

#### movableNodeIndices(), fixedNodeIndices()

```python
movableNodeIndices()
fixedNodeIndices()
```

Return indices of movable or fixed nodes.

**Returns:**
- `list[int]`: List of node indices

### Net Access Methods

#### nets()

```python
nets()
```

Return list of all nets.

**Returns:**
- `list[Net]`: List of Net objects

#### net()

```python
net(index)
```

Get a specific net by index.

**Parameters:**
- `index` (int): Net index

**Returns:**
- `Net`: Net object

#### netProperty()

```python
netProperty(index)
netProperty(net)
```

Get net properties.

**Parameters:**
- `index` (int) or `net` (Net): Net identifier

**Returns:**
- `NetProperty`: Net property object

**Example:**
```python
net = db.net(0)
prop = db.netProperty(net)
print(f"Net name: {prop.name()}")
print(f"Pins: {len(prop.nodes())}")
```

#### setNetWeight()

```python
setNetWeight(index, weight)
```

Set net weight.

**Parameters:**
- `index` (int): Net index
- `weight` (float): Net weight

#### isIgnoredNet()

```python
isIgnoredNet(index)
isIgnoredNet(net)
```

Check if a net is ignored.

**Parameters:**
- `index` (int) or `net` (Net): Net identifier

**Returns:**
- `bool`: True if ignored

### Row and Site Methods

#### rows()

```python
rows()
```

Return list of placement rows.

**Returns:**
- `list[Row]`: List of Row objects

#### row()

```python
row(index)
```

Get a specific row by index.

**Parameters:**
- `index` (int): Row index

**Returns:**
- `Row`: Row object

#### site()

```python
site()
```

Return the site definition.

**Returns:**
- `Site`: Site object

#### siteArea()

```python
siteArea()
```

Return total site area.

**Returns:**
- `int`: Site area

#### rowHeight()

```python
rowHeight()
```

Return row height.

**Returns:**
- `int`: Row height

**Example:**
```python
rows = db.rows()
for i in range(min(3, len(rows))):
    row = db.row(i)
    print(f"Row {i}: ({row.xl()}, {row.yl()}) - ({row.xh()}, {row.yh()})")
```

### Placement and Utilization Methods

#### computeMovableUtil()

```python
computeMovableUtil()
```

Compute movable node utilization.

**Returns:**
- `float`: Utilization ratio (0.0 to 1.0)

#### computePinUtil()

```python
computePinUtil()
```

Compute pin utilization.

**Returns:**
- `float`: Pin utilization

#### totalMovableNodeArea()

```python
totalMovableNodeArea()
```

Return total area of movable nodes.

**Returns:**
- `int`: Total area

#### totalFixedNodeArea()

```python
totalFixedNodeArea()
```

Return total area of fixed nodes.

**Returns:**
- `int`: Total area

#### totalRowArea()

```python
totalRowArea()
```

Return total row area.

**Returns:**
- `int`: Total area

### Node Dimension Methods

#### minMovableNodeWidth()

```python
minMovableNodeWidth()
```

Return minimum width of movable nodes.

**Returns:**
- `int`: Minimum width

#### maxMovableNodeWidth()

```python
maxMovableNodeWidth()
```

Return maximum width of movable nodes.

**Returns:**
- `int`: Maximum width

#### avgMovableNodeWidth()

```python
avgMovableNodeWidth()
```

Return average width of movable nodes.

**Returns:**
- `float`: Average width

### Multi-Row Methods

#### numMultiRowMovable()

```python
numMultiRowMovable()
```

Return number of multi-row movable nodes.

**Returns:**
- `int`: Count of multi-row nodes

#### isMultiRowMovable()

```python
isMultiRowMovable(index)
isMultiRowMovable(node)
```

Check if a node is multi-row.

**Parameters:**
- `index` (int) or `node` (Node): Node identifier

**Returns:**
- `bool`: True if multi-row

### Routing Methods

#### numRoutingGrids()

```python
numRoutingGrids(direction)
```

Return number of routing grids.

**Parameters:**
- `direction` (Direction1DType): kX or kY

**Returns:**
- `int`: Number of grids

#### numRoutingLayers()

```python
numRoutingLayers()
```

Return number of routing layers.

**Returns:**
- `int`: Number of layers

#### routingGridOrigin()

```python
routingGridOrigin(direction)
```

Return routing grid origin.

**Parameters:**
- `direction` (Direction1DType): kX or kY

**Returns:**
- `int`: Grid origin coordinate

#### routingTileSize()

```python
routingTileSize(direction)
```

Return routing tile size.

**Parameters:**
- `direction` (Direction1DType): kX or kY

**Returns:**
- `int`: Tile size

### Unit Methods

#### lefUnit()

```python
lefUnit()
```

Return LEF unit.

**Returns:**
- `int`: LEF unit (distance)

#### lefVersion()

```python
lefVersion()
```

Return LEF version.

**Returns:**
- `str`: LEF version string

#### defUnit()

```python
defUnit()
```

Return DEF unit.

**Returns:**
- `int`: DEF unit (distance)

#### defVersion()

```python
defVersion()
```

Return DEF version.

**Returns:**
- `str`: DEF version string

### Index Map Methods

#### nodeName2Index()

```python
nodeName2Index()
```

Return name-to-index mapping for nodes.

**Returns:**
- `dict`: Node name to index mapping

#### macroName2Index()

```python
macroName2Index()
```

Return name-to-index mapping for macros.

**Returns:**
- `dict`: Macro name to index mapping

**Example:**
```python
# Get node index by name
node_map = db.nodeName2Index()
node_index = node_map['my_cell_name']
node = db.node(node_index)
```

### Group and Region Methods

#### groups()

```python
groups()
```

Return list of placement groups.

**Returns:**
- `list[Group]`: List of Group objects

#### group()

```python
group(index)
```

Get a specific group by index.

**Parameters:**
- `index` (int): Group index

**Returns:**
- `Group`: Group object

#### regions()

```python
regions()
```

Return list of placement regions.

**Returns:**
- `list[Region]`: List of Region objects

#### region()

```python
region(index)
```

Get a specific region by index.

**Parameters:**
- `index` (int): Region index

**Returns:**
- `Region`: Region object

### Macro Methods

#### macros()

```python
macros()
```

Return list of macro definitions.

**Returns:**
- `list[Macro]`: List of Macro objects

#### macro()

```python
macro(index)
```

Get a specific macro by index.

**Parameters:**
- `index` (int): Macro index

**Returns:**
- `Macro`: Macro object

#### macroPin()

```python
macroPin(index)
macroPin(pin)
```

Get macro pin.

**Parameters:**
- `index` (int) or `pin` (Pin): Macro pin identifier

**Returns:**
- `MacroPin`: Macro pin object

### Node Modification Methods

#### setNodeStatus()

```python
setNodeStatus(index, status)
```

Set node placement status.

**Parameters:**
- `index` (int): Node index
- `status` (PlaceStatusType): PLACED, FIXED, UNPLACED, or DUMMY_FIXED

#### setNodeMultiRowAttr()

```python
setNodeMultiRowAttr(index, attr)
```

Set node multi-row attribute.

**Parameters:**
- `index` (int): Node index
- `attr` (MultiRowAttrType): SINGLE_ROW, MULTI_ROW_ANY, MULTI_ROW_N, or MULTI_ROW_S

#### setNodeOrient()

```python
setNodeOrient(index, orientation)
```

Set node orientation.

**Parameters:**
- `index` (int): Node index
- `orientation` (OrientType): N, S, E, W, FN, FS, FE, or FW

## Node Class

### Geometry Methods

#### xl(), yl(), xh(), yh()

Return node bounding box coordinates.

**Returns:**
- `int`: Lower-left or upper-right coordinate

#### width(), height()

Return node dimensions.

**Returns:**
- `int`: Width or height

#### area()

Return node area.

**Returns:**
- `int`: Area

### Pin Methods

#### pins()

```python
pins()
```

Return list of pin indices.

**Returns:**
- `list[int]`: List of pin indices

#### pinPos()

```python
pinPos(pin, x, y)
pinPos(pin)
pinX(pin)
pinY(pin)
```

Calculate pin position.

**Parameters:**
- `pin` (Pin): Pin object
- `x`, `y` (int, optional): Node position (default: use node's current position)

**Returns:**
- `int` or `tuple`: Pin coordinate(s)

#### siteArea()

```python
siteArea()
```

Return node site area.

**Returns:**
- `int`: Site area

### Status Methods

#### status()

```python
status()
```

Return node placement status.

**Returns:**
- `PlaceStatus`: PLACED, FIXED, UNPLACED, or DUMMY_FIXED

#### setStatus()

```python
setStatus(status_type)
```

Set node placement status.

**Parameters:**
- `status_type` (PlaceStatusType): New status

### Orientation Methods

#### orient()

```python
orient()
```

Return node orientation.

**Returns:**
- `Orient`: N, S, E, W, FN, FS, FE, or FW

#### multiRowAttr()

```python
multiRowAttr()
```

Return multi-row attribute.

**Returns:**
- `MultiRowAttr`: SINGLE_ROW, MULTI_ROW_ANY, MULTI_ROW_N, or MULTI_ROW_S

### ID Method

#### id()

```python
id()
```

Return node ID.

**Returns:**
- `int`: Node ID

## NodeProperty Class

### Attribute Methods

#### name()

```python
name()
```

Return node name.

**Returns:**
- `str`: Node name

#### macroId()

```python
macroId()
```

Return macro cell ID.

**Returns:**
- `int`: Macro cell ID

## Net Class

### Pin Methods

#### pins()

```python
pins()
```

Return list of pin indices.

**Returns:**
- `list[int]`: List of pin indices

### Bounding Box Method

#### bbox()

```python
bbox()
```

Return net bounding box.

**Returns:**
- `BoxCoordinate`: Bounding box

### Weight Method

#### weight()

```python
weight()
```

Return net weight.

**Returns:**
- `float`: Net weight

### ID Method

#### id()

```python
id()
```

Return net ID.

**Returns:**
- `int`: Net ID

## NetProperty Class

### Name Method

#### name()

```python
name()
```

Return net name.

**Returns:**
- `str`: Net name

## Row Class

### Geometry Methods

#### xl(), yl(), xh(), yh()

Return row bounding box coordinates.

**Returns:**
- `int`: Lower-left or upper-right coordinate

#### width(), height()

Return row dimensions.

**Returns:**
- `int`: Width or height

### Attribute Methods

#### name()

```python
name()
```

Return row name.

**Returns:**
- `str`: Row name

#### macroName()

```python
macroName()
```

Return macro name associated with row.

**Returns:**
- `str`: Macro name

#### orient()

```python
orient()
```

Return row orientation.

**Returns:**
- `Orient`: Row orientation

### Site Methods

#### step()

```python
step()
```

Return site step size.

**Returns:**
- `int`: Step size

#### numSites()

```python
numSites()
```

Return number of sites in row.

**Returns:**
- `int`: Site count

### ID Method

#### id()

```python
id()
```

Return row ID.

**Returns:**
- `int`: Row ID

## Site Class

### Attribute Methods

#### name()

```python
name()
```

Return site name.

**Returns:**
- `str`: Site name

#### className()

```python
className()
```

Return site class name.

**Returns:**
- `str`: Class name

#### symmetry()

```python
symmetry()
```

Return site symmetry.

**Returns:**
- `str`: Symmetry string

### Size Methods

#### size()

```python
size()
```

Return site size as tuple.

**Returns:**
- `tuple`: (width, height)

#### width()

```python
width()
```

Return site width.

**Returns:**
- `int`: Width

#### height()

```python
height()
```

Return site height.

**Returns:**
- `int`: Height

## Macro Class

### Geometry Methods

#### xl(), yl(), xh(), yh()

Return macro bounding box coordinates.

**Returns:**
- `int`: Lower-left or upper-right coordinate

#### width(), height()

Return macro dimensions.

**Returns:**
- `int`: Width or height

### Attribute Methods

#### name()

```python
name()
```

Return macro name.

**Returns:**
- `str`: Macro name

#### className()

```python
className()
```

Return macro class name.

**Returns:**
- `str`: Class name

#### siteName()

```python
siteName()
```

Return site name.

**Returns:**
- `str`: Site name

#### edgeName()

```python
edgeName()
```

Return edge name.

**Returns:**
- `str`: Edge name

#### symmetry()

```python
symmetry()
```

Return macro symmetry.

**Returns:**
- `str`: Symmetry string

### Pin Methods

#### macroPins()

```python
macroPins()
```

Return list of macro pins.

**Returns:**
- `list[MacroPin]`: List of macro pins

#### macroPin()

```python
macroPin(index)
```

Get a specific macro pin.

**Parameters:**
- `index` (int): Macro pin index

**Returns:**
- `MacroPin`: Macro pin object

#### macroPinName2Index()

```python
macroPinName2Index()
```

Return name-to-index mapping for macro pins.

**Returns:**
- `dict`: Macro pin name to index mapping

### Origin and Obstruction Methods

#### initOrigin()

```python
initOrigin()
```

Return initial origin.

**Returns:**
- `tuple`: (x, y) origin coordinates

#### obs()

```python
obs()
```

Return macro obstruction.

**Returns:**
- `MacroObs`: Macro obstruction object

### ID Method

#### id()

```python
id()
```

Return macro ID.

**Returns:**
- `int`: Macro ID

## Pin Class

### ID Methods

#### nodeId()

```python
nodeId()
```

Return parent node ID.

**Returns:**
- `int`: Node ID

#### netId()

```python
netId()
```

Return connected net ID.

**Returns:**
- `int`: Net ID

#### macroPinId()

```python
macroPinId()
```

Return macro pin ID.

**Returns:**
- `int`: Macro pin ID

### Offset Method

#### offset()

```python
offset()
```

Return pin offset from node origin.

**Returns:**
- `tuple`: (x, y) offset

### Direction Method

#### direct()

```python
direct()
```

Return pin direction.

**Returns:**
- `SignalDirect`: INPUT, OUTPUT, or INOUT

### ID Method

#### id()

```python
id()
```

Return pin ID.

**Returns:**
- `int`: Pin ID

## Enum Classes

### OrientType

Cell orientation values:
- `N`: North (0° rotation)
- `S`: South (180° rotation)
- `E`: East (90° clockwise rotation)
- `W`: West (90° counter-clockwise rotation)
- `FN`: Flip North (mirrored N)
- `FS`: Flip South (mirrored S)
- `FE`: Flip East (mirrored E)
- `FW`: Flip West (mirrored W)
- `UNKNOWN`: Unknown orientation

### PlaceStatusType

Node placement status:
- `PLACED`: Node is placed
- `FIXED`: Node is fixed (not movable)
- `UNPLACED`: Node is not placed
- `DUMMY_FIXED`: Node is dummy fixed

### MultiRowAttrType

Multi-row cell attributes:
- `SINGLE_ROW`: Single-row cell
- `MULTI_ROW_ANY`: Multi-row cell, any orientation
- `MULTI_ROW_N`: Multi-row cell, N orientation
- `MULTI_ROW_S`: Multi-row cell, S orientation
- `UNKNOWN`: Unknown multi-row attribute

### SignalDirectType

Signal direction:
- `INPUT`: Input signal
- `OUTPUT`: Output signal
- `INOUT`: Bidirectional signal
- `UNKNOWN`: Unknown direction

### Direction1DType

Direction in one dimension:
- `kX`: X direction
- `kY`: Y direction
- `kLEFT`: Left direction
- `kRIGHT`: Right direction
- `kBOTTOM`: Bottom direction
- `kTOP`: Top direction
- `kLOW`: Low value
- `kHIGH`: High value

### SolutionFileFormat

Output file format:
- `DEF`: DEF format
- `DEFSIMPLE`: Simplified DEF format
- `BOOKSHELF`: Bookshelf format
- `BOOKSHELFALL`: Bookshelf format with all components

## Box Classes

### BoxCoordinate

Box with integer coordinates.

**Methods:**
- `xl()`, `yl()`, `xh()`, `yh()`: Corner coordinates
- `width()`, `height()`: Dimensions
- `area()`: Area
- `__str__()`: String representation

### BoxIndex

Box with index coordinates.

**Methods:** (same as BoxCoordinate)

## Region Class

**Methods:**
- `name()`: Region name
- `boxes()`: List of boxes in region
- `type()`: Region type (FENCE or GUIDE)

## Group Class

**Methods:**
- `name()`: Group name
- `nodes()`: List of node indices in group
- `region()`: Associated region object

## Example Workflows

### Basic Design Reading

```python
import circuit_io

# Read Bookshelf design
db = circuit_io.read_bookshelf('benchmark.aux')

# Access design information
print(f"Design: {db.designName()}")
print(f"Die area: ({db.xl()}, {db.yl()}) - ({db.xh()}, {db.yh()})")
print(f"Nodes: {len(db.nodes())}")
print(f"Nets: {len(db.nets())}")
```

### Iterating Through Nodes

```python
import circuit_io

db = circuit_io.read_bookshelf('design.aux')

# Iterate through nodes
for i in range(len(db.nodes())):
    node = db.node(i)
    prop = db.nodeProperty(node)

    print(f"Node {i}: {prop.name()}")
    print(f"  Size: {node.width()} x {node.height()}")
    print(f"  Status: {node.status().value().name}")
```

### Accessing Nets

```python
import circuit_io

db = circuit_io.read_bookshelf('design.aux')

# Iterate through nets
for i in range(len(db.nets())):
    net = db.net(i)
    prop = db.netProperty(net)

    print(f"Net {i}: {prop.name()}")
    print(f"  Pins: {len(net.pins())}")
    print(f"  Weight: {net.weight()}")
```

### Writing Placement Solutions

```python
import circuit_io
import numpy as np

# Read design
db = circuit_io.read_bookshelf('design.aux')

# Generate placement (e.g., from placement algorithm)
x = np.random.rand(db.numMovable()) * db.width()
y = np.random.rand(db.numMovable()) * db.height()

# Write to DEF file
circuit_io.write(db, 'placement.def',
                 circuit_io.DEF, x, y)
```

### Accessing Row Information

```python
import circuit_io

db = circuit_io.read_bookshelf('design.aux')

# Iterate through rows
rows = db.rows()
for i in range(min(5, len(rows))):
    row = rows[i]
    print(f"Row {i}:")
    print(f"  Origin: ({row.xl()}, {row.yl()})")
    print(f"  Size: {row.width()} x {row.height()}")
    print(f"  Sites: {row.numSites()}")
```

### Using Name-to-Index Maps

```python
import circuit_io

db = circuit_io.read_bookshelf('design.aux')

# Get node by name
node_map = db.nodeName2Index()
if 'my_cell' in node_map:
    idx = node_map['my_cell']
    node = db.node(idx)
    prop = db.nodeProperty(node)
    print(f"Found: {prop.name()}")
```

## Best Practices

1. **Use appropriate read function**: Choose the right API for your file format
2. **Check node types**: Verify if nodes are movable, fixed, or macros before processing
3. **Handle missing data**: Some designs may not have placement information
4. **Validate indices**: Always check array bounds when accessing by index
5. **Use name-to-index maps**: For frequent lookups by name, build and use index maps
6. **Apply vs Write**: Use `apply()` to update in-memory database, `write()` to export files

## Integration Notes

**NumPy Arrays**: Use NumPy arrays for efficient numerical processing
```python
import numpy as np

# Extract node positions
positions = np.array([[node.xl(), node.yl()] for node in db.nodes()])
```

**Pandas DataFrames**: Convert for data analysis
```python
import pandas as pd

df = pd.DataFrame({
    'name': [db.nodeProperty(node).name() for node in db.nodes()],
    'width': [node.width() for node in db.nodes()],
    'height': [node.height() for node in db.nodes()]
})
```

**DREAMPlace Compatibility**: Use `forward()` for DREAMPlace-based research code

## Data Format Reference

### Bookshelf Format

Standard format for ISPD placement contests:
- `.aux`: Points to other Bookshelf files
- `.nodes`: Node definitions
- `.nets`: Net definitions
- `.pl`: Placement information
- `.scl`: Row/cluster information

### LEF Format

Library Exchange Format:
- Cell definitions and dimensions
- Pin locations and properties
- Technology rules
- Site definitions

### DEF Format

Design Exchange Format:
- Component placement
- Routing information
- Net connectivity
- Design constraints

### Verilog Format

Hardware description language:
- Module definitions
- Instance declarations
- Net connectivity
- Port definitions
