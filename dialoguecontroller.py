# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：dialoguecontroller.py
@时间：2022/1/24  10:12
@文档说明:
"""
import datetime
import time
import numpy as np
import pandas as pd

from engagement import Engagement


class DialogueController:
    """
    @ClassName：DialogueController
    @Description：用于控制对话过程
    @Author：wuzhexiaolu
    """

    def is_sign_in(self,sign_in_time):
        limit1 = pd.Timestamp('13:00:00')
        limit2 = pd.Timestamp('18:00:00')
        now_time = datetime.datetime.now()
        if (sign_in_time != 0):
            if (now_time < limit1) & (sign_in_time < limit1) :
                # 早上时段
                return 1
            elif (now_time < limit2) & (sign_in_time < limit2) & (sign_in_time > limit1) & (now_time > limit1):
                # 下午时段
                return 1
            elif (now_time > limit2) & (sign_in_time > limit2):
                # 晚上时段
                return 1
        else:
            return 0

    def sign_in_command(self,rec):
        """
        根据时间判断是否需要签到
        """
        command = input('\n'+'请您先签个到：')
        if command == 'hyb':
            rec.sign_in()
            print('\n签到成功！')
            return self.is_sign_in(rec.sign_in_time)
        if command == 'hyb2':
            rec.sign_in()
            print('\n签到成功！')
            return 2


    def receive_command(self):
        """
        根据时间判断是否需要签到
        """
        command = input('\n'+'请输入指令：')
        return command





    def count_dowm(self, second = 1000):
        """
        倒计时
        :return:
        """
        for i in range(second):
            print('\r'+f'还需等待{second-i}秒', end='')
            time.sleep(1)
        yn = input('\n'+'任务是否完成？（y或者n）：')
        return yn

    def task_aim(self):
        aim = input('\n'+'请输入你的目标：')
        return aim

    def level_up(self,level,reward):
        print(f'--------------------恭喜你成功升级到{level}级\n'
              f'--------------------本次你获得的升级奖励是<{reward}>\n'
              f'--------------------赶紧毕业啊！把家人接过来武汉！\n')

    def day_score(self,dd):
        """
        计算日得分
        :param dd:df_day
        :return:
        """
        weight = np.mat([0.4, 0.3, 0.2, 0.1])
        dd['learn_time'] = dd.learn_time.apply(lambda x:pd.Timedelta(x))
        dd['work_time'] = dd.work_time.apply(lambda x: pd.Timedelta(x))
        dd['stime'] = dd.stime.apply(lambda x: pd.Timedelta(x))
        # 目标日数据
        d_target = dd.iloc[-1,:]
        extra_score = 0
        if '晨跑' in str(d_target.event):
            extra_score = 10
        # 参考日数据
        d_r = dd.iloc[:-1,:]
        # 有效学习时长得分
        lt_score = round(len(d_r[d_r.learn_time <= d_target.learn_time])/len(d_r)*100,2)
        # 在岗时长得分
        wt_score = round(len(d_r[d_r.work_time <= d_target.work_time])/len(d_r)*100,2)
        # 开始时间得分
        st_score = round(len(d_r[d_r.stime >= d_target.stime]) / len(d_r) * 100,2)
        # 任务完成率得分
        cp_score = round(len(d_r[d_r.complete_p <= d_target.complete_p]) / len(d_r) * 100,2)
        # 得分矩阵
        lm = np.mat([[lt_score], [wt_score], [st_score], [cp_score]])
        # 总得分
        score = round(float(weight*lm),2)+extra_score
        print(
            '--------今天又是新的一天！打起精神！超越自己吧！\n'
            '--------现在开始报告你昨天的分数情况！\n'
            f'--------你昨天的综合评分是{score}分！\n'
            '-----------------------------------！\n'
            f'--------有效学习时间评分为{lt_score}分\n'
            f'--------在岗学习时间评分为{wt_score}分\n'
            f'--------开始时间评分为{st_score}分\n'
            f'--------任务完成率评分为{cp_score}分\n'
            '--------今天给我冲起来！！\n'
        )




