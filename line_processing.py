import cv2
import numpy as np

def findLines(bw_image, LinesThres):
	horProj = cv2.reduce(bw_image, 1, cv2.REDUCE_AVG)       # making horizontal projections
	# make hist - same dimension as horProj - if 0 (space), then True, else False
	th = 0 # black pixels threshold value. this represents the space lines
	hist = horProj <= th
	#Get mean coordinate of white white pixels groups
	ycoords = []
	y = 0
	count = 0
	isSpace = False
	for i in range(0, bw_image.shape[0]):
		if (not isSpace):
			if (hist[i]): #if space is detected, get the first starting y-coordinates and start count at 1
				isSpace = True
				count = 1
				y = i
		else:
			if (not hist[i]):
				isSpace = False
				#when smoothing, thin letters will breakdown, creating a new blank lines or pixel rows, but the count will be small, so we set a threshold.
				if (count >=LinesThres):
					ycoords.append(y / count)
			else:
				y = y + i
				count = count + 1
	ycoords.append(y / count)
	#returns y-coordinates of the lines found
	return ycoords

def LinesMedian(bw_image):
	horProj = cv2.reduce(bw_image, 1, cv2.REDUCE_AVG)       # making horizontal projections
	# make hist - same dimension as horProj - if 0 (space), then True, else False
	th = 0 # black pixels threshold value. this represents the space lines
	hist = horProj <= th

	#Get mean coordinate of white white pixels groups
	count = 0
	isSpace = False
	median_count = []
	for i in range(0, bw_image.shape[0]):
		if (not isSpace):
			if (hist[i]):   #if space is detected, get the first starting y-coordinates and start count at 1
				isSpace = True
				count = 1
		else:
			if (not hist[i]):
				isSpace = False
				median_count.append(count)
			else:
				count = count + 1
	median_count.append(count)
	
	#returns counts of each blank rows of each of the lines found
	return median_count

def get_lines_threshold(percent, img_for_det):
	LinMed = LinesMedian(img_for_det)
	LinMed = sorted(LinMed)
	LinesThres = LinMed[int(len(LinMed)/3)]*(percent/100.0)
	return int(LinesThres)

def max_line_height(img,ycoords):
	max_height_on_line = []
	for i in range ( 0, len(ycoords)-1 ):               #iterate each line
		line = img[range(int(ycoords[i]),int(ycoords[i+1]))]
		# to find max_line_height of each line we find contours again in this line only
		contour0 = cv2.findContours(line.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		contours = [cv2.approxPolyDP(cnt,2,True) for cnt in contour0[0]]

		# === Extract Bounding Rectangles
		maxArea = 0
		rect=[]
		for ctr in contours:
			maxArea = max(maxArea,cv2.contourArea(ctr))
		areaRatio = 0.008
		for ctr in contours:
			if cv2.contourArea(ctr) > maxArea * areaRatio: 
				rect.append(cv2.boundingRect(cv2.approxPolyDP(ctr,1,True)))
		#Find max_line_height and width
		max_line_height = 0
		for i in rect:
			x = i[0]
			y = i[1]
			w = i[2]
			h = i[3]
			if(h>max_line_height):
				max_line_height = h
		max_height_on_line.append(max_line_height)
	return max_height_on_line
