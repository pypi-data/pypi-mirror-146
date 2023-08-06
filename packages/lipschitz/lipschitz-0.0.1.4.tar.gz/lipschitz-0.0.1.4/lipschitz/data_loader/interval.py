from dataclasses import dataclass
from typing import Union
from datetime import datetime, date

@dataclass
class Interval():
    start: Union[int, str, date, datetime] = None
    end: Union[int, str, date, datetime] = None
    datetime_column_name = "date"