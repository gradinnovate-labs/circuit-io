#!/usr/bin/env python3
"""
Test script for circuit_io module - testing all three benchmark formats
"""

import sys
import os


import circuit_io

def test_bookshelf():
    """Test 1: adaptec1 (Bookshelf format)"""
    print("=" * 70)
    print("TEST 1: adaptec1 (Bookshelf format)")
    print("=" * 70)

    aux_path = os.path.join('raw_benchmarks', 'ispd2005', 'adaptec1', 'adaptec1.aux')
    abs_path = os.path.abspath(aux_path)

    print(f"Reading: {abs_path}")

    db = circuit_io.read_bookshelf(abs_path)

    print(f"Design name: {db.designName()}")
    print(f"Number of nets: {len(db.nets())}")
    print(f"Number of nodes: {len(db.nodes())}")
    print(f"Number of movable nodes: {db.numMovable()}")
    print(f"Number of fixed nodes: {db.numFixed()}")
    print(f"Number of IO pins: {db.numIOPin()}")
    print(f"Number of macros: {db.numMacro()}")
    print(f"Number of rows: {len(db.rows())}")
    print(f"Die area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")
    print(f"Die size: {db.width()} x {db.height()}")
    print(f"Utilization: {db.computeMovableUtil():.2%}")

    print("\nFirst 5 nodes:")
    for i in range(min(5, len(db.nodes()))):
        node = db.node(i)
        node_name = db.nodeProperty(node).name()
        print(f"  [{i}] {node_name}")

    return True

def test_lef_def_verilog():
    """Test 2: mgc_des_perf_1 (LEF + DEF + Verilog)"""
    print("\n" + "=" * 70)
    print("TEST 2: mgc_des_perf_1 (LEF + DEF + Verilog)")
    print("=" * 70)

    lef1 = os.path.join('raw_benchmarks', 'ispd2015', 'mgc_des_perf_1', 'tech.lef')
    lef2 = os.path.join('raw_benchmarks', 'ispd2015', 'mgc_des_perf_1', 'cells.lef')
    def_file = os.path.join('raw_benchmarks', 'ispd2015', 'mgc_des_perf_1', 'floorplan.def')
    verilog = os.path.join('raw_benchmarks', 'ispd2015', 'mgc_des_perf_1', 'design.v')

    abs_lef1 = os.path.abspath(lef1)
    abs_lef2 = os.path.abspath(lef2)
    abs_def = os.path.abspath(def_file)
    abs_verilog = os.path.abspath(verilog)

    print(f"LEF files:")
    print(f"  {abs_lef1}")
    print(f"  {abs_lef2}")
    print(f"DEF file: {abs_def}")
    print(f"Verilog file: {abs_verilog}")

    # Use read_mixed approach
    print("\nUsing read_mixed (LEF + DEF + Verilog)...")
    db = circuit_io.read_mixed([abs_lef1, abs_lef2], abs_def, abs_verilog)

    print(f"Design name: {db.designName()}")
    print(f"Number of nets: {len(db.nets())}")
    print(f"Number of nodes: {len(db.nodes())}")
    print(f"Number of movable nodes: {db.numMovable()}")
    print(f"Number of fixed nodes: {db.numFixed()}")
    print(f"Die area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")

    return True

def test_lef_def():
    """Test 3: ispd19_test2 (LEF + DEF)"""
    print("\n" + "=" * 70)
    print("TEST 3: ispd19_test2 (LEF + DEF)")
    print("=" * 70)

    lef = os.path.join('raw_benchmarks', 'ispd2019', 'ispd19_test2', 'ispd19_test2.input.lef')
    def_file = os.path.join('raw_benchmarks', 'ispd2019', 'ispd19_test2', 'ispd19_test2.input.def')

    abs_lef = os.path.abspath(lef)
    abs_def = os.path.abspath(def_file)

    print(f"LEF file: {abs_lef}")
    print(f"DEF file: {abs_def}")

    # Use read_lef_def
    print("\nUsing read_lef_def (LEF + DEF)...")
    db = circuit_io.read_lef_def([abs_lef], abs_def)

    print(f"Design name: {db.designName()}")
    print(f"Number of nets: {len(db.nets())}")
    print(f"Number of nodes: {len(db.nodes())}")
    print(f"Number of movable nodes: {db.numMovable()}")
    print(f"Number of fixed nodes: {db.numFixed()}")
    print(f"Die area: ({db.xl()}, {db.yl()}) to ({db.xh()}, {db.yh()})")

    return True

def main():
    results = []

    # Test 1: Bookshelf format
    try:
        result1 = test_bookshelf()
        results.append(("adaptec1 (Bookshelf)", "PASSED" if result1 else "FAILED"))
    except Exception as e:
        print(f"ERROR in test 1: {e}")
        results.append(("adaptec1 (Bookshelf)", f"FAILED: {str(e)[:50]}"))

    # Test 2: LEF + DEF + Verilog
    try:
        result2 = test_lef_def_verilog()
        results.append(("mgc_des_perf_1 (LEF + DEF + Verilog)", "PASSED" if result2 else "FAILED"))
    except Exception as e:
        print(f"ERROR in test 2: {e}")
        results.append(("mgc_des_perf_1 (LEF + DEF + Verilog)", f"FAILED: {str(e)[:50]}"))

    # Test 3: LEF + DEF
    try:
        result3 = test_lef_def()
        results.append(("ispd19_test2 (LEF + DEF)", "PASSED" if result3 else "FAILED"))
    except Exception as e:
        print(f"ERROR in test 3: {e}")
        results.append(("ispd19_test2 (LEF + DEF)", f"FAILED: {str(e)[:50]}"))

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for test_name, status in results:
        symbol = "✓" if "PASSED" in status else "✗"
        print(f"{symbol} {test_name}: {status}")

    all_passed = all("PASSED" in status for _, status in results)

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 70)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
