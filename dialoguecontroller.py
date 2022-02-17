# -*- encoding:utf-8 -*-
"""
@作者：武者小路
@文件名：dialoguecontroller.py
@时间：2022/1/24  10:12
@文档说明:
"""
import time
from engagement import Engagement

class DialogueController:
    """
    @ClassName：DialogueController
    @Description：用于控制对话过程
    @Author：wuzhexiaolu
    """

    def receive_command(self):
        """
        接收命令
        """
        command = input('请输入指令：')
        return command

    def count_dowm(self, second = 1500):
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
        aim = input('\n'+'请输入你的遭遇战目标：')
        return aim

