from object_detection.yolo_opencv import object_detector as yolo
import cv2

img = cv2.imread('object_detection/dog.jpg')
yolo(img)