from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
from time import sleep
import time #fjern
from threading import Thread

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

sleep(1)

# dictionary to keep track of which buttons are pressed at any time
currentButtonsPressed = {'w': 0, 's': 0, 'a': 0, 'd': 0, 'h': 0}

# define pins
pinLBNum = 11
pinLFNum = 10
pinRBNum = 9
pinRFNum = 6

pinRightLedNum = 2
pinLeftLedNum = 13

honkPinNum = 8

pinLB = board.get_pin(f"d:{pinLBNum}:o")
pinLF = board.get_pin(f"d:{pinLFNum}:o")
pinRB = board.get_pin(f"d:{pinRBNum}:o")
pinRF = board.get_pin(f"d:{pinRFNum}:o")

pinRightLed = board.get_pin(f"d:{pinRightLedNum}:o")
pinLeftLed = board.get_pin(f"d:{pinLeftLedNum}:o")

honkPin = board.get_pin(f"d:{honkPinNum}:o")

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
    
def turn_right():
    directionSpeeds = [1, 0, 0, 1]
    move(directionSpeeds)

def turn_left():
    directionSpeeds = [0, 1, 1, 0]
    move(directionSpeeds)
    
def turn_left_while_forward():
    directionSpeeds = [0, 1, 1, 1]
    move(directionSpeeds)
    
def turn_right_while_forward():
    directionSpeeds = [1, 1, 0, 1]
    move(directionSpeeds)
    
def turn_left_while_backward():
    directionSpeeds = [1, 0, 1, 1]
    move(directionSpeeds)

def turn_right_while_backward():
    directionSpeeds = [1, 1, 1, 0]
    move(directionSpeeds)

# keeps track of which buttons are pressed
def set_current_buttons_pressed(button, action):
    global currentButtonsPressed
    
    if button in currentButtonsPressed.keys():
        if action == "released":
            value = 0
        elif action == "pressed":
            value = 1
        currentButtonsPressed[button] = value
        print(f"{button} {action}")
        print(currentButtonsPressed)
        
def drive(button):
    global currentButtonsPressed
  
    if button == "w":
        advance()
    elif button == "s":
        back()
    elif button == "a":
        if currentButtonsPressed['w'] == 1:
            turn_left_while_forward()
        elif currentButtonsPressed['s'] == 1:
            turn_left_while_backward()
        else:
            turn_left()
    elif button == "d":
        if currentButtonsPressed['w'] == 1:
            turn_right_while_forward()
        elif currentButtonsPressed['s'] == 1:
            turn_right_while_backward()
        else:
            turn_right()

def honk(button, action):
    if button == 'h':
        if action == "pressed":
            honkPin.write(1)
        elif action == "released":
            honkPin.write(0)
            
def light_up_leds():
    if currentButtonsPressed['a'] == 1:
        pinLeftLed.write(1)
        print("lighting left")
    else:
        pinLeftLed.write(0)
        print("not lighting left")
    
    if currentButtonsPressed['d'] == 1:
        pinRightLed.write(1)
    else:
        pinRightLed.write(0)

# procedure for what to do when certain keys are pressed
def on_press(key):    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
    
    # move car if 'w', 's', 'a' or 'd' is pushed
    try:
        buttonPressed = key.char
        
        # set which button is currently pressed
        set_current_buttons_pressed(buttonPressed, "pressed")
        
        drive(buttonPressed)
        
        honk(buttonPressed, "pressed")
        
        light_up_leds()
        
    except:
        stop()

#procedure for what do when releasing buttons
def on_release(key):
    stop()
    
    try:
        buttonReleased = key.char
        set_current_buttons_pressed(buttonReleased, "released")
        
        honk(buttonReleased, "released")
        
        light_up_leds()
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