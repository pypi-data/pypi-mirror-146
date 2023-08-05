import sys
import time
import numpy as np

sys.path.append("../..\\")

from lipschitz.data_loader.loader import DataLoader
from lipschitz.data_loader.interval import Interval


class DummyStrategy():
    def __init__(self, data_loader:DataLoader=None, train_interval:Interval=None, 
        test_interval:Interval=None):
        self.data_loader = data_loader
        self.train_interval = train_interval
        self.test_interval = test_interval
    
    def train(self):
        print(f"I'm training on interval {self.train_interval}")
        time.sleep(4)

    def test(self):
        print(f"I'm testing on interval {self.test_interval}")
        time.sleep(2)
    
    def exec(self):
        decision = np.random.randint(10)
        print(f"On test interval {self.test_interval}, my decision is {decision}")
        time.sleep(2)
        return decision 

