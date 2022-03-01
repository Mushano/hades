"""
@文件名：analysis.py
@描述：
@作者：武者小路
@时间：2022/2/28 19:17
@联系方式：wuzhexiaolua
@Copyright：©武汉大学测绘遥感信息工程国家重点实验室UBDR小组
"""
import pandas as pd
import matplotlib.pyplot as plt
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Bar
import datetime
import numpy as np

class Analysis:
    """
    @ClassName：Analysis
    @Description：
    用于基本的数据分析
    @Author：wuzhexiaolu
    """
    def __init__(self,x):
        """
        确定x轴和y轴的对象
        :param x: ('date','week','day','today')中的一个
        :param y:('time','p')
        """
        self.x = x

    def start_plot(self):
        if self.x == 'date':
            self.date_analysis()
        elif self.x == 'week':
            self.week_analysis()
        elif self.x == 'day':
            self.day_analysis()
        elif self.x == 'today':
            self.day_analysis()


    def date_analysis(self):
        """
        用于进行日期的数据分析
        Parameters
        ----------
         file_name: str
            参数a
        Returns
        -------
        result_a : int
            结果a
        """
        file_name = '日清单.txt'
        df = pd.read_csv(file_name)
        df = self.trans_df(df,'date')
        self.plot_line(df['date'],df['work_time'],df['learn_time'])

    def week_analysis(self):
        """
        用于进行星期的数据分析
        Parameters
        ----------
         file_name: str
            参数a
        Returns
        -------
        result_a : int
            结果a
        """
        file_name = '日清单.txt'
        df = pd.read_csv(file_name)
        df = self.trans_df(df,'week')
        self.plot_line(df['week'],df['work_time'], df['learn_time'])


    def day_analysis(self):
        """
        用于进行任务清单的数据分析
        Parameters
        ----------
         : int
            参数a
         : str
            参数b

        Returns
        -------
        result_a : int
            结果a
        """
        file_name = '任务清单.txt'
        df = pd.read_csv(file_name)
        if self.x == 'today':
            df = df[df.date == str(datetime.date.today())]
        df = self.trans_df(df,'day')
        self.plot_day(df)


    def get_week_day(self,week):
        week_day_dict = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五',
            5: '周六',
            6: '周日',
        }
        return week_day_dict[week]

    def trans_df(self,df,s):
        """
        对dataframe的格式进行转换，方便进行数据分析
        提取日期
        提取星期
        提取小时
        Parameters
        ----------
         s: str
            s为{'date','week','hour'}中的一个
        Returns
        -------
        result_a : df
            返回处理完成的dataframe
        """
        if s =='date':
            df['date'] = df.date.apply(lambda x:x[5:])
            df['work_time'] = df.work_time.apply(lambda x:self.time2hour(x))
            df['learn_time'] = df.learn_time.apply(lambda x: self.time2hour(x))

        elif s == 'week':
            df['date'] = pd.to_datetime(df['date'])
            df['week'] = df.date.apply(lambda x:x.weekday())

            df['week'] = df.week.apply(lambda x:self.get_week_day(x))
            df['work_time'] = df.work_time.apply(lambda x: self.time2hour(x))
            df['learn_time'] = df.learn_time.apply(lambda x: self.time2hour(x))
            # 按照week排序
            df['week'] = pd.Categorical(df['week'],['周一','周二','周三','周四','周五','周六','周日'])
            df = df.sort_values('week')

            df = df.groupby('week')[['learn_time','work_time','complete_p','time_p']].agg('mean').reset_index()

            #小数点保留2位
            df = df.round(2)

        elif s=='day':
            # 分箱（早上，下午，晚上）
            df['interval'] = df['stime'].apply(lambda x:int(x[:2]))
            df['interval'] = pd.cut(df['interval'],bins = [6,12,17,23],labels=['早上','下午','晚上'])
            df['stime'] = pd.to_datetime(df['stime'])
            df['etime'] = pd.to_datetime(df['etime'])
            df['time'] = df['etime'] - df['stime']
            df['time'] = df['time'].apply(lambda x:str(x)[7:])
            df['time'] = df.time.apply(lambda x:self.time2hour(x))
            # 排序
            df['interval'] = pd.Categorical(df['interval'], ['早上','下午','晚上'])
            df = df.sort_values('interval')
            # 求均值
            df = df.groupby(['date','interval']).agg({'time':'sum','stime':'min','etime':'max','task':'count','iscomplete':'sum'}).reset_index()
            # 总时间计算
            df = df[df.time>0]
            df['all_time'] = df['etime'] - df['stime']
            df['all_time'] = df['all_time'].apply(lambda x: str(x)[7:])
            df['all_time'] = df.all_time.apply(lambda x: self.time2hour(x))
            # 摸鱼时间计算
            df['my_time'] = df['all_time'] - df['time']
            df['complete_p'] = df['iscomplete']/df['task']
            wm = lambda x: np.average(x, weights=df.loc[x.index, 'task'])
            df = df.groupby('interval')[['time','my_time','all_time','complete_p']].agg(wm).reset_index()
            df['p'] = df['time']/df['all_time']
            df =df.round(2)

        return df



    def time2hour(self,s):
        """
        把时间转化成几点几个小时
        :return:
        """
        l = list(map(int,s.split(':')))
        return round(l[0]+l[1]/60+l[2]/3600,2)




    def plot_line(self, x_axis, y1, y2):
        (
            Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
                .add_xaxis(xaxis_data=x_axis)
                .add_yaxis(
                series_name="在岗时间",
                y_axis=y1,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="平均值")]
                ),
            )
                .add_yaxis(
                series_name="有效时间",
                y_axis=y2,
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="平均值")]
                ),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值"),
                    ]
                ),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="学习情况图", subtitle="日期"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            )
                .render(f"{self.x}_line.html")
        )

    def plot_day(self,df):
        list1 = []
        list2 = []
        for i in range(len(df)):
            list1.append(dict(zip(['value','percent'],[df.iloc[i,1],df.iloc[i,4]])))
            list2.append(dict(zip(['value', 'percent'], [df.iloc[i, 2], round(1.0-df.iloc[i, 4],2)])))

        bar = (
            Bar(init_opts=opts.InitOpts())
                .add_xaxis(list(df['interval']))
                .add_yaxis("有效学习时间", list1, stack="stack1", category_gap="50%", label_opts=True)
                .add_yaxis("摸鱼时间", list2, stack="stack1", category_gap="50%", label_opts=True)
                .set_series_opts(
                label_opts=opts.LabelOpts(
                    position="right",
                    formatter=JsCode(
                        "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                        ),
                    )
                )
                .extend_axis(
                yaxis=opts.AxisOpts(
                    name="完成率",
                    type_="value",
                    min_=0,
                    max_=1,
                    )
                )
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                    is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                ),
                yaxis_opts=opts.AxisOpts(
                    name="小时",
                    type_="value",
                    min_=0,
                    max_=5,
                    axislabel_opts=opts.LabelOpts(formatter="{value} 小时"),
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
        )
        line = (
            Line()
                .add_xaxis(list(df['interval']))
                .add_yaxis(
                series_name="完成率",
                yaxis_index=1,
                y_axis=list(df['complete_p']),
                label_opts=opts.LabelOpts(is_show=True),
                )
        )
        bar.overlap(line).render(f"{self.x}_analysis.html")


a = Analysis('day')
a.start_plot()