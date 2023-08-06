#pragma once
#include "common.hpp"
#include "base_window.hpp"
#include "pixels.hpp"

struct ChildWindow : public BaseWindow {
    // Init parameter
    bool above_main;

    // Pixels
    Pixels pixels;
};

ChildWindow * meth_child_window(PyObject * self, PyObject * args, PyObject * kwargs);

extern PyType_Spec ChildWindow_spec;
extern PyTypeObject * ChildWindow_type;
