#include <opc/font.h>
#include <stdio.h>

void print_char(char c) {
    for(int i=0;i<8;i++) {
        int col=font[c][i];
        printf("%02x\n", col);
    }
}

int main(int argc, char *argv[]) {
    if(argc!=2) {
        printf("Please provide exactly one argument\n");
        return 1;
    }
    for(int i=0;argv[1][i]!='\0';i++) {
        print_char(argv[1][i]);
    }
}