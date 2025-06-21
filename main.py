import pandas as pd

import src.preprocessing as preprocessing
import src.feature_engineering as feature_engineering

def operations():
    """
    Main function to run the preprocessing operations on the dataset.
    """
    # Load and preprocess the data
    data = pd.read_excel("data/data.xlsx")
    preprocess_data = preprocessing.preprocess_data(data)
    preprocess_data.to_csv("data/preprocessed_data.csv", index=False)

    del data  # Clear memory

    feature_data = pd.read_csv("data/preprocessed_data.csv")
    feature_data = feature_engineering.feature_engineering(feature_data)
    feature_data = feature_data.dropna()
    feature_data.to_csv("data/feature_data.csv", index=False)

    del feature_data  # Clear memory


if __name__ == "__main__":
    operations()