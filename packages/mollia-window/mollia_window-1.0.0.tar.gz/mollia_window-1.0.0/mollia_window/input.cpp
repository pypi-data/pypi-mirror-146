#include "input.hpp"

void process_input(HWND hwnd, RawInput & raw, WndInput & input) {
    // Update keyboard input
    for (int i = 0; i < 256; ++i) {
        switch (input.key_state[i]) {
            case KEY_PRESSED:
            case KEY_DOWN:
                input.key_state[i] = raw.key_down[i] ? KEY_DOWN : KEY_RELEASED;
                break;

            case KEY_RELEASED:
            case KEY_UP:
                input.key_state[i] = raw.key_down[i] ? KEY_PRESSED : KEY_UP;
                break;
        }
    }
    // Update text input
    if (raw.text_input_size || input.text_input_size) {
        memcpy(input.text_input, raw.text_input, raw.text_input_size * sizeof(wchar_t));
        input.text_input_size = raw.text_input_size;
        raw.text_input_size = 0;
    }
    // Update drop files
    if (raw.num_drop_files || input.num_drop_files) {
        if (input.num_drop_files) {
            for (int i = 0; i < input.num_drop_files; ++i) {
                free(input.drop_files[i]);
            }
            free(input.drop_files);
        }
        input.num_drop_files = raw.num_drop_files;
        input.drop_files = raw.drop_files;
        raw.num_drop_files = 0;
        raw.drop_files = 0;
    }
    // Update commands
    input.num_commands = raw.num_commands;
    if (raw.num_commands) {
        memcpy(input.commands, raw.commands, raw.num_commands * sizeof(int));
        raw.num_commands = 0;
    }
    // Update mouse coordinates
    if (hwnd == GetForegroundWindow()) {
        RECT rect = {};
        POINT mouse = {};
        GetClientRect(hwnd, &rect);
        ClientToScreen(hwnd, (POINT *)(&rect.left));
        ClientToScreen(hwnd, (POINT *)(&rect.right));
        GetCursorPos(&mouse);
        if (raw.grab_mouse) {
            input.mouse = raw.mouse_delta;
            raw.mouse_delta = POINT{0, 0};
        } else {
            input.mouse = POINT{mouse.x - rect.left, mouse.y - rect.top};
        }
        input.mouse_wheel = raw.mouse_wheel;
        raw.mouse_wheel = 0;
    }
}
