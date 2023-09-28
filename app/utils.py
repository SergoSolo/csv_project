import pandas as pd


def work_with_data(data: pd.DataFrame, column: str, value: str):
    if value.isdigit():
        return data[data[column] == int(value)]
    return data[data[column] == value]
