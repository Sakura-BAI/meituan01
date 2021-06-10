# _*_coding:utf-8 _*_
import pandas as pd
import numpy as np
import os
import time

# 地址


path = r"C:\Users\1\Desktop\工作\202106\test"

# 当前时间
time = time.strftime("%Y-%m-%d", time.localtime())

print(path + '\\' + time + '.xlsx')
# print(a)

filenames = os.listdir(path)
df = pd.DataFrame()
# 遍历需要文件夹所有文件

for i in filenames:
    #     print (path + '\\'+ i )   -- 验证地址
    data = pd.read_excel(path + '\\' + i)
    df = df.append(data)

adres = path + '\\' + time + '.' + 'xlsx'

df.to_excel(adres)

