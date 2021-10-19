import numpy as np
import cv2
src = cv2.imread('diff.png', cv2.IMREAD_GRAYSCALE) #different와 같이 작용
minlight = 100
# 에지 검출
#edges = cv2.Canny(src, 50, 150)
ret, mask = cv2.threshold( src, minlight, 255, cv2.THRESH_BINARY)
# 직선 성분 검출
# 허프 변환을 통해 직선을 검출할 수 있는데, 그 함수는 2가지가 있으며, HoughLines보다 HoughLinesP 함수가 더 효율적 (부분 탐색을 하므로 짧은 시간 내에 가능)
lines = cv2.HoughLinesP(mask, 1, np.pi / 180., 160, minLineLength=100, maxLineGap=30)
# threshold: 일치해야 하는 점의 개수
# minLineLength: 직선의 최소 길이
# maxLineGap: 직선을 이루는 점 간 최소 간격

# 컬러 영상으로 변경 (영상에 빨간 직선을 그리기 위해)
dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

if lines is not None:  # 라인 정보를 받았으면
    for i in range(lines.shape[0]):
        pt1 = (lines[i][0][0], lines[i][0][1])  # 시작점 좌표 x,y
        pt2 = (lines[i][0][2], lines[i][0][3])  # 끝점 좌표, 가운데는 무조건 0
        cv2.line(dst, pt1,
        pt2, (0, 0, 255), 2, cv2.LINE_AA)



cv2.imwrite('detectln.png',dst)
cv2.imwrite('edges.png',mask)