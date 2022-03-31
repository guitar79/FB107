import cv2
import os
import pandas as pd
import numpy as np
import FB107_utilities


def getMAD(data):  # 중간값 평균편차
    return np.mean(np.absolute(data - np.median(data)))


log_file = os.path.basename(__file__)[:-3] + ".log"
err_log_file = os.path.basename(__file__)[:-3] + "_err.log"
print("log_file: {}".format(log_file))
print("err_log_file: {}".format(err_log_file))

base_dir_name = '../SAVE/'

from datetime import datetime
from dateutil.relativedelta import relativedelta

processing_date_str = '2021-07-01'
processing_DT = datetime.fromisoformat(processing_date_str)
processing_DT1 = processing_DT + relativedelta(hours=12)
processing_DT2 = processing_DT + relativedelta(hours=36)
# processing_DT1.strftime('%Y-%m-%d %H:%M')

# processing_dir_name = "{}{:04d}/{:02d}/{:02d}/".format(base_dir_name, processing_DT1.year, processing_DT2.month, processing_DT2.day)

processing_dir_names = [
    "{}{:04d}/{:02d}/{:02d}/".format(base_dir_name, processing_DT1.year, processing_DT1.month, processing_DT1.day),
    "{}{:04d}/{:02d}/{:02d}/".format(base_dir_name, processing_DT2.year, processing_DT2.month, processing_DT2.day)]
save_dir_name = "../result/"
processing_log_fname = "statistics_result_{}.csv".format(processing_date_str)
thumbnail_dir_name = "../thumbnail_Y/"
point = 300, 300

fullnames = []
for processing_dir_name in processing_dir_names:
    fullnames.extend(FB107_utilities.getFullnameListOfallFiles(processing_dir_name))
df_new = pd.DataFrame({'fullname': fullnames})

# jpg만 남기고 지우기
df_new = df_new[df_new.fullname.str.contains(".JPG")]

for idx, row in df_new.iterrows():
    df_new.at[idx, "DT"] = FB107_utilities.fullname_to_DT_str_for_SAVE(df_new.loc[idx, "fullname"])
df_new['DT'] = pd.to_datetime(df_new.DT)
df_new.sort_values(by='DT')
# df_new.index = df_new['DT']

df_new = df_new[(df_new['DT'] >= processing_DT1.strftime('%Y-%m-%d %H:%M')) & (
            df_new['DT'] < processing_DT2.strftime('%Y-%m-%d %H:%M'))]

# make list all files
if os.path.exists('{0}{1}'.format(save_dir_name, processing_log_fname)):
    df_old = pd.read_csv('{0}{1}'.format(save_dir_name, processing_log_fname), sep=',')
    # make list all files
    if len(df_new) == len(df_old):
        df = df_old
else:
    df = df_new

df = df_new
print("df:\n{}".format(df))

minlight = 1
k = 0
for idx, row in df.iterrows():
    try:

        print(row["fullname"])
        # df.at[idx, "fullname_dt"] = MODIS_hdf_utilities.fullname_to_datetime_for_DAAC3K(df.loc[idx, "fullname"])
        image1_Gray = cv2.imread("{}".format(df.loc[idx, "fullname"]), cv2.IMREAD_GRAYSCALE)  # 직전에 촬영된 이미지 불러오기
        image2_Gray = cv2.imread("{}".format(df.loc[idx + 1, "fullname"]), cv2.IMREAD_GRAYSCALE)  # 방금 촬영된 이미지 불러오기
        different = cv2.absdiff(image1_Gray, image2_Gray)  # 둘에서 달라진 점을 계산
        # print("debug #1")
        ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)

        df.at[idx, "sum(sum(mask))"] = sum(sum(mask))
        print('idx, sum(sum(mask)): {}, {}'.format(idx, sum(sum(mask))))
        image1_color = cv2.imread("{}".format(df.loc[idx, "fullname"]))
        # print("debug #2")

        image1_hsv = cv2.cvtColor(image1_color, cv2.COLOR_BGR2HSV)
        # print("debug #3")

        h, s, v = cv2.split(image1_hsv)
        # print("debug #4")
        lines = cv2.HoughLinesP(mask, 1, np.pi / 180., 160, minLineLength=300, maxLineGap=30)
        if lines is None: lines = []
        thumbnail = cv2.resize(image1_Gray, dsize=(600, 400))
        print("deb")
        cv2.putText(thumbnail, '{0}, {1}, DOP: {2}, NOBP: {3}, BM: {4}, NOL: {5}'.format(
            round(np.mean(v), 2), round(np.std(v), 3), round(getDOP(v), 3), getNOBP(v), round(np.mean(different), 3),
            len(lines)), (30, 30), 0, 0.4, 255, 1)
        cv2.imwrite('{0}{1}T.png'.format(thumbnail_dir_name, row['fullname'].split('\\')[1].split('.')[0]), thumbnail)
        df.at[idx, "brightness_mean"] = np.mean(v)
        print('idx, brightness_mean: {}, {}'.format(idx, np.mean(v)))


    except Exception as err:
        # FB107_utilities.write_log(err_log_file, err)
        print(err)
        continue

print("end")
exit()
# df.to_csv('{0}{1}'.format(save_dir_name, processing_log_fname))
#         .format(fullnames[i], sum(sum(mask)))


# for i in range(len(fullnames)-1) :
#     #i=0
#     image1 = cv2.imread("{}".format(fullnames[i]), cv2.IMREAD_GRAYSCALE )  #직전에 촬영된 이미지 불러오기
#     image2 = cv2.imread("{}".format(fullnames[i+1]), cv2.IMREAD_GRAYSCALE )  #방금 촬영된 이미지 불러오기
#     different = cv2.absdiff(image1, image2) #둘에서 달라진 점을 계산
#     ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)

#         .format(fullnames[i], sum(sum(mask)))


#
# #height = image1.shape[0]    #세로 픽셀 수
# #width = image1.shape[1]    #가로 픽셀 수
# #absofD = cv2.mean(different)
# #minlight = 100
# ret, mask = cv2.threshold(different, minlight, 255, cv2.THRESH_BINARY)


# ret, mask = FB107_utilities.difference_2images(fullnames[i], fullnames[i+1], minlight)
# print("type(ret): {}".format(type(ret)))
# print("type(mask): {}".format(type(mask)))

# processing_log += "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".\
#     format(fullnames[i], aaa, bbb, bbb, time.strftime('%Y-%m-%d %H:%M:%S'))

# print('#' * 60)
# with open('{0}{1}'.format(save_dir_name, processing_log_fname), 'w') as f:
#     f.write(processing_log)