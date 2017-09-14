// exampleApp.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <iostream>
#include <string>
#include <unistd.h>
#include "jetsonGPIO.h"
using namespace std;

int main(int argc, char *argv[]){

    cout << "Starting the 100,000 blink test" << endl;

    jetsonTX1GPIONumber orangeLED = gpio219 ;     // Ouput
    gpioExport(orangeLED) ;
    gpioSetDirection(orangeLED,outputPin) ;

    // Flash the LED 100,000 times
    for(int i = 0; i < 100000; ++i){
        cout << "Setting the LED on" << endl;
        gpioSetValue(orangeLED, on);
        usleep(80000);         // on for 200ms
        cout << "Setting the LED off" << endl;
        gpioSetValue(orangeLED, off);
        usleep(80000);         // off for 200ms
    }


    gpioUnexport(orangeLED);     // unexport the LED
    return 0;
}


