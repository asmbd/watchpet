#include "mbed.h"
#include "Servo.h"
#include "buzzer.h"

Beep buzzer(PA_1); 
Servo myservo(PA_3);
Servo servo_p(PA_7);
I2CSlave slave(D4,D5);
EventQueue queue;
Thread thr_queue;
int p_status = 0;
int end = 0;

void feeding_alert(void) {
    for(int i = 0 ; i<=1 ; i++) {
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(830,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(659,0.2);
        ThisThread::sleep_for(150);
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(830,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(659,0.2);
        ThisThread::sleep_for(150);
     
        buzzer.beep(1319,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1568,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1568,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
     
        ThisThread::sleep_for(150);
     
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(830,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(659,0.2);
        ThisThread::sleep_for(150);
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(830,0.2);
        buzzer.beep(1024,0.2);
        buzzer.beep(659,0.2);
        ThisThread::sleep_for(150);
     
        buzzer.beep(1319,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1568,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1568,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1480,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1319,0.2);
        buzzer.beep(1175,0.2);
        buzzer.beep(1568,0.2);
    }
}

void playing(int p_status) {
    if(p_status == 2)  {
        printf("--- start playing ---\n");
        servo_p = 0;
        float last_degree = 0;
        for(int i =0 ; i<=44 ; i++)  {
            float rand_degree = ((rand() % 10) / 10.0);
            if(last_degree<rand_degree) {
                for (float p=last_degree; p<rand_degree; p += 0.1) {
                    servo_p = p;
                    last_degree = rand_degree;
                    ThisThread::sleep_for(100);
                }
            }
            else if(last_degree>rand_degree) {
                for (float p=last_degree; p>rand_degree; p -= 0.1) {
                    servo_p = p;
                    last_degree = rand_degree;
                    ThisThread::sleep_for(100);
                }
            }
        ThisThread::sleep_for(300);
        }
        servo_p = 0;
//        int end = 2;
        printf("stop playing\n");
    }
}
 
void feeding(int status) {
    if(status == 1) {
        queue.call(feeding_alert);
        printf("start feeding\n");
        for (float p=0; p<1.0; p += 0.1) {
            myservo = p;
            ThisThread::sleep_for(100);
        }
        myservo = 1;
        ThisThread::sleep_for(3000);
        for(float p=1; p>=0; p -= 0.1) {
            myservo = p;
            ThisThread::sleep_for(100);
        }
        myservo = 0;
        printf("--- stop feeding ---\n");
//        int end = 1;
    }
}
 
int main() {
    char buf[20];
    printf("STM32 started...\n");
    slave.address(0xA0); // actual address = 0x50 (last bit ignored)
    thr_queue.start(
    callback(&queue,&EventQueue::dispatch_forever));
    myservo = 0;
    servo_p = 0;
    int end = 0;
    while(1) {
        int i = slave.receive();
        for(int i = 0; i < sizeof(buf); i++) buf[i] = 0; // Clear buffer
        switch (i) {
            case I2CSlave::ReadAddressed:
                if (end == 1) // switch pressed 
                    slave.write("Feeding Off", 3);
                else if (end == 2)
                    slave.write("Playing Off", 3);
//                else 
//                    slave.write("NNN", 3);
//                break;
            case I2CSlave::WriteAddressed:
                slave.read(buf, sizeof(buf)-1);
                queue.call(feeding,buf[0]);
                queue.call(playing,buf[0]);
                break;
//        end = 0; 
        }
    }
}
 
 