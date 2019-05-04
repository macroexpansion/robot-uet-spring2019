import math
import matplotlib
import matplotlib.pyplot as plt
from ai2thor.controller import Controller
from ai2thor.controller import BFSController

from PIL import Image, ImageDraw

import copy
import numpy as np


class ThorPositionTo2DFrameTranslator(object):
    def __init__(self, frame_shape, cam_position, orth_size):
        self.frame_shape = frame_shape
        self.lower_left = np.array((cam_position[0], cam_position[2])) - orth_size
        self.span = 2 * orth_size

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

if __name__ == '__main__': 
	c = Controller()
	c.start()
	c.reset("FloorPlan1")
	topview = get_agent_map_data(c)
	plt.imshow(topview["frame"])
	plt.show()