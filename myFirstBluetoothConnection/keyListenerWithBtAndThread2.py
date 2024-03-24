from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
import time
from threading import Thread

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

# define pin numbers
greenPinNum = 4
bluePinNum = 5
yellowPinNum = 6

prevState = ""
greenPrintNotExecuted = True 
stopThreads = False

# define pins
pinGreen = board.get_pin(f"d:{greenPinNum}:o")
pinBlue = board.get_pin(f"d:{bluePinNum}:o")
pinYellow = board.get_pin(f"d:{yellowPinNum}:o")

time.sleep(1)

# procedure for what to do when certain keys are presses
def on_press(key):
    global prevState
    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
    
    # light up yellow LED when "y" is pressed
    if key.char == "y":
        pinYellow.write(1)
        pinBlue.write(0)
        if prevState != "Yellow": 
            print("Yellow pin lit")
        
        prevState = "Yellow"
        
    # light up blue LED when "b" is pressed
    elif key.char == "b":
        pinYellow.write(0)
        pinBlue.write(1)
        if prevState != "Blue":
            print("Blue pin lit")
        
        prevState = "Blue"

# procedure for what to do when certain keys are released
def on_release(key):
    global prevState
    
    # turn off leds
    pinYellow.write(0)
    pinBlue.write(0)
    
    # print which LED is no longer shining
    if prevState != "Released":
        pinReleased = prevState.lower()
        print(f"Released {pinReleased} pin")
    
    prevState = "Released"
   
# procedure for key listening
def get_keys():
        global stopThreads
        with Listener(on_press=on_press, on_release = on_release) as listener:
            listener.join()
            
            # exit all threads when program is no longer key listening
            stopThreads = True

# procedure for lighting green LED
def lightGreenLed():
    global greenPrintNotExecuted
    global stopThreads
    
    while True:
        if stopThreads:
            return False
           
        pinGreen.write(1)
        
        # print that LED is shining one time
        if greenPrintNotExecuted:
            print("Green pin lit")
            greenPrintNotExecuted = False
            

# define and start threads  
thread1 = Thread(target = get_keys)
thread1.start()

thread2 = Thread(target = lightGreenLed)
thread2.start()

        
    
    
       
 
    
        