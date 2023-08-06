#include "preview_window.hpp"

#include "module.hpp"
#include "ui_thread.hpp"

PreviewWindow * meth_preview_window(PyObject * self, PyObject * args, PyObject * kwargs) {
    /*
        Create a preview_window
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

    static char * keywords[] = {"name", "size", "position", "bpp", "flip", "visible", 0};

    int args_ok = PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        "s(ii)|$(ii)iip",
        keywords,
        &name,
        &size.x,
        &size.y,
        &pos.x,
        &pos.y,
        &bpp,
        &flip,
        &visible
    );

    if (!args_ok) {
        return 0;
    }

    // Name check
    if (PyDict_GetItemString(named_windows, name)) {
        PyErr_Format(PyExc_Exception, "%s already exists", name);
        return 0;
    }

    // Create the python object for the preview_window
    PreviewWindow * preview_window = PyObject_New(PreviewWindow, PreviewWindow_type);
    memset(&preview_window->lock, 0, sizeof(preview_window->lock));
    memset(&preview_window->init, 0, sizeof(preview_window->init));
    memset(&preview_window->pixels, 0, sizeof(preview_window->pixels));
    preview_window->hwnd = 0;
    InitializeCriticalSection(&preview_window->lock);

    Py_INCREF(preview_window);
    PyDict_SetItemString(named_windows, name, (PyObject *)preview_window);

    // Init parameters for the ui thread
    preview_window->init.visible = !!visible;
    preview_window->init.size = size;
    preview_window->init.pos = pos;

    // Allocate memory for the pixels
    init_pixels(preview_window->pixels, size, bpp, flip);

    // Notify the ui thread to create the actual window for the preview_window
    PostThreadMessage(ui_thread_id, WM_USER_CREATE_PREVIEW, 0, (LPARAM)preview_window);
    // Wait for the window to be created
    WaitForSingleObject(preview_window_ready, INFINITE);
    ResetEvent(preview_window_ready);

    Py_INCREF(preview_window);
    return preview_window;
}

PyObject * PreviewWindow_meth_update(PreviewWindow * self, PyObject * data) {
    /*
        Write to the pixels and notify the ui thread to refresh the device content asyncronously
    */
    PyObject * res = update_pixels(self->pixels, data);
    self->pixels.dirty = true;
    InvalidateRect(self->hwnd, 0, 0);
    UpdateWindow(self->hwnd);
    return res;
}

PyObject * PreviewWindow_meth_show(PreviewWindow * self) {
    /*
        Show the preview_window
    */
    ShowWindow(self->hwnd, SW_SHOW);
    Py_RETURN_NONE;
}

PyObject * PreviewWindow_meth_hide(PreviewWindow * self) {
    /*
        Hide the preview_window
    */
    ShowWindow(self->hwnd, SW_HIDE);
    Py_RETURN_NONE;
}

PyObject * PreviewWindow_get_pixels(PreviewWindow * self) {
    /*
        Return a memory view of the pixels
    */
    return PyMemoryView_FromMemory((char *)self->pixels.ptr, self->pixels.size, PyBUF_WRITE);
}

PyObject * PreviewWindow_get_visible(PreviewWindow * self) {
    /*
        Is the preview_window visible
    */
    return PyBool_FromLong(IsWindowVisible(self->hwnd));
}

int PreviewWindow_set_title(PreviewWindow * self, PyObject * value) {
    /*
        Set the title
    */
	wchar_t * title_str = PyUnicode_AsWideCharString(value, 0);
    if (!title_str) {
        return -1;
    }
	SetWindowText(self->hwnd, title_str);
	PyMem_Free(title_str);
	return 0;
}

void PreviewWindow_dealloc(PreviewWindow * self) {
    /*
        Dealloc the preview_window
    */
    Py_TYPE(self)->tp_free(self);
}

PyMethodDef PreviewWindow_methods[] = {
    {(char *)"update", (PyCFunction)PreviewWindow_meth_update, METH_O, 0},
    {(char *)"show", (PyCFunction)PreviewWindow_meth_show, METH_NOARGS, 0},
    {(char *)"hide", (PyCFunction)PreviewWindow_meth_hide, METH_NOARGS, 0},
    {0},
};

PyGetSetDef PreviewWindow_getset[] = {
    {(char *)"visible", (getter)PreviewWindow_get_visible, 0, 0},
    {(char *)"pixels", (getter)PreviewWindow_get_pixels, 0, 0},
    {(char *)"title", 0, (setter)PreviewWindow_set_title, 0},
    {0},
};

PyType_Slot PreviewWindow_slots[] = {
    {Py_tp_methods, PreviewWindow_methods},
    {Py_tp_getset, PreviewWindow_getset},
    {Py_tp_dealloc, PreviewWindow_dealloc},
    {0},
};

PyType_Spec PreviewWindow_spec = {
    "mollia_window.PreviewWindow",
    sizeof(PreviewWindow),
    0,
    Py_TPFLAGS_DEFAULT,
    PreviewWindow_slots,
};

PyTypeObject * PreviewWindow_type;
