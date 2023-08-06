#pragma once
#include <Python.h>

#define UNICODE
#include <Windows.h>

#define xstr(s) str(s)
#define str(s) #s

#define xstr(x) str(x)
#define TRACE() __FUNCTION__ " (" __FILE__ ":" xstr(__LINE__) ")"

#define WND_STYLE (WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX)

inline POINT window_size(POINT size, bool menu) {
    /*
        Shortcut to calculate the width and height of the window
    */
    RECT rect = {0, 0, size.x, size.y};
    AdjustWindowRect(&rect, WND_STYLE, menu);
    return {rect.right - rect.left, rect.bottom - rect.top};
}
