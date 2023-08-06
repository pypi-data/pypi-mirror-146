import os
import sys
import concurrent.futures
import numpy as np
import pandas as pd
from typing import Any
from typeguard import typechecked

sys.path.append(os.path.join(*["..", ""]))

from lipschitz.data_loader.loader import DataLoader
from lipschitz.data_loader.interval_generator import Interval, IntervalGenerator
from lipschitz.data_loader.factor import Factor
from lipschitz.evaluation.transaction_cost import transaction_cost_table
from lipschitz.evaluation.execution_cost import execution_cost_table
from lipschitz.report_visualization.visualization import Visualization

# TODO:
    # Multi item test
    # Save back test results
    # decorator

class BackTest(object):
    @typechecked
    def __init__(
        self, 
        data_loader: DataLoader,
        strategy:Any, 
        pattern:str,
        pattern_config:dict,
        result_path:str,
        **kwargs
    ) -> None:
        super().__init__()
        
        allowed_patterns = {"rolling_window"}
        if pattern in allowed_patterns:
            self.pattern = pattern
        else:
            raise ValueError(f"Invalid pattern. Must be one of {allowed_patterns}")

        self.strategy = strategy 
        self.loader = data_loader
        self.result_path = result_path
        self.pattern_config = pattern_config
        self.transaction_cost_table = transaction_cost_table
        self.execution_cost_table = execution_cost_table

        valid_keys = []
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
    
    def one_window_backtest(self, train_interval:Interval, test_interval:Interval,
        **kwargs):
        strategy = self.strategy.clone()
        strategy.train(interval=train_interval)
        decision = strategy.predict_decision(interval=test_interval)
        return decision
    
    def one_window_backtest_wrapper(self, kwargs):
        return self.one_window_backtest(**kwargs)
    
    def rolling_window_backtest(self):
        config_required_keys = {
            "start_date", 
            "end_date", 
            "train_interval_span", 
            "test_interval_span"
        }
        if not config_required_keys.issubset(self.pattern_config):
            raise ValueError(f"Simple rolling window config require keys {config_required_keys}")
        
        # Prepare a list of parameters needed by self.one_window_backtest_wrapper
        train_start = self.pattern_config["start_date"]
        train_interval_span = self.pattern_config["train_interval_span"]
        train_step_size = self.pattern_config["test_interval_span"]
        
        test_end = self.pattern_config["end_date"]
        test_interval_span = self.pattern_config["test_interval_span"]
        test_step_size = self.pattern_config["test_interval_span"]

        train_end = pd.to_datetime(test_end) - pd.Timedelta(test_step_size)
        train_end = train_end.strftime("%Y-%m-%d")
        test_start = pd.to_datetime(train_start) + pd.Timedelta(train_interval_span)
        test_start = test_start.strftime("%Y-%m-%d")

        train_interval_generator = IntervalGenerator(
            method = "equal_step_date",
            start = train_start,
            end = train_end,
            interval_span = train_interval_span,
            step_size = train_step_size,
        )
        test_interval_generator = IntervalGenerator(
            method = "equal_step_date",
            start = test_start,
            end = test_end,
            interval_span = test_interval_span,
            step_size = test_step_size
        )
        train_intervals = train_interval_generator.generate_intervals()
        test_intervals = test_interval_generator.generate_intervals()
        if len(train_intervals) != len(test_intervals):
            raise ValueError((
                f"Length of train_intervals {len(train_intervals)} doesn't match"
                f"with length of test_intervals {len(test_intervals)}"
            ))

        # FIXME: Seems that last test interval is missing?
        task_list = [
            {
                "train_interval": train_intervals[i],
                "test_interval": test_intervals[i],
            }
                for i in range(len(train_intervals))
        ]
        
        # Distribute workload to workers(processes)
        decisions = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # the return value from worker will send back to master(main) and saved in result
            backtest_results = executor.map(
                self.one_window_backtest_wrapper,
                task_list
            )
        for result in backtest_results:
            decisions.append(result)
        
        # Aggregate results
        decisions = pd.concat(list(decisions))
        rt = self._decisions_to_return(decisions)
        
        # Calculate costs
        size = self._compute_size(decisions)
        transaction_cost = self._compute_transaction_cost(
            item_name=self.strategy.item_name,
            size_sequence=size
        )
        execution_cost = self._compute_transaction_cost(
            item_name=self.strategy.item_name,
            size_sequence=size
        )
        
        # Visualization
        visualizer = Visualization(
            sequence=rt, 
            category="commodity-China-mixed",
            trading_volume=size,
            transaction_cost=transaction_cost,
            execution_cost=execution_cost,
            asset_list=[self.strategy.item_name],
            pdf_path=self.result_path,
        )
        visualizer.match_category()
        visualizer.visualize()
    
    def execute(self):
        if self.pattern == "rolling_window":
            self.rolling_window_backtest()
    
    def _decisions_to_return(self, decisions:pd.Series):
        # Assume decision is made at the beginning of a trading day
        return_interval = Interval(
            start=decisions.index[0], 
            end=decisions.index[-1] # FIXME: loss of one point here
        )
        target = [
            Factor(name="return", column_name="close", method="pct_change")
        ]
        close_price_pct_change = self.loader.get(
            column_list=target,
            interval=return_interval
        )
        close_price_pct_change = close_price_pct_change["return"]
        rt = close_price_pct_change.multiply(
            decisions.loc[decisions.index[len(decisions.index)-1]]
        )
        return rt

    # ==========================================================================
    # Cost related functions
    def _compute_transaction_cost(self, item_name:str, size_sequence:pd.Series) -> pd.Series:
        key_list = self.transaction_cost_table.keys()
        nondouble_list = ["国债","黄金","锌","天然橡胶","燃料油","铅","不锈钢","线材"]
        for key in key_list:
            if key in item_name:
                ###matched
                for double_item in nondouble_list:
                    ##if need to double:
                    if double_item not in item_name:
                        return self.transaction_cost_table[key]*2 * size_sequence
                ##else no doubling
                return self.transaction_cost_table[key] * size_sequence
        print("transaction cost not found\n", item_name)
        return pd.Series([np.nan]*len(size_sequence.index), index=size_sequence.index)
    
    def _compute_execution_cost(self,item_name:str, size_sequence:pd.Series) -> pd.Series:
        key_list = execution_cost_table.keys()
        for key in key_list:
            if key in item_name:
                return execution_cost_table[key]/4 * size_sequence
        print("bid-ask spread not found\n")
        return pd.Series([np.nan]*len(size_sequence.index), index=size_sequence.index)
    
    def _compute_size(self, decisions:pd.Series):
        return decisions.abs()
