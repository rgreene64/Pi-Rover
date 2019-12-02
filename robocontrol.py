import time
import pygame
from adafruit_crickit import crickit

motorL = crickit.dc_motor_1
motorR = crickit.dc_motor_2
servo1 = crickit.servo_1
servo2 = crickit.servo_2
servo3 = crickit.servo_3
servo4 = crickit.servo_4


servo1_position = 0
servo2_position = 0
servo3_position = 0
servo4_position = 0
servo_increment_step = 10

axisUpDown = 3
axisLeftRight = 1
buttonSpinLeft = 5
buttonSpinRight = 4
buttonTiltForward = 6
buttonTiltBack = 7
buttonTiltUp = 0
buttonTiltDown = 2
buttonClose = 8
buttonOpen = 9
interval = 0.1

global hadEvent
global forward
global backward
global turnLeft
global turnRight
global spinLeft
global spinRight
global tiltForward
global tiltBack
global tiltUp
global tiltDown
global closeGrip
global openGrip


hadEvent = True
forward = False
backward = False
turnLeft = False
turnRight = False
spinLeft = False
spinRight = False
tiltForward = False
tiltBack = False
tiltUp = False
tiltDown = False
closeGrip = False
openGrip = False

pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

def PygameHandler(events):
    global hadEvent
    global forward
    global backward
    global turnLeft
    global turnRight
    global spinLeft
    global spinRight
    global tiltForward
    global tiltBack
    global tiltUp
    global tiltDown
    global closeGrip
    global openGrip
    
    for event in events:
        if event.type == pygame.JOYBUTTONDOWN:
            hadEvent = True
            if joystick.get_button(buttonSpinLeft):
                spinLeft = True
                spinRight = False
            elif joystick.get_button(buttonSpinRight):
                spinLeft = False
                spinRight = True
            elif joystick.get_button(buttonTiltForward):
                tiltForward = True
                tiltBack = False
            elif joystick.get_button(buttonTiltBack):
                tiltForward = False
                tiltBack = True
            elif joystick.get_button(buttonTiltUp):
                tiltUp = True
                tiltDown = False
            elif joystick.get_button(buttonTiltDown):
                tiltUp = False
                tiltDown = True
            elif joystick.get_button(buttonOpen):
                openGrip = True
                closeGrip = False
            elif joystick.get_button(buttonClose):
                openGrip = False
                closeGrip = True
            else:
                spinLeft = False
                spinRight = False
                tiltForward = False
                tiltBack = False
                tiltUp = False
                tiltDown = False
                openGrip = False
                closeGrip = False

        elif event.type == pygame.JOYBUTTONUP:
            hadEvent = True
            if not joystick.get_button(buttonSpinLeft):
                spinLeft = False
                spinRight = False
            elif not joystick.get_button(buttonSpinRight):
                spinLeft = False
                spinRight = False
            elif not joystick.get_button(buttonTiltForward):
                tiltForward = False
                tiltBack = False
            elif not joystick.get_button(buttonTiltBack):
                tiltForward = False
                tiltBack = False
            elif not joystick.get_button(buttonTiltUp):
                tiltUp = False
                tiltDown = False
            elif not joystick.get_button(buttonTiltDown):
                tiltUp = False
                tiltDown = False
            elif not joystick.get_button(buttonOpen):
                openGrip = False
                closeGrip = False
            elif not joystick.get_button(buttonClose):
                openGrip = False
                closeGrip = False     
            else:
                print("do nothing")
                
        elif event.type == pygame.JOYAXISMOTION:
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            if upDown > 0.1:
                forward = True
                backward = False
            elif upDown < -0.1:
                forward = False
                backward = True
            else:
                forward = False
                backward = False
            if leftRight > 0.1:
                turnLeft = True
                turnRight = False
            elif leftRight < -0.1:
                turnLeft = False
                turnRight = True
            else:
                turnLeft = False
                turnRight = False              
try:
    while True:
        PygameHandler(pygame.event.get()) 
        if hadEvent:  
            hadEvent = False
            if turnLeft:
                motorR.throttle = 1
                motorL.throttle = -1
            elif turnRight:
                motorR.throttle = -1
                motorL.throttle = 1
            elif forward:
                motorR.throttle = 1
                motorL.throttle = 1
            elif backward:
                motorR.throttle = -1
                motorL.throttle = -1
            elif spinLeft:
                servo1_position -= servo_increment_step
                if servo1_position < 0:
                    servo1_position = 0
                servo1.angle = servo1_position
            elif spinRight:
                servo1_position += servo_increment_step
                if servo1_position > 180:
                    servo1_position = 180
                servo1.angle = servo1_position
            elif tiltUp:
                servo2_position -= servo_increment_step
                servo3._pwm_out.duty_cycle = 0
                if servo2_position < 0:
                    servo2_position = 0
                servo2.angle = servo2_position
            elif tiltDown:
                servo2_position += servo_increment_step
                servo3._pwm_out.duty_cycle = 0
                if servo2_position > 180:
                    servo2_position = 180
                servo2.angle = servo2_position
            elif tiltForward:
                servo3_position -= servo_increment_step
                servo2._pwm_out.duty_cycle = 0
                if servo3_position < 0:
                    servo3_position = 0
                servo3.angle = servo3_position
            elif tiltBack:
                servo3_position += servo_increment_step
                servo2._pwm_out.duty_cycle = 0
                if servo3_position > 180:
                    servo3_position = 180
                servo3.angle = servo3_position
            elif openGrip:
                servo4_position -= servo_increment_step
                if servo4_position < 0:
                    servo4_position = 0
                servo4.angle = servo4_position
            elif closeGrip:
                servo4_position += servo_increment_step
                if servo4_position > 180:
                    servo4_position = 180
                servo4.angle = servo4_position
            else:
                motorR.throttle = 0
                motorL.throttle = 0
                servo1._pwm_out.duty_cycle = 0
                servo2._pwm_out.duty_cycle = 0
                servo3._pwm_out.duty_cycle = 0
                servo4._pwm_out.duty_cycle = 0
        time.sleep(interval)
except KeyboardInterrupt:
    motorR.throttle = 0
    motorL.throttle = 0
    servo1._pwm_out.duty_cycle = 0
    servo2._pwm_out.duty_cycle = 0
    servo3._pwm_out.duty_cycle = 0
    servo4._pwm_out.duty_cycle = 0
    

