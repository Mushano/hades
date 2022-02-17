# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：engagement.py
@时间：2022/1/24  10:11
@文档说明:
"""
import pandas as pd
import time

class Engagement:
    """
    @ClassName：Engager
    @Description：遭遇战和副本相关类
    @Author：wuzhexiaolu
    """
    def __init__(self, user, aim):
        self.user = user
        self.date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.stime = time.strftime('%H:%M:%S',time.localtime(time.time()))
        self.etime = 0
        self.task = aim
        self.iscomplete = 0

    def to_df(self, df_task):
        df_task.loc[len(df_task)] = [self.user, self.date, self.stime, self.etime, self.task, self.iscomplete]
        return df_task