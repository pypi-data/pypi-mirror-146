import os
import sys
import json

sys.path.append(os.path.join(*["..", ""])) 

from lipschitz.data_loader.factor import Factor
from lipschitz.data_loader.loader import DataLoader
from lipschitz.evaluation.backtest import BackTest
from lipschitz.strategies.svm import SVMStrategy

def main(json_setting_file_path):
    # Opening JSON setting file to retrieve settings
    setting = {}
    with open(json_setting_file_path, encoding='utf-8') as json_file:
        setting = json.load(json_file)
    
    # Set up data loader 
    data_loader = DataLoader()
    data_loader.load_csv(
        file_path = os.path.join(*setting["data"]["file_path"]),
        index_column = setting["data"]["date_column_name"]
    )

    # Initialize Strategy
    features = [
        Factor(name="sma_2", column_name="close", method="sma", window_size=2),
        Factor(name="sma_5", column_name="close", method="sma", window_size=5),
    ]
    target = [
        Factor(name="return_sign", column_name="close", method="pct_change_sign")
    ]
    svm = SVMStrategy(
        item_name = setting["data"]["item_name"],
        features=features,
        target=target,
        data_loader = data_loader
    )

    # Back test
    back_test = BackTest(
        strategy = svm,
        data_loader = data_loader,
        pattern = "rolling_window", 
        pattern_config = {
            "start_date": setting["data"]["start_date"],
            "end_date": setting["data"]["end_date"],
            "train_interval_span": setting["data"]["train_interval_span"],
            "test_interval_span": setting["data"]["test_interval_span"],
        },
        result_path=os.path.join(*setting["save_result_to"])
    )
    back_test.execute()

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        main(sys.argv[1])   # pass json setting's file path to main function
    else:
        print("python3 backtest.py {json_setting_file_path}")
