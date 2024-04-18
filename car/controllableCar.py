from pyfirmata2 import Arduino, util
from pynput.keyboard import Key
from time import sleep

class controllableCar:
    def __init__(self, pinLeftReverse, pinLeftForward, pinRightReverse, pinRightForward, driveCommand="w", reverseCommand="s", leftCommand="a", rightCommand="d"):
        self._pinLeftReverse = pinLeftReverse
        self._pinLeftForward = pinLeftForward
        self._pinRightReverse = pinRightReverse
        self._pinRightForward = pinRightForward
        self._driveCommand = driveCommand
        self._reverseCommand = reverseCommand
        self._leftCommand = leftCommand
        self._rightCommand = rightCommand
        self._currentButtonsPressed = {self._driveCommand: 0, self._reverseCommand: 0, self._leftCommand: 0, self._rightCommand: 0}
        self._onOffLightCommandsAndPins = {}
        
    def add_on_off_lights(self, pin, commandKey):
        self._onOffLightCommandsAndPins[commandKey] = [pin, False] # set pin attached to command and an initial value of False on light
        
    def turn_on_or_off_light(self, commandKey):
        if commandKey in self._onOffLightCommandsAndPins.keys():
            if self._onOffLightCommandsAndPins[commandKey][1] == False:
                self._onOffLightCommandsAndPins[commandKey][0].write(1)
                self._onOffLightCommandsAndPins[commandKey][1] = True
            else:
                self._onOffLightCommandsAndPins[commandKey][0].write(0)
                self._onOffLightCommandsAndPins[commandKey][1] = False
        
    def add_servo(self, pinServo, moveLeftKey=Key.left, moveRightKey=Key.right, moveToDefaultAngleKey=Key.up, increment=5, defaultServoAngle=90, minAngle=0, maxAngle=179):
        self._pinServo = pinServo
        self._moveServoLeftKey = moveLeftKey
        self._moveServoRightKey = moveRightKey
        self._moveToDefaultAngleKey = moveToDefaultAngleKey
        self._servoIncrement = increment
        self._minServoAngle = minAngle
        self._maxServoAngle = maxAngle
        self._defaultServoAngle = defaultServoAngle
        self._currentServoAngle = defaultServoAngle
        
        # set initial angle
        self._pinServo.write(self._currentServoAngle)
        
    def move_servo(self, key):
        if key != self._moveServoLeftKey and key != self._moveServoRightKey and key != self._moveToDefaultAngleKey:
            return

        moveServo = False   
        if key == self._moveServoLeftKey:
            if self._currentServoAngle >= self._minServoAngle + self._servoIncrement:
                angle = self._currentServoAngle - self._servoIncrement
                moveServo = True
            elif self._currentServoAngle > self._minServoAngle:
                angle = self._currentServoAngle - 1
                moveServo = True              
        elif key == self._moveServoRightKey:
            if self._currentServoAngle <= self._maxServoAngle - self._servoIncrement:
                angle = self._currentServoAngle + self._servoIncrement
                moveServo = True
            elif self._currentServoAngle < self._maxServoAngle:
                angle = self._currentServoAngle + 1
                moveServo = True
        elif key == self._moveToDefaultAngleKey:
            angle = self._defaultServoAngle
            moveServo = True
                
        if moveServo:
            self._pinServo.write(angle)
            self._currentServoAngle = angle
            sleep(0.005)
        
    # drives according to user input, stops if car is too close too obstacle       
    def drive(self, button):
        if button == self._driveCommand:
            self._advance()
        elif button == self._reverseCommand:
            self._back()
        elif button == self._leftCommand:
            if self._currentButtonsPressed[self._leftCommand] == 1:
                self._turn_left_while_forward()
            elif self._currentButtonsPressed[self._rightCommand] == 1:
                self._turn_left_while_backward()
            else:
                self._turn_left()
        elif button == self._rightCommand:
            if self._currentButtonsPressed[self._driveCommand] == 1:
                self._turn_right_while_forward()
            elif self._currentButtonsPressed[self._reverseCommand] == 1:
                self._turn_right_while_backward()
            else:
                self._turn_right()
    
    def _advance(self):
        directionSpeeds = [0, 1, 0, 1]
        self._move(directionSpeeds)
    
    def _back(self):
        directionSpeeds = [1, 0, 1, 0]
        self._move(directionSpeeds)
        
    def stop(self):
        directionSpeeds = [1, 1, 1, 1]
        self._move(directionSpeeds)
       
    def _turn_right(self):
        directionSpeeds = [1, 0, 0, 1]
        self._move(directionSpeeds)

    def _turn_left(self):
        directionSpeeds = [0, 1, 1, 0]
        self._move(directionSpeeds)
        
    def _turn_left_while_forward(self):
        directionSpeeds = [0, 1, 1, 1]
        self._move(directionSpeeds)
        
    def _turn_right_while_forward(self):
        directionSpeeds = [1, 1, 0, 1]
        self._move(directionSpeeds)
        
    def _turn_left_while_backward(self):
        directionSpeeds = [1, 0, 1, 1]
        self._move(directionSpeeds)

    def _turn_right_while_backward(self):
        directionSpeeds = [1, 1, 1, 0]
        self._move(directionSpeeds)
        
    def _move(self, directionSpeeds):
        self._pinLeftReverse.write(directionSpeeds[2])
        self._pinLeftForward.write(directionSpeeds[3])
        self._pinRightReverse.write(directionSpeeds[0])
        self._pinRightForward.write(directionSpeeds[1])
        
    # keeps track of which buttons are pressed
    def set_current_buttons_pressed(self, button, action):
        if button in self._currentButtonsPressed.keys():
            if action == "released":
                value = 0
            elif action == "pressed":
                value = 1
            self._currentButtonsPressed[button] = value
        
        