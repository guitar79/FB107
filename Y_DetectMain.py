# 유성체감시네트워크에 적용될, 최종 유성 및 기타 물체 탐지 코드
import numpy as np
import cv2
image1 = cv2.imread( "Filename.format", cv2.IMREAD_GRAYSCALE )  #직전에 촬영된 이미지 불러오기
image2 = cv2.imread( "Filename.format", cv2.IMREAD_GRAYSCALE )  #방금 촬영된 이미지 불러오기
different = cv2.absdiff( image1, image2 ) #둘에서 달라진 점을 계산
height = image1.shape[0]    #세로 픽셀 수
width = image1.shape[1]    #가로 픽셀 수
absofD = cv2.mean(different)

minlight = 100
ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)
