import os
from datetime import datetime
import time
import cv2
import FB107_utilities
import Python_utilities

processing_date_str = "2021-10-04"

#if add_log == True:
#    log_file = "{}_logfile.log".format("My")

base_dir_name = '../SAVE/'
processing_dir_name = "{}{}/{}/{}/".format(base_dir_name, 
                                            processing_date_str[0:4],
                                            processing_date_str[5:7],
                                            processing_date_str[8:10])
save_dir_name = "../result/"
processing_log_fname = "statistics_result_{}.csv".format(processing_date_str)
            
#make list all files
fullnames = FB107_utilities.getFullnameListOfallFiles(processing_dir_name)

minlight = 100
processing_log = "#This file is created using Python : https://github.com/guitar79/FB107_python\n"
processing_log += "minlight = {}\n".format(minlight)
processing_log += "fullname, difference_mask(sum(sum))\n"
processing_log += "{}\n".format(len(fullnames)) # the number of files
#processing_log += "fullname, BrightR(mean), BrightR(std), BrightR(max), BrightR(min), BrightG(mean), BrightG(std), BrightG(max), BrightG(min),  BrightB(mean), BrightB(std), BrightB(max), BrightB(min), star No, FB, proc time\n"

for i in range(len(fullnames)-1)[:10] :
    # 이날 사진의 유성 판별해서 옮기는 거
    image1 = cv2.imread("{}".format(fullnames[i]), cv2.IMREAD_GRAYSCALE )  #직전에 촬영된 이미지 불러오기
    image2 = cv2.imread("{}".format(fullnames[i+1]), cv2.IMREAD_GRAYSCALE )  #방금 촬영된 이미지 불러오기
    different = cv2.absdiff(image1, image2) #둘에서 달라진 점을 계산
    ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)
    S1 = sum(sum(image1))
    S2 = sum(sum(image2))
    INCM = 0 # 0: 달이 있는 사진 1: 달이 없는 사진
    MODIF = cv2.mean(different) # 차이 픽셀값의 평균
    STDODIF = cv2.meanStdDev(different) # 차이 픽셀값의 표준편차
    ITM = 0 # 0: meteor(dotted line) 1: cloud(scattered) 2: airplane or satellite(solid line)
    processing_log += "{}, {}, {}, {}\n"\
        .format(fullnames[i], sum(sum(mask)), INCM, ITM)

    # 
    # #height = image1.shape[0]    #세로 픽셀 수
    # #width = image1.shape[1]    #가로 픽셀 수
    # #absofD = cv2.mean(different)
    # #minlight = 100
    # ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)
    
    
    # ret, mask = FB107_utilities.difference_2images(fullnames[i], fullnames[i+1], minlight)
    # print("type(ret): {}".format(type(ret)))
    # print("type(mask): {}".format(type(mask)))
    
    # processing_log += "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".\λ ℉
    #     format(fullnames[i], aaa, bbb, bbb, time.strftime('%Y-%m-%d %H:%M:%S'))

print('#' * 60)
with open('{0}{1}'.format(save_dir_name, processing_log_fname), 'w') as f:
    f.write(processing_log)