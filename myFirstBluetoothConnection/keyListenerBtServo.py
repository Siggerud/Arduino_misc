from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener
import time
from threading import Thread

# define board
board = Arduino("COM7")

it = util.Iterator(board)
it.start()

stopThreads = False

# define pin numbers
yellowPinNum1 = 2
greenPinNum = 3
yellowPinNum2 = 4
servoPinNum = 9

# define pins
pinYellow1 = board.get_pin(f"d:{yellowPinNum1}:o")
pinGreen = board.get_pin(f"d:{greenPinNum}:o")
pinYellow2 = board.get_pin(f"d:{yellowPinNum2}:o")
pinServo = board.get_pin(f"d:{servoPinNum}:s")

time.sleep(1)

initialAngle = 90
print(f"Setting initial angle to {initialAngle} degrees")
pinServo.write(initialAngle)
currentAngle = initialAngle

# procedure for what to do when certain keys are presses
def on_release(key):
    global currentAngle
    
    # if delete is pressed, then exit thread
    if key == Key.delete:
        return False
    
    # light up yellow LED when "y" is pressed
    try:
        if key.char == "a":
            if currentAngle >= 10:
                tempAngle = currentAngle - 10
                pinServo.write(tempAngle)
                
                currentAngle = tempAngle
                print(f"Moved servo to angle {currentAngle}")
            else:
                print("Can't move servo further")
            
        # light up blue LED when "b" is pressed
        elif key.char == "d":
            if currentAngle <= 169:
                tempAngle = currentAngle + 10
                pinServo.write(tempAngle)
                
                currentAngle = tempAngle
                print(f"Moved servo to angle {currentAngle}")
            else:
                print("Can't move servo further")
    except:
        pass
   
# procedure for key listening
def get_keys():
        global stopThreads
        with Listener(on_press=on_release) as listener:
            print("Press 'a' to decrease angle and 'd' to decrease angle")
            listener.join()
            
            # exit all threads when program is no longer key listening
            stopThreads = True

# procedure for lighting Leds according to servo position
def lightLeds():
    global currentAngle
    global stopThreads
    
    while True:
        if stopThreads:
            return False
           
        if currentAngle == 90:
            pinGreen.write(1)
            pinYellow1.write(0)
            pinYellow2.write(0)
        elif currentAngle < 90:
            pinGreen.write(0)
            pinYellow1.write(1)
            pinYellow2.write(0)
        elif currentAngle > 90:
            pinGreen.write(0)
            pinYellow1.write(0)
            pinYellow2.write(1)
            

# define and start threads  
thread1 = Thread(target = get_keys)
thread1.start()

thread2 = Thread(target = lightLeds)
thread2.start()

        
    
    
       
 
    
        