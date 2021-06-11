# _*_coding:utf-8 _*_
import pandas as pd
import numpy as np
import os
import time

# 这个可以写成一个类，保存文件，获取文件的初始化类。

path = r"C:\Users\1\Desktop\工作\202106\练习文件"

path1 = r"C:\Users\1\Desktop\工作\202106\save"

# 当前时间格式，很有用。
tim = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

filenames = os.listdir(path)
df = pd.DataFrame()
for i in filenames:
    #     print (path + '\\'+ i )   -- 验证地址
    data = pd.read_excel(path + '\\' + i)
    df = df.append(data)

data1 = pd.melt(df, id_vars=['日期'], var_name="城市维度", value_name="数值")

# 总算对了，设置两级索引。这样就不会变。 设置索引 。固定日期和值
data1 = data1.set_index(['日期', '数值'])
# 根据字符切割，故意写开 。其实可以这样写 data1 = data1.set_index(['日期', '数值'])["城市维度"].str.split("-", expand=True)
data1 = data1["城市维度"].str.split("-", expand=True)
# 重置索引，四个都有索引，列转行了。
data2 = data1.reset_index()
# 再度设置索引，需要将指标行转列。
data2 = data2.set_index(['日期', 0, 1])
# 行转列，使用unstack方法。默认是最后一列变为列。 最后一列是指标 。
# 这里的level默认是-1, 表示将最后一级的索引变成列
# # 这里我们不用指定(注意: 索引从0开始), 告诉pandas, 把第一级索引变成列
data4 = data2.unstack()
# 重置索引
data4 = data4.reset_index().rename_axis()

# 地址
addres = path1 + '\\' + 'x' + tim + '.xlsx'

print(addres)

data4.to_excel(addres)
