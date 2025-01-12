# -*- coding: utf-8 -*-
"""
Spyder Editor
ModuleNotFoundError: No module named 'cv2'
conda install opencv
pip install piexif
ModuleNotFoundError: No module named 'exifread'
pip install exifread
There are only just five functions.
load(filename) - Get exif data as dict.
dump(exif_dict) - Get exif as bytes.
insert(exif_bytes, filename) - Insert exif into JPEG, or WebP.
remove(filename) - Remove exif from JPEG, or WebP.
transplant(filename, filename) - Transplant exif from JPEG to JPEG.
created by guitar79@naver.com
"""
#from datetime import datetime
# from astropy.io import fits


def write_log2(log_file, log_str):
    import os
    with open(log_file, 'a') as log_f:
        log_f.write("{}, {}\n".format(os.path.basename(__file__), log_str))
    return print("{}, {}\n".format(os.path.basename(__file__), log_str))

def write_log(log_file, log_str):
    import time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = '[' + timestamp + '] ' + log_str
    print(msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')

def fullname_to_datetime_for_SAVE(fullname):
    ############################################################
    #for ../SAVE/2021/10/05/00/FB107L-20211005-000011-KST.JPG'
    #
    from datetime import datetime
    fullname_el = fullname.split("/")
    filename_el = fullname_el[-1].split("-")
    #print(filename_el[1][:4], filename_el[1][4:6], filename_el[1][6:8], filename_el[2][:2], filename_el[2][2:4], filename_el[2][4:6])
    return datetime(int(filename_el[1][:4]), int(filename_el[1][4:6]), int(filename_el[1][6:8]), int(filename_el[2][:2]), int(filename_el[2][2:4]), int(filename_el[2][4:6]))

def fullname_to_DT_str_for_SAVE(fullname):
    ############################################################
    #for ../SAVE/2021/10/05/00/FB107L-20211005-000011-KST.JPG'
    #
    fullname_el = fullname.split("/")
    filename_el = fullname_el[-1].split("-")
    #print(filename_el[1][:4], filename_el[1][4:6], filename_el[1][6:8], filename_el[2][:2], filename_el[2][2:4], filename_el[2][4:6])
    return "{}-{}-{} {}:{}:{}".format(filename_el[1][:4], filename_el[1][4:6], filename_el[1][6:8], filename_el[2][:2], filename_el[2][2:4], filename_el[2][4:6])


def difference_2images(img1_fullname, img2_fullname, minlight):
    # 유성체감시네트워크에 적용될, 최종 유성 및 기타 물체 탐지 코드
    # img1_fullname, img2_fullname, 
    # minlight : int
    # import numpy as np
    import cv2
    image1 = cv2.imread("{}".format(img1_fullname), cv2.IMREAD_GRAYSCALE )  #직전에 촬영된 이미지 불러오기
    image2 = cv2.imread("{}".format(img2_fullname), cv2.IMREAD_GRAYSCALE )  #방금 촬영된 이미지 불러오기
    different = cv2.absdiff(image1, image2) #둘에서 달라진 점을 계산
    #height = image1.shape[0]    #세로 픽셀 수
    #width = image1.shape[1]    #가로 픽셀 수
    #absofD = cv2.mean(different)
    #minlight = 100
    ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)
    return ret, mask



def getFullnameListOfallFiles(dirName):
    ##############################################
    # "dirName" 안에 있는 모든 파일을 리스트로 반환 #
    ##############################################
    import os
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = sorted(os.listdir(dirName))
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getFullnameListOfallFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles #list


def getFullnameListOfallsubDirs1(dirName):
    ##############################################
    #
    import os
    allFiles = list()
    for file in sorted(os.listdir(dirName)):
        d = os.path.join(dirName, file)
        allFiles.append(d)
        if os.path.isdir(d):
            allFiles.extend(getFullnameListOfallsubDirs1(d))

    return allFiles


def getFullnameListOfallsubDirs(dirName):
    ##############################################3
    import os
    allFiles = list()
    for it in os.scandir(dirName):
        if it.is_dir():
            allFiles.append(it.path)
            allFiles.extend(getFullnameListOfallsubDirs(it))

    return allFiles


def checkDuplicated_jpg(fullname1, fullname2):
    import cv2
    # pip install opencv-python
    # pip install opencv-contrib-python
    Duplicated_im = False
    try:
        im1 = cv2.imread("{}".format(fullname1))
        im2 = cv2.imread("{}".format(fullname2))

        # 1) Check if 2 images are equals
        if im1.shape == im2.shape:
            # print("The images have same size and channels")
            difference = cv2.subtract(im1, im2)
            b, g, r = cv2.split(difference)

            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                Duplicated_im = True
                # print("The images are completely Equal")

    except:
        print("reading error with {}, {}".format(fullname1, fullname2))
    return Duplicated_im


# for checking time
def print_working_time(cht_start_time):
    from datetime import datetime
    working_time = (datetime.now() - cht_start_time)  # total days for downloading
    return print('working time ::: %s' % (working_time))


def get_image_datetime_str(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'EXIF DateTimeOriginal' in tags:
        image_datetime = tags['EXIF DateTimeOriginal'].values.replace(':', '')
        image_datetime = image_datetime.replace(' ', '-')

    elif 'Image DateTime' in tags:
        image_datetime = tags['Image DateTime'].values.replace(':', '')
        image_datetime = image_datetime.replace(' ', '-')
    else:
        image_datetime = "00000000-000000"

    return image_datetime


def get_image_number(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'MakerNote FileNumber' in tags:
        image_num = tags['MakerNote FileNumber'].printable
    else:
        image_num = "00"
    return image_num


def get_fileInfo_from_heifexif(fullname):
    # Open the file
    import pyheif
    import piexif
    heif_file = pyheif.read(fullname)

    # Retrive the metadata
    for metadata in heif_file.metadata or []:
        if metadata['type'] == 'Exif':
            exif_dict = piexif.load(metadata['data'])
    image_datetime = exif_dict['0th'][306].decode('utf-8').replace(':', '')
    image_datetime = image_datetime.replace(' ', '-')
    camera_company = exif_dict['0th'][271].decode('utf-8')
    camera_model = exif_dict['0th'][272].decode('utf-8').replace(' ', '-')
    image_Software = "-"
    return image_datetime, camera_company, camera_model, image_Software


def get_fileInfo_from_image(fullname):
    fullname_el = fullname.split(".")
    if fullname_el[-1].lower() == "heic":
        # Open the file
        import pyheif
        import piexif
        heif_file = pyheif.read(fullname)

        # Retrive the metadata
        for metadata in heif_file.metadata or []:
            if metadata['type'] == 'Exif':
                exif_dict = piexif.load(metadata['data'])
        image_datetime = exif_dict['0th'][306].decode('utf-8').replace(':', '')
        image_datetime = image_datetime.replace(' ', '-')
        camera_company = exif_dict['0th'][271].decode('utf-8')
        camera_model = exif_dict['0th'][272].decode('utf-8').replace(' ', '-')
        image_Software = "-"

    elif fullname_el[-1].lower() == "cr2" or fullname_el[-1].lower() == "jpg":
        import exifread
        f = open(fullname, 'rb')
        tags = exifread.process_file(f)
        f.close()
        ##########################################################
        if 'EXIF DateTimeOriginal' in tags:
            image_datetime = tags['EXIF DateTimeOriginal'].values.replace(':', '')
            image_datetime = image_datetime.replace(' ', '-')

        elif 'Image DateTime' in tags:
            image_datetime = tags['Image DateTime'].values.replace(':', '')
            image_datetime = image_datetime.replace(' ', '-')
        else:
            image_datetime = "00000000-000000"
        ##########################################################

        if 'Image Make' in tags and 'Image Model' in tags:
            camera_model = tags['Image Make'].printable.replace(' ', '') \
                           + tags['Image Model'].printable.replace(' ', '')
        elif 'MakerNote ModelID' in tags:
            camera_model = tags['MakerNote ModelID'].printable.replace(' ', '')
        else:
            camera_model = '-'
        ##########################################################
        if 'Image Software' in tags:
            image_Software = tags['Image Software'].printable.replace(' ', '')
        else:
            image_Software = '-'
        if 'ACDSystems' in image_Software:
            image_Software = 'ACDSystems'

        image_Software = image_Software.replace('DigitalPhotoProfessional', 'DPP')

    return image_datetime, camera_company, camera_model, image_Software


def get_image_Model_name(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'Image Make' in tags and 'Image Model' in tags:
        image_ModelID = tags['Image Make'].printable.replace(' ', '') \
                        + tags['Image Model'].printable.replace(' ', '')

    elif 'MakerNote ModelID' in tags:
        image_ModelID = tags['MakerNote ModelID'].printable.replace(' ', '')

    else:
        image_ModelID = '-'
    image_ModelID = image_ModelID.replace('CanonCanon', 'Canon')
    image_ModelID = image_ModelID.replace('/', '')
    image_ModelID = image_ModelID.replace('\\', '')
    image_ModelID = image_ModelID.replace('EASTMANKODAKCOMPANYKODAKDC3400ZOOMDIGITALCAMERA', 'KODAK_DC3400')
    image_ModelID = image_ModelID.replace('OLYMPUSOPTICALCO.,LTDC3100Z,C3020Z', 'OLYMPUS_C3100Z')
    image_ModelID = image_ModelID.replace('OLYMPUSCORPORATIONC-5000Z', 'OLYMPUS_C5000Z')
    image_ModelID = image_ModelID.replace('CanonEOSKissDigitalN', 'CANON_EOS-KissN')
    image_ModelID = image_ModelID.replace('CanonEOS350DDIGITAL', 'CANON_EOS-350D')
    image_ModelID = image_ModelID.replace('CanonEOS400DDIGITAL', 'CANON_EOS-400D')
    image_ModelID = image_ModelID.replace('CanonEOS', 'CANON_EOS')
    image_ModelID = image_ModelID.replace('EOS5DMarkII', 'EOS-5DMarkII')
    image_ModelID = image_ModelID.replace('EOS650D', 'EOS-650D')
    image_ModelID = image_ModelID.replace('CanonPowerShotS230', 'CANON_S230')
    image_ModelID = image_ModelID.replace('CanonPowerShotG', 'CANON_G')
    image_ModelID = image_ModelID.replace('CanonDIGITALIXUS50', 'CANON_IXUS50')
    image_ModelID = image_ModelID.replace('CanonIXYDIGITAL800IS', 'CANON_IXY800IS')
    image_ModelID = image_ModelID.replace('SONYDCR-TRV17', 'SONY_DCR-TRV17')
    image_ModelID = image_ModelID.replace('SONYCYBERSHOT', 'SONY_CYBERSHOT')
    image_ModelID = image_ModelID.replace('SONYDSC', 'SONY_DSC')
    image_ModelID = image_ModelID.replace('SONYNEX-5N', 'SONY_NEX-5N')
    image_ModelID = image_ModelID.replace('SONYILCE', 'SONY_ILCE')
    image_ModelID = image_ModelID.replace('NIKONE', 'NIKON_E')
    image_ModelID = image_ModelID.replace('NIKONCORPORATIONNIKOND', 'NIKON_D')
    image_ModelID = image_ModelID.replace('SAMSUNGELECTRONICSVM-C630', 'SAMSUNG_SVM-C630')
    image_ModelID = image_ModelID.replace('SAMSUNGTECHWINCO.,LTDDigimaxV5KenoxV5', 'SAMSUNG_DigimaxV5')
    image_ModelID = image_ModelID.replace('SamsungTechwinDigimax530KENOXD530', 'SAMSUNG_Digimax530')
    image_ModelID = image_ModelID.replace('SAMSUNGES95', 'SAMSUNG-ES95')
    image_ModelID = image_ModelID.replace('SAMSUNGWB150WB150FWB,...]', 'SAMSUNG_WB150')
    image_ModelID = image_ModelID.replace('SAMSUNGSM', 'SAMSUNG_SM')
    image_ModelID = image_ModelID.replace('SAMSUNGEK', 'SAMSUNG_EK')
    image_ModelID = image_ModelID.replace('SAMSUNGSH', 'SAMSUNG_SH')
    image_ModelID = image_ModelID.replace('SAMSUNGSSV', 'SAMSUNG_SHV')
    image_ModelID = image_ModelID.replace('SamsungTechwinDigimaxV4', 'SAMSUNG_DigimaxV4')
    image_ModelID = image_ModelID.replace('LGElectronicsLG', 'LG')
    image_ModelID = image_ModelID.replace('PanasonicDMC-LX2', 'PANASONIC_DMC-LX2')
    image_ModelID = image_ModelID.replace('ApplePhone', 'APPLE_iPhone')
    image_ModelID = image_ModelID.replace('Applei', 'APPLE_i')
    image_ModelID = image_ModelID.replace('DJIFC1102', 'DJI_FC1102')
    image_ModelID = image_ModelID.replace('DJIFC6310', 'DJI_FC6310')
    image_ModelID = image_ModelID.replace('XIAOYIYDXJ1', 'XIAOYI_YDXJ1')
    image_ModelID = image_ModelID.replace('PANTECH', 'PANTECH_')

    return image_ModelID


def get_mov_creation_date(fullname):
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata
    parser = createParser(fullname)
    metadata = extractMetadata(parser)
    if 'creation_date' in metadata:
        creation_date = metadata.get('creation_date').strftime("%Y%m%d-%H%M%S")
    else:
        import os.path, time
        from dateutil.parser import parse
        creation_date = parse(time.ctime(os.path.getctime(fullname))).strftime("%Y%m%d-%H%M%S")
    return creation_date


def get_image_Software(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'Image Software' in tags:
        image_Software = tags['Image Software'].printable.replace(' ', '')
    else:
        image_Software = '-'

    if 'ACDSystems' in image_Software:
        image_Software = 'ACDSystems'
    image_Software = image_Software.replace('DigitalPhotoProfessional', 'DPP')
    return image_Software





def bgr2rgb(bgr_image):
    import numpy as np
    RGB = np.zeros((bgr_image.shape[0], bgr_image.shape[1], 3), dtype=np.uint8)
    RGB[:, :, 0] = bgr_image[:, :, 2]
    RGB[:, :, 1] = bgr_image[:, :, 1]
    RGB[:, :, 2] = bgr_image[:, :, 0]
    return RGB


def clahe_equalized(imgs):
    import cv2
    lab = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr


def readJpgPhoto_to_ImagesAndTimes(fullnames):
    # source : https://learnopencv.com/high-dynamic-range-hdr-imaging-using-opencv-cpp-python/
    import exifread
    import numpy as np
    # import rawpy
    import cv2

    images = []
    times = []
    for fullname in fullnames:
        # im = rawpy.imread(fullname)
        im = cv2.imread(fullname)
        images.append(im)

        f = open(fullname, 'rb')
        tags = exifread.process_file(f)
        f.close()
        if 'EXIF ExposureTime' in tags:
            image_ExposureTime = tags['EXIF ExposureTime'].values
        times.append(image_ExposureTime)
    # images = np.array(images, dtype=np.uint8)
    times = np.array(times, dtype=np.float32)
    return images, times
