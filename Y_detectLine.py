import exifread as exif
import cv2
import matplotlib
import numpy as np
src = cv2.imread('diffGrayMeteor.png', cv2.IMREAD_GRAYSCALE)
minlight = 30
# 에지 검출
#edges = cv2.Canny(src, 50, 150)
ret, mask = cv2.threshold( src, minlight, 255, cv2.THRESH_BINARY)
# 직선 성분 검출
lines = cv2.HoughLinesP(mask, 1, np.pi / 180., 160, minLineLength=300, maxLineGap=30)

# 컬러 영상으로 변경 (영상에 빨간 직선을 그리기 위해)
dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
lines[1][0][0]

if lines is not None:  # 라인 정보를 받았으면
    for i in range(lines.shape[0]):
        pt1 = (lines[i][0][0], lines[i][0][1])  # 시작점 좌표 x,y
        pt2 = (lines[i][0][2], lines[i][0][3])  # 끝점 좌표, 가운데는 무조건 0
        cv2.line(dst, pt1,
        pt2, (0, 0, 255), 2, cv2.LINE_AA)

cv2.imwrite('detectlnMeteor.png',dst)
cv2.imwrite('edgesMeteor.png',mask)
# 시작점 pt1 주변 300칸 안에 선이 8개 이상 없다 & 선을 이루는 점의 밝기가 128보다 크다
#그러면 구름은 안걸릴거 같긴해