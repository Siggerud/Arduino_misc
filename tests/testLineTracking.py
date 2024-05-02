
import time
from pyfirmata2 import Arduino, util

board = Arduino("COM4")

it = util.Iterator(board)
it.start()

time.sleep(1)

sensorPin = board.get_pin("d:7:i")
greenLedPin = board.get_pin("d:4:o")
redLedPin = board.get_pin("d:3:o")

start = time.time()
while time.time() - start < 120:
    if sensorPin.read():
        greenLedPin.write(1)
        redLedPin.write(0)
        
    else:
        greenLedPin.write(0)
        redLedPin.write(1)

