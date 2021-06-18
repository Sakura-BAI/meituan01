# _*_coding:utf-8 _*_
import pandas as pd
import numpy as np
import os
import time


#  主要是简单合并excel， 太多了。麻烦的很，不想搞 。
# 地址
# 修改一下，换一个新的保存地址。最好加上时间

class yuchuli:
    # 初始化数据
    def __init__(self):
        self.pd = pd
        # 开始地址
        self.path = r"C:\Users\1\Desktop\工作\202106\test"
        # 输出保存地址
        self.save = r"C:\Users\1\Desktop\工作\202106\save"
        # 时间格式
        self.tim = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    # 数据合并
    def get_data(self):
        filenames = os.listdir(self.path)
        df = self.pd.DataFrame()
        for i in filenames:
            #     print (path + '\\'+ i )   -- 验证地址
            data = pd.read_excel(self.path + '\\' + i)
            df = df.append(data)
        return df

    # 数据处理
    def deal_data(self):
        df = self.get_data()
        str = 'h'
        # 去除重复
        df1 = df.drop_duplicates()
        # 增加筛选 特定文档。 不想筛选就注释掉。
        if '营业状态' in df.columns:
            str = '营业状态'
            df1 = df1[df1['营业状态'].isin(['正常营业', '未上线', '歇业'])]
            a = 1

        return df1, str

    # 保存数据
    def save_data(self):
        #  这样可以少跑一次速度更快。获取数据存起来。
        data = self.deal_data()
        # 数组
        data1 = data[0]
        # 营业状态
        str = data[1]
        # str = 'h'
        # if '营业状态' in data.columns:
        #     str = '筛选过后'
        addr = self.save + '\\' + str + self.tim + '.xlsx'
        print(addr)
        data1.to_excel(addr)


if __name__ == '__main__':
    yuchuli().save_data()
    a = 1
