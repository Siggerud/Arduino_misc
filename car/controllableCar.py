from pyfirmata2 import Arduino, util
from pynput.keyboard import Key
from time import sleep, time

class controllableCar:
    def __init__(self, pinLeftReverse, pinLeftForward, pinRightReverse, pinRightForward, driveCommand="w", reverseCommand="s", leftCommand="a", rightCommand="d"):
        
        # driving pins
        self._pinLeftReverse = pinLeftReverse
        self._pinLeftForward = pinLeftForward
        self._pinRightReverse = pinRightReverse
        self._pinRightForward = pinRightForward
        
        # driving commands
        self._driveCommand = driveCommand
        self._reverseCommand = reverseCommand
        self._leftCommand = leftCommand
        self._rightCommand = rightCommand
        
        self._currentKeysPressed = {self._driveCommand: 0, self._reverseCommand: 0, self._leftCommand: 0, self._rightCommand: 0}
        self._onOffLightCommandsAndPins = {}
        self._servoSet = False
        self._lightsSet = False
        self._honkSet = False
        self._brakeLightsSet = False
        self._reverseSoundSet = False 
        self._startTime = time()
        self._timerRunning = False
        self._reverseSoundOn = False
        
        # obstacle sensor pins
        self._frontObstacleSensorPin = None
        self._backObstacleSensorPin = None
        self._leftObstacleSensorPin = None
        self._rightObstacleSensorPin = None
        
        self._frontObstacleSensorSet = False
        self._backObstacleSensorSet = False
        self._leftObstacleSensorSet = False
        self._rightObstacleSensorSet = False
        
    def _print_test_text(self, component):
        print(f"Testing {component}...\n")
        
    def _turn_on_and_off_for_test(self, pin, numOfTimes, sleepTime):
        for i in range(numOfTimes):
            pin.write(1)
            sleep(sleepTime)
            pin.write(0)
            sleep(sleepTime)
        
    def _test_lights(self, pin, component):
        self._print_test_text(component)
        self._turn_on_and_off_for_test(pin, 8, 0.15)
            
    def _test_servo(self):
        self._print_test_text("servo")
        self._pinServo.write(self._minServoAngle)
        sleep(0.75)
        self._pinServo.write(self._maxServoAngle)
        sleep(0.75)
        self._pinServo.write(self._defaultServoAngle)
        sleep(0.75)
        
    def _test_honk(self, text):
        self._print_test_text("honk")
        self._turn_on_and_off_for_test(self._honkPin, 5, 0.2)
        
    def _test_obstacle_sensor(self, side):
        self._print_test_text(f"{side} obstacle sensor")
        if side == "front":
            sensor = self._frontObstacleSensorPin
        elif side == "back":
            sensor = self._backObstacleSensorPin
        elif side == "left":
            sensor = self._leftObstacleSensorPin
        elif side == "right":
            sensor = self._rightObstacleSensorPin
            
        if not sensor.read():
            print(f"{side.capitalize()} sensor failed to read values...")
        else:
            print(f"{side.capitalize()} sensor reading was succesful!")
        print("\n")
              
    def test_car_functions(self):
        # testing all lights except brake lights
        if self._lightsSet:
            for index, value in enumerate(self._onOffLightCommandsAndPins.values()):
                pin = value[0]
                self._test_lights(pin, f"light #{index + 1}")
        
        # testing brake lights
        if self._brakeLightsSet:
            self._test_lights(self._brakeLightPin, "brake lights")
        
        # testing servo
        if self._servoSet:
            self._test_servo()
        
        # testing honking
        if self._honkSet:
            self._test_honk("Testing honk")
        
        # testing all obstacle sensors
        if self._frontObstacleSensorSet:
            self._test_obstacle_sensor("front")
                
        if self._backObstacleSensorSet:
            self._test_obstacle_sensor("back")
            
        if self._leftObstacleSensorSet:
            self._test_obstacle_sensor("left")
            
        if self._rightObstacleSensorSet:
            self._test_obstacle_sensor("right")
                   
    def add_obstacle_sensor(self, pin, side):
        if side == "front":
            self._frontObstacleSensorPin = pin
            self._frontObstacleSensorSet = True
        elif side == "back":
            self._backObstacleSensorPin = pin
            self._backObstacleSensorSet = True
        elif side == "left":
            self._leftObstacleSensorPin = pin
            self._leftObstacleSensorSet = True
        elif side == "right":
            self._rightObstacleSensorPin = pin
            self._rightObstacleSensorSet = True
        else:
            raise SideNotFoundError 
        
    def add_brake_lights(self, pin):
        self._brakeLightPin = pin
        self._brakeLightsSet = True
        
    def add_on_off_lights(self, pin, commandKey):
        self._onOffLightCommandsAndPins[commandKey] = [pin, False] # set pin attached to command and an initial value of False on light
        self._lightsSet = True
        
    def toggle_on_light(self, commandKey):
        if self._lightsSet == False:
            raise ComponentNotSetError
    
        if commandKey in self._onOffLightCommandsAndPins.keys():
            self._onOffLightCommandsAndPins[commandKey][0].write(1)
            self._onOffLightCommandsAndPins[commandKey][1] = True
            
    def toggle_off_light(self, commandKey):
        if self._lightsSet == False:
            raise ComponentNotSetError
            
        if commandKey in self._onOffLightCommandsAndPins.keys():
            self._onOffLightCommandsAndPins[commandKey][0].write(0)
            self._onOffLightCommandsAndPins[commandKey][1] = False          
        
    def turn_on_or_off_light(self, commandKey):
        if commandKey in self._onOffLightCommandsAndPins.keys():
            if self._onOffLightCommandsAndPins[commandKey][1] == False:
                self.toggle_on_light(commandKey)
            else:
                self.toggle_off_light(commandKey)
                
    def add_honk(self, pin, commandKey):
        self._honkPin = pin
        self._honkCommandKey = commandKey
        self._honkSet = True
        
    def honk(self, key, action):
        if self._honkSet == False:
            raise ComponentNotSetError
            
        if key == self._honkCommandKey:
            if action == "released":
                self._honkPin.write(0)
            elif action == "pressed":
                self._honkPin.write(1)
                
    def add_reverse_sound(self, pin):
        self._reverseSoundPin = pin
        self._reverseSoundSet = True
        
    def _make_reverse_sound(self):
        if self._timerRunning == False:
            self._startTime = time()
            self._timerRunning = True
            
        end = time()
        timeDelta = int((end - self._startTime) * 1000) # time elapsed in miliseconds
        if timeDelta > 300:
            # switch state of sound every 300 miliseconds
            if self._reverseSoundOn == False:
                self._reverseSoundPin.write(1)
                self._reverseSoundOn = True
            else:
                self._reverseSoundPin.write(0)
                self._reverseSoundOn = False
            self._startTime = time()
    
    def _stop_reverse_sound(self):  
        self._timerRunning = False
        self._reverseSoundPin.write(0)
        self._reverseSoundOn = False
        
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
        self._servoSet = True
        
        # set initial angle
        self._pinServo.write(self._currentServoAngle)
        
    def move_servo(self, key):
        if self._servoSet == False:
            raise ComponentNotSetError
    
        if key == self._moveServoLeftKey or key == self._moveServoRightKey or key == self._moveToDefaultAngleKey:
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
    
    def _too_close(self, pin):
        pinValue = pin.read()
        
        return not pinValue
        
    # drives according to user input, stops if car is too close too obstacle       
    def drive(self, key, action):
        if action == "pressed":
            if key == self._driveCommand:
                if self._frontObstacleSensorSet:
                    if self._too_close(self._frontObstacleSensorPin):
                        self._stop()
                        return
                        
                    self._advance()
            elif key == self._reverseCommand:
                if self._backObstacleSensorSet:
                    if self._too_close(self._backObstacleSensorPin):
                        self._stop()
                        return
                    
                    self._back()
  
                    if self._brakeLightsSet:
                        self._brakeLightPin.write(1)
                        
                    if self._reverseSoundSet:
                        self._make_reverse_sound()
                
            elif key == self._leftCommand:
                if self._leftObstacleSensorSet:
                    if self._too_close(self._leftObstacleSensorPin):
                        self._stop()
                        return
            
                if self._currentKeysPressed[self._leftCommand] == 1:
                    self._turn_left_while_forward()
                elif self._currentKeysPressed[self._rightCommand] == 1:
                    self._turn_left_while_backward()
                else:
                    self._turn_left()
                    
            elif key == self._rightCommand:
                if self._rightObstacleSensorSet:
                    if self._too_close(self._rightObstacleSensorPin):
                        self._stop()
                        return
                
                if self._currentKeysPressed[self._driveCommand] == 1:
                    self._turn_right_while_forward()
                elif self._currentKeysPressed[self._reverseCommand] == 1:
                    self._turn_right_while_backward()
                else:
                    self._turn_right()
                    
        elif action == "released":
            self._stop()
            
            if self._brakeLightsSet:
                self._brakeLightPin.write(0)
                
            if self._reverseSoundSet:
                self._stop_reverse_sound()
    
    def _advance(self):
        directionSpeeds = [0, 1, 0, 1]
        self._move(directionSpeeds)
    
    def _back(self):
        directionSpeeds = [1, 0, 1, 0]
        self._move(directionSpeeds)
        
    def _stop(self):
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
        
    # keeps track of which keys are pressed
    def set_current_keys_pressed(self, key, action):
        if key in self._currentKeysPressed.keys():
            if action == "released":
                value = 0
            elif action == "pressed":
                value = 1
            self._currentKeysPressed[key] = value
        
        
        
        
class ComponentNotSetError(Exception):
    pass
    
class SideNotFoundError(Exception):
    pass