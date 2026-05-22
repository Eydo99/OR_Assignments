import pandas as pd
import numpy as np


def load_and_clean_data(file_path='data/AmesHousing.csv'):

    df=pd.read_csv(file_path)
    df_clean = df[['Gr Liv Area', 'SalePrice']].dropna()

    x=df_clean['Gr Liv Area'].values
    y=df_clean['SalePrice'].values #convert column into array
    return x, y

def normalization(x,y):
    x_mean = np.mean(x)
    x_std = np.std(x)

    x_norm = (x - x_mean) / x_std

    y_mean = np.mean(y)
    y_std = np.std(y)

    y_norm = (y - y_mean) / y_std

    return x_norm, y_norm, x_mean, x_std, y_mean, y_std
