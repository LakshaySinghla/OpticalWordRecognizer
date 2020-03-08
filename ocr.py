import cv2
import numpy as np
import image_processing as ip

img = cv2.imread("Image/Test_.jpg",0)
img = ip.image_for_extraction(img)
cv2.imwrite("Image/Binary Test.png",img)
img,M = ip.getTransformationMatrixAndImg(img)
cv2.imwrite("Image/Rotated Img.png",img)

ycoords, max_height_on_line = ip.extract_line(img)
print("ycoords" , ycoords)
print("max_height_on_line",max_height_on_line)

words_on_line, all_words = ip.extract_words(img,ycoords)
print("words_on_line",words_on_line)

ip.extract_character(words_on_line, all_words, max_height_on_line, use_dict=False)