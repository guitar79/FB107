import cv2
import os
import pandas as pd 
import numpy as np
import FB107_utilities

log_file = os.path.basename(__file__)[:-3]+".log"
err_log_file = os.path.basename(__file__)[:-3]+"_err.log"
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))    

base_dir_name = '../SAVE/'
save_dir_name = "../result_Kevin/"
thumbnail_dir_name = "../thumbnail_Kevin/"
from datetime import datetime

proc_dates = []
#make processing period tuple
from dateutil.relativedelta import relativedelta
start_DT = datetime(2020, 5, 1) #convert startdate to date type
#end_DT = datetime(year+1, 1, 1)
end_DT = datetime.now()
k=0
date1 = start_DT
date2 = start_DT

while date2 < end_DT :
    k += 1
    date2 = date1 + relativedelta(days=1)
    date = (date1, date2, k)
    proc_dates.append(date)
    date1 = date2

print(len(proc_dates))

for proc_date in proc_dates[:]:
    #processing_date_str = '2021-10-03'
    #processing_DT = datetime.fromisoformat(processing_date_str)
    #processing_DT1 = processing_DT + relativedelta(hours=12)
    #processing_DT2 = processing_DT + relativedelta(hours=36)
    
    processing_DT1 = proc_date[0] + relativedelta(hours=12)
    processing_DT2 = proc_date[1] + relativedelta(hours=12)
    processing_date_str = processing_DT1.strftime('%Y-%m-%d')
        
    #processing_DT1.strftime('%Y-%m-%d %H:%M')
    #processing_dir_name = "{}{:04d}/{:02d}/{:02d}/".format(base_dir_name, processing_DT1.year, processing_DT2.month, processing_DT2.day)
                            
    processing_dir_names = ["{}{:04d}/{:02d}/{:02d}/".format(base_dir_name, processing_DT1.year, processing_DT1.month, processing_DT1.day),
                            "{}{:04d}/{:02d}/{:02d}/".format(base_dir_name, processing_DT2.year, processing_DT2.month, processing_DT2.day)]
    
    processing_log_fname = "statistics_result_{}.csv".format(processing_date_str)
    
    fullnames = []
    for processing_dir_name in processing_dir_names :
        try : 
            fullnames.extend(FB107_utilities.getFullnameListOfallFiles(processing_dir_name))
        except Exception as err :
            #FB107_utilities.write_log(err_log_file, err)
            print(err)
            continue  
    
    if len(fullnames) == 0 :
        print("There is no files...")
    else : 
        df_new = pd.DataFrame({'fullname':fullnames})
        
        #jpg만 남기고 지우기
        df_new = df_new[df_new.fullname.str.contains(".JPG")] 
        
        for idx, row in df_new.iterrows():
            df_new.at[idx, "DT"] = FB107_utilities.fullname_to_DT_str_for_SAVE(df_new.loc[idx, "fullname"])
        df_new['DT'] =pd.to_datetime(df_new.DT)
        df_new.sort_values(by='DT')
        #df_new.index = df_new['DT']
        
        df_new = df_new[(df_new['DT'] >= processing_DT1.strftime('%Y-%m-%d %H:%M')) & (df_new['DT'] < processing_DT2.strftime('%Y-%m-%d %H:%M'))]
        
        #make list all files
        if os.path.exists('{0}{1}'.format(save_dir_name, processing_log_fname)) :
            df_old = pd.read_csv('{0}{1}'.format(save_dir_name, processing_log_fname), sep=',')
            #make list all files
            if len(df_new) == len(df_old) :
                df = df_old
        else :
            df = df_new
        
        df = df_new
        print("df:\n{}".format(df))    
        
        minlight = 100
        
        for idx, row in df.iterrows():
            try : 
                print(row["fullname"])
                fullname_el = row["fullname"].split("/")
                #df.at[idx, "fullname_dt"] = MODIS_hdf_utilities.fullname_to_datetime_for_DAAC3K(df.loc[idx, "fullname"])
                image1_Gray = cv2.imread("{}".format(df.loc[idx, "fullname"]), cv2.IMREAD_GRAYSCALE )  #직전에 촬영된 이미지 불러오기
                image2_Gray = cv2.imread("{}".format(df.loc[idx+1, "fullname"]), cv2.IMREAD_GRAYSCALE )  #방금 촬영된 이미지 불러오기
                different = cv2.absdiff(image1_Gray, image2_Gray) #둘에서 달라진 점을 계산
                #print("debug #1")
                ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)
                df.at[idx, "sum(sum(mask))"] = sum(sum(mask))
                print('idx, sum(sum(mask)): {}, {}'.format(idx, sum(sum(mask))))
                
                image1_color = cv2.imread("{}".format(df.loc[idx, "fullname"]))
                #print("debug #2")
                
                image1_hsv = cv2.cvtColor(image1_color, cv2.COLOR_BGR2HSV)
                #print("debug #3")
                
                h, s, v = cv2.split(image1_hsv)
                #print("debug #4")
                df.at[idx, "brightness_mean"] = np.mean(v)
                print('idx, brightness_mean: {}, {}'.format(idx, np.mean(v)))
                
                df.at[idx, "brightness_std"] = np.std(v)
                print('idx, brightness_std: {}, {}'.format(idx, np.std(v)))
                image1_color.shape[0]/4
                image1_color_thumnail = cv2.resize(image1_color, 
                                                   (int(image1_color.shape[1]/4), int(image1_color.shape[0]/4)),
                                                   interpolation=cv2.INTER_AREA)
                image1_color_thumnail = cv2.putText(image1_color_thumnail,
                                                    "difference:{}\nbrightness mean: {:.02f}, std:{:.02f}".format(sum(sum(mask)), np.mean(v), np.std(v)), 
                                                    (100, 100), 
                                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                                    0.5, (255, 255, 255))
                cv2.imwrite("{}{}".format(thumbnail_dir_name, fullname_el[-1]), image1_color_thumnail)
            
            except Exception as err :
                #FB107_utilities.write_log(err_log_file, err)
                print(err)
                continue  
        
        df.to_csv('{0}{1}'.format(save_dir_name, processing_log_fname))
        #         .format(fullnames[i], sum(sum(mask)))

  