import time, os, sys, cv2, numpy
import FB107_utilities as FB
import shutil
from datetime import datetime
from dateutil.relativedelta import relativedelta

processing_Date = '2021-10-04'
save_Dir_Name = '../SAVE/'
result_Dir_Name = '../result/'
FB_Dir_Name = 'Fireball'
Cloud_Dir_Name = 'Cloud'
Plane_Dir_Name = 'Plane'
Default_Dir_Name = 'Default'
Get_Dir_Name = 'statistics_result_'

Location_csv = "%s%s%s.csv" % (result_Dir_Name, Get_Dir_Name, processing_Date)

# -------------------------------------------------------------------------
def getCurrentDate():
# --------------------------------------------------------------------------
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

# --------------------------------------------------------------------------
def getYYYYMMDDHHMISS():
# --------------------------------------------------------------------------
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

# -------------------------------------------------------------------------------
def calcYYYYMMDDHHMISS(YYYYMMDDHHMISS, Sec):
# -------------------------------------------------------------------------------
    OldTime = time.mktime(time.strptime(YYYYMMDDHHMISS, "%Y%m%d%H%M%S"))
    NewTime = OldTime + Sec
    NewYYYYMMDDHHMISS = time.strftime("%Y%m%d%H%M%S", time.localtime(NewTime))
    return NewYYYYMMDDHHMISS

# --------------------------------------------------------------------------
def diffSecYYYYMMDDHHMISS(DT1, DT2):
# --------------------------------------------------------------------------
    time1 = time.mktime(time.strptime(DT1, "%Y%m%d%H%M%S"))
    time2 = time.mktime(time.strptime(DT2, "%Y%m%d%H%M%S"))
    sec = int(time1 - time2)
    return sec

# --------------------------------------------------------------------------
def cvtToFieldYYYYMMDDHHMISS(YYYYMMDDHHMISS):
# --------------------------------------------------------------------------
    YYYY = YYYYMMDDHHMISS[:4]
    MM = YYYYMMDDHHMISS[4:6]
    DD = YYYYMMDDHHMISS[6:8]
    HH = YYYYMMDDHHMISS[8:10]
    MI = YYYYMMDDHHMISS[10:12]
    SS = YYYYMMDDHHMISS[12:14]
    return YYYY, MM, DD, HH, MI, SS


# --------------------------------------------------------------------------
def getFiles(YYYY, MM, DD, HH, MI):
# --------------------------------------------------------------------------
    Dir = './%s/%s/%s/%s' % (YYYY, MM, DD, HH)
    ret = ""

    for file in os.listdir(Dir):

        f = file.split('-')
        HHMISS = f[2]
        MINUTE = HHMISS[2:4]
        if MINUTE == MI:
            ret.append(file)

    return ret


# --------------------------------------------------------------------------
def isFireBall(file):
# --------------------------------------------------------------------------
    if True:
        return True
    else:
        return False


###(유성인지 아닌지 판별)
"""
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
"""


# --------------------------------------------------------------------------
def updateLog(data):
# --------------------------------------------------------------------------
    logDir = "../log.txt"
    f = open(logDir, 'a')
    f.write(data)
    f.write('\n')
    f.close()

# --------------------------------------------------------------------------
def moveFile(fromDir, toDir, fileName, code):
# --------------------------------------------------------------------------

    From = "%s/%s" % (fromDir,fileName)
    To = "%s/%s" % (toDir, fileName)

    if not os.path.exists(toDir):
        os.makedirs(toDir, exist_ok = True)

    try:
        fi = open(From, 'rb')
        dat = fi.read()
        fi.close()
    except Exception as err:
        updateLog("Error in opening file : [%s]" % From)
        print(err)
        return

    try:
        fo = open(To, 'wb')
        fo.write(dat)
        fo.close()
    except Exception as err:
        updateLog("Error in writing filr : [%s]" % To)
        return

    updateLog("Moved Successful!!! [%s], Code : %s" % (fileName, code))

# --------------------------------------------------------------------------
def init():
# --------------------------------------------------------------------------
    YYYYMMDDHHMISS = getYYYYMMDDHHMISS()
    YYYYMMDD = YYYYMMDDHHMISS[:8]
    HHMISS = YYYYMMDDHHMISS[8:]
    updateLog("[%s-%s] : Running on %s" % (YYYYMMDD, HHMISS, Location_csv))

# --------------------------------------------------------------------------
def main():
# --------------------------------------------------------------------------

    init()

    f = open(Location_csv, 'rb')
    dat = f.read()
    Data = dat.decode().split('\n')
    Data = Data[1:]

    length = len(Data)-2
    infos = []
    for i in range(length):
        Data[i] = Data[i].split(',')
        print(Data[i][1])
    ct = [0,0,0]
    for i in range(length):
        try:
            fileName = Data[i][1]
            Code = Data[i][4]
            if int(float(Code)) > 50:
                Code = 2
            elif int(float(Code)) > 20:
                Code = 0
            else:
                Code = 1
            codeList = ["FB", "Default", "Cloud"]
            if int(Code) >= 0 and int(Code) < len(codeList):
                code = codeList[int(Code)]
            else:
                updateLog("Error in receiving code")

            ct[int(Code)] += 1
            fileNames = fileName.split('-')
            YYYY=fileNames[1][:4]
            MM=fileNames[1][4:6]
            DD=fileNames[1][6:8]
            HH=fileNames[2][:2]
            MI=fileNames[2][2:4]
            SS=fileNames[2][4:6]
            processing_Dir = "%s%s/%s/%s/%s" % (save_Dir_Name, YYYY, MM, DD, HH)
            fileName = fileName.split("/")
            fileName = fileName[-1]
            print(fileName)
            if code == "FB":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, FB_Dir_Name, YYYY, MM, DD, HH), fileName, code)
            elif code == "Cloud":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, Cloud_Dir_Name, YYYY, MM, DD, HH), fileName,
                         code)
            elif code == "Plane":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, Plane_Dir_Name, YYYY, MM, DD, HH), fileName,
                         code)
            elif code == "Default":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, Default_Dir_Name, YYYY, MM, DD, HH), fileName,
                         code)
            else:
                updateLog("Error in receiving code")
        except Exception as err:
            print(err)
            continue
    updateLog("")
    updateLog("Task finished!")
    updateLog("Fireballs : "+str(ct[0]))
    updateLog("Clouds : "+str(ct[2]))
    updateLog("Default : "+str(ct[1]))
    updateLog("\n\n")

main()
