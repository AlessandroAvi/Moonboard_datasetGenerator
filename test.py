import cv2 
import numpy as np
import matplotlib.pyplot as plt 
from PIL import ImageGrab
import time
import win32api, win32con
import json
import pytesseract



# THINGS TO MODIFY FOR MAKING IT WORK ON ANY COMPUTER
# ****************************************************************************************************


# Open JSON file
json_path = r"C:/Users/massi/OneDrive/Documenti/Python/MoonBoard_CreateDataset/sample.json"


# These values define the pixel region where the code will take a screenshot. Inside this area should
# be contained the emulator screen with the moonboard app opened on the first problem
ss_region_tl_x = 100		# screen shot region, top left, x coord
ss_region_tl_y = 41 		# screen shot region, top left, y coord
ss_region_br_x = 3000		# screen shot region, bottom right, x coord
ss_region_br_y = 3000		# screen shot region, bottom left, y coord


tot_problems = 1236		# Number of problems that you want to write in the dataset


# Height and width of your screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


# These are the values that will define where are the real holds, need to fine tune this depending on your screen
yoff = 165
xoff = 84
x_sep = 43
y_sep = 43


# Capture and save screen image 
ss_region = (ss_region_tl_x,ss_region_tl_y, ss_region_br_x, ss_region_br_y)
ss_img = ImageGrab.grab(ss_region)


image = np.array(ss_img)
img = image[:, :, ::-1]


cv2.imshow('ciao', img)

cv2.waitKey(0)
