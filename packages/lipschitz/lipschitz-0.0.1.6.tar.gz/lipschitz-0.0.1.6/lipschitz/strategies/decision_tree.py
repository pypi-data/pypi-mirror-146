import os
import sys
from sklearn import tree

sys.path.append(os.path.join("", ""))

from lipschitz.strategies.strategy_interface import StrategyInterface
from lipschitz.data_loader.loader import DataLoader
from lipschitz.data_loader.interval import Interval

class DecisionTreeStrategy(StrategyInterface):
    """
        DecisionTree is an class based on the StrategyModel interface.

        Examples
        --------
        >>> dec_tree = DecisionTree(features=features, target=target, data_loader=loader, min_samples_leaf=1)
        >>> dec_tree.train(interval=train_interval, num_of_observations=train_num_of_observations)
        >>> prediction = dec_tree.predict_prob(interval=test_interval, num_of_observations=test_num_of_observations)
        """
    def __init__(self, item_name:str, features: list, target: list, 
        data_loader: DataLoader, min_samples_leaf: int = 1, **kwargs):
        super().__init__(
            item_name = item_name,
            features=features, 
            target=target, 
            data_loader=data_loader, 
            **kwargs
        )
        self.model = tree.DecisionTreeClassifier(min_samples_leaf)

    def train(self, interval: Interval = None, num_of_observations: int = None, **kwargs):
        features_data, target_data = self.load_dataset(interval=interval, num_of_observations=num_of_observations)
        self.model.fit(features_data.values, target_data)

    def predict_prob(self, interval: Interval = None, num_of_observations: int = None, **kwargs):

        features_data, target_data = self.load_dataset(interval=interval, num_of_observations=num_of_observations)
        predict_result = self.model.predict_proba(features_data.values)
        return predict_result

    def predict_decision(self, interval: Interval = None, num_of_observations: int = None,
                         decision_percentage: float = 0.5, **kwargs):
        features_data, target_data = self.load_dataset(interval=interval, num_of_observations=num_of_observations)
        predict_prob = self.model.predict_proba(features_data.values)
        predict_result = self.model.predict(features_data.values)

        # change the result according to the decision percentage level
        for i in range(0, len(predict_result)):
            if predict_prob[i][0] < decision_percentage and predict_prob[i][0] > (1 - decision_percentage):
                predict_result[i] = 0
        print(
            f"I'm testing on interval {interval}. I have made {len(predict_result)} decisions. My decision is {predict_result}")
        return predict_result


