// TODO: The value is rough estimation for a regular laptop.
static int TICKS_PER_MS = 450000;

void sleep(int ms) {
    int _x=1;
    int steps = TICKS_PER_MS * ms;
    for(int i=0;i<steps;i++) _x*=_x;
}