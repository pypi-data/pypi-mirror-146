#include "ui_thread.hpp"

#include "child_window.hpp"
#include "main_window.hpp"
#include "preview_window.hpp"

HANDLE main_window_ready;
HANDLE child_window_ready;
HANDLE preview_window_ready;

HINSTANCE ui_thread_hinst;
HANDLE ui_thread_ready;
HANDLE ui_thread;
DWORD ui_thread_id;

#define WGL_ACCELERATION 0x2003
#define WGL_COLOR_BITS 0x2014
#define WGL_CONTEXT_FLAGS 0x2094
#define WGL_CONTEXT_MAJOR_VERSION 0x2091
#define WGL_CONTEXT_MINOR_VERSION 0x2092
#define WGL_DEPTH_BITS 0x2022
#define WGL_DOUBLE_BUFFER 0x2011
#define WGL_DRAW_TO_WINDOW 0x2001F
#define WGL_FULL_ACCELERATION 0x2027
#define WGL_PIXEL_TYPE 0x2013
#define WGL_SAMPLES 0x2042
#define WGL_STENCIL_BITS 0x2023
#define WGL_SUPPORT_OPENGL 0x2010
#define WGL_TYPE_RGBA 0x202B
#define WGL_CONTEXT_PROFILE_MASK 0x9126
#define WGL_CONTEXT_CORE_PROFILE_BIT 0x0001

typedef HGLRC (WINAPI * _wglCreateContextAttribsProc)(HDC hdc, HGLRC hglrc, const int * attribList);
_wglCreateContextAttribsProc _wglCreateContextAttribs;

// default pixel format descriptor
PIXELFORMATDESCRIPTOR pfd = {
    sizeof(PIXELFORMATDESCRIPTOR),
    1,
    PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_GENERIC_ACCELERATED | PFD_DOUBLEBUFFER,
    0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 0,
};

void paint_pixels(HWND hwnd, Pixels * pixels, POINT size) {
    /*
        Copy the pixels to the device content of the window
        Used by the child_window and the preview_window
    */
    PAINTSTRUCT ps = {};
    HDC hdc = BeginPaint(hwnd, &ps);
    BITMAPINFO info = {};
    info.bmiHeader.biBitCount = pixels->bpp * 8;
    info.bmiHeader.biWidth = size.x;
    info.bmiHeader.biHeight = pixels->flip ? size.y : -size.y;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biSizeImage = pixels->size;
    info.bmiHeader.biCompression = BI_RGB;
    StretchDIBits(hdc, 0, 0, size.x, size.y, 0, 0, size.x, size.y, pixels->ptr, &info, DIB_RGB_COLORS, SRCCOPY);
    EndPaint(hwnd, &ps);
}

LRESULT CALLBACK BaseWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    /*
        Handle window create, inputs and drop files
    */
    BaseWindow * window = (BaseWindow *)GetWindowLongPtr(hWnd, GWLP_USERDATA);
    switch (uMsg) {
        case WM_CREATE: {
            // Store the pointer to the python object in the user data of the hwnd
            SetWindowLongPtr(hWnd, GWLP_USERDATA, (LPARAM)((CREATESTRUCT *)lParam)->lpCreateParams);
            window = (BaseWindow *)lParam;
            break;
        }
		case WM_DROPFILES: {
            // Handle drop files
            EnterCriticalSection(&window->lock);
            int count = DragQueryFile((HDROP)wParam, -1, 0, 0);
            window->raw.num_drop_files += count;
            window->raw.drop_files = (wchar_t **)realloc(window->raw.drop_files, sizeof(wchar_t *) * window->raw.num_drop_files);
            for (int i = 0; i < count; ++i) {
                int size = DragQueryFile((HDROP)wParam, i, 0, 0);
                wchar_t * filename = (wchar_t *)malloc(sizeof(wchar_t) * (size + 1));
                DragQueryFile((HDROP)wParam, i, filename, size + 1);
                window->raw.drop_files[window->raw.num_drop_files - count + i] = filename;
            }
            DragFinish((HDROP)wParam);
            LeaveCriticalSection(&window->lock);
			return 0;
		}
        case WM_USER_GRAB_MOUSE: {
            // Hide the cursor on grab_mouse
            ShowCursor(!lParam);
            break;
        }
        case WM_COMMAND: {
            EnterCriticalSection(&window->lock);
            // Handle menu commands
            window->raw.commands[window->raw.num_commands++] = LOWORD(wParam);
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_MOUSEMOVE: {
            EnterCriticalSection(&window->lock);
            // Handle mouse movement
            RECT rect = {};
            POINT mouse = {};
            GetClientRect(window->hwnd, &rect);
            ClientToScreen(window->hwnd, (POINT *)(&rect.left));
            ClientToScreen(window->hwnd, (POINT *)(&rect.right));
            GetCursorPos(&mouse);
            // Handle grab mouse
            if (window->raw.grab_mouse) {
                int cx = (rect.left + rect.right) / 2;
                int cy = (rect.top + rect.bottom) / 2;
                if (mouse.x != cx || mouse.y != cy) {
                    window->raw.mouse_delta.x += mouse.x - cx;
                    window->raw.mouse_delta.y += mouse.y - cy;
                    SetCursorPos(cx, cy);
                }
            }
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_LBUTTONDOWN: {
            EnterCriticalSection(&window->lock);
            // mouse1 or lbutton
            window->raw.key_down[1] = true;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_LBUTTONUP: {
            EnterCriticalSection(&window->lock);
            // mouse1 or lbutton
            window->raw.key_down[1] = false;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_RBUTTONDOWN: {
            EnterCriticalSection(&window->lock);
            // mouse2 or rbutton
            window->raw.key_down[2] = true;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_RBUTTONUP: {
            EnterCriticalSection(&window->lock);
            // mouse2 or rbutton
            window->raw.key_down[2] = false;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_MBUTTONDOWN: {
            EnterCriticalSection(&window->lock);
            // mouse3 or mbutton
            window->raw.key_down[4] = true;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_MBUTTONUP: {
            EnterCriticalSection(&window->lock);
            // mouse3 or mbutton
            window->raw.key_down[4] = false;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_MOUSEWHEEL: {
            EnterCriticalSection(&window->lock);
            // Mouse wheel
            window->raw.mouse_wheel += GET_WHEEL_DELTA_WPARAM(wParam);
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_KEYDOWN: {
            EnterCriticalSection(&window->lock);
            // Keyboard
            window->raw.key_down[wParam & 0xFF] = true;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_KEYUP: {
            EnterCriticalSection(&window->lock);
            // Keyboard
            window->raw.key_down[wParam & 0xFF] = false;
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_CHAR: {
            EnterCriticalSection(&window->lock);
            // Text input
            if (window->raw.text_input_size < 256 - 1) {
                window->raw.text_input[window->raw.text_input_size++] = wParam & 0xFFFF;
            }
            LeaveCriticalSection(&window->lock);
            break;
        }
        case WM_ACTIVATE: {
            EnterCriticalSection(&window->lock);
            // Clear keyboard inputs on inactivate
            if (wParam == WA_INACTIVE) {
                for (int i = 0; i < 256; ++i) {
                    window->raw.key_down[i] = false;
                }
            }
            LeaveCriticalSection(&window->lock);
            break;
        }
    }
    return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

LRESULT CALLBACK MainWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    /*
        Handle main_window close
    */
    MainWindow * window = (MainWindow *)GetWindowLongPtr(hWnd, GWLP_USERDATA);
    switch (uMsg) {
        case WM_CLOSE: {
            EnterCriticalSection(&window->lock);
            // Signal the next update()
            window->raw.alive = false;
            LeaveCriticalSection(&window->lock);
            return 0;
        }
    }
    // Handle window create, inputs and drop files
    return BaseWindowProc(hWnd, uMsg, wParam, lParam);
}

LRESULT CALLBACK ChildWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    /*
        Handle child_window close and paint
    */
    ChildWindow * window = (ChildWindow *)GetWindowLongPtr(hWnd, GWLP_USERDATA);
    switch (uMsg) {
        case WM_CLOSE: {
            // Hide on close.
            ShowWindow(hWnd, SW_HIDE);
            return 0;
        }
        case WM_PAINT: {
            // Copy the pixels and mark as non dirty
            paint_pixels(window->hwnd, &window->pixels, window->init.size);
            window->pixels.dirty = false;
            break;
        }
    }
    // Handle window create, inputs and drop files
    return BaseWindowProc(hWnd, uMsg, wParam, lParam);
}

LRESULT CALLBACK PreviewWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    /*
        Handle preview_window
    */
    PreviewWindow * window = (PreviewWindow *)GetWindowLongPtr(hWnd, GWLP_USERDATA);
    switch (uMsg) {
        case WM_CREATE: {
            // Store the pointer to the python object in the user data of the hwnd
            SetWindowLongPtr(hWnd, GWLP_USERDATA, (LPARAM)((CREATESTRUCT *)lParam)->lpCreateParams);
            window = (PreviewWindow *)lParam;
            break;
        }
        case WM_CLOSE: {
            // Hide on close
            ShowWindow(hWnd, SW_HIDE);
            return 0;
        }
        case WM_PAINT: {
            paint_pixels(window->hwnd, &window->pixels, window->init.size);
            window->pixels.dirty = false;
            break;
        }
    }
    return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

void ui_thread_proc(const char ** error_trace) {
    /*
        Separate non-python thread to run the windows message loop
    */

    {
        // Load modern opengl context

        HMODULE hinst = GetModuleHandle(0);
        if (!hinst) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        WNDCLASS extClass = {CS_OWNDC, DefWindowProc, 0, 0, hinst, 0, 0, 0, 0, L"mollia_context_loader"};
        if (!RegisterClass(&extClass)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        HWND loader_hwnd = CreateWindow(L"mollia_context_loader", 0, 0, 0, 0, 0, 0, 0, 0, hinst, 0);
        if (!loader_hwnd) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        HDC loader_hdc = GetDC(loader_hwnd);
        if (!loader_hdc) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        int loader_pixelformat = ChoosePixelFormat(loader_hdc, &pfd);
        if (!loader_pixelformat) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        if (!SetPixelFormat(loader_hdc, loader_pixelformat, &pfd)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        HGLRC loader_hglrc = wglCreateContext(loader_hdc);
        if (!loader_hglrc) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        if (!wglMakeCurrent(loader_hdc, loader_hglrc)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        // Lookup the function for modern opengl context creation
        _wglCreateContextAttribs = (_wglCreateContextAttribsProc)wglGetProcAddress("wglCreateContextAttribsARB");
        if (!_wglCreateContextAttribs) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        // Destroy the loader

        if (!wglMakeCurrent(0, 0)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        if (!wglDeleteContext(loader_hglrc)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        if (!ReleaseDC(loader_hwnd, loader_hdc)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        if (!DestroyWindow(loader_hwnd)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }

        if (!UnregisterClass(L"mollia_context_loader", hinst)) {
            *error_trace = TRACE();
            SetEvent(main_window_ready);
            return;
        }
    }

    // Create a window with modern opengl context

    ui_thread_hinst = GetModuleHandle(0);

    if (!ui_thread_hinst) {
        *error_trace = TRACE();
        SetEvent(main_window_ready);
        return;
    }

    // Register the main_window class

    WNDCLASSW wnd_class = {
        CS_OWNDC,
        MainWindowProc,
        0,
        0,
        ui_thread_hinst,
        0,
        (HCURSOR)LoadCursor(0, IDC_ARROW),
        0,
        0,
        L"mollia_main_window",
    };

    if (!RegisterClass(&wnd_class)) {
        *error_trace = TRACE();
        SetEvent(main_window_ready);
        return;
    }

    // Register the child_window class

    WNDCLASSW child_wnd_class = {
        0,
        ChildWindowProc,
        0,
        0,
        ui_thread_hinst,
        0,
        (HCURSOR)LoadCursor(0, IDC_ARROW),
        0,
        0,
        L"mollia_child_window",
    };

    if (!RegisterClass(&child_wnd_class)) {
        *error_trace = TRACE();
        SetEvent(main_window_ready);
        return;
    }

    // Register the preview_window class

    WNDCLASSW preview_wnd_class = {
        0,
        PreviewWindowProc,
        0,
        0,
        ui_thread_hinst,
        0,
        (HCURSOR)LoadCursor(0, IDC_ARROW),
        0,
        0,
        L"mollia_preview_window",
    };

    if (!RegisterClass(&preview_wnd_class)) {
        *error_trace = TRACE();
        SetEvent(main_window_ready);
        return;
    }

    // Main windows message loop

    MSG msg;
    // Peek the message to ensure that the message queue is created before reporting ui_thread_redy
    PeekMessage(&msg, 0, 0, 0, PM_NOREMOVE);
    // Allow the parent thread to continue
    SetEvent(ui_thread_ready);

    // Enter the main loop

    while (GetMessage(&msg, 0, 0, 0)) {
        // Handle window creation on the ui thread
        switch (msg.message) {
            case WM_USER_CREATE_MAIN: {
                /*
                    Create the main_window on the ui thread
                */

                // Create the menubar

                main_window->menubar = CreateMenu();
                main_window->menu_commands = CreateMenu();
                main_window->menu_windows = CreateMenu();

                AppendMenuA(main_window->menubar, MF_POPUP, (UINT_PTR)main_window->menu_commands, "&Commands");
                AppendMenuA(main_window->menubar, MF_POPUP, (UINT_PTR)main_window->menu_windows, "&Windows");

                // Calculate the window size depending on the style and menu
                POINT wnd_size = window_size(main_window->init.size, main_window->init.menubar);

                // Create the window
                main_window->hwnd = CreateWindowEx(
                    0,
                    L"mollia_main_window",
                    0,
                    main_window->init.visible ? (WS_VISIBLE | WND_STYLE) : WND_STYLE,
                    main_window->init.pos.x,
                    main_window->init.pos.y,
                    wnd_size.x,
                    wnd_size.y,
                    0,
                    main_window->init.menubar ? main_window->menubar : 0,
                    ui_thread_hinst,
                    main_window
                );

                if (!main_window->hwnd) {
                    *error_trace = TRACE();
                    SetEvent(main_window_ready);
                    return;
                }

                // Show and activate the window
                SetForegroundWindow(main_window->hwnd);
                SetActiveWindow(main_window->hwnd);
                SetFocus(main_window->hwnd);

                main_window->hdc = GetDC(main_window->hwnd);

                if (!main_window->hdc) {
                    *error_trace = TRACE();
                    SetEvent(main_window_ready);
                    return;
                }

                {
                    /*
                        Create an opengl 3.3 context.
                    */

                    int pixelformat = ChoosePixelFormat(main_window->hdc, &pfd);
                    if (!pixelformat) {
                        *error_trace = TRACE();
                        SetEvent(main_window_ready);
                        return;
                    }

                    if (!SetPixelFormat(main_window->hdc, pixelformat, &pfd)) {
                        *error_trace = TRACE();
                        SetEvent(main_window_ready);
                        return;
                    }

                    int attriblist[] = {
                        WGL_CONTEXT_PROFILE_MASK, WGL_CONTEXT_CORE_PROFILE_BIT,
                        WGL_CONTEXT_MAJOR_VERSION, 3,
                        WGL_CONTEXT_MINOR_VERSION, 3,
                        0, 0,
                    };

                    // Use the function from the context loader
                    main_window->hrc = _wglCreateContextAttribs(main_window->hdc, 0, attriblist);
                    if (!main_window->hrc) {
                        *error_trace = TRACE();
                        SetEvent(main_window_ready);
                        return;
                    }
                }

                // Signal the next update()
                main_window->raw.alive = true;

                // Signal the main thread
                SetEvent(main_window_ready);
                break;
            }
            case WM_USER_CREATE_CHILD: {
                /*
                    Create a child_window on the ui thread
                */

                ChildWindow * child_window = (ChildWindow *)msg.lParam;

                // Create the menubar

                child_window->menubar = CreateMenu();
                child_window->menu_commands = CreateMenu();

                AppendMenuA(child_window->menubar, MF_POPUP, (UINT_PTR)child_window->menu_commands, "&Commands");

                // Calculate the window size depending on the style and menu
                POINT wnd_size = window_size(child_window->init.size, child_window->init.menubar);

                // Create the window
                child_window->hwnd = CreateWindowEx(
                    0,
                    L"mollia_child_window",
                    0,
                    child_window->init.visible ? (WS_VISIBLE | WND_STYLE) : WND_STYLE,
                    child_window->init.pos.x,
                    child_window->init.pos.y,
                    wnd_size.x,
                    wnd_size.y,
                    child_window->above_main ? main_window->hwnd : 0,
                    child_window->init.menubar ? child_window->menubar : 0,
                    ui_thread_hinst,
                    child_window
                );

                if (!child_window->hwnd) {
                    *error_trace = TRACE();
                    SetEvent(child_window_ready);
                    return;
                }

                // Signal the main thread
                SetEvent(child_window_ready);
                break;
            }
            case WM_USER_CREATE_PREVIEW: {
                /*
                    Create a preview_window on the ui thread
                */
                PreviewWindow * preview_window = (PreviewWindow *)msg.lParam;

                // Calculate the window size depending on the style and menu
                POINT wnd_size = window_size(preview_window->init.size, false);

                // Create the window
                preview_window->hwnd = CreateWindowEx(
                    0,
                    L"mollia_preview_window",
                    0,
                    preview_window->init.visible ? (WS_VISIBLE | WND_STYLE) : WND_STYLE,
                    preview_window->init.pos.x,
                    preview_window->init.pos.y,
                    wnd_size.x,
                    wnd_size.y,
                    0,
                    0,
                    ui_thread_hinst,
                    preview_window
                );

                // Signal the main thread
                SetEvent(preview_window_ready);
                break;
            }
            default: {
                // Standard windows messages
                TranslateMessage(&msg);
                DispatchMessage(&msg);
                break;
            }
        }
    }
}

int init_ui_thread() {
    /*
        Initialize the ui thread
        Create the events and the thread with the message loop
        Wait for the ui thread to reach the main loop
        The ui thread will be created only once
    */
    static bool first_run = true;
    if (first_run) {
        first_run = false;

        ui_thread_ready = CreateEvent(0, 1, 0, 0);
        main_window_ready = CreateEvent(0, 1, 0, 0);
        child_window_ready = CreateEvent(0, 1, 0, 0);
        preview_window_ready = CreateEvent(0, 1, 0, 0);

        const char * error_trace = 0;
        ui_thread = CreateThread(0, 0, (LPTHREAD_START_ROUTINE)ui_thread_proc, &error_trace, 0, &ui_thread_id);
        WaitForSingleObject(ui_thread_ready, INFINITE);
        if (error_trace) {
            PyErr_Format(PyExc_Exception, "error in %s", error_trace);
            return -1;
        }
    }
    return 0;
}
