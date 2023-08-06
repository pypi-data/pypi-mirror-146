#include "child_window.hpp"

#include "main_window.hpp"
#include "module.hpp"
#include "ui_thread.hpp"

ChildWindow * meth_child_window(PyObject * self, PyObject * args, PyObject * kwargs) {
    /*
        Create a child_window
    */

    if (init_ui_thread()) {
        return 0;
    }

    const char * name;
    POINT size;
    POINT pos = {0, 0};
    int bpp = 3;
    int flip = false;
    int visible = true;
    int above_main = false;
    int menubar = false;

    static char * keywords[] = {"name", "size", "position", "bpp", "flip", "visible", "above_main", "menubar", 0};

    int args_ok = PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        "s(ii)|$(ii)iippp",
        keywords,
        &name,
        &size.x,
        &size.y,
        &pos.x,
        &pos.y,
        &bpp,
        &flip,
        &visible,
        &above_main,
        &menubar
    );

    if (!args_ok) {
        return 0;
    }

    // The main_window must exist
    if (!main_window->hwnd) {
        PyErr_Format(PyExc_Exception, "missing main window");
        return 0;
    }

    // Name check
    if (PyDict_GetItemString(named_windows, name)) {
        PyErr_Format(PyExc_Exception, "%s already exists", name);
        return 0;
    }

    ChildWindow * child_window = PyObject_New(ChildWindow, ChildWindow_type);
    memset(&child_window->lock, 0, sizeof(child_window->lock));
    memset(&child_window->init, 0, sizeof(child_window->init));
    memset(&child_window->raw, 0, sizeof(child_window->raw));
    memset(&child_window->input, 0, sizeof(child_window->input));
    memset(&child_window->pixels, 0, sizeof(child_window->pixels));
    child_window->menubar = 0;
    child_window->menu_commands = 0;
    child_window->hwnd = 0;
    child_window->above_main = 0;
    InitializeCriticalSection(&child_window->lock);

    Py_INCREF(child_window);
    PyDict_SetItemString(named_windows, name, (PyObject *)child_window);

    // Init parameters for the ui thread
    child_window->init.visible = !!visible;
    child_window->init.menubar = !!menubar;
    child_window->above_main = !!above_main;
    child_window->init.size = size;
    child_window->init.pos = pos;

    // Allocate memory for the pixels
    init_pixels(child_window->pixels, child_window->init.size, bpp, flip);

    // Notify the ui thread to create the actual window for the child_window
    PostThreadMessage(ui_thread_id, WM_USER_CREATE_CHILD, 0, (LPARAM)child_window);
    // Wait for the window to be created
    WaitForSingleObject(child_window_ready, INFINITE);
    ResetEvent(child_window_ready);

    // Register a command on the main_window to show this child_wndow by name
    int command_code = (int)PyObject_Size(commands) + 1;
    AppendMenuA(main_window->menu_windows, MF_STRING, command_code, name);
    PyDict_SetItem(commands, PyLong_FromLong(command_code), (PyObject *)child_window);

    // Keep track of all the child_windows
    PyList_Append(child_windows, (PyObject *)child_window);

    return child_window;
}

PyObject * ChildWindow_meth_update(ChildWindow * self, PyObject * data) {
    /*
        Write to the pixels and notify the ui thread to refresh the device content asyncronously
    */
    PyObject * res = update_pixels(self->pixels, data);
    self->pixels.dirty = true;
    InvalidateRect(self->hwnd, 0, 0);
    UpdateWindow(self->hwnd);
    return res;
}

PyObject * ChildWindow_get_pixels(ChildWindow * self) {
    /*
        Return a memory view of the pixels
    */
    return PyMemoryView_FromMemory((char *)self->pixels.ptr, self->pixels.size, PyBUF_WRITE);
}

PyObject * ChildWindow_call(ChildWindow * self) {
    /*
        Calling the child_window will show the window if hidden
    */
    ShowWindow(self->hwnd, SW_SHOW);
    SetForegroundWindow(self->hwnd);
    SetActiveWindow(self->hwnd);
    SetFocus(self->hwnd);
    Py_RETURN_NONE;
}

PyMethodDef ChildWindow_methods[] = {
    {"command", (PyCFunction)BaseWindow_meth_command, METH_VARARGS, 0},
    {"grab_mouse", (PyCFunction)BaseWindow_meth_grab_mouse, METH_O, 0},
    {"update", (PyCFunction)ChildWindow_meth_update, METH_O, 0},
    {"key_pressed", (PyCFunction)BaseWindow_meth_key_pressed, METH_O, 0},
    {"key_down", (PyCFunction)BaseWindow_meth_key_down, METH_O, 0},
    {"key_released", (PyCFunction)BaseWindow_meth_key_released, METH_O, 0},
    {"key_up", (PyCFunction)BaseWindow_meth_key_up, METH_O, 0},
    {"show", (PyCFunction)BaseWindow_meth_show, METH_NOARGS, 0},
    {"hide", (PyCFunction)BaseWindow_meth_hide, METH_NOARGS, 0},
    {0},
};

PyGetSetDef ChildWindow_getset[] = {
    {"visible", (getter)BaseWindow_get_visible, 0, 0},
    {"width", (getter)BaseWindow_get_width, 0, 0},
    {"height", (getter)BaseWindow_get_height, 0, 0},
    {"ratio", (getter)BaseWindow_get_ratio, 0, 0},
    {"size", (getter)BaseWindow_get_size, 0, 0},
    {"mouse", (getter)BaseWindow_get_mouse, 0, 0},
    {"mouse_wheel", (getter)BaseWindow_get_mouse_wheel, 0, 0},
    {"text_input", (getter)BaseWindow_get_text_input, 0, 0},
    {"drop_files", (getter)BaseWindow_get_drop_files, 0, 0},
    {"pixels", (getter)ChildWindow_get_pixels, 0, 0},
    {"title", 0, (setter)BaseWindow_set_title, 0},
    {"accept_drop_files", 0, (setter)BaseWindow_set_accept_drop_files, 0},
    {"placement", (getter)BaseWindow_get_placement, (setter)BaseWindow_set_placement, 0},
    {0},
};

PyType_Slot ChildWindow_slots[] = {
    {Py_tp_methods, ChildWindow_methods},
    {Py_tp_getset, ChildWindow_getset},
    {Py_tp_call, ChildWindow_call},
    {0},
};

PyType_Spec ChildWindow_spec = {
    "mollia_window.ChildWindow",
    sizeof(ChildWindow),
    0,
    Py_TPFLAGS_DEFAULT,
    ChildWindow_slots,
};

PyTypeObject * ChildWindow_type;
