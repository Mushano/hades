# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：reward.py
@时间：2022/2/2  9:46
@文档说明:负责遭遇战完成后的奖励或者惩罚
"""
import random
import numpy as np
import pandas as pd

class Reward:
    """
    @ClassName：Reward
    @Description：
    @Author：wuzhexiaolu
    """

    def __init__(self, ori_exp, ori_money, sign_in_time, grade, is_sign_in):
        # 计算衰减和增加系数
        self.c = round(pow(1.1,grade - 1),2)
        if is_sign_in == 2:
            self.f = 1
        else:
            self.f = self.get_f(sign_in_time)

        # 计算经验值
        self.ori_exp = round(ori_exp * self.f,2)
        self.ori_money = round(ori_money * self.c * self.f,2)
        self.final_exp = 0
        self.financial_pool = 0
        self.pre_blessing = []
        self.blessing_dic = {'经验祝福': 0,
                             '时间祝福': 0,
                             '移除祝福': 0,
                             '翻倍祝福': 0,
                             '理财祝福': 0,
                             '双重祝福': 0}
        # 奖励次数
        self.frequency = 0



    def get_f(self,t):
        """
        经验值和金钱的衰减系数
        :return:
        """
        t_hms = pd.Timestamp(t.strftime('%H:%M:%S'))
        limit1 = pd.Timestamp('08:30:00')
        # 时段的签到开始时间和签到结束时间
        limit2_1 = pd.Timestamp('12:30:00')
        limit2_2 = pd.Timestamp('14:00:00')
        limit3_1 = pd.Timestamp('18:00:00')
        limit3_2 = pd.Timestamp('19:00:00')
        if (t_hms < limit2_1) & (t_hms > limit1):
            # 早上时段
            d = (t_hms - limit1)/pd.Timedelta('01:00:00')
            normal = np.random.normal(loc =0.0 , scale= 0.1,size = 1)[0]
            return  np.round(np.exp(-(d+normal)),2)

        elif (t_hms < limit3_1) & (t_hms > limit2_2):
            # 下午时段
            d = (t_hms - limit2_2) / pd.Timedelta('01:00:00')
            normal = np.random.normal(loc=0.0, scale=0.1, size=1)[0]
            return  np.round(np.exp(-(d + normal)), 2)

        elif  (t_hms > limit3_2):

            # 晚上时段
            d = (t_hms - limit3_2) / pd.Timedelta('01:00:00')
            normal = np.random.normal(loc=0.0, scale=0.1, size=1)[0]
            return np.round(np.exp(-(d + normal)), 2)
        else:
            return 1




    def get_final_exp(self,inc):
        """
        得到遭遇战计算最后的经验值
        """
        for k in self.blessing_dic.keys():
            # 根据祝福列表依次计算
            # 存在1及以上的则代入祝福
            v = self.blessing_dic[k]
            extra_exp = 0
            if v == 0:
                continue
            else:
                inc = inc * self.get_bless_inc(k, inc)
                self.blessing_dic[k] -=1
                # if self.blessing_dic['理财祝福'] == 0:
                #     extra_exp = self.financial_pool
                #     self.financial_pool = 0
                #     print('执行理财结算')
        pool_exp = (self.financial_pool // 5)+extra_exp
        self.final_exp = round(inc * self.ori_exp + pool_exp,2)
        self.financial_pool = self.financial_pool - pool_exp
        return inc

    def get_bless_inc(self, k, inc):
        '''
        计算每个祝福所产生的经验值增益系数
        :return:
        '''
        # 增益系数， 用来对所有祝福增益的累加
        if k == '经验祝福':
            inc = 1.5
        elif k == '时间祝福':
            inc = 1.3
        elif k == '移除祝福':
            self.financial_pool += round(self.ori_exp*(inc-1),2)
            inc = 1
        elif k == '翻倍祝福':
            inc = 2
        elif k == '理财祝福':
            if self.blessing_dic[k] == 5:
                self.financial_pool += round(inc*1.5*self.ori_exp,2)
            inc = 1
        elif k == '双重祝福':
            if self.financial_pool <= 25:
                self.financial_pool = round(self.financial_pool * 2,2)
            inc = 1
        return inc

    def blessing_former(self, ran):
        bl = ['经验祝福', '时间祝福', '移除祝福',
              '翻倍祝福', '理财祝福', '双重祝福']
        if ran == 2:
            # 移除祝福
            self.blessing_dic[bl[ran]] += 1
        if ran == 4:
            # 理财祝福
            if self.blessing_dic[bl[ran]] == 0:
                self.blessing_dic[bl[ran]] += 5
        self.frequency -= 1

    def blessing_later(self, ran):
        """
        计算之后再祝福的
        :param ran:
        :return:
        """
        bl = ['经验祝福', '时间祝福', '移除祝福',
              '翻倍祝福', '理财祝福', '双重祝福']
        if ran == 0:
            # 经验祝福
            self.blessing_dic[bl[ran]] += 1
        if ran == 1:
            # 时间祝福
            self.blessing_dic[bl[ran]] += 2
        if ran == 3:
            # 翻倍祝福
            self.blessing_dic[bl[ran]] += 1
        if ran == 5:
            # 双重祝福
            self.blessing_dic[bl[ran]] += 1
            self.frequency += 1
        self.frequency -= 1

    def get_pre_bless(self):
        """
        获取当前的祝福
        """
        self.pre_blessing = []
        for k in self.blessing_dic.keys():
            # 根据祝福列表依次计算
            # 存在1及以上的则代入祝福
            v = self.blessing_dic[k]
            if v == 0:
                continue
            else:
                # 存储当前祝福
                self.pre_blessing.append({k:v})

    def get_level_bless(self):
        """
        升级奖励
        :return:
        """
        np.random.seed(0)
        r = {'饭后散步':20
             ,'食堂大亨':30
             ,'小资生活':10
             ,'来集小新':30
             ,'豪华下午茶':20
             ,'购物津贴':20
             ,'开发续命':40}

        res = np.random.choice(list(r.keys()), p=np.array(list(r.values())) / np.array(list(r.values())).sum().ravel())
        return res

