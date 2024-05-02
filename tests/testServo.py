#from pymata4 import pymata4
import time
from pyfirmata2 import Arduino, util

trig_pin = 3
echo_pin = 2
pin_servo = 5

#board.set_pin_mode_servo(pin_servo, min_pulse = 0, max_pulse = 180)
#board.servo_write(pin_servo, 100)

board = Arduino("COM4")

it = util.Iterator(board)
it.start()

time.sleep(1)

echo = board.get_pin(f"d:{echo_pin}:i")
trig = board.get_pin(f"d:{trig_pin}:o")

trig.write(0)
time.sleep(1)

def getMicroSeconds(num):
    return num / 1000000

start = time.time()
while True:
    if (time.time() - start) > 10:
        break
    trig.write(0)
    #digitalWrite(outputPin, LOW);
    time.sleep(getMicroSeconds(2))
    #delayMicroseconds(2);
    trig.write(1)
    #digitalWrite(outputPin, HIGH);
    time.sleep(getMicroSeconds(10))
    #delayMicroseconds(10);
    trig.write(0)
    #digitalWrite(outputPin, LOW);
    if echo.read() != None:
        print(echo.read())
    #float Fdistance = pulseIn(inputPin, HIGH);
    #Fdistance= Fdistance/5.8/10;
    #Serial.print("F distance:");
    #Serial.println(Fdistance);
    #Fspeedd = Fdistance;
