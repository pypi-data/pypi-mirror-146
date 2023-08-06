#include "base_window.hpp"

#include "module.hpp"
#include "ui_thread.hpp"

void update_base_window(BaseWindow * self) {
    /*
        Process inputs
    */
    EnterCriticalSection(&self->lock);
    process_input(self->hwnd, self->raw, self->input);
    LeaveCriticalSection(&self->lock);
}

int call_base_window_commands(BaseWindow * wnd) {
    /*
        Call commands while holding the GIL
    */
    for (int i = 0; i < wnd->input.num_commands; ++i) {
        PyObject * key = PyLong_FromLong(wnd->input.commands[i]);
        if (PyObject * command = PyDict_GetItem(commands, key)) {
            PyObject * res = PyObject_CallFunction(command, NULL);
            if (!res) {
                return -1;
            }
            Py_DECREF(res);
        }
        Py_DECREF(key);
    }
    return 0;
}

PyObject * BaseWindow_meth_command(BaseWindow * self, PyObject * args) {
    /*
        Register a command
    */

    const char * name;
    PyObject * command;

    if (!PyArg_ParseTuple(args, "sO", &name, &command)) {
        return 0;
    }

    int command_code = (int)PyObject_Size(commands) + 1;
    AppendMenuA(self->menu_commands, MF_STRING, command_code, name);
    PyDict_SetItem(commands, PyLong_FromLong(command_code), command);
    Py_RETURN_NONE;
}

PyObject * BaseWindow_meth_grab_mouse(BaseWindow * self, PyObject * arg) {
    /*
        Enable or disable grab mouse
    */

    bool grab = PyObject_IsTrue(arg);
    EnterCriticalSection(&self->lock);
    bool old_grab = self->raw.grab_mouse;
    self->raw.grab_mouse = grab;
    LeaveCriticalSection(&self->lock);
    // Detect changes in mouse grab
    if (!old_grab && grab) {
        // Remember where to restore the cursor
        GetCursorPos(&self->raw.mouse_restore);
        // Hide the cursor on the ui thread
        SendMessage(self->hwnd, WM_USER_GRAB_MOUSE, 0, true);
        RECT rect = {};
        GetClientRect(self->hwnd, &rect);
        ClientToScreen(self->hwnd, (POINT *)(&rect.left));
        ClientToScreen(self->hwnd, (POINT *)(&rect.right));
        int cx = (rect.left + rect.right) / 2;
        int cy = (rect.top + rect.bottom) / 2;
        // Center the cursor
        SetCursorPos(cx, cy);
        EnterCriticalSection(&self->lock);
        // Reset mouse delta
        self->raw.mouse_delta = POINT{0, 0};
        LeaveCriticalSection(&self->lock);
        self->input.mouse = POINT{0, 0};
    } else if (old_grab && !grab) {
        // Show the cursor on the ui thread
        SendMessage(self->hwnd, WM_USER_GRAB_MOUSE, 0, false);
        // Restore the cursor position
        SetCursorPos(self->raw.mouse_restore.x, self->raw.mouse_restore.y);
    }
    Py_RETURN_NONE;
}

PyObject * BaseWindow_meth_key_pressed(BaseWindow * self, PyObject * key) {
    /*
        Key pressed
    */
    // lookup the key by name
    PyObject * item = PyDict_GetItem(keymap, key);
    if (!item) {
        PyErr_Format(PyExc_KeyError, "unknown key");
        return 0;
    }
    // get the virtual key code
    int code = PyLong_AsLong(item) & 0xFF;
    // return key state
    return PyBool_FromLong(self->input.key_state[code] == KEY_PRESSED);
}

PyObject * BaseWindow_meth_key_down(BaseWindow * self, PyObject * key) {
    /*
        Key pressed or down or released
    */
    // lookup the key by name
    PyObject * item = PyDict_GetItem(keymap, key);
    if (!item) {
        PyErr_Format(PyExc_KeyError, "unknown key");
        return 0;
    }
    // get the virtual key code
    int code = PyLong_AsLong(item) & 0xFF;
    // return key state
    return PyBool_FromLong(self->input.key_state[code] != KEY_UP);
}

PyObject * BaseWindow_meth_key_released(BaseWindow * self, PyObject * key) {
    /*
        Key released
    */
    // lookup the key by name
    PyObject * item = PyDict_GetItem(keymap, key);
    if (!item) {
        PyErr_Format(PyExc_KeyError, "unknown key");
        return 0;
    }
    // get the virtual key code
    int code = PyLong_AsLong(item) & 0xFF;
    // return key state
    return PyBool_FromLong(self->input.key_state[code] == KEY_RELEASED);
}

PyObject * BaseWindow_meth_key_up(BaseWindow * self, PyObject * key) {
    /*
        Key up
    */
    // lookup the key by name
    PyObject * item = PyDict_GetItem(keymap, key);
    if (!item) {
        PyErr_Format(PyExc_KeyError, "unknown key");
        return 0;
    }
    // get the virtual key code
    int code = PyLong_AsLong(item) & 0xFF;
    // return key state
    return PyBool_FromLong(self->input.key_state[code] == KEY_UP);
}

PyObject * BaseWindow_meth_show(BaseWindow * self) {
    /*
        Show the window
    */
    ShowWindow(self->hwnd, SW_SHOW);
    Py_RETURN_NONE;
}

PyObject * BaseWindow_meth_hide(BaseWindow * self) {
    /*
        Hide the window
    */
    ShowWindow(self->hwnd, SW_HIDE);
    Py_RETURN_NONE;
}

PyObject * BaseWindow_get_visible(BaseWindow * self) {
    /*
        Is the window visible
    */
    return PyBool_FromLong(IsWindowVisible(self->hwnd));
}

PyObject * BaseWindow_get_width(BaseWindow * self) {
    /*
        Width
    */
    return Py_BuildValue("i", self->init.size.x);
}

PyObject * BaseWindow_get_height(BaseWindow * self) {
    /*
        Height
    */
    return Py_BuildValue("i", self->init.size.y);
}

PyObject * BaseWindow_get_ratio(BaseWindow * self) {
    /*
        Ratio
    */
    return Py_BuildValue("d", (double)self->init.size.x / self->init.size.y);
}

PyObject * BaseWindow_get_size(BaseWindow * self) {
    /*
        The width and height as a tuple
    */
    return Py_BuildValue("(ii)", self->init.size.x, self->init.size.y);
}

PyObject * BaseWindow_get_mouse(BaseWindow * self) {
    /*
        The mouse coordinates in the window
    */
    return Py_BuildValue("(ii)", self->input.mouse.x, self->input.mouse.y);
}

PyObject * BaseWindow_get_mouse_wheel(BaseWindow * self) {
    /*
        Mouse wheel delta
    */
    return Py_BuildValue("i", self->input.mouse_wheel);
}

PyObject * BaseWindow_get_text_input(BaseWindow * self) {
    /*
        Text input
    */
    return PyUnicode_FromWideChar(self->input.text_input, self->input.text_input_size);
}

PyObject * BaseWindow_get_drop_files(BaseWindow * self) {
    /*
        The filenames dropped on the window if the window accepts drop files
    */
    PyObject * res = PyList_New(self->input.num_drop_files);
    for (int i = 0; i < self->input.num_drop_files; ++i) {
        PyList_SET_ITEM(res, i, PyUnicode_FromWideChar(self->input.drop_files[i], -1));
    }
    return res;
}

PyObject * BaseWindow_get_placement(BaseWindow * self) {
    /*
        Binary representation of the window placement
    */
    WINDOWPLACEMENT wp = {sizeof(WINDOWPLACEMENT)};
    GetWindowPlacement(self->hwnd, &wp);
    if (!(GetWindowLong(self->hwnd, GWL_STYLE) & WS_VISIBLE)) {
        wp.showCmd = SW_HIDE;
    }
    return PyBytes_FromStringAndSize((char *)&wp, wp.length);
}

int BaseWindow_set_title(BaseWindow * self, PyObject * value) {
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

int BaseWindow_set_accept_drop_files(BaseWindow * self, PyObject * value) {
    /*
        Enable or disable accept drop files
    */
    DragAcceptFiles(self->hwnd, PyObject_IsTrue(value));
	return 0;
}

int BaseWindow_set_placement(BaseWindow * self, PyObject * value) {
    /*
        Restore window placement
    */
    WINDOWPLACEMENT * wp = (WINDOWPLACEMENT *)PyBytes_AsString(value);
    SetWindowPlacement(self->hwnd, wp);
	return 0;
}
