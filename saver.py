# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：saver.py
@时间：2022/1/24  9:36
@文档说明:
"""
import pandas as pd
import datetime


class Saver:
    """
    @ClassName：Saver
    @Description：用于保存进度、用户数据等
    @Author：wuzhexiaolu
    @改进方案
        saver不应该一下子就全部把表格读进内存，应该根据使用情况来进行读取
    """
    def __init__(self, user_path, task_path, day_path, sign_in_path):
        self.user_path = user_path
        self.task_path = task_path
        self.day_path = day_path
        self.sign_in_path = sign_in_path

        self.df_user = pd.read_csv(self.user_path, sep=',')
        self.df_task = pd.read_csv(self.task_path, sep=',')
        self.df_day = pd.read_csv(self.day_path, sep=',')
        self.df_sign = pd.read_csv(self.sign_in_path, sep=',')



    def to_csv(self):
        self.df_user.to_csv(self.user_path, index = False)
        self.df_task.to_csv(self.task_path, index=False)

    def to_day_csv(self):
        self.df_day.to_csv(self.day_path, index = False)

    def to_sign_csv(self,rec):
        date = datetime.date.today()
        t_in = rec.sign_in_time.strftime('%H:%M:%S')
        t_out = rec.sign_out_time.strftime('%H:%M:%S')
        self.df_sign.loc[len(self.df_sign)] = [date,t_in,t_out]
        self.df_sign.to_csv('签到表.txt',index = False)




