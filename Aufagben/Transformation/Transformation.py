import pandas as pd

dataFrame = pd.read_csv("Aufagben/Transformation/FinancialSample.csv",
                        sep=";",
                        encoding="utf-8-sig")

print(dataFrame.tail(10))