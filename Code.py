import time, os, sys, cv2, numpy


# --------------------------------------------------------------------------
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
        YYYYMMDD = f[1]
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



# --------------------------------------------------------------------------
def moveFile(file,isFB):
# --------------------------------------------------------------------------
    print('move')
    header = ""
    logDir = "./log.txt"
    logupdate=""

    ### 유성이 검출
    if isFB == True:
        header = "/FB"
        logupdate = "[%s/%s/%s %s:%s:%s] A fireball found"
        
    ### 검출 안됨
    else:
        header = "/NotFB"
        logupdate = "[%s/%s/%s %s:%s:%s] Fireball not found"

    ### 로그를 업데이트
    f = open(logDir, 'a')
    f.write(logupdate)

    ### 파일의 이름을 토대로 연, 월, 일, 시간, 분, 초를 찾아냄
    fileName = file.split('-')
    YYYY = fileName[1][0:4]
    MM = fileName[1][4:6]
    DD = fileName[1][6:8]
    HH = fileName[2][0:2]
    MI = fileName[2][2:4]
    SS = fileName[2][4:6]

    ### 새롭게 옮길 파일의 디렉토리
    Dir='.%s/%s/%s/%s/%s/FB107L-%s%s%s-%s%s%s-KST.JPG' % (header,YYYY,MM,DD,HH,YYYY,MM,DD,HH,MI,SS)

    ### move file to Dir



# --------------------------------------------------------------------------
def main():
# --------------------------------------------------------------------------
    curTime = getYYYYMMDDHHMISS()

    ### -60초 전 -> 1분 전에 찍힌 파일들을 검토
    YYYY, MM, DD, HH, MI, SS = cvtToFieldYYYYMMDDHHMISS(calcYYYYMMDDHHMISS(curTime,-60))

    #YYYY/MM/DD/HH 디렉토리에 MI분에 찍힌 사진들을 리스트로 만든 것
    TargetFiles = getFiles(YYYY, MM, DD, HH, MI)


    for file in TargetFiles:
        if isFireBall(file) == True:
            moveFile(file,True)
        else:
            moveFile(file,False)


main()