#pragma once
#include "common.hpp"

// Messages

#define WM_USER_CREATE_MAIN (WM_USER + 0)
#define WM_USER_CREATE_CHILD (WM_USER + 1)
#define WM_USER_CREATE_PREVIEW (WM_USER + 2)
#define WM_USER_GRAB_MOUSE (WM_USER + 3)

extern DWORD ui_thread_id;

// Events

extern HANDLE main_window_ready;
extern HANDLE child_window_ready;
extern HANDLE preview_window_ready;

int init_ui_thread();
