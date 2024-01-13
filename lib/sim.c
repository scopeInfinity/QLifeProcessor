#ifdef OPC_SIM_ENABLED

#include <opc/io.h>
#include <opc/logging.h>
#include <unistd.h>
#include <pthread.h>
#include <stdio.h>

static int LED8x8[8][8]={0};
static const int LED_MAX_CHARGE = 10000;
static const int LED_STEP_CHARGE = 20;
static const int LED_MIN_CHARGE = LED_MAX_CHARGE/LED_STEP_CHARGE;


void sim_display_charge() {
    while(1) {
        // break;
        int row_active = MEM_IO[0];
        int col_active = MEM_IO[1];
        // loggingf("> %d, %d\n", row_active, col_active);
        for(int i=0;i<8;i++) if(row_active&(1<<i)) {
            for(int j=0;j<8;j++) if(col_active&(1<<j)) {
                LED8x8[i][j] = LED_MAX_CHARGE;
            }
        }

        sched_yield();
    }
}

void sim_display_discharge() {
    while(1) {

        for(int i=0;i<8;i++) {
            for(int j=0;j<8;j++) {
                if(LED8x8[i][j]>LED_MIN_CHARGE) LED8x8[i][j]-=LED_MIN_CHARGE;
            }
        }
        sleep(1); // we want 20ms to should fully discharge

        sched_yield();
    }
}

void sim_display() {
    while(1) {
        logging_screenf("\033[2J\033[H");
        logging_screenf("Screen 8x8\n");
        for(int i=0;i<8;i++) {
            for(int j=0;j<8;j++) {
                logging_screenf("%c", LED8x8[i][j]>LED_MIN_CHARGE?('#'):' ');
                // loggingf("%03d ", LED8x8[i][j]);
            }
            logging_screenf("\n");
        }
        sleep(200);
        sched_yield();

    }
}

__attribute__ ((__constructor__))
void init_simulator(void) {
    pthread_t thread_id;
    pthread_t thread_id2;
    pthread_t thread_id3;
    pthread_create(&thread_id, NULL, sim_display, NULL);
    pthread_create(&thread_id2, NULL, sim_display_charge, NULL);
    pthread_create(&thread_id3, NULL, sim_display_discharge, NULL);
}

#endif