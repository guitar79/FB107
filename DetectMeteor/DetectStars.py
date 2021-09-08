# 별이 시간에 따라서 일정하게 움직이므로, 연속된 사진에서 2개의 점이 나란히 있는 것이 별임을 이용하여 별을 검출하는 코드

import cv2
image1 = cv2.imread( "Filename.format", cv2.IMREAD_GRAYSCALE )
image2 = cv2.imread( "Filename.format", cv2.IMREAD_GRAYSCALE )
different = cv2.absdiff( image1, image2 )
height = image1.shape[0]
width = image1.shape[1]