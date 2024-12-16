import pandas as pd


def extract() -> pd.DataFrame:
    data = pd.read_csv('src/database/ETL/data/CostOfLivingAndIncome.csv')
    return data


def transform(data: pd.DataFrame) -> pd.DataFrame:

    return data


def load() -> None:
    data = transform(extract())


if __name__ == "__main__":
    data = extract()
    print(data.head())
