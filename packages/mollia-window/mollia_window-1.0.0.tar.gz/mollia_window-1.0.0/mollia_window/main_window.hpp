#pragma once
#include "common.hpp"
#include "base_window.hpp"

struct MainWindow : public BaseWindow {
    // Handles
    HMENU menu_windows;
    HGLRC hrc;
    HDC hdc;
};

void create_main_window();

MainWindow * meth_main_window(PyObject * self, PyObject * args, PyObject * kwargs);

extern PyType_Spec MainWindow_spec;
extern PyTypeObject * MainWindow_type;
extern MainWindow * main_window;
