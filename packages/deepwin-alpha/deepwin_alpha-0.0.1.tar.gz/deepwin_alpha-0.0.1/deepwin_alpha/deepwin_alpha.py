from typing import Dict, List
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
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
        if "buy_cost_fee" in config:
            raise ValueError("you have not set \"buy cost fee\" in config,please use help(AlphaBacktest) to inspect")
        else:
            self._buy_cost_fee=config["buy_cost_fee"]

        if "sell_cost_fee" in config:
            raise ValueError("you have not set \"sell cost fee\" in config,please use help(AlphaBacktest) to inspect")
        else:
            self._sell_cost_fee=config["sell_cost_fee"]
        
        if "principal" in config:
            raise ValueError("you have not set \"principal\" in config,please use help(AlphaBacktest) to inspect")
        else:
            self._principal=config["principal"]
            self._net_value_list=[self._principal]
        self._is_config=True
    def run(self,position_details:pd.DataFrame,open_price:Dict[str,pd.DataFrame],close_price:Dict[str,pd.DataFrame],vwap_price:Dict[str,pd.DataFrame])->List[float]:
        """
        if just want to use close_price,you can input close_price into vwap_price
        """
        self.position_volume=defaultdict(int)
        
        for date in tqdm(position_details):
            stock_list=set(position_details[date].values.tolist())
            open_df=open_price[date].to_dict()
            close_df=close_price[date].to_dict()
            vwap_df=vwap_price[date].to_dict()
            hold_num=len(stock_list)
            average_money=self._net_value_list[-1]/hold_num
            for stock in self.position_volume:
                
                v_p=vwap_df[date]
                if stock not in stock_list:
                    self._principal+=self.position_volume[stock]*v_p
                    del self.position_volume[stock]
                
            for stock in stock_list:
                if stock not in self.position_volume:
                    v_p=vwap_df[date]
                    buy_stock_num=(average_money/v_p)//100*100
                    self.position_volume[stock]+=buy_stock_num
                    self._principal-=buy_stock_num*v_p
            self._net_value=self._principal
            for stock in self.position_volume:
                stock_num=self.position_volume[stock]
                c_p=close_df[stock]
                self._net_value+=c_p*stock_num
            self._net_value_list.append(self._net_value)
        return self._net_value_list

