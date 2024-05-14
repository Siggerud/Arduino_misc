import pygame
import time



pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

myJoystick = joysticks[0]

start = time.time()
pygame.init()
while True:
    if time.time() - start > 30:
        break
        
        
    for event in pygame.event.get():
        """
        if event.type == pygame.JOYBUTTONDOWN:
            if myJoystick.get_button(0):
                print("A")
            elif myJoystick.get_button(1):
                print("X") 
            elif myJoystick.get_button(2):
                print("B")
            elif myJoystick.get_button(3):
                print("Y")
        elif event.type == pygame.JOYHATMOTION:
            horizontal, vertical = myJoystick.get_hat(0)
            if horizontal == -1:
                print("left")
            elif horizontal == 1:
                print("right")
            if vertical == -1:
                print("down")
            elif vertical == 1:
                print("up")
            """
        print(event)