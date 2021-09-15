import cv2
import numpy
# load images
image1 = cv2.imread("leftImageRain.jpg")
image2 = cv2.imread("rightImageRain.jpg")
thrVal = 3
# compute difference
difference = cv2.absdiff(image2, image1)
diffMal = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
# color the mask red
Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
height= image1.shape[0]
width = image1.shape[1]
for i in range(0, height):
  for j in range(0, width):
    temp = int(diffMal[i][j])*10
    if(temp > 255):
        temp = 255
    diffMal[i][j] = temp
ret, mask = cv2.threshold(Conv_hsv_Gray, thrVal, 255, cv2.THRESH_BINARY_INV)
difference[mask != 255] = [0, 0, 255]

# add the red mask to the images to make the differences obvious
image1[mask != 255] = [0, 0, 255]
image2[mask != 255] = [0, 0, 255]

# store images
cv2.imwrite('maskRain.png', mask)
cv2.imwrite('diffGrayRain.png', Conv_hsv_Gray)
cv2.imwrite('diffMalRain.png',diffMal)
cv2.imwrite('diffOverImage1Rain.png', image1)
cv2.imwrite('diffOverImage2Rain.png', image2)
cv2.imwrite('diffRain.png', difference)
