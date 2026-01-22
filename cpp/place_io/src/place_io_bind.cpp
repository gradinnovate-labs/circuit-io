/**
 * @file   place_io_bind.cpp
 * @brief  Python binding entry point for place_io
 */

#include <pybind11/pybind11.h>
#include "utility/src/defs.h"

DREAMPLACE_BEGIN_NAMESPACE

void bind_PlaceDB(pybind11::module&);
void bind_PyPlaceDB(pybind11::module&);

PYBIND11_MODULE(place_io, m) {

    bind_PlaceDB(m);
    bind_PyPlaceDB(m);

}

DREAMPLACE_END_NAMESPACE
