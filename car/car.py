from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
from time import sleep

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

sleep(1)

# dictionary to keep track of which buttons are pressed at any time
currentButtonsPressed = {'w': 0, 's': 0, 'a': 0, 'd': 0}

# define pins
pinLBNum = 11
pinLFNum = 10
pinRBNum = 9
pinRFNum = 6

pinLB = board.get_pin(f"d:{pinLBNum}:o")
pinLF = board.get_pin(f"d:{pinLFNum}:o")
pinRB = board.get_pin(f"d:{pinRBNum}:o")
pinRF = board.get_pin(f"d:{pinRFNum}:o")

# moves the car according to input for directions
def move(directionSpeeds):
    global pinLB
    global pinLF
    global pinRB
    global pinRF
    
    pinRB.write(directionSpeeds[0])
    pinRF.write(directionSpeeds[1])
    pinLB.write(directionSpeeds[2])
    pinLF.write(directionSpeeds[3])

def advance():
    directionSpeeds = [0, 1, 0, 1]
    move(directionSpeeds)
    
def back():
    directionSpeeds = [1, 0, 1, 0]
    move(directionSpeeds)
    
def stop():
    directionSpeeds = [1, 1, 1, 1]
    move(directionSpeeds)
    
def turnRight():
    directionSpeeds = [1, 0, 0, 1]
    move(directionSpeeds)

def turnLeft():
    directionSpeeds = [0, 1, 1, 0]
    move(directionSpeeds)
    
def turnLeftWhileForward():
    directionSpeeds = [0, 1, 1, 1]
    move(directionSpeeds)
    
def turnRightWhileForward():
    directionSpeeds = [1, 1, 0, 1]
    move(directionSpeeds)
    
def turnLeftWhileBackward():
    directionSpeeds = [1, 0, 1, 1]
    move(directionSpeeds)

def turnRightWhileBackward():
    directionSpeeds = [1, 1, 1, 0]
    move(directionSpeeds)

# keeps track of which buttons are pressed
def setCurrentButtonsPressed(button, action):
    global currentButtonsPressed
    
    if button in currentButtonsPressed.keys():
        if action == "released":
            value = 0
        elif action == "pressed":
            value = 1
        currentButtonsPressed[button] = value

# procedure for what to do when certain keys are pressed
def on_press(key):    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
    
    # move car if 'w', 's', 'a' or 'd' is pushed
    try:
        buttonPressed = key.char
        if buttonPressed == "w":
            advance()
        elif buttonPressed == "s":
            back()
        elif buttonPressed == "a":
            if currentButtonsPressed['w'] == 1:
                turnLeftWhileForward()
            elif currentButtonsPressed['s'] == 1:
                turnLeftWhileBackward()
            else:
                turnLeft()
        elif buttonPressed == "d":
            if currentButtonsPressed['w'] == 1:
                turnRightWhileForward()
            elif currentButtonsPressed['s'] == 1:
                turnRightWhileBackward()
            else:
                turnRight()
                
        # set which button is currently pressed
        setCurrentButtonsPressed(buttonPressed, "pressed")
    except:
        stop()

#procedure for what do when releasing buttons
def on_release(key):
    stop()
    
    try:
        buttonReleased = key.char
        setCurrentButtonsPressed(buttonReleased, "released")
    except:
        pass
   
# procedure for key listening
def get_keys():
    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()

print("You can start steering now")
print("'w' for forward, 's' for backward, 'a' for left, 'd' for right")
get_keys()
print("Exiting program")