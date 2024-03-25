from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
from time import sleep

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

sleep(1)

# define pins
pinLBNum = 6
pinLFNum = 9
pinRBNum = 10
pinRFNum = 11

pinLB = board.get_pin(f"d:{pinLBNum}:o")
pinLF = board.get_pin(f"d:{pinLFNum}:o")
pinRB = board.get_pin(f"d:{pinRBNum}:o")
pinRF = board.get_pin(f"d:{pinRFNum}:o")

def advance():
    global pinLB
    global pinLF
    global pinRB
    global pinRF
    
    pinRB.write(1)
    pinRF.write(0)
    pinLB.write(1)
    pinLF.write(0)
    
def back():
    global pinLB
    global pinLF
    global pinRB
    global pinRF
    
    pinRB.write(0)
    pinRF.write(1)
    pinLB.write(0)
    pinLF.write(1)
    
def stop():
    global pinLB
    global pinLF
    global pinRB
    global pinRF

    pinRB.write(1)
    pinRF.write(1)
    pinLB.write(1)
    pinLF.write(1)
    
def turnRight():
    global pinLB
    global pinLF
    global pinRB
    global pinRF

    pinRB.write(1)
    pinRF.write(0)
    pinLB.write(0)
    pinLF.write(1)

def turnLeft():
    global pinLB
    global pinLF
    global pinRB
    global pinRF

    pinRB.write(0)
    pinRF.write(1)
    pinLB.write(1)
    pinLF.write(0)

# procedure for what to do when certain keys are pressed
def on_press(key):    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
    
    # light up yellow LED when "y" is pressed
    try:
        if key.char == "w":
            advance()
        elif key.char == "s":
            back()
        elif key.char == "a":
            turnLeft()
        elif key.char == "d":
            turnRight()
    except:
        stop()

#procedure for what do when releasing buttons
def on_release(key):
    stop()
   
# procedure for key listening
def get_keys():
    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()

print("You can start steering now")
print("'w' for forward, 's' for backward, 'a' for left, 'd' for right")
get_keys()
print("Exiting program")