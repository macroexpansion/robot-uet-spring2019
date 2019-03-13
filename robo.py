import ai2thor.controller
import keyboard
import time
controller = ai2thor.controller.Controller()
controller.start()

# Kitchens: FloorPlan1 - FloorPlan30
# Living rooms: FloorPlan201 - FloorPlan230
# Bedrooms: FloorPlan301 - FloorPlan330
# Bathrooms: FloorPLan401 - FloorPlan430

controller.step(dict(action='Initialize', gridSize=0.25, rotation=1))

while True:
    if   keyboard.is_pressed("d"):
        controller.step(dict(action="MoveRight"))
        time.sleep(0.5)
    elif keyboard.is_pressed("s"):
        controller.step(dict(action="MoveBack"))
        time.sleep(0.5)
    elif keyboard.is_pressed("a"):
        controller.step(dict(action="MoveLeft"))
        time.sleep(0.5)
    elif keyboard.is_pressed("w"):
        controller.step(dict(action="MoveAhead"))
        time.sleep(0.5)
    elif keyboard.is_pressed("q"):
        controller.step(dict(action="RotateLeft"))
        time.sleep(0.5)
    elif keyboard.is_pressed("e"):
        controller.step(dict(action="RotateRight"))
        time.sleep(0.5)
    elif keyboard.is_pressed("2"):
        controller.step(dict(action="LookUp"))
        time.sleep(0.5)
    else:
        pass