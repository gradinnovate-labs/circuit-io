# place_io API 測試結果

## 測試環境
- Python 3.11
- place_io 模塊編譯成功
- 時間: 2026-01-23

## 測試結果摘要

### ✓ 所有測試通過

| 測試項目 | 格式 | 狀態 | 詳細信息 |
|----------|------|------|----------|
| adaptec1 (Bookshelf) | Bookshelf | ✓ PASSED | 成功讀取 .aux 文件 |
| mgc_des_perf_1 | LEF + DEF + Verilog | ✓ PASSED | 成功讀取混合格式 |
| ispd19_test2 | LEF + DEF | ✓ PASSED | 成功讀取 LEF + DEF |

---

## 新增的 Python API 函數

### 1. read_bookshelf
```python
import place_io

# 讀取 Bookshelf 格式
db = place_io.read_bookshelf('path/to/design.aux')
```

### 2. read_lef_def
```python
import place_io

# 讀取 LEF + DEF 格式
db = place_io.read_lef_def(['tech.lef', 'cells.lef'], 'design.def')
```

### 3. read_verilog
```python
import place_io

# 讀取 Verilog 格式
db = place_io.read_verilog('path/to/design.v')
```

### 4. read_mixed (NEW)
```python
import place_io

# 讀取 LEF + DEF + Verilog 混合格式
db = place_io.read_mixed(
    ['tech.lef', 'cells.lef'],  # LEF 文件列表
    'floorplan.def',                # DEF 文件
    'design.v'                     # Verilog 文件
)
```

### 5. forward (Legacy)
```python
import place_io

# 向後兼容的命令行參數方式（舊代碼仍可使用）
args = ['DREAMPlace', '--bookshelf_aux_input', 'design.aux']
db = place_io.forward(args)
```

---

## 測試詳細結果

### 測試 1: adaptec1 (Bookshelf format)
```
======================================================================
TEST 1: adaptec1 (Bookshelf format)
======================================================================
Reading: /.../raw_benchmarks/ispd2005/adaptec1/adaptec1.aux

Design name: RowBasedPlacement
Number of nets: 221,142
Number of nodes: 211,447
Number of movable nodes: 210,904
Number of fixed nodes: 543
Number of IO pins: 0
Number of macros: 211,447
Number of rows: 890
Die area: (22, 22) to (11589, 11589)
Die size: 11567 x 11567
Utilization: 74.43%
```

### 測試 2: mgc_des_perf_1 (LEF + DEF + Verilog)
```
======================================================================
TEST 2: mgc_des_perf_1 (LEF + DEF + Verilog)
======================================================================
LEF files:
  tech.lef
  cells.lef
DEF file: floorplan.def
Verilog file: design.v

Design name: des_perf
Number of nets: 112,878
Number of nodes: 113,018
Number of movable nodes: 112,644
Number of fixed nodes: 0
Die area: (0, 0) to (445000, 445000)
```

### 測試 3: ispd19_test2 (LEF + DEF)
```
======================================================================
TEST 3: ispd19_test2 (LEF + DEF)
======================================================================
LEF file: ispd19_test2.input.lef
DEF file: ispd19_test2.input.def

Design name: ispd19_test2
Number of nets: 72,410
Number of nodes: 73,305
Number of movable nodes: 72,090
Number of fixed nodes: 4
Die area: (0, 0) to (1745600, 1178400)
```

---

## API 對比

| API | 優點 | 缺點 | 推薦使用場景 |
|-----|--------|--------|--------------|
| `read_bookshelf(aux)` | 簡潔，單參數 | 只支持 Bookshelf | ISPD 競賽格式 |
| `read_lef_def(lef, def)` | 直觀，明確的參數 | 只支持 LEF+DEF | 工業 LEF/DEF 設計 |
| `read_verilog(v)` | 簡單 | 只支持 Verilog | 純網表分析 |
| `read_mixed(lef, def, v)` | 支持最複雜的混合場景 | 參數較多 | **mgc_des_perf_1 類型設計** |
| `forward(args)` | 向後兼容 | 需要記憶命令行格式 | 舊 DREAMPlace 代碼遷移 |

---

## 實施的改進

### C++ 代碼修改
1. **新增函數**（在 `place_io.cpp` 中）：
   - `read_bookshelf(const std::string& aux_file)`
   - `read_lef_def(pybind11::list lef_files, const std::string& def_file)`
   - `read_verilog(const std::string& verilog_file)`
   - `read_mixed(pybind11::list lef_files, const std::string& def_file, const std::string& verilog_file)`

2. **Python 綁定**（在 `PYBIND11_MODULE` 中）：
   ```cpp
   m.def("read_bookshelf", &DREAMPLACE_NAMESPACE::read_bookshelf, ...);
   m.def("read_lef_def", &DREAMPLACE_NAMESPACE::read_lef_def, ...);
   m.def("read_verilog", &DREAMPLACE_NAMESPACE::read_verilog, ...);
   m.def("read_mixed", &DREAMPLACE_NAMESPACE::read_mixed, ...);
   ```

3. **保留向後兼容性**：
   - 繼續支持 `forward()` 函數
   - 現有 DREAMPlace 代碼無需修改

---

## 結論

✅ **完整方案實施成功**

- ✓ 新增 4 個優雅的 Python API 函數
- ✓ 支持三種主要格式：Bookshelf, LEF+DEF, Verilog
- ✓ 特別支持 LEF+DEF+Verilog 混合格式（針對 mgc_des_perf_1 類型設計）
- ✓ 向後兼容舊的 `forward()` 接口
- ✓ 所有測試通過

**用戶現在可以選擇最適合的 API：**
- 新項目：使用 `read_bookshelf()`, `read_lef_def()`, `read_mixed()`
- 舊項目：繼續使用 `forward()`
- 複雜場景：使用 `read_mixed()` 處理混合格式
