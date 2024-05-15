from pyfirmata2 import Arduino, util
from pynput.keyboard import Key, KeyCode, Listener
from time import sleep, time
import pygame

class controllableCar:
    def __init__(self, controllerType):
        
        self._controllerType = controllerType
        
        self._onOffLightCommandsAndPins = {}
        self._drivingEnabled = False
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
        
        #commands
        self._drivingCommands = ["drive", "reverse", "left", "right", "left forward", "left reverse", "right forward", "right reverse", "stop"]
        self._moveServoCommands = ["move servo left", "move servo right", "move servo to default"]   
        self._honkCommands = ["start honk", "stop honk"]
         
        self._numOfLights = 0
        
        if controllerType == "keyboard":
            
            self._advanceKey = "w"
            self._reverseKey = "s"
            self._leftKey = "a"
            self._rightKey = "d"
            
            self._currentKeysPressed = {self._advanceKey: 0, self._reverseKey: 0, self._leftKey: 0, self._rightKey: 0}
            
            self._moveServoKeys = [Key.left, Key.right, Key.up]
            self._moveServoLeftKey, self._moveServoRightKey, self._moveToDefaultAngleKey = self._moveServoKeys
            
            self._honkKey = "h"
            
            self._lightKeys = ["j", "k", "l"]
            
            self._exitKey = Key.delete
            
        elif controllerType == "xbox":
            self._lightButtons = [0, 1, 3]
        
        self._turnOnLightCommands = []
        self._turnOffLightCommands = []
        for i in range(3):
            self._turnOnLightCommands.append(f"turn on light {i}")
            self._turnOffLightCommands.append(f"turn off light {i}")
            
        
    def enable_driving(self, pinLeftReverse, pinLeftForward, pinRightReverse, pinRightForward):
        # driving pins
        self._pinLeftReverse = pinLeftReverse
        self._pinLeftForward = pinLeftForward
        self._pinRightReverse = pinRightReverse
        self._pinRightForward = pinRightForward
        
        self._drivingEnabled = True    
        
    def start_listening(self):
        if self._controllerType == "keyboard":
            with Listener(on_press=self._on_press, on_release = self._on_release) as listener:
                listener.join() 
                
        elif self._controllerType == "xbox":
            self._set_joystick()
            
            pygame.init()
            while True:
                for event in pygame.event.get():
                    command = self._convert_xbox_input_to_command(event)
                    if command == "exit program":
                        return
                    
                    self._execute_car_command(command)
                            
    def _execute_car_command(self, command):
        if self._drivingEnabled:
            if command in self._drivingCommands:
                self._drive(command)
                
        if self._honkSet:
            if command in self._honkCommands:
                self._honk(command)
                
        if self._servoSet:
            if command in self._moveServoCommands:
                self._move_servo(command)
                
        if self._lightsSet:
            if command in self._turnOnLightCommands:
                self._toggle_on_light(command)
            elif command in self._turnOffLightCommands:
                self._toggle_off_light(command)
    
    # TODO: check if it works in start_listening    
    def _set_joystick(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self._myJoystick = joysticks[0]
    
    def _convert_xbox_input_to_command(self, event):
        command = ""
        
        eventType = event.type
        if eventType == pygame.JOYHATMOTION:
            horizontal, vertical = self._myJoystick.get_hat(0)
            if horizontal == 0 and vertical == 0:
                command = "stop"
            elif horizontal == -1 and vertical == 1:
                command = "left forward"
            elif horizontal == -1 and vertical == -1:
                command = "left reverse"
            elif horizontal == 1 and vertical == 1:
                command = "right forward"
            elif horizontal == 1 and vertical == -1:
                command = "right reverse"
            elif horizontal == -1:
                command = "left"
            elif horizontal == 1:
                command = "right"
            elif vertical == -1:
                command = "reverse"
            elif vertical == 1:
                command = "drive"
        
        elif eventType == pygame.JOYAXISMOTION:
            treshold = 0.9
            valueLeftRight = self._myJoystick.get_axis(2)
            if valueLeftRight < -1 * treshold:
                command = "move servo left"
            elif valueLeftRight > treshold:
                command = "move servo right"
                
            valueUpDown = self._myJoystick.get_axis(3)
            if valueUpDown >= treshold:
                command = "move servo to default"
                
        elif eventType == pygame.JOYBUTTONDOWN:
            buttonPressed = event.button
            if buttonPressed == 2:
                command = "start honk"
            elif buttonPressed == 5:
                command = "exit program"
            elif buttonPressed in list(self._onOffLightCommandsAndPins.keys()):
                if buttonPressed == 0:
                    index = 0
                elif buttonPressed == 1:
                    index = 1
                elif buttonPressed == 3:
                    index = 2
                
                if self._onOffLightCommandsAndPins[index][1] == False:
                    command = f"turn on light {index}"
                elif self._onOffLightCommandsAndPins[index][1]:
                    command = f"turn off light {index}"
            
        elif eventType == pygame.JOYBUTTONUP:
            buttonReleased = event.button
            if buttonReleased == 2:
                command = "stop honk"
        
        return command
        
    def _convert_keyboard_input_to_command(self, key, action):
        command = ""
    
        if type(key) == KeyCode:
            button = key.char
            
            if button in list(self._currentKeysPressed.keys()):
                self._set_current_keys_pressed(button, action)
                
                if self._currentKeysPressed[self._advanceKey] == 1 and self._currentKeysPressed[self._leftKey] == 1:
                    command = "left forward"
                elif self._currentKeysPressed[self._reverseKey] == 1 and self._currentKeysPressed[self._leftKey] == 1:
                    command = "left reverse"
                elif self._currentKeysPressed[self._advanceKey] == 1 and self._currentKeysPressed[self._rightKey] == 1:
                    command = "right forward"
                elif self._currentKeysPressed[self._reverseKey] == 1 and self._currentKeysPressed[self._rightKey] == 1:
                    command = "right reverse"       
                elif self._currentKeysPressed[self._advanceKey] == 1:
                    command = "drive"
                elif self._currentKeysPressed[self._reverseKey] == 1:
                    command = "reverse"
                elif self._currentKeysPressed[self._leftKey] == 1:
                    command = "left"
                elif self._currentKeysPressed[self._rightKey] == 1:
                    command = "right"
                elif 1 not in list(self._currentKeysPressed.values()):
                    command = "stop"
                    
            elif button == self._honkKey:
                if action == "pressed":
                    command = "start honk"
                elif action == "released":
                    command = "stop honk"
                    
            elif button in self._lightKeys:
                if action == "pressed":
                    index = self._lightKeys.index(button)
                    if index in list(self._onOffLightCommandsAndPins.keys()):
                        if self._onOffLightCommandsAndPins[index][1] == False:
                            command = f"turn on light {index}"
                        elif self._onOffLightCommandsAndPins[index][1]:
                            command = f"turn off light {index}"
                    
        elif type(key) == Key:
            if key in self._moveServoKeys:
                if key == self._moveServoLeftKey:
                    command = "move servo left"
                elif key == self._moveServoRightKey:
                    command = "move servo right"
                elif key == self._moveToDefaultAngleKey:
                    command = "move servo to default"
            elif key == self._exitKey:
                command = "exit program"
                   
        return command
 
            
    # procedure for what to do when certain keys are pressed
    def _on_press(self, key):              
        command = self._convert_keyboard_input_to_command(key, "pressed")
        if command == "exit program":
            return False
        
        self._execute_car_command(command)

    #procedure for what do when releasing buttons
    def _on_release(self, key):
        command = self._convert_keyboard_input_to_command(key, "released")
        
        self._execute_car_command(command)    
        
    def print_instructions_for_car(self):
        if self._controllerType == "keyboard":
            print("Keys and commands:")
            
            # gather all keys and commands in one dictionary
            userInputAndCommands = {self._advanceKey: "drive forward",
            self._reverseKey: "reverse",
            self._leftKey: "turn left",
            self._rightKey: "turn right"}
            
            if self._lightsSet:
                for command in list(self._onOffLightCommandsAndPins):
                    userInputAndCommands[command] = "light"
            
            if self._servoSet:
                userInputAndCommands[self._moveServoLeftKey] = "move servo left"
                userInputAndCommands[self._moveServoRightKey] = "move servo right"
                userInputAndCommands[self._moveToDefaultAngleKey] = "move servo to default angle"
                
            if self._honkSet:
                userInputAndCommands[self._honkKey] = "honk"
                
            userInputAndCommands[self._exitKey] = "exit program"
                
            
        elif self._controllerType == "xbox":
            print("Buttons and commands")
            
            userInputAndCommands = {"Pad up": "drive forward",
            "Pad down": "reverse",
            "Pad left": "turn left",
            "Pad right": "turn right",
            }
            
            if self._lightsSet:
                userInputAndCommands["A"] = "light"
                userInputAndCommands["B"] = "light"
                userInputAndCommands["Y"] = "light"
            
            if self._servoSet:
                userInputAndCommands["Left stick left"] = "move servo left"
                userInputAndCommands["Left stick right"] = "move servo right"
                userInputAndCommands["Left stick up"] = "move servo to default angle"
                
            if self._honkSet:
                userInputAndCommands["X"] = "honk"
                
            userInputAndCommands["RB"] = "exit program"
            
        
        for userInput, command in userInputAndCommands.items():
            print(f"{userInput}: {command}")
        print("\n")        
        print("You can start steering now\n")
            
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
        servoSleepTime = 0.75
        self._pinServo.write(self._minServoAngle)
        sleep(servoSleepTime)
        self._pinServo.write(self._maxServoAngle)
        sleep(servoSleepTime)
        self._pinServo.write(self._defaultServoAngle)
        sleep(servoSleepTime)
        
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
        
    def add_on_off_lights(self, pin):
        self._onOffLightCommandsAndPins[self._numOfLights] = [pin, False] # set pin attached to command and an initial value of False on light
        self._lightsSet = True
        self._numOfLights += 1
        
    def _toggle_on_light(self, command):
        index = int(command[-1])
        self._onOffLightCommandsAndPins[index][0].write(1)
        self._onOffLightCommandsAndPins[index][1] = True
            
    def _toggle_off_light(self, command):
        index = int(command[-1])
        self._onOffLightCommandsAndPins[index][0].write(0)
        self._onOffLightCommandsAndPins[index][1] = False                 
                
    def add_honk(self, pin):
        self._honkPin = pin
        self._honkSet = True
        
    def _honk(self, command):
        if command == "start honk":
            self._honkPin.write(1)
        elif command == "stop honk":
            self._honkPin.write(0)
                
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
        
    def add_servo(self, pinServo, increment=5, defaultServoAngle=90, minAngle=0, maxAngle=179):
        self._pinServo = pinServo
        self._servoIncrement = increment
        self._minServoAngle = minAngle
        self._maxServoAngle = maxAngle
        self._defaultServoAngle = defaultServoAngle
        self._currentServoAngle = defaultServoAngle
        self._servoSet = True
        
        # set initial angle
        self._pinServo.write(self._currentServoAngle)
        
    def _move_servo(self, command):   
        moveServo = False
        if command == "move servo left":
            if self._currentServoAngle >= self._minServoAngle + self._servoIncrement:
                angle = self._currentServoAngle - self._servoIncrement
                moveServo = True
            elif self._currentServoAngle > self._minServoAngle:
                angle = self._currentServoAngle - 1
                moveServo = True
        elif command == "move servo right":
            if self._currentServoAngle <= self._maxServoAngle - self._servoIncrement:
                angle = self._currentServoAngle + self._servoIncrement
                moveServo = True
            elif self._currentServoAngle < self._maxServoAngle:
                angle = self._currentServoAngle + 1
                moveServo = True
        elif command == "move servo to default":
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
    def _drive(self, command):
        if command == "drive":
            if self._frontObstacleSensorSet:
                if self._too_close(self._frontObstacleSensorPin):
                    self._stop()
                    return
                    
            self._advance()
        elif command == "reverse":
            if self._backObstacleSensorSet:
                if self._too_close(self._backObstacleSensorPin):
                    self._stop()
                    return
                
            self._back()

            if self._brakeLightsSet:
                self._brakeLightPin.write(1)
                
            if self._reverseSoundSet:
                self._make_reverse_sound()
            
        elif command == "left":
            if self._leftObstacleSensorSet:
                if self._too_close(self._leftObstacleSensorPin):
                    self._stop()
                    return
                
            self._turn_left()
        
        elif command == "left forward":
            if self._leftObstacleSensorSet:
                if self._too_close(self._leftObstacleSensorPin):
                    self._stop()
                    return
        
            self._turn_left_while_forward()
        elif command == "left reverse":
            if self._leftObstacleSensorSet:
                if self._too_close(self._leftObstacleSensorPin):
                    self._stop()
                    return
                    
            self._turn_left_while_backward()
                
        elif command == "right":
            if self._rightObstacleSensorSet:
                if self._too_close(self._rightObstacleSensorPin):
                    self._stop()
                    return
                    
            self._turn_right()
            
        elif command == "right forward":
            if self._rightObstacleSensorSet:
                if self._too_close(self._rightObstacleSensorPin):
                    self._stop()
                    return
            
            self._turn_right_while_forward()
        elif command == "right reverse":
            if self._rightObstacleSensorSet:
                if self._too_close(self._rightObstacleSensorPin):
                    self._stop()
                    return
        
            self._turn_right_while_backward()
        
        elif command == "stop":       
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
    def _set_current_keys_pressed(self, key, action):
        if action == "released":
            value = 0
        elif action == "pressed":
            value = 1
        self._currentKeysPressed[key] = value
        
# TODO: finn ut hvorfor sensorene ikke fungerer like bra på xbox controller
            



        
