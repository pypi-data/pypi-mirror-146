#pragma once
#include "common.hpp"

struct Pixels {
    int bpp; // bit per pixel
    void * ptr; // pointer to the first pixel
    int size; // the size of the pixels in bytes
    bool flip; // flip on the vertical axis
    bool dirty; // dirty flag for WM_PAINT
};

void init_pixels(Pixels & pixels, POINT size, int bpp, bool flip);
PyObject * update_pixels(Pixels & pixels, PyObject * data);
