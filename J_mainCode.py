import time
import os

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

    From = "%s/%s" % (fromDir, fileName)
    To = "%s/%s" % (toDir, fileName)

    if not os.path.exists(toDir):
        os.makedirs(toDir, exist_ok=True)

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
        updateLog("Error in writing file : [%s]" % To)
        print(err)
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
    Data = dat.decode().split('\r\n')
    Data = Data[1:]

    length = len(Data) - 2
    for i in range(length):
        Data[i] = Data[i].split(',')
        print(Data[i])
    for i in range(length):
        try:
            fileName = Data[i][1]
            Code = Data[i][4]
            if int(float(Code)) > 20:
                Code = 0
            else:
                Code = 1
            codeList = ["FB", "Default"]
            if 0 <= int(Code) < len(codeList):
                code = codeList[int(Code)]
            else:
                updateLog("Error in receiving code")

            fileNames = fileName.split('-')
            YYYY = fileNames[1][:4]
            MM = fileNames[1][4:6]
            DD = fileNames[1][6:8]
            HH = fileNames[2][:2]
            processing_Dir = "%s%s/%s/%s/%s" % (save_Dir_Name, YYYY, MM, DD, HH)
            fileName = fileName.split("\\")
            fileName = fileName[1]
            print(fileName)
            if code == "FB":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, FB_Dir_Name, YYYY, MM, DD, HH),
                         fileName, code)
            elif code == "Cloud":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, Cloud_Dir_Name, YYYY, MM, DD, HH),
                         fileName,
                         code)
            elif code == "Plane":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, Plane_Dir_Name, YYYY, MM, DD, HH),
                         fileName,
                         code)
            elif code == "Default":
                moveFile(processing_Dir, "%s%s/%s/%s/%s/%s" % (result_Dir_Name, Default_Dir_Name, YYYY, MM, DD, HH),
                         fileName,
                         code)
            else:
                updateLog("Error in receiving code")
        except Exception as err:
            print(err)
            continue

    updateLog("\n\n")


main()
