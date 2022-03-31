import cv2
import os
import pandas as pd 
import numpy as np
import pymysql
from urllib import parse
import Python_utilities
import FB107_utilities

#########################################
log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))
#########################################

#########################################
# mariaDB info
#########################################
SET_MariaDB = True
if SET_MariaDB == True :
    import pymysql
    db_host = '192.168.0.20'
    db_host = '10.114.0.120'

    db_user = 'modis'
    db_pass = 'Modis12345!'
    db_name = 'MODIS_Aerosol'

    db_user = 'FB107'
    db_pass = 'Gses12345!'
    db_name = 'FB107'

    table_hdf_info = 'SAVE_file_info'

    conn = pymysql.connect(host=db_host, port=3306,
                           user=db_user, password=db_pass, db=db_name,
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cur = conn.cursor()

    q1 = """CREATE TABLE IF NOT EXISTS `{}`.`{}` (
        `id` INT NOT NULL AUTO_INCREMENT ,
        `fullname` VARCHAR(16384) default NULL ,
        `brightness_mean` VARCHAR(16) default NULL ,
        `brightness_std` VARCHAR(16) default NULL ,
        `Line` VARCHAR(5) default NULL ,
    	`EXIF` TEXT default NULL ,
        `Update_DT` TIMESTAMP on update CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
        PRIMARY KEY (`id`)) ENGINE = InnoDB;""".format(db_name, table_hdf_info)
    cur.execute(q1)
    conn.commit()
#########################################

base_drs = ['../SAVE/']

fullnames = []
for dirName in base_drs :
    #dirName = "../Aerosol/MODIS Aqua C6.1 - Aerosol 5-Min L2 Swath 3km/2002/185/"
    try :
        fullnames.extend(Python_utilities.getFullnameListOfallFiles("{}".format(dirName)))
    except Exception as err :
        #Python_utilities.write_log(err_log_file, err)
        print(err)
        continue
fullnames = sorted(fullnames)
#########################################

for fullname in fullnames :
    #fullname = fullnames[10]
    if fullname[-4:].lower() == ".jpg":
        print("Starting: {}".format(fullname))
        fullname_el = fullname.split("/")
        filename_el = fullname_el[-1].split("/")

        try:
            # cur = conn.cursor()

            q2 = """SELECT `id` FROM `{}`.`{}` WHERE `fullname`= '{}';""".format(db_name, table_hdf_info, fullname)
            q2_sel = cur.execute(q2)
            print("q2: {}".format(q2))

            '''
            q3 = """SELECT `id` FROM `{}`.`{}` WHERE `histogram_png`= '{}{}_hist.png';""".format(db_name,
                            table_hdf_info, fullname[:(fullname.find(fullname_el[-1]))],
                            fullname_el[-1][:-4])
            q3_sel = cur.execute(q3)
            print("q3: {}".format(q3))
            print("q3_sel: {}".format(q3_sel))
    
            q4 = """SELECT `id` FROM `{}`.`{}` WHERE `fullname`= '{}';""".format(db_name,
                            table_hdf_info, fullname)
            q4_sel = cur.execute(q4)
            print("q3: {}".format(q4))
            print("q3_sel: {}".format(q4_sel))
            '''

            image_color = cv2.imread("{}".format(fullname))
            image_hsv = cv2.cvtColor(image_color, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(image_hsv)
            brightness_mean, brightness_std = np.mean(v), np.std(v)

            if q2_sel == 0:
                print("q2_sel: {}".format(q2_sel))
                q3_insert = """INSERT INTO `{0}`.`{1}`                                         
                                    (`fullname`, `brightness_mean`, `brightness_std`) 
                                    VALUES ('{2}', '{3:.03f}', '{4:.03f}');""".format(db_name, table_hdf_info, fullname,
                                                        brightness_mean, brightness_std)

                cur.execute(q3_insert)

            else:
                print("q2_sel: {}".format(q2_sel))
                q3_update = """UPDATE `{0}`.`{1}` 
                                SET `fullname` = '{2}' , 
                                `brightness_mean` = '{3}', 
                                `brightness_std` = '{4}'  
                                WHERE `{1}`.`id` = {5};""".format(db_name, table_hdf_info, fullname,
                                                          brightness_mean, brightness_std)
                print("q3_update: {}".format(q3_update))
                cur.execute(q3_update)
            conn.commit()
        except Exception as err :
            #Python_utilities.write_log(err_log_file, err)
            print("err with {}".format(fullname))
            continue
  