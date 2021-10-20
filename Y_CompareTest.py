import cv2

image1 = cv2.imread("leftImage.JPG",cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread("rightImage.JPG",cv2.IMREAD_GRAYSCALE)
different = cv2.absdiff(image1, image2)
height = image1.shape[0]
width = image1.shape[1]
for i in range(0, height):
  for j in range(0, width):
    temp = int(different[i][j])*10
    if(temp > 255):
        temp = 255
    different[i][j] = temp

cv2.imwrite('test.png', different)
