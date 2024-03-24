from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
from time import sleep

board = Arduino("COM7")

it = util.Iterator(board)
it.start()

#switchPinNum = 2
#motorPinNum = 9
#switchState = 0
bluePinNum = 5
yellowPinNum = 6

#pin_switch = board.get_pin(f"d:{switchPinNum}:i")
#pin_switch.enable_reporting()
#pin_motor = board.get_pin(f"d:{motorPinNum}:o") 
pinBlue = board.get_pin(f"d:{bluePinNum}:o")
pinYellow = board.get_pin(f"d:{yellowPinNum}:o")


#sleep(1)

def on_press(key):
    if key.char == "y":
        pinYellow.write(1)
        pinBlue.write(0)
    elif key.char == "b":
        pinYellow.write(0)
        pinBlue.write(1)

def on_release(key):
    pinYellow.write(0)
    pinBlue.write(0)
    
def get_keys():
    with Listener(on_press = on_press, on_release = on_release) as listener: 
        listener.join()

while True:
    print("before")
    get_keys()
    print("after")
    
    #switchState = pin_switch.read()
    
    #if(switchState):
    #    pin_motor.write(1)
    #else:
    #    pin_motor.write(0)
    
        