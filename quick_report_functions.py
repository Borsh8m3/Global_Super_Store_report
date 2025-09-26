# quick_report_functions.py

import pandas as pd

# check shape and unique values
def check_shape(df: pd.DataFrame):
    print("-- Shape --")
    print(df.shape)

def check_uniqevalues(df: pd.DataFrame):
    print("--- Unique records ---")
    print(df.nunique())

def check_duplicates(df: pd.DataFrame):
    print("##################### Duplicates #####################")
    print(df.duplicated().sum())

def check_nulls(df: pd.DataFrame):
    print("--- missing data ---")
    print(df.isnull().sum())

def check_info(df: pd.DataFrame):
    print("##################### DataFrame Info #####################")
    print(df.info())

def quick_stats(df: pd.DataFrame):
    print("##################### Descriptive stats #####################")
    print(df.describe(include="all"))
