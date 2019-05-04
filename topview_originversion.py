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

listRectangle = []

def add_agent_view_triangle(position, rotation, frame, pos_translator):
    
    img1 = Image.fromarray(frame.astype("uint8"), "RGB").convert("RGBA")
    img2 = Image.new("RGBA", frame.shape[:-1])  # Use RGBA

    convert = pos_translator(position)

    draw = ImageDraw.Draw(img2)
    global listRectangle
    listRectangle += [((convert[1], convert[0]), (convert[1] + 20, convert[0] + 20))]
    for rect in listRectangle:
        draw.rectangle((rect[0], rect[1]), fill=(39, 174, 96))

    img = Image.alpha_composite(img1, img2)
    return np.array(img.convert("RGB"))


if __name__ == "__main__":    
    c = Controller()
    c.start()
    c.reset("FloorPlan1")
    topview = get_agent_map_data(c)
    new_frame = add_agent_view_triangle(
        position_to_tuple(c.last_event.metadata["agent"]["position"]),
        c.last_event.metadata["agent"]["rotation"]["y"],
        topview["frame"],
        topview["pos_translator"],
    )
    plt.imshow(new_frame)
    plt.show(block = False)
    while True:
        try:
            if keyboard.is_pressed('left arrow'):
                plt.close(1)
                event = c.step(dict(action = 'MoveLeft'))
            elif keyboard.is_pressed('right arrow'):
                plt.close(1)
                event = c.step(dict(action = 'MoveRight'))
            elif keyboard.is_pressed('up arrow'):
                plt.close(1)
                event = c.step(dict(action = 'MoveAhead'))
            elif keyboard.is_pressed('down arrow'):
                plt.close(1)
                event = c.step(dict(action = 'MoveBack'))
            elif keyboard.is_pressed('r'):
                plt.close(1)
                event = c.step(dict(action = 'RotateLeft'))
            new_frame1 = add_agent_view_triangle(
                position_to_tuple(c.last_event.metadata["agent"]["position"]),
                c.last_event.metadata["agent"]["rotation"]["y"],
                topview["frame"],
                topview["pos_translator"],
            )
            plt.imshow(new_frame1)
            plt.show(block = False)
        except Exception as error:
            raise error