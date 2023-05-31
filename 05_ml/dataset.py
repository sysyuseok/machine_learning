import pandas as pd
from sklearn.model_selection import train_test_split

def get_boston_dataset(path="data/boston_hosing.csv",test_size=0.25):
    df=pd.read_csv(path)
    X=df.drop(columns="MEDV")
    y=df['MEDV']
    dataset=train_test_split(X,y,test_size=test_size, random_state=0)
    return dataset
