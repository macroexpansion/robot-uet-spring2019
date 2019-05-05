import ai2thor.controller
import keyboard
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

controller = ai2thor.controller.Controller()
controller.start()

controller.reset('FloorPlan28')
controller.step(dict(action = 'Initialize', gridSize = 0.1))
controller.step(dict(action = 'ToggleMapView'))

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

im = np.array(controller.last_event.frame, dtype = np.uint8)

fig, ax = plt.subplots(1)

ax.imshow(im)

cam_position = controller.last_event.metadata["cameraPosition"]
cam_orth_size = controller.last_event.metadata["cameraOrthSize"]
pos_translator = ThorPositionTo2DFrameTranslator(
    controller.last_event.frame.shape, position_to_tuple(cam_position), cam_orth_size
)
convert = pos_translator(position_to_tuple(controller.last_event.metadata['agent']['position']))

rect = patches.Rectangle((convert[1], convert[0]), 20, 20, facecolor = 'g')

ax.add_patch(rect)

plt.show(block = False)
controller.step(dict(action = 'ToggleMapView'))

while True:
	try:
		if keyboard.is_pressed('left arrow'):
			plt.clf()
			controller.step(dict(action = 'MoveLeft'))
		elif keyboard.is_pressed('right arrow'):
			plt.clf()
			controller.step(dict(action = 'MoveRight'))
		elif keyboard.is_pressed('up arrow'):
			plt.clf()
			controller.step(dict(action = 'MoveAhead'))
		elif keyboard.is_pressed('down arrow'):
			plt.clf()
			controller.step(dict(action = 'MoveBack'))
		elif keyboard.is_pressed('r'):
			plt.clf()
			controller.step(dict(action = 'RotateLeft'))

		cam_position = controller.last_event.metadata["cameraPosition"]
		cam_orth_size = controller.last_event.metadata["cameraOrthSize"]	
		pos_translator = ThorPositionTo2DFrameTranslator(
		    controller.last_event.frame.shape, position_to_tuple(cam_position), cam_orth_size
		)
		convert = pos_translator(position_to_tuple(controller.last_event.metadata['agent']['position']))

		rect = patches.Rectangle((convert[1], convert[0]), 20, 20, facecolor = 'g')

		ax.add_patch(rect)

		plt.show(block = False)
	except Exception as e:
		raise e