from object_detection import yolo_opencv as yolo
import ai2thor.controller
import keyboard
import cv2

controller = ai2thor.controller.Controller()
controller.start()
controller.reset('FloorPlan1')
event = controller.step(dict(action='Initialize', gridSize=0.25))

def main():
    while True:
        last_event = controller.last_event
        if keyboard.is_pressed('a'):
            event = controller.step(dict(action = 'MoveLeft'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('d'):
            event = controller.step(dict(action = 'MoveRight'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('w'):
            event = controller.step(dict(action = 'MoveAhead'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('s'):
            event = controller.step(dict(action = 'MoveBack'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('e'):
            event = controller.step(dict(action = 'RotateRight'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('u'):
            event = controller.step(dict(action = 'LookUp'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('j'):
            event = controller.step(dict(action = 'LookDown'))
            yolo.object_detector(event.cv2img)
        elif keyboard.is_pressed('p'):
            break
        else:
            event = last_event

if __name__=="__main__":
    main()

