#include "module.hpp"

#include "child_window.hpp"
#include "main_window.hpp"
#include "preview_window.hpp"
#include "ui_thread.hpp"

PyObject * commands;
PyObject * child_windows;
PyObject * named_windows;

PyObject * module;
PyObject * keymap;
PyObject * updates;

PyObject * pillow_image;

void add_key(PyObject * key, PyObject * value) {
    /*
        Register a single key
    */

    PyDict_SetItem(keymap, key, value);
    Py_DECREF(key);
    Py_DECREF(value);
}

void register_keys() {
    /*
        Register keys by name
    */

    for (int i = 0; i < 256; ++i) {
        add_key(PyLong_FromLong(i), PyLong_FromLong(i));
    }

    for (int i = '0'; i <= '9'; ++i) {
        add_key(PyUnicode_FromStringAndSize((char *)&i, 1), PyLong_FromLong(i));
    }

    for (int i = 'A'; i <= 'Z'; ++i) {
        add_key(PyUnicode_FromStringAndSize((char *)&i, 1), PyLong_FromLong(i));
    }

    for (int i = 'a'; i <= 'z'; ++i) {
        add_key(PyUnicode_FromStringAndSize((char *)&i, 1), PyLong_FromLong(i - 'a' + 'A'));
    }

    for (int i = 1; i <= 24; ++i) {
        add_key(PyUnicode_FromFormat("f%d", i), PyLong_FromLong(VK_F1 + i - 1));
    }

    add_key(PyUnicode_FromString("mouse1"), PyLong_FromLong(VK_LBUTTON));
    add_key(PyUnicode_FromString("mouse2"), PyLong_FromLong(VK_RBUTTON));
    add_key(PyUnicode_FromString("mouse3"), PyLong_FromLong(VK_MBUTTON));
    add_key(PyUnicode_FromString("control"), PyLong_FromLong(VK_CONTROL));
    add_key(PyUnicode_FromString("ctrl"), PyLong_FromLong(VK_CONTROL));
    add_key(PyUnicode_FromString("shift"), PyLong_FromLong(VK_SHIFT));
    add_key(PyUnicode_FromString("tab"), PyLong_FromLong(VK_TAB));
    add_key(PyUnicode_FromString("pageup"), PyLong_FromLong(VK_PRIOR));
    add_key(PyUnicode_FromString("pagedown"), PyLong_FromLong(VK_NEXT));

    add_key(PyUnicode_FromString("up"), PyLong_FromLong(VK_UP));
    add_key(PyUnicode_FromString("down"), PyLong_FromLong(VK_DOWN));
    add_key(PyUnicode_FromString("left"), PyLong_FromLong(VK_LEFT));
    add_key(PyUnicode_FromString("right"), PyLong_FromLong(VK_RIGHT));

    add_key(PyUnicode_FromString("tilde"), PyLong_FromLong(VK_OEM_3));
    add_key(PyUnicode_FromString("~"), PyLong_FromLong(VK_OEM_3));

    add_key(PyUnicode_FromString("space"), PyLong_FromLong(VK_SPACE));

    // space should be written as "space" not " "
    add_key(PyUnicode_FromString(" "), PyLong_FromLong(VK_SPACE));
}

PyObject * meth_update(PyObject * self) {
    /*
        Update the main_window and the child_windows
    */

    // The main window was closed
    if (!main_window->raw.alive) {
        Py_RETURN_FALSE;
    }

    // Get the updaters
    PyObject ** update_array = PySequence_Fast_ITEMS(updates);
    int num_updates = (int)PySequence_Fast_GET_SIZE(updates);

    // Call the updaters
    for (int i = 0; i < num_updates; ++i) {
        PyObject * res = PyObject_CallFunctionObjArgs(update_array[i], 0);
        if (!res) {
            return 0;
        }
        Py_DECREF(res);
    }

    // Get the child_windows
    ChildWindow ** child_window_array = (ChildWindow **)PySequence_Fast_ITEMS(child_windows);
    int num_child_windows = (int)PySequence_Fast_GET_SIZE(child_windows);

    // Update the windows without holding the GIL
    Py_BEGIN_ALLOW_THREADS;
    update_base_window(main_window);
    for (int i = 0; i < num_child_windows; ++i) {
        update_base_window(child_window_array[i]);
    }
    // Swapbuffers will block until vsync
    SwapBuffers(main_window->hdc);
    Py_END_ALLOW_THREADS;

    // Finish the update while holding the GIL

    // Call the commands of the main_window
    if (call_base_window_commands(main_window)) {
        return 0;
    }

    // Call the commands of the child_windows
    for (int i = 0; i < num_child_windows; ++i) {
        if (call_base_window_commands(child_window_array[i])) {
            return 0;
        }
    }

    Py_RETURN_TRUE;
}

PyMethodDef module_methods[] = {
    {"main_window", (PyCFunction)meth_main_window, METH_VARARGS | METH_KEYWORDS, 0},
    {"child_window", (PyCFunction)meth_child_window, METH_VARARGS | METH_KEYWORDS, 0},
    {"preview_window", (PyCFunction)meth_preview_window, METH_VARARGS | METH_KEYWORDS, 0},
    {"update", (PyCFunction)meth_update, METH_NOARGS, 0},
    {0},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "mollia_window", 0, -1, module_methods, 0, 0, 0, 0};

PyObject * PyInit_mollia_window() {
    /*
        Initialize the module
    */
    module = PyModule_Create(&module_def);

    // PIL.Image dependency for update()
    PyObject * pillow = PyImport_ImportModule("PIL.Image");
    if (!pillow) {
        return 0;
    }

    // PIL.Image.Image dependency for update()
    pillow_image = PyObject_GetAttrString(pillow, "Image");
    if (!pillow_image) {
        return 0;
    }

    // Register python types
    MainWindow_type = (PyTypeObject *)PyType_FromSpec(&MainWindow_spec);
    ChildWindow_type = (PyTypeObject *)PyType_FromSpec(&ChildWindow_spec);
    PreviewWindow_type = (PyTypeObject *)PyType_FromSpec(&PreviewWindow_spec);

    // Internal collections
    keymap = PyDict_New();
    updates = PyList_New(0);
    commands = PyDict_New();
    child_windows = PyList_New(0);
    named_windows = PyDict_New();

    // Populate keymap
    register_keys();

    // Create the main_window python object early
    create_main_window();

    // Module members

    Py_INCREF(main_window);
    PyDict_SetItemString(named_windows, "main window", (PyObject *)main_window);

    Py_INCREF(main_window);
    PyModule_AddObject(module, "wnd", (PyObject *)main_window);

    Py_INCREF(named_windows);
    PyModule_AddObject(module, "windows", named_windows);

    Py_INCREF(keymap);
    PyModule_AddObject(module, "keymap", keymap);

    Py_INCREF(updates);
    PyModule_AddObject(module, "updates", updates);

    return module;
}
