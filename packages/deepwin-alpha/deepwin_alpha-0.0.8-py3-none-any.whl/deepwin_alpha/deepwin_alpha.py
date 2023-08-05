from typing import Dict, List
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import math
import matplotlib.pyplot as plt
class AlphaBacktest:
    """
    alpha_backtest=AlphaBacktest()
    config={
        "buy_cost_fee":1e-3,
        "sell_cost_fee":1e-3,

    }
    """
    def __init__(self):
        self._buy_cost_fee=None
        self._sell_cost_fee=None
        self._principal=None
        self._is_config=False
    def set_backtest_config(self,config:Dict):
        if "buy_cost_fee" not in config:
            raise ValueError("you have not set \"buy cost fee\" in config,please use help(AlphaBacktest) to inspect")
        else:
            self._buy_cost_fee=config["buy_cost_fee"]

        if "sell_cost_fee" not in config:
            raise ValueError("you have not set \"sell cost fee\" in config,please use help(AlphaBacktest) to inspect")
        else:
            self._sell_cost_fee=config["sell_cost_fee"]
        
        if "principal" not in config:
            raise ValueError("you have not set \"principal\" in config,please use help(AlphaBacktest) to inspect")
        else:
            self._principal=config["principal"]
            self._net_value_list=[self._principal]
        self.position_volume=defaultdict(int)
        self._is_config=True
        self.config=config
    def run(self,position_details:pd.DataFrame,open_price:Dict[str,pd.DataFrame],close_price:Dict[str,pd.DataFrame],vwap_price:Dict[str,pd.DataFrame],index_price:Dict[str,float])->List[float]:
        """
        if just want to use close_price,you can input close_price into vwap_price
        index_price:you should input index close price and index_price ,short volume is same to net_value
        """
        
        date_0=list(position_details.keys())[0]
        for date in tqdm(position_details):
            stock_list=set(position_details[date].values.tolist())
            open_df=open_price[date].to_dict()
            close_df=close_price[date].to_dict()
            vwap_df=vwap_price[date].to_dict()
            hold_num=len(stock_list)
            average_money=self._net_value_list[-1]/hold_num
            date_1=date
            for stock in list(self.position_volume.keys()):
                
                v_p=vwap_df[stock]
                if stock not in stock_list:
                    self._principal+=self.position_volume[stock]*v_p*(1-self._sell_cost_fee)
                    del self.position_volume[stock]
                
            for stock in stock_list:
                if stock not in self.position_volume:
                    v_p=vwap_df[stock]
                    buy_stock_num=(average_money/v_p)//100*100
                    self.position_volume[stock]+=buy_stock_num
                    self._principal-=buy_stock_num*v_p*(1+self._buy_cost_fee)
            self._net_value=self._principal
            
#             print(short_index_return)
            for stock in self.position_volume:
                stock_num=self.position_volume[stock]
                c_p=close_df[stock]

                self._net_value+=c_p*stock_num
            
            self._net_value_list.append(self._net_value)
            date_0=date
        alpha_series=pd.Series(self._net_value_list[1:],index=list(position_details.keys()))

        alpha_series=(alpha_series.pct_change(1)+1).fillna(1)

        index_price:pd.Series=pd.Series(index_price)
        index_price=(index_price.pct_change(1)+1).fillna(1)
        alpha=(1+(alpha_series-index_price)).cumprod()-1
        alpha_series=alpha_series.cumprod()-1
        index_price=index_price.cumprod()-1
        
        self.total_return_df=pd.DataFrame(alpha_series)
        self.total_return_df.columns=["return"]
        self.total_return_df["alpha"]=alpha
        self.total_return_df["index"]=index_price

        return self.total_return_df
    # # 在回测中用到的函数，不需要联网
    def get_risk_index(self,return_se): #输入收益率序列，从0开始

        total_returns = return_se[-1]
        total_an_returns = (1+total_returns)**(250/len(return_se))-1
        #sharpe = (total_an_returns-0.04)/np.std(return_se)
        # 夏普率计算公式： 年化收益/日收益率的标准差/sqrt(250)
        dailyReturn = (return_se[1:]+1).values/(return_se[:-1]+1).values  #求出日收益的标准差
        sharpe = total_an_returns/np.std(dailyReturn)/math.sqrt(250)

        ret = return_se.dropna()
        ret = ret+1
        maxdown_list = []
        for i in range(1,len(ret)):
            low  = min(ret[i:])
            high = max(ret[0:i]) 
            if high>low:
                maxdown_list.append((high-low)/high)
            else:
                maxdown_list.append(0)
        max_drawdown = max(maxdown_list)
        total_returns = str(round(total_returns*100,2))+'%'
        total_an_returns = str(round(total_an_returns*100,2))+'%'
        sharpe = str(round(sharpe,2))
        max_drawdown = str(round(max_drawdown*100,2))+'%'

        return total_returns,total_an_returns,sharpe,max_drawdown
    def summary(self):
        
        summary = pd.DataFrame(index=['总收益','年化收益','夏普率','最大回撤'])
        #     summary['ret'] = get_risk_index(return_all_df['ret'].cumprod()-1)
        summary['alpha']=self.get_risk_index(self.total_return_df["alpha"])
        #     summary['index']=get_risk_index(return_all_df['index'].cumprod()-1)
        summary.drop(index = '总收益',inplace=True)
        summary = summary.T
        #     summary['每日收益'] = (return_all_df).mean()

        # print('\n全阶段内，每次调仓平均交易换手股票百分比为：{}'.format(round(np.mean(tur_list),3)))
        print('=====策略运行时间：{} 至 {}====='.format(str(self.total_return_df["alpha"].index[0])[:10],str(self.total_return_df["alpha"].index[-1])[:10]))
        self.total_return_df.plot(figsize=(10,4))
        # plt.legend(["alpha"])


        # 换手率绘图
        #     tur_list_DF = pd.DataFrame(tur_list)
        #     tur_list_DF.plot.bar(title='Turnover Rate',figsize=(12, 2),legend = '' )

        print(summary)

        
