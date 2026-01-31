#!/usr/bin/env python3
"""
Test script for circuit_io module.
Reads a Bookshelf benchmark and prints circuit properties.
"""

import sys
import os



import circuit_io

def main():
    # Path to mgc_des_perf_a benchmark (ispd2015)
    lef1 = os.path.join(os.path.dirname(__file__), 'raw_benchmarks', 'ispd2015', 'mgc_des_perf_a', 'tech.lef')
    lef2 = os.path.join(os.path.dirname(__file__), 'raw_benchmarks', 'ispd2015', 'mgc_des_perf_a', 'cells.lef')
    def_file = os.path.join(os.path.dirname(__file__), 'raw_benchmarks', 'ispd2015', 'mgc_des_perf_a', 'floorplan.def')
    verilog = os.path.join(os.path.dirname(__file__), 'raw_benchmarks', 'ispd2015', 'mgc_des_perf_a', 'design.v')

    print(f"Reading benchmark: mgc_des_perf_a (LEF + DEF + Verilog)")
    print("=" * 60)

    # Use forward function to read LEF/DEF/Verilog files
    # forward expects a list of command-line arguments
    args = [
        'DREAMPlace',
        '--lef_input', lef1,
        '--lef_input', lef2,
        '--def_input', def_file,
        '--verilog_input', verilog
    ]
    db = circuit_io.forward(args)

    # Output 1: Basic circuit properties
    print("\n1. BASIC CIRCUIT PROPERTIES")
    print("-" * 60)
    print(f"Design name: {db.designName()}")
    print(f"Number of nets: {len(db.nets())}")
    print(f"Number of nodes: {len(db.nodes())}")
    print(f"Number of movable nodes: {db.numMovable()}")
    print(f"Number of fixed nodes: {db.numFixed()}")
    print(f"Number of IO pins: {db.numIOPin()}")
    print(f"Number of macros: {db.numMacro()}")
    print(f"Number of rows: {len(db.rows())}")

    # Die area
    print(f"\nDie area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")
    print(f"Die width: {db.width()}")
    print(f"Die height: {db.height()}")

    # Row info
    print(f"Row height: {db.rowHeight()}")
    print(f"Site width: {db.siteWidth()}")
    print(f"Site height: {db.siteHeight()}")

    # Utilization
    print(f"\nMovable utilization: {db.computeMovableUtil():.2%}")

    # Output 2: Node details (first 10 nodes)
    print("\n2. NODE DETAILS (First 10 nodes)")
    print("-" * 60)
    print(f"{'ID':<6} {'Name':<20} {'Width':<10} {'Height':<10} {'Status':<10} {'X':<12} {'Y':<12}")
    print("-" * 60)

    for i in range(min(10, len(db.nodes()))):
        node = db.node(i)
        node_name = db.nodeProperty(node).name()
        status_str = "FIXED" if node.status() == circuit_io.PlaceStatusEnum.FIXED else \
                   "PLACED" if node.status() == circuit_io.PlaceStatusEnum.PLACED else \
                   "UNPLACED"
        orient_str = str(node.orient()) if node.orient() else "N"

        print(f"{i:<6} {node_name:<20} {node.width():<10} {node.height():<10} {status_str:<10} {node.xl():<12} {node.yl():<12}")

    print("=" * 60)

    # Convert to PyPlaceDB for more Python-friendly data access
    pydb = circuit_io.pydb(db)

    print(f"\nPyPlaceDB num_nodes: {pydb.num_nodes}")
    print(f"PyPlaceDB num_terminals: {pydb.num_terminals}")
    print(f"PyPlaceDB num_terminal_NIs: {pydb.num_terminal_NIs}")

if __name__ == "__main__":
    main()
