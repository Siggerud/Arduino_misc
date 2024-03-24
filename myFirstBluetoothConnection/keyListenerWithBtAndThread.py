from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
import time
from threading import Thread
import os

board = Arduino("COM7")

it = util.Iterator(board)
it.start()

greenPinNum = 4
bluePinNum = 5
yellowPinNum = 6

prevState = ""
greenPrintNotExecuted = True

pinGreen = board.get_pin(f"d:{greenPinNum}:o")
pinBlue = board.get_pin(f"d:{bluePinNum}:o")
pinYellow = board.get_pin(f"d:{yellowPinNum}:o")

time.sleep(1)

endOfTime = False

def on_press(key):
    global prevState
    if key.char == "y":
        pinYellow.write(1)
        pinBlue.write(0)
        if prevState != "Yellow": 
            print("Yellow pin lit")
        
        prevState = "Yellow"
    elif key.char == "b":
        pinYellow.write(0)
        pinBlue.write(1)
        if prevState != "Blue":
            print("Blue pin lit")
        
        prevState = "Blue"

def on_release(key):
    global prevState
    pinYellow.write(0)
    pinBlue.write(0)
    
    if prevState != "Released":
        pinReleased = prevState.lower()
        print(f"Released {pinReleased} pin")
    
    prevState = "Released"
   

def get_keys():
        with Listener(on_press=on_press, on_release = on_release) as listener:
            def time_out(period_sec: int):
                time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
                listener.stop()

            Thread(target=time_out, args=(15.0,)).start()
            listener.join()
        
thread1 = Thread(target = get_keys)
thread1.start()

start = time.time()
while True:
    pinGreen.write(1)
    if greenPrintNotExecuted:
        print("Green pin lit")
        greenPrintNotExecuted = False
    
    end = time.time()
    
    if end - start > 15:
        print("Exiting program")
        exit(1)
        
    
    
       
 
    
        