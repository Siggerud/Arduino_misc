from pyfirmata2 import Arduino, util
from time import sleep

board = Arduino("COM5")

it = util.Iterator(board)
it.start()

board.analog[0].enable_reporting()

for i in range(100):
    if board.analog[0].read():
        print(((board.analog[0].read() * 5) - 0.5) * 100)
    sleep(0.25) 
"""

from pymata4 import pymata4
from time import sleep

board = pymata4.Pymata4(arduino_instance_id=1)

analog_pin = 0

board.set_pin_mode_analog_input(analog_pin)
sleep(1)

for i in range(100):
    print(board.analog_read(analog_pin)[0])
    sleep(0.25)
"""