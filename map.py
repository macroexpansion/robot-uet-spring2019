import ai2thor.controller
import keyboard
import time
import cv2 as cv
import numpy as np

controller = ai2thor.controller.Controller()
controller.start()
controller.reset('FloorPlan18')

event = controller.step(dict(action='Initialize', gridSize=0.2, rotation=0.1))

X_ROOM, Y_ROOM = 600, 600
img = np.zeros((X_ROOM, Y_ROOM,3), np.uint8)

color = {
    'BLUE': (255,0,0),
    'GREEN': (0,255,0),
    'WHITE': (255,255,255)
}

x, y = int(X_ROOM / 2), int(Y_ROOM / 2)

def drawGrid(x, y, color):
    cv.rectangle(img, (x, y), (x + 15, y + 15), color , -1)

def drawMap():
    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

drawGrid(x,y, color['BLUE'])
while True:
    if   keyboard.is_pressed('d'):
        event = controller.step(dict(action='MoveRight'))
        if event.metadata['lastActionSuccess'] is True:
            drawGrid(x, y, color['GREEN'])
            x, y = x + 15, y
            drawGrid(x, y, color['WHITE'])
        drawMap()
    elif keyboard.is_pressed('s'):
        event = controller.step(dict(action='MoveBack'))
        if event.metadata['lastActionSuccess'] is True:
            drawGrid(x, y, color['GREEN'])
            x, y = x, y + 15
            drawGrid(x, y, color['WHITE'])
        drawMap()
    elif keyboard.is_pressed('a'):
        event = controller.step(dict(action='MoveLeft'))
        if event.metadata['lastActionSuccess'] is True:
            drawGrid(x, y, color['GREEN'])
            x, y = x - 15, y
            drawGrid(x, y, color['WHITE'])
        drawMap()
    elif keyboard.is_pressed('w'):
        event = controller.step(dict(action='MoveAhead'))
        if event.metadata['lastActionSuccess'] is True:
            drawGrid(x, y, color['GREEN'])
            x, y = x, y - 15
            drawGrid(x, y, color['WHITE'])
        drawMap()
    elif keyboard.is_pressed('j'):
        event = controller.step(dict(action='RotateLeft'))
    elif keyboard.is_pressed('l'):
        event = controller.step(dict(action='RotateRight'))
    elif keyboard.is_pressed('i'):
        event = controller.step(dict(action='LookUp'))
    elif keyboard.is_pressed('k'):
        event = controller.step(dict(action='LookDown'))
    elif keyboard.is_pressed('z'):
        break
    else:
        pass
