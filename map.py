import ai2thor.controller
import keyboard
import time
import cv2 as cv
import numpy as np

controller = ai2thor.controller.Controller()
controller.start()
controller.reset('FloorPlan28')

img = np.zeros((512,512,3), np.uint8)
x, y = 250, 250

event = controller.step(dict(action='Initialize', gridSize=0.05, rotation=0.1))
cv.rectangle(img,(x, y),(x + 15, y + 15),(255,0,0),-1)

while True:
    if   keyboard.is_pressed('d'):
        event = controller.step(dict(action='MoveRight'))
        x, y = x + 15, y
        cv.rectangle(img, (x, y), (x + 15, y + 15), (0,255,0), -1)
        # print('right')
        time.sleep(1)
        # print(event.metadata['objects'])
    elif keyboard.is_pressed('s'):
        event = controller.step(dict(action='MoveBack'))
        x, y = x, y + 15
        cv.rectangle(img, (x, y), (x + 15, y + 15), (0,255,0), -1)
        # print('down')
        time.sleep(1)
    elif keyboard.is_pressed('a'):
        event = controller.step(dict(action='MoveLeft'))
        x, y = x - 15, y
        cv.rectangle(img,(x,y), (x + 15,y + 15), (0,255,0), -1)
        # print('left')
        time.sleep(1)
    elif keyboard.is_pressed('w'):
        event = controller.step(dict(action='MoveAhead'))
        x, y = x, y - 15
        cv.rectangle(img, (x, y), (x + 15, y + 15), (0,255,0), -1)
        # print('up')
        time.sleep(1)
    elif keyboard.is_pressed('j'):
        event = controller.step(dict(action='RotateLeft'))
        time.sleep(1)
    elif keyboard.is_pressed('l'):
        event = controller.step(dict(action='RotateRight'))
        time.sleep(1)
    elif keyboard.is_pressed('i'):
        event = controller.step(dict(action='LookUp'))
        time.sleep(1)
    elif keyboard.is_pressed('k'):
        event = controller.step(dict(action='LookDown'))
        time.sleep(1)
    elif keyboard.is_pressed('z'):
        break
    elif keyboard.is_pressed('o'):
        cv.imshow('img', img)
        cv.waitKey(0)
        # cv.destroyAllWindows()
    else:
        pass
