#pragma once
#include "common.hpp"
#include "input.hpp"

struct BaseWindow {
    PyObject_HEAD

    // Handles
    CRITICAL_SECTION lock;
    HMENU menu_commands;
    HMENU menubar;
    HWND hwnd;

    // Init parameters
    struct {
        POINT pos;
        POINT size;
        bool visible;
        bool menubar;
    } init;

    // Input
    RawInput raw;
    WndInput input;
};

void update_base_window(BaseWindow * self);
int call_base_window_commands(BaseWindow * wnd);

PyObject * BaseWindow_meth_command(BaseWindow * self, PyObject * args);
PyObject * BaseWindow_meth_grab_mouse(BaseWindow * self, PyObject * arg);
PyObject * BaseWindow_meth_key_pressed(BaseWindow * self, PyObject * key);
PyObject * BaseWindow_meth_key_down(BaseWindow * self, PyObject * key);
PyObject * BaseWindow_meth_key_released(BaseWindow * self, PyObject * key);
PyObject * BaseWindow_meth_key_up(BaseWindow * self, PyObject * key);
PyObject * BaseWindow_meth_show(BaseWindow * self);
PyObject * BaseWindow_meth_hide(BaseWindow * self);

PyObject * BaseWindow_get_visible(BaseWindow * self);
PyObject * BaseWindow_get_width(BaseWindow * self);
PyObject * BaseWindow_get_height(BaseWindow * self);
PyObject * BaseWindow_get_ratio(BaseWindow * self);
PyObject * BaseWindow_get_size(BaseWindow * self);
PyObject * BaseWindow_get_mouse(BaseWindow * self);
PyObject * BaseWindow_get_mouse_wheel(BaseWindow * self);
PyObject * BaseWindow_get_text_input(BaseWindow * self);
PyObject * BaseWindow_get_drop_files(BaseWindow * self);
PyObject * BaseWindow_get_placement(BaseWindow * self);

int BaseWindow_set_title(BaseWindow * self, PyObject * value);
int BaseWindow_set_accept_drop_files(BaseWindow * self, PyObject * value);
int BaseWindow_set_placement(BaseWindow * self, PyObject * value);
