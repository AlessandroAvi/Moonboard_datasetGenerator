import cv2 
import numpy as np
import matplotlib.pyplot as plt 
from PIL import ImageGrab
import time
import win32api, win32con
import json




# -------------------------------------------------------
#    _____ _   _ _   _  ____ _____ ___ ___  _   _ ____  
#   |  ___| | | | \ | |/ ___|_   _|_ _/ _ \| \ | / ___| 
#   | |_  | | | |  \| | |     | |  | | | | |  \| \___ \ 
#   |  _| | |_| | |\  | |___  | |  | | |_| | |\  |___) |
#   |_|    \___/|_| \_|\____| |_| |___\___/|_| \_|____/ 
#
# -------------------------------------------------------




def detect_circle(image, name, verbose):

	all_circs = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, 30, param1=60, param2=40, minRadius=0, maxRadius=1000)
	if(all_circs is None):
		all_circs_rounded = []
	else:
		all_circs_rounded = np.uint16(np.around(all_circs))

	count = 1
	if(all_circs is not None):
		for i in all_circs_rounded[0,:]:
			cv2.circle(image, (i[0],i[1]),i[2],(50,200,200),5)
			cv2.circle(image, (i[0],i[1]),2,(255,0,0),3)
			count +=1

	if(verbose==1):
		cv2.imshow(name, image)

	return all_circs_rounded




def closest_hold(y,x,holds_pos):
	lett_str = ["A","B","C","D","E","F","G","H","I","J","K"]
	num_str = ["18","17","16","15","14","13","12","11","10","9","8","7","6","5","4","3","2","1"]

	# find the closest on y axis
	ymin = 1000
	for i in range(0,18):
		ydist = np.abs(y-holds_pos[i,0,0])
		if(ydist < ymin):
			ymin = ydist
			closest_row = i
	# find the closest on x axis
	xmin = 1000
	for j in range(0,11):
		xdist = np.abs(x-holds_pos[0,j,1])
		if(xdist < xmin):
			xmin = xdist
			closest_col = j
	
	return [num_str[closest_row], lett_str[closest_col]]




def nextProblem(tl_x, tl_y, br_x, r_y, SCREEN_WIDTH, SCREEN_HEIGHT):

	x = tl_x + (br_x-tl_x) * 0.88
	y = (tl_y+tl_y)/2



	win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/SCREEN_WIDTH*65535.0), int(y/SCREEN_HEIGHT*65535.0))    
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

	win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int((x-50)/SCREEN_WIDTH*65535.0), int(y/SCREEN_HEIGHT*65535.0))      
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x-50,y,0,0)




def writeJSONfile(n, r_hold, g_hold, b_hold, json_decoded):


	# Write the json informations
	problem_name = str(n)

	problem_dict = {
        "Name" : "to_be_done",
        "Grade" : "to_be_done",
        "Moves" : [],
    	"Sended":"false"
    }

	# Cycle over red holds - TOP
	for k in range(0, len(r_hold)):

		hold_name = str(r_hold[k][0])+str(r_hold[k][1])
		hold_start = "false"
		hold_top = "true"

		move_dict = {
					"Description": hold_name,
					"IsStart": hold_start,
					"IsEnd": hold_top
		}

		problem_dict["Moves"].append(move_dict)

	# Cycle over blue holds - MIDDLE
	for k in range(0, len(b_hold)):

		hold_name = str(b_hold[k][0])+str(b_hold[k][1])
		hold_start = "false"
		hold_top = "false"

		move_dict = {
					"Description": hold_name,
					"IsStart": hold_start,
					"IsEnd": hold_top
		}

		problem_dict["Moves"].append(move_dict)

	# Cycle over green holds - START
	for k in range(0, len(g_hold)):

		hold_name = str(g_hold[k][0])+str(g_hold[k][1])
		hold_start = "true"
		hold_top = "false"

		move_dict = {
					"Description": hold_name,
					"IsStart": hold_start,
					"IsEnd": hold_top
		}

		problem_dict["Moves"].append(move_dict)



	json_decoded[str(n)] = problem_dict





# --------------------------------
#    __  __    _    ___ _   _ 
#   |  \/  |  / \  |_ _| \ | |
#   | |\/| | / _ \  | ||  \| |
#   | |  | |/ ___ \ | || |\  |
#   |_|  |_/_/   \_\___|_| \_|
#
# --------------------------------




# THINGS TO MODIFY FOR MAKING IT WORK ON ANY COMPUTER
# ****************************************************************************************************


# Open JSON file
json_path = r"YOUR_PATH_TO_THIS_REPO/sample.json"


# These values define the pixel region where the code will take a screenshot. Inside this area should
# be contained the emulator screen with the moonboard app opened on the first problem
ss_region_tl_x = 1316		# screen shot region, top left, x coord
ss_region_tl_y = 41 		# screen shot region, top left, y coord
ss_region_br_x = 1879		# screen shot region, bottom right, x coord
ss_region_br_y = 1040		# screen shot region, bottom left, y coord


tot_problems = 1236		# Number of problems that you want to write in the dataset


# Height and width of your screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


# These are the values that will define where are the real holds, need to fine tune this depending on your screen
yoff = 165
xoff = 84
x_sep = 43
y_sep = 43

# ****************************************************************************************************




with open(json_path) as json_file:
    json_decoded = json.load(json_file)


# Cycle over all the problems available in the app
for n in range(0, 1):

	# Capture and save screen image 
	ss_region = (ss_region_tl_x,ss_region_tl_y, ss_region_br_x, ss_region_br_y)
	ss_img = ImageGrab.grab(ss_region)

	image = np.array(ss_img)
	img = image[:, :, ::-1]


	# Exctract the circles (G,R,B)
	low_r  = np.array([0, 0, 210])				# minimum color red accepted in the mask
	high_r = np.array([30, 30, 255])			# maximum color red accepted in the mask
	maskR  = cv2.inRange(img, low_r, high_r)

	low_b  = np.array([210, 0, 0])
	high_b = np.array([255, 30, 30])
	maskB  = cv2.inRange(img, low_b, high_b)

	low_g  = np.array([0, 210, 0])
	high_g = np.array([30, 255, 30])
	maskG  = cv2.inRange(img, low_g, high_g)
	

	# Detect the centers and radiuses of circles
	red_circles   = detect_circle(maskR, "red detection",1)
	blue_circles  = detect_circle(maskB, "blue detection",1)
	green_circles = detect_circle(maskG, "green detection",1)


	# Create matrix that contains the real holds positions, need to fine tune parameter depending on the screen
	holds_pos = np.zeros((18,11,2))
	for j in range(0,18):
		for i in range(0,11):
			holds_pos[j,i,1] = xoff+x_sep*i
			holds_pos[j,i,0] = yoff+y_sep*j

			# ******** Uncomment the line below to debug and fine tune the parameters ********
			#cv2.circle(img, (xoff+x_sep*i,yoff+y_sep*j),2,(255,0,0),3)

	# ******** Uncomment the line below to debug and fine tune the parameters ********
	#cv2.imshow('moon', img)


	# Assign to each fiund circle the closes real hold
	r_hold = []
	b_hold = []
	g_hold = []

	if type(red_circles) is not list:
		for i in range(0,red_circles.shape[1]):
			hold = closest_hold(red_circles[0,i,1],red_circles[0,i,0], holds_pos)
			r_hold.append(hold)

	if type(blue_circles) is not list:
		for i in range(0,blue_circles.shape[1]):
			hold = closest_hold(blue_circles[0,i,1],blue_circles[0,i,0], holds_pos)
			b_hold.append(hold)

	if type(green_circles) is not list:
		for i in range(0,green_circles.shape[1]):
			hold = closest_hold(green_circles[0,i,1],green_circles[0,i,0], holds_pos)
			g_hold.append(hold)


	# Write the results in a JSON file
	writeJSONfile(n, r_hold, g_hold, b_hold, json_decoded)


	nextProblem(ss_region_tl_x, ss_region_tl_y, ss_region_br_x, ss_region_br_y, SCREEN_WIDTH, SCREEN_HEIGHT)
	print(n)

	cv2.waitKey(0)


# Write everything in one json file
with open(json_path, 'w') as json_file:
    json.dump(json_decoded, json_file, sort_keys=True, indent=4, separators=(',', ': '))