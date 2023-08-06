#include "pixels.hpp"

#include "module.hpp"

void init_pixels(Pixels & pixels, POINT size, int bpp, bool flip) {
    /*
        Allocate memory for the pixels
    */
    pixels.size = ((size.x * bpp + 3) & ~3) * size.y;
    pixels.ptr = malloc(pixels.size);
    memset(pixels.ptr, 0, pixels.size);
    pixels.flip = flip;
    pixels.bpp = bpp;
    pixels.dirty = true;
}

PyObject * update_pixels(Pixels & pixels, PyObject * data) {
    /*
        Update pixels
    */

    // Allow pillow images
    if ((PyObject *)data->ob_type == pillow_image) {
        // Call Image.tobytes(...)
        PyObject * bytes = PyObject_CallMethod(data, "tobytes", "ssii", "raw", pixels.bpp == 3 ? "BGR" : "BGRX", 0, 1);
        if (!bytes) {
            return 0;
        }
        // recursive call to land to use the buffer protocol
        PyObject * res = update_pixels(pixels, bytes);
        Py_DECREF(bytes);
        return res;
    } else if (data != Py_None) {
        // Use the buffer protocol to get the pixels
        Py_buffer view = {};
        if (PyObject_GetBuffer(data, &view, PyBUF_STRIDED_RO)) {
            return 0;
        }
        if (pixels.size != view.len) {
            PyErr_Format(PyExc_Exception, pixels.size < view.len ? "buffer overflow" : "buffer underflow");
            return 0;
        }
        // Copy the pixels
        PyBuffer_ToContiguous(pixels.ptr, &view, view.len, 'C');
        PyBuffer_Release(&view);
    }
    Py_RETURN_NONE;
}
