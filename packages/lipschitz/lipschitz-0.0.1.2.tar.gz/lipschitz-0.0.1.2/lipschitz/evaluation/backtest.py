import os
import sys
import concurrent.futures
import pandas as pd
from typing import Any
from typeguard import typechecked

sys.path.append(os.path.join(*["..", ""]))

from lipschitz.data_loader.interval_generator import Interval, IntervalGenerator

# TODO:
    # Multi item test
    # Save back test results
    # decorator

class BackTest(object):
    @typechecked
    def __init__(
        self, 
        strategy:Any, 
        pattern:str,
        pattern_config:dict,
        **kwargs
    ) -> None:
        super().__init__()
        
        allowed_patterns = {"rolling_window"}
        if pattern in allowed_patterns:
            self.pattern = pattern
        else:
            raise ValueError(f"Invalid pattern. Must be one of {allowed_patterns}")

        self.strategy = strategy 
        self.pattern_config = pattern_config

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
            print(train_intervals)
            print(test_intervals)
            raise ValueError((
                f"Length of train_intervals {len(train_intervals)} doesn't match"
                f"with length of test_intervals {len(test_intervals)}"
            ))

        task_list = [
            {
                "train_interval": train_intervals[i],
                "test_interval": test_intervals[i],
            }
                for i in range(len(train_intervals))
        ]
        
        # Distribute workload to workers(processes)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # the return value from worker will send back to master(main) and saved in result
            backtest_results = executor.map(
                self.one_window_backtest_wrapper,
                task_list
            )
        for result in backtest_results:
            print(result)

    def execute(self):
        if self.pattern == "rolling_window":
            self.rolling_window_backtest()