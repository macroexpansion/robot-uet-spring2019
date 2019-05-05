import ai2thor.controller
import keyboard
import time
from object_detection.yolo_opencv import object_detector as yolo
import cv2
controller = ai2thor.controller.Controller()
controller.start()

# Kitchens: FloorPlan1 - FloorPlan30
# Living rooms: FloorPlan201 - FloorPlan230
# Bedrooms: FloorPlan301 - FloorPlan330
# Bathrooms: FloorPLan401 - FloorPlan430

controller.reset('FloorPlan25')
event = controller.step(dict(action='Initialize', gridSize=0.05, renderClassImage=True, renderObjectImage=True))

while True:
    if   keyboard.is_pressed("d"):
        event = controller.step(dict(action="MoveRight"))
        yolo(event.cv2img)
    elif keyboard.is_pressed("s"):
        event = controller.step(dict(action="MoveBack"))
        yolo(event.cv2img)
    elif keyboard.is_pressed("a"):
        event = controller.step(dict(action="MoveLeft"))
        yolo(event.cv2img)
    elif keyboard.is_pressed("w"):
        event = controller.step(dict(action="MoveAhead"))
        yolo(event.cv2img)
    elif keyboard.is_pressed("j"):
        event = controller.step(dict(action="RotateLeft"))
        yolo(event.cv2img)
        time.sleep(0.5)
    elif keyboard.is_pressed("l"):
        event = controller.step(dict(action="RotateRight"))
        yolo(event.cv2img)
        time.sleep(0.5)
    elif keyboard.is_pressed("i"):
        event = controller.step(dict(action="LookUp"))
        yolo(event.cv2img)
        time.sleep(0.5)
    elif keyboard.is_pressed("k"):
        event = controller.step(dict(action="LookDown"))
        yolo(event.cv2img)
        time.sleep(0.5)
    else:
        pass