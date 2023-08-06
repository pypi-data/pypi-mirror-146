#pragma once
#include "common.hpp"

enum KeyState {
    KEY_UP,
    KEY_PRESSED,
    KEY_DOWN,
    KEY_RELEASED,
};

// Raw input is generated on the ui thread

struct RawInput {
    bool grab_mouse;
    bool key_down[256];
    int mouse_wheel;
    int text_input_size;
    wchar_t text_input[256];
    POINT mouse_restore;
    POINT mouse_delta;
    wchar_t ** drop_files;
    int num_drop_files;
    bool alive;
    int commands[256];
    int num_commands;
};

// Window input is generated on update() using the raw input

struct WndInput {
    POINT mouse;
    int mouse_wheel;
    KeyState key_state[256];
    int text_input_size;
    wchar_t text_input[256];
    wchar_t ** drop_files;
    int num_drop_files;
    int commands[256];
    int num_commands;
};

void process_input(HWND hwnd, RawInput & raw, WndInput & input);
