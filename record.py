"""
@文件名：record.py
@描述：
@作者：武者小路
@时间：2022/2/15 9:24
@联系方式：wuzhexiaolua
@Copyright：©武汉大学测绘遥感信息工程国家重点实验室UBDR小组
"""
import time
from datetime import datetime
import pandas as pd
import math
from datetime import datetime

class Record:
    """
    @ClassName：Record
    @Description：
    用来记录签到数据
    用来记录天的数据
    @Author：wuzhexiaolu
    """
    def __init__(self):
        # 签到和签退时间
        self.sign_in_time = 0
        self.sign_out_time = 0

        # 记录天的总结数据
        self.df_task = 0
        self.user = 0
        self.date = 0
        self.stime = 0
        self.etime = 0
        self.learn_time = 0
        self.n = 0
        self.complete_n = 0
        # 完成的次数/总次数
        self.complete_p = 0
        # 有效学习时间/在岗时间
        self.time_p = 0
        # 在岗时间
        self.work_time = 0
        # 今日事件
        self.event = 0

    def compute_time(self, task_path):
        self.df_task = pd.read_csv(task_path, sep=',')
        # 获取任务表里面最近一条的日期
        self.user = self.df_task.loc[len(self.df_task)-1, 'user']
        self.date = self.df_task.loc[len(self.df_task)-1, 'date']
        df_date = self.df_task.loc[self.df_task.date == self.date]
        self.stime = df_date.iloc[0].stime
        self.etime = df_date.iloc[len(df_date)-1].etime
        self.learn_time = str(pd.to_timedelta(1800 * len(df_date) * pow(10,9)))[-8:]
        self.n = len(df_date)
        self.complete_n = len(df_date.loc[df_date.iscomplete == 1])
        self.complete_p = round(self.complete_n / self.n, 3)

        # 计算在岗时间，及时间利用率
        timedelta = pd.to_datetime(self.etime) - pd.to_datetime(self.stime)
        self.work_time = str(timedelta)[-8:]
        self.time_p = round(pd.to_timedelta(1800 * len(df_date) * pow(10,9)) / timedelta, 3)

    def sign_in(self):
        self.sign_in_time = datetime.now()

    def sign_out(self):
        self.sign_out_time = datetime.now()
        return 1

    def to_df(self, df_day):
        df_day.loc[len(df_day)] = [self.user, self.date, self.stime, self.etime
            , self.learn_time, self.n, self.complete_n
            , self.time_p, self.complete_p, self.work_time, self.event]
        return df_day