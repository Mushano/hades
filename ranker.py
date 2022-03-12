# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：ranker.py
@时间：2022/1/24  10:12
@文档说明:
"""
import math

class Ranker:
    """
    @ClassName：Ranker
    @Description：用于输出用户的等级数据
    @Author：wuzhexiaolu
    """
    def __init__(self, grade, exp, money):
        self.grade = grade
        self.occ_list = ['科研小白','科研助手','科研主力','科研狂魔','院士']
        self.occupation = self.get_occupation()
        self.money = money
        self.exp = exp
        self.exp_limit = 50 * math.pow(2, grade // 10)

    def add_exp(self, final_exp):
        """
        添加经验值
        控制是否升级
        :param final_exp: 由前面所计算最终的经验值
        :return: 1表示升级，0表示没升级
        """
        self.exp += final_exp
        if self.exp >= self.exp_limit:
            self.exp = self.exp - self.exp_limit
            self.grade += 1
            return 1
        return 0

    def add_money(self, m):
        """
        添加金钱
        :param final_exp: 由前面所计算最终的经验值
        :return: 1表示升级，0表示没升级
        """
        self.money += m


    def get_occupation(self):
        if self.grade // 10 == 0:
            return self.occ_list[0]
        elif self.grade // 10 == 1:
            return self.occ_list[1]
        elif self.grade // 10 == 2:
            return self.occ_list[2]
        elif self.grade // 10 == 3:
            return self.occ_list[3]
        elif self.grade // 10 == 4:
            return self.occ_list[4]

    def to_df(self,df):
        df.loc[0, 'grade'] = self.grade
        df.loc[0, 'exp'] = self.exp
        df.loc[0, 'occupation'] = self.occupation
        df.loc[0, 'money'] = self.money
        return df




