#include <string>
#include <iostream>
#include <stdio.h>
#include <sstream>

void handle_output(void (*callback)(int,int), int process_id, int value) {
    callback(process_id, value);
}

void fast_io(void (*callback)(int,int)) {
    unsigned int pid, v;
    int len = scanf("IPC %x %x\n", &pid, &v);
    if(len>0) {
        handle_output(callback, pid, v);
    }
}

extern "C" void fast_io_loop(void (*callback)(int,int)) {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    while(1) {
        fast_io(callback);
    }
}
