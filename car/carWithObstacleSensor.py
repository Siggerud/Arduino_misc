from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
from time import sleep

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

sleep(1)

# dictionary to keep track of which buttons are pressed at any time
currentButtonsPressed = {'w': 0, 's': 0, 'a': 0, 'd': 0, 'h': 0}

# define pins
pinLeftBackNum = 11
pinLeftForwardNum = 10
pinRightBackNum = 9
pinRightForwardNum = 6

pinRightLedNum = 2
pinLeftLedNum = 13

pinObstacleSensorNum = 3

honkPinNum = 8

pinLeftBack = board.get_pin(f"d:{pinLeftBackNum}:o")
pinLeftForward = board.get_pin(f"d:{pinLeftForwardNum}:o")
pinRightBack = board.get_pin(f"d:{pinRightBackNum}:o")
pinRightForward = board.get_pin(f"d:{pinRightForwardNum}:o")

pinRightLed = board.get_pin(f"d:{pinRightLedNum}:o")
pinLeftLed = board.get_pin(f"d:{pinLeftLedNum}:o")

pinObstacleSensor = board.get_pin(f"d:{pinObstacleSensorNum}:")

honkPin = board.get_pin(f"d:{honkPinNum}:o")

# moves the car according to input for directions
def move(directionSpeeds):
    global pinLeftBack
    global pinLeftForward
    global pinRightBack
    global pinRightForward
    
    pinRightBack.write(directionSpeeds[0])
    pinRightForward.write(directionSpeeds[1])
    pinLeftBack.write(directionSpeeds[2])
    pinLeftForward.write(directionSpeeds[3])

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

# drives according to user input, stops if car is too close too obstacle       
def drive(button):
    global currentButtonsPressed
    global stopCar
  
    if button == "w":
        advance()
    elif button == "s":
        if too_close_to_obstacle():
            stop()
            print("Stopping car")
        else:
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

# makes the buzzer 'honk'
def honk(button, action):
    if button == 'h':
        if action == "pressed":
            honkPin.write(1)
        elif action == "released":
            honkPin.write(0)

# lights up leds when turning the car          
def light_up_leds():
    if currentButtonsPressed['a'] == 1:
        pinLeftLed.write(1)
    else:
        pinLeftLed.write(0)
    
    if currentButtonsPressed['d'] == 1:
        pinRightLed.write(1)
    else:
        pinRightLed.write(0)

# procedure for what to do when certain keys are pressed
def on_press(key):    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
     
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

# checks if car is too close to a obstacle
def too_close_to_obstacle():
    global pinObstacleSensor
    global currentButtonsPressed
    global stopCar

    noDanger = pinObstacleSensor.read()
    
    if noDanger == False:
        return True
    else:
        return False

print("You can start steering now")
print("'w' for forward, 's' for backward, 'a' for left, 'd' for right")
get_keys()
print("Exiting program")