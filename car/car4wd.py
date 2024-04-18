from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener, KeyCode
from time import sleep
import controllableCar

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

sleep(1)

# define pins
pinRBNum = 7
pinRFNum = 6
pinLBNum = 5
pinLFNum = 4

pinServoNum = 2
pinFloodLightsNum = 3

pinLeftBack = board.get_pin(f"d:{pinLBNum}:o")
pinLeftForward = board.get_pin(f"d:{pinLFNum}:o")
pinRightBack = board.get_pin(f"d:{pinRBNum}:o")
pinRightForward = board.get_pin(f"d:{pinRFNum}:o")

pinServo = board.get_pin(f"d:{pinServoNum}:s")
pinFloodLights = board.get_pin(f"d:{pinFloodLightsNum}:o")
      
# lights up flood lights
def light_up_flood_lights(button):
    global floodLightsOn

    if button == 'f':
        if floodLightsOn:
            pinFloodLights.write(0)
            
            floodLightsOn = False
        else:
            pinFloodLights.write(1)
            floodLightsOn = True
        

# procedure for what to do when certain keys are pressed
def on_press(key):    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
     
    global car
    if type(key) == KeyCode:
        buttonPressed = key.char
        
        # set which button is currently pressed
        car.set_current_buttons_pressed(buttonPressed, "pressed")
        
        car.drive(buttonPressed)
        car.turn_on_or_off_light(buttonPressed)
        #light_up_flood_lights(buttonPressed)
        
    elif type(key) == Key:
        car.move_servo(key)

#procedure for what do when releasing buttons
def on_release(key):
    global car
    car.stop()

    if type(key) == KeyCode:
        buttonReleased = key.char
        car.set_current_buttons_pressed(buttonReleased, "released")
        
    elif type(key) == Key:
        pass
   
# procedure for key listening
def get_keys():
    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join() 
        


# turn on flood lights
#pinFloodLights.write(1)
#floodLightsOn = True

# explanatory text
print("You can start steering now")
print("'w' for forward, 's' for backward, 'a' for left, 'd' for right")

car = controllableCar.controllableCar(pinLeftBack, pinLeftForward, pinRightBack, pinRightForward)
car.add_servo(pinServo)
car.add_on_off_lights(pinFloodLights, "f")

# start main loop
get_keys()

print("Exiting program")

