cmake_minimum_required(VERSION 3.15)
project(circuit_io LANGUAGES CXX)

# Find required dependencies
find_package(ZLIB REQUIRED)

# Support both old ABI (0) and new ABI (1) for compatibility
# Default to old ABI for backward compatibility, but allow override
if(NOT DEFINED CMAKE_CXX_ABI)
    set(CMAKE_CXX_ABI 0 CACHE STRING
        "Choose the value for _GLIBCXX_USE_CXX11_ABI, options are: 0 (old) | 1 (new)."
        FORCE)
endif()
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=${CMAKE_CXX_ABI})

set(OP_NAME circuit_io)

set(TARGET_NAME ${OP_NAME})

set(LIMBO_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../Limbo)
set(UTILITY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../utility)

set(INCLUDE_DIRS
  ${CMAKE_CURRENT_SOURCE_DIR}/..
  ${LIMBO_DIR}
  ${UTILITY_DIR}
  ${Boost_INCLUDE_DIRS}
  ${ZLIB_INCLUDE_DIRS}
  )

set(LINK_LIBS
  ${ZLIB_LIBRARIES}
  utility_cxx
  # begin targets in Limbo
  lefparseradapt
  defparseradapt
  verilogparser
  bookshelfparser
  gdsparser
  programoptions
  gzstream
  # end targets in Limbo
)

if(CAIRO_FOUND)
  set(INCLUDE_DIRS ${INCLUDE_DIRS} ${CAIRO_INCLUDE_DIRS})
  set(LINK_LIBS ${LINK_LIBS} ${CAIRO_LIBRARIES})
  set(DRAWPLACE 1)
else()
  set(DRAWPLACE 0)
endif()

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Get pybind11 include directory using Python
execute_process(COMMAND ${Python_EXECUTABLE} -c
    "import pybind11; import os; print(os.path.dirname(pybind11.__file__))"
    OUTPUT_VARIABLE PYBIND11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
set(PYBIND11_INCLUDE_DIR ${PYBIND11_DIR}/include)
message(STATUS "pybind11 include dir: ${PYBIND11_INCLUDE_DIR}")

# Get Python extension suffix for proper module naming
execute_process(COMMAND ${Python_EXECUTABLE} -c
    "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))"
    OUTPUT_VARIABLE Python_EXT_SUFFIX
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
message(STATUS "Python extension suffix: ${Python_EXT_SUFFIX}")

# Add subdirectories for dependencies
add_subdirectory(${UTILITY_DIR} ${CMAKE_BINARY_DIR}/utility)
add_subdirectory(${LIMBO_DIR} ${CMAKE_BINARY_DIR}/Limbo)

# Create pybind11 module manually
add_library(${TARGET_NAME} MODULE SHARED
  src/BenchMetrics.cpp
  src/BinMap.cpp
  src/Enums.cpp
  src/Net.cpp
  src/Node.cpp
  src/Region.cpp
  src/Group.cpp
  src/Params.cpp
  src/PlaceDB.cpp
  src/DefWriter.cpp
  src/BookshelfWriter.cpp
  src/PyPlaceDB.cpp
  src/PybindPlaceDB.cpp
  src/PybindPyPlaceDB.cpp
  src/place_io.cpp
  )

target_include_directories(${TARGET_NAME} PRIVATE
  ${INCLUDE_DIRS}
  ${PYBIND11_INCLUDE_DIR}
  ${Python_INCLUDE_DIRS}
  )

target_link_libraries(${TARGET_NAME} PRIVATE ${LINK_LIBS} ${Python_LIBRARIES})
target_compile_definitions(${TARGET_NAME} PRIVATE DRAWPLACE=${DRAWPLACE})

# Set RPATH to find zlib at runtime
set_target_properties(${TARGET_NAME} PROPERTIES
  INSTALL_RPATH "$ORIGIN;$ORIGIN/../.."
  BUILD_WITH_INSTALL_RPATH TRUE
)

# Set module properties
set_target_properties(${TARGET_NAME} PROPERTIES
  PREFIX ""
  OUTPUT_NAME ${TARGET_NAME}
  SUFFIX "${Python_EXT_SUFFIX}"
  )

# Install - using scikit-build-core's Python integration
install(TARGETS ${TARGET_NAME}
  LIBRARY DESTINATION circuit_io)

file(GLOB INSTALL_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.py)
install(FILES ${INSTALL_SRCS}
  DESTINATION circuit_io)
