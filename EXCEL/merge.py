# _*_coding:utf-8 _*_
import pandas as pd
import numpy as np
import os
import time

#  主要是简单合并excel， 太多了。麻烦的很，不想搞 。
# 地址
# 修改一下，换一个新的保存地址。最好加上时间

path = r"C:\Users\1\Desktop\工作\202106\test"

path1 = r"C:\Users\1\Desktop\工作\202106\save"

# 当前时间格式，很有用。
tim = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
# hour = time.strftime("%H:%M", time.localtime())
# print(path + '\\' + tim + '.xlsx')
# print(a)

filenames = os.listdir(path)
df = pd.DataFrame()
# 遍历需要文件夹所有文件

for i in filenames:
    #     print (path + '\\'+ i )   -- 验证地址
    data = pd.read_excel(path + '\\' + i)
    df = df.append(data)

adres = path1 + '\\' + tim + '.xlsx'

print(adres)
df.to_excel(adres)
