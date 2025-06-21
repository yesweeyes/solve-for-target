import pandas as pd

import src.preprocessing as preprocessing

data = pd.read_excel("data/data.xlsx")
data = preprocessing.preprocess_data(data)
