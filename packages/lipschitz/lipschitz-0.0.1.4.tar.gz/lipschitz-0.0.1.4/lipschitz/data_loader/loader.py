from lipschitz.data_loader.interval import Interval
from lipschitz.data_loader.utils import get_data_column
import sys
import os
import numpy as np
import pandas as pd
from typing import Union
from datetime import datetime, date

sys.path.append(os.path.join(*["..", ""]))


# TODO:
# Support alerting if the csv ending date is less than interval.end_date


class DataLoader():
    """
    Data_Loader is a class using pandas dataframe as cache.
    Providing basic gathering and preparing data methods to have a smooth API for strategies instance.

    Examples
    --------
    >>> dl = data_loader()
    >>> dl.load_csv(file_path="./sample_data/commodity-daily/A9999_豆一主力合约_2015-01-05_2021-08-13.csv")
    >>> dl.load_pandas(df)
    >>> dl.print()
    >>> dl.get_date_list("2021-08-10","2021-08-12","date")
    >>> dl.get_date_list(1608, 1610,"date")
    >>> result = dl.get(
            column_list=[
                "date",
                "open",
                "close",
                Factor(name="001", method="sma", column_name="close", window_size=2),
                Factor(name="001", method="sma", column_name="close", window_size=5)
            ],
            interval=temp_interval
        )
    """

    def __init__(self, df=None) -> None:
        self.df = None
        if (df != None):
            self.load_pandas(df)

    def load_csv(self, file_path: str, index_column: str=None) -> None:
        """
        Load a comma-separated values (csv) file into this instance.

        Parameters
        ----------
        file_path : str
            The csv file path.
        """
        df = pd.read_csv(file_path)
        if index_column is not None:
            df.index.name = "row_num"
            df = df.reset_index(drop=False).set_index(index_column, drop=False)
        self.load_pandas(df)

    def load_pandas(self, df: pd.DataFrame) -> None:
        """
        Load a pandas dataframe into this instance.

        Parameters
        ----------
        df : pandas.DataFrame
            Load the pandas DataFrame into this instance.
        """
        self.df = df

    def print(self) -> None:
        """
        Print the datasets for debugging purpose.
        Including the index dtype and columns, non-null values and memory usage.
        And print in table format
        """
        print(self.df.info(verbose=True))
        print(self.df)

    def get_row_num_by_date(self, that_date: Union[int, str, datetime], 
        date_column_name: str = "date") -> list:
        """
        Search the index number by date

        Parameters
        ----------
        that_date : Union[int, str, datetime]

        Return
        ------
        int
            index
        """
        if (type(that_date) == int):
            return that_date
        if (type(that_date) == str):
            first_valid_index = self.df.loc[self.df[date_column_name] >= that_date].first_valid_index()
            # Assume unique index
            first_valid_row_num = self.df.index.get_loc(first_valid_index)
            assert isinstance(first_valid_row_num, int)
            return first_valid_row_num
        if (type(that_date) == date):
            first_valid_index = self.df.loc[self.df[date_column_name] >= (that_date).strftime("%Y-%m-%d")].first_valid_index()
            # Assume unique index
            first_valid_row_num = self.df.index.get_loc(first_valid_index)
            assert isinstance(first_valid_row_num, int)
            return first_valid_row_num
        return None

    def get(self, column_list: list, interval: Interval, num_of_observations: int = 0) -> pd.DataFrame:
        """
        Getting pd.DataFrame based on interval's start and end (exclusive)
        Support interval with int, str, date, not supporting datetime yet
        If num_of_observations > 0, the interval will be [end - num_of_observations + 1 , end]

        Parameters
        ----------
        column_list : list of (Factor or str)
        interval : Interval
        num_of_observations : int, default 0
            0 or any invalid num_of_observations : range [interval.start , interval.end]
            >0 : range [interval.end - num_of_observations + 1 , interval.end]
        """
        payload = pd.DataFrame()    # the returning pandas dataframe filtered by date
        end_index = self.get_row_num_by_date(
            that_date=interval.end, 
            date_column_name=interval.datetime_column_name 
        )    
        start_index = None
        if (type(num_of_observations) == int):
            # perform validation to avoid invalid num_of_observations data type
            if (num_of_observations > 0):
                # if num_of_observation > 0
                # start index will be end_index - num_of_observations + 1
                start_index = end_index - num_of_observations + 1
        if (start_index == None):
            # if num_of_observation == 0 or num_of_observation is invalid
            # get the row index based on interval.start
            start_index = self.get_row_num_by_date(
                that_date=interval.start, 
                date_column_name=interval.datetime_column_name
            )
        if ((start_index != None) and (end_index != None)):
            # if start_index and end_index successfully fetched
            # for each element in column_list,
            # fetch, process and append to payload
            for element in column_list:
                payload[str(element)] = get_data_column(
                    data_column=element, 
                    df=self.df, 
                    start_index=start_index, 
                    end_index=end_index
                )
            return payload
        else:
            # start_index or end_index fail to find its index
            return None
