import os
from datetime import datetime
import time
import cv2
import FB107_utilities

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
processing_log += "fullname, BrightR(mean), BrightR(std), BrightR(max), BrightR(min), BrightG(mean), BrightG(std), BrightG(max), BrightG(min),  BrightB(mean), BrightB(std), BrightB(max), BrightB(min), star No, FB, proc time\n"
#processing_log += "fullname, BrightR(mean), BrightR(std), BrightR(max), BrightR(min), BrightG(mean), BrightG(std), BrightG(max), BrightG(min),  BrightB(mean), BrightB(std), BrightB(max), BrightB(min), star No, FB, proc time\n"

for i in range(len(fullnames)-1)[:10] :

    


    # image1 = cv2.imread("{}".format(img1_fullname), cv2.IMREAD_GRAYSCALE )  #직전에 촬영된 이미지 불러오기
    # image2 = cv2.imread("{}".format(img2_fullname), cv2.IMREAD_GRAYSCALE )  #방금 촬영된 이미지 불러오기
    # different = cv2.absdiff(image1, image2) #둘에서 달라진 점을 계산
    # #height = image1.shape[0]    #세로 픽셀 수
    # #width = image1.shape[1]    #가로 픽셀 수
    # #absofD = cv2.mean(different)
    # #minlight = 100
    # ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)
    
    
    # ret, mask = FB107_utilities.difference_2images(fullnames[i], fullnames[i+1], minlight)
    # print("type(ret): {}".format(type(ret)))
    # print("type(mask): {}".format(type(mask)))
    
    # processing_log += "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".\
    #     format(fullnames[i], aaa, bbb, bbb, time.strftime('%Y-%m-%d %H:%M:%S'))
           
    