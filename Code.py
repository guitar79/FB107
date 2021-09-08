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
# --------------------------------------------------------------------------
###(유성인지 아닌지 판별)

# --------------------------------------------------------------------------
def moveFile(file,isFB):
# --------------------------------------------------------------------------
    print('move')
    header = ""
    if isFB == True:
        header = "/FB"
        logupdate = "[%s/%s/%s %s:%s:%s] A fireball found"
    else:
        header = "/NotFB"
        logupdate = "[%s/%s/%s %s:%s:%s] Fireball not found"
    fileName = file.split('-')
    YYYYMMDD = fileName[1]
    HHMISS = fileName[2]
    YYYY = fileName[1][0:4]
    MM = fileName[1][4:6]
    DD = fileName[1][6:8]
    HH = fileName[2][0:2]
    MI = fileName[2][2:4]
    SS = fileName[2][4:6]
    logDir = '.log.txt'

    Dir='.%s/%s/%s/%s/%s/FB107L-%s%s%s-%s%s%s-KST.JPG' % (header,YYYY,MM,DD,HH,YYYY,MM,DD,HH,MI,SS)


# --------------------------------------------------------------------------
def main():
# --------------------------------------------------------------------------
    curTime = getYYYYMMDDHHMISS()
    YYYY, MM, DD, HH, MI, SS = cvtToFieldYYYYMMDDHHMISS(calcYYYYMMDDHHMISS(curTime,-60))
    TargetFiles = getFiles(YYYY, MM, DD, HH, MI)
    for file in TargetFiles:
        if isFireBall(file) == True:
            moveFile(file,True)
        else:
            moveFile(file,False)


main()