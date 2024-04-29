from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener, KeyCode
from time import sleep
import controllableCar
from threading import Thread
import sensorGUI
from tkinter import Tk
import pinManager

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

sleep(1)

stopThreads = False

# define pins
pinRBNum = 7
pinRFNum = 6
pinLBNum = 5
pinLFNum = 4

pinServoNum = 2
pinFloodLightsNum = 3
pinHeadLightsNum = 8
pinBrakeLightsNum = 10
pinHonkNum = 9
pinObstacleSensorBackNum = 11
pinObstacleSensorFrontNum = 12

pinManager = pinManager.PinManager(board)

pinLeftBack = pinManager.add_digital_pin_output(pinLBNum)
pinLeftForward = pinManager.add_digital_pin_output(pinLFNum)
pinRightBack = pinManager.add_digital_pin_output(pinRBNum)
pinRightForward = pinManager.add_digital_pin_output(pinRFNum)

pinServo = pinManager.add_digital_pin_servo(pinServoNum)
pinFloodLights = pinManager.add_digital_pin_output(pinFloodLightsNum)
pinHeadLights = pinManager.add_digital_pin_output(pinHeadLightsNum)
pinBrakeLights = pinManager.add_digital_pin_output(pinBrakeLightsNum)
pinHonk = pinManager.add_digital_pin_output(pinHonkNum)
pinObstacleSensorFront = pinManager.add_digital_pin_input(pinObstacleSensorFrontNum)
pinObstacleSensorBack = pinManager.add_digital_pin_input(pinObstacleSensorBackNum)
print(pinObstacleSensorBack)
# procedure for what to do when certain keys are pressed
def on_press(key):    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
        
    
     
    global car
    if type(key) == KeyCode:
        buttonPressed = key.char
        
        # set which button is currently pressed
        car.set_current_keys_pressed(buttonPressed, "pressed")
        
        car.drive(buttonPressed, "pressed")
        car.turn_on_or_off_light(buttonPressed)
        car.honk(buttonPressed, "pressed")
        
    elif type(key) == Key:
        car.move_servo(key)

#procedure for what do when releasing buttons
def on_release(key):
    global car

    if type(key) == KeyCode:
        buttonReleased = key.char
        car.set_current_keys_pressed(buttonReleased, "released")
        car.drive(key, "released")
        car.honk(buttonReleased, "released")
        
    elif type(key) == Key:
        pass
   
# procedure for key listening
def get_keys():
    global stopThreads

    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join() 
        stopThreads = True
        
def start_gui():
    master = Tk()

    tempPinNum = 0
    noisePinNum = 5
    lightFrontPinNum = 1
    lightBackPinNum = 2
    
    tempPin = pinManager.add_analog_pin_input(tempPinNum)
    noisePin = pinManager.add_analog_pin_input(noisePinNum)
    lightFrontPin = pinManager.add_analog_pin_input(lightFrontPinNum)
    lightBackPin = pinManager.add_analog_pin_input(lightBackPinNum)
    
    myGUI = sensorGUI.SensorGUI(master, tempPin, noisePin, lightFrontPin, lightBackPin)
    master.mainloop()
    

# explanatory text
print("You can start steering now")
print("'w' for forward, 's' for backward, 'a' for left, 'd' for right")

#initialize car class
car = controllableCar.controllableCar(pinLeftBack, pinLeftForward, pinRightBack, pinRightForward)

# add components to car class
car.add_servo(pinServo)
car.add_on_off_lights(pinFloodLights, "f")
car.add_on_off_lights(pinHeadLights, "l")

# add brake lights to car
car.add_brake_lights(pinBrakeLights)

# add honking to car
car.add_honk(pinHonk, "h")

car.add_reverse_sound(pinHonk)

# light up headlights
car.toggle_on_light("l")

# add obstacle sensors
car.add_obstacle_sensor(pinObstacleSensorFront, "front")
car.add_obstacle_sensor(pinObstacleSensorBack, "back")

# start main loop
<<<<<<< HEAD
thread1 = Thread(target = get_keys)
thread1.start()

thread2 = Thread(target = start_gui)
thread2.start()
=======
get_keys() 
>>>>>>> 5003c49a5a85a6436af8c6a35baba7f608f3d91e

print("Exiting program")

