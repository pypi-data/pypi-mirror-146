import os
import sys
import pandas as pd
from typing import Union, List
from datetime import datetime
from typeguard import typechecked

sys.path.append(os.path.join(*["..", ""]))

from lipschitz.data_loader.interval import Interval

# TODO
    # Test interval is empty, raise error

class IntervalGenerator():
    @typechecked
    def __init__(
        self, 
        method:str, 
        start: Union[int, str, datetime],
        end: Union[int, str, datetime],
        interval_span: Union[int, str, datetime],
        step_size: Union[int, str, datetime],
        **kwargs
    ):
        """Generate intervals for spliting purpose

        Parameters
        ----------
        method : str
            The method to generate intervals. Must be one of {"equal_step_date", "equal_step_idx}
        start : Union[int, str, datetime]
            The starting point of the sample to be splitted
        end : Union[int, str, datetime]
            The ending point of the sample to be splitted
        interval_span : Union[int, str, datetime]
            The length of one interval
        step_size : Union[int, str, datetime]
            The rolling step size

        Raises
        ------
        ValueError
            Valid methods are "equal_step_date", "equal_step_idx"
        """
        valid_methods = {"equal_step_date", "equal_step_idx"}
        if method in valid_methods:
            self.method = method
        else:
            raise ValueError(f"method must be one of {valid_methods}")
        
        if start == end:
            raise ValueError(f"start {start} should not be the same as end {end}")
        
        if isinstance(step_size, str):
            try:
                pd.tseries.frequencies.to_offset(step_size)
            except ValueError:
                raise ValueError(
                    (
                        "Invalid step size. Please follow" 
                        "https://pandas.pydata.org/docs/reference/api/pandas.tseries.offsets.DateOffset.html"
                        "to see valid step size formats"
                    )
                )
        if isinstance(interval_span, str):
            try:
                pd.tseries.frequencies.to_offset(interval_span)
            except ValueError:
                raise ValueError(
                    (
                        "Invalid interval span. Please follow" 
                        "https://pandas.pydata.org/docs/reference/api/pandas.tseries.offsets.DateOffset.html"
                        "to see valid step size formats"
                    )
                )
        self.start = start
        self.end = end
        self.interval_span = interval_span
        self.step_size = step_size

        self.date_format = "%Y-%m-%d"
        valid_keys = {"date_format"}
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))

    def __equal_step_date(self) -> List[Interval]:
        """Create a list of intervals where each interval has span of 
        IntervalGenerator.interval_span. 

        Returns
        -------
        List[Interval]
            A list of Intervals
        """
        last_interval_start = pd.to_datetime(self.end) - pd.Timedelta(self.interval_span)
        interval_start = pd.date_range(
            start=self.start, 
            end=last_interval_start, 
            freq=self.step_size
        )

        interval_end = interval_start + pd.Timedelta(self.interval_span)

        # Format dates
        interval_start = list(interval_start.strftime(self.date_format))
        interval_end = list(interval_end.strftime(self.date_format))

        interval_config = list(zip(interval_start, interval_end))
        interval_list = list(
            map(
                lambda config: Interval(
                    start=config[0], 
                    end=config[1]
                ), 
                interval_config
            )
        )
        return interval_list

    def __equal_step_idx(self):
        last_interval_start = self.end - self.interval_span
        interval_start = list(range(self.start, last_interval_start, self.step_size))
        if interval_start[-1] == last_interval_start:
            interval_start.append(last_interval_start)
        interval_end = list(map(lambda start: start + self.interval_span, interval_start))

        interval_config = list(zip(interval_start, interval_end))
        interval_list = list(
            map(
                lambda config: Interval(
                    start=config[0],
                    end=config[1]
                ),
                interval_config
            )
        )
        return interval_list

    def generate_intervals(self) -> List[Interval]:
        """Generate intervals 

        Returns
        -------
        List[Interval]
            A list of intervals
        
        Examples
        -------
        >>> generator = IntervalGenerator(
                method = "equal_step_date",
                start = "2020-01-01",
                end = "2022-01-01",
                interval_span = "360d",
                step_size = "30d",
                date_format = "%Y-%m-%d"
            )
        >>> window_info = generator.generate_intervals()
        """
        if self.method == "equal_step_date":
            return self.__equal_step_date() 
        elif self.method == "equal_step_idx":
            return self.__equal_step_idx()


