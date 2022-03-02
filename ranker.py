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
    def __init__(self, grade, exp):
        self.grade = grade
        self.occupation = self.get_occupation()
        self.exp = exp
        self.exp_limit = 50 * math.pow(2, grade // 10)

    def add_exp(self, final_exp):
        self.exp += final_exp
        if self.exp >= self.exp_limit:
            self.exp = self.exp - self.exp_limit
            self.grade += 1
            return 1
        return 0

    def get_occupation(self):
        if self.grade // 10 == 0:
            return '新手'
        elif self.grade // 10 == 1:
            return '战士'
        elif self.grade // 10 == 2:
            return '枪战士'
        elif self.grade // 10 == 3:
            return '龙骑士'
        elif self.grade // 10 == 4:
            return '黑骑士'

    def to_df(self,df):
        df.loc[0, 'grade'] = self.grade
        df.loc[0, 'exp'] = self.exp
        df.loc[0, 'occupation'] = self.occupation
        return df




