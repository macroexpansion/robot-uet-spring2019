import ai2thor.controller
import keyboard
import time
controller = ai2thor.controller.Controller()
controller.start()

# Kitchens: FloorPlan1 - FloorPlan30
# Living rooms: FloorPlan201 - FloorPlan230
# Bedrooms: FloorPlan301 - FloorPlan330
# Bathrooms: FloorPLan401 - FloorPlan430

controller.reset('FloorPlan28')
event = controller.step(dict(action='Initialize', gridSize=0.05, rotation=-0.01))

def getInfo(_event):
    for o in _event.metadata['objects']:
        if o['visible'] and o['receptacle']:
            receptacle_object_id = o['objectId']
            return receptacle_object_id

while True:
    if   keyboard.is_pressed("d"):
        event = controller.step(dict(action="MoveRight"))
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
    elif keyboard.is_pressed("p"):
        dist = dict()
        for o in event.metadata['objects']:
            if o['visible'] and o['pickupable']:
                dist[o['objectId']] = o['distance']
        # print(dist)
        minDist_objectId = min(dist, key=dist.get)
        event = controller.step(dict(action='PickupObject', objectId=minDist_objectId), raise_for_failure=True)
        object_id = minDist_objectId
        time.sleep(1)
    elif keyboard.is_pressed("["):
        dist = dict()
        for o in event.metadata['objects']:
            if o['receptacle']:
                dist[o['objectId']] = o['distance']
        minDist_receptacleObjectId = min(dist, key=dist.get)
        event = controller.step(dict(action='PutObject', receptacleObjectId=minDist_receptacleObjectId, objectId=object_id), raise_for_failure=True)
        time.sleep(1)

    else:
        pass