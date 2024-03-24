from pynput.keyboard import Key, Listener
from time import sleep
from serial import Serial

port = "COM6" # arduino Port
SerialObj = Serial(port, 9600)

sleep(1) # wait a short while
print("hello")
def on_press(key):
    #keys need to be converted to strin
    if str(key) == "'g'":
        print("Chose green")
        SerialObj.write(b'green')  
        print(SerialObj.readline())
    elif str(key) == "'r'":
        print("Chose red")
        SerialObj.write(b'red')
        print(SerialObj.readline())
       
    if key == Key.delete:
        return False
    
    
def on_release(key):
    #keys need to be converted to strings
    pass
    #if str(key) == "'g'" or str(key) == "'r'":
    #    print("stop")
    #    SerialObj.write(b'stop')
		
with Listener(on_press = on_press, on_release=on_release) as listener:
    listener.join()