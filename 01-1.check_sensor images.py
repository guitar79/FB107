import os
from datetime import datetime
import FB107_utilities

base_dir_name = '/mnt/FB107/STIL/'

fullnames = photo_utilities.getFullnameListOfallFiles(base_dir_name)

for ext_name in ext_names :

    # for debugging
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