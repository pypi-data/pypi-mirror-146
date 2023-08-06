#include "main_window.hpp"

#include "ui_thread.hpp"

MainWindow * main_window;

void create_main_window() {
    // Create the python object for the main_window
    main_window = PyObject_New(MainWindow, MainWindow_type);
    memset(&main_window->lock, 0, sizeof(main_window->lock));
    memset(&main_window->init, 0, sizeof(main_window->init));
    memset(&main_window->raw, 0, sizeof(main_window->raw));
    memset(&main_window->input, 0, sizeof(main_window->input));
    main_window->menubar = 0;
    main_window->menu_commands = 0;
    main_window->menu_windows = 0;
    main_window->hwnd = 0;
    main_window->hdc = 0;
    main_window->hrc = 0;
    InitializeCriticalSection(&main_window->lock);
}

MainWindow * meth_main_window(PyObject * self, PyObject * args, PyObject * kwargs) {
    /*
        Create the main_window
    */

    if (init_ui_thread()) {
        return 0;
    }

    POINT size = {1280, 720};
    POINT pos = {0, 0};
    int visible = true;
    int menubar = true;

    static char * keywords[] = {"size", "position", "visible", "menubar", 0};

    int args_ok = PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        "|(ii)$(ii)pp",
        keywords,
        &size.x,
        &size.y,
        &pos.x,
        &pos.y,
        &visible,
        &menubar
    );

    if (!args_ok) {
        return 0;
    }

    // There is only one main_window
    if (main_window->hwnd) {
        PyErr_Format(PyExc_Exception, "main window already exists");
        return 0;
    }

    // Init parameters for the ui thread
    main_window->init.visible = !!visible;
    main_window->init.menubar = !!menubar;
    main_window->init.size = size;
    main_window->init.pos = pos;

    // Notify the ui thread to create the actual window for the preview_window
    PostThreadMessage(ui_thread_id, WM_USER_CREATE_MAIN, 0, 0);
    // Wait for the window to be created
    WaitForSingleObject(main_window_ready, INFINITE);

    // Render to this window
    if (!wglMakeCurrent(main_window->hdc, main_window->hrc)) {
        PyErr_BadInternalCall();
        return 0;
    }

    // Enable sync if available
    typedef void (WINAPI * _wglSwapIntervalProc)(int interval);
    _wglSwapIntervalProc _wglSwapInterval = (_wglSwapIntervalProc)wglGetProcAddress("wglSwapIntervalEXT");
    if (_wglSwapInterval) {
        _wglSwapInterval(1);
    }

    Py_INCREF(main_window);
    return main_window;
}

PyMethodDef MainWindow_methods[] = {
    {"command", (PyCFunction)BaseWindow_meth_command, METH_VARARGS, 0},
    {"grab_mouse", (PyCFunction)BaseWindow_meth_grab_mouse, METH_O, 0},
    {"key_pressed", (PyCFunction)BaseWindow_meth_key_pressed, METH_O, 0},
    {"key_down", (PyCFunction)BaseWindow_meth_key_down, METH_O, 0},
    {"key_released", (PyCFunction)BaseWindow_meth_key_released, METH_O, 0},
    {"key_up", (PyCFunction)BaseWindow_meth_key_up, METH_O, 0},
    {0},
};

PyGetSetDef MainWindow_getset[] = {
    {"visible", (getter)BaseWindow_get_visible, 0, 0},
    {"width", (getter)BaseWindow_get_width, 0, 0},
    {"height", (getter)BaseWindow_get_height, 0, 0},
    {"ratio", (getter)BaseWindow_get_ratio, 0, 0},
    {"size", (getter)BaseWindow_get_size, 0, 0},
    {"mouse", (getter)BaseWindow_get_mouse, 0, 0},
    {"mouse_wheel", (getter)BaseWindow_get_mouse_wheel, 0, 0},
    {"text_input", (getter)BaseWindow_get_text_input, 0, 0},
    {"drop_files", (getter)BaseWindow_get_drop_files, 0, 0},
    {"title", 0, (setter)BaseWindow_set_title, 0},
    {"accept_drop_files", 0, (setter)BaseWindow_set_accept_drop_files, 0},
    {"placement", (getter)BaseWindow_get_placement, (setter)BaseWindow_set_placement, 0},
    {0},
};

PyType_Slot MainWindow_slots[] = {
    {Py_tp_methods, MainWindow_methods},
    {Py_tp_getset, MainWindow_getset},
    {0},
};

PyType_Spec MainWindow_spec = {
    "mollia_window.MainWindow",
    sizeof(MainWindow),
    0,
    Py_TPFLAGS_DEFAULT,
    MainWindow_slots,
};

PyTypeObject * MainWindow_type;
