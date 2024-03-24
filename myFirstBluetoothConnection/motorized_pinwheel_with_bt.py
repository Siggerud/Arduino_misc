from pyfirmata2 import Arduino, util
from time import sleep

board = Arduino("COM7")

it = util.Iterator(board)
it.start()

switchPinNum = 2
motorPinNum = 9
switchState = 0

pin_switch = board.get_pin(f"d:{switchPinNum}:i")
pin_switch.enable_reporting()
pin_motor = board.get_pin(f"d:{motorPinNum}:o") 

sleep(1)

while True:
    switchState = pin_switch.read()
    
    if(switchState):
        pin_motor.write(1)
    else:
        pin_motor.write(0)
    
        