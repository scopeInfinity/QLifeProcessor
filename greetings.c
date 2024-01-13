#include <stdint.h>
#include <opc/io.h>
#include <opc/time.h>
#include <opc/logging.h>
#include <opc/font.h>

int is_clicked() {
    // check bit-0
    uint8_t *key = &MEM_IO[2];
    if((*key)&1) {
        // can lead to race conditions, but it's ok
        (*key) &= ~1;  // reset bit
        // TODO: need some sort of flush
    }
}

void print_character(char c) {
  if(c>=128) return;
  // display char for 1s
  for(int dur=0;dur<200;dur++) {
    for(int i=0;i<8;i++) {
      MEM_IO[0]=1<<i; // enable only ith row in 8x8 matrix
      MEM_IO[1]=font[c][i]; // set data to ith row in 8x8 matrix
      loggingf("%d,%d\n", MEM_IO[0], MEM_IO[1]);
      sleep(1);
    }
  }
}

void update_screen(char *msg) {
  for(int i=0;msg[i]!='\0';i++) {
    print_character(msg[i]);
  }
}

void main() {
  int msg_index = 0;
  char* msgs[] = {"Happy Diwali", "Merry Christmas!"};
  int msg_len = 2;

  while(1) {
     if(is_clicked()) {
        msg_index = (msg_index+1)%msg_len;
     }
    update_screen(msgs[msg_index]);
  }
}
