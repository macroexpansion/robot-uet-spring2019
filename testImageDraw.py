from PIL import Image, ImageDraw
import keyboard
from matplotlib import pyplot as plt

source_image = Image.open('/Users/minhmon/robot-uet-spring2019/map.png')
draw = ImageDraw.Draw(source_image)
x = 0
y = 0
draw.rectangle(((x,y) , (x+50, y-50)), fill = 'green')
plt.imshow(draw)
# while True:
# 	try:
# 		if keyboard.is_pressed('left arrow'):
# 			x -= 50
# 		elif keyboard.is_pressed('right arrow'):
# 			x += 50
# 		elif keyboard.is_pressed('up arrow'):
# 			y += 50
# 		elif keyboard.is_pressed('down arrow'):
# 			y -= 50
# 		draw.rectangle(((x,y) , (x+50, y-50)), fill = 'green')

# 	except Exception as error:
# 		raise error