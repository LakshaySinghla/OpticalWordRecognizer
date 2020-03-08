import cv2
import numpy as np
import line_processing as lp
import word_processing as wp
import character_processing as cp
import user_input


### ========== Image Extraction ==========
def image_for_extraction(raw_image):
	raw_image = cv2.GaussianBlur(raw_image,(3,3),0)
	ret,no_sm_bw_image = cv2.threshold(raw_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	return no_sm_bw_image

def image_for_detection(raw_image):
	sm_image = cv2.GaussianBlur(raw_image,(5,5),0)
	ret, bw_image = cv2.threshold(sm_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	kernel = np.ones((2,2),np.uint8)
	bw_image = cv2.dilate(bw_image,kernel)
	return bw_image

def getTransformationMatrixAndImg(img):     #input should be a binarized image - text white, bg black
	pts = np.empty([0,0])           #Find all white pixels
	pts = cv2.findNonZero(img)
	rect = cv2.minAreaRect(pts)     #Get rotated rect of white pixels
	
	# rect[0] has the center of rectangle, rect[1] has width and height, rect[2] has the angle
	# To draw the rotated box and save the png image, uncomment below
	drawrect = img.copy()
	drawrect = cv2.cvtColor(drawrect, cv2.COLOR_GRAY2BGR)
	box = cv2.boxPoints(rect)
	box = np.int0(box) # box now has four vertices of rotated rectangle
	cv2.drawContours(drawrect,[box],0,(0,0,255),10)
	cv2.imwrite('Image/rotated_rect.png', drawrect)

	#Change rotation angle if the tilt is in another direction
	rect = list(rect)
	if (rect[1][0] < rect[1][1]): # rect.size.width > rect.size.height
		temp = list(rect[1])
		temp[0], temp[1] = temp[1], temp[0]
		rect[1] = tuple(temp)
		rect[2] = rect[2] + 90.0
	#convert rect back to numpy/tuple
	rect = np.asarray(rect)
	
	#Rotate the image according to the found angle
	rotated_image = np.empty([0,0])
	M = cv2.getRotationMatrix2D(rect[0], rect[2], 1.0)
	return cv2.warpAffine(img, M, (img.shape[1],img.shape[0])) , M

### ========== Lines Extraction ==========
def extract_line(img):
	#get threshold to determine how much gap should be considered as the line gap
	LinesThres = lp.get_lines_threshold(40, img)
	ycoords = lp.findLines(img, LinesThres)
	# save image with lines printed ==========
	img_with_lines = img.copy()
	for i in ycoords:
		cv2.line(img_with_lines,(0,int(i)),(img_with_lines.shape[1],int(i)),255,1)
	cv2.imwrite('Image/img_with_lines.png', img_with_lines)
	#calculate max_line_height on each line
	max_height_on_line = lp.max_line_height(img,ycoords)
	return ycoords, max_height_on_line

### ========== Word Extraction ==========
def extract_words(img,ycoords):
	#get the threshold to determine how much gap should be considered as the space between the words
	threshold_space = wp.get_spaces_threshold(ycoords, img)

	#split lines based on the ycoords of the detected lines
	#each line is put into the var 'line' and the words are found
	#based on the threshold_space value.
	words_on_line=[]
	all_words=[]
	count = 0
	number_of_words = 0
	for i in range ( 0, len(ycoords)-1 ): #iterate line
		line = img[range(int(ycoords[i]),int(ycoords[i+1]))]
		#cv2.imwrite('lines/'+str(i)+'.png', line)
		#finding the x-coordinates of the spaces
		xcoords = wp.findSpaces(line, threshold_space)
		#print len(xcoords)
		for x in xcoords:
			cv2.line(line, (int(x),0), (int(x),line.shape[0]), 255, 1)
		cv2.imwrite('Image/lines/'+str(i)+'.png', line)
		count = 0
		for j in range (0, len(xcoords)-1 ): #iterate words
			#use image with no smoothing
			line = img[range(int(ycoords[i]),int(ycoords[i+1]))]
			word = line[:, int(xcoords[j]): int(xcoords[j+1])]
			all_words.append(word)
			cv2.imwrite('Image/words/'+str(number_of_words)+'.png', word)
			count = count + 1
			number_of_words = number_of_words + 1
			#Generate space here
		words_on_line.append(count)
		# Line Change
	return words_on_line, all_words


### ========= Character Processsing ==========
def extract_character(words_on_line, all_words, max_height_on_line, use_dict=False):
	#to write the output into a file
	fp = open("output.txt", 'w')
	fp.truncate()
	count = 0
	for i in range(0, len(words_on_line)):
		for j in range(0, words_on_line[i]):
			all_characters = cp.get_characters(all_words[count],max_height_on_line[i],i,j)
			if use_dict:
				None
				# print (correction(get_string_from_nn(all_characters)))
				# fp.write(correction(get_string_from_nn(all_characters)))
				# fp.write(" ")
			else:
				word = user_input.get_string_from_nn(all_characters)
				print (str(count)+" word - "+word)
				fp.write(word)
				fp.write(" ")
			# exit(0)
			# cv2.imshow("all_words[count]",all_words[count])
			# cv2.waitKey()
			count = count + 1
		# print ("\n")
		fp.write("\n")
	fp.close()
	return