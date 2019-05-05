import numpy as np
import cv2 as cv
import keyboard as kb
import time
# Create a black image
img = np.zeros((512,512,3), np.uint8)
# Draw a diagonal blue line with thickness of 5 px
# cv.line(img,(0,0),(511,511),(255,0,0),5)
x, y = 250, 250
cv.rectangle(img,(x,y), (x + 15,y + 15), (255,0,0), -1)
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()

while True:
    if kb.is_pressed('a'): #left
        x, y = x - 15, y
        cv.rectangle(img,(x,y), (x + 15,y + 15), (0,255,0), -1)
        print('left')
        time.sleep(1)
    elif kb.is_pressed('d'): #right
        x, y = x + 15, y
        cv.rectangle(img, (x, y), (x + 15, y + 15), (0,255,0), -1)
        print('right')
        time.sleep(1)
    elif kb.is_pressed('w'): #up
        x, y = x, y - 15
        cv.rectangle(img, (x, y), (x + 15, y + 15), (0,255,0), -1)
        print('up')
        time.sleep(1)
    elif kb.is_pressed('s'): #down
        x, y = x, y + 15
        cv.rectangle(img, (x, y), (x + 15, y + 15), (0,255,0), -1)
        print('down')
        time.sleep(1)
    elif kb.is_pressed('z'):
        break
    else:
        # cv.imshow('img', img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        pass