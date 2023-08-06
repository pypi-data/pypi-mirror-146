from abc import abstractmethod, ABC
import os
import copy
import sys

sys.path.append(os.path.join(*["..", ""]))

from lipschitz.data_loader.loader import DataLoader
from lipschitz.data_loader.interval import Interval

class StrategyInterface(ABC):
    """
    StrategyModel is an interface built for all strategies in Lipschitz such as SVM and DecisionTree.
    It will be a standard module for further strategy design and API connection.
    """
    def __init__(self, item_name:str, features: list, target: list, 
        data_loader: DataLoader, **kwargs):
        """
        Strategy Initialization

        Parameters
        ----------
        item_name: str
        features: list
        target: list
        data_loader: TechnicalFeatureDataLoader
            The data_loader object to connect with database
        kwargs:
            Other parameters needed when generating other strategies

        Return
        ------
        A strategy model
        """
        self.item_name = item_name
        self.features = features
        self.target = target
        self.loader = data_loader

    @abstractmethod
    def train(self, interval: Interval = None, num_of_observations: int = None, **kwargs):
        """
        The train function of different strategies. Needed to be implemented in different strategy classes.
        Before training, collecting data from data loader is needed.

        Parameters
        ----------
        interval: Interval
            The date range of selected data. Default is None
        num_of_observations: integer
            The number of data records needed from data_loader. Default is None

        """
        raise NotImplemented

    @abstractmethod
    def predict_prob(self, interval: Interval = None, num_of_observations: int = None, **kwargs):
        """
        The predict with probabilities  of different strategies. Needed to be implemented in different strategy classes
        Return is a list with the probabilities of different decisions.
        Before predicting, collecting data from data loader is needed.

        Parameters
        ----------
        interval: Interval
            The date range of selected data. Default is None
        num_of_observations: integer
            The number of data records needed from data_loader. Default is None
        """
        raise NotImplemented

    @abstractmethod
    def predict_decision(self, interval: Interval = None, num_of_observations: int = None,
                         decision_percentage: float = 0.5, **kwargs):
        """
        The predict with decisions of different strategies. Needed to be implemented in different strategy classes
        Return is a list of decisions decisions.
        Before predicting, collecting data from data loader is needed.

        Parameters
        ----------
        decision_percentage: float
            Probability level when making decision. Default value is 0.5
        interval: Interval
            The date range of selected data. Default is None
        num_of_observations: integer
            The number of data records needed from data_loader. Default is None
        """
        raise NotImplemented

    def load_dataset(self, interval: Interval = None, num_of_observations: int = None):
        """
        Loading data from data loader and split the train/test dataset

        Parameters
        ----------
        interval: Interval
            The date range of selected data. Default is None
        num_of_observations: integer
            The number of data records needed from data_loader. Default is None
        random_state : int
            random seed of the train/test data splitting. Default value is 0

        Return
        ------
        features_data and target_data collected from data loader
        """
        # get data set from data loader
        features_data = self.loader.get(
            column_list=self.features,
            num_of_observations=num_of_observations,
            interval=interval
        )

        target_data = self.loader.get(
            column_list=self.target,
            num_of_observations=num_of_observations,
            interval=interval
        )
        if target_data is None:
            raise ValueError(f"failed to get target data on interval {interval}")
        if features_data is None:
            raise ValueError(f"failed to get features data on interval {interval}")

        if features_data.shape[1] != len(self.features):
            raise ValueError("Number of fields of sample is different")

        if features_data.shape[0] != target_data.shape[0]:
            raise ValueError("Number of collected records is different")

        return features_data, target_data

    def clone(self):
        return copy.deepcopy(self)
