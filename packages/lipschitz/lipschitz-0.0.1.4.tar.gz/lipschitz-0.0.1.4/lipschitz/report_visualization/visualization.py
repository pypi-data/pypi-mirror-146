#!/usr/bin/python
#-*- coding: utf-8 -*-

####this module is for visualization

####input: one sequence of returns (from back test)
####item names, a string, to match with indices

####output: charts and tables

###Need to import from back_test.py --> import from path.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy.stats

import reportlab
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# ===========================================================================================
# 设置字体
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont    
pdfmetrics.registerFont(TTFont("SimHei", os.path.dirname(__file__) + "/SimHei.ttf"))
from reportlab.lib import fonts
fonts.addMapping("SimHei", 0, 0, "SimHei")
import copy

# ===========================================================================================

import datetime
import time
import pytz
from pathlib import Path

script_dir = os.path.dirname(__file__)
main_abs_path = Path(script_dir).parent.absolute()
strategies_test_rel_path = "strategies-test"
strategies_test_abs_path = os.path.join(main_abs_path, strategies_test_rel_path)
visualization_path = os.path.join(main_abs_path, "report_visualization")

# ================================================================================================================================ 

# 生成北京时间的当前时间13位时间戳
def get_timestamp():
    t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d %H:%M:%S')
    ts = int(time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))) * 1000
    return ts

# 将13位时间戳转化为datetime数据
def timestamp_to_time(timeNum):
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

# ================================================================================================================================ 

class Visualization(object):
    # 初始化
    def __init__(self, sequence, category, trading_volume, transaction_cost, 
        execution_cost, asset_list, auc_up_df=None, auc_down_df=None, 
        hedging_count_dict=None, diff_dict=None, correlation_frames=None,
        pdf_path=None, pair_trade_info_dict=None):
        super(Visualization, self).__init__()
        self.pdf_path = pdf_path
        ###this is the sequence of returns
        self.sequence = sequence
        ###this is the category of trading product(s) to be matched
        self.category = category
        ###this is the index matched by the category
        self.index = ""
        ###这个是每日的trading volume
        self.trading_volume = trading_volume
        ###这个是每日的交易手续费
        self.transaction_cost = transaction_cost
        ###这个是交易产品的列表
        self.asset_list = asset_list
        self.execution_cost = execution_cost
        ###auc sequence
        self.auc_up_df = auc_up_df
        self.auc_down_df = auc_down_df
        ###hedging dic
        self.hedging_count_dict = hedging_count_dict
        self.diff_dict = diff_dict
        ###correlation of strategies
        self.correlation_frames = correlation_frames
        ###pair trade info dict
        self.pair_trade_info_dict = pair_trade_info_dict
    # 匹配标地资产
    def match_category(self):
        
        # 此处做一个假设，为之后对接做基础
        # self.category的格式为 Product Type -> Market -> Product Name
        # 比如 equity-US-AAPL 或者 commodity-China-Cu
        # 如果commodity是混合产品，则使用相应市场的股票index，比如commodity-China-mixed，则返回equity_SHSZ300 Index
        # self.index的返回值为一个index的名称
        waitlist_equity = {
            "US": "SPX Index",
            "HK": "HSI Index",
            "China": "SHSZ300 Index"
        }

        temp = self.category.split("-")
        if temp[0] == "equity":
            if temp[1] in waitlist_equity:
                self.index = "equity_" + waitlist_equity[temp[1]]
            else:
                self.index = "No Market Matched"
        elif temp[0] == "commodity":
            if temp[2] == "mixed":
                self.index = "equity_" + waitlist_equity[temp[1]]
            else:
                self.index = "commodity_" + temp[1] + " " + temp[2].upper() + " Index"
        else:
            self.index = "No Product Type Matched"
        print("self index is \n")
        print(self.category)
        print(self.index)
        
# ================================================================================================================================ 
        
    # 进行可视化操作
    def visualize(self):
        
        # ============================================================================================================
        
        # 建立pdf文件的基础设置
        
        # 调用模板，创建指定名称的PDF文档
        timing = timestamp_to_time(get_timestamp())
        if self.pdf_path == None:
            name = os.path.join(*[strategies_test_abs_path, self.category + " " + str(timing).replace(":", "-") + ".pdf"])
        else:
            name = self.pdf_path
        doc = SimpleDocTemplate(name, rightMargin = 20, leftMargin = 20, topMargin = 20, bottomMargin = 20)

        # 获得模板表格
        styles = getSampleStyleSheet()
        
        # 设置中文输入格式
        normalStyle = copy.deepcopy(styles["Normal"])
        normalStyle.fontName = "SimHei"
        
        # 初始化内容
        story = []
        
        # 将段落添加到内容中
        story.append(Paragraph("Backtest Report on " + str(timing), styles["Title"]))
        story.append(Spacer(5, 10))
        
        # ============================================================================================================

        # 准备标地资产的数据
        
        # Assumption: Index sequence should be of the form pandas.core.series.Series
        # 此处要设置index数据储存的地址
        # 这里虽然应对了index匹配不到的情况，但尚未在后续代码中处理该事宜
        # 一个处理方法是，若index匹配不到，则在最终构图部分不画出index的图，然后在构图后pdf中加入提示阐述未匹配到index
        # 但目前尚未在代码中落实此处理方法，若真实出现则会报错
        # equity_index_address = script_dir + r"\indice_equity.xlsx"
        # equity_commodity_address = script_dir + r"\indice_commodity.xlsx"
        equity_index_address = "indice_equity.xlsx"
        equity_commodity_address = "indice_commodity.xlsx"
        if self.index == "No Product Type Matched":
            index_temp = "No Product Type Matched"
        elif self.index == "No Market Matched":
            index_temp = "No Market Matched"
        elif self.index == "":
            index_temp = "No Index Matched"
        else:
            index_templist = self.index.split("_")
            if index_templist[0] == "equity":
                try:
                    index_temp = pd.read_excel(equity_index_address, sheet_name = index_templist[1])
                except:
                    path_temp = os.path.join(visualization_path, equity_index_address)
                    #print(path_temp)
                    index_temp = pd.read_excel(path_temp, sheet_name = index_templist[1])
                index_temp["date"] = index_temp["date"].astype(str)
                #print(index_temp["date"], type(index_temp["date"][0]))
                #print(self.sequence.index[0], type(self.sequence.index[0]))
                index_temp.set_index(['date'], inplace = True)
                index_temp = pd.Series(index_temp["index"].values, index = index_temp.index)
                index_temp = index_temp[index_temp.index <= self.sequence.index[-1]]
            elif index_templist[0] == "commodity":
                # 这里用try except的方法来判断所交易产品的对应指数是否存在
                # 目前这里仅考虑了交易单个产品的index匹配问题
                # 若要设计多个产品的综合benchmark，需要考虑到不同期货指数的日期不同
                # 原因包括不同期货的交易时间不同，以及期货指数的记录起终时间不同
                try:
                    index_temp = pd.read_excel(equity_commodity_address, sheet_name = index_templist[1])
                    index_temp["date"] = index_temp["date"].astype(str)
                    index_temp.set_index(['date'], inplace = True)
                    index_temp = pd.Series(index_temp["index"].values, index = index_temp.index)
                    index_temp = index_temp[index_temp.index <= self.sequence.index[-1]]
                except:
                    index_temp = "No Index Matched"
            else:
                index_temp = "No Index Matched"
        
        # 匹配index和实际交易的日期
        target_date = self.sequence.index[0]
        start_point = ""
        for i in index_temp.index:
            if i < target_date:
                start_point = i
            else:
                break
        # 如果这里start_point仍然为""，则说明回测时间段起始点不晚于index数据的起始点，说明index的时间段过短
        # 但在实际操作中，预期不会出现此类现象
        index_index_temp = [start_point]
        index_value_temp = [index_temp[start_point]]
        for i in index_temp.index:
            if i in self.sequence.index:
                index_index_temp.append(i)
                index_value_temp.append(index_temp[i])
        index_temp = pd.Series(index_value_temp, index = index_index_temp)
        
        # 计算index的daily return
        index_daily_return = []
        for j in range(1,len(index_temp)):
            index_daily_return.append(index_temp.iloc[j] / index_temp.iloc[j - 1] - 1)
        index_daily_return = pd.Series(index_daily_return, index = index_temp.index[1:])
        
        # 计算index的cumulative return
        index_cumulative_return = []
        for k in range(len(index_daily_return)):
            if k == 0:
                index_cumulative_return.append(index_daily_return.iloc[0])
            else:
                index_cumulative_return.append((1 + index_cumulative_return[-1]) * (1 + index_daily_return.iloc[k]) - 1)
        index_cumulative_return = pd.Series(index_cumulative_return, index = index_daily_return.index)
        
        # ============================================================================================================

        # 用于判断是否有异常交易日期出现
        # 此处指的异常日期，为，标地产品在当日无交易数据，但策略交易产品在该日却有交易数据的日期
        for date in self.sequence.index:
            # print("date is\n")
            # print(date)
            # print(index_daily_return.index)
            if date not in list(index_daily_return.index):
                print("出现异常交易日期！该日期为：" + date + "。即将进行后续补全操作......")
                # break
            
        # 进行后续补全操作
        temp_fillup_index = self.sequence.index
        temp_fillup_return = []
        for temp_index in temp_fillup_index:
            if temp_index in index_cumulative_return:   # 如果无需补全
                temp_fillup_return.append(index_cumulative_return[temp_index])
            else:   # 如果需要补全，补全方法为该日期前后两天有数据的平均值
                temp_fillup_before = index_cumulative_return[index_cumulative_return.index < temp_index]
                temp_fillup_after = index_cumulative_return[index_cumulative_return.index > temp_index]
                if len(temp_fillup_before) == 0 and len(temp_fillup_after) != 0:
                    temp_fillup_return.append(temp_fillup_after[0])
                elif len(temp_fillup_before) != 0 and len(temp_fillup_after) == 0:
                    temp_fillup_return.append(temp_fillup_before[-1])
                elif len(temp_fillup_before) != 0 and len(temp_fillup_after) != 0:
                    temp_fillup_return.append(temp_fillup_before[-1] * 0.5 + temp_fillup_after[0] * 0.5)
                else:
                    print("后续补全操作出现异常错误！")
        index_cumulative_return = pd.Series(temp_fillup_return, index = temp_fillup_index)
        
        # ============================================================================================================

        # 对每日回报率进行交易费用的调整
        ##先不调整 - Ye
        #self.sequence = self.sequence - self.transaction_cost
        
        # ============================================================================================================

        # 计算累计回报

        # 通过每次回报计算累计回报（加法）
        cumulative_return = []
        for i in self.sequence:
            if len(cumulative_return) == 0:
                cumulative_return.append(i)
            else:
                cumulative_return.append(i + cumulative_return[-1])
        cumulative_return = pd.Series(cumulative_return, index = self.sequence.index)
        print("cr\n",cumulative_return[-1])
        print(np.sum(self.sequence))
        # ============================================================================================================
        
        # Start reporting performance!
        # print("正在生成策略表现报告......")
        # 对于后续的策略表现报告，在适当的地方会提供标地的表现以供比较

        # =======================================================================

        # 输出回测基础信息
        time_period_string = "时间范围：" + self.sequence.index[0] + " --- " + self.sequence.index[-1]
        story.append(Paragraph(time_period_string, normalStyle))
        story.append(Spacer(2, 4))
        product_string = "交易资产：" + "、".join(product for product in self.asset_list)
        story.append(Paragraph(product_string, normalStyle))
        story.append(Spacer(5, 10))
        
        # =======================================================================
        
        # 输出策略收益率
        strategy_cumulative_return = cumulative_return[-1]
        benchmark_cumulative_return = index_cumulative_return[-1]
        cumulative_return_string = "Strategy Cumulative Return: " + format(strategy_cumulative_return * 100, ".4f") + "% (Benchmark Cumulative Return: " + format(benchmark_cumulative_return * 100, ".4f") + "%)"
        story.append(Paragraph(cumulative_return_string, styles["Normal"]))
        story.append(Spacer(2, 4))
        
        # =======================================================================
        
        # 计算年化收益率。此处需要设置每年交易天数
        # 使用几何计算法，通过开根号获得年化收益率
        annual_trading_days = 250
        total_days = len(cumulative_return)
        year_count = total_days / annual_trading_days
        #strategy_annualized_return = pow(1 + cumulative_return[-1], 1 / year_count) - 1
        #benchmark_annualized_return = pow(1 + index_cumulative_return[-1], 1 / year_count) - 1
        strategy_annualized_return = cumulative_return[-1] / year_count
        benchmark_annualized_return = pow(1 + index_cumulative_return[-1], 1 / year_count) - 1
        annualized_return_string = "Strategy Annualized Return: " + format(strategy_annualized_return * 100, ".4f") + "% (Benchmark Annualized Return: " + format(benchmark_annualized_return * 100, ".4f") + "%)"
        story.append(Paragraph(annualized_return_string, styles["Normal"]))
        story.append(Spacer(2, 4))

        # =======================================================================

        # 计算每日平均交易额和交易费用
        average_trading_volume = self.trading_volume.mean()
        average_trading_volume_string = "Daily Average Trading Volume: " + format(average_trading_volume, ".2f")
        story.append(Paragraph(average_trading_volume_string, styles["Normal"]))
        story.append(Spacer(2, 4))
        average_transaction_cost = self.transaction_cost.mean()
        average_transaction_cost_string = "Daily Average Transaction Cost (as a percentage of total capital): " + format(average_transaction_cost * 100, ".4f") + "%"
        story.append(Paragraph(average_transaction_cost_string, styles["Normal"])) 
        story.append(Spacer(2, 4))

        # =======================================================================
                
        # 计算年化交易费用
        total_transaction_cost = self.transaction_cost.sum()
        annualized_transaction_cost = total_transaction_cost / year_count
        annualized_transaction_cost_string = "Annualized Transaction Cost (as a percentage of total capital): " + format(annualized_transaction_cost * 100, ".4f") + "%"
        story.append(Paragraph(annualized_transaction_cost_string, styles["Normal"])) 
        story.append(Spacer(2, 4))

        # =======================================================================

        # 计算年化execution 费用
        total_execution_cost = self.execution_cost.sum()
        annualized_execution_cost = total_execution_cost  / year_count 
        annualized_execution_cost_string = "Annualized execution Cost (as a percentage of total capital): " + format(annualized_execution_cost * 100, ".4f") + "%"
        story.append(Paragraph(annualized_execution_cost_string, styles["Normal"])) 
        story.append(Spacer(2, 4))
        
        # =======================================================================

        # 计算策略波动率。此处波动率由标准差表现
        strategy_volatility = self.sequence.std()
        volatility_string = "Strategy Volativity: " + format(strategy_volatility, ".4f")
        story.append(Paragraph(volatility_string, styles["Normal"]))
        story.append(Spacer(2, 4))

        # =======================================================================

        # 计算夏普比率，此处无风险利率目前预期使用投资时间段初期的无风险利率（有待讨论，是否使用这个时间段中无风险利率的平均值）
        # 此处需要一个无风险利率数据集，从而获得无风险利率具体数值
        # 目前基于罗老师的指导，无风险利率设置为0.04
        # 2022/01/07 Update: In calculation of Sharpe ratio, rf=0.
        rf = 0
        sharpe_ratio = (self.sequence.mean() - rf / annual_trading_days) / (self.sequence.std() + 10**(-6))
        daily_sharpe_string = "Daily-based Strategy Sharpe Ratio: " + format(sharpe_ratio, ".4f")
        story.append(Paragraph(daily_sharpe_string, styles["Normal"]))
        story.append(Spacer(2, 4))
        annualized_sharpe_string = "Annualized Strategy Sharpe Ratio: " + format((annual_trading_days ** 0.5) * sharpe_ratio, ".4f")
        story.append(Paragraph(annualized_sharpe_string, styles["Normal"]))
        story.append(Spacer(2, 4))
        
        # =======================================================================
        
        # 计算胜率与盈利天数
        winning_day = len(self.sequence[self.sequence > 0])
        winning_day_string = "Winning Days: " + str(winning_day)
        story.append(Paragraph(winning_day_string, styles["Normal"]))
        story.append(Spacer(2, 4))
        winning_rate = len(self.sequence[self.sequence > 0]) / len(self.sequence)
        winning_rate_string = "Winning Rate: " + format(winning_rate * 100, ".4f") + "%"
        story.append(Paragraph(winning_rate_string, styles["Normal"]))
        story.append(Spacer(2, 4))

        # =======================================================================

        # 计算最大回撤率
        print("正在计算最大回撤率！")
        max_retrace = 0
        peak = 0
        for i in range(len(cumulative_return)):
            if cumulative_return[i] > peak:
                peak = cumulative_return[i]
            retrace_rate = (1 + cumulative_return[i]) / (1 + peak) - 1
            if retrace_rate < max_retrace:
                max_retrace = retrace_rate
        max_retrace = -max_retrace
        if max_retrace == 0:
            maximum_drawdown_string = "Maximum Drawdown: 0"
        else:
            maximum_drawdown_string = "Maximum Drawdown: " + format(max_retrace * 100, ".4f") + "%"
        story.append(Paragraph(maximum_drawdown_string, styles["Normal"]))
        story.append(Spacer(2, 4))

        # =======================================================================

        # 计算极端回报天数
        # 此处极端回报阈值可以手动调整
        extreme_rate_1 = 0.03
        extreme_1 = len(self.sequence[self.sequence > extreme_rate_1]) + len(self.sequence[self.sequence < -extreme_rate_1])
        extreme_1_string = "PNL Exceed " + str(extreme_rate_1) + " Days: " + str(extreme_1)
        story.append(Paragraph(extreme_1_string, styles["Normal"]))
        story.append(Spacer(2, 4))

        extreme_rate_2 = 0.05
        extreme_2 = len(self.sequence[self.sequence > extreme_rate_2]) + len(self.sequence[self.sequence < -extreme_rate_2])
        extreme_2_string = "PNL Exceed " + str(extreme_rate_2) + " Days: " + str(extreme_2)
        story.append(Paragraph(extreme_2_string, styles["Normal"]))
        story.append(Spacer(10, 20))

        # ===============================================================================================================

        # Start visualizing performance!
        print("正在生成策略表现图像......")
        # 输出各种图像
        figure_generation_starting_time = time.time()
        figure_generation_starting_time = datetime.datetime.fromtimestamp(figure_generation_starting_time).strftime("%Y-%m-%d %H-%M-%S")

        # =======================================================================

        # 输出daily return直方图与正态分布拟合曲线
        
        # 需注意，输出图表中的每个柱体高度是未被归一化的，但面积之和可确定为1，每个柱体的面积即为此区间的pdf
        # 并且由于直方图和正态分布曲线的面积均为1，在同一个图中相当于都rescale到了同一个量级，故蕴含有效信息
        mean = self.sequence.mean() * 100
        std = self.sequence.std() * 100
        n, bins, patches = plt.hist(self.sequence * 100, bins = 200, density = True, color = "blue")
        y = scipy.stats.norm.pdf(bins, mean, std)
        plt.plot(bins, y, "r--")
        plt.xlabel("Daily Return (%)", fontsize = 14)
        plt.ylabel("Probability (divided by bin space)", fontsize = 14)
        plt.title("Daily Return Performance", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.savefig(figure_generation_starting_time + "daily_return.jpg")
        t1 = Image(figure_generation_starting_time + "daily_return.jpg")
        t1._restrictSize(300, 225)
        story.append(t1)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # 输出cumulative return与benchmark折线图
        
        # 进行volatility match
        strategy_std = cumulative_return.std()
        benchmark_std = index_cumulative_return.std()
        factor = benchmark_std / (strategy_std + 10**(-6))
        adjusted_cumulative_return = cumulative_return * factor

        # 落实构图过程
        index_cumulative_return.plot(kind = "line", label = self.index.split("_")[1], color = "b")
        adjusted_cumulative_return.plot(kind = "line", label = "strategy", color = "r")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Cumulative Return", fontsize = 14)
        plt.title("Cumulative Return Performance", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.legend()
        plt.savefig(figure_generation_starting_time + "cumulative_return.jpg")
        t2 = Image(figure_generation_starting_time + "cumulative_return.jpg")
        t2._restrictSize(300, 225)
        story.append(t2)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # 输出Winning Rate的MA折线图
        smoothing_parameter = 20
        temp_winning = []
        for i in range(smoothing_parameter, len(self.sequence)):
            temp_winning_rate = sum(self.sequence[:i].tail(smoothing_parameter) > 0) / smoothing_parameter
            temp_winning.append(temp_winning_rate)
        smoothed_winning_rate = pd.Series(temp_winning, index = self.sequence[smoothing_parameter:].index)
        smoothed_winning_rate.plot(kind = "line", color = "b")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Winning Rate", fontsize = 14)
        plt.title("Winning Rate (MA" + str(smoothing_parameter) + ")", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.savefig(figure_generation_starting_time + "winning_rate.jpg")
        t3 = Image(figure_generation_starting_time + "winning_rate.jpg")
        t3._restrictSize(300, 225)
        story.append(t3)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # 输出Trading Volume的折线图
        smoothing_parameter = 20
        temp_list = []
        for i in range(smoothing_parameter, len(self.trading_volume)):
            temp_list.append(self.trading_volume[:i].tail(20).mean())
        smoothed_trading_volume = pd.Series(temp_list, index = self.trading_volume[smoothing_parameter:].index)
        smoothed_trading_volume.plot(kind = "line", color = "b")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Trading Volume", fontsize = 14)
        plt.title("Trading Volume Trend (MA" + str(smoothing_parameter) + ")", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.savefig(figure_generation_starting_time + "trading_volume.jpg")
        t4 = Image(figure_generation_starting_time + "trading_volume.jpg")
        t4._restrictSize(300, 225)
        story.append(t4)
        story.append(Spacer(5, 10))
        plt.cla()
        
        # =======================================================================
        
        # 输出Transaction Cost的折线图
        smoothing_parameter = 20
        temp_list = []
        for i in range(smoothing_parameter, len(self.transaction_cost)):
            temp_list.append(self.transaction_cost[:i].tail(20).mean())
        smoothed_transaction_cost = pd.Series(temp_list, index = self.transaction_cost[smoothing_parameter:].index)
        smoothed_transaction_cost.plot(kind = "line", color = "b")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Transaction Cost", fontsize = 14)
        plt.title("Transaction Cost Trend (MA" + str(smoothing_parameter) + ")", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.savefig(figure_generation_starting_time + "transaction_cost.jpg")
        t5 = Image(figure_generation_starting_time + "transaction_cost.jpg")
        t5._restrictSize(300, 225)
        story.append(t5)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # 输出cumulative return的一百天rolling-window折线图
        
        # 设置rollling-window的时间窗口
        rolling_window_days_1 = 100
        
        # 计算cumulative return的rolling-window数据
        cumulative_rolling_index = self.sequence[rolling_window_days_1 - 1:].index
        cumulative_return_rolling = {}
        for i in cumulative_rolling_index:
            rolling_temp_daily = self.sequence[self.sequence.index <= i][-rolling_window_days_1:]
            temp_cumulative_return = 0
            for j in rolling_temp_daily:
                temp_cumulative_return = temp_cumulative_return + j
            cumulative_return_rolling[i] = temp_cumulative_return
        cumulative_return_rolling_series = pd.Series(cumulative_return_rolling)
        
        # 落实构图过程
        cumulative_return_rolling_series.plot(kind = "line", label = str(rolling_window_days_1) + " days rolling-window cumulative return")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Cumulative Return", fontsize = 14)
        plt.title("Rolling-window Cumulative Return Performance", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.legend()
        plt.savefig(figure_generation_starting_time + "cumulative_rolling.jpg")
        t6 = Image(figure_generation_starting_time + "cumulative_rolling.jpg")
        t6._restrictSize(300, 225)
        story.append(t6)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # 输出Sharpe ratio的一百天rolling-window折线图
        
        # 设置rollling-window的时间窗口
        rolling_window_days_2 = 100
        
        # 计算sharpe ratio的rolling-window数据
        sharpe_rolling_index = self.sequence[rolling_window_days_2 - 1:].index
        sharpe_ratio_rolling = {}
        for i in sharpe_rolling_index:
            rolling_temp_daily = self.sequence[self.sequence.index <= i][-rolling_window_days_2:]
            try:
                temp_sharpe_ratio = (rolling_temp_daily.mean() - rf / annual_trading_days) / rolling_temp_daily.std() * (annual_trading_days ** 0.5)
            except:
                temp_sharpe_ratio = 0
            sharpe_ratio_rolling[i] = temp_sharpe_ratio
        sharpe_ratio_rolling_series = pd.Series(sharpe_ratio_rolling)
        
        # 落实构图过程
        sharpe_ratio_rolling_series.plot(kind = "line", label = str(rolling_window_days_2) + " days rolling-window sharpe ratio")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Sharpe Ratio", fontsize = 14)
        plt.title("Rolling-window Sharpe Ratio Performance", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.legend()
        plt.savefig(figure_generation_starting_time + "sharpe_rolling.jpg")
        t7 = Image(figure_generation_starting_time + "sharpe_rolling.jpg")
        t7._restrictSize(300, 225)
        story.append(t7)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # 输出maximum drawdown的一百天rolling-window折线图

        # 设置rollling-window的时间窗口
        rolling_window_days_3 = 100
        
        # 计算maximum drawdown的rolling-window数据
        drawdown_rolling_index = self.sequence[rolling_window_days_3 - 1:].index
        maximum_drawdown_rolling = {}
        for i in drawdown_rolling_index:
            rolling_temp_daily = self.sequence[self.sequence.index <= i][-rolling_window_days_3:]
            # 计算当前窗口累计收益率
            rolling_temp_cumulative = []
            for ii in rolling_temp_daily:
                if len(rolling_temp_cumulative) == 0:
                    rolling_temp_cumulative.append(ii)
                else:
                    rolling_temp_cumulative.append(rolling_temp_cumulative[-1] + ii)
            rolling_temp_cumulative = pd.Series(rolling_temp_cumulative, index = rolling_temp_daily.index)
            # 计算当前窗口最大回撤
            temp_maximum_dropdown = 0
            for j in range(len(rolling_temp_cumulative)):
                for k in range(j, len(rolling_temp_cumulative)):
                    temp_retrace_rate = (1 + rolling_temp_cumulative[k]) / (1 + rolling_temp_cumulative[j]) - 1
                    if temp_retrace_rate < temp_maximum_dropdown:
                        temp_maximum_dropdown = temp_retrace_rate
            temp_maximum_dropdown = -temp_maximum_dropdown
            maximum_drawdown_rolling[i] = temp_maximum_dropdown
        maximum_drawdown_rolling_series = pd.Series(maximum_drawdown_rolling)
        
        # 落实构图过程
        maximum_drawdown_rolling_series.plot(kind = "line", label = str(rolling_window_days_3) + " days rolling-window maximum drawdown")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
        plt.grid()
        ax = plt.gca()
        ax.spines["bottom"].set_position(("data", 0))
        plt.xlabel("Date", fontsize = 14)
        plt.xticks(fontsize = 7)
        plt.ylabel("Maximum Drawdown", fontsize = 14)
        plt.title("Rolling-window Maximum Drawdown Performance", fontsize = 18)
        plt.rcParams["savefig.dpi"] = 300
        plt.legend()
        plt.savefig(figure_generation_starting_time + "drawdown_rolling.jpg")
        t8 = Image(figure_generation_starting_time + "drawdown_rolling.jpg")
        t8._restrictSize(300, 225)
        story.append(t8)
        story.append(Spacer(5, 10))
        plt.cla()

        # =======================================================================

        # Output heatmap of auc score

        if isinstance(self.auc_up_df, pd.DataFrame):
            plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
            plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
            rng = sns.diverging_palette(240, 10, n = 20)
            ax = sns.heatmap(self.auc_up_df, annot = True, cmap = rng, vmin = 0, vmax = 1)
            ax.figure.tight_layout()
            plt.title("AUC up", fontsize = 12)
            plt.savefig(figure_generation_starting_time + "auc_up.jpg")
            t9 = Image(figure_generation_starting_time + "auc_up.jpg")
            t9._restrictSize(300,225)
            story.append(t9)
            story.append(Spacer(5,10))
            plt.cla()
            plt.close()

        if isinstance(self.auc_down_df, pd.DataFrame):
            plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
            plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
            rng = sns.diverging_palette(240, 10, n = 20)
            ax = sns.heatmap(self.auc_down_df, annot = True, cmap = rng, vmin = 0, vmax = 1)
            ax.figure.tight_layout()
            plt.title("AUC down", fontsize = 12)
            plt.savefig(figure_generation_starting_time + "auc_down.jpg")
            t10 = Image(figure_generation_starting_time + "auc_down.jpg")
            t10._restrictSize(300,225)
            story.append(t10)
            story.append(Spacer(5,10))
            plt.cla()
            plt.close()
            

        # =======================================================================

        # Output hedging information

        if (isinstance(self.hedging_count_dict, dict)) and (bool(self.hedging_count_dict)):
            plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
            plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
            names = list(self.hedging_count_dict.keys())
            r = list(range(len(names)))
            temp_df = pd.DataFrame(self.hedging_count_dict)
            missing_opportunities_count = list(temp_df.iloc[0])
            no_effects_count = list(temp_df.iloc[1])
            hedging_success_count = list(temp_df.iloc[2])

            bars = np.add(missing_opportunities_count, no_effects_count).tolist()
            plt.bar(r, missing_opportunities_count, color='#5E96E9', edgecolor='white', label = "missed")
            plt.bar(r, no_effects_count, bottom = missing_opportunities_count, color='#999999', edgecolor='white', label = "no effect")
            plt.bar(r, hedging_success_count, bottom = bars, color='#E17979', edgecolor='white', label = "success")
            plt.xticks(r, names, rotation=90)
            plt.tight_layout()
            plt.title("hedging outcome count by category", fontsize = 12)
            plt.legend()
            plt.savefig(figure_generation_starting_time + "hedging_count.jpg")
            t11 = Image(figure_generation_starting_time + "hedging_count.jpg")
            t11._restrictSize(300, 225)
            story.append(t11)
            story.append(Spacer(5, 10))
            plt.cla()
            plt.close()

        if (isinstance(self.diff_dict, dict)) and (bool(self.diff_dict)):
            plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
            plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
            names = list(self.diff_dict.keys())
            for name in names:
                full_seq_diff_ts = self.diff_dict[name][0]
                hedging_diff = self.diff_dict[name][1]
                fig, (axs1, axs2) = plt.subplots(1,2)
                fig.suptitle(name)
                axs1.plot(full_seq_diff_ts)
                axs1.set_xticks(full_seq_diff_ts.index[::90])
                axs2.hist([i*100 for i in hedging_diff], bins = 200, density = True, color = "blue")
                axs2.axvline(np.mean([i*100 for i in hedging_diff]), color='r', linestyle='dashed', linewidth=1)
                min_ylim, max_ylim = axs2.get_ylim()
                axs2.text(np.mean([i*100 for i in hedging_diff])*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(np.mean([i*100 for i in hedging_diff])))
                axs2.set_xlabel("Hedged Return - Unhedged Return (%)")
                plt.setp(axs1.get_xticklabels(), rotation=90)
                plt.tight_layout()
                plt.savefig(figure_generation_starting_time + "hedging_info_" + name + ".jpg")
                t = Image(figure_generation_starting_time + "hedging_info_" + name + ".jpg")
                t._restrictSize(300, 225)
                story.append(t)
                story.append(Spacer(5, 10))
                plt.cla()
                plt.close()
        
        # =======================================================================

        # Output pair trade plots
        if (isinstance(self.pair_trade_info_dict, dict)):
            num_of_pairs = len(self.pair_trade_info_dict["asset_1"])
            for i in range(num_of_pairs):
                window_test_start = self.pair_trade_info_dict["window_test_start"][i]
                window_test_start_string = "Window test start: " + str(window_test_start)
                story.append(Paragraph(window_test_start_string, styles["Normal"]))
                story.append(Spacer(2, 4))
                
                window_test_end = self.pair_trade_info_dict["window_test_end"][i]
                window_test_end_string = "Window test start: " + str(window_test_end)
                story.append(Paragraph(window_test_end_string, styles["Normal"]))
                story.append(Spacer(2, 4))
                
                asset1 = self.pair_trade_info_dict["asset_1"][i]
                asset2 = self.pair_trade_info_dict["asset_2"][i]
                pair_string = "Traded pairs: " + asset1 + " & " + asset2
                story.append(Paragraph(pair_string, normalStyle))
                story.append(Spacer(2, 4))            
                
                test_stat = self.pair_trade_info_dict["test_stat"][i]
                test_stat_string = "Augmented Engle Granger Test Stat: " + format(test_stat, ".4f")
                story.append(Paragraph(test_stat_string, styles["Normal"]))
                story.append(Spacer(2, 4))
                
                train_half_life = self.pair_trade_info_dict["train_half_life_info"][i]
                train_half_life_string = "Train half life string: " + format(train_half_life, ".4f")
                story.append(Paragraph(train_half_life_string, styles["Normal"]))
                story.append(Spacer(2, 4))                
                
                test_half_life = self.pair_trade_info_dict["test_half_life_info"][i]
                test_half_life_string = "Test half life string: " + format(test_half_life, ".4f")
                story.append(Paragraph(test_half_life_string, styles["Normal"]))
                story.append(Spacer(2, 4))

                trade_info = self.pair_trade_info_dict["trade_info"][i]
                
                # Plot spreads
                spreads = trade_info[["spread", "mean_spread_kalman", "mean_spread_rolling"]]
                spreads.plot(
                    kind = "line",
                    label = "Spreads Plot",
                    secondary_y = ["mean_spread_kalman"]
                )
                plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
                plt.grid()
                ax = plt.gca()
                ax.spines["bottom"].set_position(("data", 0))
                plt.xlabel("Date", fontsize = 14)
                plt.xticks(fontsize = 7)
                plt.ylabel("Spread", fontsize = 14)
                plt.title("Pair Trade Spreads", fontsize = 18)
                plt.rcParams["savefig.dpi"] = 300
                plt.savefig(figure_generation_starting_time + "spread" + str(i) + ".jpg")
                t = Image(figure_generation_starting_time + "spread" + str(i) + ".jpg")
                t._restrictSize(300, 225)
                story.append(t)
                story.append(Spacer(5, 10))
                plt.cla()
                plt.close()
                
                # Plot trade signals
                spreads = trade_info[["z_score", "num_units"]]
                spreads.plot(
                    kind = "line",
                    label = "Signals Plot",
                    secondary_y = ["num_units"]
                )
                plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
                plt.grid()
                ax = plt.gca()
                ax.spines["bottom"].set_position(("data", 0))
                plt.xlabel("Date", fontsize = 14)
                plt.xticks(fontsize = 7)
                plt.ylabel("Singals", fontsize = 14)
                plt.title("Pair Trade Signals", fontsize = 18)
                plt.rcParams["savefig.dpi"] = 300
                plt.savefig(figure_generation_starting_time + "signal" + str(i) + ".jpg")
                t = Image(figure_generation_starting_time + "signal" + str(i) + ".jpg")
                t._restrictSize(300, 225)
                story.append(t)
                story.append(Spacer(5, 10))
                plt.cla()
                plt.close()
        
        # Output correlation plots
        if (isinstance(self.correlation_frames, dict)):
            window_end_list = list(self.correlation_frames.keys())
            for i in range(len(window_end_list)):
                window_end = window_end_list[i]
                correlation_frame = self.correlation_frames[window_end]
                plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
                plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
                rng = sns.diverging_palette(240, 10, n = 20)
                ax = sns.heatmap(correlation_frame.round(2), annot = True, cmap = rng, vmin = -1, vmax = 1, annot_kws={"fontsize":6})
                ax.figure.tight_layout()
                plt.title(window_end + " Correlation", fontsize = 12)
                plt.savefig(figure_generation_starting_time + window_end + "_correlation_plot.jpg")
                t = Image(figure_generation_starting_time + window_end + "_correlation_plot.jpg")
                t._restrictSize(300,225)
                story.append(t)
                story.append(Spacer(5,10))
                plt.cla()
                plt.close()

        # 将全部内容输出到PDF中，并清除缓存图片文件
        doc.build(story)
        os.remove(figure_generation_starting_time + "daily_return.jpg")
        os.remove(figure_generation_starting_time + "cumulative_return.jpg")
        os.remove(figure_generation_starting_time + "winning_rate.jpg")
        os.remove(figure_generation_starting_time + "trading_volume.jpg")
        os.remove(figure_generation_starting_time + "transaction_cost.jpg")
        os.remove(figure_generation_starting_time + "cumulative_rolling.jpg")
        os.remove(figure_generation_starting_time + "sharpe_rolling.jpg")
        os.remove(figure_generation_starting_time + "drawdown_rolling.jpg")
        if os.path.isfile(figure_generation_starting_time + "auc_up.jpg"):
            os.remove(figure_generation_starting_time + "auc_up.jpg")
        if os.path.isfile(figure_generation_starting_time + "auc_down.jpg"):
            os.remove(figure_generation_starting_time + "auc_down.jpg")
        if os.path.isfile(figure_generation_starting_time + "hedging_count.jpg"):
            os.remove(figure_generation_starting_time + "hedging_count.jpg")
        if isinstance(self.diff_dict, dict):
            for name in list(self.diff_dict.keys()):
                os.remove(figure_generation_starting_time + "hedging_info_" + name + ".jpg")
        if isinstance(self.correlation_frames, dict):
            for window_end in list(self.correlation_frames.keys()):
                os.remove(figure_generation_starting_time + window_end + "_correlation_plot.jpg")
        if isinstance(self.pair_trade_info_dict, dict):
            num_of_pairs = len(self.pair_trade_info_dict["asset_1"])
            for i in range(num_of_pairs):
                os.remove(figure_generation_starting_time + "spread" + str(i) + ".jpg")
                os.remove(figure_generation_starting_time + "signal" + str(i) + ".jpg")
# ================================================================================================================================