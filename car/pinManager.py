from pyfirmata2 import Arduino

class PinManager:
    def __init__(self, board):
        self._board = board
    
    def add_digital_pin_input(self, pinNumber):
        return self._add_pin("d", pinNumber, "i")
        
    def add_digital_pin_output(self, pinNumber):
        return self._add_pin("d", pinNumber, "o")
        
    def add_digital_pin_servo(self, pinNumber):
        return self._add_pin("d", pinNumber, "s")
        
    def add_analog_pin_input(self, pinNumber):
        return self._add_pin("a", pinNumber, "i")
        
    def _add_pin(self, firstLetter, pinNumber, secondLetter):
        return self._board.get_pin(f"{firstLetter}:{pinNumber}:{secondLetter}")