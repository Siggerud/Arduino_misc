from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, Listener, KeyCode
from time import sleep
import controllableCar
print("i")
# define board
board = Arduino("COM5")
print("j")
it = util.Iterator(board)
it.start()

sleep(1)

#const int microphonePin = A0;
microphonePinNum = 2

microphonePin = board.get_pin("d:2:i")

for i in range(100):
    print(microphonePin.read())