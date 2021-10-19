import time, os, sys, cv2, numpy
import FB107_utilities as FB


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


# --------------------------------------------------------------------------
def updateLog(data):
# --------------------------------------------------------------------------
    logDir = ".log.txt"
    f = open(logDir, 'a')
    f.write(data)
    f.close()

# --------------------------------------------------------------------------
def moveFile(fromDir, toDir, fileName, code):
# --------------------------------------------------------------------------

    From = "%s/%s" % (fromDir,fileName)
    To = "%s/%s" % (toDir, fileName)

    if not os.path.exists(toDir):
        os.mkdir(toDir)

    try:
        fi = open(From, 'rb')
        dat = fi.read().encode("hex")
        fi.close()
    except:
        updateLog("Error in opening file : [%s]" % From)
        return

    try:
        fo = open(To, 'wb')
        fo.write(dat)
        fo.close()
    except:
        updateLog("Error in writing filr : [%s]" % To)
        return

    updateLog("%s, %s" % (fileName, code))


# --------------------------------------------------------------------------
def main():
# --------------------------------------------------------------------------

    save_Dir_Name = '../SAVE/'
    result_Dir_Name = '../result/'
    FB_Dir_Name = 'Fireball'
    Cloud_Dir_Name = 'Cloud'
    Plane_Dir_Name = 'Plane'
    Default_Dir_Name = 'Default'

    processing_Date = '2021-10-04'
    YYYY=processing_Date[:4]
    MM=processing_Date[5:7]
    DD=processing_Date[8:10]

    processing_Dir = "%s%s/%s/%s" % (save_Dir_Name,YYYY,MM,DD)

    N = input()
    length = int(N)
    infos = []
    for i in range(length):
        A = input().split(',')
        A[1]=A[1][1:]
        infos.append([A[0][-1], A[1]])

    for i in range(length):
        fileName = infos[i][0]
        Code = infos[i][1]
        codeList = ["FB", "Default"]
        if int(Code) >= 0 and int(Code) < len(codeList):
            code = codeList[int(Code)]
        else:
            updateLog("Error in receiving code")

        if code == "FB":
            moveFile(processing_Dir,"%s%s/%s/%s/%s" % (result_Dir_Name, FB_Dir_Name, YYYY, MM, DD), fileName, code)
        elif code == "Cloud":
            moveFile(processing_Dir,"%s%s/%s/%s/%s" % (result_Dir_Name, Cloud_Dir_Name, YYYY, MM, DD), fileName, code)
        elif code == "Plane":
            moveFile(processing_Dir,"%s%s/%s/%s/%s" % (result_Dir_Name, Plane_Dir_Name, YYYY, MM, DD), fileName, code)
        elif code == "Default":
            moveFile(processing_Dir,"%s%s/%s/%s/%s" % (result_Dir_Name, Default_Dir_Name, YYYY, MM, DD), fileName, code)
        else:
            updateLog("Error in receiving code")

main()
