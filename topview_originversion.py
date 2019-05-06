import math
import matplotlib
import matplotlib.pyplot as plt
from ai2thor.controller import Controller
from PIL import Image, ImageDraw
import copy
import numpy as np
import keyboard

class ThorPositionTo2DFrameTranslator(object):
    def __init__(self, frame_shape, cam_position, orth_size):
        self.frame_shape = frame_shape
        self.lower_left = np.array((cam_position[0], cam_position[2])) - orth_size
        self.span = 2 * orth_size

    def __call__(self, position):
        if len(position) == 3:
            x, _, z = position
        else:
            x, z = position

        camera_position = (np.array((x, z)) - self.lower_left) / self.span
        return np.array(
            (
                round(self.frame_shape[0] * (1.0 - camera_position[1])),
                round(self.frame_shape[1] * camera_position[0]),
            ),
            dtype=int,
        )


def position_to_tuple(position):
    return (position["x"], position["y"], position["z"])


def get_agent_map_data(c: Controller):
    c.step(dict(action = 'ToggleMapView'))
    cam_position = c.last_event.metadata["cameraPosition"]
    cam_orth_size = c.last_event.metadata["cameraOrthSize"]
    pos_translator = ThorPositionTo2DFrameTranslator(
        c.last_event.frame.shape, position_to_tuple(cam_position), cam_orth_size
    )
    to_return = {
        "frame": c.last_event.frame,
        "cam_position": cam_position,
        "cam_orth_size": cam_orth_size,
        "pos_translator": pos_translator
    }
    c.step(dict(action = 'ToggleMapView'))
    return to_return

listCircle = []

def add_agent_view_triangle(position, rotation, frame, pos_translator, c:Controller):
    
    img1 = Image.fromarray(frame.astype("uint8"), "RGB").convert("RGBA")
    img2 = Image.new("RGBA", frame.shape[:-1])  # Use RGBA

    convert = pos_translator(position)

    draw = ImageDraw.Draw(img2)
    
    # Make color head
    point1 = (convert[1] - 10, convert[0] - 10)
    point2 = (convert[1] + 10, convert[0] - 10)
    
    if rotation == 90:
        point1 = rotatePoint(point1, convert)
        point2 = rotatePoint(point2, convert)
    elif rotation == 180:
        point1 = rotatePoint(point1, convert)
        point2 = rotatePoint(point2, convert)
        point1 = rotatePoint(point1, convert)
        point2 = rotatePoint(point2, convert)
    elif rotation == 270:
        point1 = rotatePoint(point1, convert)
        point2 = rotatePoint(point2, convert)
        point1 = rotatePoint(point1, convert)
        point2 = rotatePoint(point2, convert)
        point1 = rotatePoint(point1, convert)
        point2 = rotatePoint(point2, convert) 

    triangle = [(convert[1], convert[0])]
    triangle += [(point1)]
    triangle += [(point2)]

    draw.polygon(triangle, fill = 'purple')

    global listCircle
    if c.last_event.metadata['lastActionSuccess'] == True:
    	z = listCircle[-1][0]
    	x = listCircle[-1][1]
    	if z != (convert[1] - 5, convert[0] - 5)  or x != (convert[1] + 5, convert[0] + 5):
    		listCircle += [((convert[1] - 5, convert[0] - 5), (convert[1] + 5, convert[0] + 5))]
    
    length = len(listCircle)
    red = math.ceil(length*0.1)
    green = round(length*0.1)
    yellow = round(length*0.1)
    orange = round(length*0.1)
    blue = length - red - green - yellow - orange
    
    # Make color tail
    for index in range(length):
        if index >= (length - red):
            draw.ellipse((listCircle[index][0], listCircle[index][1]), fill='red')
        elif index >= (length - red - orange) and index < (length - red):
            draw.ellipse((listCircle[index][0], listCircle[index][1]), fill='orange')
        elif index >= (length - red - orange - yellow) and index < (length - red - orange):
            draw.ellipse((listCircle[index][0], listCircle[index][1]), fill='yellow')
        elif index >= (length - red - orange - yellow - green) and index < (length - red - orange - yellow):
            draw.ellipse((listCircle[index][0], listCircle[index][1]), fill='green')
        elif index < (length - red - orange - yellow - green):
            draw.ellipse((listCircle[index][0], listCircle[index][1]), fill='blue')
        
    img = Image.alpha_composite(img1, img2)
    return np.array(img.convert("RGB"))

def rotatePoint(point, root):
    x = point[0] - root[1]
    y = point[1] - root[0]
    return (-y + root[1], x + root[0])


if __name__ == "__main__":    
    c = Controller()
    c.start()
    c.reset("FloorPlan1")
    c.step(dict(action = 'Initialize', gridSize = 0.2))
    topview = get_agent_map_data(c)
    convert = topview["pos_translator"](position_to_tuple(c.last_event.metadata["agent"]["position"]))
    listCircle += [((convert[1] - 5, convert[0] - 5), (convert[1] + 5, convert[0] + 5))]
    new_frame = add_agent_view_triangle(
        position_to_tuple(c.last_event.metadata["agent"]["position"]),
        c.last_event.metadata["agent"]["rotation"]["y"],
        topview["frame"],
        topview["pos_translator"],
        c
    )
    
    plt.ion()
    plt.imshow(new_frame)
    plt.show()
    while True:
        try:
            if keyboard.is_pressed('left arrow'):
                plt.clf()
                event = c.step(dict(action = 'MoveLeft'))
            elif keyboard.is_pressed('right arrow'):
                plt.clf()
                event = c.step(dict(action = 'MoveRight'))
            elif keyboard.is_pressed('up arrow'):
                plt.clf()
                event = c.step(dict(action = 'MoveAhead'))
            elif keyboard.is_pressed('down arrow'):
                plt.clf()
                event = c.step(dict(action = 'MoveBack'))
            elif keyboard.is_pressed('r'):
                plt.clf()
                event = c.step(dict(action = 'RotateRight'))
            elif keyboard.is_pressed('u'):
            	plt.clf()
            	event = c.step(dict(action = 'LookUp'))
            elif keyboard.is_pressed('d'):
            	plt.clf()
            	event = c.step(dict(action = 'LookDown'))
            new_frame = add_agent_view_triangle(
                position_to_tuple(c.last_event.metadata["agent"]["position"]),
                c.last_event.metadata["agent"]["rotation"]["y"],
                topview["frame"],
                topview["pos_translator"],
                c
            )
            plt.imshow(new_frame)
            plt.show()
            plt.pause(0.001)
        except Exception as error:
            raise error