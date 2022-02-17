# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：main.py
@时间：2022/2/2  9:51
@文档说明:主要执行文件
"""
from dialoguecontroller import DialogueController
from saver import Saver
from ranker import Ranker
from engagement import Engagement
from reward import Reward
from record import Record
import random
import time

# 初始化对象
saver = Saver('用户基本数据.txt', '任务清单.txt', '日清单.txt')
df_user = saver.df_user
ranker = Ranker(df_user.loc[0, 'grade'], df_user.loc[0, 'exp'])
dia = DialogueController()
rew = Reward(10)
rec = Record()
# 开场对话
# 前一天的数据
se = saver.df_day.loc[len(saver.df_day)-1]
print(
    '--------今天又是新的一天！打起精神！超越自己吧！\n'
    f'--------昨天你一共进行了{se.n}次遭遇战,一共完成了{se.complete_n}次遭遇战,完成率为{se.complete_p}\n'
    f'--------你昨天的在岗时间一共是{se.work_time}，有效学习时间是{se.learn_time}，时间利用率为{se.time_p}\n'

)
# 获取命令
command = dia.receive_command()
# 命令判断
while(command != 'exit'):
    if command == 's':
        # 开始任务
        # 输入目标
        aim = dia.task_aim()
        en = Engagement(df_user.user[0], aim)
        # 开始倒计时
        yn = dia.count_dowm()
        en.etime = time.strftime('%H:%M:%S',time.localtime(time.time()))

        if yn == 'y':
            # 遭遇战情况
            en.iscomplete = 1
            # 补充随机祝福次数
            rew.frequency += 1
            n = rew.frequency   # 用n来控制双重祝福只作用于下一轮
            # 调用奖励机制
            inc = 1
            while n > 0:
                ran = random.randint(0, 5)
                if ran in [2,4]:
                    rew.blessing_former(ran)
                    inc = rew.get_final_exp(inc)
                    n = n - 1
                else:
                    inc = rew.get_final_exp(inc)
                    rew.blessing_later(ran)
                    n = n - 1
                print(f'--------------------你被幸运点数是{ran+1}，{list(rew.blessing_dic.keys())[ran]}降临到你身上')
            ranker.add_exp(rew.final_exp)
            print(
                f'--------------------你的理财池共有{rew.financial_pool}点经验值\n'
                f'--------------------本次战斗你得到了{rew.final_exp}点经验\n'
                f'--------------------距离升级还差{ranker.exp_limit - ranker.exp}点经验\n'
            )

        if yn == 'n':
            # 调用惩罚机制
            en.iscomplete = 0
            print('继续加油！！别放弃！！！')
        # 存储
        saver.df_user = ranker.to_df(saver.df_user)
        saver.df_task = en.to_df(saver.df_task)
        saver.to_csv()
    if command == 'i':
        rew.get_pre_bless()
        # 查看用户信息
        print(
            f'用户名:{df_user.user[0]}\n'
            f'等级：{df_user.grade[0]}\n'
            f'职业：{df_user.occupation[0]}\n'
            f'经验值：{df_user.exp[0]}\n'
            f'当前祝福：{rew.pre_blessing}\n'
            f'理财池：{rew.financial_pool}\n'
        )
    if command == 'e':
        event = input('\n' + '请输入今天发生的事件：')
        rec.event = event
    # 重新调用
    command = dia.receive_command()
rec.compute_time('任务清单.txt')
saver.df_day = rec.to_df(saver.df_day)
saver.to_day_csv()
print(
    '\n---------准备结束今天的战斗\n'
    f'---------今天你一共进行了{rec.n}次遭遇战,一共完成了{rec.complete_n}次遭遇战,完成率为{rec.complete_p}\n'
    f'---------你的在岗时间一共是{rec.work_time}，有效学习时间是{rec.learn_time}，时间利用率为{rec.time_p}\n'
    '---------明天继续加油！'
)




