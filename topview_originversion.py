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


def add_agent_view_triangle(
    position, rotation, frame, pos_translator, scale=1.0, opacity=0.7
):
    p0 = np.array((position[0], position[2]))
    p1 = copy.copy(p0)
    p2 = copy.copy(p0)

    theta = -2 * math.pi * (rotation / 360.0)
    rotation_mat = np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]
    )
    offset1 = scale * np.array([-1, 1]) * math.sqrt(2) / 2
    offset2 = scale * np.array([1, 1]) * math.sqrt(2) / 2

    p1 += np.matmul(rotation_mat, offset1)
    p2 += np.matmul(rotation_mat, offset2)

    img1 = Image.fromarray(frame.astype("uint8"), "RGB").convert("RGBA")
    img2 = Image.new("RGBA", frame.shape[:-1])  # Use RGBA

    opacity = int(round(255 * opacity))  # Define transparency for the triangle.
    points = [tuple(reversed(pos_translator(p))) for p in [p0, p1, p2]]
    draw = ImageDraw.Draw(img2)
    draw.polygon(points, fill=(39, 174, 96, opacity))

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