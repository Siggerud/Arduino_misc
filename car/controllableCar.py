from pyfirmata2 import Arduino, util
from pynput.keyboard import Key
from time import sleep, time
import pygame

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
        
    def set_joystick(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        self.myJoystick = joysticks[0]
        
        pygame.init()
        
    def controller_input(self, event):
        if event.type == pygame.JOYHATMOTION:
            print(event)
            horizontal, vertical = self.myJoystick.get_hat(0)
            if horizontal == 0 and vertical == 1:
                self._advance()
            elif horizontal == 0 and vertical == -1:
                self._back()
            elif horizontal == -1 and vertical == 0:
                self._turn_left()
            elif horizontal == 1 and vertical == 0:
                self._turn_right()
            elif horizontal == -1 and vertical == 1:
                self._turn_left_while_forward()
            elif horizontal == -1 and vertical == -1:
                self._turn_left_while_backward()
            elif horizontal == 1 and vertical == 1:
                self._turn_right_while_forward()
            elif horizontal == 1 and vertical == -1:
                self._turn_right_while_backward()
            else:
                self._stop()
        
    def drive_from_controller(self, key, action):
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