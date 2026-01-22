set(OP_NAME utility)

file(GLOB CPP_SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/*.c"
    )

set(TARGET_NAME ${OP_NAME})

set(INCLUDE_DIRS
  ${CMAKE_CURRENT_SOURCE_DIR}/..
  )

set(LINK_LIBS "")

add_library(${TARGET_NAME}_cxx STATIC ${CPP_SOURCES})
set_target_properties(${TARGET_NAME}_cxx PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    CXX_VISIBILITY_PRESET hidden
)
target_include_directories(${TARGET_NAME}_cxx PRIVATE ${INCLUDE_DIRS})
target_link_libraries(${TARGET_NAME}_cxx PRIVATE ${LINK_LIBS})
