#ifndef OPS_SIM
#include <stdarg.h>
#include <stdio.h>

int loggingf(char *fmt, ...) {
  va_list args;
  va_start (args, fmt);
  int ret = vfprintf(stderr, fmt, args);
  fflush(stdout);
  va_end (args);
  return ret;
}
int logging_screenf(char *fmt, ...) {
  va_list args;
  va_start (args, fmt);
  int ret = vfprintf(stdout, fmt, args);
  fflush(stdout);
  va_end (args);
  return ret;
}


#else
int loggingf(char *fmt, ...) {
}
int logging_screenf(char *fmt, ...){
}
#endif