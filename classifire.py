import os  # shutil模块主要是用于拷贝文件
import shutil
import csv



router = './audio_train'

# 取得目录下的文件名称
# files_list = os.listdir(path)

# 取得python脚本的名字
# __file__是取得当前脚本路径,如果路径是“\anaconda3\python”这样的格式，则要使用“\\”做切分
#py_name = __file__.split('/')[-1]

# 開啟 CSV 檔案
with open('train.csv', newline='') as csvfile:

  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)
  #print(rows)

  # listen = [air_conditioner, car_horn, children_playing, dog_bark, drilling, enginge_idling, gun_shot, jackhammer, siren, street_music]
  
  # 以迴圈輸出每一列
  for row in rows:
    try:
      files = '{}/{}'.format(router,row[0]) #檔案名稱路徑
      
      classifire  = '{}/{}/'.format(router,row[1]) #分類資料夾路徑
      # print(files)
      # classifire2 = row[1]
      # print(classifire)
      #  如果没有某个格式的文件夹，则创建这个文件夹
      if not os.path.exists(classifire):
          os.mkdir(classifire)
      
      shutil.move(files,classifire)
      # print(classifire)
    except:
      continue



# for file in files_list:
#     # 如果是文件是当前执行的py脚本，则跳过
#     # if file == py_name:
#     #     continue
#     # 如果当前文件格式不是一个文件如“.”，则跳过
#     if not os.path.isfile(file):
#         continue
 
#     # 取得当前文件名称的格式，（切分文件名，取最后的列表元素）
#     # file_type = file.split('.')[-1]
#     # 如果没有某个格式的文件夹，则创建这个文件夹
#     # if not os.path.exists(file_type):
#     #     os.mkdir(file_type)
 
#     # 获取当前路径
#     path = os.getcwd()
#     # 获取分类文件夹路径
#     subdir = os.path.join(path,'%s'%file_type)
#     # 进入分类文件夹
#     os.chdir(subdir)
#     if os.path.exists(file):
#         # 如果文件夹存在当前文件，则跳过
#         continue
#     else:
#         # 返回之前文件夹进行归类
#         os.chdir(path)
#         # shutil.move(源文件，指定路径):递归移动一个文件
#         shutil.move(file,file_type)