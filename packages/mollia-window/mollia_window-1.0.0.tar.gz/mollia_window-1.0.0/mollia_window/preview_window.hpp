#pragma once
#include "common.hpp"
#include "pixels.hpp"

struct PreviewWindow {
    PyObject_HEAD

    // Handles
    CRITICAL_SECTION lock;
    HWND hwnd;

    // Init parameters
    struct {
        POINT pos;
        POINT size;
        bool visible;
    } init;

    // Pixels
    Pixels pixels;
};

PreviewWindow * meth_preview_window(PyObject * self, PyObject * args, PyObject * kwargs);

extern PyType_Spec PreviewWindow_spec;
extern PyTypeObject * PreviewWindow_type;
