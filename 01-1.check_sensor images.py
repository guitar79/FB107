import os
from datetime import datetime
import time
import FB107_utilities

base_dir_name = '../STIL/'

fullnames = FB107_utilities.getFullnameListOfallFiles(base_dir_name)

#for fullname in fullnames :
#    fullname = fullnames[0]
#    fullname_el = fullname.split("/")
#    filename_el = fullname_el[-1].split("-")
    
for i in range(len(fullnames)-1) :
    fullname = fullnames[0]
    fullname_el = fullname.split("/")
    filename_el = fullname_el[-1].split("-")
    
    fullnames[i+1]
    fullnames[i]
    
    Imgfirst = cv2.imread('{}'.format(fullnames[i]))
    Imgsecond = cv2.imread('{}'.format(fullnames[i+1]))


    
    processing_log = "#This file is created using Python : https://github.com/guitar79/MODIS_hdf_Python\n"
    processing_log += "filename, BrightR(mean), BrightR(std), BrightR(max), BrightR(min), BrightG(mean), BrightG(std), BrightG(max), BrightG(min),  BrightB(mean), BrightB(std), BrightB(max), BrightB(min), ,star No, FB, proc time\n".format(filename, aaa, bbb, bbb)
    processing_log += "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(filename, aaa, bbb, bbb, time.strftime('%Y-%m-%d %H:%M:%S'))
           
            
            
    debuging = False
    add_log = True
    if add_log == True:
        log_file = "{}_file_rename.log".format(ext_name)

    save_base_dir_name = "../../{}file/".format(ext_name)

    image_Num = 0
    for fullname in fullnames[:]:
    #fullname = fullnames[10]
        if fullname[-4:].lower() == ".{}".format(ext_name) :
            image_Num += 1
            try :
                print("Trying the file :\n{}".format(fullname))
                image_datetime = photo_utilities.get_image_datetime_str(fullname)
                image_ModelID = photo_utilities.get_image_Model_name(fullname).replace(' ','')
                image_Software = photo_utilities.get_image_Software(fullname)

                save_dir_name = '{0}{1}/{1}-{2}-{3}_{4}_{5}/'\
                          .format(save_base_dir_name, image_datetime[0:4], \
                          image_datetime[4:6], image_datetime[6:8], image_ModelID, image_Software)

                while not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name)
                    print ("*"*80)
                    print ("{0} is created".format(save_dir_name))