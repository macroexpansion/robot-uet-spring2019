import ai2thor.controller
import keyboard
import time
controller = ai2thor.controller.Controller()
controller.start()

# Kitchens: FloorPlan1 - FloorPlan30
# Living rooms: FloorPlan201 - FloorPlan230
# Bedrooms: FloorPlan301 - FloorPlan330
# Bathrooms: FloorPLan401 - FloorPlan430

controller.reset('FloorPlan18')
event = controller.step(dict(action='Initialize', gridSize=0.05, rotation=-0.01))

while True:
    if   keyboard.is_pressed("d"):
        event = controller.step(dict(action="MoveRight"))
        if event.metadata['lastActionSuccess'] is True:
            print(1)
        # print(event.metadata['objects'])
    elif keyboard.is_pressed("s"):
        event = controller.step(dict(action="MoveBack"))
    elif keyboard.is_pressed("a"):
        event = controller.step(dict(action="MoveLeft"))
    elif keyboard.is_pressed("w"):
        event = controller.step(dict(action="MoveAhead"))
    elif keyboard.is_pressed("j"):
        event = controller.step(dict(action="RotateLeft"))
        time.sleep(0.5)
    elif keyboard.is_pressed("l"):
        event = controller.step(dict(action="RotateRight"))
        time.sleep(0.5)
    elif keyboard.is_pressed("i"):
        event = controller.step(dict(action="LookUp"))
        time.sleep(0.5)
    elif keyboard.is_pressed("k"):
        event = controller.step(dict(action="LookDown"))
        time.sleep(0.5)
    

    else:
        pass